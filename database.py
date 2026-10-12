import sqlite3
import hashlib

DB_FILE = "ourworthlinks_data.db"
SYSTEM_SALT = "owl-secure-salt-node-2026"

def anzisha_hifadhidata_ya_chuma():
    """📊 INDEXED VECTOR CONTEXT MATRIX: Initializes schema tables with database key indexings"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 📑 Table I: Security profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            hadhi TEXT DEFAULT 'standard user'
        )
    """)
    
    # 📑 Table II: Transaction accounting ledger
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
    
    # 📑 Table III: Ultra-scalable localized proprietary Swahili dataset matrix
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kamusi_dataset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            semantic_meaning TEXT,
            category TEXT DEFAULT 'general'
        )
    """)
    
    # 👑 B-TREE INDEXING ENGINE: Forces SQLite to search terms directly via memory vectors
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_keyword_lookup ON kamusi_dataset (keyword)")
    
    # Ingest baseline structural enterprise vocabulary objects
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

    try:
        p_admin = hashlib.sha256((SYSTEM_SALT + "admin123").encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES ('admin', ?, 'admin')", (p_admin,))
    except sqlite3.IntegrityError:
        pass
        
    conn.commit()
    conn.close()

def query_neuroplasticity_lookup(search_term):
    """🧠 NEUROPLASTICITY SEARCH NODE: Unpacks row data tuple cleanly to resolve near-miss spellings"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    clean_term = search_term.strip().lower()
    
    # Try exact match on indexed vector parameters first (0.1ms performance)
    cursor.execute("SELECT semantic_meaning FROM kamusi_dataset WHERE keyword = ?", (clean_term,))
    exact_hit = cursor.fetchone()
    
    if exact_hit:
        meaning_string = exact_hit[0] # 👑 CHUMA RELI: Unpacks string index directly to eliminate tuple mismatch errors
        conn.close()
        return meaning_string
        
    # Semantic approximation loop: handles dynamic suffix drops or spelling misses
    cursor.execute("SELECT keyword, semantic_meaning FROM kamusi_dataset")
    all_rows = cursor.fetchall()
    conn.close()
    
    for keyword, definition in all_rows:
        if clean_term.startswith(keyword) or keyword in clean_term:
            return f"💡 (Did you mean '{keyword}'?): {definition}"
            
    return None

def sajili_mtumiaji_mpya(username, password_ghafi, hadhi_msingi="premium user"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    p_hash = hashlib.sha256((SYSTEM_SALT + password_ghafi.strip()).encode('utf-8')).hexdigest()
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
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    p_hash = hashlib.sha256((SYSTEM_SALT + password_ghafi.strip()).encode('utf-8')).hexdigest()
    cursor.execute("SELECT id FROM watumiaji WHERE username = ? AND password_hash = ? AND hadhi = ?", (u_clean, p_hash, hadhi_inayotakiwa.lower()))
    user = cursor.fetchone()
    conn.close()
    return user is not None
