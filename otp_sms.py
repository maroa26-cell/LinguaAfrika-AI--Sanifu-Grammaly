"""OTP kwa SMS kwa ajili ya login ya dashboard.

Secrets zinazohitajika (Streamlit -> Settings -> Secrets):

    SMS_PROVIDER = "beem"            # au "africastalking"

    # Ukitumia Beem Africa
    BEEM_API_KEY = "..."
    BEEM_SECRET_KEY = "..."
    BEEM_SENDER_ID = "..."           # Sender ID yako iliyoidhinishwa

    # Ukitumia Africa's Talking
    AT_USERNAME = "..."              # "sandbox" kwa majaribio
    AT_API_KEY = "..."
    AT_SENDER_ID = ""                # hiari
"""
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import time
from contextlib import closing

import requests
import streamlit as st

OTP_TTL = 300               # sekunde 300 = dakika 5
MAX_TRIES = 5               # majaribio ya kuingiza msimbo
RESEND_COOLDOWN = 60        # sekunde kati ya SMS mbili
MAX_SENDS_PER_HOUR = 5      # SMS kwa namba moja kwa saa
MAX_LOGIN_FAILS = 5         # password mbaya kwa username kwa dakika 15
LOGIN_WINDOW = 900

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "otp_phones.db")


def _secret(key, default=""):
    try:
        return str(st.secrets.get(key, default)).strip()
    except Exception:
        return default


# ------------------------------------------------------------------ #
#  Namba za simu
# ------------------------------------------------------------------ #
def safisha_simu(simu):
    """Rudisha namba ya Tanzania kwa muundo 255XXXXXXXXX, au None kama si sahihi."""
    d = re.sub(r"\D", "", str(simu or ""))
    if d.startswith("255") and len(d) == 12:
        pass
    elif d.startswith("0") and len(d) == 10:
        d = "255" + d[1:]
    elif len(d) == 9 and d[0] in "67":
        d = "255" + d
    else:
        return None
    return d if d[3] in "67" else None


def ficha_simu(simu):
    s = str(simu or "")
    return f"{s[:5]}****{s[-3:]}" if len(s) >= 9 else "***"


def _conn():
    c = sqlite3.connect(DB_FILE)
    c.execute(
        "CREATE TABLE IF NOT EXISTS simu_za_watumiaji ("
        "username TEXT PRIMARY KEY, simu TEXT NOT NULL UNIQUE)"
    )
    return c


def pata_simu(username):
    with closing(_conn()) as c:
        row = c.execute(
            "SELECT simu FROM simu_za_watumiaji WHERE username = ?",
            (str(username).strip().lower(),),
        ).fetchone()
    return row[0] if row else None


def simu_inatumika(simu, isipokuwa_username=None):
    """True kama namba tayari ipo kwa mtumiaji mwingine."""
    with closing(_conn()) as c:
        row = c.execute(
            "SELECT username FROM simu_za_watumiaji WHERE simu = ?", (simu,)
        ).fetchone()
    if not row:
        return False
    return row[0] != str(isipokuwa_username or "").strip().lower()


def hifadhi_simu(username, simu):
    """Hifadhi namba. Hurejesha False kama namba inatumika na akaunti nyingine."""
    try:
        with closing(_conn()) as c:
            c.execute(
                "INSERT INTO simu_za_watumiaji (username, simu) VALUES (?, ?) "
                "ON CONFLICT(username) DO UPDATE SET simu = excluded.simu",
                (str(username).strip().lower(), simu),
            )
            c.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# ------------------------------------------------------------------ #
