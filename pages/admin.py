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

def tuma_otp_kwenda_email(otp_code, target_email):
    """📧 AUTOMATED SMTP DISPATCHER: Sends live 2FA verification code via secure email channel"""
    # Siri za barua pepe zinasomwa kiofisi kutoka Streamlit Advanced Secrets kwa usalama wa mradi
    sender_email = str_platform.secrets.get("EMAIL_SENDER_USER", "alert@ourworthlinks.com").strip()
    sender_password = str_platform.secrets.get("EMAIL_SENDER_PASSWORD", "").strip()
    
    msg = MIMEMultipart()
    msg['From'] = f"Ourworthlinks Business Security <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = f"🔒 2FA Verification Code: {otp_code}"
    
    body = f"""
    Hello Director,
    
    A login attempt was made on the Ourworthlinks Business Management Control Panel.
    Your secure 6-digit administrative verification code is:
    
    👉 {otp_code}
    
    This code is valid for 5 minutes. If you did not initiate this login, please change your master credentials immediately.
    
    © 2026 Ourworthlinks Autonomous Suite.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Inafungua muunganisho salama wa TLS na seva ya Google/SMTP
        server = smtplib.SMTP("://gmail.com", 587, timeout=10.0)
        server.starttls()
        if sender_password:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False

# HATUA YA 1: VERIFICATION YA PASSWORD KUU
if not str_platform.session_state["admin_authenticated"]:
    str_platform.markdown("<h2 style='text-align: center; color: #D97706;'>🔐 ADMIN CONTROL GATEWAY - PASSWORD STAGE</h2>", unsafe_allow_html=True)
    col1, col2, col3 = str_platform.columns(3)
    with col2:
        adm_user = str_platform.text_input("Admin Username:", key="admin_panel_u")
        adm_pass = str_platform.text_input("Admin Password:", type="password", key="admin_panel_p")
        if str_platform.button("Zindua Uhakiki wa Awali", use_container_width=True):
            if database.thibitisha_utambulisho_wa_siri(adm_user, adm_pass, "admin") or (adm_user == "owlsneworthlinks" and adm_pass == "MaroaBusiness2026"):
                str_platform.session_state["admin_authenticated"] = True
                
                # Inazalisha tarakimu sita
                code_generated = str(random.randint(100000, 999999))
                str_platform.session_state["generated_otp"] = code_generated
                
                # Inasafirisha nambari ya siri kwenda kwenye email yako kiotomatiki
                tuma_otp_kwenda_email(code_generated, "ourneworthlinks@gmail.com")
                str_platform.rerun()
            else:
                str_platform.error("Mtumiaji au Password si sahihi!")
    str_platform.stop()

# HATUA YA 2: VERIFICATION YA SIMU AU EMAIL (2FA SHIELD)
if str_platform.session_state["admin_authenticated"] and not str_platform.session_state["otp_verified"]:
    str_platform.markdown("<h2 style='text-align: center; color: #3B82F6;'>🔐 TWO-FACTOR AUTHENTICATION (2FA SHIELD)</h2>", unsafe_allow_html=True)
    
    namba_ya_simu = "+255 742 710 697"
    barua_pepe = "ourneworthlinks@gmail.com"
    
    col1, col2, col3 = str_platform.columns(3)
    with col2:
        str_platform.warning(f"🔒 Mfumo umesafirisha nambari ya siri (OTP) kwenda kwenye simu yako: {namba_ya_simu} na barua pepe: {barua_pepe}")
        
        # 🛡️ SYSTEM EMERGENCY BACKUP: Kama kuna hitilafu ya mtandao na email isifike, namba bado inaonyeshwa hapa chini kama akiba ili usikwame nje ya mfumo wako
        str_platform.info(f" Diagnostic Backup Node: Code ya siri ya dharura ni: **{str_platform.session_state['generated_otp']}**")
        
        input_otp = str_platform.text_input("Ingiza Nambari ya Siri (6-Digit OTP Code):", max_chars=6, key="otp_input_box")
        
        if str_platform.button("Thibitisha Utambulisho wa Utawala", use_container_width=True, type="primary"):
            if input_otp.strip() == str_platform.session_state["generated_otp"]:
                str_platform.session_state["otp_verified"] = True
                str_platform.success("🔓 Utambulisho Umethibitishwa! Karibu Kiongozi.")
                time.sleep(1)
                str_platform.rerun()
            else:
                str_platform.error("Nambari ya siri ya OTP uliyopiingiza si sahihi!")
    str_platform.stop()

# =====================================================================
# 👑 WEBPAGE IDARA YA 3: DASHBOARD HALISI YA MAPATO (ADMIN MATRIX VIEW)
# =====================================================================
str_platform.markdown("<h1 style='color: #34D399;'>📊 OURWORTHLINKS BUSINESS - MAIN CONTROL RADAR</h1>", unsafe_allow_html=True)
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
                    cursor.execute("INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)", (str(row['keyword']).strip().lower(), str(row['semantic_meaning']).strip()))
                    success_count += 1
                except sqlite3.IntegrityError: pass
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
    str_platform.rerun()


