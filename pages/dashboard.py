import streamlit as str_platform
import sqlite3
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path: 
    sys.path.append(root_path)

import database
import pesapal_core
import skin_appearance

str_platform.set_page_config(page_title="Ourworthlinks Business Dashboard", layout="wide")
skin_appearance.inject_premium_glassmorphic_skin()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900;'>🔐 OURWORTHLINKS BUSINESS MANAGEMENT ENGINE</h1>", unsafe_allow_html=True)
str_platform.write("---")

try:
    v = str_platform.query_params
    tid = v.get("OrderTrackingId") or v.get("pesapal_tracking_id")
    if tid:
        if database.pandisha_hadhi_ya_mteja_kiotomatiki(tid.strip(), v.get("status", "completed")):
            str_platform.success(" Handshake ya Webhook imekamilika kikamilifu!")
except Exception: 
    pass

if "active_gateway" not in str_platform.session_state: 
    str_platform.session_state["active_gateway"] = "mlangoni"
gate = str_platform.session_state["active_gateway"]

if gate == "mlangoni":
    str_platform.info("👋 Karibu Kiongozi! Tafadhali chagua lango unalotaka kufungua:")
    c1, c2 = str_platform.columns(2)
    with c1: 
        if str_platform.button(" Lango la Admin (Utawala)"): 
            str_platform.session_state["active_gateway"] = "admin_s"
            str_platform.rerun()
    with c2: 
        if str_platform.button(" Lango la Mteja (Sign In / Sign Up)"): 
            str_platform.session_state["active_gateway"] = "client_auth_s"
            str_platform.rerun()

elif gate == "admin_s":
    if str_platform.button("← Rudi Mlangoni"): 
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
    u = str_platform.text_input("Admin Username:")
    p = str_platform.text_input("Admin Password:", type="password")
    if str_platform.button("Ingia Utawala") and database.thibitisha_utambulisho_wa_siri(u, p, "admin"):
        str_platform.success("🔓 Karibu Kiongozi!")

elif gate == "client_auth_s":
    if str_platform.button("← Rudi Mlangoni"): 
        str_platform.session_state["active_gateway"] = "mlangoni"
        str_platform.rerun()
    t1, t2 = str_platform.tabs(["📝 SIGN UP", "🔑 SIGN IN"])
    with t1:
        un = str_platform.text_input("Username Mpya:")
        pw = str_platform.text_input("Password Mpya:", type="password")
        if str_platform.button("Thibitisha Usajili") and un.strip() and pw.strip():
            if database.sajili_mtumiaji_mpya(un.strip(), pw.strip(), "premium user"): 
                str_platform.success("Usajili umekubaliwa!")
    with t2:
        un_o = str_platform.text_input("Ingiza Username:")
        pw_o = str_platform.text_input("Ingiza Password:", type="password")
        if str_platform.button("Ingia Mfumo") and database.thibitisha_utambulisho_wa_siri(un_o.strip(), pw_o.strip(), "premium user"):
            str_platform.session_state["active_gateway"] = "premium_member_suite"
            str_platform.session_state["member_username"] = un_o.strip()
            str_platform.rerun()

elif gate == "premium_member_suite":
    u_active = str_platform.session_state["member_username"]
    str_platform.markdown(f"### Welcome to the Ourworthlinks Global Marketplace, {u_active.upper()}!")
    
    curr = str_platform.selectbox("Chagua Sarafu:", ["USD (Base)", "TZS (Converted)", "KES (Converted)"])
    amt = kiasi_cha_msingi_usd = 5.00
    if "TZS" in curr:
        amt = kiasi_cha_msingi_usd * 2600.00
    elif "KES" in curr:
        amt = kiasi_cha_msingi_usd * 130.00
        
    s_symbol = "TZS" if "TZS" in curr else ("KES" if "KES" in curr else "USD")
    str_platform.info(f"Kiwango cha Kulipa: **{amt:,.2f} {s_symbol}**")
    
    pesapal_redirect = pesapal_core.anzisha_muamala_wa_pesapal(u_active, f"{u_active}@ourworthlinks.com", kiasi_usd=5.00, sarafu=s_symbol)
    stripe_redirect = f"https://stripe.com{u_active.lower()}&amount=49.00&currency=usd"

    cp1, cp2 = str_platform.columns(2)
    with cp1:
        str_platform.markdown(f"<div style='border:1px solid #3B82F6; padding:20px; border-radius:12px;'><h3>💎 LINGUAAFRIKA PREMIUM SUITE</h3><h1>{s_symbol} {amt:,.2f}</h1></div>", unsafe_allow_html=True)
        if "error" in str(pesapal_redirect) or str(pesapal_redirect).strip() == "#":
            str_platform.warning("⚠️ Lango la Pesapal Live liko kwenye maboresho. Tafadhali tumia Stripe kulipa.")
            str_platform.code(str(pesapal_redirect))
        else:
            str_platform.markdown(f'<a href="{str(pesapal_redirect).strip()}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#3B82F6; color:white; padding:12px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; margin-top:10px;">💳 Subscribe via Local Mobile Money</button></a>', unsafe_allow_html=True)
    with cp2:
        str_platform.markdown("<div style='border:1px solid #D97706; padding:20px; border-radius:12px;'><h3>🛡️ SOVEREIGN CODE AUDITOR</h3><h1>USD $49.00</h1></div>", unsafe_allow_html=True)
        str_platform.link_button("Purchase Commercial B2B License", stripe_redirect, type="secondary", use_container_width=True)
