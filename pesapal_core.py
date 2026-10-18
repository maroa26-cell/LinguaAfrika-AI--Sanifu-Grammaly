import re
import time
import uuid

import requests
import streamlit as st

# ====================================================================== #
#  PESAPAL API 3.0
# ====================================================================== #
#  Live:    https://pay.pesapal.com/v3
#  Sandbox: https://cybqa.pesapal.com/pesapalv3
#  Funguo (Consumer Key/Secret) lazima zilingane na mazingira (live au sandbox).
PESAPAL_BASE = "https://pay.pesapal.com/v3"
AUTH_URL = f"{PESAPAL_BASE}/api/Auth/RequestToken"
ORDER_URL = f"{PESAPAL_BASE}/api/Transactions/SubmitOrderRequest"
STATUS_URL = f"{PESAPAL_BASE}/api/Transactions/GetTransactionStatus"


def _secret(key, default=""):
    """Soma Streamlit secret bila kuvunjika kama secrets hazipo."""
    try:
        return str(st.secrets.get(key, default)).strip()
    except Exception:
        return default


# URL ya app yako (inaweza kuwekwa pia kwenye Secrets kama APP_URL)
APP_URL = _secret(
    "APP_URL",
    "https://linguaafrika-ai--sanifu-grammaly-mftitfb5knlg6sgnbsrfdc.streamlit.app",
).rstrip("/")

# IPN id kutoka Pesapal (inaweza kuwekwa kwenye Secrets kama PESAPAL_IPN_ID)
IPN_ID = _secret("PESAPAL_IPN_ID", "329329ce-4caf-438d-b30b-d9ca91cf68a6")


def _pata_funguo():
    """Soma Consumer Key/Secret kutoka Streamlit Secrets."""
    return _secret("PESAPAL_CONSUMER_KEY"), _secret("PESAPAL_CONSUMER_SECRET")


def _pata_token():
    """Pata bearer token kutoka Pesapal. Hurejesha (token, error)."""
    consumer_key, consumer_secret = _pata_funguo()
    if not consumer_key or not consumer_secret:
        return None, "Missing_Secrets"

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
    try:
        resp = requests.post(AUTH_URL, headers=headers, json=payload, timeout=20.0)
    except Exception as e:
        print(f"[pesapal] auth exception: {e}")
        return None, "System_Exception"

    if resp.status_code != 200:
        print(f"[pesapal] auth failed {resp.status_code}: {resp.text[:300]}")
        return None, f"Auth_Failed_{resp.status_code}"
    try:
        data = resp.json()
    except Exception:
        return None, "Auth_JSON_Fail"

    token = data.get("token")
    if not token:
        print(f"[pesapal] auth no token: {str(data)[:300]}")
        return None, "Auth_No_Token"
    return token, None


