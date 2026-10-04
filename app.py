import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa wa Kifalme - Ngazi ya Edition 2 Responsive Suite
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Ultra Premium Super Masterpiece Edition 2",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 Kichocheo cha Usalama wa Siri (.env / Streamlit Secrets Enterprise)
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
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI (OPENAI_API_KEY) haujapatikana kwenye mifumo ya Secrets!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA MUONEKANO NA RANGI (EDITION 2 ENTERPRISE CSS INJECTION)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAFAFA !important;
        font-family: 'Helvetica Neue', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
        color: #ffffff !important;
        border-right: 3px solid #D97706 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stRadio"] > label {
        background-color: rgba(255, 255, 255, 0.05) !important;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease-in-out !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    div[data-testid="stRadio"] div[aria-checked="true"] {
        background-color: #D97706 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.15) !important;
        width: 100% !important;
    }
    textarea, input {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🏰 Muonekano wa Juu wa Jukwaa la Kimataifa (Edition 2 Corporate Header)
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: sans-serif; font-weight: 800; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: sans-serif; font-weight: 600; margin-top: 5px;'>The Ultra Premium Super Masterpiece • Edition 2</h3>", unsafe_allow_html=True)
str_platform.write("---")

# 🧭 UNDAJI WA MENYI YA PEMBENI YA KIFALME
str_platform.sidebar.markdown("<h2 style='color: #ffffff; text-align: center; font-weight: bold;'>LinguaAfrika AI</h2>", unsafe_allow_html=True)
str_platform.sidebar.write("---")

chaguo_menyu = str_platform.sidebar.radio(
    "CHAGUA HUDUMA KUU:",
    [
        "📝 Mhariri wa Kiswahili Sanifu Pro",
        "🔀 Mtafsiri wa Lugha & Muktadha Suite",
        "📚 Maktaba ya Msamiati na Nahau Kuu",
        "🔊 Mtambo wa Sauti (Darasa la Sauti)",
        "🤖 AI Phonetic Robot (Ukaguzi Mkuu)"
    ]
)

# =====================================================================
# CHAGUO 1: MHARIRI WA KISWAHILI SANIFU PRO
# =====================================================================
if chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() != "":
            pro_prompt = f"Wewe ni mtaalamu wa Kiswahili. Kagua na usahihishe maandishi haya:\n\n{maandishi_mhariri}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": pro_prompt}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)
        else:
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")

# =====================================================================
# CHAGUO 2: MTAFSIRI WA LUGHA & MUKTADHA SUITE (14 LUGHA + KIDINI)
# =====================================================================
elif chaguo_menyu == "🔀 Mtafsiri wa Lugha & Muktadha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kichewa (Chichewa)", "Kinyarwanda", "Kiganda (Luganda)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kihindi (Hindi)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    col1, col2, col3 = str_platform.columns(3)
    with col1:
        lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1)
    with col2:
        lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0)
    with col3:
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

# =====================================================================
# CHAGUO 3: MAKTABA YA MSAMIATI NA NAHAU KUU
# =====================================================================
elif chaguo_menyu == "📚 Maktaba ya Msamiati na Nahau Kuu":
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

# =====================================================================
# CHAGUO 4: MTAMBO WA SAUTI (DARASA LA SAUTI)
# =====================================================================
elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa la Sauti)":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    col_v1, col_v2 = str_platform.columns(2)
    with col_v1:
        sauti_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
        maandishi_mwalimu = str_platform.text_area("Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_text_input")
    with col_v2:
        sauti_mwanafunzi_opt = str_platform.selectbox("Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"])
        maandishi_mwanafunzi = str_platform.text_area("Mwanafunzi:", "Asante sana mwalimu wangu.", key="student_text_input")
    if str_platform.button("Zalisha Sauti za Darasa", key="tts_classroom_btn"):
        if maandishi_mwalimu.strip() != "" and maandishi_mwanafunzi.strip() != "":
            file_mwalimu = "sauti_mwalimu.mp3"
            res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu)
            f_teacher = open(file_mwalimu, "wb")
            f_teacher.write(res_mwalimu.content)
            f_teacher.close()
            str_platform.audio(file_mwalimu)
            
            file_mwanafunzi = "sauti_mwanafunzi.mp3"
            res_mwanafunzi = client.audio.speech.create(model="tts-1", voice=sauti_mwanafunzi_opt, input=maandishi_mwanafunzi)
            f_student = open(file_mwanafunzi, "wb")
            f_student.write(res_mwanafunzi.content)
            f_student.close()
            str_platform.audio(file_mwanafunzi)
        else:
            str_platform.warning("Tafadhali hakikisha umejaza maandishi yote mawili!")

# =====================================================================
# CHAGUO 5: 🤖 AI PHONETIC ROBOT (UPGRADE YA KIWANGO CHA JUU)
# =====================================================================
elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi Mkuu)":
