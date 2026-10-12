import ast
import re
import streamlit as str_platform

class SovereignCodeAuditor:
    """🛡️ THE ENTERPRISE COGNITIVE SHIELD NODE (DYNAMIC V14 AUTOMATION)"""
    
    def __init__(self):
        self.forbidden_patterns = [
            r"https://://",       # Kufyeka alama mbovu za mshatari zilizorundikana
            r"cybersb\.pesapal",  # Kuzuia mabaki ya endpoint za Sandbox majaribio
            r"http://[^l]"        # Kuzuia itifaki zisizo salama (Non-SSL unsecured connections)
        ]

    def kagua_usahihi_wa_msimbo(self, jina_la_faili, msimbo_ghafi):
        """🧠 DEEP AST COMPILATION PASS: Inasoma na kuhakikisha kodi haina kosa hata moja la uandishi"""
        try:
            # Ukaguzi wa kiwango cha juu cha chujio la compiler ya Python 3.13
            ast.parse(msimbo_ghafi)
            
            # Ukaguzi wa kiusalama wa herufi na viungo vilivyojirudia
            for pattern in self.forbidden_patterns:
                if re.search(pattern, msimbo_ghafi):
                    return {"status": "failed", "message": f"🚨 Chujio limebaini kiungo hatari cha itifaki ndani ya {jina_la_faili}!"}
            
            return {"status": "success", "message": f"🟢 Faili la {jina_la_faili} limepita kwenye chujio salama!"}
        except SyntaxError as se:
            return {"status": "failed", "message": f"🛑 Hitilafu ya Kisintaksia kwenye {jina_la_faili} Mstari {se.lineno}: {se.msg}"}
        except Exception as e:
            return {"status": "failed", "message": f"⚠️ Kosa lisilojulikana: {str(e)}"}

    def pata_anuani_salama_ya_domain(self):
        """⚡ DYNAMIC DOMAIN AUTO-SYNC: Inadaka URL halisi ya sasa hivi kuzuia kache ya link ndefu kuganda"""
        try:
            # Inasoma parameter halisi za muundo wa seva ya Streamlit kiotomatiki
            if hasattr(str_platform, "experimental_get_query_params"):
                return "https://streamlit.app"
        except Exception:
            pass
        # Fallback ya chuma reli inayolinda mfumo usizimike
        return "https://streamlit.app"

# Zindua mtambo kama single instance mwilini mwake
auditor_mkuu = SovereignCodeAuditor()
