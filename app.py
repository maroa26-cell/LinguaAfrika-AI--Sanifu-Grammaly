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
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI (OPENAI_API_KEY) haujapatikana kwenye mifumo ya Secrets!")
    str_platform.stop()

# 🏰 Muonekano wa Juu wa Jukwaa la Kimataifa (Enterprise Corporate Header)
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: \"Helvetica Neue\", sans-serif; font-weight: 800;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: \"Helvetica Neue\", sans-serif;'>The Ultra Premium Super Masterpiece Enterprise Edition</h3>", unsafe_allow_html=True)
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
    str_platform.write("Ingiza maandishi yako ya Kiswahili hapa chini ili AI ya Ngazi ya Enterprise yakubalie kurekebisha sarufi, tahajia, na mtiririko kulingana na miongozo ya Baraza la Kiswahili.")
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            with str_platform.spinner("AI Enterprise anachambua sarufi..."):
                try:
                    pro_prompt = f"Wewe ni mtaalamu mwandamizi wa lugha ya Kiswahili Sanifu. Kagua maandishi haya, sahihisha makosa yote ya sarufi na tahajia, kisha ulete majibu nadhifu yakionyesha marekebisho yaliyofanyika:\n\n{maandishi_mhariri}"
                    jibu = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": pro_prompt}]
                    )
                    str_platform.success("Marekebisho ya Kiofisi Yamekamilika!")
                    str_platform.write(jibu.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Mfumo: {error_msg}")

# =====================================================================
# TAB 2: 🔀 MTAFSIRI WA LUGHA & MUKTADHA SUITE (14 LUGHA + KIDINI)
# =====================================================================
with tab2:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    str_platform.write("Mfumo wa tafsiri ya kimataifa unaounga mkono lugha 14 za kimkakati pamoja na muktadha maalum.")
    
    orodha_lugha = [
        "Kiswahili", "Kiingereza (English)", "Kichewa (Chichewa)", "Kinyarwanda", 
        "Kiganda (Luganda)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", 
        "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kihindi (Hindi)",
        "Kifaransa (French)", "Kiarabu (Arabic)"
    ]
    
    col1, col2, col3 = str_platform.columns(3)
    with col1:
        lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1, key="src_lang")
    with col2:
        lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0, key="tgt_lang")
    with col3:
        muktadha_tafsiri = str_platform.selectbox("Muktadha wa Matumizi (Context):", [
            "Mazungumzo ya Kawaida (Casual Conversation)", "Kiakademia na Shule (Academic/Educational)",
            "Kidini na Kiimani (Religious/Faith-Based)", "Kisheria na Kiofisi (Legal/Official Documentation)",
            "Kibiashara na Kiuchumi (Business/Finance)", "Fasihi na Ushairi (Literature/Poetry)"
        ], key="context_lang")
        
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi unayotaka kutafsiri hapa:", height=150, key="translate_input_pro")
    
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi ya kutafsiri kwanza!")
        else:
            with str_platform.spinner("Mtafsiri Mkuu wa Enterprise anachambua lugha..."):
                try:
                    trans_prompt = (
                        f"Wewe ni mtafsiri mwandamizi wa kimataifa na mtaalamu wa lugha. "
                        f"Tafsiri maandishi yafuatayo kutoka lugha ya {lugha_chanzo} kwenda lugha ya {lugha_lengwa}. "
                        f"Zingatia kwa makini sana muktadha wa matumizi ambao ni: {muktadha_tafsiri}. "
                        f"Hakikisha tafsiri inakuwa ya kiwango cha juu, ya asili, na mtiririko unaofaa ngazi hiyo ya muktadha:\n\n{maandishi_tafsiri}"
                    )
                    jibu_tafsiri = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": trans_prompt}]
                    )
                    str_platform.success(f"🔮 Matokeo ya Tafsiri ya Kiwango cha Juu ({muktadha_tafsiri}):")
                    str_platform.write(jibu_tafsiri.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Mfumo: {error_msg}")

# =====================================================================
# TAB 3: 📚 MAKTABA YA MSAMIATI NA NAHAU KUU
# =====================================================================
with tab3:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Nahau Kuu</h3>", unsafe_allow_html=True)
    str_platform.write("Gundua na uchambue maana ya misamiati migumu, methali, nahau, na tamathali za usemi.")
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali (Mfano: 'Kitendawili', 'Kula chumvi nyingi'):", key="vocab_input_royal")
    
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="vocab_btn_royal"):
        if msamiati_input.strip() == "":
            str_platform.warning("Tafadhali andika msamiati kwanza!")
        else:
            with str_platform.spinner("AI anatafuta kwenye kamusi kuu..."):
                try:
                    vocab_prompt = f"Wewe ni Kamusi Hai Kuu ya Kiswahili ya kiwango cha juu. Toa maana ya kina, asili ya neno, na mifano miwili ya sentensi kwa kutumia msamiati huu:\n\n{msamiati_input}"
                    jibu_vocab = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": vocab_prompt}]
                    )
                    str_platform.info("Uchambuzi wa Kitaalamu wa Kamusi Kuu:")
                    str_platform.write(jibu_vocab.choices.message.content)
                except Exception as error_msg:
                    str_platform.error(f"Hitilafu ya Mfumo: {error_msg}")

# =====================================================================
# TAB 4: 🔊 MTAMBO WA SAUTI (DARASA LA SAUTI - NO TRY BLOCK!)
# =====================================================================
with tab4:
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    str_platform.write("Zalisha faili za sauti za kielimu zinazoiga mifano ya darasani kati ya Mwalimu na Mwanafunzi.")
    
    col_v1, col_v2 = str_platform.columns(2)
    with col_v1:
        sauti_mwalimu = str_platform.selectbox("Chagua Sauti ya Mwalimu:", ["onyx", "echo", "alloy"], key="teacher_voice_opt")
        maandishi_mwalimu = str_platform.text_area("Andika Maelezo ya Mwalimu:", "Karibu darasani mwanafunzi wangu. Leo tutajifunza matumizi sahihi ya viambishi vya Kiswahili Sanifu.", key="teacher_text_input")
    with col_v2:
        sauti_mwanafunzi_opt = str_platform.selectbox("Chagua Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"], key="student_voice_opt")
        maandishi_mwanafunzi = str_platform.text_area("Andika Majibu ya Mwanafunzi:", "Asante sana mwalimu wangu wa kifalme. Nipo tayari kabisa kusikiliza na kujifunza.", key="student_text_input")
    
    if str_platform.button("Zalisha Sauti za Darasa", key="tts_classroom_btn"):
        if maandishi_mwalimu.strip() == "" or maandishi_mwanafunzi.strip() == "":
            str_platform.warning("Tafadhali hakikisha umejaza maandishi yote mawili!")
        else:
            with str_platform.spinner("Mtambo wa sauti unaoka sauti..."):
