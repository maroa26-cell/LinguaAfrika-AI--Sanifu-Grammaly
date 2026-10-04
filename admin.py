import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Mipangilio ya Ukurasa wa Kisimamizi - Ngazi ya Admin Masterpiece Suite
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Independent Admin Portal",
    page_icon="🔐",
    layout="wide"
)

# 🔒 Kichocheo cha Usalama wa Siri
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

# Kuwasha mtambo OpenAI Suite
if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI haujapatikana!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA RANGI ZA KIKIPENZI (ADMIN GOLD SKIN)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important; /* Obsidian Dark */
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    div.stButton > button {
        background-color: #D97706 !important; /* Gold */
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #B45309 !important;
    }
    input {
        background-color: #1E293B !important;
        color: white !important;
        border: 2px solid #334155 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🏰 Muonekano wa Juu
str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>🔐 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #ffffff;'>Independent Administrative Portal • Edition 3</h3>", unsafe_allow_html=True)
str_platform.write("---")

# Mfumo wa ulinzi
if "logged_in_global" not in str_platform.session_state:
    str_platform.session_state["logged_in_global"] = False

if not str_platform.session_state["logged_in_global"]:
    str_platform.markdown("<h4 style='text-align: center;'>Mfumo Umefungwa. Tafadhali thibitisha mamlaka yako:</h4>", unsafe_allow_html=True)
    col_left, col_mid, col_right = str_platform.columns([1,2,1])
    with col_mid:
        nenosiri_admin = str_platform.text_input("Ingiza Nenosiri la Usimamizi:", type="password", key="master_key_field")
        if str_platform.button("Fungua Jopo la Usimamizi"):
            if nenosiri_admin == "Maroa2026":
                str_platform.session_state["logged_in_global"] = True
                str_platform.rerun()
            else:
                str_platform.error("🛑 Hitilafu: Nenosiri si sahihi! Walinzi wamekataa mamlaka yako.")

if str_platform.session_state["logged_in_global"]:
    str_platform.success("🔓 Karibu Mkuu Maroa! Mfumo mkuu unajitegemea sasa.")
    if str_platform.button("Funga Jopo (Logout)"):
        str_platform.session_state["logged_in_global"] = False
        str_platform.rerun()
        
    str_platform.write("---")
    str_platform.markdown("### 📊 Ripoti Kuu ya Utendaji (System Operations Dashboard)")
    
    col_stat1, col_stat2, col_stat3 = str_platform.columns(3)
    with col_stat1:
        str_platform.info("🧠 **Akili Mnemba (AI Engine)**\n\nStatus: Salama (100% Online)\n\nModel Source: OpenAI GPT-4o Enterprise")
    with col_stat2:
        str_platform.info("🔊 **Mtambo wa Sauti (Audio TTS)**\n\nStatus: Hai\n\nModel Source: OpenAI TTS-1 Suite")
    with col_stat3:
        str_platform.info("🌐 **Seva Kuu (Cloud Host)**\n\nStatus: Imara\n\nHost Server: Streamlit Global Node")

    str_platform.write("---")
    str_platform.markdown("### ⚙️ Mipangilio ya Dharura (System Configuration)")
    ujumbe_mpya = str_platform.text_input("Badilisha Tangazo la Juu la Mfumo wa Watumiaji:", "Mfumo upo tayari kwa matumizi ya kiofisi na kiserikali.")
    str_platform.success(f"Marekebisho yamehifadhiwa kiofisi: '{ujumbe_mpya}'")
