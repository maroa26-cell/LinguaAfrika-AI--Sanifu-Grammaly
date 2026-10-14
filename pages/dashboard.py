elif str_platform.session_state["active_gateway"] == "premium_member_suite":
    username_active = str_platform.session_state["member_username"]
    str_platform.markdown(f"<h3 style='color: #3B82F6;'>👋 Welcome to the Ourworthlinks Global Marketplace, {username_active.upper()}!</h3>", unsafe_allow_html=True)
    str_platform.write("---")
    
    # 👑 BASE CURRENCY INTERFACE: Thamani ya msingi ni USD, ubadilishaji wa kiotomatiki kwa Streamlit vigezo
    kiasi_cha_msingi_usd = 5.00
    sarafu_chaguo = str_platform.selectbox("💳 Chagua Sarafu Unayotaka Kulipia (Select Payment Currency):", ["USD (Dola ya Marekani - Base)", "TZS (Shilingi ya Tanzania - Converted)", "KES (Shilingi ya Kenya - Converted)"], key="currency_select_node")
    
    if "TZS" in sarafu_chaguo:
        sarafu_halisi = "TZS"
        onyesha_kiasi = kiasi_cha_msingi_usd * 2600.00
    elif "KES" in sarafu_chaguo:
        sarafu_halisi = "KES"
        onyesha_kiasi = kiasi_cha_msingi_usd * 130.00
    else:
        sarafu_halisi = "USD"
        onyesha_kiasi = kiasi_cha_msingi_usd

    str_platform.info(f"💰 Thamani ya Kifurushi: **${kiasi_cha_msingi_usd:.2f} USD** ──► Kiasi Halisi cha Kulipa: **{onyesha_kiasi:,.2f} {sarafu_halisi}**")
    str_platform.write("---")
    col_package_1, col_package_2 = str_platform.columns(2)
    
    with col_package_1:
        str_platform.markdown(f"""
        <div class='monetize-card' style='border-color: #3B82F6 !important; padding: 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h3 style='color: #3B82F6; margin: 0;'>💎 LINGUAAFRIKA PREMIUM SUITE</h3>
            <p style='color: #64748B; font-size: 13px;'>Localized Contextual AI Processing Engine</p>
            <h1 style='margin: 15px 0;'>{sarafu_halisi} {onyesha_kiasi:,.2f} <span style='font-size:14px; color:#64748B;'>/ mo</span></h1>
            <p style='font-size:14px; color:#E2E8F0;'>• Multi-contextual Swahili translation<br>• Zero rate limits and 150ms priority execution channels</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🚀 Tuma oda kwenda pesapal_core kupata link rasmi ya kibenki
        pesapal_redirect = pesapal_core.anzisha_muamala_wa_pesapal(username_active, f"{username_active}@ourworthlinks.com", kiasi_usd=kiasi_cha_msingi_usd, sarafu=sarafu_halisi)
        
        # 🔥 STREAMLIT NATIVE VACCINE: Inatumia kitufe asili 100% cha mfumo kuruka pop-up blocks zote salama!
        str_platform.link_button(
            label=f"💳 Subscribe via Local Mobile Money ({sarafu_halisi} {onyesha_kiasi:,.2f})",
            url=pesapal_redirect,
            type="primary",
            use_container_width=True,
            key="native_pesapal_btn"
        )

    with col_package_2:
        str_platform.markdown("""
        <div class='monetize-card' style='border-color: #D97706 !important; padding: 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h3 style='color: #D97706; margin: 0;'>🛡️ SOVEREIGN CODE AUDITOR LICENSE</h3>
            <p style='color: #64748B; font-size: 13px;'>Biomimetic AI Self-Healing Security Shield</p>
            <h1 style='margin: 15px 0;'>USD $49.00 <span style='font-size:14px; color:#64748B;'>/ mo</span></h1>
            <p style='font-size:14px; color:#E2E8F0;'>• Autonomous syntax phagocytosis and protection<br>• Fully sandboxed administrative threat presentation controls</p>
        </div>
        """, unsafe_allow_html=True)
        stripe_redirect = pesapal_core.generate_stripe_global_checkout(username_active, client_package="code_auditor_license", dynamic_cost=49.00)
        
        # 🔥 STREAMLIT NATIVE VACCINE: Inatumia kitufe asili 100% cha mfumo kuruka pop-up blocks zote salama!
        str_platform.link_button(
            label="💳 Purchase Commercial B2B License ($49.00 USD)",
            url=stripe_redirect,
            type="secondary",
            use_container_width=True,
            key="native_stripe_btn"
        )

    str_platform.write("---")
    if str_platform.button("← Toka Kwenye Akaunti Yako (Log Out)", key="b_logout"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>© 2026 Ourworthlinks • Automated Monetization Nodes Connected</p>", unsafe_allow_html=True)