def anzisha_muamala_wa_pesapal(username, email, kiasi_usd=5.00, sarafu="TZS", simu=None):
    """Hupeleka oda Pesapal na kurejesha redirect_url.

    Kama kuna hitilafu, hurejesha APP_URL?error=... (ili UI iweze kuionyesha).
    """
    # Pesapal: 'id' ni max herufi 50, hivyo tunaikata na kusafisha username.
    jina_safi = re.sub(r"[^a-z0-9]", "", str(username).lower())[:15] or "user"
    id_ya_muamala = f"owl-{int(time.time())}-{uuid.uuid4().hex[:8]}-{jina_safi}"[:50]

    # Badilisha sarafu / kiasi (viwango ni vya kukadiria; badilisha ukihitaji)
    sarafu_halisi = str(sarafu).upper().strip()
    if sarafu_halisi == "TZS":
        kiasi_cha_malipo = float(kiasi_usd) * 2600.00
    elif sarafu_halisi == "KES":
        kiasi_cha_malipo = float(kiasi_usd) * 130.00
    else:
        sarafu_halisi = "USD"
        kiasi_cha_malipo = float(kiasi_usd)
    kiasi_kilichozungushwa = round(kiasi_cha_malipo, 2)

    # 1) Pata token
    access_token, err = _pata_token()
    if err:
        return f"{APP_URL}?error={err}"

    # 2) Peleka oda
    nchi = "TZ" if sarafu_halisi == "TZS" else ("KE" if sarafu_halisi == "KES" else "US")
    # Pesapal inahitaji angalau email AU namba ya simu.
    if not email and not simu:
        return f"{APP_URL}?error=Missing_Email_Or_Phone"
    billing = {
        "country_code": nchi,
        "first_name": str(username) if len(str(username)) >= 2 else "Mteja",
        "last_name": "Business",
    }
    if email:
        billing["email_address"] = email
    if simu:  # namba halisi ya mteja (mf. 2557XXXXXXXX)
        billing["phone_number"] = str(simu)

    order_payload = {
        "id": id_ya_muamala,
        "currency": sarafu_halisi,
        "amount": kiasi_kilichozungushwa,
        "description": f"Ourworthlinks BUSINESS premium suite (base ${kiasi_usd} usd)"[:100],
        "callback_url": f"{APP_URL}/dashboard",
        "cancellation_url": f"{APP_URL}/dashboard",
        "notification_id": IPN_ID,
        "billing_address": billing,
    }
    headers_order = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        resp = requests.post(ORDER_URL, json=order_payload, headers=headers_order, timeout=20.0)
    except Exception as e:
        print(f"[pesapal] order exception: {e}")
        return f"{APP_URL}?error=System_Exception"

    if resp.status_code != 200:
        print(f"[pesapal] order failed {resp.status_code}: {resp.text[:500]}")
        return f"{APP_URL}?error=Order_Failed_{resp.status_code}"
    try:
        data = resp.json()
    except Exception:
        return f"{APP_URL}?error=Order_JSON_Fail"

    redirect_url = data.get("redirect_url")
    if not redirect_url:
        # Pesapal mara nyingine huweka hitilafu kwenye 'error'
        print(f"[pesapal] no redirect_url: {str(data)[:500]}")
        return f"{APP_URL}?error=Order_No_Redirect"
    return redirect_url


def angalia_hali_ya_malipo(order_tracking_id):
    """Hakiki hali HALISI ya malipo moja kwa moja na Pesapal.

    Hurejesha dict: {status_desc, amount, currency, reference, raw}.
    Tumia hii kabla ya kumpandisha mteja Premium - usiamini kigezo cha
    'status' kutoka kwenye URL pekee.
    """
    tokeo = {"status_desc": "UNKNOWN", "amount": 0.0, "currency": "", "reference": "", "raw": None}
    if not order_tracking_id:
        return tokeo

    access_token, err = _pata_token()
    if err:
        tokeo["status_desc"] = f"ERROR_{err}"
        return tokeo

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        resp = requests.get(
            STATUS_URL,
            params={"orderTrackingId": order_tracking_id},
            headers=headers,
            timeout=20.0,
        )
        data = resp.json()
    except Exception as e:
        print(f"[pesapal] status exception: {e}")
        tokeo["status_desc"] = "ERROR_System_Exception"
        return tokeo

    tokeo["status_desc"] = (data.get("payment_status_description") or "UNKNOWN").upper()
    tokeo["amount"] = float(data.get("amount", 0) or 0)
    tokeo["currency"] = data.get("currency", "")
    tokeo["reference"] = data.get("merchant_reference", "")
    tokeo["raw"] = data
    return tokeo


def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """GLOBAL CREDIT CARD PIPELINE (placeholder).

    TAHADHARI: bado inarejesha kiungo cha mfano. Ili ifanye kazi halisi,
    tengeneza Stripe Checkout Session upande wa seva.
    """
    base_stripe_vault_link = "https://stripe.com"
    query = f"?package={client_package}&user={str(username).lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query}"
