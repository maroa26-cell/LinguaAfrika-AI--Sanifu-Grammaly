import hashlib
import hmac
import re
import bcrypt
import os
from datetime import datetime, timedelta, timezone

import db_conn

# Faili la SQLite linatumika TU kama `DATABASE_URL` haijawekwa kwenye Secrets
# (mf. majaribio kwenye kompyuta yako). Kwenye Streamlit Cloud tumia Neon (Postgres).
db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ourworthlinks_data.db")

# ONYO: Chumvi tuli ya zamani (SHA-256). Inatunzwa TU kwa ajili ya kuhakiki
# nywila za zamani zilizohifadhiwa kabla ya kuhamia bcrypt, kisha kuzipandisha
# daraja (upgrade) kiotomatiki. HAITUMIKI kutengeneza hash mpya.
LEGACY_SYSTEM_SALT = "owl-secure-salt-node-2026"

# Premium inadumu siku ngapi baada ya kila malipo yaliyokamilika.
SIKU_ZA_PREMIUM = 30

# Majina ambayo mtumiaji wa kawaida haruhusiwi kujisajili nayo.
RESERVED_USERNAMES = {"admin", "administrator", "root", "support", "owner", "system", "staff", "ourworthlinks"}
USERNAME_RE = re.compile(r"^[a-z0-9_.-]{3,30}$")

IntegrityError = db_conn.IntegrityError


def _tengeneza_hash(password_ghafi):
    """🔐 Tengeneza bcrypt hash yenye chumvi ya kipekee kwa kila nywila."""
    # bcrypt ina kikomo cha baiti 72; tunakata kwa usalama ili kuepuka makosa.
    pwd_bytes = password_ghafi.strip().encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


# Hash ya bandia: inatumika kufanya muda wa jibu uwe sawa hata username isipokuwepo
# (inazuia mtu kubaini usernames zilizopo kwa kupima kasi ya jibu).
_DUMMY_HASH = bcrypt.hashpw(b"dummy-password-for-timing", bcrypt.gensalt()).decode("utf-8")


def _ni_hash_ya_zamani(stored_hash):
    """Hash za bcrypt huanza na $2a$/$2b$/$2y$. Nyingine ni za zamani (SHA-256)."""
    return not (stored_hash or "").startswith(("$2a$", "$2b$", "$2y$"))


