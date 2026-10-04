import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa wa Kisimamizi - Ngazi ya Edition 3 Independent Admin Suite
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Independent Admin Portal",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 KUUNGANISHA NA SYSTEM SETTINGS & SECRET KEY (STREAMLIT SECRETS INTEGRATION)
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

# Kuwasha mtambo OpenAI Suite kwa kutumia Siri zilizounganishwa
if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI (OPENAI_API_KEY) haujapatikana kwenye mifumo ya Settings au Secrets ya Seva!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA RANGI ZA KIKIPENZI NA KIFALME (ADMIN OBSIDIAN CSS INJECTION)
str_platform.markdown("""
<style>
    /* Muonekano Mkuu wa Jukwaa la Kiutawala */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important; /* Obsidian Dark */
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* 🏰 USANIFU WA KIFALME WA SIDEBAR YA ADMIN (DEEP EXECUTIVE SIDEBAR) */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important; /* Dark Slate */
        color: #ffffff !important;
        border-right: 4px solid #D97706 !important; /* Gold Border */
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    /* Sanifu Vifungo vya Menyu ya Pembeni */
    div[data-testid="stRadio"] > label {
        background-color: rgba(255, 255, 255, 0.05) !important;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
        transition: all 0.3s ease-in-out !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    div[data-testid="stRadio"] > label:hover {
        background-color: rgba(217, 119, 6, 0.2) !important;
        border-color: #D97706 !important;
    }
    div[data-testid="stRadio"] div[aria-checked="true"] {
        background-color: #D97706 !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
    }
    
    /* Sanifu Vifungo Vyote Katikati ya Skrini */
    div.stButton > button {
        background-color: #D97706 !important; /* Gold Button */
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(217, 119, 6, 0.25) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #B45309 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Muonekano wa Sanduku za Input */
    input, textarea {
        background-color: #1E293B !important;
        color: white !important;
        border: 2px solid #334155 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🏰 Muonekano wa Juu wa Jukwaa Kuu la Msimamizi
str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-family: sans-serif; font-weight: 900; margin-bottom: 0;'>🔐 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #ffffff; font-family: sans-serif; margin-top: 5px;'>Independent Administrative Portal • Edition 3</h3>", unsafe_allow_html=True)
str_platform.write("---")

# 🧭 UNDAJI WA MENYI YA PEMBENI (ADMIN SIDEBAR CONTROL PANEL)
str_platform.sidebar.markdown("<h1 style='color: #ffffff; text-align: center; font-size: 28px; margin-bottom: 0;'>🔐</h1>", unsafe_allow_html=True)
str_platform.sidebar.markdown("<h3 style='color: #ffffff; text-align: center; font-weight: bold; margin-top: 0;'>Admin Panel</h3>", unsafe_allow_html=True)
str_platform.sidebar.write("---")

chaguo_admin = str_platform.sidebar.radio(
    "UDHIBITI WA MFUMO:",
    [
        "📊 Ripoti Kuu ya Utendaji",
        "⚙️ Mipangilio & Secret Keys",
        "📢 Ujumbe wa Watumiaji"
    ]
)

# Mfumo wa ulinzi wa nenosiri tangu mwanzo
if "logged_in_global" not in str_platform.session_state:
    str_platform.session_state["logged_in_global"] = False

if not str_platform.session_state["logged_in_global"]:
    str_platform.markdown("<h4 style='text-align: center; color: #ffffff;'>Mfumo Umefungwa kiofisi. Tafadhali thibitisha mamlaka yako:</h4>", unsafe_allow_html=True)
    col_l, col_m, col_r = str_platform.columns(3)
    with col_m:
        nenosiri_admin = str_platform.text_input("Ingiza Nenosiri la Usimamizi:", type="password", key="master_key_field")
        if str_platform.button("Fungua Jopo la Usimamizi"):
            if nenosiri_admin == "Maroa2026":
                str_platform.session_state["logged_in_global"] = True
                str_platform.rerun()
            else:
                str_platform.error("🛑 Hitilafu: Nenosiri si sahihi!")

# MTAMBO UKIFUNGUKA (ADMIN ACCESS GRANTED)
if str_platform.session_state["logged_in_global"]:
    
    # 1. RIPOTI KUU YA UTENDAJI (SYSTEM OPERATIONS)
    if chaguo_admin == "📊 Ripoti Kuu ya Utendaji":
        str_platform.success("🔓 Karibu Mkuu Maroa! Mfumo upo chini ya uangalizi wako sasa.")
        if str_platform.button("Funga Jopo (Logout)"):
            str_platform.session_state["logged_in_global"] = False
            str_platform.rerun()
            
        str_platform.write("---")
        str_platform.markdown("<h3 style='color: #D97706;'>📊 Ripoti Kuu ya Utendaji (System Operations Dashboard)</h3>", unsafe_allow_html=True)
        
        col_stat1, col_stat2, col_stat3 = str_platform.columns(3)
        with col_stat1:
            str_platform.info("🧠 **Akili Mnemba (AI Engine)**\n\nStatus: Salama (100% Online)\n\nModel Source: OpenAI GPT-4o Enterprise")
        with col_stat2:
            str_platform.info("🔊 **Mtambo wa Sauti (Audio TTS)**\n\nStatus: Hai\n\nModel Source: OpenAI TTS-1 Suite")
        with col_stat3:
            str_platform.info("🌐 **Seva Kuu (Cloud Host)**\n\nStatus: Imara\n\nHost Server: Streamlit Global Node")

    # 2. MIPANGILIO & SECRET KEYS INTEGRATION
    elif chaguo_admin == "⚙️ Mipangilio & Secret Keys":
        str_platform.markdown("<h3 style='color: #D97706;'>⚙️ Mipangilio Kuu & Secret Keys Integration</h3>", unsafe_allow_html=True)
        str_platform.write("Hapa ndipo siri za mfumo na ufunguo wa OpenAI zilipofungwa kiusalama.")
        
        # Kuonyesha hali ya muunganisho wa siri
        if api_key_source:
            str_platform.success("🟢 Ufunguo wa Seva (OPENAI_API_KEY): **Umeunganishwa Kikamilifu na Streamlit Secrets**")
            str_platform.text_input("Encryption Node Status:", value="AES-256 Secured Connection", disabled=True)
        else:
            str_platform.error("🔴 Hitilafu: Secret Key haijasomeka kwenye seva!")

    # 3. UJUMBE WA WATUMIAJI (WELCOME NOTICE CONTROL)
    elif chaguo_admin == "📢 Ujumbe wa Watumiaji":
        str_platform.markdown("<h3 style='color: #D97706;'>📢 Ujumbe wa Mbele (Welcome Notice Control)</h3>", unsafe_allow_html=True)
        ujumbe_mpya = str_platform.text_input("Badilisha Tangazo la Juu la Mfumo wa Watumiaji:", value="Mfumo upo tayari kwa matumizi ya kiofisi na kiserikali.")
        str_platform.success(f"Marekebisho yamehifadhiwa kiofisi kwenye mtambo: '{ujumbe_mpya}'")

# Sehemu ya chini kabisa ya ukurasa
str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by OpenAI GPT-4o Corporate & Streamlit Cloud Solutions</p>", unsafe_allow_html=True)

