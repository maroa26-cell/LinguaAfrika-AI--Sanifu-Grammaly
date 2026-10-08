import sqlite3
import os

DB_NAME = "linguaafrika.db"

def anzisha_hifadhidata_ya_chuma():
    """Inatengeneza meza za siri kwenye diski ya seva kama hazina ya kudumu"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Meza ya Premium Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    
    # 2. Meza ya Executive Administrators
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wasimamizi (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    
    # 3. 👑 MEZA MPYA YA CHUMA: B2B API TOKENS (UBORESHAJI WA MAREKEBISHO!)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS b2b_tokens (
            api_key TEXT PRIMARY KEY,
            company_name TEXT,
            status TEXT
        )
    """)
    conn.commit()
    
    # AUTOMATED MSIMAMIZI SEEDING
    cursor.execute("SELECT COUNT(*) FROM wasimamizi")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO wasimamizi VALUES (?, ?)", ("admin", "Maroa2026"))
        conn.commit()
        
    # 🏢 AUTOMATED B2B CLIENT SEEDING (KUREKODI TOKEN YA KAMPUNI YA NJE)
    cursor.execute("SELECT COUNT(*) FROM b2b_tokens")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO b2b_tokens VALUES (?, ?, ?)", ("owl-live-secret-enterprise-key-2026", "Global Tech Client v1", "active"))
        conn.commit()
        
    conn.close()

def sajili_mtumiaji_mpya(username, password, role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        if role == "Admin":
            cursor.execute("INSERT INTO wasimamizi VALUES (?, ?)", (username, password))
        else:
            cursor.execute("INSERT INTO watumiaji VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def thibitisha_utambulisho_wa_siri(username, password, role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if role == "Admin":
        cursor.execute("SELECT * FROM wasimamizi WHERE username=? AND password=?", (username, password))
    else:
        cursor.execute("SELECT * FROM watumiaji WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# 👑 KAZI MPYA ZINAZOINGIA KWENYE CHUMA KIOFISI (B2B READ/WRITE LOGIC)
def sajili_kampuni_ya_nje_mpya(api_key, company_name):
    """Inasajili ufunguo mpya wa kibiashara wa mteja wa kigeni kwenye SQLite"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO b2b_tokens VALUES (?, ?, ?)", (api_key, company_name, "active"))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def thibitisha_b2b_api_key_kwenye_chuma(api_key):
    """Inakagua kama ufunguo wa kampuni ya nje upo hai na umeruhusiwa kiofisi"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM b2b_tokens WHERE api_key=? AND status='active'", (api_key,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