def _hakiki_hash(password_ghafi, stored_hash):
    """✅ Hakiki nywila dhidi ya hash iliyohifadhiwa (bcrypt au SHA-256 ya zamani)."""
    if not stored_hash:
        return False
    pwd = password_ghafi.strip()
    if _ni_hash_ya_zamani(stored_hash):
        # Njia ya zamani: SHA-256 + chumvi tuli (kwa ulinganifu wa nyuma)
        legacy = hashlib.sha256((LEGACY_SYSTEM_SALT + pwd).encode("utf-8")).hexdigest()
        return hmac.compare_digest(legacy, stored_hash)
    try:
        return bcrypt.checkpw(pwd.encode("utf-8")[:72], stored_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def _safisha_jina(username):
    return str(username or "").strip().lower()


def pata_muunganisho_wa_chuma():
    """👑 Muunganisho wa database: Neon Postgres (DATABASE_URL) au SQLite ya ndani.

    Tumia `conn.cursor()`, `cursor.execute(sql, params)` na `?` kama kishika-nafasi
    kwa SQL zote; safu hii inazibadilisha kuwa `%s` kwa Postgres.
    """
    return db_conn.connect(db_file)


def anzisha_hifadhidata_ya_chuma():
    """📊 SCHEMA INITIALIZER: Creates and indexes localized production tables"""
    conn = pata_muunganisho_wa_chuma()
    try:
        id_col = db_conn.aina_ya_id(conn)

        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS watumiaji (
                id {id_col},
                username TEXT UNIQUE,
                password_hash TEXT,
                hadhi TEXT DEFAULT 'standard user'
            )
        """)

        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS malipo_trans (
                id {id_col},
                username TEXT,
                tracking_id TEXT UNIQUE,
                kiasi DOUBLE PRECISION,
                status TEXT DEFAULT 'pending',
                muda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS kamusi_dataset (
                id {id_col},
                keyword TEXT UNIQUE,
                semantic_meaning TEXT,
                category TEXT DEFAULT 'general'
            )
        """)

        # Migration: safu mpya za premium na za kulinganisha malipo na oda.
        db_conn.ongeza_safu_kama_haipo(conn, "watumiaji", "premium_hadi", "TEXT")
        db_conn.ongeza_safu_kama_haipo(conn, "malipo_trans", "merchant_ref", "TEXT")
        db_conn.ongeza_safu_kama_haipo(conn, "malipo_trans", "sarafu", "TEXT")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_malipo_merchant_ref ON malipo_trans (merchant_ref)")

        conn.execute("CREATE INDEX IF NOT EXISTS idx_keyword_lookup ON kamusi_dataset (keyword)")

        baseline_data = [
            ("mshandao", "Mstari imara au kiungo kilichounganishwa katika mtandao wa mawasiliano (Network Pathway / Pipeline Node).", "technical"),
            ("mnyororo wa kache", "Hifadhi ya muda pfupi ya kumbukumbu ya kompyuta inayozuia mifumo isigande kiofisi.", "infrastructure"),
            ("chujio", "Zana maalum ya kukagua na kusafisha mistari ya msimbo dhidi ya hitilafu za uandishi au kiusalama.", "security"),
            ("urari", "Usawa kamili uliopo kati ya ankara za kiofisi na fedha zilizochakatwa kupitia lango la malipo.", "billing")
        ]

        for key, definition, cat in baseline_data:
            # ON CONFLICT DO NOTHING inafanya kazi kwenye SQLite na Postgres
            # (kukamata IntegrityError kungeharibu transaction ya Postgres).
            conn.execute(
                "INSERT INTO kamusi_dataset (keyword, semantic_meaning, category) VALUES (?, ?, ?) "
                "ON CONFLICT (keyword) DO NOTHING",
                (key, definition, cat),
            )

        # Tengeneza admin wa mwanzo tu ikiwa nywila imewekwa wazi kwenye Secrets.
        # Hakuna nywila ya kawaida iliyowekwa ndani ya msimbo.
        try:
            import streamlit as st
            admin_pwd = str(st.secrets.get("ADMIN_SEED_PASSWORD", "") or "").strip()
        except Exception:
            admin_pwd = ""

        if admin_pwd:
            conn.execute(
                "INSERT INTO watumiaji (username, password_hash, hadhi) VALUES ('admin', ?, 'admin') "
                "ON CONFLICT (username) DO NOTHING",
                (_tengeneza_hash(admin_pwd),),
            )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query_neuroplasticity_lookup(search_term):
    """🧠 NEUROPLASTICITY SEARCH: Fast exact matches and suffix phonetic lookups"""
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()
    clean_term = search_term.strip().lower()

    cursor.execute("SELECT semantic_meaning FROM kamusi_dataset WHERE keyword = ?", (clean_term,))
    exact_hit = cursor.fetchone()

    if exact_hit:
        meaning_string = exact_hit[0]
        conn.close()
        return meaning_string

    cursor.execute("SELECT keyword, semantic_meaning FROM kamusi_dataset")
    all_rows = cursor.fetchall()
    conn.close()

    for keyword, definition in all_rows:
        if clean_term.startswith(keyword) or keyword in clean_term:
            return f"💡 (Did you mean '{keyword}'?): {definition}"

    return None


