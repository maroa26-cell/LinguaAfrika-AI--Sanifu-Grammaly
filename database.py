

import sqlite3
import hashlib
import bcrypt

db_file = "ourworthlinks_data.db"

# ONYO: Chumvi tuli ya zamani (SHA-256). Inatunzwa TU kwa ajili ya kuhakiki
# nywila za zamani zilizohifadhiwa kabla ya kuhamia bcrypt, kisha kuzipandisha
# daraja (upgrade) kiotomatiki. HAITUMIKI kutengeneza hash mpya.
LEGACY_SYSTEM_SALT = "owl-secure-salt-node-2026"


def _tengeneza_hash(password_ghafi):
    """🔐 Tengeneza bcrypt hash yenye chumvi ya kipekee kwa kila nywila."""
    # bcrypt ina kikomo cha baiti 72; tunakata kwa usalama ili kuepuka makosa.
    pwd_bytes = password_ghafi.strip().encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


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
        return legacy == stored_hash
    try:
        return bcrypt.checkpw(pwd.encode("utf-8")[:72], stored_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def pata_muunganisho_wa_chuma():
    """👑 NO-LOCK CONNECTION MATRIX: Resolves concurrency database lock risks"""
    return sqlite3.connect(
        db_file,
        timeout=30.0,
        check_same_thread=False
    )


def anzisha_hifadhidata_ya_chuma():
    """📊 SCHEMA INITIALIZER: Creates and indexes localized production tables"""
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            hadhi TEXT DEFAULT 'standard user'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS malipo_trans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            tracking_id TEXT UNIQUE,
            kiasi REAL,
            status TEXT DEFAULT 'pending',
            muda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kamusi_dataset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            semantic_meaning TEXT,
            category TEXT DEFAULT 'general'
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_keyword_lookup ON kamusi_dataset (keyword)")

    baseline_data = [
        ("mshandao", "Mstari imara au kiungo kilichounganishwa katika mtandao wa mawasiliano (Network Pathway / Pipeline Node).", "technical"),
        ("mnyororo wa kache", "Hifadhi ya muda pfupi ya kumbukumbu ya kompyuta inayozuia mifumo isigande kiofisi.", "infrastructure"),
        ("chujio", "Zana maalum ya kukagua na kusafisha mistari ya msimbo dhidi ya hitilafu za uandishi au kiusalama.", "security"),
        ("urari", "Usawa kamili uliopo kati ya ankara za kiofisi na fedha zilizochakatwa kupitia lango la malipo.", "billing")
    ]

    for key, definition, cat in baseline_data:
        try:
            cursor.execute("INSERT INTO kamusi_dataset (keyword, semantic_meaning, category) VALUES (?, ?, ?)", (key, definition, cat))
        except sqlite3.IntegrityError:
            pass

    # Panda admin wa mwanzo kwa bcrypt. Nywila halisi IWEKWE kupitia Streamlit
    # Secrets, SI ndani ya msimbo. 'admin123' ni ya mwanzo tu ya maendeleo.
    try:
        import streamlit as st
        admin_pwd = st.secrets.get("ADMIN_SEED_PASSWORD", "admin123")
    except Exception:
        admin_pwd = "admin123"

    try:
        p_admin = _tengeneza_hash(admin_pwd)
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES ('admin', ?, 'admin')", (p_admin,))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
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


def sajili_mtumiaji_mpya(username, password_ghafi, hadhi_msingi="premium user"):
    """Sajili mtumiaji mpya kwa nywila iliyofanyiwa hashing kwa bcrypt."""
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    p_hash = _tengeneza_hash(password_ghafi)
    try:
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES (?, ?, ?)", (u_clean, p_hash, hadhi_msingi.lower()))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success


def thibitisha_utambulisho_wa_siri(username, password_ghafi, hadhi_inayotakiwa):
    """Hakiki utambulisho. Hupata hash kwa username+hadhi, kisha huilinganisha kwa
    bcrypt. Nywila za zamani (SHA-256) hupandishwa daraja hadi bcrypt zinapofanikiwa."""
    conn = pata_muunganisho_wa_chuma()
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    h_clean = hadhi_inayotakiwa.lower()

    cursor.execute(
        "SELECT id, password_hash FROM watumiaji WHERE username = ? AND hadhi = ?",
        (u_clean, h_clean)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
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
            pass

    conn.close()
    return True
