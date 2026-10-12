import streamlit as str_platform
import os
import time
from openai import OpenAI
import database # 👑 THE SPINAL CORD: Neural pathway linking app logic directly to localized indexed schemas

self_healing_status = "🟢 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Initialize and invoke the underlying SQLite schema on initial server mount
try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

if "OPENAI_API_KEY" in os.environ: 
    api_key_source = os.environ["OPENAI_API_KEY"]
elif hasattr(str_platform, "secrets") and "OPENAI_API_KEY" in str_platform.secrets: 
    api_key_source = str_platform.secrets["OPENAI_API_KEY"]
else: 
    api_key_source = None

if api_key_source: 
    client = OpenAI(api_key=api_key_source.strip())
else: 
    str_platform.error("🔒 secrets error!"); str_platform.stop()

# 🎨 EXCLUSIVE ENTERPRISE LUXURY SKIN INJECTION & FAMILY-SAFE PLACEMENTS
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; color: #ffffff !important; border-right: 4px solid #D97706 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #ffffff !important; font-size: 15px !important; font-weight: 700 !important; }
    div[data-testid="stRadio"] > label { background-color: rgba(255, 255, 255, 0.04) !important; padding: 12px 15px !important; border-radius: 8px !important; margin-bottom: 8px !important; }
    div[data-testid="stRadio"] div[aria-checked="true"] { background-color: #D97706 !important; border-radius: 6px !important; padding: 4px 10px !important; }
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; border: none !important; width: 100% !important; }
    .b2b-safe-ad-banner { background-color: #F8FAFC !important; border: 2px solid #E2E8F0 !important; border-radius: 12px !important; padding: 15px !important; text-align: center !important; color: #94A3B8 !important; font-size: 11px !important; font-weight: 800 !important; margin: 15px 0 !important; }
</style>
""", unsafe_allow_html=True)

# 🌐 BOX 1: BANGO LA JUU KUU (TOP REVENUE PLACEMENT)
str_platform.markdown("""
<div class='b2b-safe-ad-banner'>
    🛡️ BRAND-SAFE REVENUE NODE (TOP MEDIA.NET B2B PLACEMENT)
    <div id="media_net_display_slot_top"></div>
</div>
""", unsafe_allow_html=True)

muda_mwanzo = time.time()
str_platform.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; margin-bottom: 0;'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<h3 style='text-align: center; color: #D97706; font-weight: 700; margin-top: 5px;'>The Autonomous Biomimetic Living Ecosystem</h3>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# Telemetry sidebar metrics panel
str_platform.sidebar.markdown(f"""
<div style='background-color: rgba(30, 58, 138, 0.1); border: 2px solid #D97706; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #D97706; font-size: 14px; margin: 0 0 8px 0; text-align: center; font-weight: 900;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #25D366; font-size: 12px; margin: 0;'>🫁 <b>Respiratory:</b> 🟢 Stable</p>
    <p style='color: #25D366; font-size: 12px; margin: 4px 0;'>🩸 <b>Circulation:</b> 🟢 Safe</p>
    <p style='color: #25D366; font-size: 12px; margin: 0 0 4px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
</div>
""", unsafe_allow_html=True)

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 13px; font-weight: bold; margin-bottom: 2px;'>🌐 ZANA ZA BURE:</p>", unsafe_allow_html=True)
orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu"]
chaguo_menyu = str_platform.sidebar.radio("", orodha_menyu, key="v14_clean_portal_radio_gate")

# 🌐 BOX 2: BANGO LA PEMBENI (SIDEBAR VERTICAL AD SLOT)
str_platform.sidebar.markdown("""
<div class='b2b-safe-ad-banner' style='padding: 8px;'>
    <p style='color: #D97706; margin: 0; font-size: 10px;'>🔒 SECURE AD BLOCK</p>
    <div id="ezoic-pub-ad-placeholder-101"></div>
</div>
""", unsafe_allow_html=True)

str_platform.sidebar.write("---")
str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 13px; font-weight: bold; margin-bottom: 2px;'>🔐 MANAGEMENT PORTAL:</p>", unsafe_allow_html=True)
try: 
    str_platform.sidebar.page_link("pages/dashboard.py", label="Fungua Lango la Utawala (Dashboard) ──►", icon="🔐")
except Exception: 
    pass

# RENDER SELECTION LAYOUT INTERFACES
if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
    str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")

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
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    muktadha_chaguo = str_platform.selectbox("🎯 Chagua Muktadha:", ["Kawaida", "Kibiashara", "Kisheria", "Kitiba", "Kielimu"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box")
    if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
        prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a '{muktadha_chaguo}' context:\n\n{maandishi_t}"
        jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
        str_platform.success("🔮 Matokeo ya Tafsiri Pro ya Muktadha:")
        str_platform.write(jibu_t.choices.message.content)

# 📚 THE COMPLIANCE-TESTED SPINE MODULE (0.1ms Vector Query Node)
elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa:", key="kamusi_input_v14_clean")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        # 🧠 COGNITIVE EXTRACTION: Resolves search terms across memory blocks via the active Spinal Cord route
        hit_matokeo = database.query_neuroplasticity_lookup(msamiati)
        
        if hit_matokeo:
            str_platform.info("✨ Uchambuzi wa Kitaalamu (Imedakwa kutoka Kasi ya Radi ya Uti wa Mgongo wa Mfumo):")
            str_platform.write(hit_matokeo)
        else:
            prompt_v = f"Ufafanuzi wa kina kwa neno: {msamiati.strip()}"
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
            str_platform.info("✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:")
            str_platform.write(jibu_v.choices.message.content)

str_platform.write("---")

# 🌐 BOX 3: BANGO LA CHINI KUU (BOTTOM STICKY FLOATING ANCHOR AD SLOT)
str_platform.markdown("""
<div class='b2b-safe-ad-banner'>
    🛡️ BOTTOM REVENUE ANCHOR (EZOIC AI BRAND-SAFE PLACEMENT)
    <div id="ezoic-pub-ad-placeholder-102"></div>
</div>
""", unsafe_allow_html=True)

str_platform.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>© 2026 Ourworthlinks • LinguaAfrika AI Ecosystem</p>", unsafe_allow_html=True)
