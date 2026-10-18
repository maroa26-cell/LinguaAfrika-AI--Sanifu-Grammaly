
import streamlit as str_platform
import sqlite3
import os
import sys
import pandas as pd
import numpy as np
import secrets as py_secrets
import time
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import database
import skin_appearance
import pesapal_core

str_platform.set_page_config(page_title="Ourworthlinks Business - Admin Matrix", layout="wide")
skin_appearance.inject_premium_glassmorphic_skin()

# ------------------------------------------------------------------ #
#  VIGEZO VYA USALAMA
# ------------------------------------------------------------------ #
MAX_LOGIN_ATTEMPTS = 5          # majaribio kabla ya kufungiwa
LOCKOUT_SECONDS = 300           # dakika 5 za kufungiwa
SESSION_TIMEOUT_SECONDS = 900   # dakika 15 bila kazi -> toka
OTP_TTL_SECONDS = 300           # OTP huisha baada ya dakika 5
MAX_OTP_ATTEMPTS = 5              # jaribio la OTP kabla ya lockout
MAX_CSV_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_CSV_ROWS = 20000            # kiwango cha juu cha mistari

# ------------------------------------------------------------------ #
#  HALI YA KIPINDI (session state)
# ------------------------------------------------------------------ #
for _k, _v in {
    "admin_authenticated": False,
    "otp_verified": False,
    "generated_otp": None,
    "otp_email_sent": False,
    "otp_email_reason": "",
    "otp_created_at": 0.0,
    "otp_attempts": 0,
    "login_attempts": 0,
    "lockout_until": 0.0,
    "auth_time": 0.0,
}.items():
    if _k not in str_platform.session_state:
        str_platform.session_state[_k] = _v


