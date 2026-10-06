import streamlit as str_platform
import os
import time
from openai import OpenAI

# 👑 Zindua Mipangilio ya Seva Kuu ya Sayari
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Super Biomimetic Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 KUUNGANISHA NA SYSTEM SECRET KEY (STREAMLIT SECRETS INTEGRATION)
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

# 🎨 8) NGOZI YA NJE: DIRECT SKIN INJECTION (EDITION 4 ENTERPRISE LUXURY SKIN)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0F172A !important; /* Obsidian Dark */
        color: #ffffff !important;
        border-right: 4px solid #D97706 !important; /* Gold Border */
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] > label {
        background-color: rgba(255, 255, 255, 0.04) !important;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease-in-out !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    div[data-testid="stRadio"] div[aria-checked="true"] {
        background-color: #D97706 !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
    }
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.2) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #D97706 !important;
        transform: translateY(-2px) !important;
    }
    textarea, input {
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

# 🏰 Corporate Header Layout
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem • Edition 4 Suite</h3>", unsafe_allow_html=True)
str_platform.write("---")

# 🫁 5 & 1) AUTONOMIC SEVA TELEMETRY (MEDULLA OBLONGATA)
try:
    import errorfix
    import circulatory_transport
    import Central_Nervous_System
    afya_ya_mapafu = errorfix.kagua_afya_ya_mapafu_ya_seva()
    shinikizo_la_data = circulatory_transport.kagua_shinikizo_la_damu_ya_seva()
    errorfix.safisha_uchafu_wa_kache()
    mifumo_tayari = True
except Exception:
    afya_ya_mapafu = "🫁 Mifumo ya ndani inayumba: Unda mafaili tanzu GitHub sasa"
    shinikizo_la_data = "🩸 Mzunguko wa Ndani: Kusubiri Usafishaji"
    mifumo_tayari = False

str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(37, 211, 102, 0.08); border: 1px solid #25D366; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
    <p style='color: #25D366; font-size: 13px; margin: 0; text-align: center;'>🫁 <b>RESPIRATORY STATUS:</b><br>{afya_ya_mapafu}</p>
    <hr style='border-color: rgba(37, 211, 102, 0.2); margin: 6px 0;'>
    <p style='color: #25D366; font-size: 13px; margin: 0; text-align: center;'>🩸 <b>CIRCULATORY TRAFFIC:</b><br>{shinikizo_la_data}</p>
</div>
""", unsafe_allow_html=True)

# 🧭 SIDEBAR OMNI NAVIGATION CONTROLLER (ROLE-BASED NERVOUS ROUTING)
str_platform.sidebar.markdown("<h2 style='text-align: center; color: #ffffff; font-weight: bold;'>🧠 Neural Panel</h2>", unsafe_allow_html=True)

if str_platform.session_state["user_status"] == "admin":
    chaguo_menyu = str_platform.sidebar.radio("UDHIBITI WA ENDOCRINE:", ["📊 Ripoti Kuu ya Utendaji", "🚪 Toka Kwenye Mfumo (Logout)"])
else:
    if str_platform.session_state["user_status"] == "standard_premium":
        str_platform.sidebar.markdown("<p style='color: #D97706; text-align: center; font-weight: bold;'>💎 Premium Member (Unlocked)</p>", unsafe_allow_html=True)
    else:
        str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center; font-weight: bold;'>👤 Guest Account (Free Portal)</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🔐 Ingia / Jisajili (Sign In)"])

# =====================================================================
# 🧠 RUNNING THE BIOMIMETIC BRAIN KERNEL ORCHESTRATION
# =====================================================================
if mifumo_tayari:
    Central_Nervous_System.zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu)
else:
    str_platform.error("🛑 Ubongo unatafuta viungo vyake GitHub: Tafadhali hakikisha umeunda faili la Central_Nervous_System.py na mafaili tanzu yote kulingana na mwongozo.")

# Logout Handler inside the core brain
if chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by Super Modular Central Nervous System Architecture</p>", unsafe_allow_html=True)
