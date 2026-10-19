"""Uthibitisho wa hatua mbili kwa app ya Authenticator (TOTP, RFC 6238).

Inafanya kazi na Google Authenticator, Microsoft Authenticator, Authy, 2FAS, n.k.
Haihitaji mtoa huduma wa SMS wala internet ya ziada: kila kitu kinahesabiwa
kwenye seva yako na kwenye simu ya mteja.

Mahitaji ya hiari (kwa picha ya QR): ongeza `segno` kwenye requirements.txt.
Bila `segno`, mteja ataona "setup key" na ataiingiza kwa mkono kwenye app.
"""
import base64
import hashlib
import hmac
import io
import os
import re
import secrets
import sqlite3
import struct
import time
from contextlib import closing
from urllib.parse import quote

import streamlit as st

import db_conn

ISSUER = "Ourworthlinks"
STEP = 30           # sekunde 30 kwa kila msimbo
DIGITS = 6
WINDOW = 1          # kubali msimbo uliopita na ujao (tofauti ya saa kidogo)
RECOVERY_COUNT = 8

MAX_LOGIN_FAILS = 5     # makosa kwa username kwa dakika 15
LOGIN_WINDOW = 900

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth_2fa.db")


# ------------------------------------------------------------------ #
#  TOTP (stdlib tu)
# ------------------------------------------------------------------ #
def generate_secret():
    """Siri ya base32 ya herufi 32 (biti 160)."""
    return base64.b32encode(secrets.token_bytes(20)).decode()


