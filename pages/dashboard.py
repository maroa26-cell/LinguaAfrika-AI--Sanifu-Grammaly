import streamlit as str_platform
import sqlite3
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import database
import pesapal_core
import otp_sms
import skin_appearance

str_platform.set_page_config(page_title="Ourworthlinks Business - Premium Hub", layout="wide")
skin_appearance.inject_premium_glassmorphic_skin()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>\U0001F510 OURWORTHLINKS BUSINESS PREMIUM HUB</h1>", unsafe_allow_html=True)
str_platform.write("---")

# ------------------------------------------------------------------ #
#  WEBHOOK / CALLBACK: Mteja amerudi kutoka Pesapal
#  USALAMA: HATUAMINI kigezo 'status' kutoka URL. Tunahakiki hali
#  HALISI moja kwa moja na Pesapal kabla ya kumpandisha mteja Premium.
# ------------------------------------------------------------------ #
try:
    v = str_platform.query_params
    tid = v.get("OrderTrackingId") or v.get("pesapal_tracking_id")
    if tid:
        hali = pesapal_core.angalia_hali_ya_malipo(str(tid).strip())
        if hali["status_desc"] == "COMPLETED":
            if database.pandisha_hadhi_ya_mteja_kiotomatiki(str(tid).strip(), "completed"):
                str_platform.success("\u2705 Malipo yamethibitishwa! Hadhi yako imepandishwa kuwa Premium.")
        elif hali["status_desc"] == "PENDING":
            str_platform.info("\u23F3 Malipo bado yanasubiri (PENDING). Tafadhali subiri kidogo kisha pakia upya.")
        elif hali["status_desc"].startswith("ERROR"):
            str_platform.warning("\u26A0\uFE0F Imeshindikana kuhakiki malipo kwa sasa. Jaribu tena baadaye.")
        else:
            str_platform.error(f"\u274C Hali ya malipo: {hali['status_desc']}")
except Exception:
    # Pesapal status may be temporarily unavailable; keep the page usable.
    str_platform.warning("Tumerejea kutoka Pesapal, lakini hali ya malipo haikuweza kuhakikiwa sasa hivi. Tafadhali jaribu kupakia upya.")

# Do not overwrite an existing authenticated session on every rerun.
if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "client_auth_s"

gate = str_platform.session_state["active_gateway"]

# ------------------------------------------------------------------ #
#  HATUA 1: Sign Up / Sign In (username + password)
# ------------------------------------------------------------------ #
if gate == "client_auth_s":
    t1, t2 = str_platform.tabs(["\U0001F4DD MTUMIAJI MPYA (Sign Up)", "\U0001F511 PREMIUM SIGN IN"])
    with t1:
        un = str_platform.text_input("Username Mpya:")
        simu_su = str_platform.text_input("Namba ya Simu (mf. 0712 345 678):", key="simu_signup")
        pw = str_platform.text_input("Password Mpya:", type="password")
        if str_platform.button("Thibitisha Usajili") and un.strip() and pw.strip():
            simu_safi = otp_sms.safisha_simu(simu_su)
            if not simu_safi:
                str_platform.error("Namba ya simu si sahihi. Tumia namba ya Tanzania, mf. 0712345678.")
            elif otp_sms.simu_inatumika(simu_safi):
                str_platform.error("Namba hii tayari inatumika na akaunti nyingine.")
            elif database.sajili_mtumiaji_mpya(un.strip(), pw.strip(), "premium user"):
                otp_sms.hifadhi_simu(un.strip(), simu_safi)
                str_platform.success("Usajili umekubaliwa! Proceed to Sign In.")
            else:
                str_platform.error("Usajili umeshindikana (huenda username tayari ipo).")
    with t2:
        un_o = str_platform.text_input("Ingiza Username:")
        pw_o = str_platform.text_input("Ingiza Password:", type="password")
        if str_platform.button("Ingia Mfumo") and un_o.strip() and pw_o.strip():
            if otp_sms.login_imefungwa(un_o):
                str_platform.error("Majaribio mengi yameshindikana. Subiri dakika 15 kisha jaribu tena.")
            elif database.thibitisha_utambulisho_wa_siri(un_o.strip(), pw_o.strip(), "premium user"):
                otp_sms.futa_makosa_ya_login(un_o)
                simu_ya_mteja = otp_sms.pata_simu(un_o.strip())
                str_platform.session_state["pending_user"] = un_o.strip()
                str_platform.session_state["pending_simu"] = simu_ya_mteja
                str_platform.session_state["simu_mpya"] = False
                if simu_ya_mteja:
                    ok, err = otp_sms.tuma_otp(un_o.strip(), simu_ya_mteja)
                    if ok:
                        str_platform.session_state["active_gateway"] = "otp_step"
                        str_platform.rerun()
                    else:
                        str_platform.error(err)
                else:
                    # Akaunti ya zamani isiyo na namba: mtumiaji aiongeze kwenye hatua ya OTP.
                    str_platform.session_state["active_gateway"] = "otp_step"
                    str_platform.rerun()
            else:
                otp_sms.rekodi_kosa_la_login(un_o)
                str_platform.error("Username au password si sahihi.")

