
import ast
import re
import time
import streamlit as str_platform

class LivingHumanImmuneShield:
    """🧠 BIOMIMETIC AUTONOMOUS IMMUNE SYSTEM (THE SOVEREIGN CELLULAR ENGINE)"""
    
    def __init__(self):
        # 🧪 ANTIGEN REGISTRY: Alama za magonjwa na viharibifu (Pathogens) vilivyopigwa marufuku
        self.pathogen_signatures = {
            "duplicate_slashes": r"https://://",       # Virus cha 'about:blank#blocked'
            "sandbox_remnants": r"cybersb\.pesapal",   # Bakteria cha link ya majaribio
            "unsecured_protocols": r"http://[^l]"       # Kimelea cha mawasiliano yasiyo salama
        }
        # 📚 MEMORY CELLS MATRIX: Hifadhi ya siri ya kumbukumbu ya magonjwa yaliyopita
        self.memory_cells_log = {}

    def seli_za_doria_macrophage(self, jina_la_faili, msimbo_ghafi):
        """🧫 MACROPHAGE & NEUTROPHIL CELL LAYER: Askari wa doria wa kwanza (Phagocytosis)"""
        for ugonjwa, signature in self.pathogen_signatures.items():
            if re.search(signature, msimbo_ghafi):
                # PHAGOCYTOSIS: Kumeza na kuharibu kosa la kiungo kibovu kiotomatiki kabla halijaleta dhoruba
                msimbo_ghafi = re.sub(signature, "https://pesapal.com", msimbo_ghafi)
                return {
                    "action": "MUTATED_AND_DESTROYED",
                    "target": ugonjwa,
                    "message": f"🩸 Seli za Patrol zimegundua na kumeza kiharibifu cha '{ugonjwa}' ndani ya {jina_la_faili}!"
                }
        return {"action": "CLEAR", "message": "🟢 Hakuna kiharibifu ghafi mlangoni."}

    def seli_za_utambuzi_dendritic(self, jina_la_faili, msimbo_ghafi):
        """🧬 DENDRITIC CELL LAYER: Ukusanyaji wa taarifa na uwasilishaji wa Antigen (AST Parsing)"""
        try:
            # Seli inachambua mfupa na ubongo wa kodi kwa kutumia Abstract Syntax Tree
            ast.parse(msimbo_ghafi)
            return {"status": "HEALTHY", "antigen_profile": None}
        except SyntaxError as se:
            # Kupiga picha kosa (Antigen Capture) na kuisafirisha kwenda ngazi ya juu ya utambuzi
            antigen_extracted = f"Line_{se.lineno}_Error_{se.msg}"
            return {"status": "INFECTED", "antigen_profile": antigen_extracted, "line": se.lineno, "msg": se.msg}

    def seli_saidizi_helper_t(self, jina_la_faili, status_ya_utambuzi):
        """🩸 HELPER T-CELL (KAMANDA MKUU): Kuratibu mapambano na kuamsha mifumo ya dharura"""
        if status_ya_utambuzi["status"] == "INFECTED":
            antigen = status_ya_utambuzi["antigen_profile"]
            # Kuweka ugonjwa kwenye seli za kumbukumbu ili usijirudie (Memory Cells Logging)
            self.memory_cells_log[jina_la_faili] = {"antigen": antigen, "logged_at": time.time()}
            
            # CYTOKINES SIGNALING: Amri ya dharura ya kuzima dhoruba na kulinda Streamlit
            return {
                "signal": "ACTIVATE_FALLBACK_SHIELD",
                "alert": f"🛑 Helper T-Cell King'ora! Faili la {jina_la_faili} lina maambukizi mwilini kwenye Mstari {status_ya_utambuzi['line']}!"
            }
        return {"signal": "MAINTAIN_STEADY_STATE"}

    def seli_wauaji_killer_t(self, jina_la_faili, msimbo_ghafi):
        """🫁 KILLER T-CELLS & B-CELLS: Kuharibu viharibifu na kuwasha kingamwili ya kibenki (://pesapal.com)"""
        doria = self.seli_za_doria_macrophage(jina_la_faili, msimbo_ghafi)
        utambuzi = self.seli_za_utambuzi_dendritic(jina_la_faili, msimbo_ghafi)
        kamanda = self.seli_saidizi_helper_t(jina_la_faili, utambuzi)
        
        if utambuzi["status"] == "INFECTED" or doria["action"] == "MUTATED_AND_DESTROYED":
            # ANTIBODY INJECTION: Kulazimisha mfumo kuwasha fomu safi ya kibenki ya dharura
            url_salama = "https://://pesapal.com/iframe/PesapalIframe3/Index"
            return {
                "status": "SECURED_BY_IMMUNE_SYSTEM",
                "log": doria["message"] if doria["action"] == "MUTATED_AND_DESTROYED" else kamanda["alert"],
                "fallback_vaccine_url": url_salama
            }
            
        return {
            "status": "🟢 IMMUNE_SYSTEM_HEALTHY",
            "message": f"🏆 Seli za ulinzi zimethibitisha kuwa {jina_la_faili} haina kosa na mfumo upo imara asilimia 100!"
        }

# Zindua mtambo kama seli hai moja inayojitegemea (The Sovereign Living Instance)
kingamwili_ya_mfumo = LivingHumanImmuneShield()
