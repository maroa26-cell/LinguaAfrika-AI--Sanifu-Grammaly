import os
import json
import ast
import re
import time
import sys

class OurworthlinksOmniCognitiveAuditor:
    def __init__(self, filename="app.py"):
        self.filename = filename
        self.ledger_file = "fault_history.json"
        self.billing_rate_per_audit = 0.05  # Ada ya SaaS ya $0.05 kwa kila audit ya makampuni mengine ya B2B
        self.mifumo_iliyosajiliwa = []
        self.kumbukumbu_ya_makosa = self.pakia_kumbukumbu_kamili()
        
        # 📚 DATABASE YA SHERIA ZA MIFUMO YA KIWANDA (COMPLIANCE MATRIX INTERCEPT)
        self.sheria_za_mifumo = {
            "streamlit": {
                "mitego": [
                    (r"key\s*=\s*['\"][a-zA-Z0-9_]*['\"]", "Duplicate Widget ID Danger: Kagua vitufe vyote viwe na keys za kipekee (v11, v12) kuzuia crash."),
                    (r"st\.secrets", "Secrets Dashboard Guard: Hakikisha funguo zote za siri zinasomwa kutoka Secrets Dashboard na sio ghafi kwenye kodi.")
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
                    (r"sk-[a-zA-Z0-9]{32,}", "🛑 CRITICAL SECURITY LEAK: Ufunguo ghafi wa OpenAI umepatikana ndoni ya kodi! Futa sekunde hii na uuhamishie kwenye Secrets Dashboard.")
                ]
            }
        }

    def pakia_kumbukumbu_kamili(self):
        """🧠 LONG-TERM PERSISTENT MEMORY MODULE: Inasoma na kutunza makosa yote yaliyopita ya mradi wetu na ya dunia"""
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Msingi wa kumbukumbu uliodaka makosa yetu ya ndani na ya jumuiya ya kimataifa ya wahandisi (Open-Source Logs)
        kumbukumbu_msingi = {
            "OWL-001": {"kosa": "IndentationError", "tathmini": "Spaces na tabs zimeingiliana kwenye Kamusi.", "suluhisho": "Kunyoosha kwa spaces 4 mlangoni."},
            "OWL-002": {"kosa": "SyntaxError_Monolith", "tathmini": "Kufungia kila kitu ndani ya try block moja.", "suluhisho": "Kusimika atomic sandbox handlers."},
            "GLOBAL-001": {"kosa": "StreamlitDuplicateElementId", "tathmini": "Kutumia jina linalofanana la radio element.", "suluhisho": "Kuongeza toleo la siri (key='radio_v12')."},
            "GLOBAL-002": {"kosa": "ModuleNotFoundError", "tathmini": "Kusahau kuandika neno la siri la library kwenye requirements.txt.", "suluhisho": "Ongeza jina la library kule requirements.txt."}
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(kumbukumbu_msingi, f, indent=4)
        return kumbukumbu_msingi

    def sajili_mifumo_ya_mradi(self, orodha_mifumo):
        """📋 FRAMEWORK REGISTRY LAYER: Mhandisi au AI anasajili mifumo atakayotumia katika mradi kabla ya chujio kuanza"""
        self.mifumo_iliyosajiliwa = [m.lower().strip() for m in orodha_mifumo]

    def jifunze_kutoka_kwa_wengine(self, kosa_la_nje, tathmini_ya_nje, suluhisho_la_nje):
        """💾 EXPERENTIAL COGNITIVE LEARNING LOOP: Kusoma makosa ya watengenezaji wengine duniani na kujifunza walivyorekebisha"""
        id_mpya = f"LEARNED-{int(time.time())}"
        self.kumbukumbu_ya_makosa[id_mpya] = {
            "kosa": kosa_la_nje,
            "tathmini": tathmini_ya_nje,
            "suluhisho": suluhisho_la_nje,
            "chanzo": "Global Open-Source Community Log Engine (Dunia)"
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(self.kumbukumbu_ya_makosa, f, indent=4)

    def kagua_na_ujifunze_mradi_kitalaalamu(self, jina_la_faili="app.py", anza_tathmini=True, b2b_client="Ourworthlinks Internal Core"):
        """🔮 PRE-FLIGHT COMPLIANCE COMPILER (THE MASTER GAETKEEPER): Inasoma, inachuja, na kutoa mapendekezo ya ushindi"""
        muda_mwanzo = time.time()
        
        if not os.path.exists(jina_la_faili):
            return {"status": "error", "message": f"Faili la {jina_la_faili} halipatikani kwenye diski ya repo!"}
            
        with open(jina_la_faili, "r", encoding="utf-8") as f:
            kodi_ghafi = f.read()

        mapungufu_ya_sheria = []
        # 1. Ukaguzi wa Sheria za Kiofisi za Mifumo Iliyosajiliwa (Cross-Framework Validation)
        for mfumo in self.mifumo_iliyosajiliwa:
            if mfumo in self.sheria_za_mifumo:
                for pattern, onyo in self.sheria_za_mifumo[mfumo]["mitego"]:
                    if re.search(pattern, kodi_ghafi):
                        mapungufu_ya_sheria.append(f"[{mfumo.upper()} COMPLIANCE] {onyo}")

        try:
            # 2. Ukaguzi wa kisintaksia wa Python AST Compiler Gate
            ast.parse(kodi_ghafi, filename=jina_la_faili)
            kasi_ya_radi = (time.time() - muda_mwanzo) * 1000
            status = "🟢 PASSED" if not mapungufu_ya_sheria else "⚠️ COMPLIANCE WARNING"
            msg = "Kodi ipo safi na imenyooka kiofisi!" if not mapungufu_ya_sheria else "🛑 TAHADHARI: Kodi haina kosa la spaces lakini inakiuka sheria za usalama za mifumo!"
            
            return {
                "status": status,
                "project_audit": "Ourworthlinks Automated Omni-Cognitive Auditor SaaS",
                "b2b_client": b2b_client,
                "mifumo_iliyokaguliwa": self.mifumo_iliyosajiliwa,
                "sheria_zilizokiukwa": mapungufu_ya_sheria if mapungufu_ya_sheria else "🟢 100% Flawless Compliance!",
                "metrics": {
                    "latency_ms": f"{kasi_ya_radi:.3f}ms",
                    "billing_accrued_usd": f"${self.billing_rate_per_audit:.2f}"
                },
                "ripoti_ya_ubongo": msg
            }
        except (IndentationError, SyntaxError) as err:
            sura = "IndentationError" if isinstance(err, IndentationError) else "SyntaxError"
            
            # Tafuta kama kosa hili lina suluhisho lililopo tayari kwenye kumbukumbu ya makosa yaliyopita
            ushauri_wa_kihistoria = "Kagua rula ya spaces 4."
            for k, v in self.kumbukumbu_ya_makosa.items():
                if v["kosa"] == sura:
                    ushauri_wa_kihistoria = v["suluhisho"]

            return {
                "status": "🛑 COMPILATION FAILED",
                "error_type": sura,
                "line_error": err.lineno,
                "ujumbe_wa_compiler": err.msg,
                "mapendekezo_ya_ushindi": ushauari_wa_kihistoria if anza_tathmini else "Mteja alikataa ripoti ya ushauri wa chujio."
            }

if __name__ == "__main__":
    # Test local execution execution
    auditor = OurworthlinksOmniCognitiveAuditor("app.py")
    auditor.sajili_mifumo_ya_mradi(["Streamlit", "Pesapal", "OpenAI"])
    # Mfano: Inasoma na kujifunza makosa ya watu wengine mtandaoni kiofisi hapa papo hapo
    auditor.jifunze_kutoka_kwa_wengine("TimeoutError", "API ya kibenki kuchelewa kujibu mtandao ukiwa chini.", "Kufungia kitufe ndani ya st.spinner ya sekunde 5.")
    print(json.dumps(auditor.kagua_na_ujifunze_mradi_kitalaalamu("app.py", anza_tathmini=True), indent=4))
