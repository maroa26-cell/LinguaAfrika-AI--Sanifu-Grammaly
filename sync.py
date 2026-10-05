import streamlit as str_platform
import model

def anzisha_mtafsiri(client):
    """
    IDARA YA 3: USANIFU WA MFUMO WA USAFIRISHAJI DATA (CIRCULATORY & TRANSPORT SYSTEM)
    Inatawala na kusafirisha maana ya maneno kutoka lugha moja kwenda nyingine kiotomatiki
    """
    # 👑 Vichwa vya Habari kwa Vipengele Husika (Executive Headings)
    str_platform.markdown("<h2 style='color: #1E3A8A; font-weight: bold;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h2>", unsafe_allow_html=True)
    str_platform.markdown("<p style='color: #64748B; font-size: 15px;'>Injini Kuu ya Usafirishaji wa Maudhui katika Lugha 14 za Kimataifa na Kidini</p>", unsafe_allow_html=True)
    str_platform.write("---")
    
    # 🌍 Mipangilio ya Usafirishaji (Lugha na Muktadha Configuration Layout)
    str_platform.markdown("#### ⚙️ Hatua ya 1: Sanifu Njia ya Usafirishaji Data")
    col1, col2, col3 = str_platform.columns(3)
    
    # Orodha Kamili ya Lugha zetu 14 za Kimkakati duniani
    orodha_lugha = [
        "Kiswahili", 
        "Kiingereza (English)", 
        "Kinyarwanda", 
        "Kiganda (Luganda)", 
        "Kichewa (Chichewa)", 
        "Kinyanja", 
        "Kiafrikana (Afrikaans)", 
        "Kilingala (Lingala)", 
        "Kiamhari (Amharic)", 
        "Kichina (Chinese)", 
        "Kireno (Portuguese)", 
        "Kihindi (Hindi)", 
        "Kifaransa (French)", 
        "Kiarabu (Arabic)"
    ]
    
    with col1:
        lugha_chanzo = str_platform.selectbox("Kutoka Lugha (From Source):", orodha_lugha, index=1, key="src_lang_select")
    with col2:
        lugha_lengwa = str_platform.selectbox("Kwenda Lugha (To Target):", orodha_lugha, index=0, key="trg_lang_select")
    with col3:
        muktadha = str_platform.selectbox(
            "Muktadha wa Tafsiri (Semantic Context):", 
            ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara", "Fasihi na Ushairi"],
            key="context_select"
        )
        
    str_platform.write("---")
    
    # 📝 Eneo la Kuchakata Data (Processing Area)
    str_platform.markdown("#### 📝 Hatua ya 2: Ingiza Matini ya Kutafsiri")
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi yako hapa chini:", height=150, key="translate_text_area_node")
    
    # 💥 Kitufe Kuu cha Utendaji (Muscular Trigger Button)
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="launch_enterprise_translation_btn"):
        if maandishi_tafsiri.strip() != "":
            str_platform.info("🧠 Seli za Ubongo Zinasafirisha Data... Tafadhali subiri sekunde chache.")
            
            # Kusuka Prompt ya Kijeshi inayoamrisha AI kufuata lugha na muktadha sahihi
            prompt_ya_mtafsiri = (
                f"Wewe ni Mtafsiri Mkuu Mwandamizi na Daktari wa Lugha duniani. "
                f"Tafsiri matini yafuatayo kutoka lugha ya {lugha_chanzo} kwenda lugha ya {lugha_lengwa}. "
                f"HAKIKISHA unafuata kwa ukamilifu muktadha wa kimaandishi wa '{muktadha}'. "
                f"Toa matokeo ya tafsiri pekee yaliyonyooka na nadhifu bila maelezo ya ziada ya ziada.\n\n"
                f"Matini ya kutafsiri:\n{maandishi_tafsiri}"
            )
            
            # Kuchochea faili la model.py kupiga OpenAI GPT-4o Seva kiusalama
            matokeo_tafsiri = model.piga_gpt4o(client, prompt_ya_mtafsiri)
            
            # 🔮 Kuonyesha Matokeo ya Ushindi kwa Mlaji
            str_platform.write("---")
            str_platform.markdown("#### 🔮 Hatua ya 3: Matokeo ya Tafsiri ya Kitaalamu")
            str_platform.success(f"Tafsiri Imekamilika kwa Muktadha wa: {muktadha} ✨")
            str_platform.write(matokeo_tafsiri)
        else:
            str_platform.warning("⚠️ Tafadhali ingiza maandishi kwanza kwenye sanduku la juu!")
