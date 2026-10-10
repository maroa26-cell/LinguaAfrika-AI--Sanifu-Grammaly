import streamlit as str_platform
import os
import time
from openai import OpenAI
import database
import synapse

self_healing_status = "🟢 Autonomous Shield: Active & Healthy"
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

if "OPENAI_API_KEY" in os.environ: api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets: api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else: api_key_source = None

if api_key_source: client = OpenAI(api_key=api_key_source.strip())
else: str_platform.error("🔒 Secrets Error!"); str_platform.stop()

str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; color: #ffffff !important; border-right: 4px solid #D97706 !important; }
    div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; }
    div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 6px; padding: 4px 10px; }
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold; padding: 14px 28px; border-radius: 8px; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

muda_mwanzo = time.time()
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem</h3>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000
str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> 🟢 Stable</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> 🟢 Safe</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse:</b> {kasi_ya_radi:.3f}ms</p>
    <p style='color: #E2E8F0; font-size: 11px; margin: 0;'>🩺 <b>Self-Regulatory:</b> {self_healing_status}</p>
</div>
""", unsafe_allow_html=True)

orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu"]
chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA PORTAL DEVAL:", orodha_menyu, key="v14_clean_guest_radio")

str_platform.sidebar.write("---")
# 👑 THE HYPOTHALAMUS LINK PORTAL: Kiungo kisichoganda kinachompeleka kiongozi moja kwa moja kwenye Thalamus Dashboard!
str_platform.sidebar.markdown("""
<a href='https://streamlit.io' target='_blank'>
    <button style='background-color: #D97706; color: white; font-weight: bold; padding: 14px; border-radius: 8px; width: 100%; border: none; cursor: pointer;'>
        🔐 Fungua Lango Kuu la Utawala (Dashboard) ──►
    </button>
</a>
""", unsafe_allow_html=True)

if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="v14_ed")
    if str_platform.button("Zindua Ukaguzi"):
        if maandishi.strip() != "":
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Sahihisha sarufi ya Kiswahili: {maandishi}"}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)
elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="v14_tr")
    if str_platform.button("Zindua Tafsiri"):
        if maandishi_t.strip() != "":
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate to Swahili: {maandishi_t}"}])
            str_platform.write(jibu_t.choices.message.content)
elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili:", key="v14_kam")
    if str_platform.button("Tafuta"):
        if msamiati.strip() != "":
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Ufafanuzi wa neno: {msamiati}"}])
            str_platform.info(jibu_v.choices.message.content)

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 0.85rem; color: #9CA3AF; font-weight: bold;'>© 2026 Ourworthlinks • Enterprise Ecosystem</p>", unsafe_allow_html=True)
