import streamlit as str_platform

def onyesha_admin(client, api_key_source):
    str_platform.markdown("<h3 style='color: #D97706;'>📊 Jopo la Msimamizi (System Operations Hub)</h3>", unsafe_allow_html=True)
    str_platform.success("🔓 Karibu Mkuu Maroa! Mifumo yote ipo chini ya uangalizi wako kiofisi.")
    
    col_s1, col_s2, col_s3 = str_platform.columns(3)
    with col_s1:
        str_platform.info("🧠 **AI Core (GPT-4o)**\n\nStatus: Online (100%)\n\nNode: Enterprise Corporate")
    with col_s2:
        str_platform.info("🔊 **TTS Engine**\n\nStatus: Imara\n\nNode: OpenAI TTS-1 Node")
    with col_s3:
        str_platform.info("🌐 **Host Server**\n\nStatus: Secure\n\nNode: Streamlit Global Cloud")
