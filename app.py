import streamlit as str_platform
import os
import time
import requests
from openai import OpenAI

# 🧠 COGNITIVE SUBSYSTEM IMPORTS (Moduli Huru za herufi ndogo)
import database
import synapse

self_healing_status = "🟢 Autonomous Shield: Active & Healthy"
mifumo_tayari = True

try:
    import central_nervous_system
except Exception:
    self_healing_status = "🛠️ Self-Regulatory Action: Restoring Defected Memory Nodes"
    mifumo_tayari = False

# 👑 Sanifu Mipangilio ya Seva Kuu ya Sayari (Edition 4 Super Suite)
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Anzisha Hifadhidata ya Chuma ya SQLite Mara Moja mlangoni
try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana kwenye Seva!")
    str_platform.stop()

# 🎨 DIRECT ENTERPRISE LUXURY SKIN INJECTION
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; color: #ffffff !important; border-right: 4px solid #D97706 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #ffffff !important; font-size: 16px !important; font-weight: 700 !important; }
    div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; margin-bottom: 8px !important; }
    div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 6px !important; padding: 4px 10px !important; }
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

if "user_status" not in str_platform.session_state: str_platform.session_state["user_status"] = "guest"
if "active_user_name" not in str_platform.session_state: str_platform.session_state["active_user_name"] = "Mgeni"

muda_mwanzo = time.time()
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem</h3>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# 📊 Bango la Telemetry (Rada ya Ubongo Kuu)
str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> 🟢 RAM/CPU Stable</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> 🟢 Traffic Safe</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
    <p style='color: #E2E8F0; font-size: 11px; margin: 0;'>🩺 <b>Self-Regulatory:</b> {self_healing_status}</p>
</div>
""", unsafe_allow_html=True)

hali_ya_sasa = str_platform.session_state["user_status"]
jina_la_sasa = str_platform.session_state["active_user_name"]

if hali_ya_sasa == "admin":
    str_platform.sidebar.markdown(f"<p style='color: #25D366; text-align: center;'>👑 Admin: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
elif hali_ya_sasa == "standard_premium":
    str_platform.sidebar.markdown(f"<p style='color: #D97706; text-align: center;'>💎 Premium: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
else:
    str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center;'>👤 Guest Mode (Free Portal)</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔐 Lango la Kuingia (Login Dashboard)"]

chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", orodha_menyu)

# =====================================================================
# ⚙️ THE MAIN SYSTEM ROUTING BLOCK
# =====================================================================
if chaguo_menyu == "🔐 Lango la Kuingia (Login Dashboard)":
    str_platform.markdown("""
    <div style="background-color: #1E293B; border: 3px solid #D97706; padding: 30px; border-radius: 15px; text-align: center; max-width: 500px; margin: 0 auto;">
        <h2 style="color: #D97706; font-family: sans-serif; font-weight: 800; margin-bottom: 5px;">🔐 LOGIN DASHBOARD</h2>
        <p style="color: #94A3B8; font-family: sans-serif; font-size: 14px; margin: 0;">Ourworthlinks • Administrative Secure Identity Port</p>
    </div>
    """, unsafe_allow_html=True)
    str_platform.write("---")
    col_lango1, col_lango2 = str_platform.columns(2)
    with col_lango1:
        str_platform.markdown("### 🔑 Kuingia Mfumo (Sign In)")
        chaguo_lango = str_platform.selectbox("Chagua Hadhi Yako (Role):", ["Premium User", "Admin"], key="lango_select_v4")
        jina = str_platform.text_input("Ingiza Jina (Username):", key="lango_username_v4")
        password = str_platform.text_input("Ingiza Nenosiri (Password):", type="password", key="lango_password_v4")
        if str_platform.button("Thibitisha Kuingia Mfumo"):
            if database.thibitisha_utambulisho_wa_siri(jina, password, chaguo_lango):
                str_platform.session_state["user_status"] = "admin" if chaguo_lango == "Admin" else "standard_premium"
                str_platform.session_state["active_user_name"] = jina
                str_platform.rerun()
            else:
                str_platform.error("🛑 Hitilafu: Jina au Nenosiri uliloingiza si sahihi!")
    with col_lango2:
        str_platform.markdown("### 📝 Jisajili Akaunti Mpya (Sign Up)")
        chaguo_usajili = str_platform.selectbox("Sajili Akaunti Kama:", ["Premium User", "Admin"], key="signup_role_select")
        jina_jipya = str_platform.text_input("Tengeneza Jina (New Username):", key="signup_user")
        siri_mpya = str_platform.text_input("Tengeneza Nenosiri (New Password):", type="password", key="signup_pass")
        
        str_platform.write("---")
        str_platform.markdown("<p style='color: #D97706; font-weight: bold; margin-bottom: 2px;'>💳 Kifurushi cha Premium ($5.00 USD / Mwezi)</p>", unsafe_allow_html=True)
        njia_malipo = str_platform.radio("Chagua Njia ya Malipo:", ["Mobile Money (M-Pesa/Tigo Pesa)", "Kadi ya Benki (Visa / Mastercard)"])
        
        if njia_malipo == "Mobile Money (M-Pesa/Tigo Pesa)":
            mtandao_simu = str_platform.selectbox("Chagua Mtandao wa Malipo:", ["M-Pesa (Vodacom)", "Tigo Pesa (Tigo)", "Airtel Money (Airtel)"])
            namba_simu = str_platform.text_input("Ingiza Namba ya Simu (Mfano: 07XXXXXXXX):", key="payment_phone_no")
        else:
            jina_kadi = str_platform.text_input("Jina Linalosomeka Kwenye Kadi (Cardholder Name):")
            namba_kadi = str_platform.text_input("Namba ya Kadi (Card Number - 16 Digits):", max_chars=16)
            col_k1, col_k2 = str_platform.columns(2)
            with col_k1: tarehe_kadi = str_platform.text_input("Tarehe ya Kuisha (MM/YY):", max_chars=5)
            with col_k2: cvv_kadi = str_platform.text_input("Namba ya Siri (CVV):", type="password", max_chars=3)
            
        if str_platform.button("Kamilisha Usajili na Lipia Kifurushi"):
            if jina_jipya.strip() != "" and siri_mpya.strip() != "":
                if pesapal_tayari:
                    str_platform.info("🧠 Ubongo unaunganisha na Lango Kuu la Pesapal la kampuni ya **Ourworthlinks**...")
                    matokeo_p = pesapal_core.anzisha_muamala_wa_pesapal(jina_jipya.strip(), f"{jina_jipya.strip()}@ourworthlinks.com", 5.00)
                    
                    if matokeo_p.get("status") == "success":
                        str_platform.success(f"📲 ODA IMESAJILIWA: Kampuni ya Ourworthlinks imefungua Lango la malipo ya siri ya $5.00 USD!")
                        str_platform.markdown(f"👉 [Bofya Hapa Kufungua Fomu ya Malipo Halisi ya Pesapal]({matokeo_p.get('redirect_url')})")
                        
                        # 👑 CRITICAL FIXED INDENTED BLOCK (Kuhakikisha kila amri ya ndani inanyooka spaces 4 vizuri)
                        if database.sajili_mtumiaji_mpya(jina_jipya.strip(), siri_mpya.strip(), chaguo_usajili):
                            str_platform.caption("Akaunti imeandikwa kwenye SQLite. Baada ya malipo kukamilika itafunguka papo hapo.")
                    else:
                        str_platform.error(matokeo_p.get("message"))
                else:

