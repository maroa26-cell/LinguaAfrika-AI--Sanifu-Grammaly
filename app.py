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
    "🔀 Mtafsiri wa Kiingereza - Kiswahili", 
    "📚 Maktaba ya Msamiati na Nahau", 
    "🔊 Mtambo wa Sauti ya AI (Text-to-Speech)", 
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
                    pro_prompt = f"Wewe ni mtaalamu mwandamizi wa lugha ya Kiswahili Sanifu. Kagua maandishi haya, sahihisha makosa yote ya sarufi na tahajia, kisha ulete majibu nadhifu yakionyesha marekebisho yaliyofanyika:\n\n{maandishi_mhariri}"
                    jibu = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": pro_prompt}]
                    )
                    str_platform.success("Marekebisho Yamekamilika!")
                    str_platform.write(jibu.choices[0].message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Seva: {error_msg}")

# =====================================================================
# TAB 2: 🔀 MTAFSIRI WA KIINGREZA - KISWAHILI
# =====================================================================
with tab2:
    str_platform.header("🔀 Mtafsiri wa Kiingereza - Kiswahili")
    str_platform.write("Tafsiri makala, sentensi, au maneno kutoka Kiingereza kwenda Kiswahili cha Ngazi ya Juu.")
    
    maandishi_tafsiri = str_platform.text_area("Ingiza Maandishi ya Kiingereza (English Text):", height=150, key="translate_input_royal")
    
    if str_platform.button("Tafsiri Sasa", key="translate_btn_royal"):
        if maandishi_tafsiri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi ya Kiingereza kwanza!")
        else:
            with str_platform.spinner("Mtafsiri wa AI anageuza lugha..."):
                try:
                    trans_prompt = f"Translate the following English text into native, elegant, and standard Swahili (Kiswahili Sanifu):\n\n{maandishi_tafsiri}"
                    jibu_tafsiri = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": trans_prompt}]
                    )
                    str_platform.success("Tafsiri ya Kifalme:")
                    str_platform.write(jibu_tafsiri.choices[0].message.content)
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
                    str_platform.write(jibu_vocab.choices[0].message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Seva: {error_msg}")

# =====================================================================
# TAB 4: 🔊 MTAMBO WA SAUTI YA AI (TEXT-TO-SPEECH)
# =====================================================================
with tab4:
    str_platform.header("🔊 Mtambo wa Sauti ya AI (Text-to-Speech)")
    str_platform.write("Badilisha maandishi yako ya Kiswahili kuwa sauti safi ya roboti wa AI anayetamka lafudhi ya Tanzania.")
    
    maandishi_sauti = str_platform.text_area("Andika maandishi unayotaka yatamkwe kwa sauti:", height=100, key="tts_input_royal")
    uchaguzi_sauti = str_platform.selectbox("Chagua Aina ya Sauti ya AI:", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], key="tts_voice_royal")
    
    if str_platform.button("Tengeneza Sauti", key="tts_btn_royal"):
        if maandishi_sauti.strip() == "":
            str_platform.warning("Tafadhali andika maandishi kwanza!")
        else:
            with str_platform.spinner("Roboti wa AI anafanya mazoezi ya kuongea..."):
                try:
                    fayli_sauti = "sauti_kifalme.mp3"
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice=uchaguzi_sauti,
                        input=maandishi_sauti
                    )
                    response.stream_to_file(fayli_sauti)
                    str_platform.success("Sauti ya AI Ipo Tayari!")
                    str_platform.audio(fayli_sauti)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Mtambo wa Sauti: {error_msg}")

# =====================================================================
# TAB 5: 🤖 AI PHONETIC ROBOT (UKAGUZI WA LAFUDHI)
# =====================================================================
with tab5:
    str_platform.header("🤖 AI Phonetic Robot (Ukaguzi wa Lafudhi)")
    str_platform.write("Mzee wangu, hapa ndipo mtambo mkuu wa sauti ulipolala. Rekodi au pakia faili la sauti (.wav/.mp3) ili AI robot akague lafudhi na usahihi wa matamshi yako ya Kiswahili.")
    
    sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti ya mazoezi hapa:", type=["wav", "mp3"], key="audio_uploader_royal")
    
    if sauti_mwanafunzi and str_platform.button("🤖 Ruhusu Robot Akague Sauti Yako", key="check_student_speech_btn_royal_final"):
        with str_platform.spinner("AI Robot wa Tanzania anasikiliza lafudhi yako..."):
            try:
                # 🛠️ MSTARI WA 182 SOMA NA KUNAKILI AUDIO SAFU
                trans_audio = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read())
                )
                str_platform.info(f"🗣️ Robot amekusikia ukisema: '{trans_audio.text}'")
                
                # Uchambuzi wa kiwango cha matamshi
                robot_prompt = f"Mwanafunzi ametamka sentensi hii: '{trans_audio.text}'. Wewe kama mtaalamu wa fonetiki ya Kiswahili, toa ripoti fupi ya usahihi wa lafudhi yake, mpe asilimia ya alama (% Score kutoka 0-100), na mpe ushauri mmoja wa kuboresha matamshi."
                jibu_robot = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": robot_prompt}]
                )
                str_platform.success("🔮 Ripoti ya Ukaguzi wa Lafudhi ya Roboti:")
                str_platform.write(jibu_robot.choices[0].message.content)
                
            except Exception as error_msg:
                str_platform.error(f"Hitilafu ya Ukaguzi wa Sauti: {error_msg}")

# 🏰 Maandishi ya Chini ya Mamlaka ya Kifalme
str_platform.write("---")
