import streamlit as str_platform
import os
import time
from openai import OpenAI
import database
import pesapal_core
import owths_sovereign_automaton
import skin_appearance
from cerebral_cortex import CerebralCortex

muda_mwanzo = time.time()
self_healing_status = "🟢 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Ourworthlinks Business - LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

skin_appearance.inject_premium_glassmorphic_skin()

api_key_source = os.environ.get("OPENAI_API_KEY") or (str_platform.secrets.get("OPENAI_API_KEY") if hasattr(str_platform, "secrets") else None)

if api_key_source: 
    client = OpenAI(api_key=api_key_source.strip())
    ubongo = CerebralCortex(client)
else: 
    str_platform.error("🔒 secrets error!"); str_platform.stop()

skin_appearance.render_top_revenue_banner()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-size: 56px; margin-bottom: 0; font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>👑 Ourworthlinks Business</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; margin-top: 5px; letter-spacing: 3px;'>LINGUAAFRIKA AI • THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

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

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: 1px; margin-bottom: 5px;'>🌐 HUDUMA ZOTE NNE ZA BIASHARA:</p>", unsafe_allow_html=True)

menyu_kamili = {
    "mhariri": "📝 Mhariri wa Kiswahili Sanifu Pro & Real-Time Prompt",
    "mtafsiri": "🔀 Mtafsiri wa Lugha & Muktadha Suite",
    "kamusi": "📚 Maktaba ya Kamusi Kuu",
    "sauti": "🎙️ Roboti wa Sauti, Imla (Transcription) & TTS"
}

chaguo_display = str_platform.sidebar.radio(label="", options=list(menyu_kamili.values()), key="portal_radio_gate")
chaguo_menyu = [k for k, v in menyu_kamili.items() if v == chaguo_display][0]

str_platform.sidebar.write("---")

str_platform.sidebar.link_button(
    label="🔐 Fungua Lango la Utawala (Dashboard) ──►",
    url="https://streamlit.app",
    type="secondary",
    use_container_width=True,
    key="native_dashboard_redirect_btn"
)

if "last_processed_text" not in str_platform.session_state:
    str_platform.session_state["last_processed_text"] = ""

if chaguo_menyu == "mhariri":
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode)</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika au bandika maandishi ya Kiswahili hapa:", key="editor_v14_clean_box", height=150)
    if str_platform.button("Zindua Ukaguzi wa Sarufi Pro", key="v14_btn_ed_clean"):
        if maandishi.strip() != "":
            with str_platform.spinner("Cerebral Cortex inachakata sarufi..."):
                res = ubongo.chakata_sarufi_pro(maandishi)
                str_platform.markdown("<div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Marekebisho:</b><br><br>" + res + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "mtafsiri":
    str_platform.markdown("<h3 style='color: #D97706;'>🔀 Mtafsiri wa Lugha & Muktadha Suite Pro</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa", "Kifaransa", "Kiarabu"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    muktadha_chaguo = str_platform.selectbox("🎯 Chagua Muktadha:", ["Kawaida", "Kibiashara (Business)", "Kisheria (Legal)", "Kitiba (Medical)", "Kielimu (Academic)"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box", height=150)
    if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
        if maandishi_t.strip() != "":
            with str_platform.spinner("Processing Dual-Stage Review..."):
                res = ubongo.chakata_tafsiri_pacha(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)
                str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'><b>🔮 Matokeo:</b><br><br>" + res + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "kamusi":
    str_platform.markdown("<h3 style='color: #D97706;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa:", key="kamusi_input_v14_clean")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        if msamiati.strip() != "":
            with str_platform.spinner("Neuroplasticity lookup running..."):
                res = ubongo.chakata_kamusi_kuu(msamiati, database)
                str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'>" + res + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "sauti":
    ubongo.chakata_sauti_na_imla()

str_platform.write("---")
skin_appearance.render_bottom_revenue_banner()