# ------------------------------------------------------------------ #
#  HATUA 2: Thibitisha kwa msimbo wa SMS (OTP)
# ------------------------------------------------------------------ #
elif gate == "otp_step":
    u_pend = str_platform.session_state.get("pending_user")
    simu_pend = str_platform.session_state.get("pending_simu")

    if not u_pend:
        str_platform.session_state["active_gateway"] = "client_auth_s"
        str_platform.rerun()

    str_platform.markdown("### \U0001F4F2 Thibitisha kwa SMS")

    if not simu_pend:
        str_platform.info("Akaunti yako haina namba ya simu. Ongeza namba, tutakutumia msimbo wa kuithibitisha.")
        simu_mpya = str_platform.text_input("Namba ya Simu (mf. 0712 345 678):", key="simu_enroll")
        if str_platform.button("Tuma Msimbo"):
            s = otp_sms.safisha_simu(simu_mpya)
            if not s:
                str_platform.error("Namba ya simu si sahihi. Tumia namba ya Tanzania.")
            elif otp_sms.simu_inatumika(s, u_pend):
                str_platform.error("Namba hii tayari inatumika na akaunti nyingine.")
            else:
                ok, err = otp_sms.tuma_otp(u_pend, s)
                if ok:
                    str_platform.session_state["pending_simu"] = s
                    str_platform.session_state["simu_mpya"] = True
                    str_platform.rerun()
                else:
                    str_platform.error(err)
    else:
        str_platform.info(f"Msimbo wa tarakimu 6 umetumwa kwa {otp_sms.ficha_simu(simu_pend)}.")
        msimbo = str_platform.text_input("Ingiza msimbo:", max_chars=6, key="otp_code")
        c_a, c_b, c_c = str_platform.columns(3)
        with c_a:
            if str_platform.button("Thibitisha", type="primary", use_container_width=True):
                ok, err = otp_sms.hakiki_otp(u_pend, msimbo)
                if ok:
                    if str_platform.session_state.get("simu_mpya") and not otp_sms.hifadhi_simu(u_pend, simu_pend):
                        str_platform.session_state["pending_simu"] = None
                        str_platform.error("Namba hii imechukuliwa na akaunti nyingine. Tumia namba tofauti.")
                    else:
                        str_platform.session_state["member_username"] = u_pend
                        str_platform.session_state["member_simu"] = simu_pend
                        str_platform.session_state["active_gateway"] = "premium_member_suite"
                        for k in ("pending_user", "pending_simu", "simu_mpya"):
                            str_platform.session_state.pop(k, None)
                        str_platform.rerun()
                else:
                    str_platform.error(err)
        with c_b:
            if str_platform.button("Tuma tena msimbo", use_container_width=True):
                ok, err = otp_sms.tuma_otp(u_pend, simu_pend)
                if ok:
                    str_platform.success("Msimbo mpya umetumwa.")
                else:
                    str_platform.error(err)
        with c_c:
            if str_platform.button("Rudi nyuma", use_container_width=True):
                str_platform.session_state.clear()
                str_platform.rerun()

