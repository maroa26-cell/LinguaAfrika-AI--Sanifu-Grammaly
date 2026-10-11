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
    div.stButton > button { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; width: 100% !important; border: none !important; }
    div.stButton > button:hover { background-color: #3B82F6 !important; }
</style>
""", unsafe_allow_html=True)

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900; margin-bottom: 0;'>🔐 OURWORTHLINKS MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px;'>Sovereign Triple-Gateway Identity Portal & B2B Analytics Suite</p>", unsafe_allow_html=True)
str_platform.write("---")

if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "mlangoni"

# =====================================================================
# 🎛️ NYERERE GATEWAY SELECTOR (UCHAGUZI WA VYUMBA VITATU MBALIKAMBALI)
# =====================================================================
if str_platform.session_state["active_gateway"] == "mlangoni":
    str_platform.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Tafadhali chagua lango lako la kiofisi ili kuingia hewani:</h4>", unsafe_allow_html=True)
    
    col_g1, col_g2, col_g3 = str_platform.columns(3)
    with col_g1:
        if str_platform.button("🚪 Fungua Lango la Utawala (Admin)", key="btn_gate_admin"):
            str_platform.session_state["active_gateway"] = "admin_suite"
            str_platform.rerun()
    with col_g2:
        if str_platform.button("🔐 Kuingia Kama Premium User (Sign In)", key="btn_gate_premium"):
            str_platform.session_state["active_gateway"] = "premium_suite"
            str_platform.rerun()
    with col_g3:
        if str_platform.button("✨ Lango la Malipo ya Premium (Pesapal)", key="btn_gate_signup"):
            str_platform.session_state["active_gateway"] = "premium_billing_funnel"
            str_platform.rerun()

# =====================================================================
# 📂 CHUMBA CHA 1: 👑 LANGO LA UTAWALA (ADMIN SUITE LOGIC)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "admin_suite":
    if str_platform.button("← Rudi Mlangoni", key="back_from_admin"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    jina_admin = str_platform.text_input("Username ya Siri ya Utawala:", key="v14_admin_user")
    pass_admin = str_platform.text_input("Nenosiri la Siri la Utawala:", type="password", key="v14_admin_pass")
    
    if str_platform.button("Zindua Mifumo ya Utawala", key="v14_btn_admin_verify"):
        if database.thibitisha_utambulisho_wa_siri(jina_admin, pass_admin, "Admin"):
            str_platform.success("🔓 Karibu Kiongozi! Mifumo yote ya B2B Token Channels ipo hai.")
            str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
            data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
            str_platform.table(data_b2b)
        else:
            str_platform.error("🛑 Hitilafu: Data si sahihi!")

# =====================================================================
# 📂 CHUMBA CHA 2: 🚪 LANGO LA MTEJA WA PREMIUM (SIGN IN PREMIUM)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "premium_suite":
    if str_platform.button("← Rudi Mlangoni", key="back_from_premium"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    jina_premium = str_platform.text_input("Ingiza Username Yako ya Premium:", key="v14_premium_user")
    pass_premium = str_platform.text_input("Ingiza Nenosiri Lako:", type="password", key="v14_premium_pass")
    
    if str_platform.button("Thibitisha Identity ya Premium", key="v14_btn_premium_login"):
        if database.thibitisha_utambulisho_wa_siri(jina_premium, pass_premium, "Premium User"):
            str_platform.session_state["user_status"] = "standard_premium"
            str_platform.session_state["active_user_name"] = jina_premium
            str_platform.success("✅ Karibu Kiongozi! Vifurushi vyote vipo hai sasa hivi.")
        else:
            str_platform.error("🛑 Hitilafu: Password au Username si sahihi!")

# =====================================================================
# 📂 CHUMBA CHA 3: 💳 LANGO LA PREMIUM BILLING FUNNEL (TABO MBILI)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "premium_billing_funnel":
    if str_platform.button("← Rudi Mlangoni", key="back_from_billing"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
        
    tab_mpya, tab_wa_zamani = str_platform.tabs(["📝 MIMI NI MTUMIAJI MPYA (Sign Up)", "🔑 MIMI NI MTUMIAJI WA ZAMANI (Sign In to Pay)"])
    
    with tab_mpya:
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
                    str_platform.error("🛑 Jina hili limechukuliwa tayari!")
            else:
                str_platform.warning("⚠️ Jaza vigezo vyote!")
                
        if str_platform.session_state["signup_completed"]:
            str_platform.success(f"✅ Usajili wa akaunti '{str_platform.session_state['saved_signup_username'].upper()}' umekubaliwa kiofisi mwilini mwa database!")
            str_platform.write("---")
            str_platform.markdown("### 💳 Hatua ya 2: Kamilisha Malipo ya Pesapal ($5.00 USD)")
            njia_malipo_1 = str_platform.radio("Chagua Njia ya Malipo:", ["Mobile Money (M-Pesa/Tigo Pesa)", "Kadi ya Benki"], key="v14_pay_radio_tab1")
            if str_platform.button("Zindua Ankara ya Pesapal", key="v14_btn_pesapal_tab1"):
                try:
                    matokeo_p = pesapal_core.anzisha_muamala_wa_pesapal(str_platform.session_state["saved_signup_username"], str_platform.session_state["saved_signup_email"], 5.00)
                    if matokeo_p.get("status") == "success":
                        str_platform.success("📲 Lango la malipo limefunguka!")
                        str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL]({matokeo_p.get('redirect_url')})")
                    else:
                        str_platform.error(matokeo_p.get("message"))
                except Exception as e:
                    str_platform.error(f"🛑 Hitilafu: {str(e)}")

    with tab_wa_zamani:
        str_platform.markdown("### 🔑 Ingia Ili Kufungua Fomu ya Malipo")
        jina_luhula = str_platform.text_input("Username Yako Uliyojisajili Nayo:", key="v14_tab2_user")
        siri_luhula = str_platform.text_input("Nenosiri Lako la Siri:", type="password", key="v14_tab2_pass")
        
        if "signin_pay_unlocked" not in str_platform.session_state:
            str_platform.session_state["signin_pay_unlocked"] = False
            
        if str_platform.button("Uhakiki wa Akaunti", key="v14_btn_tab2_verify"):
            if database.thibitisha_utambulisho_wa_siri(jina_luhula, siri_luhula, "Premium User"):
                str_platform.session_state["signin_pay_unlocked"] = True
                str_platform.session_state["saved_pay_username"] = jina_luhula.strip()
                str_platform.session_state["saved_pay_email"] = f"{jina_luhula.strip()}@ourworthlinks.com"
            else:
                str_platform.error("🛑 Jina au password si sahihi!")
                
        # 👑 THE ABSOLUTE REPAIR FIX: Kufunga try-except block yote ya kishindo hadi mwisho bila herufi iliyokatika!
        if str_platform.session_state["signin_pay_unlocked"]:
            str_platform.success(f"🔓 Akaunti ya '{str_platform.session_state['saved_pay_username'].upper()}' imetambuliwa!")
            str_platform.write("---")
            njia_malipo_2 = str_platform.radio("Chagua Njia ya Malipo:", ["Mobile Money (M-Pesa/Tigo Pesa)", "Kadi ya Benki"], key="v14_pay_radio_tab2")
