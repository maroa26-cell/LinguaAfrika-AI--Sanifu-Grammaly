
#!/usr/bin/env python3
"""api_server.py — API ya AI Lingual kwa kiendelezi cha Chrome ("Grammarly ya Kiswahili").

Toleo 2.0 (marekebisho ya ukaguzi):
- Structured logging: kila ombi linaandikwa na request_id, method, path, status,
  dur_ms. HAKUNA maandishi ya mtumiaji kwenye logi (faragha).
- Request ID: UUID kwa kila ombi, inatumwa kwenye X-Request-ID na kwenye
  sehemu ya 'request_id' ya majibu ya makosa (kwa msaada wa kesi).
- Security headers: X-Content-Type-Options: nosniff, Cache-Control: no-store.
- Content-Type validation: 415 kwa maombi yasiyo JSON.
- Dynamic body limit: takriban 4 * max_chars + 1024 bytes (UTF-8 + JSON overhead).
- Graceful shutdown: SIGINT/SIGTERM -> seva.shutdown() kutoka thread tofauti.
- Health endpoint: ina toleo na uptime.
- HTTP/1.1 keep-alive: performance bora kwa fetch() ya Chrome extension.
- BrokenPipeError handling: client akikatiza, seva haianguki.

Siri (environment variables) zinazohitajika kwenye seva:
  LINGUAL_API_KEYS   funguo za kiendelezi, zikitenganishwa kwa koma
  GEMINI_API_KEY / GROQ_API_KEY / OPENAI_API_KEY   (angalau moja)
Hiari: PORT, LINGUAL_LIMIT_DAKIKA (20), LINGUAL_LIMIT_SIKU (400), LINGUAL_MAX_CHARS (3000),
  LINGUAL_TAFSIRI_DAKIKA (6), LINGUAL_TAFSIRI_SIKU (120), LINGUAL_TAFSIRI_MAX_CHARS (2000),
  LINGUAL_TAFSIRI=0 kuzima, LOG_LEVEL (INFO)

Njia:
  POST /v1/kagua    ukaguzi wa makosa ya Kiswahili (kiendelezi cha Chrome)
  POST /v1/tafsiri  tafsiri kwa mnyororo wa AI: rasimu -> mhariri mkuu -> uhakiki
  GET  /health      afya ya seva (toleo, uptime)
  GET  /            sawa na /health
"""
import hmac
import json
import logging
import os
import signal
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import lingual_core

log = logging.getLogger("ai-lingual")

VERSION = "0.2.0"
_STARTED = time.time()


