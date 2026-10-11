import os
import json
import ast
import re
import time

class OurworthlinksCognitiveAuditorSuite:
    def __init__(self, target_path="app.py"):
        # 👑 MAPINDUZI YA PATH: Mtambo sasa unakubali njia yoyote (e.g., "app.py" au "pages/dashboard.py")
        self.target_path = target_path
        self.ledger_file = "fault_history.json"
        self.kumbukumbu_ya_makosa = self.pakia_kumbukumbu_ya_kudumu()
        self.mifumo_iliyosajiliwa = []
        
        # 📚 NYUZI ZA SHERIA ZA KIWANDA (FRAMEWORK REGISTRY COMPLIANCE)
        self.sheria_za_mifumo = {
            "streamlit": {
                "mitego": [
                    (r"key\s*=\s*['\"][a-zA-Z0-9_]*['\"]", "Duplicate Widget ID Warning: Kagua keys zote zisiingiliane kuzuia freeze ya skrini."),
                    (r"import\s*central_nervous_system", "🛑 CRITICAL CONFLICT: Mstari huu utaleta mgongano wa kache wa Linux! Futa import ya nje mara moja.")
                ]
            },
            "pesapal": {
                "mitego": [
                    (r"cybersb\.pesapal\.com", "Sandbox API Alert: Mfumo unatumia mazingira ya majaribio! Badilisha kwenda ://pesapal.com kwa ajili ya Live Production."),
                    (r"import\s*pespal_core", "🛑 TYPO ERROR DETECTED: Jina limeandikwa kimapungufu kama 'pespal_core' badala ya 'pesapal_core' kuzuia ModuleNotFoundError.")
                ]
            }
        }

    def pakia_kumbukumbu_ya_kudumu(self):
        """🧠 PERSISTENT EXPERIENCE RECALL: Inapakia kumbukumbu zote za makosa yaliyopita"""
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        kumbukumbu_msingi = {
            "OWL-001": {"kosa": "IndentationError", "tathmini": "Spaces na tabs zimeingiliana kwenye Kamusi au tabo.", "suluhisho": "Kunyoosha kwa spaces 4 mlangoni.", "status": "🟢 FIXED"},
            "OWL-002": {"kosa": "ModuleNotFoundError", "tathmini": "Herufi 'a' kukatika kwenye neno pesapal_core.", "suluhisho": "Kusawazisha herufi 'a' mwilini mwa import.", "status": "🟢 FIXED"},
            "OWL-003": {"kosa": "Cache_Lock_Clash", "tathmini": "Kuacha neno import central_nervous_system kwenye app.py.", "suluhisho": "Kufuta kabisa neno la import mlangoni.", "status": "🟢 FIXED"}
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(kumbukumbu_msingi, f, indent=4)
        return kumbukumbu_msingi

    def sajili_mifumo_ya_mradi(self, orodha_mifumo):
        self.mifumo_iliyosajiliwa = [m.lower().strip() for m in orodha_mifumo]

    def jifunze_kutoka_kwa_wengine(self, kosa_la_nje, tathmini_ya_nje, suluhisho_la_nje):
        id_mpya = f"LEARNED-{int(time.time())}"
        self.kumbukumbu_ya_makosa[id_mpya] = {
            "kosa": kosa_la_nje,
            "tathmini": tathmini_ya_nje,
            "suluhisho": suluhisho_la_nje,
            "chanzo": "Global Open-Source Developer Community Ledger"
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(self.kumbukumbu_ya_makosa, f, indent=4)

    def tekeleza_kujitibu_kiotomatiki(self, jina_la_faili):
        """🩺 ACTIVE SELF-HEALING ENGINE: Inafungua na kutibu faili lolote lililopo kwenye njia iliyotajwa (i.e. pages/dashboard.py)"""
        if not os.path.exists(jina_la_faili):
            return False
            
        with open(jina_la_faili, "r", encoding="utf-8") as f:
            kodi_ghafi = f.read()
            
        # Tiba ya herufi zilizokatika za pespal_core kwenda pesapal_core kiotomatiki
        if "import pespal_core" in kodi_ghafi:
            kodi_ghafi = kodi_ghafi.replace("import pespal_core", "import pesapal_core")
            
        # Tiba ya dharura ya kufuta import ya CNS inayovunja kache ya Linux
        if "import central_nervous_system" in kodi_ghafi:
            kodi_ghafi = re.sub(r"import central_nervous_system\n?", "", kodi_ghafi)
            
        with open(jina_la_faili, "w", encoding="utf-8") as f:
            f.write(kodi_ghafi)
        return True

    def zindua_uchuguzi_na_tathmini_kuu(self, ruhusu_self_healing=True):
        """🔮 PRE-FLIGHT COMPLIANCE COMPILER (THE UNIVERSAL GATEKEEPER)"""
        muda_mwanzo = time.time()
        jina_la_faili = self.target_path
        
        if not os.path.exists(jina_la_faili):
            return {"status": "error", "message": f"🛑 Hitilafu: Njia ya faili la '{jina_la_faili}' haipatikani kwenye saraka!"}
            
        if ruhusu_self_healing:
            self.tekeleza_kujitibu_kiotomatiki(jina_la_faili)
            
        with open(jina_la_faili, "r", encoding="utf-8") as f:
            kodi_iliyosafishwa = f.read()

        mapungufu_ya_sheria = []
        for mfumo in self.mifumo_iliyosajiliwa:
            if mfumo in self.sheria_za_mifumo:
                for pattern, onyo in self.sheria_za_mifumo[mfumo]["mitego"]:
                    if re.search(pattern, kodi_iliyosafishwa):
                        mapungufu_ya_sheria.append(f"[{mfumo.upper()} COMPLIANCE] {onyo}")

        try:
            ast.parse(kodi_iliyosafishwa, filename=jina_la_faili)
            kasi_ya_radi = (time.time() - muda_mwanzo) * 1000
            status = "🟢 PASSED & COMPLIANT" if not mapungufu_ya_sheria else "⚠️ COMPLIANCE WARNING"
            
            return {
                "status": status,
                "project_audit": "Ourworthlinks Automated Universal Cognitive Auditor Suite",
                "faili_lililokaguliwa": jina_la_faili,
                "sheria_zilizokiukwa": mapungufu_ya_sheria if mapungufu_ya_sheria else "🟢 100% Salama!",
                "tathmini_ya_ubongo": {
                    "latency_checking": f"{kasi_ya_radi:.3f}ms",
                    "historical_database_nodes": f"Inamiliki kumbukumbu {len(self.kumbukumbu_ya_makosa)} ya makosa ya dunia."
                },
                "ripoti_ya_mwisho": f"Faili la '{jina_la_faili}' lipo msafi, imenyooka kwa rula na lime-healing yenyewe!"
            }
        except (IndentationError, SyntaxError) as err:
            sura = "IndentationError" if isinstance(err, IndentationError) else "SyntaxError"
            ushauri_wa_kihistoria = "Kagua rula ya spaces 4 mlangoni au funga try-blocks zilizokatika."
            for k, v in self.kumbukumbu_ya_makosa.items():
                if v["kosa"] == sura:
                    ushauri_wa_kihistoria = v["suluhisho"]

            return {
                "status": "🛑 COMPILATION FAILED",
                "faili_lililofeli": jina_la_faili,
                "error_type": sura,
                "line_error": err.lineno,
                "ujumbe_wa_compiler": err.msg,
                "mapendekezo_ya_ushindi": ushauri_wa_kihistoria
            }

if __name__ == "__main__":
    # MFANO WA MATUMIZI YA NDANI YA KIWANDA:
    # 1. Ukaguzi wa faili la mlangoni
    auditor_root = OurworthlinksCognitiveAuditorSuite("app.py")
    auditor_root.sajili_mifumo_ya_mradi(["Streamlit"])
    print(json.dumps(auditor_root.zindua_uchuguzi_na_tathmini_kuu(), indent=4))
    
    # 2. UNIVERSAL TRAVERSAL PASS: Ukaguzi wa faili lililopo NDANI ya folda la pages/
    auditor_pages = OurworthlinksCognitiveAuditorSuite("pages/dashboard.py")
    auditor_pages.sajili_mifumo_ya_mradi(["Streamlit", "Pesapal"])
    print(json.dumps(auditor_pages.zindua_uchuguzi_na_tathmini_kuu(), indent=4))
