import streamlit as str_platform
import database
import pesapal_core
import sqlite3

str_platform.set_page_config(page_title="Ourworthlinks Dashboard", page_icon="🔐", layout="wide")
try: 
    database.anzisha_hifadhidata_ya_chuma()
except Exception: 
    pass

str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #0F172A !important; font-family: 'Segoe UI', sans-serif !important; color: #ffffff !important; }
    .stTextInput label, .stSelectbox label { color: #E2E8F0 !important; font-weight: bold !important; }
    div.stButton > button, div.stLinkButton > a { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; padding: 14px 28px !important; border-radius: 8px !important; width: 100% !important; border: none !important; text-align: center !important; text-decoration: none !important; display: inline-block !important; }
    div.stButton > button:hover, div.stLinkButton > a:hover { background-color: #3B82F6 !important; }
    .pricing-card { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important; border: 3px solid #D97706 !important; border-radius: 16px !important; padding: 35px !important; text-align: center; margin: 20px auto !important; max-width: 450px !important; }
</style>
""", unsafe_allow_html=True)

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>🔐 OURWORTHLINKS GLOBAL MANAGEMENT PORTAL</h1>", unsafe_allow_html=True)
str_platform.write("---")

if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "mlangoni"

if str_platform.session_state["active_gateway"] == "mlangoni":
    col_g1, col_g2 = str_platform.columns(2)
    with col_g1:
        if str_platform.button("🚪 Lango la Admin (Utawala)", key="g_admin"):
            str_platform.session_state["active_gateway"] = "admin_s"; str_platform.rerun()
    with col_g2:
        if str_platform.button("🔐 Lango la Mteja (Sign In / Sign Up)", key="g_client"):
            str_platform.session_state["active_gateway"] = "client_auth_s"; str_platform.rerun()

elif str_platform.session_state["active_gateway"] == "admin_s":
    if str_platform.button("← Rudi Mlangoni", key="b_ad"): 
        str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    
    user = str_platform.text_input("Admin Username:")
    pas = str_platform.text_input("Admin Password:", type="password")
    
    if str_platform.button("Ingia Utawala"):
        if database.thibitisha_utambulisho_wa_siri(user, pas, "admin"):
            str_platform.session_state["admin_logged_in"] = True
            str_platform.success("🔓 Karibu Kiongozi!")
        else: 
            str_platform.error("Hitilafu ya usalama!")

    if str_platform.session_state.get("admin_logged_in"):
        str_platform.write("---")
        str_platform.markdown("### 📚 BULK SWAHILI DATASET UPLOADER")
        uploaded_file = str_platform.file_uploader("Upload Swahili Dataset (CSV Format Only):", type=["csv"])
        
        if uploaded_file is not None:
            try:
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                if 'keyword' in df.columns and 'semantic_meaning' in df.columns:
                    conn = database.pata_muunganisho_wa_chuma()
                    cursor = conn.cursor()
                    success_count = 0
                    
                    for _, row in df.iterrows():
                        try:
                            cursor.execute("INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)", (str(row['keyword']).strip().lower(), str(row['semantic_meaning']).strip()))
                            success_count += 1
                        except sqlite3.IntegrityError:
                            pass
                    conn.commit()
                    conn.close()
                    str_platform.success(f"✅ Ingestion successful! Loaded {success_count} terms into the system spinal cord!")
                else:
                    str_platform.error("CSV must contain 'keyword' and 'semantic_meaning' columns.")
            except Exception as e:
                str_platform.error(f"Error parsing file: {str(e)}")

elif str_platform.session_state["active_gateway"] == "client_auth_s":
    if str_platform.button("← Rudi Mlangoni", key="b_cl"): 
        str_platform.session_state["active_gateway"] = "mlangoni"; str_platform.rerun()
    t_mpya, t_zamani = str_platform.tabs(["📝 MTUMIAJI MPYA (Sign Up)", "🔑 SIGN IN (Premium Sign In)"])
    
    with t_mpya:
        u_new = str_platform.text_input("Unda Username Mpya:", key="unew")
        p_new = str_platform.text_input("Unda Password Mpya:", type="password", key="pnew")
        if str_platform.button("Thibitisha Usajili wa Akaunti", key="b_up"):
            if u_new.strip() != "" and p_new.strip() != "":
                if database.sajili_mtumiaji_mpya(u_new.strip(), p_new.strip(), "premium user"):
                    str_platform.success(f"✅ Usajili umekubaliwa! Ingia kupitia tabo ya pili.")
                else: 
                    str_platform.error("Jina limechukuliwa tayari!")

    with t_zamani:
        u_old = str_platform.text_input("Ingiza Username Yako:", key="uold")
        p_old = str_platform.text_input("Ingiza Password Yako:", type="password", key="pold")
        if str_platform.button("Ingia Ndani ya Mfumo", key="b_in"):
            if database.thibitisha_utambulisho_wa_siri(u_old.strip(), p_old.strip(), "premium user"):
                str_platform.session_state["active_gateway"] = "premium_member_suite"
                str_platform.session_state["member_username"] = u_old.strip()
                str_platform.rerun()
            else: 
                str_platform.error("Hadhi au password si sahihi!")

elif str_platform.session_state["active_gateway"] == "premium_member_suite":
    str_platform.markdown(f"<h3 style='text-align: center; color: #3B82F6;'>👋 Karibu Ndani ya Mfumo wa Dunia, {str_platform.session_state['member_username'].upper()}!</h3>", unsafe_allow_html=True)
    
    str_platform.markdown("""
    <div class='pricing-card'>
        <h2 style='color: #D97706; margin-bottom: 5px;'>💎 LINGUAAFRIKA PREMIUM</h2>
        <p style='color: #94A3B8; font-size: 14px;'>Global Swahili Voice & AI Phonetic Core</p>
        <hr style='border-color: rgba(217,119,6,0.2);'>
        <h1 style='color: #ffffff; font-size: 48px; margin: 15px 0;'>$5.00 <span style='font-size: 16px; color: #94A3B8;'>/ Mwezi</span></h1>
        <ul style='text-align: left; color: #E2E8F0; font-size: 14px; padding-left: 20px; line-height: 1.8;'>
            <li>✨ Ukaguzi wa Sarufi na Ukalimani wa Lugha 14 Pro</li>
            <li>⚡ Kasi ya Radi ya Chini ya 150ms Synapse Latency</li>
            <li>🏢 Global Stripe & PayPal Multi-Currency Support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = str_platform.columns(3)
    with col_c2:
        lango_chaguo = str_platform.radio("Chagua Njia ya Malipo (Select Gateway):", ["🇹🇿 Pesapal (Mobile Money / East Africa)", "🌐 Stripe / PayPal (International Cards)"], key="v14_global_pay_radio")
        str_platform.write("---")
        
        user_active = str_platform.session_state["member_username"]
        
        if "🇹🇿 Pesapal" in lango_chaguo:
            live_pesapal_url = pesapal_core.anzisha_muamala_wa_pesapal(user_active, f"{user_active}@ourworthlinks.com")
            str_platform.link_button("💳 Lipia via Pesapal ($5.00 USD)", url=live_pesapal_url, key="b_pesa_btn")
        else:
            stripe_checkout_live_url = f"https://stripe.com{user_active}"
            str_platform.link_button("💳 Lipia via Stripe / PayPal ($5.00 USD)", url=stripe_checkout_live_url, key="b_stripe_btn")
            
    str_platform.write("---")
    if str_platform.button("← Toka Kwenye Akaunti Yako (Log Out)", key="b_logout"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 Ourworthlinks • Global AI Pipeline</p>", unsafe_allow_html=True)
