import ast
import os
import sys
import re
import time

class OurworthlinksCodeAuditor:
    def __init__(self, filename="app.py"):
        self.filename = filename
        self.billing_rate_per_audit = 0.05  # Ada ya $0.05 kwa kila faili moja linalokaguliwa B2B
        
    def kagua_uvujaji_wa_funguo_za_siri(self, kodi_ghafi):
        """🛡️ PREMIUM SECURITY AUDIT: Inabaini kama mwandishi ameacha API Keys ghafi kwenye kodi"""
        # Regex maalum ya kusaka herufi za siri (mfano sk-proj-... au AIza...)
        mitego_ya_siri = {
            "OpenAI API Key Leak": r"sk-[a-zA-Z0-9]{32,}",
            "Generic Password Leak": r"password\s*=\s*['\"][a-zA-Z0-9_@#]{6,}['\"]",
            "Generic API Key Leak": r"api_key\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]"
        }
        
        makosa_yaliyopatikana = []
        for jina_la_kosa, pattern in mitego_ya_siri.items():
            matches = re.findall(pattern, kodi_ghafi, re.IGNORECASE)
            if matches:
                makosa_yaliyopatikana.append(jina_la_kosa)
        return makosa_yaliyopatikana

    def zindua_ukaguzi_wa_kibiashara(self, b2b_client_name="Anonymous External Developer"):
        """🏢 B2B COMMERCIAL ENTERPRISE ENGINE WITH BILLING LOGS"""
        muda_mwanzo = time.time()
        
        if not os.path.exists(self.filename):
            return {
                "status": "error",
                "message": f"🛑 Faili la {self.filename} halijapatikana kwenye mfumo wetu!"
            }
            
        with open(self.filename, "r", encoding="utf-8") as f:
            kodi_ghafi = f.read()
            
        latency_start = time.time()
        try:
            # 1. Ukaguzi wa Kisintaksia (Syntax and Indentation)
            ast.parse(kodi_ghafi, filename=self.filename)
            
            # 2. Ukaguzi wa Usalama wa Ndani (Security Audit)
            vifu_vya_siri = self.kagua_uvujaji_wa_funguo_za_siri(kodi_ghafi)
            
            kasi_ya_radi = (time.time() - muda_mwanzo) * 1000
            
            status_flag = "🟢 PASSED" if not vifu_vya_siri else "⚠️ WARNING"
            msg = "Kodi haina kosa la spaces au sintaksia." if not vifu_vya_siri else "🛑 TAHADHARI: Kodi haina kosa la spaces lakini ina uvujaji wa data za siri!"
            
            return {
                "status": "success",
                "project": "Ourworthlinks Automated Code Auditor SaaS",
                "b2b_client": b2b_client_name,
                "audit_result": status_flag,
                "syntax_validation": "🟢 Flawless Code Structure",
                "security_leaks_detected": vifu_vya_siri if vifu_vya_siri else "🟢 Clean (No Keys Leaked)",
                "metrics": {
                    "latency_ms": f"{kasi_ya_radi:.3f}ms",
                    "billing_accrued_usd": f"${self.billing_rate_per_audit:.2f}"
                },
                "message": msg
            }
            
        except IndentationError as ie:
            return {
                "status": "failed",
                "error_type": "IndentationError",
                "line_number": ie.lineno,
                "message": f"🛑 DHURUMA YA SPACES IMEDAKWA! Line {ie.lineno}: {ie.msg}. Tafadhali weka nafasi 4 safi!"
            }
        except SyntaxError as se:
            return {
                "status": "failed",
                "error_type": "SyntaxError",
                "line_number": se.lineno,
                "message": f"🛑 DHURUMA YA UTANZI IMEDAKWA! Line {se.lineno}: {se.msg}. Kagua mabano au try/except blocks!"
            }
        except Exception as e:
            return {"status": "error", "message": f"⚠️ Internal Engine Exception: {str(e)}"}

if __name__ == "__main__":
    # Test local execution execution
    auditor = OurworthlinksCodeAuditor("app.py")
    report = auditor.zindua_ukaguzi_wa_kibiashara("Ourworthlinks Internal Suite")
    print(json.dumps(report, indent=4) if "json" in sys.modules else report)
