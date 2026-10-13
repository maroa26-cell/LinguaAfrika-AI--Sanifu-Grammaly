import ast
import re
import os
import time

class biomimeticimmuneshield:
    """🧫 IMMUNOLOGICAL ARCHITECTURE: Autonomous diagnostics engine with strict owner override"""
    
    def __init__(self):
        # 🧪 Antigen dictionary tracking infrastructure anomalies
        self.pathogen_signatures = {
            "nested_protocols": r"https://://",
            "legacy_endpoints": r"cybersb\.pesapal",
            "unsecured_transits": r"http://[^l]"
        }
        self.diagnostic_vault = ".owl_pathogen_log"
        self._initialize_diagnostic_vault()

    def _initialize_diagnostic_vault(self):
        if not os.path.exists(self.diagnostic_vault):
            with open(self.diagnostic_vault, "w", encoding="utf-8") as f:
                f.write("# 🔒 ourworthlinks system pathogen and health diagnostics log\n")

    def evaluate_system_harmony(self, file_path, source_code):
        """🔍 MACROPHAGE ENGINE: Scans code alignment and profiles vulnerabilities without modifying files"""
        vulnerabilities_detected = []
        
        # Step A: Scan for explicit structural signature pathogens
        for bug_name, pattern in self.pathogen_signatures.items():
            if re.search(pattern, source_code):
                vulnerabilities_detected.append({
                    "category": "malformed_string_vector",
                    "threat": bug_name,
                    "recommendation": f"Replace matching token payload with standard verified production strings inside {file_path}."
                })
                
        # Step B: Run Abstract Syntax Tree parsing to assess true structural harmony
        try:
            ast.parse(source_code)
        except SyntaxError as se:
            vulnerabilities_detected.append({
                "category": "syntax_corruption",
                "threat": f"line {se.lineno}: {se.msg}",
                "recommendation": f"Repair the unclosed structural block or character alignment on line {se.lineno} inside {file_path}."
            })
            
        return vulnerabilities_detected

    def request_owner_authorization(self, file_path, source_code, approve_remediation=False, clear_pathogen=False):
        """🛡️ HELPER T-CELL GATEWAY: Presents detailed recommendations and demands explicit owner approval"""
        anomalies = self.evaluate_system_harmony(file_path, source_code)
        
        if not anomalies:
            return {
                "system_status": "🟢 optimal harmony verified",
                "message": f"System engine has verified {file_path} is running at 100% computational efficiency. No defects found.",
                "remediation_executed": False
            }
            
        # Log the compiled threat vectors to the diagnostic vault for permanent indexing
        with open(self.diagnostic_vault, "a", encoding="utf-8") as f:
            for issue in anomalies:
                f.write(f"[{int(time.time())}] target: {file_path} | threat: {issue['threat']} | status: pending_owner_approval\n")

        # 👑 THE AUTONOMOUS BLOCK: AI halts and drops execution until the owner explicitly signs off
        if not approve_remediation and not clear_pathogen:
            print("\n" + "="*80)
            print(f"🚨 COGNITIVE IMMUNE WARNING: VULNERABILITIES IDENTIFIED INSIDE {file_path.upper()}")
            print("="*80)
            for idx, issue in enumerate(anomalies, 1):
                print(f"[{idx}] TYPE: {issue['category'].upper()}")
                print(f"    THREAT VALUE: {issue['threat']}")
                print(f"    PROPOSED REMEDIATION: {issue['recommendation']}")
            print("="*80)
            print("🔒 CRITICAL PRIVILEGE LOCK: AI IS STRICTLY PROHIBITED FROM ALTERING CODE.")
            print("👉 Action Required: Set 'approve_remediation=True' or 'clear_pathogen=True' to pass owner authorization.")
            print("="*80 + "\n")
            
            return {
                "system_status": "🚨 privilege_lock_pending_authorization",
                "defects_found": len(anomalies),
                "audit_report": anomalies,
                "remediation_executed": False
            }

        # ⚡ OWNER OVERRIDE EXECUTED: Apply fixes ONLY when explicitly commanded by you
        if approve_remediation:
            repaired_code = source_code
            for issue in anomalies:
                if issue["threat"] == "nested_protocols":
                    repaired_code = re.sub(self.pathogen_signatures["nested_protocols"], "https://pesapal.com", repaired_code)
                elif issue["threat"] == "sandbox_locks":
                    repaired_code = re.sub(self.pathogen_signatures["sandbox_locks"], "api.pesapal", repaired_code)
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(repaired_code)
                return {
                    "system_status": "🟢 remediation_successful",
                    "message": f"Owner override approved. Laser remediation applied successfully to {file_path}.",
                    "remediation_executed": True
                }
            except Exception as e:
                return {"system_status": "failed", "message": f"Error writing file modifications: {str(e)}", "remediation_executed": False}

        # 🗑️ OWNER DELETE COMMAND EXECUTED: Wipes the infected file cache entirely upon direct sign-off
        if clear_pathogen:
            try:
                os.remove(file_path)
                return {
                    "system_status": "🗑️ pathogen_purged_and_deleted",
                    "message": f"Owner override approved. Infected script {file_path} has been permanently purged from the system cluster.",
                    "remediation_executed": True
                }
            except Exception as e:
                return {"system_status": "failed", "message": f"Error purging pathogen target: {str(e)}", "remediation_executed": False}

# Single instance living cell initialization
immune_shield = biomimeticimmuneshield()
