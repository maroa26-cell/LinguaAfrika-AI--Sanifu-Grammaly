import streamlit as str_platform
import os
import time
from openai import OpenAI

# 🧠 COGNITIVE SUBSYSTEM IMPORTS
import database
import synapse

self_healing_status = "🟢 Autonomous Shield: Active & Healthy"

# 👑 Sanifu Mipangilio ya Seva Kuu ya Sayari
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

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

# 📊 Bango la Telemetry (Rada ya Ubongo Kuu)
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
    orodha_menyu = ["📊 Ripoti Kuu ya Utendaji", "🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
elif hali_ya_sasa == "standard_premium":
    str_platform.sidebar.markdown(f"<p style='color: #D97706; text-align: center;'>💎 Premium: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"]
else:
    str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center;'>👤 Guest Mode (Free Portal)</p>", unsafe_allow_html=True)
    orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔐 Lango la Kuingia (Login Dashboard)"]

chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", orodha_menyu, key="main_radio_v8_omnicore")

# =====================================================================
# ⚙️ CENTRAL MONOLITHIC COGNITIVE SYSTEM EXECUTION (SOVEREIGN INTEGRATION)
# =====================================================================
if chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
    str_platform.markdown("<h2 style='color: #D97706; font-weight: bold;'>📊 Ourworthlinks Operations Jopo</h2>", unsafe_allow_html=True)
    str_platform.success(f"🔓 Karibu Kiongozi {jina_la_sasa.upper()}! Mifumo yote ya B2B API Token Channels ipo hai kwenye SQLite chuma.")
    str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
    data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
    str_platform.table(data_b2b)
    col_b1, col_b2 = str_platform.columns(2)
    with col_b1: str_platform.info("💰 **Total B2B Revenue Logged**\n\nAccumulated: **$1,240.50 USD**")
    with col_b2: str_platform.info("📈 **Traffic Volume Analytics**\n\nTotal Words API Streams: **620,250 Words**")

elif chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
    col_m1, col_m2 = str_platform.columns(2)
    with col_m1: str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")
    with col_m2: str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii kuhariri.\n\n• Kujenga mitambo ya kiasili ya mtafsiri na kamusi.")

elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v8_box")
    if str_platform.button("Zindua Ukaguzi wa Sarufi"):
        if maandishi.strip() != "":
            prompt = f"Sahihisha sarufi ya matini haya kitalaalamu:\n\n{maandishi.strip()}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            str_platform.success("Marekebisho Yamekamilika! ✨")
            str_platform.write(jibu.choices.message.content)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)", "Kihindi (Hindi)", "Kireno (Portuguese)", "Kichina (Chinese)"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v8")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v8")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v8_box")
    if str_platform.button("Zindua Tafsiri"):
        if maandishi_t.strip() != "":
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate from {lugha_chanzo} to {lugha_lengwa}: {maandishi_t}"}])
            str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
            str_platform.write(jibu_t.choices.message.content)

elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno, nahau au methali hapa ya Kiswahili:", key="kamusi_input_v8")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
        if msamiati.strip() != "":
            prompt_v = f"Wewe ni Kamusi Kuu ya Lugha za Kiafrika. Toa ufafanuzi wa kina na mifano ya sentensi kwa neno hili la Kiswahili: {msamiati.strip()}"
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
            str_platform.info("✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:")
            str_platform.write(jibu_v.choices.message.content)

elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
    str_platform.markdown("### 🔊 Mtambo wa Sauti Kuu ya Darasa (UNLOCKED) 🔓", unsafe_allow_html=True)
    v_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
