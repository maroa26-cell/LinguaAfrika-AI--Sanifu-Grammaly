import streamlit as str_platform
import database
import pesapal_core

str_platform.set_page_config(page_title="Ourworthlinks Dashboard", page_icon="🔐", layout="wide")
try: database.anzisha_hifadhidata_ya_chuma()
except Exception: pass

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>🔐 OURWORTHLINKS SYSTEM</h1>", unsafe_allow_html=True)
str_platform.write("---")

if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "mlangoni"

# =====================================================================
# 🎛️ NYERERE GATEWAY SELECTOR (VYUMBA VIWILI PEKEE MLANGONI)
# =====================================================================
if str_platform.session_state["active_gateway"] == "mlangoni":
    str_platform.markdown("<h4 style='text-align: center; color: #E2E8F0;'>Tafadhali chagua lango lako la kiofisi:</h4>", unsafe_allow_html=True)
    col_g1, col_g2 = str_platform.columns(2)
    with col_g1:
        if str_platform.button("🚪 Lango la Admin (Utawala)", key="g_admin"):
            str_platform.session_state["active_gateway"] = "admin_s"; str_platform.rerun()
    with col_g2:
        if str_platform.button("🔐 Lango la Mteja (Sign In / Sign Up)", key="g_client"):
            str_platform.session_state["active_gateway"] = "client_auth_s"; str_platform.rerun()

# 📂 CHUMBA CHA 1: LANGO LA ADMIN
elif str_platform.session_state["active_gateway"] == "admin_s":
    if str_platform.button("← Rudi Mlangoni", key="b_ad"): 
        str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    user = str_platform.text_input("Admin Username:")
    pas = str_platform.text_input("Admin Password:", type="password")
    if str_platform.button("Ingia Utawala"):
        if database.thibitisha_utambulisho_wa_siri(user, pas, "Admin"):
            str_platform.success("🔓 Karibu Kiongozi!")
            str_platform.write("💰 **B2B Revenue: $1,240.50 USD**")
        else: str_platform.error("Hitilafu ya usalama!")

# 📂 CHUMBA CHA 2: LANGO LA AUTHENTICATION (INGIA AU JISAJILI KWANZA)
elif str_platform.session_state["active_gateway"] == "client_auth_s":
    if str_platform.button("← Rudi Mlangoni", key="b_cl"): 
        str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
        
    t_mpya, t_zamani = str_platform.tabs(["📝 MTUMIAJI MPYA (Sign Up)", "🔑 MTUMIAJI WA ZAMANI (Sign In)"])
    
    with t_mpya:
        u_new = str_platform.text_input("Unda Username Mpya:", key="unew")
        p_new = str_platform.text_input("Unda Password Mpya:", type="password", key="pnew")
        if str_platform.button("Thibitisha Usajili wa Akaunti", key="b_up"):
            if u_new.strip() != "" and p_new.strip() != "":
                if database.sajili_mtumiaji_mpya(u_new.strip(), p_new.strip(), "Premium User"):
                    str_platform.success(f"✅ Usajili umekubaliwa! Ingia kupitia tabo ya pili kuelekea kiofisi.")
                else: str_platform.error("Jina limechukuliwa tayari!")

    with t_zamani:
        u_old = str_platform.text_input("Ingiza Username Yako:", key="uold")
        p_old = str_platform.text_input("Ingiza Password Yako:", type="password", key="pold")
        if str_platform.button("Ingia Ndani ya Mfumo", key="b_in"):
            if database.thibitisha_utambulisho_wa_siri(u_old.strip(), p_old.strip(), "Premium User"):
                str_platform.session_state["active_gateway"] = "premium_member_suite"
                str_platform.session_state["member_username"] = u_old.strip()
                str_platform.rerun()
            else: str_platform.error("Hadhi au password si sahihi!")

# =====================================================================
# 📂 CHUMBA CHA 3: KATI KATI YA MFUMO PEKEE (PREMIUM MEMBER SUITE & PESAPAL)
# =====================================================================
elif str_platform.session_state["active_gateway"] == "premium_member_suite":
    str_platform.markdown(f"### 👑 KARIBU NDANI YA MFUMO WA LINGUAAFRIKA AI, {str_platform.session_state['member_username'].upper()}!")
    str_platform.write("---")
    
    # 👑 HOOK YA BIASHARA: Lango la malipo sasa hivi limefichwa ndani ya chumba cha siri cha mteja pekee!
    str_platform.warning("⚠️ Hadhi ya Akaunti Yako: MTUMIAJI WA KAWAIDA. Ili kuwasha mitambo ya Sauti ya Premium, unapaswa kusafisha ankara ya mwezi.")
    
    if str_platform.button("💳 Amsha Huduma za Premium ($5.00 USD via Pesapal)", key="b_live_pay"):
        user_active = str_platform.session_state["member_username"]
        res = pesapal_core.anzisha_muamala_wa_pesapal(user_active, f"{user_active}@ourworthlinks.com")
        str_platform.success("📲 Ankara ya kiofisi imezalishwa salama!")
        str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL KULIPIA]({res.get('redirect_url')})")
        
    str_platform.write("---")
    if str_platform.button("← Toka Kwenye Akaunti Yako (Log Out)", key="b_logout"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 Ourworthlinks</p>", unsafe_allow_html=True)
