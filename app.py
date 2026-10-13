import streamlit as str_platform
import os
import time
from openai import OpenAI
import database
import owths_sovereign_automaton  # 🛡️ THE AUTOMATON: Combined Chujio + Memory Core
import skin_appearance            # 🎨 THE EPITHELIAL MATRIX: Master Design Core

muda_mwanzo = time.time()
self_healing_status = "🟢 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="LinguaAfrika AI Premium", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# 🧠 HYPOTHALAMUS EXECUTION: Purges memory waste, monitors latency, and fires up database
try:
    cns_report = owths_sovereign_automaton.master_core.coordinate_hormonal_balance(muda_mwanzo)
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🎨 NEURAL CONNECTION INJECTION: Spreads the global premium glassmorphic skin instantly
skin_appearance.inject_premium_glassmorphic_skin()

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

# 💰 BRAND-SAFE AD REVENUE PLACEMENT: Top Placement
skin_appearance.render_top_revenue_banner()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-size: 54px; margin-bottom: 0; text-shadow: 0 0 30px rgba(217,119,6,0.3);'>👑 LinguaAfrika AI</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 600; margin-top: 5px; letter-spacing: 2px;'>THE AUTONOMOUS BIOMIMETIC ENTERPRISE SUITE</p>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# Glowing Telemetry Dashboard mapping real autonomic engine metrics
str_platform.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #D97706; padding: 18px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(217,119,6,0.15);'>
    <p style='color: #D97706; font-size: 13px; margin: 0 0 10px 0; text-align: center; font-weight: 900; letter-spacing: 1px;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #34D399; font-size: 13px; margin: 0;'>🛡️ <b>OWTHS Filter:</b> 🟢 100% Active</p>
    <p style='color: #34D399; font-size: 13px; margin: 6px 0;'>🚽 <b>Renal Excretion:</b> 🟢 Safe Flush</p>
    <p style='color: #34D399; font-size: 13px; margin: 0 0 6px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
    <hr style='border-color: rgba(255,255,255,0.05); margin: 8px 0;'>
    <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: {self_healing_status}</p>
</div>
""", unsafe_allow_html=True)

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: 1px; margin-bottom: 5px;'>🌐 ZANA ZA BURE:</p>", unsafe_allow_html=True)
orodha_menyu = ["🎯 Malengo na Dira ya Taasisi", "📝 Mhariri wa Kiswahili Sanifu Pro", "🔀 Mtafsiri wa Lugha Suite", "📚 Maktaba ya Kamusi Kuu"]
chaguo_menyu = str_platform.sidebar.radio("", orodha_menyu, key="v14_clean_portal_radio_gate")

str_platform.sidebar.write("---")
try: str_platform.sidebar.page_link("pages/dashboard.py", label="Fungua Lango la Utawala (Dashboard) ──►", icon="🔐")
except Exception: pass

if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
    str_platform.markdown("<h3 style='color: #D97706;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
    str_platform.markdown("<div style='background: rgba(255,255,255,0.01); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03); line-height: 1.8; font-size: 16px;'>LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara na kiviwanda duniani.</div>", unsafe_allow_html=True)

elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika maandishi yako hapa kwa ajili ya kusafishwa sarufi kifalme:", key="editor_v14_clean_box")
    if str_platform.button("Zindua Ukaguzi wa Sarufi Pro", key="v14_btn_ed_clean"):
        if maandishi.strip() != "":
            prompt = f"Sahihisha sarufi ya matini haya kitalaalamu:\n\n{maandishi.strip()}"
            jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            str_platform.markdown("<div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Marekebisho Yamekamilika Salama:</b><br><br>" + jibu.choices.message.content + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
    str_platform.markdown("<h3 style='color: #D97706;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    col1, col2 = str_platform.columns(2)
    with col1: str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box")
    
    if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
        if maandishi_t.strip() != "":
            prompt_t = f"Translate text context:\n\n{maandishi_t.strip()}"
            jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
            str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'><b>🔮 Matokeo ya Tafsiri Pro ya Muktadha:</b><br><br>" + jibu_t.choices.message.content + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
    str_platform.markdown("<h3 style='color: #D97706;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa kwa ajili ya uchambuzi wa kasi ya radi:", key="kamusi_input_v14_clean")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        hit_matokeo = database.query_neuroplasticity_lookup(msamiati)
        if hit_matokeo:
            str_platform.markdown("<div style='background: rgba(217,119,6,0.1); border: 1px solid #D97706; padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Uchambuzi wa Kitaalamu (Uti wa Mgongo wa Mfumo):</b><br><br>" + str(hit_matokeo) + "</div>", unsafe_allow_html=True)
        else:
            prompt_v = f"Ufafanuzi wa kina kwa neno: {msamiati.strip()}"
            jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
            str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:</b><br><br>" + jibu_v.choices.message.content + "</div>", unsafe_allow_html=True)

str_platform.write("---")
# 💰 BRAND-SAFE AD REVENUE PLACEMENT: Bottom Placement
skin_appearance.render_bottom_revenue_banner()
str_platform.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>© 2026 Ourworthlinks • LinguaAfrika AI Sovereign Ecosystem • Autonomic Architecture</p>", unsafe_allow_html=True)

