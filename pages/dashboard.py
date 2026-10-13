import streamlit as str_platform
import database
import pesapal_core
import sqlite3
import skin_appearance            # 🎨 THE EPITHELIAL MATRIX: Loaded inside the management portal too!

str_platform.set_page_config(page_title="Ourworthlinks Dashboard", page_icon="🔐", layout="wide")
try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🎨 INTERFACE SKIN TRIGGER: Applies the glowing neon theme across the administrative space
skin_appearance.inject_premium_glassmorphic_skin()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>🔐 OURWORTHLINKS COMMERCIAL MANAGEMENT ENGINE</h1>", unsafe_allow_html=True)
str_platform.write("---")

try:
    if hasattr(str_platform, "experimental_get_query_params"):
        vigezo_vya_url = str_platform.experimental_get_query_params()
        tracking_id_halisi = vigezo_vya_url.get("OrderTrackingId", [None]) or vigezo_vya_url.get("pesapal_tracking_id", [None])
        status_ya_benki = vigezo_vya_url.get("status", ["completed"])
        
        if tracking_id_halisi:
            ufanisi = database.pandisha_hadhi_ya_mteja_kiotomatiki(tracking_id_halisi.strip(), status_ya_benki)
            if ufanisi:
                str_platform.success("🟢 webhook handshake: status 200 ok. client upgraded successfully!")
except Exception:
    pass

if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "mlangoni"

if str_platform.session_state["active_gateway"] == "mlangoni":
    str_platform.info("👋 Karibu Kiongozi! Tafadhali chagua lango unalotaka kufungua hapa chini ili kuanza utambuzi wa mfumo:")
    col_g1, col_g2 = str_platform.columns(2)
    with col_g1:
        if str_platform.button("🚪 Lango la Admin (Utawala)", key="g_admin"):
            str_platform.session_state["active_gateway"] = "admin_s"
            str_platform.rerun()
    with col_g2:
        if str_platform.button("🔐 Lango la Mteja (Sign In / Sign Up)", key="g_client"):
            str_platform.session_state["active_gateway"] = "client_auth_s"
            str_platform.rerun()

elif str_platform.session_state["active_gateway"] == "admin_s":
    if str_platform.button("← Rudi Mlangoni", key="b_ad"): 
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
    
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
        str_platform.markdown("### 📚 BULK DATASET INGESTION NODE")
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
                    str_platform.success(f"✅ Loaded {success_count} structural vocabulary terms directly into the system spinal cord!")
                else: str_platform.error("CSV requires 'keyword' and 'meaning' column headers.")
            except Exception as e: str_platform.error(f"Ingestion anomaly caught: {str(e)}")

elif str_platform.session_state["active_gateway"] == "client_auth_s":
    if str_platform.button("← Rudi Mlangoni", key="b_cl"): 
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
    t_mpya, t_zamani = str_platform.tabs(["📝 MTUMIAJI MPYA (Sign Up)", "🔑 SIGN IN (Premium Sign In)"])
    
    with t_mpya:
        u_new = str_platform.text_input("Unda Username Mpya:", key="unew")
        p_new = str_platform.text_input("Unda Password Mpya:", type="password", key="pnew")
        if str_platform.button("Thibitisha Usajili wa Akaunti", key="b_up"):
            if u_new.strip() != "" and p_new.strip() != "":
                if database.sajili_mtumiaji_mpya(u_new.strip(), p_new.strip(), "premium user"):
                    str_platform.success("✅ Usajili umekubaliwa! Proceed to Sign In.")
                else: str_platform.error("Jina limechukuliwa tayari!")

    with t_zamani:
        u_old = str_platform.text_input("Ingiza Username Yako:", key="uold")
        p_old = str_platform.text_input("Ingiza Password Yako:", type="password", key="pold")
        if str_platform.button("Ingia Ndani ya Mfumo", key="b_in"):
            if database.thibitisha_utambulisho_wa_siri(u_old.strip(), p_old.strip(), "premium user"):
                str_platform.session_state["active_gateway"] = "premium_member_suite"
                str_platform.session_state["member_username"] = u_old.strip()
                str_platform.rerun()
            else: str_platform.error("Hadhi au password si sahihi!")

elif str_platform.session_state["active_gateway"] == "premium_member_suite":
    username_active = str_platform.session_state["member_username"]
    str_platform.markdown(f"<h3 style='color: #3B82F6;'>👋 Welcome to the Ourworthlinks Global Marketplace, {username_active.upper()}!</h3>", unsafe_allow_html=True)
    str_platform.write("---")
    col_package_1, col_package_2 = str_platform.columns(2)
    
    with col_package_1:
        str_platform.markdown("""
        <div class='monetize-card' style='border-color: #3B82F6 !important;'>
            <h3 style='color: #3B82F6; margin: 0;'>💎 LINGUAAFRIKA PREMIUM SUITE</h3>
            <p style='color: #64748B; font-size: 13px;'>Localized Contextual AI Processing Engine</p>
            <h1 style='margin: 15px 0;'>$5.00 <span style='font-size:14px; color:#64748B;'>/ mo</span></h1>
            <p style='font-size:14px; color:#E2E8F0;'>• Multi-contextual Swahili translation<br>• Zero rate limits and 150ms priority execution channels</p>
        </div>
        """, unsafe_allow_html=True)
        pesapal_redirect = pesapal_core.anzisha_muamala_wa_pesapal(username_active, f"{username_active}@ourworthlinks.com", kiasi=5.00)
        str_platform.link_button("💳 Subscribe via Local Mobile Money ($5.00)", url=pesapal_redirect, key="sub_premium_btn")

    with col_package_2:
        str_platform.markdown("""
        <div class='monetize-card' style='border-color: #D97706 !important;'>
            <h3 style='color: #D97706; margin: 0;'>🛡️ SOVEREIGN CODE AUDITOR LICENSE</h3>
            <p style='color: #64748B; font-size: 13px;'>Biomimetic AI Self-Healing Security Shield</p>
            <h1 style='margin: 15px 0;'>$49.00 <span style='font-size:14px; color:#64748B;'>/ mo</span></h1>
            <p style='font-size:14px; color:#E2E8F0;'>• Autonomous syntax phagocytosis and protection<br>• Fully sandboxed administrative threat presentation controls</p>
        </div>
        """, unsafe_allow_html=True)
        stripe_redirect = pesapal_core.generate_stripe_global_checkout(username_active, client_package="code_auditor_license", dynamic_cost=49.00)
        str_platform.link_button("💳 Purchase Commercial B2B License ($49.00)", url=stripe_redirect, key="buy_auditor_btn")

    str_platform.write("---")
    if str_platform.button("← Toka Kwenye Akaunti Yako (Log Out)", key="b_logout"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px; color: #64748B;'>© 2026 Ourworthlinks • Automated Monetization Nodes Connected</p>", unsafe_allow_html=True)
