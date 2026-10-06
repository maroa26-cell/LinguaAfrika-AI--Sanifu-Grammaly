import streamlit as str_platform

def onyesha_sauti(client):
    """
    IDARA YA 4: MUSCULAR-SKELETAL NODE 2 (AUDIO TTS)
    Inazalisha sauti safi za darasa la kidijitali kwa ushirikiano wa OpenAI
    """
    str_platform.markdown("<h2 style='color: #1E3A8A; font-weight: bold;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    sauti_mwalimu = str_platform.selectbox("Sauti ya Mwalimu (Teacher Voice):", ["onyx", "echo", "alloy"], key="voice_t_node")
    maandishi_mwalimu = str_platform.text_area("Mwalimu Maelezo (Teacher Text):", "Karibu darasani mwanafunzi wangu.", key="teacher_text_node")
    
    sauti_mwanafunzi_opt = str_platform.selectbox("Sauti ya Mwanafunzi (Student Voice):", ["nova", "shimmer", "fable"], key="voice_s_node")
    maandishi_mwanafunzi = str_platform.text_area("Mwanafunzi Maelezo (Student Text):", "Asante sana mwalimu wangu.", key="student_text_node")
    
    if str_platform.button("Zalisha Sauti za Darasa Direct", key="perfect_audio_btn"):
        if maandishi_mwalimu.strip() != "" and maandishi_mwanafunzi.strip() != "":
            str_platform.info("🧠 Ubongo unazalisha misuli ya sauti... Tafadhali subiri.")
            
            res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu.strip())
            open("sauti_mwalimu.mp3", "wb").write(res_mwalimu.content)
            str_platform.audio("sauti_mwalimu.mp3")
            
            res_mwanafunzi = client.audio.speech.create(model="tts-1", voice=sauti_mwanafunzi_opt, input=maandishi_mwanafunzi.strip())
            open("sauti_mwanafunzi.mp3", "wb").write(res_mwanafunzi.content)
            str_platform.audio("sauti_mwanafunzi.mp3")
        else:
            str_platform.warning("⚠️ Tafadhali hakikisha umejaza visanduku vyote viwili vya matini!")
