
import streamlit as str_platform
import requests
import time
import uuid

# ====================================================================== #
#  PESAPAL API 3.0 - ENDPOINTS HALISI (zilikuwa za uongo awali)
# ====================================================================== #
#  Live:    https://pay.pesapal.com/v3
#  Sandbox: https://cybqa.pesapal.com/pesapalv3
PESAPAL_BASE = "https://pay.pesapal.com/v3"
AUTH_URL = f"{PESAPAL_BASE}/api/Auth/RequestToken"
ORDER_URL = f"{PESAPAL_BASE}/api/Transactions/SubmitOrderRequest"
STATUS_URL = f"{PESAPAL_BASE}/api/Transactions/GetTransactionStatus"

#  URL HALISI ya app yako (ilikuwa 'https://streamlit.app' - si sahihi)
APP_URL = str_platform.secrets.get("APP_URL", "https://linguaafrika-ai--sanifu-grammaly-9jv3o9ocfcjmjtzbqkvwfw.streamlit.app").rstrip("/")
#  IPN id yako kutoka Pesapal
IPN_ID = "329329ce-4caf-438d-b30b-d9ca91cf68a6"


def _pata_funguo():
    """Soma Consumer Key/Secret kutoka Streamlit Secrets."""
    if hasattr(str_platform, "secrets"):
        consumer_key = str_platform.secrets.get("PESAPAL_CONSUMER_KEY", "").strip()
        consumer_secret = str_platform.secrets.get("PESAPAL_CONSUMER_SECRET", "").strip()
    else:
        consumer_key = consumer_secret = ""
    return consumer_key, consumer_secret


def _pata_token():
    """Pata bearer token kutoka Pesapal. Hurejesha (token, error)."""
    consumer_key, consumer_secret = _pata_funguo()
    if not consumer_key or not consumer_secret:
        return None, "Missing_Secrets"

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
    try:
        resp = requests.post(AUTH_URL, headers=headers, json=payload, timeout=20.0)
    except Exception:
        return None, "System_Exception"

    if resp.status_code != 200:
        return None, f"Auth_Failed_{resp.status_code}"
    try:
        data = resp.json()
    except Exception:
        return None, "Auth_JSON_Fail"

    token = data.get("token")
    if not token:
        return None, "Auth_No_Token"
    return token, None


def anzisha_muamala_wa_pesapal(username, email, kiasi_usd=5.00, sarafu="TZS"):
    """\U0001F451 LIVE PRODUCTION GATEWAY: Hupeleka oda Pesapal na kurejesha redirect_url.

    IMEREKEBISHWA: endpoints halisi za Pesapal API 3.0 na URL halisi ya app.
    """
    id_ya_muamala = f"owl-{int(time.time())}-{uuid.uuid4().hex[:8]}-{str(username).lower()}"

    # Badilisha sarafu / kiasi
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
    order_payload = {
        "id": id_ya_muamala,
        "currency": sarafu_halisi,
        "amount": kiasi_kilichozungushwa,
        "description": f"Ourworthlinks BUSINESS premium suite (base ${kiasi_usd} usd)"[:100],
        "callback_url": f"{APP_URL}/dashboard",
        "cancellation_url": f"{APP_URL}/dashboard",
        "notification_id": IPN_ID,
        "billing_address": {
            "email_address": email,
            "phone_number": "0712345678",
            "country_code": nchi,
            "first_name": username if len(str(username)) >= 2 else "Mteja",
            "last_name": "Business",
        },
    }
    headers_order = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        resp = requests.post(ORDER_URL, json=order_payload, headers=headers_order, timeout=20.0)
    except Exception:
        return f"{APP_URL}?error=System_Exception"

    if resp.status_code != 200:
        return f"{APP_URL}?error=Order_Failed_{resp.status_code}"
    try:
        data = resp.json()
    except Exception:
        return f"{APP_URL}?error=Order_JSON_Fail"

    redirect_url = data.get("redirect_url")
    if not redirect_url:
        # Pesapal mara nyingine huweka hitilafu kwenye 'error'
        return f"{APP_URL}?error=Order_No_Redirect"
    return redirect_url


def angalia_hali_ya_malipo(order_tracking_id):
    """Hakiki hali HALISI ya malipo moja kwa moja na Pesapal.

    Hurejesha dict: {status_desc, amount, currency, reference, raw}.
    Hii ndiyo tunayotumia kabla ya kumpandisha mteja Premium - usiamini
    kigezo cha 'status' kutoka kwenye URL pekee.
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
    except Exception:
        tokeo["status_desc"] = "ERROR_System_Exception"
        return tokeo

    tokeo["status_desc"] = (data.get("payment_status_description") or "UNKNOWN").upper()
    tokeo["amount"] = float(data.get("amount", 0) or 0)
    tokeo["currency"] = data.get("currency", "")
    tokeo["reference"] = data.get("merchant_reference", "")
    tokeo["raw"] = data
    return tokeo


def generate_stripe_global_checkout(username, client_package="code_auditor_license", dynamic_cost=49.00):
    """\U0001F310 GLOBAL CREDIT CARD PIPELINE (placeholder).

    TAHADHARI: hii bado inatumia kiungo cha mfano cha Stripe. Ili ifanye kazi
    halisi, unahitaji kuunda Stripe Checkout Session upande wa seva. Kwa sasa
    inarejesha URL ya mfano tu.
    """
    base_stripe_vault_link = "https://stripe.com"
    query = f"?package={client_package}&user={str(username).lower()}&amount={dynamic_cost}&currency=usd"
    return f"{base_stripe_vault_link}{query}"

