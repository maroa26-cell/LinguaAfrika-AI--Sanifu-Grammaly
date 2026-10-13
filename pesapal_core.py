import streamlit as str_platform
import requests
import json
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi=5.00):
    """程式 LIVE PRODUCTION TERMINAL: Locked directly to ://pesapal.com and ://pesapal.com"""
    if hasattr(str_platform, "secrets"):
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        return "https://://pesapal.com/iframe/PesapalIframe3/Index"

    if not consumer_key or not consumer_secret:
        return "https://://pesapal.com/iframe/PesapalIframe3/Index"

    auth_url = "https://://pesapal.com/api/Auth/RegisterToken"
    order_url = "https://://pesapal.com/api/Transactions/SubmitOrderRequest"
    id_ya_muamala = f"owl-{int(time.time())}-{username.lower()}"
    
    # 👑 PATH SYNC: Imejazwa URL mpya kabisa rasmi ya bqd8esgjivmepvphzdztwc kulinda mnyororo!
    url_yako_halisi = "https://streamlit.app"

    try:
        auth_response = requests.post(auth_url, headers={"content-type": "application/json", "accept": "application/json"}, json={"consumer_key": consumer_key, "consumer_secret": consumer_secret}, timeout=10.0)
        if auth_response.status_code == 200:
            access_token = auth_response.json().get("token")
            order_payload = {
                "id": id_ya_muamala,
                "amount": kiasi,
                "description": "linguaafrika premium utility tier license",
                "callback_url": url_yako_halisi,
                "cancellation_url": url_yako_halisi,
                "notification_id": "ffa26ad8-4037-4b7a-a122-d9cbf46dc415", # Weka IPN ID yako mpya hapa
                "billing_address": {
                    "email_address": email,
                    "country_code": "tz",
                    "first_name": username,
                    "last_name": "client"
                }
            }
            order_response = requests.post(order_url, headers={"content-type": "application/json", "accept": "application/json", "authorization": f"Bearer {access_token}"}, json=order_payload, timeout=10.0)
            if order_response.status_code == 200:
                return order_response.json().get("redirect_url")
        return f"https://://pesapal.com/iframe/PesapalIframe3/Index?OrderTrackingId={id_ya_muamala}&return_url={url_yako_halisi}"
    except Exception:
        return f"https://://pesapal.com/iframe/PesapalIframe3/Index?OrderTrackingId={id_ya_muamala}"

def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """🌐 GLOBAL CREDIT CARD PIPELINE: Secure checkout link intents for international buyers"""
    base_stripe_vault_link = "https://stripe.com"
    query_parameters = f"?package={client_package}&user={username.lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query_parameters}"
