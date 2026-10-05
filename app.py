import streamlit as str_platform
import os
from openai import OpenAI

# 🧠 KUVIKARIBA MAFAILI TANZU KAMA UBONGOLANZI (MICROSERVICES CALL)
import validate_entries
import errorfix
import admin
import sauti
import robot

# 👑 Sanifu Mipangilio ya Master Machine File
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Master Control Core",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 KUUNGANISHA NA SYSTEM SECRET KEY
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana kwenye seva!")
    str_platform.stop()

# 🎨 DESIGN CODES (EDITION 4 ENTERPRISE GOLD SKIN)
str_platform.markdown("""<style>html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }[data-testid="stSidebar"] { background-color: #0F172A !important; border-right: 4px solid #D97706 !important; }[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #ffffff !important; font-weight: 700; }div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; margin-bottom: 8px !important; }div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 4px; }</style>""", unsafe_allow_html=True)

if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Decentralized Master Machine • Edition 4 Suite</h3>", unsafe_allow_html=True)
str_platform.write("---")

# 🧭 SIDEBAR NAVIGATION CONTROLLER
if str_platform.session_state["user_status"] == "admin":
    chaguo_menyu = str_platform.sidebar.radio("DASHBOARD YA USIMAMIZI:", ["📊 Ripoti Kuu ya Utendaji", "🚪 Toka Kwenye Mfumo (Logout)"])
else:
    if str_platform.session_state["user_status"] == "standard_premium":
        str_platform.sidebar.markdown("<p style='color: #D97706; text-align: center;'>💎 Premium Member (Unlocked)</p>", unsafe_allow_html=True)
    else:
        str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center;'>👤 Guest Mode (Free Portal)</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio("CHAGUA HUDUMA KUU:", ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Msamiati na Kamusi", "🔊 Mtambo wa Sauti (Darasa la Sauti)", "🤖 AI Phonetic Robot (Ukaguzi)", "🔐 Ingia / Jisajili (Sign In)"])

# =====================================================================
# SYSTEM EXECUTION ENGINES (THE CONTROL ACTION)
# =====================================================================
if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("### 🎯 Malengo na Dira ya Kimkakati")
    str_platform.info("Kuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")

elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    maandishi = str_platform.text_area("Andika maandishi yako hapa:")
    if str_platform.button("Zindua Ukaguzi wa Sarufi"):
        if validate_entries.kagua_matini(maandishi):
            msafi = errorfix.safisha_spaces(maandishi)
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Sahihisha sarufi: {msafi}"}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:")
    if str_platform.button("Zindua Tafsiri ya Kitaalamu"):
        if validate_entries.kagua_matini(maandishi_t):
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate to English: {maandishi_t}"}])
            str_platform.success(" Matokeo ya Tafsiri:")
            str_platform.write(jibu_t.choices.message.content)

elif chaguo_menyu == "📚 Maktaba ya Msamiati na Kamusi":
    msamiati = str_platform.text_input("Andika neno au nahau:")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
        if validate_entries.kagua_matini(msamiati):
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Toa maana na mifano ya sentensi kwa: {msamiati}"}])
            str_platform.info("Uchambuzi wa Kamusi Kuu:")
            str_platform.write(jibu_v.choices.message.content)

elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa la Sauti)":
    if str_platform.session_state["user_status"] == "guest":
        str_platform.warning("👑 Kifurushi cha Majaribio ya Bure Kimeisha (Premium Lock). Tafadhali bofya '🔐 Ingia / Jisajili' upande wa menyu.")
    else:
        sauti.onyesha_sauti(client) # Ubongo unaamrisha faili tanzu liingie hewani

elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
    if str_platform.session_state["user_status"] == "guest":
        str_platform.warning("👑 Kipengele hiki kinahinajika Akaunti ya Premium. Tafadhali bofya '🔐 Ingia / Jisajili' upande wa menyu.")
    else:
        robot.onyesha_robot(client) # Ubongo unaamrisha faili tanzu liingie hewani

elif chaguo_menyu == "🔐 Ingia / Jisajili (Sign In)":
    chaguo_lango = str_platform.selectbox("Nia ya Kuingia yako:", ["Premium User", "Admin"])
    jina = str_platform.text_input("Username:")
    password = str_platform.text_input("Password:", type="password")
    if str_platform.button("Thibitisha Kuingia Mfumo"):
        if chaguo_lango == "Admin" and password == "Maroa2026":
            str_platform.session_state["user_status"] = "admin"
            str_platform.rerun()
        elif chaguo_lango == "Premium User" and jina.strip() != "" and password.strip() != "":
            str_platform.session_state["user_status"] = "standard_premium"
            str_platform.rerun()

elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
    admin.onyesha_admin(client, api_key_source) # Ubongo unaamrisha faili la admin ya siri

elif chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by Decentralized Oxford Architecture Framework</p>", unsafe_allow_html=True)

