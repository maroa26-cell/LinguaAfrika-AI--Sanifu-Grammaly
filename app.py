import streamlit as str_platform
import os
from openai import OpenAI

# 👑 Sanifu Mipangilio ya Ukurasa wa Kifalme - Ngazi ya Enterprise Omnichannel Suite
str_platform.set_page_config(
    page_title="LinguaAfrika AI: Ultra Premium Super Masterpiece Edition 2",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 Kichocheo cha Usalama wa Siri (.env / Streamlit Secrets Enterprise)
if "OPENAI_API_KEY" in os.environ:
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets:
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else:
    api_key_source = None

# Kuwasha mtambo OpenAI Suite
if api_key_source:
    client = OpenAI(api_key=api_key_source)
else:
    str_platform.error("🔒 Hitilafu ya Usalama: Ufunguo wa siri wa OpenAI (OPENAI_API_KEY) haujapatikana kwenye mifumo ya Secrets!")
    str_platform.stop()

# 🎨 UPANDISHAJI WA MUONEKANO NA RANGI (EDITION 2 ENTERPRISE CSS INJECTION)
str_platform.markdown("""
<style>
    /* Muonekano wa Jukwaa Mkuu */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAFAFA !important;
        font-family: 'Helvetica Neue', sans-serif !important;
    }
    
    /* 🏰 USANIFU WA KIFALME WA MENYU YA PEMBENI (SIDEBAR ULTRA UPGRADE) */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
        color: #ffffff !important;
        border-right: 3px solid #D97706 !important;
    }
    
    /* Maandishi yote ya ndani ya Sidebar yawe meupe safi */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Sanifu Vifungo vya Radio Buttons vya Ndani ya Sidebar ya Enterprise */
    div[data-testid="stRadio"] > label {
        background-color: rgba(255, 255, 255, 0.05) !important;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease-in-out !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        cursor: pointer !important;
    }
    
    /* Mihemko ya Vifungo vya Menyu pindi Vinapoguswa (Hover) */
    div[data-testid="stRadio"] > label:hover {
        background-color: rgba(217, 119, 6, 0.15) !important;
        border-color: #D97706 !important;
    }
    
    /* Kitufe Kilichochaguliwa Kilipuke kwa Dhahabu ya Kifalme */
    div[data-testid="stRadio"] div[aria-checked="true"] {
        background-color: #D97706 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }
    
    /* Sanifu Vifungo Vyote vya Programu Katikati ya Skrini */
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.15) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #D97706 !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(217, 119, 6, 0.3) !important;
    }
    textarea, input {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🏰 Muonekano wa Juu wa Jukwaa la Kimataifa (Edition 2 Corporate Header)
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: \"Helvetica Neue\", sans-serif; font-weight: 800; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-family: \"Helvetica Neue\", sans-serif; font-weight: 600; margin-top: 5px;'>The Ultra Premium Super Masterpiece • Edition 2</h3>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; font-size: 1.2rem; color: #4B5563; max-width: 850px; margin: 0 auto; line-height: 1.6;'>Mfumo mkuu wa kimkakati wa akili mnemba (AI) uliosajiliwa kusanifisha sarufi, kutafsiri lugha 14, na kukagua lafudhi ya Lugha ya Kiswahili duniani kwa kiwango cha kibiashara na kiofisi.</p>", unsafe_allow_html=True)
str_platform.write("---")

# 🧭 UNDAJI WA MENYI YA PEMBENI YA KIFALME (PREMIUM SideBar SUITE)
str_platform.sidebar.markdown("<h1 style='color: #ffffff; text-align: center; font-size: 28px; margin-bottom: 0;'>👑</h1>", unsafe_allow_html=True)
str_platform.sidebar.markdown("<h2 style='color: #ffffff; text-align: center; font-weight: bold; margin-top: 0; font-size: 22px;'>LinguaAfrika AI</h2>", unsafe_allow_html=True)
str_platform.sidebar.markdown("<p style='color: #E5E7EB; text-align: center; font-size: 12px; font-style: italic;'>Enterprise Menu Suite</p>", unsafe_allow_html=True)
str_platform.sidebar.write("---")

chaguo_menyu = str_platform.sidebar.radio(
    "CHAGUA HUDUMA KUU:",
    [
        "📝 Mhariri wa Kiswahili Sanifu Pro",
        "🔀 Mtafsiri wa Lugha & Muktadha Suite",
        "📚 Maktaba ya Msamiati na Nahau Kuu",
        "🔊 Mtambo wa Sauti (Darasa la Sauti)",
        "🤖 AI Phonetic Robot (Ukaguzi Mkuu)"
    ]
)

# =====================================================================
# CHAGUO 1: MHARIRI WA KISWAHILI SANIFU PRO
# =====================================================================
if chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    str_platform.write("Ingiza maandishi yako ya Kiswahili hapa chini ili AI ya Ngazi ya Enterprise yakubalie kurekebisha sarufi, tahajia, na mtiririko kulingana na miongozo ya Baraza la Kiswahili.")
    maandishi_mhariri = str_platform.text_area("Andika maandishi yako hapa:", height=150, key="editor_input_royal")
    
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="editor_btn_royal"):
        if maandishi_mhariri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            with str_platform.spinner("AI Enterprise anachambua sarufi..."):
                pro_prompt = f"Wewe ni mtaalamu mwandamizi wa lugha ya Kiswahili Sanifu. Kagua maandishi haya, sahihisha makosa yote ya sarufi na tahajia, kisha ulete majibu nadhifu yakionyesha marekebisho yaliyofanyika:\n\n{maandishi_mhariri}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": pro_prompt}])
                str_platform.success("Marekebisho ya Kiofisi Yamekamilika!")
                str_platform.write(jibu.choices.message.content)

# =====================================================================
# CHAGUO 2: MTAFSIRI WA LUGHA & MUKTADHA SUITE (14 LUGHA + KIDINI)
# =====================================================================
elif chaguo_menyu == "🔀 Mtafsiri wa Lugha & Muktadha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
    str_platform.write("Mfumo wa tafsiri ya kimataifa unaounga mkono lugha 14 za kimkakati pamoja na muktadha maalum.")
    
    orodha_lugha = [
        "Kiswahili", "Kiingereza (English)", "Kichewa (Chichewa)", "Kinyarwanda", 
        "Kiganda (Luganda)", "Kinyanja", "Kiafrikana (Afrikaans)", "Kilingala (Lingala)", 
        "Kiamhari (Amharic)", "Kichina (Chinese)", "Kireno (Portuguese)", "Kihindi (Hindi)",
        "Kifaransa (French)", "Kiarabu (Arabic)"
    ]
    
    col1, col2, col3 = str_platform.columns(3)
    with col1:
        lugha_chanzo = str_platform.selectbox("Lugha ya Chanzo (From):", orodha_lugha, index=1, key="src_lang")
    with col2:
        lugha_lengwa = str_platform.selectbox("Lugha Lengwa (To):", orodha_lugha, index=0, key="tgt_lang")
    with col3:
        muktadha_tafsiri = str_platform.selectbox("Muktadha wa Matumizi (Context):", ["Mazungumzo ya Kawaida", "Kiakademia na Shule", "Kidini na Kiimani", "Kisheria na Kiofisi", "Kibiashara", "Fasihi na Ushairi"], key="context_lang")
        
    maandishi_tafsiri = str_platform.text_area("Ingiza maandishi unayotaka kutafsiri hapa:", height=150, key="translate_input_pro")
    
    if str_platform.button("Zindua Tafsiri ya Kitaalamu", key="translate_btn_pro"):
        if maandishi_tafsiri.strip() == "":
            str_platform.warning("Tafadhali ingiza maandishi kwanza!")
        else:
            with str_platform.spinner("Mtafsiri Mkuu wa Enterprise anachambua lugha..."):
                trans_prompt = f"Tafsiri kutoka {lugha_chanzo} kwenda {lugha_lengwa} katika muktadha wa {muktadha_tafsiri}:\n\n{maandishi_tafsiri}"
                jibu_tafsiri = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": trans_prompt}])
                str_platform.success(f"🔮 Matokeo ya Tafsiri ya Kiwango cha Juu ({muktadha_tafsiri}):")
                str_platform.write(jibu_tafsiri.choices.message.content)

# =====================================================================
# CHAGUO 3: MAKTABA YA MSAMIATI NA NAHAU KUU
# =====================================================================
elif chaguo_menyu == "📚 Maktaba ya Msamiati na Nahau Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Nahau Kuu</h3>", unsafe_allow_html=True)
    str_platform.write("Gundua na uchambue maana ya misamiati migumu, methali, nahau, na tamathali za usemi.")
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali (Mfano: 'Kitendawili', 'Kula chumvi nyingi'):", key="vocab_input_royal")
    
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="vocab_btn_royal"):

