import streamlit as str_platform
import sqlite3
import os
import sys
import re

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import database
import pesapal_core
import risiti
import auth_2fa
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
def _onyesha_historia_ya_malipo(username):
    """Historia ya malipo + risiti (PDF) za mteja aliyeingia. Inasomwa kutoka Neon."""
    malipo = database.orodha_ya_malipo(username)
    if not malipo:
        return
    with str_platform.expander(f"\U0001F9FE Risiti na historia ya malipo yako ({len(malipo)})", expanded=False):
        for i, m in enumerate(malipo):
            c1, c2 = str_platform.columns([3, 1])
            c1.markdown(
                f"**{m['sarafu']} {m['kiasi']:,.2f}** \u2022 {m['tarehe'] or '-'}  \n"
                f"Risiti: `{m['order_ref']}` \u2022 Uthibitisho: {m['confirmation_code'] or '-'} "
                f"\u2022 {m['payment_method'] or '-'}"
            )
            pdf = risiti.tengeneza_pdf(m)
            if pdf:
                c2.download_button(
                    "\u2B07\uFE0F Pakua PDF", data=pdf,
                    file_name=f"risiti_{m['order_ref']}.pdf", mime="application/pdf",
                    key=f"risiti_pdf_{i}_{m['order_ref']}",
                )
            else:
                c2.download_button(
                    "\u2B07\uFE0F Pakua risiti", data=risiti.tengeneza_html(m).encode("utf-8"),
                    file_name=f"risiti_{m['order_ref']}.html", mime="text/html",
                    key=f"risiti_html_{i}_{m['order_ref']}",
                )
            str_platform.write("---")


def _hakiki_malipo_yaliyorudi():
    """Mteja amerudi kutoka Pesapal: hakiki, kisha SAFISHA URL ili isirudie."""
    v = str_platform.query_params
    tid = v.get("OrderTrackingId") or v.get("pesapal_tracking_id")
    if not tid:
        return
    tid = str(tid).strip()
    try:
        hali = pesapal_core.angalia_hali_ya_malipo(tid)
    except Exception:
        hali = {"status_desc": "ERROR_Exception"}
    st_desc = hali["status_desc"]

    if st_desc == "PENDING" or st_desc.startswith("ERROR"):
        # Usisafishe URL: mteja abonyeze "Angalia tena" na tutahakiki tena.
        str_platform.info("\u23F3 Tunasubiri uthibitisho wa malipo yako (thibitisha PIN kwenye simu kama bado).")
        if str_platform.button("\U0001F504 Angalia tena hali ya malipo"):
            str_platform.rerun()
        return

    if st_desc == "COMPLETED":
        natija = database.pandisha_hadhi_ya_mteja_kiotomatiki(
            tid, "completed",
            merchant_reference=hali.get("reference", ""),
            kiasi=hali.get("amount", 0.0),
            sarafu=hali.get("currency", ""),
            confirmation_code=hali.get("confirmation_code", ""),
            payment_method=hali.get("payment_method", ""),
            tarehe_malipo=hali.get("created_date", ""),
        )
        if natija in ("applied", "already"):
            jina = database.pata_mteja_wa_oda(hali.get("reference", ""))
            if jina:
                str_platform.session_state["jina_la_kulipa"] = jina
            ujumbe = ("success", "\u2705 Malipo yamethibitishwa! Premium yako imewashwa. Ingia hapa chini (username yako imeandaliwa) kuendelea kwenye Dashboard yako na kupakua risiti yako.")
        elif natija == "mismatch":
            ujumbe = ("error", f"\u274C Kiasi au sarafu havilingani na oda. Wasiliana na msaada na namba hii: {tid}")
        elif natija == "unknown_order":
            ujumbe = ("error", f"\u274C Malipo hayakupatikana kwenye mfumo wetu. Wasiliana na msaada na namba hii: {tid}")
        else:
            ujumbe = ("warning", "\u26A0\uFE0F Malipo yamekamilika lakini akaunti haikusasishwa sasa hivi. Pakia upya ukurasa au wasiliana na msaada.")
    else:
        ujumbe = ("error", f"\u274C Malipo hayakukamilika (hali: {st_desc}). Unaweza kujaribu tena.")

    str_platform.session_state["pesapal_msg"] = ujumbe
    str_platform.query_params.clear()  # huzuia kuhakiki tena kila rerun