def tuma_otp_kwenda_email(otp_code, target_email):
    """\U0001F4E7 Hutuma OTP ya 2FA kwa barua pepe (smtp.gmail.com:587 + TLS).

    Inarudi tuple (ok, sababu):
      - ok:    True ikiwa barua imetumwa; vinginevyo False
      - sababu: 'ok' | 'no_secrets' | 'auth_failed' | 'smtp_error'
    """
    sender_email = (str_platform.secrets.get("EMAIL_SENDER_USER", "") or "").strip()
    sender_password = (str_platform.secrets.get("EMAIL_SENDER_PASSWORD", "") or "").strip()
    smtp_server = (str_platform.secrets.get("SMTP_SERVER", "smtp.gmail.com") or "smtp.gmail.com").strip()
    try:
        smtp_port = int(str_platform.secrets.get("SMTP_PORT", 587) or 587)
    except (TypeError, ValueError):
        return False, "bad_smtp_port"

    # Gmail App Password mara nyingi huonyeshwa ikiwa na nafasi; ziondoe kwa login.
    sender_password = sender_password.replace(" ", "")
    target_email = (target_email or "").strip()

    if not sender_email or not sender_password or not target_email:
        return False, "no_secrets"

    msg = MIMEMultipart()
    msg["From"] = f"Ourworthlinks Business Security <{sender_email}>"
    msg["To"] = target_email
    msg["Subject"] = f"🔒 2FA Verification Code: {otp_code}"
    body = f"""
Hello,

A login attempt was made on the Ourworthlinks Business Management Control Panel.
Your six-digit administrative verification code is:

{otp_code}

This code expires in 5 minutes. If you did not initiate this login, secure your account.

© 2026 Ourworthlinks Autonomous Suite.
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        # Port 465 uses implicit SSL; other configured ports use STARTTLS.
        context = ssl.create_default_context()
        if smtp_port == 465:
            with smtplib.SMTP_SSL(
                smtp_server, smtp_port, timeout=20.0, context=context
            ) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=20.0) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, sender_password)
                server.send_message(msg)
        return True, "ok"
    except smtplib.SMTPAuthenticationError:
        logging.exception("SMTP authentication failed while sending admin OTP.")
        return False, "auth_failed"
    except Exception:
        # Log technical details on the server only; never log credentials or OTP.
        logging.exception("SMTP delivery failed while sending admin OTP.")
        return False, "smtp_error"


def funga_kipindi():
    """Safisha hali ya kipindi (log out)."""
    str_platform.session_state["admin_authenticated"] = False
    str_platform.session_state["otp_verified"] = False
    str_platform.session_state["generated_otp"] = None
    str_platform.session_state["otp_email_sent"] = False
    str_platform.session_state["otp_email_reason"] = ""
    str_platform.session_state["otp_created_at"] = 0.0
    str_platform.session_state["otp_attempts"] = 0
    str_platform.session_state["auth_time"] = 0.0


# ------------------------------------------------------------------ #
#  HATUA YA 1: PASSWORD KUU (+ rate limiting / lockout)
# ------------------------------------------------------------------ #
if not str_platform.session_state["admin_authenticated"]:
    str_platform.markdown("<h2 style='text-align: center; color: #D97706;'>\U0001F510 ADMIN CONTROL GATEWAY - PASSWORD STAGE</h2>", unsafe_allow_html=True)
    col1, col2, col3 = str_platform.columns(3)
    with col2:
        sasa = time.time()
        kufungiwa = str_platform.session_state["lockout_until"] - sasa
        if kufungiwa > 0:
            str_platform.error(f"\U0001F6AB Umefungiwa kwa muda. Jaribu tena baada ya sekunde {int(kufungiwa)}.")
            str_platform.stop()

        adm_user = str_platform.text_input("Admin Username:", key="admin_panel_u")
        adm_pass = str_platform.text_input("Admin Password:", type="password", key="admin_panel_p")
        if str_platform.button("Zindua Uhakiki wa Awali", use_container_width=True):
            admin_user_ok = str_platform.secrets.get("ADMIN_USERNAME", "").strip()
            admin_pass_ok = str_platform.secrets.get("ADMIN_PASSWORD", "").strip()
            ni_sahihi = database.thibitisha_utambulisho_wa_siri(adm_user, adm_pass, "admin")
            if admin_user_ok and admin_pass_ok:
                ni_sahihi = ni_sahihi or (adm_user == admin_user_ok and adm_pass == admin_pass_ok)

            if ni_sahihi:
                str_platform.session_state["admin_authenticated"] = True
                str_platform.session_state["login_attempts"] = 0
                code_generated = str(py_secrets.randbelow(900000) + 100000)
                str_platform.session_state["generated_otp"] = code_generated
                str_platform.session_state["otp_created_at"] = time.time()
                target = (str_platform.secrets.get("ADMIN_OTP_EMAIL", "") or "").strip()
                ok_sent, sababu_sent = tuma_otp_kwenda_email(code_generated, target)
                str_platform.session_state["otp_email_sent"] = ok_sent
                str_platform.session_state["otp_email_reason"] = sababu_sent
                str_platform.rerun()
            else:
                str_platform.session_state["login_attempts"] += 1
                zilizobaki = MAX_LOGIN_ATTEMPTS - str_platform.session_state["login_attempts"]
                if zilizobaki <= 0:
                    str_platform.session_state["lockout_until"] = time.time() + LOCKOUT_SECONDS
                    str_platform.session_state["login_attempts"] = 0
                    str_platform.error(f"\U0001F6AB Majaribio mengi mno! Umefungiwa kwa dakika {LOCKOUT_SECONDS // 60}.")
                else:
                    str_platform.error(f"Mtumiaji au Password si sahihi! (Majaribio {zilizobaki} yamebaki)")
    str_platform.stop()

# ------------------------------------------------------------------ #
#  HATUA YA 2: 2FA (OTP + muda wa kuisha)
# ------------------------------------------------------------------ #
if str_platform.session_state["admin_authenticated"] and not str_platform.session_state["otp_verified"]:
    str_platform.markdown("<h2 style='text-align: center; color: #3B82F6;'>\U0001F510 TWO-FACTOR AUTHENTICATION (2FA SHIELD)</h2>", unsafe_allow_html=True)
    barua_pepe = (str_platform.secrets.get("ADMIN_OTP_EMAIL", "") or "").strip()

    col1, col2, col3 = str_platform.columns(3)
    with col2:
        otp_umri = time.time() - str_platform.session_state["otp_created_at"]
        if otp_umri > OTP_TTL_SECONDS:
            str_platform.error("\u23F0 Nambari ya siri (OTP) imeisha muda. Tafadhali ingia upya.")
            if str_platform.button("Rudi Kuingia"):
                funga_kipindi()
                str_platform.rerun()
            str_platform.stop()

        if not str_platform.session_state["otp_email_sent"]:
            sababu = str_platform.session_state.get("otp_email_reason", "smtp_error")
            if sababu == "no_secrets":
                str_platform.error(
                    "Mipangilio ya barua pepe haijakamilika. Weka EMAIL_SENDER_USER, "
                    "EMAIL_SENDER_PASSWORD, na ADMIN_OTP_EMAIL kwenye Streamlit Secrets."
                )
            elif sababu == "auth_failed":
                str_platform.error(
                    "Gmail imekataa kuingia. Hakikisha unatumia Google App Password, "
                    "si nywila ya kawaida ya Gmail."
                )
            elif sababu == "bad_smtp_port":
                str_platform.error("SMTP_PORT si namba halali. Tumia 587 (STARTTLS) au 465 (SSL), kulingana na mtoa huduma.")
            else:
                str_platform.error(
                    "OTP haikutumwa. Angalia SMTP_SERVER, SMTP_PORT, credentials, na logs za hosting. "
                    "Kwa usalama, mfumo hautaonyesha OTP ya dharura kwenye ukurasa."
                )
            if str_platform.button("Rudia kuingia baada ya kurekebisha email"):
                funga_kipindi()
                str_platform.rerun()
            str_platform.stop()

        str_platform.warning(f"OTP imetumwa kwenye barua pepe ya msimamizi: {barua_pepe}")

        input_otp = str_platform.text_input("Ingiza Nambari ya Siri (6-Digit OTP Code):", max_chars=6, key="otp_input_box")
        if str_platform.button("Thibitisha Utambulisho wa Utawala", use_container_width=True, type="primary"):
            if input_otp.strip() == str_platform.session_state["generated_otp"]:
                str_platform.session_state["otp_verified"] = True
                str_platform.session_state["auth_time"] = time.time()
                str_platform.success("\U0001F513 Utambulisho Umethibitishwa! Karibu Kiongozi.")
                time.sleep(1)
                str_platform.rerun()
            else:
                str_platform.session_state["otp_attempts"] += 1
                zilizobaki_otp = MAX_OTP_ATTEMPTS - str_platform.session_state["otp_attempts"]
                if zilizobaki_otp <= 0:
                    str_platform.session_state["lockout_until"] = time.time() + LOCKOUT_SECONDS
                    funga_kipindi()
                    str_platform.error("Majaribio ya OTP yamezidi. Akaunti imefungwa kwa dakika 5.")
                    str_platform.rerun()
                else:
                    str_platform.error(f"OTP si sahihi. Una majaribio {zilizobaki_otp} yaliyobaki.")

    str_platform.stop()

# ------------------------------------------------------------------ #
#  SESSION TIMEOUT: toka otomatiki baada ya muda bila kazi
# ------------------------------------------------------------------ #
if (time.time() - str_platform.session_state["auth_time"]) > SESSION_TIMEOUT_SECONDS:
    funga_kipindi()
    str_platform.warning("\u23F3 Kipindi chako kimeisha muda kwa usalama. Tafadhali ingia upya.")
    str_platform.rerun()
# sasisha muda wa shughuli ya mwisho
str_platform.session_state["auth_time"] = time.time()

# =====================================================================
# \U0001F451 IDARA YA 3: DASHBOARD YA MAPATO (ADMIN MATRIX VIEW)
# =====================================================================
str_platform.markdown("<h1 style='color: #34D399;'>\U0001F4CA OURWORTHLINKS BUSINESS - MAIN CONTROL RADAR</h1>", unsafe_allow_html=True)
str_platform.write("---")

c1, c2, c3, c4 = str_platform.columns(4)
with c1:
    str_platform.metric(label=" Jumla ya Mapato", value="$1,450.00 USD", delta="+12% Wiki hii")
with c2:
    str_platform.metric(label=" Malipo ya Pesapal Live", value="TZS 2,600,000", delta=" Live Channel Active")
with c3:
    str_platform.metric(label=" Watumiaji wa Premium", value="142 Active", delta="+8 Leo")
with c4:
    str_platform.metric(label=" Freemium Sessions", value="1,105 Users", delta="-3%")

str_platform.write("---")

# ------------------------------------------------------------------ #
#  HAKIKI MALIPO MOJA KWA ORDER TRACKING ID
# ------------------------------------------------------------------ #
str_platform.markdown("### \U0001F50E Hakiki Hali ya Malipo (Order Tracking ID)")
tid_check = str_platform.text_input("Weka Order Tracking ID:", key="admin_tid_check")
if str_platform.button("Hakiki Sasa", key="admin_tid_btn") and tid_check.strip():
    with str_platform.spinner("Inahakiki na Pesapal..."):
        hali = pesapal_core.angalia_hali_ya_malipo(tid_check.strip())
    cc1, cc2, cc3 = str_platform.columns(3)
    cc1.metric("Hali", hali["status_desc"])
    cc2.metric("Kiasi", f"{hali['amount']:,.0f} {hali['currency']}")
    cc3.metric("Ref", str(hali["reference"]))
    if hali.get("raw"):
        str_platform.json(hali["raw"])

str_platform.write("---")

str_platform.markdown("###  Mwenendo wa Shughuli za Mradi na Malipo (Operational Analytics)")
Muda_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Tafsiri Pro', 'Ukaguzi Sarufi', 'Malipo ya Simu']
)
str_platform.line_chart(Muda_data)

str_platform.write("---")

# ------------------------------------------------------------------ #
#  UPAKIAJI WA CSV (pamoja na uthibitishaji wa usalama)
# ------------------------------------------------------------------ #
str_platform.markdown("###  COGNITIVE DATASET INGESTION Mainframe")
uploaded_file = str_platform.file_uploader("Upload Swahili Vocabulary Matrix (CSV Format):", type=["csv"])
if uploaded_file is not None:
    # 1) Thibitisha ukubwa
    if getattr(uploaded_file, "size", 0) > MAX_CSV_BYTES:
        str_platform.error(f"Faili ni kubwa mno (zaidi ya {MAX_CSV_BYTES // (1024*1024)} MB). Punguza kwanza.")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            # 2) Thibitisha idadi ya mistari
            if len(df) > MAX_CSV_ROWS:
                str_platform.error(f"Faili lina mistari mingi mno ({len(df)}). Kiwango cha juu ni {MAX_CSV_ROWS}.")
            # 3) Thibitisha safu zinazohitajika
            elif 'keyword' in df.columns and 'semantic_meaning' in df.columns:
                conn = database.pata_muunganisho_wa_chuma()
                cursor = conn.cursor()
                success_count = 0
                for index_row, row in df.iterrows():
                    kw = str(row['keyword']).strip().lower()
                    mean = str(row['semantic_meaning']).strip()
                    if not kw or not mean:
                        continue
                    try:
                        # Query yenye vigezo (parameterized) - salama dhidi ya SQL injection
                        cursor.execute(
                            "INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)",
                            (kw[:200], mean[:1000]),
                        )
                        success_count += 1
                    except sqlite3.IntegrityError:
                        pass
                conn.commit()
                conn.close()
                str_platform.success(f"Loaded {success_count} terms into the system spinal cord!")
            else:
                str_platform.error("CSV requires 'keyword' and 'semantic_meaning' columns.")
        except Exception as e:
            str_platform.error(f"Anomaly caught: {str(e)}")

if str_platform.button(" Funga Lango la Utawala (Log Out)", type="primary"):
    funga_kipindi()
    str_platform.rerun()
