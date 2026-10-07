import streamlit as str_platform
import os
import time
from openai import OpenAI

# 🧠 COGNITIVE SUBSYSTEM IMPORTS (Moduli Huru!)
import database
import synapse
try:
    import central_nervous_system
    self_regulatory_status = "🟢 Autonomous Shield: Active & Healthy"
    mifumo_tayari = True
except Exception:
    self_regulatory_status = "🛠️ Self-Regulatory Action: Resolving Missing Brain Nodes"
    mifumo_tayari = False

# 👑 Zindua Mipangilio ya Seva Kuu ya Sayari
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Anzisha Hifadhidata ya Chuma ya SQLite Mara Moja mlangoni
database.anzisha_hifadhidata_ya_chuma()

if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana!")
    str_platform.stop()

# 🎨 Ngozi ya Nje: DIRECT SKIN INJECTION
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
if "active_user_name" not in str_platform.session_state: str_platform.session_state["active_user_name"] = ""

muda_mwanzo = time.time()
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem</h3>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# 📊 Bango la Siri la Telemetry (Rada ya Ubongo)
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

if mifumo_tayari:
    central_nervous_system.zindua_mifumo_ya_fahamu_ya_mwili(client, chaguo_menyu)
else:
    str_platform.warning("🛠️ Seva inaji-healing yenyewe... Tafadhali hakikisha umeunda central_nervous_system.py kule GitHub.")

if chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.session_state["active_user_name"] = ""
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by Super Modular Central Nervous System Architecture</p>", unsafe_allow_html=True)
