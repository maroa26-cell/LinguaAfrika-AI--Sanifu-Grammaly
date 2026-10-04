import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa wa Kifalme
str_platform.set_page_config(
    page_title="LinguaAfrika AI: The Ultimate Premium Masterpiece",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 Kichocheo cha Usalama wa Siri (.env / Streamlit Secrets)
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

# Kuwasha mtambo rasmi wa OpenAI
if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu: Ufunguo wa siri wa OpenAI (OPENAI_API_KEY) haujapatikana kwenye mifumo ya Secrets!")
    str_platform.stop()

# 🏰 Muonekano wa Juu wa Jukwaa (Header)
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A;'>👑 LinguaAfrika AI: The Ultimate Premium Masterpiece</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; font-size: 1.2rem; color: #4B5563;'>Mfumo mkuu wa akili mnemba wa kusanifisha, kutafsiri, na kukagua lafudhi ya Lugha ya Kiswahili duniani.</p>", unsafe_allow_html=True)
str_platform.write("---")

# 🗺️ Undaji wa Tabo Tano Kuu za Kifalme
tab1, tab2, tab3, tab4, tab5 = str_platform.tabs([
    "📝 Mhariri wa Kiswahili Sanifu", 
    "🔀 Mtafsiri wa Lugha & Muktadha Pro", 
    "📚 Maktaba ya Msamiati na Nahau", 
    "🔊 Mtambo wa Sauti ya AI (Darasa la Sauti)", 
    "🤖 AI Phonetic Robot (Ukaguzi wa Lafudhi)"
])

# =====================================================================
# TAB 1: 📝 MHARIRI WA KISWAHILI SANIFU (GRAMMARLY PRO)
# =====================================================================
with tab1:
    str_platform.header("📝 Mhariri wa Kiswahili Sanifu (Grammarly Pro)")
    str_platform.write("Ingiza maandishi yako ya Kiswahili hapa chini ili AI yakubalie kurekebisha sarufi, tahajia, na mtiririko wa maneno kulingana na Kamusi Kuu.")
    
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    
    if str_platform.button("Kagua na Sahihisha", key="editor_btn_royal"):
        if maandishi_mhariri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            with str_platform.spinner("AI mzawa anatafiti sarufi..."):
                try:
                    pro_prompt = f"Wewe ni mtaalamu mwandamizi wa lugha ya Kiswahili Sanifu. Kagua maandishi haya, sahihisha makosa yote ya sarufi and tahajia, kisha ulete majibu nadhifu yakionyesha marekebisho yaliyofanyika:\n\n{maandishi_mhariri}"
                    jibu = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": pro_prompt}]
                    )
                    str_platform.success("Marekebisho Yamekamilika!")
                    str_platform.write(jibu.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Seva: {error_msg}")

# =====================================================================
# TAB 2: 🔀 MTAFSIRI WA LUGHA & MUKTADHA PRO
# =====================================================================
with tab2:
    str_platform.header("🔀 Mtafsiri wa Lugha & Muktadha wa Kiakademia")
    str_platform.write("Boresha tafsiri yako kwa kuchagua lugha lengwa pamoja na muktadha maalum ili kupata maana sahihi zaidi.")
    
    col1, col2, col3 = str_platform.columns(3)
    with col1:
        lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", ["Kiingereza (English)", "Kiswahili", "Kifaransa (French)", "Kiarabu (Arabic)"], key="src_lang")
    with col2:
        lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", ["Kiswahili", "Kiingereza (English)", "Kifaransa (French)", "Kiarabu (Arabic)"], key="tgt_lang")
    with col3:
        muktadha_tafsiri = str_platform.selectbox("Muktadha wa Matumizi (Context):", [
            "Mazungumzo ya Kawaida (Casual Conversation)",
            "Kiakademia na Shule (Academic/Educational)",
            "Kisheria na Kiofisi (Legal/Official Documentation)",
            "Kibiashara na Kiuchumi (Business/Finance)",
            "Fasihi na Ushairi (Literature/Poetry)"
        ], key="context_lang")
        
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi unayotaka kutafsiri hapa:", height=150, key="translate_input_pro")
    
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi ya kutafsiri kwanza!")
        else:
            with str_platform.spinner("Mtafsiri Mkuu wa AI anachambua muktadha..."):
                try:
                    trans_prompt = (
                        f"Wewe ni mtafsiri mwandamizi wa kimataifa na mtaalamu wa lugha. "
                        f"Tafsiri maandishi yafuatayo kutoka lugha ya {lugha_chanzo} kwenda lugha ya {lugha_lengwa}. "
                        f"Zingatia kwa makini sana muktadha wa matumizi ambao ni: {muktadha_tafsiri}. "
                        f"Hakikisha tafsiri inakuwa ya asili, yenye mtiririko mzuri na inayofaa ngazi hiyo ya muktadha:\n\n{maandishi_tafsiri}"
                    )
                    jibu_tafsiri = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": trans_prompt}]
                    )
                    str_platform.success(f"🔮 Matokeo ya Tafsiri ({muktadha_tafsiri}):")
                    str_platform.write(jibu_tafsiri.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Seva: {error_msg}")

# =====================================================================
# TAB 3: 📚 MAKTABA YA MSAMIATI NA NAHAU
# =====================================================================
with tab3:
    str_platform.header("📚 Maktaba ya Msamiati na Nahau")
    str_platform.write("Gundua maana ya misamiati migumu, methali, nahau, na tamathali za usemi za Kiswahili.")
    
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali (Mfano: 'Kitendawili', 'Kula chumvi nyingi'):", key="vocab_input_royal")
    
    if str_platform.button("Tafuta Maana", key="vocab_btn_royal"):
        if msamiati_input.strip() == "":
            str_platform.warning("Tafadhali andika msamiati kwanza!")
        else:
            with str_platform.spinner("AI anafungua kamusi za siri..."):
                try:
                    vocab_prompt = f"Wewe ni Kamusi Hai ya Kiswahili. Toa maana ya kina, asili ya neno, na mifano miwili ya sentensi kwa kutumia msamiati huu:\n\n{msamiati_input}"
                    jibu_vocab = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": vocab_prompt}]
                    )
                    str_platform.info("Uchambuzi wa Kamusi Kuu:")
                    str_platform.write(jibu_vocab.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Seva: {error_msg}")

# =====================================================================
# TAB 4: 🔊 MTAMBO WA SAUTI YA AI (DARASA LA SAUTI - MWALIMU & MWANAFUNZI)
# =====================================================================
with tab4:
    str_platform.header("🔊 Mtambo wa Sauti ya AI: Darasa la Kidijitali")
    str_platform.write("Zalisha sauti za kielimu zinazoiga mifano ya darasani kati ya Mwalimu anayefundisha na Mwanafunzi anayeitikia au kuuliza.")
    
    col_v1, col_v2 = str_platform.columns(2)
    with col_v1:
        sauti_mwalimu = str_platform.selectbox("Chagua Sauti ya Mwalimu (Lafudhi Nzito):", ["onyx", "echo", "alloy"], key="teacher_voice_opt")
        maandishi_mwalimu = str_platform.text_area("Andika Maelezo/Maswali ya Mwalimu:", "Karibu darasani mwanafunzi wangu. Leo tutajifunza matumizi sahihi ya viambishi vya Kiswahili Sanifu.", key="teacher_text_input")
        
    with col_v2:
        sauti_mwanafunzi_opt = str_platform.selectbox("Chagua Sauti ya Mwanafunzi (Lafudhi Laini):", ["nova", "shimmer", "fable"], key="student_voice_opt")
        maandishi_mwanafunzi = str_platform.text_area("Andika Majibu/Itikio la Mwanafunzi:", "Asante sana mwalimu wangu wa kifalme. Nipo tayari kabisa kusikiliza na kujifunza.", key="student_text_input")
    
    if str_platform.button("Zalisha Sauti za Darasa", key="tts_classroom_btn"):
        if maandishi_mwalimu.strip() == "" or maandishi_mwanafunzi.strip() == "":
            str_platform.warning("Tafadhali hakikisha umejaza maandishi ya mwalimu na mwanafunzi!")
        else:
            with str_platform.spinner("Mwalimu na Mwanafunzi wanaingia darasani..."):
                try:
                    # 👨‍🏫 1. Sauti ya Mwalimu
                    file_mwalimu = "sauti_mwalimu.mp3"
                    res_mwalimu = client.audio.speech.create(
                        model="tts-1",
                        voice=sauti_mwalimu,
                        input=maandishi_mwalimu
                    )
                    res_mwalimu.write_to_file(file_mwalimu)
                    str_platform.markdown("#### 👨‍🏫 Sauti ya Mwalimu:")
                    str_platform.audio(file_mwalimu)
                    
                    # 🧑‍🎓 2. Sauti ya Mwanafunzi
                    file_mwanafunzi = "sauti_mwanafunzi.mp3"
                    res_mwanafunzi = client.audio.speech.create(
                        model="tts-1",
                        voice=sauti_mwanafunzi_opt,
                        input=maandishi_mwanafunzi
                    )
                    res_mwanafunzi.write_to_file(file_mwanafunzi)
