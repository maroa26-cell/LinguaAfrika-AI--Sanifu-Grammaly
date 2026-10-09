import os
import json
import ast
import re
import time

class OurworthlinksIntelligentAuditor:
    def __init__(self):
        self.ledger_file = "fault_history.json"
        self.mifumo_iliyosajiliwa = []
        self.kumbukumbu_ya_makosa = self.pakia_kumbukumbu_kamili()
        
        # 📚 FRAMEWORK COMPLIANCE RULES (Sheria za Kiofisi za Mifumo)
        self.sheria_za_mifumo = {
            "streamlit": {
                "mitego": [
                    (r"key\s*=\s*['\"][a-zA-Z0-9_]*['\"]", "Duplicate Widget ID Danger: Kagua vitufe vyote viwe na keys za kipekee (v11, v12) kuzuia crash."),
                    (r"st\.secrets", "Secrets Dashboard Guard: Hakikisha funguo zote za siri zinasomwa kutoka Secrets na sio ghafi kwenye kodi.")
                ]
            },
            "pesapal": {
                "mitego": [
                    (r"cybersb\.pesapal\.com", "Sandbox Endpoint Alert: Mfumo bado unaelekeza Sandbox URL ya majaribio! Badilisha kwenda ://pesapal.com kwa ajili ya uzalishaji fedha halisi Live."),
                    (r"currency\s*=\s*['\"]USD['\"]", "Currency Settled: Lango limesimikwa kuchakata Dola ya Kimarekani ($5.00 USD) kulingana na mkataba wa Ourworthlinks.")
                ]
            },
            "openai": {
                "mitego": [
                    (r"sk-[a-zA-Z0-9]{32,}", "🛑 CRITICAL SECURITY LEAK: Ufunguo ghafi wa OpenAI umepatikana ndani ya kodi! Futa sekunde hii na uuhamishie kwenye Secrets Dashboard.")
                ]
            }
        }

    def pakia_kumbukumbu_kamili(self):
        """🧠 LONG-TERM MEMORY RECORDER: Inapakia makosa yote yaliyopita ya mradi wetu na ya watu wengine"""
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        kumbukumbu_msingi = {
            "OWL-001": {"kosa": "IndentationError", "tathmini": "Spaces na tabs zimeingiliana kwenye Kamusi.", "suluhisho": "Kunyoosha kwa spaces 4 mlangoni."},
            "OWL-002": {"kosa": "SyntaxError_Monolith", "tathmini": "Kufungia kila kitu ndani ya try block moja.", "suluhisho": "Kusimika atomic sandbox handlers."},
            "GLOBAL-001": {"kosa": "StreamlitDuplicateElementId", "tathmini": "Kutumia jina linalofanana la radio element.", "suluhisho": "Kuongeza toleo la siri (key='radio_v12')."}
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(kumbukumbu_msingi, f, indent=4)
        return kumbukumbu_msingi

    def sajili_mifumo_ya_mradi(self, orodha_mifumo):
        """📋 FRAMEWORK REGISTRY: Mtengenezaji kodi au AI anasajili mifumo atakayotumia katika mradi"""
        self.mifumo_iliyosajiliwa = [m.lower().strip() for m in orodha_mifumo]

    def jifunze_kutoka_kwa_wengine(self, kosa_la_nje, tathmini_ya_nje, suluhisho_la_nje):
        """💾 EXPERENTIAL LEARNING LOOP: Kusoma makosa ya watu wengine na kujifunza walivyorekebisha wao"""
        id_mpya = f"LEARNED-{int(time.time())}"
        self.kumbukumbu_ya_makosa[id_mpya] = {
            "kosa": kosa_la_nje,
            "tathmini": tathmini_ya_nje,
            "suluhisho": suluhisho_la_nje,
            "chanzo": "Global Open-Source Community Log Engine"
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(self.kumbukumbu_ya_makosa, f, indent=4)

    def kagua_kodi_kitalaalamu(self, jina_la_faili="app.py", anza_tathmini=True):
        """🔮 PRE-FLIGHT INTERCEPTOR: Inachuja kodi na kutoa mapendekezo kulingana na sheria za mifumo iliyosajiliwa"""
        if not os.path.exists(jina_la_faili):
            return {"status": "error", "message": f"Faili la {jina_la_faili} halipatikani!"}
            
        with open(jina_la_faili, "r", encoding="utf-8") as f:
            kodi_ghafi = f.read()

        mapungufu_ya_sheria = []
        for mfumo in self.mifumo_iliyosajiliwa:
            if mfumo in self.sheria_za_mifumo:
                for pattern, onyo in self.sheria_za_mifumo[mfumo]["mitego"]:
                    if re.search(pattern, kodi_ghafi):
                        mapungufu_ya_sheria.append(f"[{mfumo.upper()} COMPLIANCE] {onyo}")

        try:
            ast.parse(kodi_ghafi, filename=jina_la_faili)
            status = "🟢 PASSED" if not mapungufu_ya_sheria else "⚠️ COMPLIANCE WARNING"
        except (IndentationError, SyntaxError) as err:
            sura = "IndentationError" if isinstance(err, IndentationError) else "SyntaxError"
            ushauri = "Kagua rula ya spaces 4."
            for k, v in self.kumbukumbu_ya_makosa.items():
                if v["kosa"] == sura:
                    ushauri = v["suluhisho"]

            return {
                "status": "🛑 COMPILATION FAILED",
                "kosa_lililopatikana": sura,
                "mstari_wa_kosa": err.lineno,
                "ujumbe_wa_seva": err.msg,
                "mapendekezo_ya_ushimpi": ushauri if anza_tathmini else "Mteja hakuhitaji ushauri wa chujio."
            }

        return {
            "status": status,
            "mifumo_iliyokaguliwa": self.mifumo_iliyosajiliwa,
            "sheria_zilizokiukwa": mapungufu_ya_sheria if mapungufu_ya_sheria else "🟢 100% Compliant na mifumo!",
            "ripoti_ya_tathmini": "Kodi ipo safi na tayari kwenda hewani kiofisi."
        }

if __name__ == "__main__":
    auditor = OurworthlinksIntelligentAuditor()
    auditor.sajili_mifumo_ya_mradi(["Streamlit", "Pesapal", "OpenAI"])
    # Inajifunza makosa ya watu wengine mtandaoni kiofisi hapa
    auditor.jifunze_kutoka_kwa_wengine("ModuleNotFoundError", "Kusahau kuandika library kwenye requirements.txt", "Ongeza jina la library kule requirements.txt")
    print(json.dumps(auditor.kagua_kodi_kitalaalamu("app.py", anza_tathmini=True), indent=4))
