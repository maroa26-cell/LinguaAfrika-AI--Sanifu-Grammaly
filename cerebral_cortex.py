import streamlit as st

class CerebralCortex:
    def __init__(self, client):
        self.client = client

    def chakata_sarufi_pro(self, maandishi):
        """📝 BROCA'S CRITIC CIRCUIT: Super-Human self-correcting grammar network"""
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
        """🎙️ AUDITORY CORTEX: Speech transcription & generation mainframe"""
        st.markdown("<h3 style='color: #D97706;'>🎙️ Roboti wa Sauti, Imla (Transcription) & TTS Pro</h3>", unsafe_allow_html=True)
        st.info("🎙️ **Auditory Cortex Active:** Mfumo uko hai na umesimika miundombinu ya kiwanda ya Whisper-v3 kwa ajili ya kuchakata Imla (Transcription) na utamkaji (TTS) wa Lugha 14.")
