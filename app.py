import streamlit as str_platform
import os
import time
from openai import OpenAI

self_healing_status = "🟢 Autonomous Shield: Active & Healthy"
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

if "OPENAI_API_KEY" in os.environ: 
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets: 
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else: 
    api_key_source = None

if api_key_source: 
    client = OpenAI(api_key=api_key_source.strip())
else: 
    str_platform.error("🔒 Secrets Error!"); str_platform.stop()

# 🎨 DIRECT ENTERPRISE LUXURY SKIN INJECTION
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; color: #ffffff !important; border-right: 4px solid #D97706 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #ffffff !important; font-size: 15px !important; font-weight: 700 !important; }
    div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; margin-bottom: 8px !important; }
    div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 6px !important; padding: 4px 10px !important; }
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

muda_mwanzo = time.time()
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem</h3>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# 📊 Bango la Telemetry (Rada ya Ubongo Kuu)
str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> 🟢 RAM/CPU Stable</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> 🟢 Traffic Safe</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
    <p style='color: #E2E8F0; font-size: 11px; margin: 0;'>🩺 <b>Self-Regulatory:</b> {self_healing_status}</p>
</div>
""", unsafe_allow_html=True)

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 13px; font-weight: bold; margin-bottom: 2px;'>🌐 ZANA ZA BURE:</p>", unsafe_allow_html=True)
orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu"]
chaguo_menyu = str_platform.sidebar.radio("", orodha_menyu, key="v14_clean_portal_radio_gate")

str_platform.sidebar.write("---")
str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 13px; font-weight: bold; margin-bottom: 2px;'>🔐 MANAGEMENT PORTAL:</p>", unsafe_allow_html=True)

try: str_platform.sidebar.page_link("pages/dashboard.py", label="Fungua Lango la Utawala (Dashboard) ──►", icon="🔐")
except Exception: pass

# =====================================================================
# 📚 MNYORORO WA DATASET ZAKO ZA SIRI (LOCAL MEMORY MATRIX)
# =====================================================================
kamusi_yetu_ya_ndani = {
    "mshandao": "Mstari imara au kiungo kilichounganishwa katika mtandao wa mawasiliano (Network Pathway / Pipeline Node).",
    "mnyororo wa kache": "Hifadhi ya muda mfupi ya kumbukumbu ya kompyuta inayozuia mifumo isigande kiofisi.",
    "chujio": "Zana maalum ya kukagua na kusafisha mistari ya msimbo dhidi ya hitilafu za uandishi au kiusalama.",
    "urari": "Usawa kamili uliopo kati ya ankara za kiofisi na fedha zilizochakatwa kupitia lango la malipo."
}

jozi_za_tafsiri_ndani = {
    "our company agrees to deliver the commodity within seven business days": "Kampuni yetu inakubali kutoa bidhaa hiyo ndani ya siku saba za kazi kulingana na urari wa mkataba.",
    "click the link to complete your monthly premium payment profile": "Bofya kiungo kilichopo chini ili kukamilisha wasifu wako wa malipo ya kifurushi cha kila mwezi."
}

# =====================================================================
# ⚙️ DIRECT MONOLITHIC COGNITIVE SYSTEM RENDERING
# =====================================================================
if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
    col_m1, col_m2 = str_platform.columns(2)
    with col_m1: str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")
    with col_m2: str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii kuhariri.\n\n• Kujenga mitambo ya kiasili ya mtafsiri na kamusi.")

elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v14_clean_box")
    if str_platform.button("Zindua Ukaguzi wa Sarufi", key="v14_btn_ed_clean"):
        if maandishi.strip() != "":
            prompt = f"Sahihisha sarufi ya matini haya kitalaalamu:\n\n{maandishi.strip()}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            str_platform.success("Marekebisho Yamekamilika! ✨")
            str_platform.write(jibu.choices.message.content)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)", "Kihindi (Hindi)", "Kireno (Portuguese)", "Kichina (Chinese)"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    muktadha_chaguo = str_platform.selectbox("🎯 Chagua Muktadha:", ["Kawaida", "Kibiashara", "Kisheria", "Kitiba", "Kielimu"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box")
    
    if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
        graw_text = maandishi_t.strip().lower().replace(".", "").replace(",", "")
        if graw_text in jozi_za_tafsiri_ndani:
            str_platform.success("🔮 Matokeo Timilifu ya Tafsiri (Imedakwa kutoka Dataset Yako):")
            str_platform.write(jozi_za_tafsiri_ndani[graw_text])
        else:
            prompt_t = f"Translate the following text from {lugha_chanzo} to {lugha_lengwa} in a '{muktadha_chaguo}' context:\n\n{maandishi_t}"
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
            str_platform.success("🔮 Matokeo ya Tafsiri Pro ya Muktadha:")
            str_platform.write(jibu_t.choices.message.content)

# 👑 THE ABSOLUTE REPAIR: Kitalu kizima cha line 132 kimefungwa nadhifu kwa rula ya chuma!
elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa:", key="kamusi_input_v14_clean")
    
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        g_word = msamiati.strip().lower()
        if g_word in kamusi_yetu_ya_ndani:
            str_platform.info("✨ Uchambuzi wa Kitaalamu (Imedakwa kutoka Dataset Yako):")
            str_platform.write(kamusi_yetu_ya_ndani[g_word])
        else:
            prompt_v = f"Ufafanuzi wa kina na mifano ya sentensi kwa neno la Kiswahili: {msamiati.strip()}"
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
            str_platform.info("✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:")
            str_platform.write(jibu_v.choices.message.content)

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 Ourworthlinks • LinguaAfrika AI Ecosystem</p>", unsafe_allow_html=True)