# ------------------------------------------------------------------ #
#  HATUA 3: Premium Hub
# ------------------------------------------------------------------ #
elif gate == "premium_member_suite":
    u_active = str_platform.session_state["member_username"]
    str_platform.markdown(f"### Welcome to the Ourworthlinks Global Marketplace, {u_active.upper()}!")

    curr = str_platform.selectbox("Chagua Sarafu:", ["USD (Base)", "TZS (Converted)", "KES (Converted)"])
    kiasi_cha_msingi_usd = 5.00
    if "TZS" in curr:
        amt = kiasi_cha_msingi_usd * 2600.00
    elif "KES" in curr:
        amt = kiasi_cha_msingi_usd * 130.00
    else:
        amt = kiasi_cha_msingi_usd

    s_symbol = "TZS" if "TZS" in curr else ("KES" if "KES" in curr else "USD")
    str_platform.info(f"Kiwango cha Kulipa: **{amt:,.2f} {s_symbol}**")

    # Create Pesapal order only after the customer clicks the payment button,
    # rather than creating a new order on every Streamlit rerun.
    # Tunatumia namba ya simu iliyothibitishwa (OTP) badala ya email ya kubuni.
    simu_mteja = str_platform.session_state.get("member_simu")
    stripe_redirect = pesapal_core.generate_stripe_global_checkout(u_active, dynamic_cost=49.00)

    cp1, cp2 = str_platform.columns(2)
    with cp1:
        str_platform.markdown(
            f"<div style='border:1px solid #3B82F6; padding:20px; border-radius:12px;'>"
            f"<h3>\U0001F48E LINGUAAFRIKA PREMIUM SUITE</h3><h1>{s_symbol} {amt:,.2f}</h1></div>",
            unsafe_allow_html=True,
        )
        if str_platform.button("💳 Subscribe via Local Mobile Money", type="primary", use_container_width=True):
            pesapal_redirect = pesapal_core.anzisha_muamala_wa_pesapal(
                u_active, "", kiasi_usd=kiasi_cha_msingi_usd, sarafu=s_symbol, simu=simu_mteja
            )
            if "error=" in str(pesapal_redirect) or str(pesapal_redirect).strip() == "#":
                sababu = str(pesapal_redirect).split("error=")[-1] if "error=" in str(pesapal_redirect) else "Unknown"
                str_platform.error(f"Pesapal haikuweza kuanzisha malipo (sababu: {sababu}). Hakikisha APP_URL na Pesapal Secrets ni sahihi.")
            elif not str(pesapal_redirect).startswith(("https://", "http://")):
                str_platform.error("Pesapal imerudisha kiungo kisicho sahihi. Jaribu tena baadaye.")
            else:
                str_platform.link_button(
                    "Fungua ukurasa wa malipo wa Pesapal",
                    str(pesapal_redirect).strip(),
                    type="primary",
                    use_container_width=True,
                )
    with cp2:
        str_platform.markdown(
            "<div style='border:1px solid #D97706; padding:20px; border-radius:12px;'>"
            "<h3>\U0001F6E1\uFE0F SOVEREIGN CODE AUDITOR</h3><h1>USD $49.00</h1></div>",
            unsafe_allow_html=True,
        )
        str_platform.link_button("Purchase Commercial B2B License", stripe_redirect, type="secondary", use_container_width=True)

    if str_platform.button("Ondoka kwenye Akaunti (Log Out)"):
        str_platform.session_state.clear()
        str_platform.rerun()