def _hotp(secret, counter, digits=DIGITS):
    key = base64.b32decode(secret.upper() + "=" * (-len(secret) % 8))
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    off = mac[-1] & 0x0F
    value = (struct.unpack(">I", mac[off:off + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(value).zfill(digits)


def verify_totp(secret, code, last_counter=0, now=None):
    """Hakiki msimbo. Hurejesha counter iliyotumika, au None kama si sahihi.

    `last_counter` huzuia msimbo uleule kutumika mara mbili (replay).
    """
    code = re.sub(r"\s", "", str(code or ""))
    if not re.fullmatch(r"\d{6}", code):
        return None
    current = int((time.time() if now is None else now) // STEP)
    found = None
    for c in range(current - WINDOW, current + WINDOW + 1):
        if hmac.compare_digest(_hotp(secret, c), code) and c > last_counter:
            found = c
    return found


def provisioning_uri(username, secret):
    label = quote(f"{ISSUER}:{username}")
    return (
        f"otpauth://totp/{label}?secret={secret}&issuer={quote(ISSUER)}"
        f"&algorithm=SHA1&digits={DIGITS}&period={STEP}"
    )


def qr_png(data):
    """Picha ya QR (bytes za PNG), au None kama `segno` haijawekwa."""
    try:
        import segno

        buf = io.BytesIO()
        segno.make(data, error="m").save(buf, kind="png", scale=6, border=2)
        return buf.getvalue()
    except Exception as e:
        print(f"[2fa] QR haikutengenezwa: {e}")
        return None


# ------------------------------------------------------------------ #
#  Hifadhi (SQLite)
# ------------------------------------------------------------------ #
_TABLE_READY_FOR = None


def _conn():
    """Muunganisho (Neon Postgres kama DATABASE_URL ipo, vinginevyo SQLite) + jedwali tayari."""
    global _TABLE_READY_FOR
    c = db_conn.connect(DB_FILE)
    ufunguo = (db_conn.database_url(), DB_FILE)
    if _TABLE_READY_FOR != ufunguo:
        c.execute(
            "CREATE TABLE IF NOT EXISTS totp_secrets ("
            "username TEXT PRIMARY KEY, secret TEXT NOT NULL, "
            "last_counter BIGINT NOT NULL DEFAULT 0, recovery TEXT NOT NULL DEFAULT '')"
        )
        c.commit()
        _TABLE_READY_FOR = ufunguo
    return c


def _u(username):
    return str(username).strip().lower()


def get_totp(username):
    """Hurejesha (secret, last_counter) au (None, 0) kama hajawasha 2FA."""
    with closing(_conn()) as c:
        row = c.execute(
            "SELECT secret, last_counter FROM totp_secrets WHERE username = ?", (_u(username),)
        ).fetchone()
    return (row[0], row[1]) if row else (None, 0)


def has_totp(username):
    return get_totp(username)[0] is not None


def _hash_recovery(code):
    norm = re.sub(r"[^a-z0-9]", "", str(code).lower())
    return hashlib.sha256(norm.encode()).hexdigest()


def new_recovery_codes():
    """Hurejesha orodha ya recovery codes (zionyeshwe mara moja tu)."""
    out = []
    for _ in range(RECOVERY_COUNT):
        raw = secrets.token_hex(5)  # herufi 10
        out.append(f"{raw[:5]}-{raw[5:]}")
    return out


def save_totp(username, secret, recovery_codes, counter):
    hashes = ",".join(_hash_recovery(c) for c in recovery_codes)
    with closing(_conn()) as c:
        c.execute(
            "INSERT INTO totp_secrets (username, secret, last_counter, recovery) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(username) DO UPDATE SET secret = excluded.secret, "
            "last_counter = excluded.last_counter, recovery = excluded.recovery",
            (_u(username), secret, int(counter), hashes),
        )
        c.commit()


def update_counter(username, counter):
    with closing(_conn()) as c:
        c.execute(
            "UPDATE totp_secrets SET last_counter = ? WHERE username = ? AND last_counter < ?",
            (int(counter), _u(username), int(counter)),
        )
        c.commit()


def use_recovery_code(username, code):
    """True kama recovery code ni sahihi; inafutwa baada ya kutumika (mara moja tu)."""
    h = _hash_recovery(code)
    with closing(_conn()) as c:
        row = c.execute(
            "SELECT recovery FROM totp_secrets WHERE username = ?", (_u(username),)
        ).fetchone()
        if not row or not row[0]:
            return False
        zamani = row[0]
        hashes = zamani.split(",")
        match = None
        for x in hashes:
            if hmac.compare_digest(x, h):
                match = x
        if match is None:
            return False
        hashes.remove(match)
        # Compare-and-set: ikiwa ombi lingine limeshatumia code hii, hakuna safu itakayobadilika.
        cur = c.execute(
            "UPDATE totp_secrets SET recovery = ? WHERE username = ? AND recovery = ?",
            (",".join(hashes), _u(username), zamani),
        )
        ok = cur.rowcount == 1
        c.commit()
    return ok


def reset_totp(username):
    """Kwa admin: mteja akipoteza simu na recovery codes, futa 2FA yake ili ajisajili upya."""
    with closing(_conn()) as c:
        c.execute("DELETE FROM totp_secrets WHERE username = ?", (_u(username),))
        c.commit()


# ------------------------------------------------------------------ #
#  Kikomo cha majaribio (kinakaa kwenye seva, si kwenye kipindi cha mtumiaji)
# ------------------------------------------------------------------ #
@st.cache_resource
def _fails():
    return {}


def login_imefungwa(username):
    now = time.time()
    u = _u(username)
    store = _fails()
    store[u] = [t for t in store.get(u, []) if now - t < LOGIN_WINDOW]
    return len(store[u]) >= MAX_LOGIN_FAILS


def rekodi_kosa(username):
    _fails().setdefault(_u(username), []).append(time.time())


def futa_makosa(username):
    _fails().pop(_u(username), None)


# ------------------------------------------------------------------ #
#  Namba ya simu ya malipo (Pesapal)
# ------------------------------------------------------------------ #
def safisha_simu_malipo(simu):
    """Namba ya Tanzania -> 255XXXXXXXXX. Namba za nchi nyingine (tarakimu 10-15) zinapita kama zilivyo."""
    d = re.sub(r"\D", "", str(simu or ""))
    if d.startswith("255") and len(d) == 12 and d[3] in "67":
        return d
    if d.startswith("0") and len(d) == 10 and d[1] in "67":
        return "255" + d[1:]
    if len(d) == 9 and d[0] in "67":
        return "255" + d
    if 10 <= len(d) <= 15 and not d.startswith("0"):
        return d
    return None
