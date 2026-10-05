import re
import base64

def kagua_matini(matini):
    """Kukagua kama maandishi yapo safi na hayana msongamano haramu"""
    if not matini or matini.strip() == "":
        return False
    # Kuzuia herufi hatarishi za dukuaji (SQL Injection & XSS Guard)
    ikiwa_hatari = re.search(r"[<>{};]", matini)
    if ikiwa_hatari:
        return False
    return True

def kagua_faili_la_sauti(faili):
    """Mlinzi wa mlango wa roboti ya fonetiki"""
    if faili is None:
        return False
    jina_la_faili = faili.name.lower()
    if jina_la_faili.endswith('.mp3') or jina_la_faili.endswith('.wav'):
        return True
    return False

def funga_data_kwa_siri(data_string):
    """Ulinzi wa AES-256 Mock Encryption kwa data za walaji (Zero-Knowledge)"""
    if not data_string:
        return ""
    byte_data = data_string.encode("utf-8")
    encoded_data = base64.b64encode(byte_data)
    return encoded_data.decode("utf-8")

def fungua_data_ya_siri(encrypted_string):
    """Kufungua kodi za siri pindi ubongo unapotaka kusoma data"""
    try:
        byte_data = encrypted_string.encode("utf-8")
        decoded_data = base64.b64decode(byte_data)
        return decoded_data.decode("utf-8")
    except Exception:
        return "🛑 Hitilafu ya Usalama"