_hakiki_malipo_yaliyorudi()

# Onyesha ujumbe wa malipo mpaka mteja aingie (login huifuta session)
_pm = str_platform.session_state.get("pesapal_msg")
if _pm:
    getattr(str_platform, _pm[0])(_pm[1])

# Do not overwrite an existing authenticated session on every rerun.
if "active_gateway" not in str_platform.session_state:
    str_platform.session_state["active_gateway"] = "client_auth_s"

gate = str_platform.session_state["active_gateway"]


def _kamilisha_login(username):
    """Mteja amepita hatua zote: mpeleke Premium Hub."""
    auth_2fa.futa_makosa(username)
    str_platform.session_state.clear()
    str_platform.session_state["member_username"] = username
    str_platform.session_state["active_gateway"] = "premium_member_suite"
    str_platform.rerun()


# ------------------------------------------------------------------ #
#  HATUA 1: Sign Up / Sign In (username + password)
# ------------------------------------------------------------------ #
if gate == "client_auth_s":
    t1, t2 = str_platform.tabs(["\U0001F4DD MTUMIAJI MPYA (Sign Up)", "\U0001F511 PREMIUM SIGN IN"])
    with t1:
        un = str_platform.text_input("Username Mpya:")
        pw = str_platform.text_input("Password Mpya:", type="password")
        if str_platform.button("Thibitisha Usajili") and un.strip() and pw.strip():
            kosa_la_usajili = database.thibitisha_data_ya_usajili(un, pw)
            if kosa_la_usajili:
                str_platform.error(kosa_la_usajili)
            elif database.sajili_mtumiaji_mpya(un.strip(), pw.strip(), "premium user"):
                str_platform.success("Usajili umekubaliwa! Proceed to Sign In. Utaombwa kuwasha Authenticator mara ya kwanza utakapoingia.")
            else:
                str_platform.error("Usajili umeshindikana (huenda username tayari ipo).")
    with t2:
        un_o = str_platform.text_input("Ingiza Username:", value=str_platform.session_state.get("jina_la_kulipa", ""))
        pw_o = str_platform.text_input("Ingiza Password:", type="password")
        if str_platform.button("Ingia Mfumo") and un_o.strip() and pw_o.strip():
            if auth_2fa.login_imefungwa(un_o):
                str_platform.error("Majaribio mengi yameshindikana. Subiri dakika 15 kisha jaribu tena.")
            elif database.thibitisha_utambulisho_wa_siri(un_o.strip(), pw_o.strip(), "premium user"):
                str_platform.session_state["pending_user"] = un_o.strip()
                if auth_2fa.has_totp(un_o.strip()):
                    str_platform.session_state["active_gateway"] = "totp_step"
                else:
                    str_platform.session_state["active_gateway"] = "totp_enroll"
                str_platform.rerun()
            else:
                auth_2fa.rekodi_kosa(un_o)
                str_platform.error("Username au password si sahihi.")

