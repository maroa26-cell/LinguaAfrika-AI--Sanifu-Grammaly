import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. UPAYAJI WA FUNGUO ZA SIRI NA USALAMA MAALUM (Enterprise Security)
load_dotenv()

st.set_page_config(page_title="LinguaAfrika AI", page_icon="👑", layout="wide")
st.title("👑 LinguaAfrika AI: The Ultimate Premium Masterpiece")
st.markdown("🔒 *Privacy Guard Active: Data zote zinasindikwa kwenye RAM na hazitumiwi kufundishia mifumo ya nje ya AI (No AI-Training Policy).*")
st.markdown("---")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.sidebar.header("🔑 Usalama wa Mfumo")
    api_key = st.sidebar.text_input("Ingiza OpenAI API Key yako hapa kwa usalama:", type="password")

if not api_key:
    st.sidebar.info("Tafadhali weka OpenAI API Key yako hapa kuanza.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2. MIFUMO YA TABO TANO KATI KATI YA SKRINI (Linear Stable Build)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Studio ya Mtafsiri Pacha (Global)", 
    "🎙️ AI Transcriber (Mahojiano & Tafiti)", 
    "📖 Kamusi ya Kiakademia & Ngeli", 
    "📝 Live Sanifu Grammarly Prompts",
    "🗣️ AI Phonetic Robot: Darasa la Lahaja"
])

# =====================================================================
# TAB 1: WORKSPACE (Side-by-Side Global Context Engine)
# =====================================================================
with tab1:
    st.header("📄 Studio ya Mtafsiri wa Kimataifa (Global Live Workspace)")
    st.caption("Tafsiri kwa muktadha thabiti kulingana na mpango kazi wetu wa kimkakati.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Matini ya Awali (Source Text)")
        text_to_translate = st.text_area("Andika au bandika (paste) maandishi yako hapa:", height=200, key="input_area")
        
        ORODHA_YA_LUGHA = [
            "Kiswahili", "Kiingereza", "Kifaransa", "Kireno", "Kiarabu", "Kichina", "Hindi", 
            "Kijapani", "Kihispania", "Kichewa", "Kinyanja", "Kinyarwanda", "Kiganda", "Kilingala", "Kizulu", "Kiafrikana"
        ]
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            lugha_chanzo = st.selectbox("Kutoka Lugha Gani (From):", ORODHA_YA_LUGHA, index=1)
        with col_lang2:
            lugha_lengwa = st.selectbox("Kwenda Lugha Gani (To):", ORODHA_YA_LUGHA, index=0)
            
        muktadha_sekta = st.selectbox(
            "Mtafsiri, unataka kufanya mradi wa aina gani leo?",
            ["Kawaida / Mazungumzo ya Jamii (General)",
             "Maandiko Matakatifu (Biblia, Quran au Kitheolojia)", 
             "Kisheria ya Mahakama na Mikataba (Legal/Contracts)", 
             "Vitabu vya Hadithi na Riwaya (Creative Fiction/Storytelling)",
             "Teknolojia, Uchumi na Tehama (Modern Tech/Finance)",
             "Kitiba, Sayansi na Afya (Medical/Sciences)"]
        )
        mtindo_lugha = st.selectbox("Sauti ya Mwandishi (Persona):", ["Ripoti Rasmi ya Kitaaluma", "Fasihi ya Ndani na Sanaa", "Lugha Rahisi ya Kuelimisha Jamii"])
        eneo_soko = st.selectbox("Chapa ya Kiswahili (Kama Kiswahili kipo):", ["Tanzania (Kiswahili Sanifu - BAKITA)", "Kenya (KICD Compliant)", "DRC / Congo Swahili"])
        faharasa_input = st.text_area("🔑 Faharasa ya Kudumu ya Mradi (Project Glossary):", value="Mungu=God\nMkataba=Contract", height=60)

    with col2:
        st.subheader("✏️ Matokeo ya Tafsiri ya Kimataifa (Inayoharirika)")
        if st.button("🔮 Anza Tafsiri ya Kiwango cha Dunia", key="doc_trans_btn"):
            if not text_to_translate.strip():
                st.warning("Tafadhali weka maandishi kwanza.")
            else:
                with st.spinner("LinguaAfrika AI inatafsiri kwa kufuata misingi ya mradi..."):
                    try:
                        instruction = f"Tafsiri kutoka {lugha_chanzo} kwenda {lugha_lengwa}. Mtindo: {mtindo_lugha}. Sekta: {muktadha_sekta}. Hakikisha upatanisho wa Ngeli ni 100% sahihi kwa Tanzania Swahili."
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "system", "content": instruction}, {"role": "user", "content": text_to_translate}],
                            temperature=0.0
                        )
                        st.session_state["raw_translation"] = response.choices.message.content
                    except Exception as e:
                        st.error(f"Hitilafu: {e}")
                        
        if "raw_translation" in st.session_state:
            st.text_area("Matokeo ya Tafsiri Safi:", value=st.session_state["raw_translation"], height=220, key="output_area_static")

