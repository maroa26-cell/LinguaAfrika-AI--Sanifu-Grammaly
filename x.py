
import streamlit as str_platform

def execute_audio_muscle(client, sauti_mwalimu, maandishi_mwalimu, sauti_mwanafunzi, maandishi_mwanafunzi):
    """Executes the computationally intensive audio rendering pipeline via OpenAI Neural channels."""
    try:
        res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu)
        open("sauti_mwalimu.mp3", "wb").write(res_mwalimu.content)
        str_platform.audio("sauti_mwalimu.mp3")
        
        res_mwanafunzi = client.audio.speech.create(model="tts-1", voice=sauti_mwanafunzi, input=maandishi_mwanafunzi)
        open("sauti_mwanafunzi.mp3", "wb").write(res_mwanafunzi.content)
        str_platform.audio("sauti_mwanafunzi.mp3")
        str_platform.success("💪 Muscular system completed speech generation successfully.")
    except Exception as e:
        str_platform.error(f"🛑 Muscular system experienced data fracture: {str(e)}")

def execute_phonetic_muscle(client, sauti_faili):
    """Executes audio translation and parsing parameters through phonetic whisper nodes."""
    try:
        trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_faili.name, sauti_faili.read()))
        return trans_audio.text
    except Exception as e:
        return f"🛑 Fracture: {str(e)}"
