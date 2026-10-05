import streamlit as str_platform

def onyesha_robot(client):
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🤖 AI Phonetic Robot Enterprise Suite</h3>", unsafe_allow_html=True)
    sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti hapa:", type=["wav", "mp3"], key="audio_uploader_royal_final")
    
    if sauti_mwanafunzi is not None:
        if str_platform.button("Zindua Ukaguzi Mkuu wa Roboti", key="check_student_speech_btn_royal_final"):
            trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read()))
            str_platform.info(f"🗣️ Robot amekusikia: '{trans_audio.text}'")
            robot_prompt = f"Wewe ni mtaalamu wa fonetiki ya Kiswahili Sanifu. Sentensi: '{trans_audio.text}'. Toa ripoti na % Score."
            jibu_robot = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": robot_prompt}])
            str_platform.success("🔮 Ripoti Kuu ya Ukaguzi wa Roboti:")
            str_platform.write(jibu_robot.choices.message.content)
