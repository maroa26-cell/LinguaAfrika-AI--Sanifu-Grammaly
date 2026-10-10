
import sqlite3
import hashlib

def anzisha_hifadhidata_ya_chuma():
    """🧠 LONG-TERM MEMORY STORAGE INITIALIZATION (SQLite Engine)"""
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    
    # 🏢 Lango la Watumiaji wa Mfumo (Admin & Premium Users)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji_wa_chuma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            hadhi_yako TEXT NOT NULL,
            muda_wa_usajili TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 👑 AUTOMATED SEEDING: Hakikisha akaunti kuu ya utawala (Admin) ipo hai mlangoni kila mara!
    username_admin = "admin"
    password_ghafi = "Maroa2026"
    password_hash = hashlib.sha256(password_ghafi.encode()).hexdigest()
    
    try:
        cursor.execute("""
            INSERT INTO watumiaji_wa_chuma (username, password_hash, hadhi_yako)
            VALUES (?, ?, ?)
        """, (username_admin, password_hash, "Admin"))
        conn.commit()
    except sqlite3.IntegrityError:
        # Akaunti tayari ipo mwilini mwa database, ruka hatua kuzuia mgongano
        pass
        
    conn.close()

def sajili_mtumiaji_mpya(username, password, hadhi):
    """💾 MEMORY RECEPTOR: Inasajili mtumiaji mpya na kukata ada ya $5.00 USD ya Pesapal"""
    if username.strip() == "" or password.strip() == "":
        return False
        
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute("""
            INSERT INTO watumiaji_wa_chuma (username, password_hash, hadhi_yako)
            VALUES (?, ?, ?)
        """, (username.strip().lower(), password_hash, hadhi))
        conn.commit()
        fanaka = True
    except sqlite3.IntegrityError:
        fanaka = False
        
    conn.close()
    return fanaka

def thibitisha_utambulisho_wa_siri(username, password, hadhi_inayotakiwa):
    """🔑 AUTHENTICATION RADAR: Inahakiki funguo za siri za Admin wakati wa kuwasha Jopo Kuu"""
    if username.strip() == "" or password.strip() == "":
        return False
        
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("""
        SELECT username FROM watumiaji_wa_chuma
        WHERE username = ? AND password_hash = ? AND hadhi_yako = ?
    """, (username.strip().lower(), password_hash, hadhi_inayotakiwa))
    
    user_record = cursor.fetchone()
    conn.close()
    
    return user_record is not None
