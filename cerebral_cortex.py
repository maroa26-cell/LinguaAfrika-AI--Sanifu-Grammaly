import streamlit as st
import tempfile
import os

class CerebralCortex:
    def __init__(self, client):
        self.client = client

    def chakata_sarufi_pro(self, maandishi):
        """📝 BROCA'S CRITIC CIRCUIT: Hyper-accurate grammar network"""
        messages_pipeline = [
            {
                "role": "system",
                "content": (
                    "You are the Broca's Area Neural Critic of Ourworthlinks BUSINESS. "
                    "Your performance exceeds human linguistic limits. Scan the input text "
                    "for deep syntax, semantic flaws, spelling errors, and style anomalies. "
                    "Provide a flawless output in professional Swahili, and append a concise "
                    "bulleted structural breakdown of the optimization changes made."
                )
            },
            {"role": "user", "content": maandishi.strip()}
        ]
        jibu = self.client.chat.completions.create(model="gpt-4o", messages=messages_pipeline, temperature=0.2)
        return jibu.choices.message.content

    def chakata_tafsiri_pacha(self, maandishi, chanzo, lengo, muktadha):
        """🔀 DUAL-STAGE LINGUISTIC HANDSHAKE: Context-Aware hyper-accurate translation matrix"""
        p1 = [
            {
                "role": "system",
                "content": (
                    f"You are the First-Stage Translator of Ourworthlinks BUSINESS. Translate from {chanzo} to {lengo}. "
                    f"Contextual Domain Target: {muktadha}. Focus completely on localization, semantic intent, "
                    "and preservation of business/legal nomenclature. Avoid word-for-word translation."
                )
            },
            {"role": "user", "content": maandishi.strip()}
        ]
        j1 = self.client.chat.completions.create(model="gpt-4o", messages=p1, temperature=0.3)
        tafsiri_kwanza = j1.choices.message.content

        p2 = [
            {
                "role": "system",
                "content": (
                    f"You are the Senior Editorial Quality Controller for Ourworthlinks BUSINESS. Optimize this initial translation "
                    f"from {chanzo} to {lengo} within the '{muktadha}' frame. Eradicate literal conversion traces, align "
                    "sentence sub-structures to executive standards, and ensure professional flow. Output ONLY the polished text."
                )
            },
            {"role": "user", "content": tafsiri_kwanza}
        ]
        j2 = self.client.chat.completions.create(model="gpt-4o", messages=p2, temperature=0.1)
        return j2.choices.message.content

    def chakata_kamusi_kuu(self, neno, database):
        """📚 RECURSIVE KNOWLEDGE LOOKUP: Semantic dictionary matrix expansion"""
        try:
            hit = database.query_neuroplasticity_lookup(neno)
            if hit:
                return f"<b>✨ Internal Core Memory Hit:</b><br><br>{hit}"
        except Exception:
            pass
        
        prompt = [
            {
                "role": "system",
                "content": (
                    "You are the Grand Dictionary Compiler of Ourworthlinks BUSINESS. Provide a deep, "
                    "academic, etymological, and practical contextual analysis of the requested Swahili word. "
                    "Break down its root origin, noun class (ngeli), synonyms, and provide real-world commercial usage examples."
                )
            },
            {"role": "user", "content": neno.strip()}
        ]
        jibu = self.client.chat.completions.create(model="gpt-4o", messages=prompt, temperature=0.2)
        return f"<b>✨ Super-Human Kamusi Core Expansion:</b><br><br>{jibu.choices.message.content}"

    def chakata_sauti_na_imla(self):
        """🎙️ AUDITORY CORTEX: OpenAI Whisper-v3 Hyper-Accurate Audio Pipeline"""
        st.markdown("<h3 style='color: #D97706;'>🎙️ Roboti wa Sauti, Imla (Transcription) & TTS Pro</h3>", unsafe_allow_html=True)
        st.write("Andaa au pakia faili la sauti hapa chini ili roboti alitafsiri kuwa maandishi safi mara moja:")

        # Lango la kupandisha faili la sauti (Audio Upload Input)
        audio_file = st.file_uploader("Pakia Faili la Sauti (MP3, WAV, M4A, au OGG):", type=["mp3", "wav", "m4a", "ogg"], key="whisper_audio_uploader")

        if audio_file is not None:
            # Muonekano wa sauti iliyopakiwa kuisikiliza
            st.audio(audio_file, format="audio/wav")
            
            if st.button("🚀 Zindua Roboti wa Sauti (Whisper-v3)"):
                with st.spinner("Mshipa wa Auditory Cortex unachakata mawimbi ya sauti..."):
                    try:
                        # Kutengeneza faili la muda (Temporary File) ili Whisper ipate kusoma kutoka kwenye diski
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
                            tmp_file.write(audio_file.read())
                            tmp_file_path = tmp_file.name

                        # Kutuma faili la sauti moja kwa moja kwenye OpenAI Whisper API
                        with open(tmp_file_path, "rb") as open_audio:
                            transcription = self.client.audio.transcriptions.create(
                                model="whisper-1", 
                                file=open_audio
                            )
                        
                        # Kufuta faili la muda baada ya kumaliza kuchakata
                        os.unlink(tmp_file_path)

                        # Kuonyesha matokeo ya Imla kwenye skrini kitalaalamu
                        st.success("✨ Imla Imekamilika kwa Kasi ya Radi!")
                        st.markdown(f"""
                        <div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 15px;'>
                            <b>🔮 Maandishi Yaliyotolewa Kwenye Sauti (Transcription):</b><br><br>
                            {transcription.text}
                        </div>
                        """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"💥 Hitilafu ya kuchakata sauti: {str(e)}")
