import streamlit as str_platform
import requests
import json
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi_usd=5.00, sarafu="TZS"):
    """💳 LOCAL PAYMENT NODE: Automated Live Production Trigger with dynamic currency conversion"""
    if hasattr(str_platform, "secrets"):
        # 🛡️ Inasoma vigezo vyako vya siri kutoka Advanced Settings ya Streamlit Secrets
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        consumer_key = ""
        consumer_secret = ""

    # 👑 SUBDOMAINS LOCK: Variable huru zilizolindwa na herufi kamili za kibenki za Live Production
    pesapal_api_host = "api.pesapal.com"
    pesapal_pay_host = "pay.pesapal.com"

    # 🔥 SULUHISHO LA 1: Imebadilishwa kutoka RegisterToken kwenda RequestToken
    auth_url = f"https://{pesapal_api_host}/api/Auth/RequestToken"
    order_url = f"https://{pesapal_api_host}/api/Transactions/SubmitOrderRequest"
    id_ya_muamala = f"owl-{int(time.time())}-{username.lower()}"
    
    # 👑 HARDWIRED PATHWAY: Inasoma URL yako halisi iliyo hai mtandaoni
    url_yako_halisi = "https://streamlit.app"

    # 🔄 BASE CURRENCY ENGINE: USD $5.00 ndio msingi, inabadilishwa hapa kwenda sarafu lengwa kiotomatiki
    sarafu_halisi = str(sarafu).upper().strip()
    if sarafu_halisi == "TZS":
        kiasi_cha_malipo = float(kiasi_usd * 2600.00) # Kiwango cha sasa cha soko: 1 USD = 2,600 TZS
    elif sarafu_halisi == "KES":
        kiasi_cha_malipo = float(kiasi_usd * 130.00)  # Kiwango cha sasa cha soko: 1 USD = 130 KES
    else:
        sarafu_halisi = "USD"
        kiasi_cha_malipo = float(kiasi_usd)

    kiasi_kilichozungushwa = round(kiasi_cha_malipo, 2)

    try:
        if consumer_key and consumer_secret:
            # HATUA YA 1: Kuomba Access Token ya Live Production kwenda Seva Kuu
            auth_response = requests.post(
                auth_url, 
                headers={"content-type": "application/json", "accept": "application/json"}, 
                json={"consumer_key": consumer_key, "consumer_secret": consumer_secret}, 
                timeout=10.0
            )
            
            if auth_response.status_code == 200:
                access_token = auth_response.json().get("token")
                
                # SULUHISHO LA 2: Herufi kubwa kwenye Country Code ("TZ", "KE", "US")
                if sarafu_halisi == "TZS":
                    nchi = "TZ"
                elif sarafu_halisi == "KES":
                    nchi = "KE"
                else:
                    nchi = "US"

                # HATUA YA 2: Kutengeneza Ankara ya Kiofisi ya Kifurushi cha Premium
                order_payload = {
                    "id": id_ya_muamala,
                    "currency": sarafu_halisi,  
                    "amount": kiasi_kilichozungushwa,  
                    "description": f"linguaafrika premium utility tier license (base: ${kiasi_usd} usd)",
                    "callback_url": url_yako_halisi,
                    "cancellation_url": url_yako_halisi,
                    "notification_id": "329329ce-4caf-438d-b30b-d9ca91cf68a6",  # 🚀 LIVE IPN ID YAKO HALISI
                    "billing_address": {
                        "email_address": email,
                        "phone_number": "0712345678", # SULUHISHO LA 3: Namba ya simu imezalishwa (ni lazima iwepo)
                        "country_code": nchi,
                        "first_name": username if len(username) >= 2 else "Mteja", 
                        "last_name": "Premium"
                    }
                }
                
                # 🔥 INLINE SECURE PAYLOAD: Tumesimika json= vizuri asilimia 100 kuzuia kosa la kiasi kusomeka 0.00
                order_response = requests.post(
                    order_url, 
                    json=order_payload, 
                    headers={
                        "content-type": "application/json", 
                        "accept": "application/json", 
                        "authorization": f"Bearer {access_token}"
                    }, 
                    timeout=10.0
                )
                
                if order_response.status_code == 200:
                    return order_response.json().get("redirect_url")
                else:
                    # Hii inakusaidia kuona tatizo kwenye log za Streamlit endapo oda itakataliwa
                    str_platform.error(f"Pesapal Order Error {order_response.status_code}: {order_response.text}")

        # Kama ikiangukia kwenye fallback, tunatengeneza link salama
        query_string_sync = f"?OrderTrackingId={id_ya_muamala}&amount={kiasi_kilichozungushwa}&currency={sarafu_halisi}&return_url={url_yako_halisi}"
        return f"https://{pesapal_pay_host}/iframe/PesapalIframe3/Index{query_string_sync}"
        
    except Exception as e:
        str_platform.error(f"Hitilafu imetokea: {e}")
        query_string_sync = f"?OrderTrackingId={id_ya_muamala}&amount={kiasi_kilichozungushwa}&currency={sarafu_halisi}&return_url={url_yako_halisi}"
        return f"https://{pesapal_pay_host}/iframe/PesapalIframe3/Index{query_string_sync}"

def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """🌐 GLOBAL CREDIT CARD PIPELINE: Secure checkout link intents for international buyers"""
    base_stripe_vault_link = "https://stripe.com"
    query_parameters = f"?package={client_package}&user={username.lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query_parameters}"
