import streamlit as str_platform

def onyesha_sauti(client):
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔊 Mtambo wa Sauti: Darasa la Kidijitali</h3>", unsafe_allow_html=True)
    sauti_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
    maandishi_mwalimu = str_platform.text_area("Mwalimu Maelezo:", "Karibu darasani mwanafunzi wangu.", key="t_text")
    sauti_mwanafunzi_opt = str_platform.selectbox("Sauti ya Mwanafunzi:", ["nova", "shimmer", "fable"])
    maandishi_mwanafunzi = str_platform.text_area("Mwanafunzi Maelezo:", "Asante sana mwalimu wangu.", key="s_text")
    
    if str_platform.button("Zalisha Sauti za Darasa Direct", key="perfect_audio_btn"):
        if  maandishi_mwalimu.strip() != "" and  maandishi_mwanafunzi.strip() != "":
            res_mwalimu = client.audio.speech.create(model="tts-1", voice=sauti_mwalimu, input=maandishi_mwalimu)
            open("sauti_mwalimu.mp3", "wb").write(res_mwalimu.content)
            str_platform.audio("sauti_mwalimu.mp3")
            res_mwanafunzi = client.audio.speech.create(model="tts-1", voice=sauti_mwanafunzi_opt, input=maandishi_mwanafunzi)
            open("sauti_mwanafunzi.mp3", "wb").write(res_mwanafunzi.content)
            str_platform.audio("sauti_mwanafunzi.mp3")
