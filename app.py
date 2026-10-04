import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa wa Kifalme - Ngazi ya Enterprise
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Ultra Premium Super Masterpiece Enterprise",
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
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI haujapatikana!")
    str_platform.stop()

# 🏰 Muonekano wa Juu wa Jukwaa la Kimataifa (Enterprise Corporate Header)
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: sans-serif; font-weight: 800;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: sans-serif;'>The Ultra Premium Super Masterpiece Enterprise Edition</h3>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; font-size: 1.2rem; color: #4B5563; max-width: 800px; margin: 0 auto;'>Mfumo mkuu wa kimkakati wa akili mnemba (AI) uliosajiliwa kusanifisha sarufi, kutafsiri lugha 14, na kukagua lafudhi ya Lugha ya Kiswahili duniani kwa kiwango cha kibiashara na kiofisi.</p>", unsafe_allow_html=True)
str_platform.write("---")

# 🗺️ Undaji wa Tabo Tano Kuu za Enterprise
tab1, tab2, tab3, tab4, tab5 = str_platform.tabs([
    "📝 Mhariri wa Kiswahili Sanifu Pro", 
    "🔀 Mtafsiri wa Lugha & Muktadha Suite", 
    "📚 Maktaba ya Msamiati na Nahau Kuu", 
    "🔊 Mtambo wa Sauti (Darasa la Sauti)", 
    "🤖 AI Phonetic Robot (Ukaguzi Mkuu)"
])

# =====================================================================
# TAB 1: 📝 MHARIRI WA KISWAHILI SANIFU PRO
# =====================================================================
with tab1:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            pro_prompt = f"Wewe ni mtaalamu wa lugha ya Kiswahili Sanifu. Kagua maandishi haya na usahihishie sarufi na tahajia:\n\n{maandishi_mhariri}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": pro_prompt}])
            str_platform.success("Marekebisho Yamekamilika!")
            str_platform.write(jibu.choices.message.content)

# =====================================================================
# TAB 2: 🔀 MTAFSIRI WA LUGHA & MUKTADHA SUITE (14 LUGHA + KIDINI)
# =====================================================================
with tab2:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kichewa (Chichewa)", "Kinyarwanda", "Kiganda (Luganda)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kihindi (Hindi)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    
    col1, col2, col3 = str_platform.columns(3)
    with col1:
        lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1, key="src_lang")
    with col2:
        lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0, key="tgt_lang")
    with col3:
        muktadha_tafsiri = str_platform.selectbox("Muktadha wa Matumizi (Context):", ["Mazungumzo ya Kawaida", "Kiakademia na Shule", "Kidini na Kiimani", "Kisheria na Kiofisi", "Kibiashara", "Fasihi na Ushairi"], key="context_lang")
        
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi unayotaka kutafsiri hapa:", height=150, key="translate_input_pro")
    
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            trans_prompt = f"Tafsiri kutoka {lugha_chanzo} kwenda {lugha_lengwa} katika muktadha wa {muktadha_tafsiri}:\n\n{maandishi_tafsiri}"
            jibu_tafsiri = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": trans_prompt}])
            str_platform.success("🔮 Matokeo ya Tafsiri:")
            str_platform.write(jibu_tafsiri.choices.message.content)

# =====================================================================
# TAB 3: 📚 MAKTABA YA MSAMIATI NA NAHAU KUU
# =====================================================================
with tab3:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Nahau Kuu</h3>", unsafe_allow_html=True)
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali hapa:", key="vocab_input_royal")
    
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="vocab_btn_royal"):
        if msamiati_input.strip() == "":
            str_platform.warning("Tafadhali andika msamiati kwanza!")
        else:
            vocab_prompt = f"Toa maana ya kina na mifano ya sentensi kwa kutumia msamiati huu wa Kiswahili: {msamiati_input}"
            jibu_vocab = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": vocab_prompt}])
            str_platform.info("Uchambuzi wa Kamusi Kuu:")
            str_platform.write(jibu_vocab.choices.message.content)

# =====================================================================
# TAB 4: 🔊 MTAMBO WA SAUTI (DARASA LA SAUTI)
# =====================================================================
with tab4:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    
    col_v1, col_v2 = str_platform.columns(2)
    with col_v1:
        sauti_mwalimu = str_platform.selectbox("Chagua Sauti ya Mwalimu:", ["onyx", "echo", "alloy"], key="teacher_voice_opt")
        maandishi_mwalimu = str_platform.text_area("Andika Maelezo ya Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_text_input")
    with col_v2:
        sauti_mwanafunzi_opt = str_platform.selectbox("Chagua Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"], key="student_voice_opt")
        maandishi_mwanafunzi = str_platform.text_area("Andika Majibu ya Mwanafunzi:", "Asante sana mwalimu wangu.", key="student_text_input")
    
    if str_platform.button("Zalisha Sauti za Darasa", key="tts_classroom_btn"):
        if maandishi_mwalimu.strip() == "" or maandishi_mwanafunzi.strip() == "":
            str_platform.warning("Tafadhali hakikisha umejaza maandishi yote mawili!")
        else:
            file_mwalimu = "sauti_mwalimu.mp3"
            res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu)
            f_teacher = open(file_mwalimu, "wb")
            f_teacher.write(res_mwalimu.content)
            f_teacher.close()
            str_platform.markdown("#### 👨‍🏫 Sauti ya Mwalimu:")
            str_platform.audio(file_mwalimu)
            
            file_mwanafunzi = "sauti_mwanafunzi.mp3"
            res_mwanafunzi = client.audio.speech.create(model="tts-1", voice=sauti_mwanafunzi_opt, input=maandishi_mwanafunzi)
            f_student = open(file_mwanafunzi, "wb")
            f_student.write(res_mwanafunzi.content)
            f_student.close()
            str_platform.markdown("#### 🧑‍🎓 Sauti ya Mwanafunzi:")
            str_platform.audio(file_mwanafunzi)
            str_platform.success("👑 Darasa la Sauti limekamilika!")

# =====================================================================
# TAB 5: 🤖 AI PHONETIC ROBOT (UKAGUZI MKUU)
# =====================================================================
with tab5:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🤖 AI Phonetic Robot (Ukaguzi Mkuu)</h3>", unsafe_allow_html=True)
    sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti (.wav/.mp3) hapa:", type=["wav", "mp3"], key="audio_uploader_royal_final")
    
    if sauti_mwanafunzi and str_platform.button("Zindua Ukaguzi wa Roboti", key="check_student_speech_btn_royal_final"):
        with str_platform.spinner("AI Robot anasikiliza lafudhi..."):
            trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read()))
            str_platform.info(f"🗣️ Robot amekusikia ukisema: '{trans_audio.text}'")
            robot_prompt = f"Mwanafunzi ametamka sentensi hii ya Kiswahili: '{trans_audio.text}'. Toa ripoti ya usahihi wa lafudhi yake, mpe alama (0-100%) na ushauri."
            jibu_robot = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": robot_prompt}])
            str_platform.success("🔮 Ripoti Kuu ya Roboti:")
            str_platform.write(jibu_robot.choices.message.content)

# =====================================================================
# 📢 SEHEMU YA KUSHEA MITANDAONI (WHATSAPP & FACEBOOK ENTERPRISE BUTTONS)
# =====================================================================
str_platform.write("---")
str_platform.markdown("<h3 style='text-align: center; color: #1E3A8A;'>📢 Kushea Mfumo Huu kwa Jamii</h3>", unsafe_allow_html=True)

link_ya_app = "https://streamlit.app"

