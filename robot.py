import streamlit as str_platform

def onyesha_robot(client):
    """
    IDARA YA 4: MUSCULAR-SKELETAL NODE 3 (PHONETIC EVALUATION)
    Roboti anasikiliza sauti ya mlaji na kutoa ripoti ya daktari wa lugha
    """
    str_platform.markdown("<h2 style='color: #1E3A8A; font-weight: bold;'>🤖 AI Phonetic Robot Enterprise Suite</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti hapa (Upload Audio):", type=["wav", "mp3"], key="audio_uploader_node")
    
    if sauti_mwanafunzi is not None:
        if str_platform.button("Zindua Ukaguzi Mkuu wa Roboti", key="check_student_speech_btn"):
            str_platform.info("🧠 Roboti anasikiliza lafudhi yako nyuma ya pazia...")
            
            trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read()))
            str_platform.info(f"🗣️ Robot amekusikia: '{trans_audio.text}'")
            
            robot_prompt = (
                f"Wewe ni mtaalamu wa fonetiki ya Kiswahili Sanifu. "
                f"Sentensi iliyotamkwa: '{trans_audio.text}'. "
                f"Toa ripoti rasmi ya fonetiki, mpe alama ya asilimia (0-100%) na ushauri wa kuboresha."
            )
            
            jibu_robot = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": robot_prompt}])
            str_platform.success("🔮 Ripoti Kuu ya Ukaguzi wa Roboti Imekamilika!")
            str_platform.write(jibu_robot.choices.message.content)
