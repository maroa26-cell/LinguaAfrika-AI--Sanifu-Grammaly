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
        
        # 🔥 ANTI-CLICKJACKING VACCINE: Inalazimisha kufungua tabo mpya salama ya nje ikiepuka kabisa iframe block ya Chrome!
        str_platform.markdown(f'<a href="{pesapal_redirect}" target="_blank" style="background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%); color: white; font-weight: bold; padding: 14px 28px; border-radius: 12px; text-decoration: none; display: block; text-align: center; box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3); font-size: 16px;">💳 Subscribe via Local Mobile Money ($5.00)</a>', unsafe_allow_html=True)

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
        
        # 🔥 ANTI-CLICKJACKING VACCINE: Inalazimisha kufungua tabo mpya salama ya nje ikiepuka kabisa iframe block ya Chrome!
        str_platform.markdown(f'<a href="{stripe_redirect}" target="_blank" style="background: linear-gradient(135deg, #D97706 0%, #B45309 100%); color: white; font-weight: bold; padding: 14px 28px; border-radius: 12px; text-decoration: none; display: block; text-align: center; box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3); font-size: 16px;">💳 Purchase Commercial B2B License ($49.00)</a>', unsafe_allow_html=True)

    str_platform.write("---")
    if str_platform.button("← Toka Kwenye Akaunti Yako (Log Out)", key="b_logout"):
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()

str_platform.write("---")
str_platform.markdown("<p style='text-align: center; font-size: 12px; color: #64748B;'>© 2026 Ourworthlinks • Automated Monetization Nodes Connected</p>", unsafe_allow_html=True)
