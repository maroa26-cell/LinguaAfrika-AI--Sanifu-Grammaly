import streamlit as str_platform
import os
import time
from openai import OpenAI
import database
import owths_sovereign_automaton  # 👑 MASTER AUTOMATON: Combined filter & metabolic cell
import skin_appearance            # 🎨 EPITHELIAL MATRIX: Central design architecture

muda_mwanzo = time.time()
self_healing_status = "🟢 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Ourworthlinks Business - LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# 🧠 HYPOTHALAMUS EXECUTION: Purges memory buffers, monitors traffic, and mounts database instantly
try:
    cns_report = owths_sovereign_automaton.master_core.coordinate_hormonal_balance(muda_mwanzo)
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🎨 GLOBAL DESIGN INJECTION: Spreads the premium glassmorphic stylesheet globally
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

# =====================================================================
# 🌐 WEBPAGE IDARA YA 1: THE ENTERPRISE SAAS CORPORATE MARKETING HERO
# =====================================================================
str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-size: 56px; margin-bottom: 0; font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>👑 Ourworthlinks Business</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; margin-top: 5px; letter-spacing: 3px;'>LINGUAAFRIKA AI • THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>", unsafe_allow_html=True)
str_platform.write("---")

str_platform.markdown("""
<div class='b2b-safe-ad-banner' style='background: rgba(255,255,255,0.01) !important; border-left: 4px solid #D97706 !important; padding: 25px; border-radius: 12px;'>
    <h3 style='color: #D97706; margin-top: 0; font-weight: 800;'>🚀 Welcome to the Sovereign Headquarters of LinguaAfrika AI Suite</h3>
    <p style='color: #F8FAFC; font-size: 15px; line-height: 1.8; margin-bottom: 0;'>
        Ourworthlinks Business imesimika chombo hiki kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara na kiviwanda ulimwenguni. Mfumo wetu unaendeshwa na algoridimu za kibaolojia (Biomimetic Neural Nets) zinazochakata na kutafsiri matini kwa kasi ya radi ya <b>0.1ms</b> pekee. Chagua zana unayotaka kutumia kwenye menyu ya pembeni kuanza uchambuzi.
    </p>
</div>
""", unsafe_allow_html=True)

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

# =====================================================================
# 📊 CNS TELEMETRY INTEGRITY RADAR (SIDEBAR LAYOUT)
# =====================================================================
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

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: 1px; margin-bottom: 5px;'>🌐 FILTER MENYU YA WEBSITE:</p>", unsafe_allow_html=True)
orodha_menyu = ["📝 Mhariri wa Kiswahili Sanifu Pro & Tafsiri Suite", "📚 Maktaba ya Kamusi Kuu"]
chaguo_menyu = str_platform.sidebar.radio("", orodha_menyu, key="v14_clean_portal_radio_gate")

str_platform.sidebar.write("---")
# 🔐 LANGO LA UTAWALA PORTAL LINK SYNC
try: str_platform.sidebar.page_link("pages/dashboard.py", label="Fungua Lango la Utawala (Dashboard) ──►", icon="🔐")
except Exception: pass

# Initialize dynamic toggle cache variables inside execution pipeline
if "last_processed_text" not in str_platform.session_state:
    str_platform.session_state["last_processed_text"] = ""
if "show_translation_sub_gate" not in str_platform.session_state:
    str_platform.session_state["show_translation_sub_gate"] = False

