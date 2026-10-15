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
                    "Provide a flawless output in professional Swahili."
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
                "content": f"Translate from {chanzo} to {lengo} within a '{muktadha}' frame. Avoid word-for-word translation."
            },
            {"role": "user", "content": maandishi.strip()}
        ]
        j1 = self.client.chat.completions.create(model="gpt-4o", messages=p1, temperature=0.3)
        
        p2 = [
            {
                "role": "system",
                "content": f"Review this initial translation from {chanzo} to {lengo} for '{muktadha}' executive fluency. Output ONLY the polished text."
            },
            {"role": "user", "content": j1.choices.message.content}
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
                "content": "You are the Grand Dictionary Compiler of Ourworthlinks BUSINESS. Provide a deep definition, synonyms, and business usage examples of the Swahili word."
            },
            {"role": "user", "content": neno.strip()}
        ]
        jibu = self.client.chat.completions.create(model="gpt-4o", messages=prompt, temperature=0.2)
        return f"<b>✨ Super-Human Kamusi Core Expansion:</b><br><br>{jibu.choices.message.content}"

    def chakata_sauti_na_imla(self, audio_file):
        """🎙️ AUDITORY CORTEX: OpenAI Whisper-v3 Hyper-Accurate Audio Pipeline"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name

        with open(tmp_file_path, "rb") as open_audio:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=open_audio
            )
        os.unlink(tmp_file_path)
        return transcription.text

    def zindua_jifunze_lugha_audio(self, maandishi, lugha_lengwa):
        """🔊 AUDIO LINGUISTIC TUTOR: Text-to-Speech (TTS) voice generation for premium language learning"""
        # Inazalisha sauti asilia (High-Fidelity) kutoka kwenye maandishi ili mteja ajifunze matamshi sahihi
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy", # Sauti ya kiofisi na yenye hisia za kibinadamu
            input=f"Hapa kuna jinsi ya kutamka kwa usahihi katika lugha ya {lugha_lengwa}: {maandishi}"
        )
        return response.content
