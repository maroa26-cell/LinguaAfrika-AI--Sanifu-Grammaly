import streamlit as str_platform
import requests
import json
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi_usd=5.00, sarafu="TZS"):
    """专 LIVE PRODUCTION PAYMENT NODE: Automated Live Production Trigger for exact web domain"""
    if hasattr(str_platform, "secrets"):
        # 🛡️ Inasoma vigezo vyako vya siri kutoka Advanced Settings ya Streamlit Secrets
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        consumer_key = ""
        consumer_secret = ""

    # 👑 SUBDOMAINS LOCK: Viunganishi rasmi vya Live Production v3
    auth_url = "https://pesapal.com"
    order_url = "https://pesapal.com"
    id_ya_muamala = f"owl-{int(time.time())}-{username.lower()}"
    
    # 🎯 SULUHISHO: Domain yako halisi na ndefu ya Streamlit mtandaoni
    url_yako_halisi = "https://streamlit.app"

    # 🔄 BASE CURRENCY ENGINE: Kubadili USD kwenda sarafu halisi ya malipo
    sarafu_halisi = str(sarafu).upper().strip()
    if sarafu_halisi == "TZS":
        kiasi_cha_malipo = float(kiasi_usd * 2600.00) # Kiwango cha soko: 1 USD = 2,600 TZS
    elif sarafu_halisi == "KES":
        kiasi_cha_malipo = float(kiasi_usd * 130.00)  # Kiwango cha soko: 1 USD = 130 KES
    else:
        sarafu_halisi = "USD"
        kiasi_cha_malipo = float(kiasi_usd)

    kiasi_kilichozungushwa = round(kiasi_cha_malipo, 2)

    try:
        if not consumer_key or not consumer_secret:
            return f"{url_yako_halisi}/dashboard?error=Missing_Secrets"

        # HATUA YA 1: Kuomba Access Token ya Live Production
        headers_auth = {"content-type": "application/json", "accept": "application/json"}
        payload_auth = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
        auth_response = requests.post(auth_url, headers=headers_auth, json=payload_auth, timeout=10.0)
        
        if auth_response.status_code == 200:
            access_token = auth_response.json().get("token")
            
            # ISO Country Code lazima ziwe herufi kubwa kamili (TZ, KE, US)
            nchi = "TZ" if sarafu_halisi == "TZS" else ("KE" if sarafu_halisi == "KES" else "US")

            # HATUA YA 2: Kuandaa Ankara ya Kiofisi kwenda Pesapal v3
            order_payload = {
                "id": id_ya_muamala,
                "currency": sarafu_halisi,  
                "amount": kiasi_kilichozungushwa,  
                "description": f"linguaafrika premium utility tier license (base: ${kiasi_usd} usd)",
                "callback_url": f"{url_yako_halisi}/dashboard",
                "cancellation_url": f"{url_yako_halisi}/dashboard",
                "notification_id": "329329ce-4caf-438d-b30b-d9ca91cf68a6",  # 🚀 IPN ID YAKO HALISI YA LIVE
                "billing_address": {
                    "email_address": email,
                    "phone_number": "0712345678", # Namba ya simu ya lazima ya mfano
                    "country_code": nchi,
                    "first_name": username if len(username) >= 2 else "Mteja",
                    "last_name": "Premium"
                }
            }
            
            # HATUA YA 3: Kutuma oda Live Pesapal
            headers_order = {
                "content-type": "application/json", 
                "accept": "application/json", 
                "authorization": f"Bearer {access_token}"
            }
            order_response = requests.post(order_url, json=order_payload, headers=headers_order, timeout=10.0)
            
            if order_response.status_code == 200:
                # Seva ikikubali, inarudisha redirect_url salama kuelekea fomu ya Pesapal Live
                return order_response.json().get("redirect_url")
            else:
                # Kama Pesapal wakikataa data, inarudisha link inayokulinda kuzuia kosa la Page Not Found
                return f"{url_yako_halisi}/dashboard?error=Pesapal_Order_Failed_{order_response.status_code}"
        else:
            # Kama siri za Streamlit Secrets zimekataliwa na Pesapal Live Auth
            return f"{url_yako_halisi}/dashboard?error=Auth_Failed_{auth_response.status_code}"

    except Exception as e:
        return f"{url_yako_halisi}/dashboard?error=System_Exception"

def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """🌐 GLOBAL CREDIT CARD PIPELINE: Secure checkout link intents for international buyers"""
    base_stripe_vault_link = "https://stripe.com"
    query_parameters = f"?package={client_package}&user={username.lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query_parameters}"
