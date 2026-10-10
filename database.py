import sqlite3
import hashlib

# 👑 ORIGINAL SYSTEM SALT: Ufunguo wa kipekee wa kampuni ya Ourworthlinks kulinda nenosiri dhidi ya mashambulizi ya kimtandao
SYSTEM_SALT = "Ourworthlinks_Sovereign_Radio_Key_2026_Secure_Token"

def zalisha_nenosiri_la_siri(password_ghafi):
    """🧠 CRYPTOGRAPHIC CORE ENGINE: Inabadilisha password kuwa hash ya herufi 64 zisizoweza kurudishwa nyuma"""
    fomula_ya_siri = password_ghafi + SYSTEM_SALT
    return hashlib.sha256(fomula_ya_siri.encode('utf-8')).hexdigest()

def anzisha_hifadhidata_ya_chuma():
    """🧠 LONG-TERM SECURE MEMORY STORAGE INITIALIZATION (SQLite Core)"""
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    
    # Kujenga Jedwali la Watumiaji wenye Ulinzi wa Hali ya Juu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji_wa_chuma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            hadhi_yako TEXT NOT NULL,
            muda_wa_usajili TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 👑 AUTOMATED ADMIN ENCRYPTION SEEDING: Hakikisha akaunti kuu ya Admin inafungwa hash tangu kuwaka kwa seva
    username_admin = "admin"
    password_admin_ghafi = "Maroa2026"
    password_hash_timilifu = zalisha_nenosiri_la_siri(password_admin_ghafi)
    
    try:
        cursor.execute("""
            INSERT INTO watumiaji_wa_chuma (username, password_hash, hadhi_yako)
            VALUES (?, ?, ?)
        """, (username_admin, password_hash_timilifu, "Admin"))
        conn.commit()
    except sqlite3.IntegrityError:
        # Akaunti tayari imeshafungwa hash na ipo mwilini mwa database, ruka hatua kuzuia duplicate
        pass
        
    conn.close()

def sajili_mtumiaji_mpya(username, password, hadhi):
    """
    Parametrize na kusajili mtumiaji mpya kwa siri:
    Mtumiaji anapojisajili na kulipa $5.00 USD Pesapal, password yake inapigwa hash ya SHA-256 kabla ya kuingia kwenye chuma!
    """
    if username.strip() == "" or password.strip() == "":
        return False
        
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    
    # Kuchakata ulinzi wa nenosiri hapa
    password_encrypted = zalisha_nenosiri_la_siri(password.strip())
    
    try:
        cursor.execute("""
            INSERT INTO watumiaji_wa_chuma (username, password_hash, hadhi_yako)
            VALUES (?, ?, ?)
        """, (username.strip().lower(), password_encrypted, hadhi))
        conn.commit()
        fanaka = True
    except sqlite3.IntegrityError:
        fanaka = False
        
    conn.close()
    return fanaka

def thibitisha_utambulisho_wa_siri(username, password, hadhi_inayotakiwa):
    """🔑 SECURE AUTHENTICATION RADAR: Inahakiki nenosiri kwa kulinganisha hash za SHA-256 pasipo kufungua password ghafi"""
    if username.strip() == "" or password.strip() == "":
        return False
        
    conn = sqlite3.connect("linguaafrika_cns.db")
    cursor = conn.cursor()
    
    # Kupiga hash password aliyoandika sasa hivi mtumiaji mlangoni ili kulinganisha na database
    hash_ya_kulinganisha = zalisha_nenosiri_la_siri(password.strip())
    
    cursor.execute("""
        SELECT username FROM watumiaji_wa_chuma
        WHERE username = ? AND password_hash = ? AND hadhi_yako = ?
    """, (username.strip().lower(), hash_ya_kulinganisha, hadhi_inayotakiwa))
    
    user_record = cursor.fetchone()
    conn.close()
    
    return user_record is not None