#  Kutuma SMS
# ------------------------------------------------------------------ #
def _tuma_sms(simu, ujumbe):
    """Hurejesha (ok, error_code)."""
    mtoa = _secret("SMS_PROVIDER", "beem").lower()
    try:
        if mtoa == "africastalking":
            user, key = _secret("AT_USERNAME"), _secret("AT_API_KEY")
            if not user or not key:
                return False, "Missing_SMS_Secrets"
            host = "api.sandbox.africastalking.com" if user == "sandbox" else "api.africastalking.com"
            data = {"username": user, "to": f"+{simu}", "message": ujumbe}
            if _secret("AT_SENDER_ID"):
                data["from"] = _secret("AT_SENDER_ID")
            r = requests.post(
                f"https://{host}/version1/messaging",
                data=data,
                headers={"apiKey": key, "Accept": "application/json"},
                timeout=20,
            )
            ok = r.status_code in (200, 201)
        else:
            key, secret = _secret("BEEM_API_KEY"), _secret("BEEM_SECRET_KEY")
            if not key or not secret:
                return False, "Missing_SMS_Secrets"
            payload = {
                "source_addr": _secret("BEEM_SENDER_ID", "INFO"),
                "schedule_time": "",
                "encoding": "0",
                "message": ujumbe,
                "recipients": [{"recipient_id": "1", "dest_addr": simu}],
            }
            r = requests.post(
                "https://apisms.beem.africa/v1/send",
                json=payload,
                auth=(key, secret),
                timeout=20,
            )
            ok = r.status_code == 200
    except Exception as e:
        print(f"[sms] exception: {e}")
        return False, "SMS_Exception"

    if not ok:
        # Usiandike msimbo kwenye logs; andika status na jibu la mtoa huduma tu.
        print(f"[sms] failed {r.status_code}: {r.text[:300]}")
        return False, f"SMS_Failed_{r.status_code}"
    return True, None


# ------------------------------------------------------------------ #
#  Vikomo (hukaa kwenye kumbukumbu ya seva, si kwenye kipindi cha mtumiaji)
# ------------------------------------------------------------------ #
@st.cache_resource
def _sms_sends():
    return {}


@st.cache_resource
def _login_fails():
    return {}


def _ruhusu_kutuma(simu):
    now = time.time()
    store = _sms_sends()
    orodha = [t for t in store.get(simu, []) if now - t < 3600]
    if len(orodha) >= MAX_SENDS_PER_HOUR:
        store[simu] = orodha
        return False
    orodha.append(now)
    store[simu] = orodha
    return True


def login_imefungwa(username):
    now = time.time()
    u = str(username).strip().lower()
    store = _login_fails()
    store[u] = [t for t in store.get(u, []) if now - t < LOGIN_WINDOW]
    return len(store[u]) >= MAX_LOGIN_FAILS


def rekodi_kosa_la_login(username):
    u = str(username).strip().lower()
    _login_fails().setdefault(u, []).append(time.time())


def futa_makosa_ya_login(username):
    _login_fails().pop(str(username).strip().lower(), None)


# ------------------------------------------------------------------ #
#  OTP
# ------------------------------------------------------------------ #
def _hash(salt, username, code):
    return hashlib.sha256(f"{salt}:{str(username).lower()}:{code}".encode()).hexdigest()


def tuma_otp(username, simu):
    """Tengeneza msimbo na utume kwa SMS. Hurejesha (ok, ujumbe_wa_kosa)."""
    now = time.time()
    o = st.session_state.get("otp_state")
    if o and now - o["sent"] < RESEND_COOLDOWN:
        sek = int(RESEND_COOLDOWN - (now - o["sent"])) + 1
        return False, f"Subiri sekunde {sek} kisha jaribu tena."
    if not _ruhusu_kutuma(simu):
        return False, "Umefikia kikomo cha misimbo kwa saa hii. Jaribu tena baadaye."

    code = f"{secrets.randbelow(10 ** 6):06d}"
    ok, err = _tuma_sms(
        simu,
        f"Msimbo wako wa Ourworthlinks ni {code}. Unaisha baada ya dakika 5. Usimpe mtu yeyote.",
    )
    if not ok:
        return False, f"Imeshindikana kutuma SMS ({err}). Jaribu tena."

    salt = secrets.token_hex(8)
    st.session_state["otp_state"] = {
        "user": str(username).lower(),
        "salt": salt,
        "hash": _hash(salt, username, code),
        "exp": now + OTP_TTL,
        "sent": now,
        "tries": 0,
    }
    return True, None


def hakiki_otp(username, code):
    """Hakiki msimbo. Hurejesha (ok, ujumbe_wa_kosa)."""
    o = st.session_state.get("otp_state")
    if not o or o["user"] != str(username).lower():
        return False, "Omba msimbo mpya."
    if time.time() > o["exp"]:
        st.session_state.pop("otp_state", None)
        return False, "Msimbo umeisha muda. Omba mwingine."
    if o["tries"] >= MAX_TRIES:
        st.session_state.pop("otp_state", None)
        return False, "Majaribio yamezidi. Omba msimbo mpya."

    o["tries"] += 1
    if hmac.compare_digest(o["hash"], _hash(o["salt"], username, str(code).strip())):
        st.session_state.pop("otp_state", None)
        return True, None
    return False, "Msimbo si sahihi."
