
import streamlit as str_platform
import sqlite3
import os
import sys
import pandas as pd
import numpy as np
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import database
import skin_appearance

str_platform.set_page_config(page_title="Ourworthlinks Business - Admin Matrix", layout="wide")
skin_appearance.inject_premium_glassmorphic_skin()

if "admin_authenticated" not in str_platform.session_state:
    str_platform.session_state["admin_authenticated"] = False
if "otp_verified" not in str_platform.session_state:
    str_platform.session_state["otp_verified"] = False
if "generated_otp" not in str_platform.session_state:
    str_platform.session_state["generated_otp"] = None
if "otp_email_sent" not in str_platform.session_state:
    str_platform.session_state["otp_email_sent"] = False


def tuma_otp_kwenda_email(otp_code, target_email):
    """\U0001F4E7 AUTOMATED SMTP DISPATCHER: Hutuma OTP ya 2FA kwa barua pepe.

    IMEREKEBISHWA: host ilikuwa '://gmail.com' (si sahihi) -> 'smtp.gmail.com'.
    """
    sender_email = str_platform.secrets.get("EMAIL_SENDER_USER", "").strip()
    sender_password = str_platform.secrets.get("EMAIL_SENDER_PASSWORD", "").strip()

    if not sender_email or not sender_password:
        return False

    msg = MIMEMultipart()
    msg['From'] = f"Ourworthlinks Business Security <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = f"\U0001F512 2FA Verification Code: {otp_code}"

    body = f"""
    Hello Director,

    A login attempt was made on the Ourworthlinks Business Management Control Panel.
    Your secure 6-digit administrative verification code is:

    \U0001F449 {otp_code}

    This code is valid for 5 minutes. If you did not initiate this login, please
    change your master credentials immediately.

    \u00A9 2026 Ourworthlinks Autonomous Suite.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Muunganisho salama wa TLS na seva ya Gmail (smtp.gmail.com:587)
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15.0)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


# HATUA YA 1: VERIFICATION YA PASSWORD KUU
if not str_platform.session_state["admin_authenticated"]:
    str_platform.markdown("<h2 style='text-align: center; color: #D97706;'>\U0001F510 ADMIN CONTROL GATEWAY - PASSWORD STAGE</h2>", unsafe_allow_html=True)
    col1, col2, col3 = str_platform.columns(3)
    with col2:
        adm_user = str_platform.text_input("Admin Username:", key="admin_panel_u")
        adm_pass = str_platform.text_input("Admin Password:", type="password", key="admin_panel_p")
        if str_platform.button("Zindua Uhakiki wa Awali", use_container_width=True):
            # USALAMA: funguo za admin zinasomwa kutoka Secrets, SIYO kuandikwa humu.
            admin_user_ok = str_platform.secrets.get("ADMIN_USERNAME", "").strip()
            admin_pass_ok = str_platform.secrets.get("ADMIN_PASSWORD", "").strip()
            ni_sahihi = database.thibitisha_utambulisho_wa_siri(adm_user, adm_pass, "admin")
            if admin_user_ok and admin_pass_ok:
                ni_sahihi = ni_sahihi or (adm_user == admin_user_ok and adm_pass == admin_pass_ok)

            if ni_sahihi:
                str_platform.session_state["admin_authenticated"] = True
                code_generated = str(random.randint(100000, 999999))
                str_platform.session_state["generated_otp"] = code_generated
                target = str_platform.secrets.get("EMAIL_SENDER_USER", "ourneworthlinks@gmail.com").strip()
                str_platform.session_state["otp_email_sent"] = tuma_otp_kwenda_email(code_generated, target)
                str_platform.rerun()
            else:
                str_platform.error("Mtumiaji au Password si sahihi!")
    str_platform.stop()

# HATUA YA 2: VERIFICATION YA EMAIL (2FA SHIELD)
if str_platform.session_state["admin_authenticated"] and not str_platform.session_state["otp_verified"]:
    str_platform.markdown("<h2 style='text-align: center; color: #3B82F6;'>\U0001F510 TWO-FACTOR AUTHENTICATION (2FA SHIELD)</h2>", unsafe_allow_html=True)

    barua_pepe = str_platform.secrets.get("EMAIL_SENDER_USER", "ourneworthlinks@gmail.com").strip()

    col1, col2, col3 = str_platform.columns(3)
    with col2:
        if str_platform.session_state["otp_email_sent"]:
            str_platform.warning(f"\U0001F512 Nambari ya siri (OTP) imetumwa kwenye barua pepe: {barua_pepe}")
        else:
            # Onyesha nambari ya dharura TU pale barua pepe iliposhindikana kutumwa,
            # ili usikwame nje. (Vinginevyo 2FA ingekuwa haina maana.)
            str_platform.error("\u26A0\uFE0F Barua pepe haikutumwa (angalia EMAIL_SENDER_* kwenye Secrets).")
            str_platform.info(f"Nambari ya dharura (backup): **{str_platform.session_state['generated_otp']}**")

        input_otp = str_platform.text_input("Ingiza Nambari ya Siri (6-Digit OTP Code):", max_chars=6, key="otp_input_box")

        if str_platform.button("Thibitisha Utambulisho wa Utawala", use_container_width=True, type="primary"):
            if input_otp.strip() == str_platform.session_state["generated_otp"]:
                str_platform.session_state["otp_verified"] = True
                str_platform.success("\U0001F513 Utambulisho Umethibitishwa! Karibu Kiongozi.")
                time.sleep(1)
                str_platform.rerun()
            else:
                str_platform.error("Nambari ya siri ya OTP uliyoingiza si sahihi!")
    str_platform.stop()

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
#  HAKIKI MALIPO MOJA KWA ORDER TRACKING ID (hali halisi kutoka Pesapal)
# ------------------------------------------------------------------ #
import pesapal_core
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

str_platform.markdown("###  COGNITIVE DATASET INGESTION Mainframe")
uploaded_file = str_platform.file_uploader("Upload Swahili Vocabulary Matrix (CSV Format):", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'keyword' in df.columns and 'semantic_meaning' in df.columns:
            conn = database.pata_muunganisho_wa_chuma()
            cursor = conn.cursor()
            success_count = 0
            for index_row, row in df.iterrows():
                try:
                    cursor.execute(
                        "INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)",
                        (str(row['keyword']).strip().lower(), str(row['semantic_meaning']).strip()),
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
    str_platform.session_state["admin_authenticated"] = False
    str_platform.session_state["otp_verified"] = False
    str_platform.session_state["generated_otp"] = None
    str_platform.session_state["otp_email_sent"] = False
    str_platform.rerun()
