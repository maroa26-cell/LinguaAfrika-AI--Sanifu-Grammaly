import streamlit as str_platform
import model

def anzisha_mtafsiri(client):
    """Inasafirisha na kubadili maana ya data katika lugha 14 tofauti"""
    str_platform.markdown("<h2 style='color: #1E3A8A; font-weight: bold;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    str_platform.markdown("#### ⚙️ Hatua ya 1: Sanifu Njia ya Usafirishaji Data")
    col1, col2, col3 = str_platform.columns(3)
    
    orodha_lugha = [
        "Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", 
        "Kichewa (Chichewa)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", 
        "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", 
        "Kihindi (Hindi)", "Kifaransa (French)", "Kiarabu (Arabic)"
    ]
    
    with col1:
        lugha_chanzo = str_platform.selectbox("Kutoka Lugha (From Source):", orodha_lugha, index=1, key="src_lang_node")
    with col2:
        lugha_lengwa = str_platform.selectbox("Kwenda Lugha (To Target):", orodha_lugha, index=0, key="trg_lang_node")
    with col3:
        muktadha = str_platform.selectbox(
            "Muktadha wa Tafsiri:", 
            ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara", "Fasihi na Ushairi"],
            key="context_node"
        )
        
    str_platform.write("---")
    str_platform.markdown("#### 📝 Hatua ya 2: Ingiza Matini ya Kutafsiri")
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi yako hapa chini:", height=150, key="trans_text_node")
    
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="trigger_trans_launch_btn"):
        if maandishi_tafsiri.strip() != "":
            str_platform.info("🧠 Seli za Ubongo Zinasafirisha Data...")
            prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha} style:\n\n{maandishi_tafsiri.strip()}"
            matokeo = model.piga_gpt4o(client, prompt_t)
            str_platform.success(f"Tafsiri Imekamilika kwa Muktadha wa: {muktadha} ✨")
            str_platform.write(matokeo)
        else:
            str_platform.warning("⚠️ Tafadhali ingiza maandishi kwanza!")