def tengeneza_seva(anwani, kagua, kategoria, funguo, kikomo=None, akiba=None,
                   max_chars=3000, wakati_mmoja=4, tafsiri=None, kikomo_tafsiri=None,
                   max_chars_tafsiri=2000):
    """Tengeneza seva. `kagua(text)` hurudisha dict kama mhariri.kagua; `funguo` ni seti ya funguo halali.
    `tafsiri(text, chanzo, lengo, muktadha)` (hiari) hurudisha dict kama CerebralCortex.chakata_tafsiri_kamili."""
    kikomo = kikomo or lingual_core.KikomoCha()
    akiba = akiba if akiba is not None else lingual_core.Akiba()
    ruhusa = threading.BoundedSemaphore(wakati_mmoja)
    kikomo_tafsiri = kikomo_tafsiri or lingual_core.KikomoCha(6, 120)
    akiba_tafsiri = lingual_core.Akiba(128)
    ruhusa_tafsiri = threading.BoundedSemaphore(2)
    funguo = [f for f in funguo if f]

    # v2.0: kikomo cha mwili kinatokana na max_chars (UTF-8 worst case: 4 bytes/char + JSON overhead).
    MAX_BODY_KAGUA = max_chars * 4 + 1024
    MAX_BODY_TAFSIRI = max_chars_tafsiri * 4 + 1024

    class Mshughulikiaji(BaseHTTPRequestHandler):
        server_version = f"AILingual/{VERSION}"
        # v2.0: HTTP/1.1 enable keep-alive — fetch() ya Chrome extension inatumia
        # muunganisho mmoja kwa maombi mengi. Tunatuma Content-Length kila mara,
        # kwa hiyo keep-alive ni salama.
        protocol_version = "HTTP/1.1"

        # ---- visaidizi vya maombi ----

        def _anza_ombi(self):
            """Weka request_id, saa ya kuanza, na kodi (kwa logging)."""
            self._rid = uuid.uuid4().hex[:12]
            self._t0 = time.perf_counter()
            self._kodi = 0

        def _maliza_ombi(self):
            """Andika mstari mmoja wa logi: hakuna maandishi ya mtumiaji."""
            dur_ms = int((time.perf_counter() - self._t0) * 1000) if hasattr(self, "_t0") else 0
            log.info(
                "req=%s method=%s path=%s status=%s dur_ms=%d",
                getattr(self, "_rid", "-"), self.command,
                self.path.split("?")[0], getattr(self, "_kodi", 0), dur_ms,
            )

        def _tuma(self, kodi, data, vichwa=None):
            self._kodi = kodi
            # v2.0: request_id kwenye majibu ya makosa (msaada wa kesi); mafanikio hayana.
            if kodi >= 400 and isinstance(data, dict) and "request_id" not in data:
                data = {**data, "request_id": self._rid}
            mwili = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(kodi)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(mwili)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            # v2.0: security + trace headers
            self.send_header("X-Request-ID", self._rid)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            for k, v in (vichwa or {}).items():
                self.send_header(k, v)
            self.end_headers()
            try:
                self.wfile.write(mwili)
            except (BrokenPipeError, ConnectionResetError):
                # v2.0: client akikatiza, usiangushe seva.
                pass

        def log_message(self, fmt, *args):
            # v2.0: BaseHTTPRequestHandler's default is noisy and would print user paths.
            # We log ourselves in _maliza_ombi.
            pass

        def _ufunguo_halali(self):
            alioutuma = (self.headers.get("X-API-Key") or "").strip()
            for f in funguo:
                if hmac.compare_digest(alioutuma.encode(), f.encode()):
                    return alioutuma
            return None

        def _content_type_sawa(self):
            """v2.0: reject non-JSON Content-Type with 415."""
            ct = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            return (not ct) or ct == "application/json"

        # ---- OPTIONS (CORS preflight) ----

        def do_OPTIONS(self):
            self._anza_ombi()
            try:
                self._kodi = 204
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Max-Age", "86400")
                self.send_header("X-Request-ID", self._rid)
                self.send_header("Content-Length", "0")
                self.end_headers()
            finally:
                self._maliza_ombi()

        # ---- GET ----

        def do_GET(self):
            self._anza_ombi()
            try:
                p = self.path.split("?")[0]
                if p in ("/", "/health"):
                    self._tuma(200, {
                        "ok": True,
                        "huduma": "AI Lingual",
                        "toleo": VERSION,
                        "uptime_s": int(time.time() - _STARTED),
                    })
                else:
                    self._tuma(404, {"ok": False, "kosa": "HAIPO"})
            finally:
                self._maliza_ombi()

        # ---- POST ----

        def do_POST(self):
            self._anza_ombi()
            try:
                self._post()
            finally:
                self._maliza_ombi()

        def _post(self):
            njia = self.path.split("?")[0]
            if njia not in ("/v1/kagua", "/v1/tafsiri"):
                return self._tuma(404, {"ok": False, "kosa": "HAIPO"})
            if njia == "/v1/tafsiri" and tafsiri is None:
                return self._tuma(404, {"ok": False, "kosa": "TAFSIRI_HAIJAWASHWA"})
            if not funguo:
                return self._tuma(503, {"ok": False, "kosa": "SEVA_HAIJAWEKWA"})
            if not self._content_type_sawa():
                return self._tuma(415, {"ok": False, "kosa": "CONTENT_TYPE_SIO_JSON"})

            ufunguo = self._ufunguo_halali()
            if not ufunguo:
                return self._tuma(401, {"ok": False, "kosa": "UFUNGUO_SIO_SAHIHI"})

            # v2.0: kikomo cha mwili kinategemea njia.
            kikomo_mwili = MAX_BODY_TAFSIRI if njia == "/v1/tafsiri" else MAX_BODY_KAGUA
            try:
                urefu = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                urefu = -1
            if urefu <= 0 or urefu > kikomo_mwili:
                return self._tuma(413, {"ok": False, "kosa": "MWILI_MKUBWA_AU_TUPU"})

            try:
                data = json.loads(self.rfile.read(urefu).decode("utf-8"))
                text = data.get("text")
                if not isinstance(text, str):
                    raise ValueError
            except Exception:
                return self._tuma(400, {"ok": False, "kosa": "JSON_SIO_SAHIHI"})

            if njia == "/v1/tafsiri":
                return self._tafsiri(ufunguo, data, text)
            return self._kagua(ufunguo, text)

        # ---- /v1/kagua ----

        def _kagua(self, ufunguo, text):
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
                    log.warning("kagua imeshindwa req=%s: %s: %s",
                                self._rid, type(e).__name__, str(e)[:120])
                    return self._tuma(500, {"ok": False, "kosa": "UKAGUZI_UMESHINDWA"})
                finally:
                    ruhusa.release()
                if jibu["ai"]:
                    akiba.weka(text, jibu)
            self._tuma(200, jibu)

        # ---- /v1/tafsiri ----

        def _tafsiri(self, ufunguo, data, text):
            if len(text) > max_chars_tafsiri:
                return self._tuma(413, {"ok": False, "kosa": "MAANDISHI_MAREFU",
                                        "kikomo": max_chars_tafsiri})
            chanzo = str(data.get("chanzo") or "Kiingereza").strip()[:40]
            lengo = str(data.get("lengo") or "Kiswahili").strip()[:40]
            muktadha = str(data.get("muktadha") or "Kawaida").strip()[:20]
            if not text.strip():
                return self._tuma(200, {"ok": True, "tafsiri": "", "hatua": [], "onyo": []})

            ok, subiri = kikomo_tafsiri.ruhusu(ufunguo)
            if not ok:
                return self._tuma(429, {"ok": False, "kosa": "LIMIT", "subiri_sekunde": subiri},
                                  {"Retry-After": str(subiri)})

            funguo_akiba = "\x00".join((text, chanzo, lengo, muktadha))
            jibu = akiba_tafsiri.pata(funguo_akiba)
            if jibu is None:
                if not ruhusa_tafsiri.acquire(timeout=30):
                    return self._tuma(503, {"ok": False, "kosa": "SEVA_IMEJAA"})
                try:
                    r = tafsiri(text, chanzo, lengo, muktadha)
                    jibu = {"ok": True, "tafsiri": r["tafsiri"], "rasimu": r.get("rasimu", ""),
                            "hatua": r.get("hatua", []), "onyo": r.get("onyo", []),
                            "makosa_yaliyobaki": r.get("makosa_yaliyobaki", 0),
                            "tofauti_za_namba": r.get("tofauti_za_namba", 0)}
                except Exception as e:
                    log.warning("tafsiri imeshindwa req=%s: %s: %s",
                                self._rid, type(e).__name__, str(e)[:120])
                    return self._tuma(500, {"ok": False, "kosa": "TAFSIRI_IMESHINDWA"})
                finally:
                    ruhusa_tafsiri.release()
                if not jibu["onyo"]:
                    akiba_tafsiri.weka(funguo_akiba, jibu)
            self._tuma(200, jibu)

    return ThreadingHTTPServer(anwani, Mshughulikiaji)


