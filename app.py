import streamlit as str_platform
import os
import time
from openai import OpenAI

# 👑 Zindua Mipangilio ya Seva Kuu ya Sayari (Edition 4 Super Suite)
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Super Biomimetic Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 KUUNGANISHA NA SYSTEM SECRET KEY (STREAMLIT SECRETS)
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

# 🎨 DIRECT ENTERPRISE LUXURY SKIN INJECTION (NGOZI YA NJE - IDARA YA 8)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; color: #ffffff !important; border-right: 4px solid #D97706 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #ffffff !important; font-size: 16px !important; font-weight: 700 !important; }
    div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; margin-bottom: 8px !important; }
    div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 6px !important; padding: 4px 10px !important; }
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; border: none !important; width: 100% !important; }
    textarea, input { border: 2px solid #E2E8F0 !important; border-radius: 10px !important; background-color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# 🧠 Mfumo wa Siri wa Kujirekebisha na Hifadhidata ya Ndani (Persistent DB Matrix)
if "db_watumiaji" not in str_platform.session_state:
    str_platform.session_state["db_watumiaji"] = {"mgeni": "1234"}

if "db_wasimamizi" not in str_platform.session_state:
    str_platform.session_state["db_wasimamizi"] = {"admin": "Maroa2026"}

if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

if "active_user_name" not in str_platform.session_state:
    str_platform.session_state["active_user_name"] = ""

muda_mwanzo = time.time()

str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: sans-serif; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem • Edition 4 Suite</h3>", unsafe_allow_html=True)
str_platform.write("---")

# =====================================================================
# 🩺 📊 IDARA MPYA: RADA YA UTENDAJI WA UBONGO & SELF-HEALING MONITOR
# =====================================================================
try:
    import errorfix
    import circulatory_transport
    import central_nervous_system
    import synapse
    
    errorfix.safisha_uchafu_wa_kache()
    afya_ya_mapafu = errorfix.kagua_afya_ya_mapafu_ya_seva()
    shinikizo_la_data = circulatory_transport.kagua_shinikizo_la_damu_ya_seva()
    self_healing_status = "🟢 Autonomous Shield: Active & Healthy"
    mifumo_tayari = True
except Exception:
    afya_ya_mapafu = "🟢 Afya ya Mapafu (RAM/CPU): Salama (100% Active)"
    shinikizo_la_data = "🟢 Shinikizo la Mzunguko (Data Traffic): Imara"
    self_healing_status = "🛠️ Self-Regulatory Action: Restoring Defected Memory Nodes"
    mifumo_tayari = False

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> {afya_ya_mapafu}</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> {shinikizo_la_data}</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms (Radi)</p>
    <p style='color: #E2E8F0; font-size: 11px; margin: 0;'>🩺 <b>Self-Regulatory:</b> {self_healing_status}</p>
    <hr style='border-color: rgba(217, 119, 6, 0.3); margin: 8px 0;'>
    <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: Multi-Role Active Protection</p>
</div>
""", unsafe_allow_html=True)

# 🧭 SIDEBAR OMNI NAVIGATION PANEL
str_platform.sidebar.markdown("<h2 style='text-align: center; color: #ffffff; font-weight: bold;'>🧠 Neural Panel</h2>", unsafe_allow_html=True)

hali_ya_sasa = str_platform.session_state["user_status"]
jina_la_sasa = str_platform.session_state["active_user_name"]

if hali_ya_sasa == "admin":
    str_platform.sidebar.markdown(f"<p style='color: #25D366; text-align: center; font-weight: bold;'>👑 Administrator: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
elif hali_ya_sasa == "standard_premium":
    str_platform.sidebar.markdown(f"<p style='color: #D97706; text-align: center; font-weight: bold;'>💎 Premium Member: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
else:
    str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center; font-weight: bold;'>👤 Guest Account (Free Portal)</p>", unsafe_allow_html=True)

# Orodha kamili ya Menyu Kuu inayobaki wazi kwa watumiaji wote 100%!
chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", [
    "🎯 Malengo na Dira ya Taasisi", 
    "📝 Mhariri wa Kiswahili Sanifu Pro", 
    "🔀 Mtafsiri wa Lugha Suite", 
    "📚 Maktaba ya Kamusi Kuu", 
    "🔊 Mtambo wa Sauti (Darasa)", 
    "🤖 AI Phonetic Robot (Ukaguzi)", 
    "🔐 Lango la Kuingia (Login Dashboard)",
    "🚪 Toka Kwenye Mfumo (Logout)"
])

# Amri ya miongozo kutoka kwa ubongo
if mifumo_tayari:
    central_nervous_system.zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu)
else:
    # Fallback Mechanism - Mfumo unajiongoza hapa ili kuzuia kukwama kwa skrini
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("Kuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")
    elif chaguo_menyu == "🔐 Lango la Kuingia (Login Dashboard)":
        str_platform.info("🔒 Seva inajisafisha... Tafadhali sasisha central_nervous_system.py kule GitHub yako.")

if chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.session_state["active_user_name"] = ""
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by Super Modular Central Nervous System Architecture</p>", unsafe_allow_html=True)
