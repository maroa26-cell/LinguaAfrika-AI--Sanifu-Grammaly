#!/usr/bin/env python3
"""api_server.py — API ya AI Lingual kwa kiendelezi cha Chrome ("Grammarly ya Kiswahili").

Inatumia injini ile ile ya app yako: mhariri.kagua + CerebralCortex (Gemini -> Groq -> OpenAI).
Haina kifurushi cha ziada: ni seva ya kawaida ya Python (http.server).

Siri (environment variables) zinazohitajika kwenye seva:
  LINGUAL_API_KEYS   funguo za kiendelezi, zikitenganishwa kwa koma (mfano: ufunguo1,ufunguo2)
  GEMINI_API_KEY / GROQ_API_KEY / OPENAI_API_KEY   (angalau moja)
Hiari: PORT, LINGUAL_LIMIT_DAKIKA (20), LINGUAL_LIMIT_SIKU (400), LINGUAL_MAX_CHARS (3000)

Faragha: seva HAIHIFADHI wala HAIANDIKI maandishi ya watumiaji kwenye logi.
"""
import hmac
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import lingual_core

MAX_BODY_BYTES = 30_000


def tengeneza_seva(anwani, kagua, kategoria, funguo, kikomo=None, akiba=None,
                   max_chars=3000, wakati_mmoja=4):
    """Tengeneza seva. `kagua(text)` hurudisha dict kama mhariri.kagua; `funguo` ni seti ya funguo halali."""
    kikomo = kikomo or lingual_core.KikomoCha()
    akiba = akiba if akiba is not None else lingual_core.Akiba()
    ruhusa = threading.BoundedSemaphore(wakati_mmoja)
    funguo = [f for f in funguo if f]

    class Mshughulikiaji(BaseHTTPRequestHandler):
        server_version = "AILingual/0.1"

        def _tuma(self, kodi, data, vichwa=None):
            mwili = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(kodi)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(mwili)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            for k, v in (vichwa or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(mwili)

        def log_message(self, fmt, *args):  # usiandike maandishi; njia tu
            sys.stderr.write("[ai-lingual] %s\n" % (fmt % args))

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Max-Age", "86400")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            if self.path.split("?")[0] in ("/", "/health"):
                self._tuma(200, {"ok": True, "huduma": "AI Lingual"})
            else:
                self._tuma(404, {"ok": False, "kosa": "HAIPO"})

        def _ufunguo_halali(self):
            alioutuma = (self.headers.get("X-API-Key") or "").strip()
            for f in funguo:
                if hmac.compare_digest(alioutuma.encode(), f.encode()):
                    return alioutuma
            return None

        def do_POST(self):
            if self.path.split("?")[0] != "/v1/kagua":
                return self._tuma(404, {"ok": False, "kosa": "HAIPO"})
            if not funguo:
                return self._tuma(503, {"ok": False, "kosa": "SEVA_HAIJAWEKWA"})
            ufunguo = self._ufunguo_halali()
            if not ufunguo:
                return self._tuma(401, {"ok": False, "kosa": "UFUNGUO_SIO_SAHIHI"})
            try:
                urefu = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                urefu = -1
            if urefu <= 0 or urefu > MAX_BODY_BYTES:
                return self._tuma(413, {"ok": False, "kosa": "MWILI_MKUBWA_AU_TUPU"})
            try:
                data = json.loads(self.rfile.read(urefu).decode("utf-8"))
                text = data.get("text")
                if not isinstance(text, str):
                    raise ValueError
            except Exception:
                return self._tuma(400, {"ok": False, "kosa": "JSON_SIO_SAHIHI"})
            if len(text) > max_chars:
                return self._tuma(413, {"ok": False, "kosa": "MAANDISHI_MAREFU", "kikomo": max_chars})
            if not text.strip():
                return self._tuma(200, {"ok": True, "ai": False, "issues": []})

            ok, subiri = kikomo.ruhusu(ufunguo)
            if not ok:
                return self._tuma(429, {"ok": False, "kosa": "LIMIT", "subiri_sekunde": subiri},
                                  {"Retry-After": str(subiri)})

            jibu = akiba.pata(text)
            if jibu is None:
                if not ruhusa.acquire(timeout=20):
                    return self._tuma(503, {"ok": False, "kosa": "SEVA_IMEJAA"})
                try:
                    matokeo = kagua(text)
                    jibu = {"ok": True, "ai": bool(matokeo.get("ai_imetumika")),
                            "issues": lingual_core.tengeneza_matatizo(text, matokeo, kategoria)}
                except Exception as e:
                    sys.stderr.write("[ai-lingual] hitilafu ya ukaguzi: %s\n" % type(e).__name__)
                    return self._tuma(500, {"ok": False, "kosa": "UKAGUZI_UMESHINDWA"})
                finally:
                    ruhusa.release()
                if jibu["ai"]:  # usihifadhi matokeo ya msingi (AI ikishindwa) ili AI ijaribiwe tena
                    akiba.weka(text, jibu)
            self._tuma(200, jibu)

    return ThreadingHTTPServer(anwani, Mshughulikiaji)


def _jenga_kagua():
    """Unganisha injini halisi ya app (mhariri + CerebralCortex)."""
    import cerebral_cortex
    import mhariri
    try:
        from openai import OpenAI
    except Exception:
        OpenAI = None
    ufunguo_oai = (os.environ.get("OPENAI_API_KEY") or "").strip()
    mteja = OpenAI(api_key=ufunguo_oai) if (OpenAI and ufunguo_oai) else None
    ubongo = cerebral_cortex.CerebralCortex(mteja)
    if not (ubongo.gemini_client or ubongo.groq_client or ubongo.openai_client):
        raise RuntimeError("Weka angalau ufunguo mmoja: GEMINI_API_KEY, GROQ_API_KEY au OPENAI_API_KEY.")
    kina = ubongo.piga_json_kina if getattr(ubongo, "gemini_pro_modeli", "") else None
    return (lambda text: mhariri.kagua(text, piga_ai=ubongo.piga_json, piga_ai_kina=kina)), getattr(mhariri, "KATEGORIA", {})


def main():
    funguo = [k.strip() for k in os.environ.get("LINGUAL_API_KEYS", "").split(",") if k.strip()]
    if not funguo:
        sys.exit("Weka LINGUAL_API_KEYS (funguo za kiendelezi, zikitenganishwa kwa koma).")
    kagua, kategoria = _jenga_kagua()
    port = int(os.environ.get("PORT", "8000"))
    kikomo = lingual_core.KikomoCha(int(os.environ.get("LINGUAL_LIMIT_DAKIKA", "20")),
                                    int(os.environ.get("LINGUAL_LIMIT_SIKU", "400")))
    seva = tengeneza_seva(("0.0.0.0", port), kagua, kategoria, funguo, kikomo,
                          max_chars=int(os.environ.get("LINGUAL_MAX_CHARS", "3000")))
    print(f"AI Lingual API inasikiliza kwenye port {port}")
    seva.serve_forever()


if __name__ == "__main__":
    main()
