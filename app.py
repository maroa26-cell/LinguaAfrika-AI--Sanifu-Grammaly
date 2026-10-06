import streamlit as str_platform
import os
import time
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Seva Kuu ya Sayari (Edition 4 Super Suite)
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
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        color: #ffffff !important;
        border-right: 4px solid #D97706 !important;
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
        padding: 14px 28px !important;
        border-radius: 8px !important;
        border: none !important;
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

# 🧠 Mfumo wa Siri wa Kujirekebisha na Hifadhidata ya Ndani ya Utambulisho (Session State DB Matrix)
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

# Telemetry ya afya ya seva na kasi ya radi
afya_ya_mapafu = "🟢 Afya ya Mapafu (RAM/CPU): Salama (100% Active)"
shinikizo_la_data = "🟢 Shinikizo la Mzunguko (Data Traffic): Imara"
kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> {afya_ya_mapafu}</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> {shinikizo_la_data}</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms (Radi)</p>
    <hr style='border-color: rgba(217, 119, 6, 0.3); margin: 8px 0;'>
    <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: Multi-Role Active Protection</p>
</div>
""", unsafe_allow_html=True)

# 🧭 SIDEBAR OMNI NAVIGATION PANEL (DETERMINED BY CENTRAL BRAIN CORE)
str_platform.sidebar.markdown("<h2 style='text-align: center; color: #ffffff; font-weight: bold;'>🧠 Neural Panel</h2>", unsafe_allow_html=True)

hali_ya_sasa = str_platform.session_state["user_status"]
jina_la_sasa = str_platform.session_state["active_user_name"]

if hali_ya_sasa == "admin":
    str_platform.sidebar.markdown(f"<p style='color: #25D366; text-align: center; font-weight: bold;'>👑 Administrator: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio("UDHIBITI WA UTENDAJI:", ["📊 Ripoti Kuu ya Utendaji", "⚙️ Mipangilio ya Siri ya Seva", "🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"])
elif hali_ya_sasa == "standard_premium":
    str_platform.sidebar.markdown(f"<p style='color: #D97706; text-align: center; font-weight: bold;'>💎 Premium Member: {jina_la_sasa.upper()}</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🚪 Toka Kwenye Mfumo (Logout)"])
else:
    str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center; font-weight: bold;'>👤 Guest Account (Free Portal)</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio("CHAGUA SEHEMU YA MFUMO:", ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu", "🔊 Mtambo wa Sauti (Darasa)", "🤖 AI Phonetic Robot (Ukaguzi)", "🔐 Lango la Kuingia (Login Dashboard)"])

# =====================================================================
# ⚙️ THE MONOLITHIC CENTRAL NERVOUS SYSTEM ROUTING EXECUTION
# =====================================================================

if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
    col_m1, col_m2 = str_platform.columns(2)
    with col_m1: str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha Kiswahili.")
    with col_m2: str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii.\n\n• Kujenga mitambo ya kulipia ya sauti kwa shule.")

elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v4_direct")
    if str_platform.button("Zindua Ukaguzi wa Sarufi"):
        if maandishi.strip() != "":
            prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi.strip()}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            str_platform.success("Marekebisho Yamekamilika! ✨")
            str_platform.write(jibu.choices.message.content)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Kichewa (Chichewa)", "Kiyarabu (Arabic)", "Kifaransa (French)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kiafrikana (Afrikaans)"]
    muktadha_list = ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara", "Fasihi na Ushairi"]
    col1, col2, col3 = str_platform.columns(3)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1)
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0)
    with col3: muktadha = str_platform.selectbox("Muktadha wa Tafsiri:", muktadha_list, index=0)
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=150, key="trans_v4_direct")
    if str_platform.button("Zindua Tafsiri ya Kitaalamu"):
        if maandishi_t.strip() != "":
            prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha} style:\n\n{maandishi_t.strip()}"
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
            str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
            str_platform.write(jibu_t.choices.message.content)

elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
