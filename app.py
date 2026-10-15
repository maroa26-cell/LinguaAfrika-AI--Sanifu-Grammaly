import streamlit as str_platform
import os
import time
import sqlite3
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

if "freemium_words_used" not in str_platform.session_state:
    str_platform.session_state["freemium_words_used"] = 0

maneno_yaliyotumika = str_platform.session_state["freemium_words_used"]
maneno_yaliyobaki = max(0, 50 - maneno_yaliyotumika)

str_platform.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #D97706; padding: 18px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(217,119,6,0.15);'>
    <p style='color: #D97706; font-size: 13px; margin: 0 0 10px 0; text-align: center; font-weight: 900; letter-spacing: 1px;'>📊 RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #F59E0B; font-size: 13px; margin: 0;'>🎁 <b>Salio la Bure:</b> {maneno_yaliyobaki}/50 Maneno</p>
    <p style='color: #34D399; font-size: 13px; margin: 6px 0 0 0;'>🛡️ <b>OWTHS Filter:</b> 🟢 100% Active</p>
    <p style='color: #34D399; font-size: 13px; margin: 6px 0;'>⚡ <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
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
chaguo_menyu = [k for k, v in menyu_kamili.items() if v == chaguo_display]

str_platform.sidebar.write("---")

str_platform.sidebar.link_button(
    label="🔐 Lango la Malipo na Usajili Mteja ──►",
    url="https://streamlit.app",
    type="primary",
    use_container_width=True,
    key="client_dashboard_redirect_btn"
)

str_platform.sidebar.write("---")

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 11px; font-weight: 800; text-align: center;'>🎛️ AREA YA UTAWALA (ADMIN NODE)</p>", unsafe_allow_html=True)
if "admin_authenticated" not in str_platform.session_state:
    str_platform.session_state["admin_authenticated"] = False

if not str_platform.session_state["admin_authenticated"]:
    with str_platform.sidebar.expander("🚪 Ingia kama Admin"):
        adm_user = str_platform.text_input("Admin User:", key="adm_u_input")
        adm_pass = str_platform.text_input("Admin Pass:", type="password", key="adm_p_input")
        if str_platform.button("Zindua Utawala", use_container_width=True):
            if database.thibitisha_utambulisho_wa_siri(adm_user, adm_pass, "admin"):
                str_platform.session_state["admin_authenticated"] = True
                str_platform.rerun()
            else:
                str_platform.error("Hadhi Batili!")
else:
    str_platform.sidebar.success("🔓 Admin Matrix Connected")
    if str_platform.sidebar.button("Funga Lango la Utawala", use_container_width=True):
        str_platform.session_state["admin_authenticated"] = False
        str_platform.rerun()

if str_platform.session_state["admin_authenticated"]:
    str_platform.markdown("<h2 style='color: #D97706;'>📚 BULK DATASET INGESTION Mainframe</h2>", unsafe_allow_html=True)
    uploaded_file = str_platform.file_uploader("Upload Swahili Vocabulary Matrix (CSV Format):", type=["csv"])
    if uploaded_file is not None:
        try:
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            if 'keyword' in df.columns and 'semantic_meaning' in df.columns:
                conn = database.pata_muunganisho_wa_chuma()
                cursor = conn.cursor()
                success_count = 0
                for index_row, row in df.iterrows():
                    try:
                        cursor.execute("INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)", (str(row['keyword']).strip().lower(), str(row['semantic_meaning']).strip()))
                        success_count += 1
                    except sqlite3.IntegrityError: pass
                conn.commit()
                conn.close()
                str_platform.success(f"Loaded {success_count} terms into the system spinal cord!")
            else: str_platform.error("CSV requires 'keyword' and 'semantic_meaning' columns.")
        except Exception as e: str_platform.error(f"Ingestion anomaly caught: {str(e)}")
    str_platform.write("---")

# 🔥 MAREKEBISHO: Upokeaji wa masharti umebadilishwa kutoka == ["key"] kuwa 'in' kuzuia UI kuzuia paneli
if "mhariri" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode)</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika au bandika maandishi ya Kiswahili hapa:", key="editor_v14_clean_box", height=150)
    heabu_maneno = len(maandishi.strip().split()) if maandishi.strip() else 0
    if maneno_yaliyobaki <= 0:
        str_platform.error("🔒 Salio LIMEISHA! Umeshatumia maneno yote 50 ya bure. Tafadhali fungua Lango la Dashboard upande wa kushoto kulipia kifurushi cha Premium.")
    else:
        if str_platform.button("Zindua Ukaguzi wa Sarufi Pro", key="v14_btn_ed_clean"):
            if maandishi.strip() != "":
                str_platform.session_state["freemium_words_used"] += heabu_maneno
                with str_platform.spinner("Cerebral Cortex inachakata sarufi..."):
                    res = ubongo.chakata_sarufi_pro(maandishi)
                    str_platform.markdown("<div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Marekebisho Yamekamilika:</b><br><br>" + res + "</div>", unsafe_allow_html=True)

elif "mtafsiri" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>🔀 Mtafsiri wa Lugha & Muktadha Suite Pro</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa", "Kifaransa", "Kiarabu"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    muktadha_chaguo = str_platform.selectbox("🎯 Chagua Muktadha:", ["Kawaida", "Kibiashara (Business)", "Kisheria (Legal)", "Kitiba (Medical)", "Kielimu (Academic)"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box", height=150)
    heabu_maneno_t = len(maandishi_t.strip().split()) if maandishi_t.strip() else 0
    if maneno_yaliyobaki <= 0:
        str_platform.error("🔒 Salio LIMEISHA! Umeshatumia maneno yote 50 ya bure. Tafadhali fungua Lango la Dashboard upande wa kushoto kulipia kifurushi cha Premium.")
    else:
        if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
            if maandishi_t.strip() != "":
                str_platform.session_state["freemium_words_used"] += heabu_maneno_t
                with str_platform.spinner("Processing Dual-Stage Review..."):
                    res = ubongo.chakata_tafsiri_pacha(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)
                    str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'><b>🔮 Matokeo:</b><br><br>" + res + "</div>", unsafe_allow_html=True)

elif "kamusi" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa kuanza uchambuzi wetu:", key="kamusi_input_v14_clean")
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        if msamiati.strip() != "":
            with str_platform.spinner("Neuroplasticity lookup running..."):
                res = ubongo.chakata_kamusi_kuu(msamiati, database)
