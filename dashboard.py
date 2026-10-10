import streamlit as str_platform
import database
import pesapal_core

str_platform.set_page_config(page_title="Ourworthlinks Operations Dashboard", page_icon="🔐", layout="wide")

# 🎨 LUXURY SKIN INJECTION
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0F172A !important; font-family: 'Segoe UI', sans-serif !important; color: #ffffff !important; }
    div.stButton > button { background-color: #D97706 !important; color: white !important; font-weight: bold !important; padding: 12px 24px !important; border-radius: 8px !important; width: 100% !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900; margin-bottom: 0;'>🔐 OURWORTHLINKS OPERATIONS JOPO</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px;'>Administrative Secure Identity Portal & B2B Analytics</p>", unsafe_allow_html=True)
str_platform.write("---")

col_lango1, col_lango2 = str_platform.columns(2)

with col_lango1:
    str_platform.markdown("### 🔑 Kuingia Mfumo (Sign In Admin)")
    chaguo_lango = str_platform.selectbox("Hadhi Yako (Role):", ["Admin", "Premium User"], key="dash_role")
    jina = str_platform.text_input("Jina (Username):", key="dash_user")
    password = str_platform.text_input("Nenosiri (Password):", type="password", key="dash_pass")
    
    if str_platform.button("Thibitisha Kuingia"):
        if database.thibitisha_utambulisho_wa_siri(jina, password, chaguo_lango):
            str_platform.success(f"🔓 Karibu Kiongozi {jina.upper()}!")
            str_platform.write("---")
            str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
            data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
            str_platform.table(data_b2b)
            
            col_b1, col_b2 = str_platform.columns(2)
            with col_b1: str_platform.info("💰 **Total B2B Revenue**\n\nAccumulated: **$1,240.50 USD**")
            with col_b2: str_platform.info("📈 **Traffic Volume**\n\nTotal Words: **620,250 Words**")
        else:
            str_platform.error("🛑 Hitilafu: Data ulizoingiza si sahihi!")

with col_lango2:
    str_platform.markdown("### 📝 Usajili Mpya wa Wateja ($5.00 USD)")
    jina_jipya = str_platform.text_input("Username Mpya:", key="dash_new_user")
    siri_mpya = str_platform.text_input("Password Mpya:", type="password", key="dash_new_pass")
    
    str_platform.write("---")
    njia_malipo = str_platform.radio("Njia ya Malipo:", ["Mobile Money (M-Pesa/Tigo Pesa)", "Kadi ya Benki"], key="dash_pay")
    namba_simu = str_platform.text_input("Namba ya Simu / Kadi:", key="dash_phone")
    
    if str_platform.button("Lipia Kifurushi & Sajili Account"):
        if jina_jipya.strip() != "" and siri_mpya.strip() != "":
            with str_platform.spinner("🧠 Inawasiliana na Lango la Pesapal..."):
                matokeo_p = pesapal_core.anzisha_muamala_wa_pesapal(jina_jipya.strip(), f"{jina_jipya.strip()}@ourworthlinks.com", 5.00)
            if matokeo_p.get("status") == "success":
                str_platform.success("📲 ODA IMESAJILIWA: Lango la malipo limefunguka!")
                str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL]({matokeo_p.get('redirect_url')})")
                database.sajili_mtumiaji_mpya(jina_jipya.strip(), siri_mpya.strip(), "Premium User")
        else:
            str_platform.warning("⚠️ Jaza vigezo vyote kwanza!")

str_platform.write("---")
if str_platform.button("← Rudi Kwenye Portal Kuu ya Kiswahili AI"):
    str_platform.markdown("<meta http-refresh content='0;URL=https://streamlit.app'>", unsafe_allow_html=True)