def _jenga_injini():
    """Unganisha injini halisi ya app (mhariri + CerebralCortex). Hurudisha (kagua, kategoria, tafsiri)."""
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
        raise RuntimeError(
            "Weka angalau ufunguo mmoja: GEMINI_API_KEY, GROQ_API_KEY au OPENAI_API_KEY."
        )
    kina = ubongo.piga_json_kina if getattr(ubongo, "gemini_pro_modeli", "") else None
    kagua = lambda text: mhariri.kagua(text, piga_ai=ubongo.piga_json, piga_ai_kina=kina)
    tafsiri = None
    if os.environ.get("LINGUAL_TAFSIRI", "1") != "0":
        tafsiri = ubongo.chakata_tafsiri_kamili
    return kagua, getattr(mhariri, "KATEGORIA", {}), tafsiri


def main():
    # v2.0: logging ya structured, inaweza kudhibitiwa kwa LOG_LEVEL.
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    funguo = [k.strip() for k in os.environ.get("LINGUAL_API_KEYS", "").split(",") if k.strip()]
    if not funguo:
        log.error("LINGUAL_API_KEYS haijawekwa (funguo za kiendelezi, zikitenganishwa kwa koma).")
        sys.exit("Hitilafu: weka LINGUAL_API_KEYS.")

    try:
        kagua, kategoria, tafsiri = _jenga_injini()
    except Exception as e:
        log.error("Imeshindwa kuwasha injini: %s: %s", type(e).__name__, str(e)[:200])
        sys.exit("Hitilafu: angalia funguo za API (GEMINI/GROQ/OPENAI).")

    port = int(os.environ.get("PORT", "8000"))
    kikomo = lingual_core.KikomoCha(
        int(os.environ.get("LINGUAL_LIMIT_DAKIKA", "20")),
        int(os.environ.get("LINGUAL_LIMIT_SIKU", "400")),
    )
    kikomo_tafsiri = lingual_core.KikomoCha(
        int(os.environ.get("LINGUAL_TAFSIRI_DAKIKA", "6")),
        int(os.environ.get("LINGUAL_TAFSIRI_SIKU", "120")),
    )
    seva = tengeneza_seva(
        ("0.0.0.0", port), kagua, kategoria, funguo, kikomo,
        max_chars=int(os.environ.get("LINGUAL_MAX_CHARS", "3000")),
        tafsiri=tafsiri, kikomo_tafsiri=kikomo_tafsiri,
        max_chars_tafsiri=int(os.environ.get("LINGUAL_TAFSIRI_MAX_CHARS", "2000")),
    )

    # v2.0: graceful shutdown kutoka signal yoyote (SIGINT = Ctrl-C, SIGTERM = docker/k8s).
    def _shutdown(sig, frame):
        log.info("signal %s imepokelewa; nafunga seva...", sig)
        # shutdown() huzuia hadi serve_forever() itoke; lazima iitwe kutoka thread tofauti.
        threading.Thread(target=seva.shutdown, daemon=True).start()

    for sig_name in ("SIGINT", "SIGTERM"):
        try:
            signal.signal(getattr(signal, sig_name), _shutdown)
        except (AttributeError, ValueError):
            pass  # SIGTERM haipo Windows; SIGINT si main thread

    log.info(
        "AI Lingual API v%s inasikiliza kwenye port %d (tafsiri=%s, kagua=%d, tafsiri_max=%d)",
        VERSION, port, "ndio" if tafsiri else "hapana",
        int(os.environ.get("LINGUAL_MAX_CHARS", "3000")),
        int(os.environ.get("LINGUAL_TAFSIRI_MAX_CHARS", "2000")),
    )
    try:
        seva.serve_forever()
    finally:
        seva.server_close()
        log.info("AI Lingual API imesimama.")


if __name__ == "__main__":
    main()