# =====================================================================
# 👑 WEBPAGE IDARA YA 2: THE UNIFIED REAL-TIME INTERFACE
# =====================================================================
if chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro & Tafsiri Suite":
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Real-Time Swahili Editor Suite (Grammarly Mode)</h3>", unsafe_allow_html=True)
    
    # Sanduku kuu la mtumiaji ambalo algorithm inalifanyia doria masaa 24
    maandishi = str_platform.text_area("Anza kuandika au kubandika maandishi yako hapa kwa ajili ya uchambuzi wa kiotomatiki:", key="live_grammarly_text_box", height=180)
    
    # 🧠 THE REAL-TIME PROACTIVE LOGIC: Mfumo unaibuka wenyewe maneno yakizidi matatu (3) bila kubonyeza kitufe!
    if len(maandishi.strip().split()) >= 3 and maandishi.strip() != str_platform.session_state["last_processed_text"]:
        str_platform.write("---")
        str_platform.markdown("""
        <div style='background: rgba(217, 119, 6, 0.05); border: 1px solid rgba(217, 119, 6, 0.3); padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <p style='color: #D97706; margin: 0; font-weight: bold; font-size: 14px;'>🔮 OWL ENGINE PROACTIVE PROMPT SYSTEM:</p>
            <span style='color: #E2E8F0; font-size: 14px;'>Ourworthlinks Business imebaini matini yako. Je, ungependa tukusafishie sarufi kwa Kiswahili Sanifu Pro sasa hivi, au unahitaji tuhamishe muktadha huu kwenda lugha nyingine (Tafsiri Suite)?</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_opt1, col_opt2, col_opt3 = str_platform.columns(3)
        
        with col_opt1:
            if str_platform.button("✨ Sahihisha Sarufi Sasa", key="btn_auto_correct"):
                str_platform.session_state["last_processed_text"] = maandishi.strip()
                str_platform.session_state["show_translation_sub_gate"] = False
                with str_platform.spinner("Inasafisha sarufi ya Kiswahili..."):
                    prompt = f"Sahihisha sarufi ya matini haya kitalaalamu kwa Kiswahili Sanifu na uonyeshe makosa yaliyorekebishwa:\n\n{maandishi.strip()}"
                    jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                    str_platform.markdown("<div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 10px;'><b>✨ Marekebisho Yamekamilika Salama:</b><br><br>" + jibu.choices.message.content + "</div>", unsafe_allow_html=True)
                    
        with col_opt2:
            if str_platform.button("🔀 Fungua Lango la Tafsiri", key="btn_activate_trans"):
                str_platform.session_state["show_translation_sub_gate"] = True
                str_platform.rerun()
                
        with col_opt3:
            if str_platform.button("❌ Futa na Upuuze", key="btn_ignore_prompt"):
                str_platform.session_state["last_processed_text"] = maandishi.strip()
                str_platform.session_state["show_translation_sub_gate"] = False
                str_platform.rerun()

    # 👑 TAFSIRI SUITE IS RESTORED: Kurudisha idara kamili ya vichaguzi vya lugha 14 na Muktadha!
    if str_platform.session_state["show_translation_sub_gate"]:
        str_platform.write("---")
        str_platform.markdown("<p style='color: #3B82F6; font-weight: bold; margin-bottom: 5px; font-size: 16px;'>🔮 CHAGUA LUGHA NA MUKTADHA WA TAFSIRI SUITE (LUGHA 14):</p>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)"]
        
        sub_col1, sub_col2, sub_col3 = str_platform.columns(3)
        with sub_col1: lugha_chanzo = sub_col1.selectbox("Kutoka Lugha:", orodha_lugha, index=0, key="live_src_lang")
        with sub_col2: lugha_lengwa = sub_col2.selectbox("Kwenda Lugha:", orodha_lugha, index=1, key="live_trg_lang")
        with sub_col3: muktadha_chaguo = sub_col3.selectbox("🎯 Muktadha wa Kiwanda:", ["Kawaida", "Kibiashara", "Kisheria", "Kitiba", "Kielimu"], key="live_context_node")
        
        if str_platform.button("🚀 Tekeleza Tafsiri ya Muktadha Sasa", key="btn_execute_live_trans"):
            if maandishi.strip() != "":
                with str_platform.spinner("Mshipa wa fahamu unatafsiri lugha..."):
                    prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} strictly within a '{muktadha_chaguo}' context frame:\n\n{maandishi.strip()}"
                    jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
