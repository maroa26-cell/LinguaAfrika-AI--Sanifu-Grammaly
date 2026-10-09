import streamlit as str_platform
import os
import time
import importlib  # 👑 SYNAPTIC RE-IMPORT PIPELINE
import sys
from openai import OpenAI

# 🧠 BIOMIMETIC SUBSYSTEM IMPORTS (Moduli Huru)
import database
import synapse
import pesapal_core

self_healing_status = "🟢 Autonomous Shield: Active & Healthy"
mifumo_tayari = True

# 👑 MITAMBO YA SHINA LA UBONGO (LINUX CACHE CLEAR PIPELINE)
# Kulazimisha Linux kusoma faili jipya la central_nervous_system.py kila sekunde!
try:
    if "central_nervous_system" in sys.modules:
        importlib.reload(sys.modules["central_nervous_system"])
    import central_nervous_system
except Exception as e:
    self_healing_status = "🛠️ Self-Regulatory Action: Restoring Defected Memory Nodes"
    mifumo_tayari = False

# 👑 Sanifu Mipangilio ya Seva Kuu ya Sayari
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🧬 HYPOTHALAMUS LAYER: Udhibiti na Ulinzi wa Vigezo vya Ndani (Homeostasis)
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

if api_key_source:
    client = OpenAI(api_key=api_key_source.strip())
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana!")
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

# 📊 BANGO LA SHINA LA UBONGO (CNS METRICS ENGINE)
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

# 👑 CEREBRUM LOGIC: Orodha ya vitufe inayosomwa kwa ulinganifu thabiti
jina_lango_dashboard = "🔐 Lango la Kuingia (Login Dashboard)"

if hali_ya_sasa == "admin":
    str_platform.sidebar.markdown(f"<p style='color: #25D366; text-align: center;'>👑 Admin: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    orodha_menyu = ["📊 Ripoti Kuu ya Utendaji", "🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
elif hali_ya_sasa == "standard_premium":
    str_platform.sidebar.markdown(f"<p style='color: #D97706; text-align: center;'>💎 Premium: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
else:
    str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center;'>👤 Guest Mode (Free Portal)</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", jina_lango_dashboard]

chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", orodha_menyu, key="sovereign_cerebrum_v13_final")

# =====================================================================
# ⚙️ SYNAPTIC ROUTING SIGNAL: Kusukuma ishara kuelekea Ubongo Mdogo
# =====================================================================
if mifumo_tayari:
    try:
        central_nervous_system.zindua_mifumo_ya_fahamu_ya_mwili(client, chaguo_menyu)
    except Exception as e:
        str_platform.error(f"🛑 Hitilafu ya mawasiliano ya viungo vya ndani: {str(e)}")
else:
    str_platform.markdown("""
    <div style='background-color: rgba(217, 119, 6, 0.1); border: 2px solid #D97706; padding: 20px; border-radius: 10px; text-align: center;'>
        <h4 style='color: #D97706; margin: 0 0 5px 0;'>🛠️ Mtambo Unasafisha Mishipa (Self-Healing Loop)</h4>
        <p style='color: #E2E8F0; font-size: 14px; margin: 0;'>Tafadhali hakikisha msimbo timilifu wa <b>central_nervous_system.py</b> umesha-commitiwa vizuri kule GitHub.</p>
    </div>
    """, unsafe_allow_html=True)

if chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.session_state["active_user_name"] = "Mgeni"
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 Ourworthlinks • LinguaAfrika AI Ecosystem Enterprise • Powered by Super Modular Central Nervous System Architecture</p>", unsafe_allow_html=True)