# =====================================================================
# TAB 2: TRANSCRIBER
# =====================================================================
with tab2:
    st.header("2. AI Transcriber (Kusikiliza Sauti Kuwa Maandishi)")
    uploaded_file = st.file_uploader("Pandisha faili la sauti ya mahojiano au utafiti (mp3, wav, m4a):", type=["mp3", "wav", "m4a"])
    if uploaded_file and st.button("🚀 Anza Kuandika Sauti"):
        with st.spinner("AI Inasikiliza sauti..."):
            try:
                transcription = client.audio.transcriptions.create(model="whisper-1", file=(uploaded_file.name, uploaded_file.read()))
                st.write(transcription.text)
                st.success("Sauti imeandikwa kikamilifu!")
            except Exception as e:
                st.error(f"Hitilafu ya sauti: {e}")

# =====================================================================
# TAB 3: KAMUSI YA KIAKADEMIA & MATAMSHI SANIFU
# =====================================================================
with tab3:
    st.header("3. Kamusi Kuu ya Kiakademia na Mchambuzi wa Msamiati")
    word_to_lookup = st.text_input("Ingiza neno la Kiswahili kulichambua (Mfano: 'Mkataba'):", key="t3_input_word")
    if st.button("🔍 Chambua Neno", key="dict_btn") or word_to_lookup:
        if word_to_lookup.strip():
            with st.spinner("AI Inachimbua lugha na Ngeli..."):
                try:
                    prompt = f"Chambua neno '{word_to_lookup}' kwa kutoa Ngeli sahihi ya Tanzania, Maana ya Jumla, Visawe vya Kitaaluma, na asili ya neno (Etymology)."
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0
                    )
                    st.session_state["dict_result_text"] = response.choices.message.content
                    st.session_state["searched_dict_word"] = word_to_lookup
                except Exception as e:
                    st.error(f"Hitilafu ya kamusi: {e}")

    if "dict_result_text" in st.session_state:
        st.markdown(st.session_state["dict_result_text"])
        st.markdown("---")
        st.subheader("🔊 Matamshi Sanifu (Standard Pronunciation)")
        if st.button("🎙️ Cheza Sauti ya Neno Hili", key="play_dict_word_audio"):
            with st.spinner("AI Inatayarisha matamshi safi..."):
                try:
                    speech_word = client.audio.speech.create(
                        model="tts-1",
                        voice="nova",
                        input=f"Neno lenyewe linatamkwa hivi: {st.session_state['searched_dict_word']}"
                    )
                    st.audio(speech_word.content, format="audio/mp3")
                except Exception as e:
                    st.error(f"Tatizo la sauti: {e}")

# =====================================================================
# TAB 4: LIVE AUTONOMOUS SANIFU GRAMMARLY
# =====================================================================
with tab4:
    st.header("📝 Live Sanifu Grammarly Prompts")
    st.caption("Mfumo wa kwanza wa Autonomous Real-Time Prompts kwa ajili ya Kiswahili Sanifu cha Tanzania (BAKITA).")
    matini_ya_kukagua = st.text_area("Andika au bandika maandishi yako hapa (AI itakagua yenyewe kiotomatiki chini ikimaliza kusoma):", height=150, key="grammarly_input")
    
    if matini_ya_kukagua.strip():
        with st.spinner("Sanifu Grammarly inachambua Ngeli na sarufi papo hapo..."):
            try:
                grammarly_prompt = f"Wewe ni mfumo wa 'Sanifu Grammarly' kwa Kiswahili rasmi cha Tanzania (BAKITA). Kagua makosa ya sarufi na Ngeli katika matini hii: {matini_ya_kukagua}."
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": grammarly_prompt}],
                    temperature=0.0
                )
                st.info("💡 Mapendekezo ya Papo kwa Papo (Live Grammarly Prompt):")
                st.markdown(response.choices.message.content)
            except Exception as e:
                st.error(f"Hitilafu: {e}")

# =====================================================================
# TAB 5: MABORESHO YA KIFALME - SIDE-BY-SIDE GRID (Inajionyesha 100%)
# =====================================================================
with tab5:
    st.header("🗣️ AI Phonetic Robot: Darasa la Matamshi na Lahaja ya Tanzania")
    st.caption("Jifunze mkazo na jinsi Kiswahili kinavyozungumzwa mtaani na wazawa wa Tanzania.")
    st.markdown("---")
    
    col_t5_kushoto, col_t5_kulia = st.columns(2)
    
    with col_t5_kushoto:
        st.subheader("🎙️ Sehemu ya Mwanafunzi")
        st.caption("Rekodi sauti yako hapa chini, kisha bofya kitufe cha kukagua.")
        sauti_mwanafunzi = st.audio_input("Bofya mic uanze kuongea:", key="unique_mic_t5_royal")
        
        if sauti_mwanafunzi and st.button("🤖 Ruhusu Robot Akague Sauti Yako", key="check_student_speech_btn_royal"):
            with st.spinner("AI Robot wa Tanzania anasikiliza lafudhi yako..."):
                try:
                    trans_audio = client.audio.transcriptions.create(model="whisper-1", file=("mwanafunzi.wav", sauti_mwanafunzi.read()))
