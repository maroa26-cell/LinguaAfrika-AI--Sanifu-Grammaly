
import ast
import re
import os
import csv
import time
import sqlite3
from io import StringIO

import requests
import streamlit as str_platform


class owthssovereignautomaton:
    """🛡️ THE SOVEREIGN AUTOMATON

    Moduli moja (self-contained) inayounganisha:
      • Immune filter / chujio cha usalama (AST + pathogen signatures)
      • Waste cleanser (metabolic cleansing ya RAM na database)
      • Latency balancer (endocrine telemetry)
      • Dictionary Engine: kupakua kamusi.csv kutoka GitHub kwa
        utambuzi KAMILI wa makosa (401/403/404/timeout/parse/schema),
        bila kumeza makosa kimya.

    Imeundwa iwe portable: sehemu ya kamusi inategemea `requests` + stdlib
    pekee, na haipokei siri moja kwa moja — mwito hupitisha url/token,
    kwa hivyo inaweza kutumika tena/kuuzwa kwa mifumo mingine ya AI.
    """

    def __init__(self):
        # 🧪 Core security signatures from the original auditor framework
        self.pathogen_signatures = {
            "nested_protocols": r"https://://",
            "legacy_endpoints": r"cybersb\.pesapal",
            "unsecured_transits": r"http://[^l]",
        }
        self.diagnostic_vault = ".owths_immune_ledger.log"
        self.db_file = "ourworthlinks_data.db"
        self._initialize_vault()

    # ------------------------------------------------------------------ #
    #  Logging ya pamoja (sababu halisi, si kimya)                        #
    # ------------------------------------------------------------------ #
    def _initialize_vault(self):
        if not os.path.exists(self.diagnostic_vault):
            with open(self.diagnostic_vault, "w", encoding="utf-8") as f:
                f.write(
                    "# 🔒 owths integrated master security, filter, "
                    "and filtration diagnostics log\n"
                )

    def _log(self, ujumbe):
        """Andika tukio moja kwenye vault kwa muda-muhuri."""
        try:
            with open(self.diagnostic_vault, "a", encoding="utf-8") as f:
                f.write(f"[{int(time.time())}] {ujumbe}\n")
        except OSError as e:
            # Hata logging ikishindwa, tusimeze kimya — toa onyo stderr.
            print(f"[owths] imeshindwa kuandika log: {e}")

    # ------------------------------------------------------------------ #
    #  IMMUNE FILTER / CHUJIO                                             #
    # ------------------------------------------------------------------ #
    def zindua_ukaguzi_wa_chujio(self, file_path, source_code):
        """🔬 THE INTEGRATED CHUJIO: Deep AST syntax scan and threat profiling pass"""
        anomalies = []
        for bug_name, pattern in self.pathogen_signatures.items():
            if re.search(pattern, source_code):
                anomalies.append({
                    "engine": "owths_immune_filter",
                    "threat": bug_name,
                    "remediation": f"Replace matching malformed payload vector inside {file_path}.",
                })
        try:
            ast.parse(source_code)
        except SyntaxError as se:
            anomalies.append({
                "engine": "owths_syntax_phagocytosis",
                "threat": f"line {se.lineno}: {se.msg}",
                "remediation": f"Close unaligned string blocks or balance spacing on line {se.lineno} inside {file_path}.",
            })
        return anomalies

    def request_owner_authorization(self, file_path, source_code, approve_remediation=False):
        """👑 ADMINISTRATIVE OVERRIDE PRIVILEGE: Hard sandbox lock requiring owner sign-off"""
        threat_profile = self.zindua_ukaguzi_wa_chujio(file_path, source_code)
        if not threat_profile:
            return {"status": "🟢 stable_harmony", "code": source_code}

        for threat in threat_profile:
            self._log(
                f"target: {file_path} | virus: {threat['threat']} | state: authorization_locked"
            )

        if not approve_remediation:
            return {
                "status": "🔒 restriction_lock_active",
                "payload": threat_profile,
                "code": source_code,
            }

        repaired_code = source_code
        for threat in threat_profile:
            if threat["threat"] == "nested_protocols":
                repaired_code = re.sub(
                    self.pathogen_signatures["nested_protocols"], "https://pesapal.com", repaired_code
                )
            elif threat["threat"] == "legacy_endpoints":
                repaired_code = re.sub(
                    self.pathogen_signatures["legacy_endpoints"], "api.pesapal", repaired_code
                )

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(repaired_code)
            return {"status": "🟢 remediation_complete", "code": repaired_code}
        except OSError as e:
            # Sababu halisi (si 'failed' tupu)
            self._log(f"remediation_write_failed: {file_path} | reason: {e}")
            return {
                "status": "🔴 remediation_failed",
                "reason": f"write_error: {e}",
                "code": source_code,
            }

    # ------------------------------------------------------------------ #
    #  WASTE CLEANSER                                                     #
    # ------------------------------------------------------------------ #
    def execute_metabolic_cleansing(self):
        """🚽 THE RENAL EXCRETORY ENGINE: RAM sweep na database log drainage"""
        cleared_buffers = 0
        protected_keys = [
            "active_gateway",
            "member_username",
            "admin_logged_in",
            "v14_clean_portal_radio_gate",
        ]
        try:
            for memory_key in list(str_platform.session_state.keys()):
                if memory_key not in protected_keys:
                    del str_platform.session_state[memory_key]
                    cleared_buffers += 1
        except Exception as e:  # noqa: BLE001 - session_state inaweza isiwepo nje ya Streamlit
            self._log(f"session_cleanse_skipped: {e}")

        if os.path.exists(self.db_file):
            try:
                conn = sqlite3.connect(self.db_file, timeout=30.0, check_same_thread=False)
                cursor = conn.cursor()
                barrier_time = int(time.time()) - (48 * 3600)
                cursor.execute(
                    "DELETE FROM malipo_trans "
                    "WHERE status = 'pending' AND strftime('%s', muda) < ?",
                    (str(barrier_time),),
                )
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                # Sababu halisi ya kosa la database (si kimya)
                self._log(f"db_cleanse_failed: {e}")

        return cleared_buffers

    def coordinate_hormonal_balance(self, start_time):
        """⚡ THE CENTRAL ENDOCRINE NERVE: Balances traffic buffers kwa live telemetry"""
        self.execute_metabolic_cleansing()
        latency_metrics = (time.time() - start_time) * 1000
        if latency_metrics > 500.0:
            return (
                f"Resource usage spikes captured. Deep cache balancing protocols "
                f"activated. Latency: {latency_metrics:.2f}ms"
            )
        return f"Stable rhythm. Latency logged at {latency_metrics:.3f}ms"

    # ------------------------------------------------------------------ #
    #  DICTIONARY ENGINE: kupakua kamusi.csv kutoka GitHub               #
    #  Hurudisha (rows, None) ikifanikiwa au (None, kosa) ikishindwa.    #
    #  Kila kosa huwa na SABABU HALISI (si onyo la jumla).               #
    # ------------------------------------------------------------------ #
    def pakua_kamusi(self, csv_url, token, safu_zinazohitajika=None, muda_timeout=15):
        """Pakua na uchakate kamusi.csv.

        Args:
            csv_url: URL ya GitHub Contents API ya faili la CSV.
            token: GitHub PAT (github_pat_... au ghp_...).
            safu_zinazohitajika: seti ya majina ya safu lazima ziwepo
                (case-insensitive). None = usikague schema.
            muda_timeout: sekunde za kusubiri ombi.

        Returns:
            (list[dict], None) ikifanikiwa, au (None, "kundi: maelezo") ikishindwa.
        """
        # 1) Hakiki usanidi kabla ya ombi
        if not csv_url:
            return None, "config_error: KAMUSI_CSV_URL haijawekwa."
        if not token:
            return None, "config_error: token haijawekwa."
        if not token.startswith(("github_pat_", "ghp_")):
            return None, "config_error: Muundo wa token si sahihi (haianzi na github_pat_ au ghp_)."

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3.raw",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        # 2) Tuma ombi kwa usalama
        try:
            resp = requests.get(csv_url, headers=headers, timeout=muda_timeout)
        except requests.exceptions.Timeout:
            self._log("kamusi_fetch: network_error timeout")
            return None, "network_error: Muda wa ombi umeisha (timeout). Jaribu tena."
        except requests.exceptions.ConnectionError:
            self._log("kamusi_fetch: network_error connection")
            return None, "network_error: Imeshindwa kuunganisha na GitHub (angalia mtandao)."
        except requests.exceptions.RequestException as e:
            self._log(f"kamusi_fetch: request_error {e}")
            return None, f"network_error: Kosa la ombi: {e}"

        # 3) Tafsiri status code kwa SABABU HALISI
        status = resp.status_code
        if status == 401:
            self._log("kamusi_fetch: auth_error 401")
            return None, "auth_error (401): Token imekataliwa — imeisha muda au si sahihi. Tengeneza mpya."
        if status == 403:
            if resp.headers.get("X-RateLimit-Remaining") == "0":
                self._log("kamusi_fetch: rate_limit 403")
                return None, "rate_limit (403): Kikomo cha maombi kimefikiwa. Subiri kidogo."
            self._log("kamusi_fetch: permission_error 403")
            return None, "permission_error (403): Token haina ruhusa 'Contents: Read' kwa repo hii."
        if status == 404:
            self._log("kamusi_fetch: not_found 404")
            return None, "not_found (404): Faili/repo haipatikani — hakiki URL na jina la kamusi.csv."
        if status != 200:
            self._log(f"kamusi_fetch: http_error {status}")
            return None, f"http_error ({status}): Jibu lisilotarajiwa kutoka GitHub."

        # 4) Chakata CSV kwa usalama
        try:
            reader = csv.DictReader(StringIO(resp.text))
            rows = [
                {(k.strip().lower() if k else k): (v.strip() if isinstance(v, str) else v)
                 for k, v in row.items()}
                for row in reader
            ]
        except csv.Error as e:
            self._log(f"kamusi_fetch: parse_error {e}")
            return None, f"parse_error: Muundo wa CSV si sahihi: {e}"

        if not rows:
            self._log("kamusi_fetch: data_error empty")
            return None, "data_error: Kamusi imepakuliwa lakini haina safu zozote."

        # 5) Hakiki schema ikiombwa
        if safu_zinazohitajika:
            zilizopo = {k for k in rows[0].keys() if k}
            zinazokosekana = {s.lower() for s in safu_zinazohitajika} - zilizopo
            if zinazokosekana:
                self._log(f"kamusi_fetch: schema_error missing {zinazokosekana}")
                return None, (
                    "schema_error: Safu zinazokosekana kwenye CSV: "
                    + ", ".join(sorted(zinazokosekana))
                )

        return rows, None

    def tafuta_neno(self, neno, rows, safu_ya_neno="neno"):
        """Tafuta neno kwenye rows (case-insensitive). Hurudisha dict au None."""
        if not neno or not rows:
            return None
        lengo = neno.strip().lower()
        kiwango = safu_ya_neno.lower()
        for row in rows:
            thamani = row.get(kiwango)
            if isinstance(thamani, str) and thamani.strip().lower() == lengo:
                return row
        return None

    @staticmethod
    def ujumbe_rafiki_wa_kosa(kosa):
        """Badilisha kosa la kiufundi kuwa ujumbe rafiki kwa mtumiaji.

        Rudisha (kiwango, ujumbe) ambapo kiwango ni 'error'/'warning'/'success'.
        Tumia: kiwango, ujumbe = master_core.ujumbe_rafiki_wa_kosa(kosa)
        """
        if kosa is None:
            return "success", ""
        if kosa.startswith(("auth_error", "permission_error", "config_error", "schema_error")):
            return "error", "⚠️ Kamusi haipatikani kwa sababu ya tatizo la usanidi. Timu imearifiwa."
        if kosa.startswith("rate_limit"):
            return "warning", "⏳ Kuna msongamano kwa sasa. Tafadhali jaribu tena baada ya dakika chache."
        if kosa.startswith("network_error"):
            return "warning", "🌐 Tatizo la muunganisho. Tafadhali jaribu tena."
        if kosa.startswith("not_found"):
            return "error", "❓ Kamusi haikupatikana kwenye chanzo. Timu imearifiwa."
        return "error", "❌ Kamusi haipatikani kwa sasa. Tafadhali jaribu tena baadaye."


master_core = owthssovereignautomaton()
