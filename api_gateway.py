import streamlit as str_platform
import database
import time

def thibitisha_ufunguo_wa_kampuni_ya_nje(api_key_ya_mteja):
    """Inakagua kama kampuni ya nje imelipia leseni ya kutumia AI yetu"""
    # Kwenye SQLite, tutatengeneza meza ya funguo za kibiashara (B2B Client Table)
    if api_key_ya_mteja == "owl-live-secret-enterprise-key-2026":
        return True
    return False

def anzisha_lango_la_api_kibiashara(client, payload_data):
    """
    🏢 B2B GATEWAY INTERFACE
    Inachukua mzigo wa data kutoka kwa kampuni ya nje, kuuchakata kwa kasi ya radi,
    na kutoa ankara (billing tracking) kwa kampuni ya Ourworthlinks.
    """
    muda_mwanzo = time.time()
    api_key = payload_data.get("api_key")
    text_to_process = payload_data.get("text", "")
    task_type = payload_data.get("task", "translation") # translation au dictionary
    
    if not thibitisha_ufunguo_wa_kampuni_ya_nje(api_key):
        return {"status": "error", "error_code": 403, "message": "🛑 Invalid B2B API Key! Access Denied."}
        
    if text_to_process.strip() == "":
        return {"status": "error", "error_code": 400, "message": "🛑 Input text cannot be empty."}

    # Kusukuma ombi kuelekea seli kuu za OpenAI GPT-4o
    try:
        if task_type == "translation":
            target_lang = payload_data.get("target_lang", "English")
            prompt = f"Translate the following text to {target_lang} professionally:\n\n{text_to_process}"
        else:
            prompt = f"Provide a comprehensive African dictionary definition and sentence examples for: {text_to_process}"
            
        jibu = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        kasi_ya_radi = (time.time() - muda_mwanzo) * 1000
        maneno_yaliyochakatwa = len(text_to_process.split())
        ankara_usd = maneno_yaliyochakatwa * 0.002 # Ada ya \$0.002 kwa kila neno moja
        
        return {
            "status": "success",
            "project": "LinguaAfrika AI",
            "company_owner": "Ourworthlinks",
            "processed_text": jibu.choices.message.content,
            "metrics": {
                "latency_ms": f"{kasi_ya_radi:.2f}ms",
                "words_counted": maneno_yaliyochakatwa,
                "billing_accrued_usd": f"${ankara_usd:.5f}"
            }
        }
    except Exception as e:
        return {"status": "error", "error_code": 500, "message": f"🛑 Internal Server Error: {str(e)}"}