# ------------------------------------------------------------------ #
#  USAJILI NA LOGIN
# ------------------------------------------------------------------ #
def thibitisha_data_ya_usajili(username, password_ghafi):
    """Hurejesha ujumbe wa kosa (str) kama data si sahihi, au None kama iko sawa."""
    u = _safisha_jina(username)
    p = str(password_ghafi or "").strip()
    if not USERNAME_RE.match(u):
        return "Username iwe na herufi 3 hadi 30: herufi ndogo, namba, na alama _ . - tu."
    if u in RESERVED_USERNAMES:
        return "Username hii imehifadhiwa. Chagua nyingine."
    if len(p) < 8:
        return "Password iwe na angalau herufi 8."
    if p.lower() == u:
        return "Password isifanane na username."
    return None


def sajili_mtumiaji_mpya(username, password_ghafi, hadhi_msingi="premium user"):
    """Sajili mtumiaji mpya kwa nywila iliyofanyiwa hashing kwa bcrypt."""
    if thibitisha_data_ya_usajili(username, password_ghafi) is not None:
        return False
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()
    u_clean = _safisha_jina(username)
    p_hash = _tengeneza_hash(password_ghafi)
    try:
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES (?, ?, ?)", (u_clean, p_hash, hadhi_msingi.lower()))
        conn.commit()
        success = True
    except IntegrityError:
        conn.rollback()
        success = False
    finally:
        conn.close()
    return success