# ------------------------------------------------------------------ #
#  HATUA 2a: Mara ya kwanza - washa Authenticator (QR + thibitisha msimbo)
# ------------------------------------------------------------------ #
elif gate == "totp_enroll":
    u_pend = str_platform.session_state.get("pending_user")
    if not u_pend:
        str_platform.session_state.clear()
        str_platform.rerun()

    if "enroll_secret" not in str_platform.session_state:
        str_platform.session_state["enroll_secret"] = auth_2fa.generate_secret()
    secret = str_platform.session_state["enroll_secret"]

    str_platform.markdown("### \U0001F4F1 Washa Uthibitisho wa Hatua Mbili")
    str_platform.write(
        "1. Weka **Google Authenticator** (au Microsoft Authenticator / Authy) kwenye simu yako.\n"
        "2. Bonyeza **+** kisha **Scan a QR code**, au chagua **Enter a setup key** na ubandike ufunguo ulio chini.\n"
        "3. Ingiza msimbo wa tarakimu 6 unaoonekana kwenye app ili kuthibitisha."
    )
    uri = auth_2fa.provisioning_uri(u_pend, secret)
    png = auth_2fa.qr_png(uri)
    c_qr, c_key = str_platform.columns([1, 2])
    with c_qr:
        if png:
            str_platform.image(png, width=220)
    with c_key:
        str_platform.caption("Setup key (kama huwezi kuscan QR):")
        str_platform.code(secret, language=None)
        str_platform.caption(f"Akaunti: {u_pend} \u2022 Aina: Time-based \u2022 Tarakimu: 6")

    msimbo = str_platform.text_input("Msimbo wa tarakimu 6:", max_chars=7, key="enroll_code")
    ca, cb = str_platform.columns(2)
    with ca:
        if str_platform.button("Thibitisha na Washa", type="primary", use_container_width=True):
            if auth_2fa.login_imefungwa(u_pend):
                str_platform.error("Majaribio mengi yameshindikana. Subiri dakika 15 kisha jaribu tena.")
            else:
                counter = auth_2fa.verify_totp(secret, msimbo, 0)
                if counter:
                    codes = auth_2fa.new_recovery_codes()
                    auth_2fa.save_totp(u_pend, secret, codes, counter)
                    str_platform.session_state["recovery_codes"] = codes
                    str_platform.session_state.pop("enroll_secret", None)
                    str_platform.session_state["active_gateway"] = "totp_recovery"
                    str_platform.rerun()
                else:
                    auth_2fa.rekodi_kosa(u_pend)
                    str_platform.error("Msimbo si sahihi. Hakikisha saa ya simu yako ni sahihi, kisha jaribu msimbo mpya.")
    with cb:
        if str_platform.button("Rudi nyuma", use_container_width=True):
            str_platform.session_state.clear()
            str_platform.rerun()

# ------------------------------------------------------------------ #
#  HATUA 2b: Onyesha recovery codes mara moja tu
# ------------------------------------------------------------------ #
elif gate == "totp_recovery":
    u_pend = str_platform.session_state.get("pending_user")
    codes = str_platform.session_state.get("recovery_codes")
    if not u_pend or not codes:
        str_platform.session_state.clear()
        str_platform.rerun()

    str_platform.success("\u2705 Authenticator imewashwa!")
    str_platform.markdown("### \U0001F9FE Recovery Codes")
    str_platform.warning(
        "Hifadhi msimbo hizi mahali salama (mf. picha ya skrini au daftari). "
        "Zinaonyeshwa mara hii tu. Ukipoteza simu, kila moja inaweza kutumika mara moja kuingia."
    )
    str_platform.code("\n".join(codes), language=None)
    if str_platform.button("Nimehifadhi, endelea", type="primary"):
        _kamilisha_login(u_pend)

