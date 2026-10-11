import streamlit as str_platform
import database
import pesapal_core
import time

# 👑 SANIFU MIPANGILI YA SEVA TANZU YANAYO JITEGEMEA
str_platform.set_page_config(page_title="Ourworthlinks Operations Dashboard", page_icon="🔐", layout="wide")

try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🎨 DIRECT ENTERPRISE LUXURY SKIN INJECTION (DARK HIGH-TECH STYLE)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0F172A !important; font-family: 'Segoe UI', sans-serif !important; color: #ffffff !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .stTextInput label, .stSelectbox label, .stRadio label { color: #E2E8F0 !important; font-weight: bold !important; font-size: 15px !important; }
    
    /* Mtindo wa Vifungo Vitatu vya Mlangoni */
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; width: 100% !important; border: none !important; transition: all 0.3s ease !important; }
    div.stButton > button:hover { background-color: #3B82F6 !important; box-shadow: 0 4px 15px rgba(59,130,246,0.4) !important; }
    
    /* Kitufe Maalum cha Usajili na Pesapal */
    .pesapal-btn button { background-color: #D97706 !important; }
    .pesapal-btn button:hover { background-color: #B45309 !important; box-shadow: 0 4px 15px rgba(217,119,6,0.4) !important; }
    
    .stTable { background-color: #1E293B !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900; margin-bottom: 0;'>🔐 OURWORTHLINKS MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px;'>Sovereign Triple-Gateway Identity Portal & B2B Analytics Suite</p>", unsafe_allow_html=True)
str_platform.write("---")

# 🧠 INITIALIZE GATE STATE: Mtambo unakariri mteja kachagua chumba kipi
if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "mlangoni"

# =====================================================================
# 🎛️ NYERERE GATEWAY SELECTOR (UCHAGUZI WA VYUMBA VITATU MBALIKAMBALI)
# =====================================================================
if str_platform.session_state["active_gateway"] == "mlangoni":
    str_platform.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Tafadhali chagua lango lako la kiofisi ili kuingia hewani:</h4>", unsafe_allow_html=True)
    str_platform.write("")
    
    col_g1, col_g2, col_g3 = str_platform.columns(3)
    
    with col_g1:
        str_platform.markdown("<div style='text-align: center; padding: 10px;'>🔑</div>", unsafe_allow_html=True)
        if str_platform.button("🚪 Fungua Lango la Utawala (Admin)", key="btn_gate_admin"):
            str_platform.session_state["active_gateway"] = "admin_suite"
            str_platform.rerun()
            
    with col_g2:
        str_platform.markdown("<div style='text-align: center; padding: 10px;'>🚪</div>", unsafe_allow_html=True)
        if str_platform.button("🔐 Kuingia Kama Premium User (Sign In)", key="btn_gate_premium"):
            str_platform.session_state["active_gateway"] = "premium_suite"
            str_platform.rerun()
            
    with col_g3:
        str_platform.markdown("<div style='text-align: center; padding: 10px;'>💳</div>", unsafe_allow_html=True)
        str_platform.markdown("<div class='pesapal-btn'>", unsafe_allow_html=True)
        if str_platform.button("✨ Lango la Malipo ya Premium (Pesapal)", key="btn_gate_signup"):
            str_platform.session_state["active_gateway"] = "premium_billing_funnel"
            str_platform.rerun()
        str_platform.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 📂 CHUMBA CHA 1: 👑 LANGO LA UTAWALA (ADMIN SUITE LOGIC)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "admin_suite":
    if str_platform.button("← Rudi Mlangoni", key="back_from_admin"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    str_platform.markdown("<h2 style='color: #D97706; font-weight: bold; text-align: center;'>👑 ADMINISTRATIVE SECURE IDENTITY PORT</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    col_a1, col_a2, col_a3 = str_platform.columns()
    with col_a2:
        jina_admin = str_platform.text_input("Username ya Siri ya Utawala:", key="v14_admin_user")
        pass_admin = str_platform.text_input("Nenosiri la Siri la Utawala:", type="password", key="v14_admin_pass")
        
        if str_platform.button("Zindua Mifumo ya Utawala", key="v14_btn_admin_verify"):
            if database.thibitisha_utambulisho_wa_siri(jina_admin, pass_admin, "Admin"):
                str_platform.session_state["user_status"] = "admin"
                str_platform.session_state["active_user_name"] = jina_admin
                str_platform.success("🔓 MUUNDO UMEKUBALIWA: Mifumo yote ya B2B Token Channels ipo hai.")
                str_platform.write("---")
                
                str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
                data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
                str_platform.table(data_b2b)
                
                col_b1, col_b2 = str_platform.columns(2)
                with col_b1: str_platform.info("💰 **Total B2B Revenue Logged**\n\nAccumulated: **$1,240.50 USD**")
                with col_b2: str_platform.info("📈 **Traffic Volume Analytics**\n\nTotal Words API Streams: **620,250 Words**")
            else:
                str_platform.error("🛑 Hitilafu ya Usalama: Username au Nenosiri la Utawala si sahihi!")

# =====================================================================
# 📂 CHUMBA CHA 2: 🚪 LANGO LA MTEJA WA PREMIUM (SIGN IN PREMIUM)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "premium_suite":
    if str_platform.button("← Rudi Mlangoni", key="back_from_premium"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    str_platform.markdown("<h2 style='color: #3B82F6; font-weight: bold; text-align: center;'>💎 PREMIUM USER IDENTITY AUTHENTICATION</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    col_p1, col_p2, col_p3 = str_platform.columns()
    with col_p2:
        jina_premium = str_platform.text_input("Ingiza Username Yako ya Premium:", key="v14_premium_user")
        pass_premium = str_platform.text_input("Ingiza Nenosiri Lako:", type="password", key="v14_premium_pass")
        
        if str_platform.button("Thibitisha Identity ya Premium", key="v14_btn_premium_login"):
            if database.thibitisha_utambulisho_wa_siri(jina_premium, pass_premium, "Premium User"):
                str_platform.session_state["user_status"] = "standard_premium"
                str_platform.session_state["active_user_name"] = jina_premium
                str_platform.success(f"✅ UNLOCKED: Karibu Kiongozi {jina_premium.upper()}! Vifurushi vyote vipo hai sasa hivi. Tumia menyu ya kushoto kurudi kwenye Portal.")
            else:
                str_platform.error("🛑 Hitilafu: Akaunti ya Premium haijapatikana au password si sahihi!")

# =====================================================================
# 📂 CHUMBA CHA 3: 💳 LANGO LA PREMIUM BILLING FUNNEL (TABO MBILI ZILIZOTENGANISHWA)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "premium_billing_funnel":
    if str_platform.button("← Rudi Mlangoni", key="back_from_billing"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    str_platform.markdown("<h2 style='color: #D97706; font-weight: bold; text-align: center;'>💳 PREMIUM ACQUISITION & MALIPO PORTAL</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    
    tab_mpya, tab_wa_zamani = str_platform.tabs(["📝 MIMI NI MTUMIAJI MPYA (Sign Up First)", "🔑 MIMI NI MTUMIAJI WA ZAMANI (Sign In to Pay)"])
    
    # 📑 TABO YA A: MTUMIAJI MPYA
    with tab_mpya:
        col_s1, col_s2, col_s3 = str_platform.columns()
        with col_s2:
            str_platform.markdown("### 📝 Hatua ya 1: Jisajili Kwanza")
            jina_jipya = str_platform.text_input("Tengeneza Username Mpya (Herufi Ndogo Pekee):", key="v14_master_new_user")
            siri_mpya = str_platform.text_input("Tengeneza Nenosiri Jipya:", type="password", key="v14_master_new_pass")
            
            if "signup_completed" not in str_platform.session_state:
                str_platform.session_state["signup_completed"] = False
            
            if str_platform.button("Thibitisha Usajili wa Akaunti", key="v14_master_btn_signup_validate"):
                if jina_jipya.strip() != "" and siri_mpya.strip() != "":
                    if database.sajili_mtumiaji_mpya(jina_jipya.strip(), siri_mpya.strip(), "Premium User"):
                        str_platform.session_state["signup_completed"] = True
                        str_platform.session_state["saved_signup_username"] = jina_jipya.strip()
                        str_platform.session_state["saved_signup_email"] = f"{jina_jipya.strip()}@ourworthlinks.com"
                    else:
                        str_platform.error("🛑 Hitilafu: Jina hili la mtumiaji tayari limeshasajiliwa! Tumia tabo ya pili kulipia.")
                else:

