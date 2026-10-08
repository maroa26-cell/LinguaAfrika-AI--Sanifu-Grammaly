import streamlit as str_platform
import requests
import json
import time

# 👑 VIWANGO VYA KIWANDA: MAZINGIRA HALISI YA UZALISHAJI FEDHA (PESAPAL LIVE PRODUCTION GATEWAY)
PESAPAL_BASE_URL = "https://pesapal.com"  # Live Production API URL

def pata_token_ya_siri_pesapal():
    """OAuth2: Inavuta Token ya kibenki ya masaa 5 kwa kutumia Credentials zako halisi za Pesapal"""
    url = f"{PESAPAL_BASE_URL}/api/Auth/RegisterConsumer"
    
    # 🔒 KUVUTA FUNGUO KUTOKA STREAMLIT SECRETS ILI KUZILINDA DHIDI YA WADUKUZI
    if hasattr(str_platform, "secrets") and "PESAPAL_CONSUMER_KEY" in str_platform.secrets:
        key = str_platform.secrets["PESAPAL_CONSUMER_KEY"]
        secret = str_platform.secrets["PESAPAL_CONSUMER_SECRET"]
    else:
        key = "missing_key"
        secret = "missing_secret"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "consumer_key": key,
        "consumer_secret": secret
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("token")
        return None
    except Exception:
        return None

def anzisha_muamala_wa_pesapal(username, email, kiasi_usd):
    """Inasajili oda mpya ya $5.00 USD Pesapal halisi na kurudisha Link ya Malipo ya Kadi na Simu"""
    token = pata_token_ya_siri_pesapal()
    if not token:
        return {"status": "error", "message": "🛑 Imefeli kuvuta Token ya Usalama Pesapal Live! Kagua kama Consumer Key na Secret zipo sawa kwenye Secrets."}
        
    url = f"{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "id": f"LA-{int(time.time())}",  # ID ya kipekee ya muamala mlangoni
        "amount": float(kiasi_usd),
        "currency": "USD",
        "description": "Ourworthlinks - LinguaAfrika AI Premium",
        "callback_url": "https://streamlit.app",  # Ukurasa wa kurudi mteja akilipa
        "notification_id": "00000000-0000-0000-0000-000000000000",
        "billing_address": {
            "email_address": email,
            "phone_number": "0712345678",
            "first_name": username,
            "last_name": "Customer",
            "country_code": "TZ"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "redirect_url": data.get("redirect_url"),
                "order_tracking_id": data.get("order_tracking_id")
            }
        return {"status": "error", "message": f"🛑 Pesapal Live ilikataa kuunda oda. Code: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"🛑 Hitilafu ya mtandao wa malipo Live: {str(e)}"}
