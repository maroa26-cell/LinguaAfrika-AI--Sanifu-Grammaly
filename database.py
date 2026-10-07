
import sqlite3
import os

DB_NAME = "linguaafrika.db"

def anzisha_hifadhidata_ya_chuma():
    """Inatengeneza meza za siri kwenye diski ya seva kama hazina ya kudumu"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watumiaji (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wasimamizi (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    
    # 👑 AUTOMATED NEURAL SEEDING (KUREKODI USERNAME NA PASSWORD YA MSIMAMIZI)
    # Mtambo unakagua kama kuna admin yeyote, asipokuwepo unaandika akaunti yako ya siri!
    cursor.execute("SELECT COUNT(*) FROM wasimamizi")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO wasimamizi VALUES (?, ?)", ("admin", "Maroa2026"))
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