def thibitisha_utambulisho_wa_siri(username, password_ghafi, hadhi_inayotakiwa):
    """Hakiki utambulisho. Hupata hash kwa username+hadhi, kisha huilinganisha kwa
    bcrypt. Nywila za zamani (SHA-256) hupandishwa daraja hadi bcrypt zinapofanikiwa."""
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()
    u_clean = _safisha_jina(username)
    h_clean = hadhi_inayotakiwa.lower()

    cursor.execute(
        "SELECT id, password_hash FROM watumiaji WHERE username = ? AND hadhi = ?",
        (u_clean, h_clean)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        _hakiki_hash(password_ghafi, _DUMMY_HASH)  # muda sawa na kesi ya username sahihi
        return False

    user_id, stored_hash = row

    if not _hakiki_hash(password_ghafi, stored_hash):
        conn.close()
        return False

    # Pandisha daraja hash ya zamani (SHA-256) hadi bcrypt baada ya kuingia kwa mafanikio
    if _ni_hash_ya_zamani(stored_hash):
        try:
            mpya = _tengeneza_hash(password_ghafi)
            cursor.execute("UPDATE watumiaji SET password_hash = ? WHERE id = ?", (mpya, user_id))
            conn.commit()
        except Exception:
            conn.rollback()

    conn.close()
    return True


# ------------------------------------------------------------------ #
#  MALIPO NA PREMIUM
#  Mtiririko: (1) oda inarekodiwa 'pending' pamoja na username kabla ya kwenda Pesapal,
#  (2) mteja akirudi, Pesapal inahakikiwa moja kwa moja, (3) tunalinganisha
#  merchant_reference + kiasi + sarafu, kisha tunampa Premium aliyeanzisha oda.
# ------------------------------------------------------------------ #
def rekodi_oda_inasubiri(merchant_ref, username, kiasi, sarafu):
    """Hifadhi oda mpya (pending). Hurejesha True/False."""
    conn = pata_muunganisho_wa_chuma()
    try:
        conn.execute(
            "INSERT INTO malipo_trans (username, merchant_ref, kiasi, sarafu, status) "
            "VALUES (?, ?, ?, ?, 'pending')",
            (_safisha_jina(username), str(merchant_ref), float(kiasi), str(sarafu).upper()),
        )
        conn.commit()
        return True
    except db_conn.Error as e:
        conn.rollback()
        print(f"[db] rekodi_oda_inasubiri failed: {e}")
        return False
    finally:
        conn.close()


def _soma_tarehe(s):
    try:
        d = datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def pandisha_hadhi_ya_mteja_kiotomatiki(tracking_id, status, merchant_reference="", kiasi=0.0, sarafu=""):
    """Mpe Premium mteja aliyeanzisha oda, baada ya Pesapal kuthibitisha malipo.

    Hurejesha moja ya:
      'applied'        - Premium imewekwa (mara ya kwanza)
      'already'        - malipo haya yalishashughulikiwa
      'mismatch'       - kiasi au sarafu hakilingani na oda
      'unknown_order'  - hakuna oda yenye merchant_reference hiyo
      'not_completed'  - hali si COMPLETED
      'error'          - hitilafu ya ndani
    """
    if str(status).strip().lower() != "completed":
        return "not_completed"
    tracking_id = str(tracking_id or "").strip()
    merchant_reference = str(merchant_reference or "").strip()
    if not tracking_id or not merchant_reference:
        return "unknown_order"

    conn = pata_muunganisho_wa_chuma()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, kiasi, sarafu, status FROM malipo_trans WHERE merchant_ref = ?",
            (merchant_reference,),
        )
        row = cursor.fetchone()
        if not row:
            return "unknown_order"
        order_id, username, kiasi_alichotarajiwa, sarafu_inayotarajiwa, hali_ya_sasa = row

        if hali_ya_sasa == "completed":
            return "already"
        if str(sarafu).upper() != str(sarafu_inayotarajiwa or "").upper() or \
                float(kiasi or 0) + 0.01 < float(kiasi_alichotarajiwa or 0):
            print(f"[db] mismatch ref={merchant_reference} lipwa={kiasi} {sarafu} tarajiwa={kiasi_alichotarajiwa} {sarafu_inayotarajiwa}")
            return "mismatch"

        # Weka 'completed' mara moja tu (hata kama ukurasa unapakiwa mara mbili kwa wakati mmoja).
        # Kwenye Postgres, ombi la pili linasubiri la kwanza likamilike, kisha linaona 0 rows.
        cursor.execute(
            "UPDATE malipo_trans SET status = 'completed', tracking_id = ? WHERE id = ? AND status != 'completed'",
            (tracking_id, order_id),
        )
        if cursor.rowcount != 1:
            conn.rollback()
            return "already"

        sasa = datetime.now(timezone.utc)
        cursor.execute("SELECT premium_hadi FROM watumiaji WHERE username = ?", (username,))
        r = cursor.fetchone()
        if r is None:
            conn.rollback()
            return "unknown_order"
        msingi = sasa
        mwisho = _soma_tarehe(r[0]) if r[0] else None
        if mwisho and mwisho > sasa:
            msingi = mwisho  # amelipa kabla ya kuisha: ongeza juu ya muda uliobaki
        mpya = msingi + timedelta(days=SIKU_ZA_PREMIUM)
        cursor.execute("UPDATE watumiaji SET premium_hadi = ? WHERE username = ?", (mpya.isoformat(), username))
        conn.commit()
        return "applied"
    except IntegrityError as e:
        conn.rollback()
        print(f"[db] integrity error: {e}")
        return "mismatch"
    except Exception as e:
        conn.rollback()
        print(f"[db] pandisha_hadhi error: {e}")
        return "error"
    finally:
        conn.close()


def premium_hadi_lini(username):
    """Tarehe ambayo Premium inaisha (datetime), au None kama hajalipa / imeisha."""
    conn = pata_muunganisho_wa_chuma()
    try:
        row = conn.execute(
            "SELECT premium_hadi FROM watumiaji WHERE username = ?", (_safisha_jina(username),)
        ).fetchone()
    finally:
        conn.close()
    mwisho = _soma_tarehe(row[0]) if row and row[0] else None
    if mwisho and mwisho > datetime.now(timezone.utc):
        return mwisho
    return None


def ni_premium_aliyelipa(username):
    """Tumia hii kuruhusu huduma za Premium. Role ya 'premium user' pekee HAIKUTHIBITISHI malipo."""
    return premium_hadi_lini(username) is not None


# Hakikisha majedwali yapo hata kama ukurasa huu ndio wa kwanza kufunguliwa
# (Streamlit inaendesha ukurasa mmoja tu).
try:
    anzisha_hifadhidata_ya_chuma()
except Exception as _e:
    print(f"[db] init failed: {_e}")
