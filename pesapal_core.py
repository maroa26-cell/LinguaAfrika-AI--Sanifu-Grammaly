import streamlit as str_platform
import requests
import json
import time

def anzisha_muamala_wa_pesapal(username, email, kiasi_usd=5.00, sarafu="TZS"):
    """👑 LIVE PRODUCTION GATEWAY: High-security pipeline for Ourworthlinks BUSINESS"""
    
    domain_kamili = "https://streamlit.app"
    auth_url = "https://pesapal.com"
    order_url = "https://pesapal.com"
    id_ya_muamala = f"owl-{int(time.time())}-{username.lower()}"

    if hasattr(str_platform, "secrets"):
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        consumer_key = ""
        consumer_secret = ""

    sarafu_halisi = str(sarafu).upper().strip()
    if sarafu_halisi == "TZS":
        kiasi_cha_malipo = float(kiasi_usd * 2600.00)
    elif sarafu_halisi == "KES":
        kiasi_cha_malipo = float(kiasi_usd * 130.00)
    else:
        sarafu_halisi = "USD"
        kiasi_cha_malipo = float(kiasi_usd)

    kiasi_kilichozungushwa = round(kiasi_cha_malipo, 2)

    # 🛡️ FIX YA MOJA KWA MOJA: Kama funguo hazipo, inarudisha link kamili ya dharura kuzuia about:blank
    if not consumer_key or not consumer_secret:
        return f"{domain_kamili}?error=Missing_Secrets"

    try:
        headers_auth = {
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        payload_auth = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
        
        auth_response = requests.post(auth_url, headers=headers_auth, json=payload_auth, timeout=15.0)
        
        if auth_response.status_code == 200:
            try:
                access_token = auth_response.json().get("token")
            except Exception:
                return f"{domain_kamili}?error=Auth_JSON_Fail"
                
            nchi = "TZ" if sarafu_halisi == "TZS" else ("KE" if sarafu_halisi == "KES" else "US")
            
            order_payload = {
                "id": id_ya_muamala,
                "currency": sarafu_halisi,  
                "amount": kiasi_kilichozungushwa,  
                "description": f"Ourworthlinks BUSINESS premium suite access authorization (base: ${kiasi_usd} usd)",
                "callback_url": domain_kamili,
                "cancellation_url": domain_kamili,
                "notification_id": "329329ce-4caf-438d-b30b-d9ca91cf68a6",
                "billing_address": {
                    "email_address": email,
                    "phone_number": "0712345678",
                    "country_code": nchi,
                    "first_name": username if len(username) >= 2 else "Mteja",
                    "last_name": "Business"
                }
            }
            
            headers_order = {
                "Content-Type": "application/json", 
                "Accept": "application/json", 
                "Authorization": f"Bearer {access_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            order_response = requests.post(order_url, json=order_payload, headers=headers_order, timeout=15.0)
            
            if order_response.status_code == 200:
                return order_response.json().get("redirect_url")
            else:
                return f"{domain_kamili}?error=Order_Failed_{order_response.status_code}"
        else:
            return f"{domain_kamili}?error=Auth_Failed_{auth_response.status_code}"

    except Exception as e:
        return f"{domain_kamili}?error=System_Exception"

def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    base_stripe_vault_link = "https://stripe.com"
    query_parameters = f"?package={client_package}&user={username.lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query_parameters}"
