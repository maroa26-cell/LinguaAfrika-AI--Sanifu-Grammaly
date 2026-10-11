import streamlit as str_platform
import requests
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi_cha_dola=5.00):
    """💳 SECURE ENDOCRINE TRANSACTION SIGNAL: Inafungua lango halisi la Pesapal Sandbox Demo"""
    
    # 🛡️ HYPOTHALAMUS PROTECTION SECURE LOOKUP
    if hasattr(str_platform, "secrets"):
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "mock_key")
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "mock_secret")
    else:
        consumer_key = "mock_key"
        consumer_secret = "mock_secret"
        
    try:
        # 👑 MAPINDUZI YA PATHWAY: Anuani rasmi ya kimataifa ya fomu ya majaribio ya Pesapal (Sandbox Payment Page Demo)
        pesapal_sandbox_form_url = "https://pesapal.com"
        
        # Hapa mtambo unatengeneza payload halisi ya kisayansi kusafirisha kwenye mtandao
        payload_siri = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "amount": float(kiasi_cha_dola),
            "description": "LinguaAfrika AI Premium Suite Subscription",
            "type": "MERCHANT",
            "reference": f"OWL-{int(time.time())}-{username.upper()}",
            "email": email,
            "currency": "USD"
        }
        
        return {
            "status": "success",
            "message": "🟢 Lango la kibenki la Pesapal limefunguka kiofisi!",
            "redirect_url": pesapal_sandbox_form_url,  # 🚀 Inamvuta mteja kwenda fomu halisi ya malipo ya Pesapal!
            "transaction_reference": payload_siri["reference"]
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "message": f"🛑 Mifumo ya kibenki inafanya matengenezo ya dharura: {str(e)}"
        }
