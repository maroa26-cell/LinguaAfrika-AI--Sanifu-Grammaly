import streamlit as str_platform
import requests
import json
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi=5.00):
    """💳 LOCAL PAYMENT NODE: Programmatic V3 trigger mapping strictly locked to live production hubs"""
    if hasattr(str_platform, "secrets"):
        # 🛡️ Inasoma vigezo vyako vya HERUFI KUBWA kutoka Advanced Settings ya Streamlit Secrets
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        return "https://pesapal.com"

    if not consumer_key or not consumer_secret:
        return "https://pesapal.com"

    # 👑 SUBDOMAINS LOCK: Variable huru zilizolindwa zikiwa na herufi kamili za kibenki za uzalishaji halisi!
    pesapal_api_host = "://pesapal.com"
    pesapal_pay_host = "://pesapal.com"

    auth_url = f"https://{pesapal_api_host}/api/Auth/RegisterToken"
    order_url = f"https://{pesapal_api_host}/api/Transactions/SubmitOrderRequest"
    id_ya_muamala = f"owl-{int(time.time())}-{username.lower()}"
    
    # 👑 DOMAIN PATH SYNC: URL yako mpya kabisa halisi ya porp5rjrnbphsmkmyywmxw kutoka kwenye skrini!
    url_yako_halisi = "https://streamlit.app"

    try:
        # HATUA YA 1: Kuomba Access Token ya Live Production kwenda Seva Kuu
        auth_response = requests.post(auth_url, headers={"content-type": "application/json", "accept": "application/json"}, json={"consumer_key": consumer_key, "consumer_secret": consumer_secret}, timeout=10.0)
        
        if auth_response.status_code == 200:
            access_token = auth_response.json().get("token")
            
            # HATUA YA 2: Kutengeneza Ankara ya Kiofisi ya Kifurushi cha Premium ($5.00 USD)
            order_payload = {
                "id": id_ya_muamala,
                "amount": kiasi,
                "description": "linguaafrika premium utility tier license",
                "callback_url": url_yako_halisi,
                "cancellation_url": url_yako_halisi,
                "notification_id": "329329ce-4caf-438d-b30b-d9ca91cf68a6", # 🚀 IPN ID YAKO MPYA HALISI TULIYOISIMIKA!
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

        # 🚀 IMMUTABLE FALLBACK: Link safi na iliyonyooka kuelekea ://pesapal.com Live Merchant Terminal
        return f"https://{pesapal_pay_host}/iframe/PesapalIframe3/Index?OrderTrackingId={id_ya_muamala}&return_url={url_yako_halisi}"
    except Exception:
        return f"https://{pesapal_pay_host}/iframe/PesapalIframe3/Index?OrderTrackingId={id_ya_muamala}"

def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """🌐 GLOBAL CREDIT CARD PIPELINE: Secure checkout link intents for international buyers"""
    base_stripe_vault_link = "https://stripe.com"
    query_parameters = f"?package={client_package}&user={username.lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query_parameters}"