# ------------------------------------------------------------------ #
#  HATUA 2c: Ingiza msimbo wa Authenticator (kila login)
# ------------------------------------------------------------------ #
elif gate == "totp_step":
    u_pend = str_platform.session_state.get("pending_user")
    if not u_pend:
        str_platform.session_state.clear()
        str_platform.rerun()

    str_platform.markdown("### \U0001F4F1 Thibitisha kwa Authenticator")
    str_platform.info("Fungua app ya Authenticator kwenye simu yako na uingize msimbo wa tarakimu 6 wa akaunti ya Ourworthlinks.")
    msimbo = str_platform.text_input("Msimbo wa tarakimu 6:", max_chars=7, key="totp_code")

    ca, cb = str_platform.columns(2)
    with ca:
        if str_platform.button("Thibitisha", type="primary", use_container_width=True):
            if auth_2fa.login_imefungwa(u_pend):
                str_platform.error("Majaribio mengi yameshindikana. Subiri dakika 15 kisha jaribu tena.")
            else:
                secret, last_counter = auth_2fa.get_totp(u_pend)
                if not secret:
                    # Hifadhi ilifutwa (mf. app iliwashwa upya): mteja ajisajili upya Authenticator.
                    str_platform.session_state["active_gateway"] = "totp_enroll"
                    str_platform.rerun()
                counter = auth_2fa.verify_totp(secret, msimbo, last_counter)
                if counter:
                    auth_2fa.update_counter(u_pend, counter)
                    _kamilisha_login(u_pend)
                else:
                    auth_2fa.rekodi_kosa(u_pend)
                    str_platform.error("Msimbo si sahihi au umeshatumika. Subiri msimbo unaofuata kisha jaribu tena.")
    with cb:
        if str_platform.button("Rudi nyuma", use_container_width=True):
            str_platform.session_state.clear()
            str_platform.rerun()

    with str_platform.expander("Nimepoteza simu yangu (tumia recovery code)"):
        rc = str_platform.text_input("Recovery code (mf. a1b2c-d3e4f):", key="recovery_input")
        if str_platform.button("Tumia Recovery Code"):
            if auth_2fa.login_imefungwa(u_pend):
                str_platform.error("Majaribio mengi yameshindikana. Subiri dakika 15 kisha jaribu tena.")
            elif auth_2fa.use_recovery_code(u_pend, rc):
                _kamilisha_login(u_pend)
            else:
                auth_2fa.rekodi_kosa(u_pend)
                str_platform.error("Recovery code si sahihi au imeshatumika.")

# ------------------------------------------------------------------ #
#  HATUA 3: Premium Hub
# ------------------------------------------------------------------ #
elif gate == "premium_member_suite":
    u_active = str_platform.session_state["member_username"]
    str_platform.markdown(f"### Welcome to the Ourworthlinks Global Marketplace, {u_active.upper()}!")
    _onyesha_historia_ya_malipo(u_active)

    premium_hadi = database.premium_hadi_lini(u_active)
    if premium_hadi:
        str_platform.success(f"\u2705 Premium yako inatumika hadi {premium_hadi.strftime('%d/%m/%Y')}.")

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

    # Pesapal inahitaji email au namba ya simu ya mteja. Tunaomba namba ya Mobile Money
    # wakati wa kulipa (si wakati wa kusajili), na tunaitumia kwenye oda.
    simu_input = str_platform.text_input(
        "Namba ya simu ya malipo (mf. 0712 345 678):", key="simu_malipo"
    )
    email_input = str_platform.text_input(
        "Barua pepe (hiari, kwa ajili ya risiti kutoka Pesapal):", key="email_malipo"
    ).strip()
    stripe_redirect = pesapal_core.generate_stripe_global_checkout(u_active, dynamic_cost=49.00)

    cp1, cp2 = str_platform.columns(2)
    with cp1:
        str_platform.markdown(
            f"<div style='border:1px solid #3B82F6; padding:20px; border-radius:12px;'>"
            f"<h3>\U0001F48E LINGUAAFRIKA PREMIUM SUITE</h3><h1>{s_symbol} {amt:,.2f}</h1></div>",
            unsafe_allow_html=True,
        )
        # Create Pesapal order only after the customer clicks the payment button,
        # rather than creating a new order on every Streamlit rerun.
        if str_platform.button("💳 Subscribe via Local Mobile Money", type="primary", use_container_width=True):
            simu_safi = auth_2fa.safisha_simu_malipo(simu_input)
            if not simu_safi:
                str_platform.error("Weka namba sahihi ya simu kwanza (mf. 0712345678).")
            elif email_input and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email_input):
                str_platform.error("Barua pepe si sahihi. Iandike vizuri au iache wazi.")
            else:
                pesapal_redirect = pesapal_core.anzisha_muamala_wa_pesapal(
                    u_active, email_input, kiasi_usd=kiasi_cha_msingi_usd, sarafu=s_symbol, simu=simu_safi
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
