import streamlit as str_platform
import os
from openai import OpenAI

# =====================================================================
# 🧠 CENTRAL NERVOUS SYSTEM OMNI-ORCHESTRATOR (UBONGO MKUU)
# =====================================================================
import style
import errorfix
import circulatory_transport
import Central_Nervous_System # Kuvuta injini kuu ya ubongo wa binadamu (MPYA!)

# 👑 Zindua Mipangilio ya Seva Kuu
str_platform.set_page_config(page_title="LinguaAfrika AI: Super Biomimetic Platform", page_icon="🧠", layout="wide")

if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key haujapatikana!")
    str_platform.stop()

# 8) Ngozi ya Nje (Integumentary Skin Layer Injection)
style.weka_mandhari_ya_kifalme()

if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

# 🏰 Corporate Header Layout
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem • Edition 4</h3>", unsafe_allow_html=True)
str_platform.write("---")

# 🫁 RESPIRATORY & CIRCULATORY TELEMETRY BANNERS
afya_ya_mapafu = errorfix.kagua_afya_ya_mapafu_ya_seva()
shinikizo_la_data = circulatory_transport.kagua_shinikizo_la_damu_ya_seva()

str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(37, 211, 102, 0.08); border: 1px solid #25D366; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
    <p style='color: #25D366; font-size: 13px; margin: 0; text-align: center;'>🫁 <b>RESPIRATORY STATUS:</b><br>{afya_ya_mapafu}</p>
    <hr style='border-color: rgba(37, 211, 102, 0.2); margin: 6px 0;'>
    <p style='color: #25D366; font-size: 13px; margin: 0; text-align: center;'>🩸 <b>CIRCULATORY TRAFFIC:</b><br>{shinikizo_la_data}</p>
</div>
""", unsafe_allow_html=True)

# 🧭 SIDEBAR OMNI NAVIGATION CONTROLLER
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
# 🧠 RUNNING THE BIOMIMETIC BRAIN KERNEL (AUTO-TRIGGER CORCHESTRATION)
# =====================================================================
Central_Nervous_System.zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu)

# Logout Handler inside the core brain
if chaguo_menyu == "🚪 Toka Kwenye Mfumo (Logout)":
    str_platform.session_state["user_status"] = "guest"
    str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 LinguaAfrika AI Ecosystem Enterprise • Powered by Super Modular Central Nervous System Architecture</p>", unsafe_allow_html=True)
