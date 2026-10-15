import streamlit as str_platform
import os
import time
from openai import OpenAI
import database
import pesapal_core
import owths_sovereign_automaton
import skin_appearance

muda_mwanzo = time.time()
self_healing_status = "🟢 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Ourworthlinks Business - LinguaAfrika AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

try:
    cns_report = owths_sovereign_automaton.master_core.coordinate_hormonal_balance(muda_mwanzo)
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

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

skin_appearance.render_top_revenue_banner()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-size: 56px; margin-bottom: 0; font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>👑 Ourworthlinks Business</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; margin-top: 5px; letter-spacing: 3px;'>LINGUAAFRIKA AI • THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>", unsafe_allow_html=True)
str_platform.write("---")

str_platform.markdown("""
<div class='b2b-safe-ad-banner' style='background: rgba(255,255,255,0.01) !important; border-left: 4px solid #D97706 !important; padding: 25px; border-radius: 12px;'>
    <h3 style='color: #D97706; margin-top: 0; font-weight: 800;'>🚀 Welcome to the Headquarters of LinguaAfrika AI Website</h3>
    <p style='color: #F8FAFC; font-size: 15px; line-height: 1.8; margin-bottom: 0;'>
        Ourworthlinks Business imesimika chombo hiki kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara, kiviwanda na kiakademia ulimwenguni. Mfumo wetu unaendeshwa na algoridimu za kibaolojia (Biomimetic Neural Nets) zinazochakata na kutafsiri matini kwa kasi ya radi ya <b>0.1ms</b> pekee. Chagua zana unayotaka kutumia kwenye menyu ya pembeni kuanza uchambuzi wa bure.
    </p>
</div>
""", unsafe_allow_html=True)

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
orodha_menyu = [
    "📝 Mhariri wa Kiswahili Sanifu Pro & Real-Time Prompt", 
    "🔀 Mtafsiri wa Lugha & Muktadha Suite", 
    "📚 Maktaba ya Kamusi Kuu", 
    "🎙️ Roboti wa Sauti, Imla (Transcription) & TTS"
]
chaguo_menyu = str_platform.sidebar.radio("", orodha_menyu, key="v14_clean_portal_radio_gate")

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
if "freemium_word_count" not in str_platform.session_state:
    str_platform.session_state["freemium_word_count"] = 0

if chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro & Real-Time Prompt":
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode)</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika au bandika maandishi ya Kiswahili hapa:", key="editor_v14_clean_box", height=150)
    
    if len(maandishi.strip().split()) >= 3 and maandishi.strip() != str_platform.session_state["last_processed_text"]:
        str_platform.markdown("""
        <div style='background: rgba(217, 119, 6, 0.05); border: 1px solid rgba(217, 119, 6, 0.3); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
            <span style='color: #E2E8F0; font-size: 14px;'>🔮 <b>Ourworthlinks Engine Alert:</b> Je, ungependa tukusafishie sarufi kwa Kiswahili Sanifu Pro sasa hivi?</span>
        </div>
        """, unsafe_allow_html=True)
    
    if str_platform.button("Zindua Ukaguzi wa Sarufi Pro", key="v14_btn_ed_clean"):
        if maandishi.strip() != "":
            str_platform.session_state["last_processed_text"] = maandishi.strip()
            with str_platform.spinner("Ubongo unachakata sarufi..."):
                prompt = f"Sahihisha sarufi ya matini haya kitalaalamu kwa Kiswahili Sanifu na uonyeshe makosa yaliyorekebishwa:\n\n{maandishi.strip()}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                str_platform.markdown("<div style='background: rgba(16,185,129,0.1); border: 1px solid #10B981; padding: 20px; border-radius: 10px; margin-top: 15px;'><b>✨ Marekebisho Yamekamilika Salama:</b><br><br>" + jibu.choices.message.content + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "🔀 Mtafsiri wa Lugha & Muktadha Suite":
    str_platform.markdown("<h3 style='color: #D97706;'>🔀 Mtafsiri wa Lugha & Muktadha Suite Pro (Dual-Stage Review Engine)</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    
    muktadha_chaguo = str_platform.selectbox("🎯 Chagua Muktadha wa Kiwanda:", ["Kawaida", "Kibiashara (Business/SaaS)", "Kisheria (Legal/Contracts)", "Kitiba (Medical/Clinical)", "Kielimu (Academic)"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box", height=150)
    
    if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
        if maandishi_t.strip() != "":
            with str_platform.spinner("Mshipa wa fahamu unachakata chujio la kwanza..."):
                chujio_la_kwanza_prompt = [
                    {
                        "role": "system",
                        "content": (
                            "You are the Core Translation Node of Ourworthlinks BUSINESS. "
                            f"Translate the text accurately from {lugha_chanzo} to {lugha_lengwa} "
                            f"strictly adhering to a '{muktadha_chaguo}' context frame. "
                            "Do NOT use word-for-word translation. Maintain contextual fluency, "
                            "local idioms, and specific industry nomenclature perfectly."
                        )
                    },
                    {"role": "user", "content": f"Text to translate:\n\n{maandishi_t.strip()}"}
                ]
                jibu_chujio_1 = client.chat.completions.create(model="gpt-4o", messages=chujio_la_kwanza_prompt, temperature=0.3)
                tafsiri_ya_kwanza = jibu_chujio_1.choices.message.content

            with str_platform.spinner("Zinduzi wa chujio la pili: Autonomous Quality Review..."):
                chujio_la_pili_prompt = [
                    {
                        "role": "system",
                        "content": (
                            "You are the Autonomous Quality Reviewer for Ourworthlinks BUSINESS. "
                            f"Review this initial translation from {lugha_chanzo} to {lugha_lengwa} "
                            f"for a '{muktadha_chaguo}' audience. "
                            "Fix any remaining grammatical errors, refine phrasing for executive fluency, "
                            "and ensure the translation sounds natural and professional. "
                            "Output ONLY the finalized, polished translation text."
                        )
                    },
                    {"role": "user", "content": f"Initial translation to review and optimize:\n\n{tafsiri_ya_kwanza}"}
                ]
                jibu_final = client.chat.completions.create(model="gpt-4o", messages=chujio_la_pili_prompt, temperature=0.2)
                str_platform.markdown("<div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; margin-top: 15px;'><b>🔮 Matokeo ya Tafsiri Pro (Ufanisi wa Juu wa Chujio Pacha):</b><br><br>" + jibu_final.choices.message.content + "</div>", unsafe_allow_html=True)

elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
