import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa Mkuu wa Kifalme - Freemium Lazy-Auth Architecture
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Premium Freemium Platform",
    page_icon="👑",
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

# Kuwasha mtambo OpenAI Suite kwa usalama wa hali ya juu
if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Secret Key (OPENAI_API_KEY) haujapatikana kwenye seva!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA MUONEKANO NA RANGI (EDITION 3 LUXURY CSS INJECTION)
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
    div[data-testid="stRadio"] > label:hover {
        background-color: rgba(217, 119, 6, 0.2) !important;
        border-color: #D97706 !important;
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
        border: none !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.2) !important;
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

# Kuanzisha kumbukumbu ya siri ya mtambo (Session State)
if "user_status" not in str_platform.session_state:
    str_platform.session_state["user_status"] = "guest"

# 🏰 Muonekano wa Juu wa Jukwaa la Kimataifa
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: sans-serif; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: sans-serif; font-weight: 700; margin-top: 5px;'>The Ultra Premium Super Masterpiece • Edition 3 Suite</h3>", unsafe_allow_html=True)
str_platform.write("---")

# =====================================================================
# 🧭 USANIFU WA MENYU YA SIDEBAR KULINGANA NA HALI YA USER STATUS
# =====================================================================
str_platform.sidebar.markdown("<h2 style='color: #ffffff; text-align: center; font-weight: bold;'>LinguaAfrika AI</h2>", unsafe_allow_html=True)

if str_platform.session_state["user_status"] == "admin":
    str_platform.sidebar.markdown("<p style='color: #25D366; text-align: center; font-weight: bold;'>👑 Administrator Mode</p>", unsafe_allow_html=True)
    chaguo_menyu = str_platform.sidebar.radio(
        "DASHBOARD YA USIMAMIZI:",
        [
            "📊 Ripoti Kuu ya Utendaji",
            "⚙️ Mipangilio & Secret Keys",
            "📢 Ujumbe wa Mbele",
            "🚪 Toka Kwenye Mfumo (Logout)"
        ]
    )
else:
    if str_platform.session_state["user_status"] == "standard_premium":
        str_platform.sidebar.markdown("<p style='color: #D97706; text-align: center; font-weight: bold;'>💎 Premium Member</p>", unsafe_allow_html=True)
    else:
        str_platform.sidebar.markdown("<p style='color: #9CA3AF; text-align: center; font-weight: bold;'>👤 Guest Mode (Free)</p>", unsafe_allow_html=True)
        
    chaguo_menyu = str_platform.sidebar.radio(
        "CHAGUA HUDUMA KUU:",
        [
            "📝 Mhariri wa Kiswahili Sanifu Pro",
            "🔀 Mtafsiri wa Lugha Suite",
            "📚 Maktaba ya Msamiati na Kamusi",
            "🔊 Mtambo wa Sauti (Darasa la Sauti)",
            "🤖 AI Phonetic Robot (Ukaguzi)",
            "🔐 Jisajili / Ingia (Sign In)"
        ]
    )

# =====================================================================
# CHAKULA CHA MAUDHUI YA NDANI (BUSINESS LOGIC EXECUTION)
# =====================================================================

# 1. MHARIRI PRO (BURE KWA WOTE)
if chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() != "":
            pro_prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi_mhariri}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": pro_prompt}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)
        else:
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")

# 2. MTAFSIRI PRO (BURE KWA WOTE)
elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kichewa (Chichewa)", "Kinyarwanda", "Kiganda (Luganda)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kihindi (Hindi)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1)
    lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0)
    muktadha_tafsiri = str_platform.selectbox("Muktadha:", ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara", "Fasihi na Ushairi"])
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=150, key="translate_input_pro")
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() != "":
            trans_prompt = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha_tafsiri} style:\n\n{maandishi_tafsiri}"
            jibu_tafsiri = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": trans_prompt}])
            str_platform.success("🔮 Matokeo ya Tafsiri ya Kitaalamu:")
            str_platform.write(jibu_tafsiri.choices.message.content)
        else:
            str_platform.warning("Tafadhali ingiza maandishi ya kutafsiri!")

# 3. KAMUSI PRO (BURE KWA WOTE)
elif chaguo_menyu == "📚 Maktaba ya Msamiati na Kamusi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Nahau Kuu</h3>", unsafe_allow_html=True)
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali hapa:", key="vocab_input_royal")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="vocab_btn_royal"):
        if msamiati_input.strip() != "":
            vocab_prompt = f"Toa maana na mifano ya sentensi kwa kutumia msamiati huu wa Kiswahili: {msamiati_input}"
            jibu_vocab = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": vocab_prompt}])
            str_platform.info("Uchambuzi wa Kitaalamu wa Kamusi Kuu:")
            str_platform.write(jibu_vocab.choices.message.content)
        else:
            str_platform.warning("Tafadhali andika msamiati kwanza!")

# 4. MTAMBO WA SAUTI (MTEGO WA MALIPO)
elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa la Sauti)":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    if str_platform.session_state["user_status"] == "guest":
        str_platform.warning("👑 Kipengele hiki ni cha kulipia (Premium feature). Tafadhali bofya '🔐 Jisajili / Ingia (Sign In)' upande wa menyu ya kushoto ili kuanza kifurushi.")
    else:
        sauti_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
        maandishi_mwalimu = str_platform.text_area("Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_text_input")
        sauti_mwanafunzi_opt = str_platform.selectbox("Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"])
        maandishi_mwanafunzi = str_platform.text_area("Mwanafunzi:", "Asante sana mwalimu wangu.", key="student_text_input")
        if str_platform.button("Zalisha Sauti za Darasa", key="tts_classroom_btn"):
