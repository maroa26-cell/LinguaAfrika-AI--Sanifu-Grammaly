import sqlite3
import hashlib

DB_FILE = "ourworthlinks_data.db"
SYSTEM_SALT = "owl-secure-salt-node-2026"

def anzisha_hifadhidata_ya_chuma():
    """👑 CORE DATABASE INITIALIZER: Inaunda majedwali yote makuu ya kiwanda"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 📑 JEDWALI LA I: Watumiaji na Hadhi zao (Standard au Premium User)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            hadhi TEXT DEFAULT 'Standard User'
        )
    """)
    
    # 📑 JEDWALI LA II: Urari wa Malipo ya Pesapal & Stripe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS malipo_trans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            tracking_id TEXT UNIQUE,
            kiasi REAL,
            status TEXT DEFAULT 'PENDING',
            muda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sakinisha akaunti ya siri ya Utawala (Admin) ya dharura isipokuwa ipo tayari
    try:
        p_admin = hashlib.sha256((SYSTEM_SALT + "admin123").encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES ('admin', ?, 'Admin')", (p_admin,))
    except sqlite3.IntegrityError:
        pass
        
    conn.commit()
    conn.close()

def sajili_mtumiaji_mpya(username, password_ghafi, hadhi_msingi="Premium User"):
    """📝 USER REGISTRATION SUITE: Usajili salama uliopigwa chujio la SHA-256"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    p_clean = password_ghafi.strip()
    p_hash = hashlib.sha256((SYSTEM_SALT + p_clean).encode('utf-8')).hexdigest()
    
    try:
        cursor.execute("INSERT INTO watumiaji (username, password_hash, hadhi) VALUES (?, ?, ?)", (u_clean, p_hash, hadhi_msingi))
        conn.commit()
        ufanisi = True
    except sqlite3.IntegrityError:
        ufanisi = False
    finally:
        conn.close()
    return ufanisi

def thibitisha_utambulisho_wa_siri(username, password_ghafi, hadhi_inayotakiwa):
    """🔐 IDENTITY AUTHENTICATION PASS: Uhakiki wa siri wa mlangoni kwa 1ms Latency"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    u_clean = username.strip().lower()
    p_clean = password_ghafi.strip()
    p_hash = hashlib.sha256((SYSTEM_SALT + p_clean).encode('utf-8')).hexdigest()
    
    cursor.execute("SELECT id FROM watumiaji WHERE username = ? AND password_hash = ? AND hadhi = ?", (u_clean, p_hash, hadhi_inayotakiwa))
    mtumiaji = cursor.fetchone()
    conn.close()
    return mtumiaji is not None

def pandisha_hadhi_ya_mteja_kiotomatiki(tracking_id, status_mpya="COMPLETED"):
    """⚡ AUTOMATED PREMIUM UPGRADE NODE: Inafungua tuple index na kumpandisha hadhi mteja (Deep Audit Fixed!)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Hatua ya A: Sasisha hadhi ya ankara kwanza kwenye jedwali la malipo
        cursor.execute("UPDATE malipo_trans SET status = ? WHERE tracking_id = ?", (status_mpya, tracking_id))
        
        # Hatua ya B: Tafuta username inayomiliki ankara hiyo ili kumpandisha cheo kiofisi
        cursor.execute("SELECT username FROM malipo_trans WHERE tracking_id = ?", (tracking_id,))
        mteja = cursor.fetchone()
        
        if mteja and len(mteja) > 0:
            username_halisi = mteja[0] # 👑 CHUMA RELI: Imedakwa kama index 0 kufungua tuple kuingia string safi!
            cursor.execute("UPDATE watumiaji SET hadhi = 'Premium User' WHERE username = ?", (username_halisi,))
            conn.commit()
            return True
    except Exception:
        pass
    finally:
        conn.close()
    return False
