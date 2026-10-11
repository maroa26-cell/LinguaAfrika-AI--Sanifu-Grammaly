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

if str_platform.session_state["active_gateway"] == "mlangoni":
    col_g1, col_g2, col_g3 = str_platform.columns(3)
    with col_g1:
        if str_platform.button("🚪 Lango la Admin", key="g_admin"): str_platform.session_state["active_gateway"] = "admin_s"; str_platform.rerun()
    with col_g2:
        if str_platform.button("🔐 Premium Sign In", key="g_prem"): str_platform.session_state["active_gateway"] = "premium_s"; str_platform.rerun()
    with col_g3:
        if str_platform.button("✨ Lipia Premium (Pesapal)", key="g_pay"): str_platform.session_state["active_gateway"] = "billing_s"; str_platform.rerun()

elif str_platform.session_state["active_gateway"] == "admin_s":
    if str_platform.button("← Rudi Mlangoni"): str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    user = str_platform.text_input("Admin Username:")
    pas = str_platform.text_input("Admin Password:", type="password")
    if str_platform.button("Ingia Utawala"):
        if database.thibitisha_utambulisho_wa_siri(user, pas, "Admin"):
            str_platform.success("🔓 Karibu Kiongozi!")
            str_platform.write("💰 **B2B Revenue: $1,240.50 USD**")
        else: str_platform.error("Hitilafu!")

elif str_platform.session_state["active_gateway"] == "premium_s":
    if str_platform.button("← Rudi Mlangoni"): str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    user = str_platform.text_input("Premium Username:")
    pas = str_platform.text_input("Premium Password:", type="password")
    if str_platform.button("Thibitisha Kuingia"):
        if database.thibitisha_utambulisho_wa_siri(user, pas, "Premium User"): str_platform.success("✅ Karibu Kwenye Zana za Premium!")
        else: str_platform.error("Hitilafu!")

elif str_platform.session_state["active_gateway"] == "billing_s":
    if str_platform.button("← Rudi Mlangoni"): str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    t_mpya, t_zamani = str_platform.tabs(["📝 MTUMIAJI MPYA (Sign Up)", "🔑 MTUMIAJI WA ZAMANI (Sign In to Pay)"])
    
    with t_mpya:
        u_new = str_platform.text_input("Unda Username Mpya:", key="unew")
        p_new = str_platform.text_input("Unda Password Mpya:", type="password", key="pnew")
        if str_platform.button("Thibitisha Usajili", key="b_up"):
            if u_new.strip() != "" and p_new.strip() != "":
                if database.sajili_mtumiaji_mpya(u_new.strip(), p_new.strip(), "Premium User"):
                    str_platform.session_state["reg_user"] = u_new.strip()
                    str_platform.success(f"✅ Usajili wa '{u_new.upper()}' umekubaliwa!")
                else: str_platform.error("Jina limechukuliwa!")
        
        if "reg_user" in str_platform.session_state:
            if str_platform.button("Bofya Hapa Kulipia Kifurushi ($5.00 USD)", key="b_pay1"):
                res = pesapal_core.anzisha_muamala_wa_pesapal(str_platform.session_state["reg_user"], f"{str_platform.session_state['reg_user']}@ourworthlinks.com")
                str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL]({res.get('redirect_url')})")

    with t_zamani:
        u_old = str_platform.text_input("Username Yako:", key="uold")
        p_old = str_platform.text_input("Password Yako:", type="password", key="pold")
        if str_platform.button("Uhakiki wa Akaunti", key="b_in"):
            if database.thibitisha_utambulisho_wa_siri(u_old.strip(), p_old.strip(), "Premium User"):
                str_platform.session_state["pay_user"] = u_old.strip()
                str_platform.success("🔓 Akaunti imetambuliwa!")
        
        if "pay_user" in str_platform.session_state:
            if str_platform.button("Bofya Hapa Kulipia Ankara ($5.00 USD)", key="b_pay2"):
                res2 = pesapal_core.anzisha_muamala_wa_pesapal(str_platform.session_state["pay_user"], f"{str_platform.session_state['pay_user']}@ourworthlinks.com")
                str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL]({res2.get('redirect_url')})")

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 Ourworthlinks</p>", unsafe_allow_html=True)
