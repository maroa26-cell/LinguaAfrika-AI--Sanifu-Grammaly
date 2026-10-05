import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa Mkuu - Oxford Freemium Framework Edition 4
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Premium Freemium Platform",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 KUUNGANISHA NA SYSTEM SETTINGS & SECRET KEY
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
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA MUONEKANO NA RANGI (EDITION 4 ENTERPRISE LUXURY SKIN)
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
        border-radius: 8px !important;
        padding: 4px 10px !important;
    }
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.2) !important;
        width: 100% !important;
    }
    textarea, input {
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Kuanzisha kumbukumbu ya siri ya mtambo (Session State)
if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

# 🏰 Muonekano wa Juu
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Ultra Premium Super Masterpiece • Edition 4</h3>", unsafe_allow_html=True)
str_platform.write("---")

# =====================================================================
# 🧭 USANIFU WA MENYU YA SIDEBAR CONTROL PANEL
# =====================================================================
str_platform.sidebar.markdown("<h2 style='text-align: center; color: #ffffff; font-weight: bold;'>LinguaAfrika AI</h2>", unsafe_allow_html=True)

if str_platform.session_state["user_status"] == "admin":
    str_platform.sidebar.markdown("<p style='color: #25D366; text-align: center; font-weight: bold;'>👑 Administrator Mode</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio(
        "DASHBOARD YA USIMAMIZI:",
        ["📊 Ripoti Kuu ya Utendaji", "⚙️ Mipangilio & Secret Keys", "📢 Ujumbe wa Mbele", "🚪 Toka Kwenye Mfumo (Logout)"]
    )
else:
    if str_platform.session_state["user_status"] == "standard_premium":
        str_platform.sidebar.markdown("<p style='color: #D97706; text-align: center; font-weight: bold;'>💎 Premium Member (Unlocked)</p>", unsafe_allow_html=True)
    else:
        str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center; font-weight: bold;'>👤 Guest Mode (Free Portal)</p>", unsafe_allow_html=True)
        
    chaguo_menyu = str_platform.sidebar.radio(
        "CHAGUA HUDUMA KUU:",
        [
            "🎯 Malengo na Dira ya Taasisi",
            "📝 Mhariri wa Kiswahili Sanifu Pro",
            "🔀 Mtafsiri wa Lugha Suite",
            "📚 Maktaba ya Msamiati na Kamusi",
            "🔊 Mtambo wa Sauti (Darasa la Sauti)",
            "🤖 AI Phonetic Robot (Ukaguzi)",
            "🔐 Ingia / Jisajili (Sign In)"
        ]
    )

# =====================================================================
# CHAKULA CHA MAUDHUI YA NDANI (FLAWLESS NO-INDENT STRUCTURE)
# =====================================================================

# 0. MALENGO NA DIRA
if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI emesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
    col_m1, col_m2 = str_platform.columns(2)
    with col_m1:
        str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha sarufi.")
    with col_m2:
        str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure za kusaidia jamii kuhariri.")

# 1. MHARIRI PRO
elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() != "":
            pro_prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi_mhariri}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": pro_prompt}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)

# 2. MTAFSIRI PRO
elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kifaransa (French)", "Kiarabu (Arabic)"]
    lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1)
    lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0)
    muktadha_tafsiri = str_platform.selectbox("Muktadha:", ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani"])
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=150, key="translate_input_pro")
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() != "":
            trans_prompt = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha_tafsiri} style:\n\n{maandishi_tafsiri}"
            jibu_tafsiri = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": trans_prompt}])
            str_platform.success("🔮 Matokeo ya Tafsiri ya Kitaalamu:")
            str_platform.write(jibu_tafsiri.choices.message.content)

# 3. KAMUSI PRO
elif chaguo_menyu == "📚 Maktaba ya Msamiati na Kamusi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Nahau Kuu</h3>", unsafe_allow_html=True)
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali hapa:", key="vocab_input_royal")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="vocab_btn_royal"):
        if msamiati_input.strip() != "":
            vocab_prompt = f"Toa maana na mifano ya sentensi kwa kutumia msamiati: {msamiati_input}"
            jibu_vocab = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": vocab_prompt}])
            str_platform.info("Uchambuzi wa Kitaalamu wa Kamusi Kuu:")
            str_platform.write(jibu_vocab.choices.message.content)

# 4. MTAMBO WA SAUTI (FLAWLESS NO-INDENT PAYWALL BANNER UPGRADE)
elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa la Sauti)":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    
    # Mfumo salama wa upimaji wa Guest kuzuia makosa ya space
    hali_ya_mtu = str_platform.session_state["user_status"]
    
    if hali_ya_mtu == "guest":
        str_platform.warning("👑 Kifurushi cha Majaribio ya Bure Kimeisha (Premium Lock). Tafadhali nenda kwenye kipengele cha '🔐 Ingia / Jisajili (Sign In)' pembeni ili kufungua kiofisi.")
    
    if hali_ya_mtu != "guest":
        sauti_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
        maandishi_mwalimu = str_platform.text_area("Mwalimu Maelezo:", "Karibu darasani mwanafunzi wangu.", key="teacher_text_input")
        sauti_mwanafunzi_opt = str_platform.selectbox("Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"])
        maandishi_mwanafunzi = str_platform.text_area("Mwanafunzi Maelezo:", "Asante sana mwalimu wangu.", key="student_text_input")
        if str_platform.button("Zalisha Sauti za Darasa Direct", key="perfect_audio_btn"):
            res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu)

