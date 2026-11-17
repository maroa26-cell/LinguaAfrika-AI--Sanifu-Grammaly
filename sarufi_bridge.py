"""
sarufi_bridge.py — kiunganishi cha BAKITA (kanuni_ya_sarufi.py) ndani ya mhariri.kagua().

Lengo: ukaguzi wa awali wa tafsiri (kwenye app.py) utumie kanuni 16 za BAKITA
(ngeli, Yambiwa, ukanushi, 'akina', 'Pale … -po-', n.k.) KABLA ya AI.

API:
  kagua_pamoja(maandishi, piga_ai=None, piga_ai_kina=None, lugha="Kiswahili")
    -> dict ile ile ya mhariri.kagua: {"issues": [...], "ai_imetumika": bool,
       "ai_kosa": str|None, "kina_imetumika": bool, "kina_kosa": str|None,
       "yaliyokataliwa": list, "mwelekeo": "ltr"|"rtl", "onyo_la_lugha": str|None}

Mbinu: mhariri.unganisha() hutumika kuunganisha BAKITA na matokeo ya mhariri,
hivyo makosa yanayopishana huondolewa na namba za id hupangwa upya.
"""

import logging
from typing import Optional

import kanuni_ya_sarufi as _ksr
import mhariri as _mhariri

logger = logging.getLogger(__name__)

# Ramani ya aina ya Kosa la BAKITA -> kodi ya mhariri.KATEGORIA.
# mhariri.KATEGORIA = {tahajia, sarufi, uakifishaji, mtindo}.
RAMANI_YA_KATEGORIA = {
    "NGELI":      "sarufi",
    "MOFOLOJIA":  "sarufi",
    "UPATANISHO": "sarufi",
    "SINTAKSIA":  "sarufi",
    "TAHAJIA":    "tahajia",
    "TAWALI":     "uakifishaji",
    "MTINDO":     "mtindo",
    "MSAMIATI":   "mtindo",
}

_mkaguzi = None


def _pata_mkaguzi():
    global _mkaguzi
    if _mkaguzi is None:
        _mkaguzi = _ksr.MkaguziSarufi()
    return _mkaguzi


def _kosa_kwenda_issue(k) -> Optional[dict]:
    """Geuza Kosa la BAKITA -> issue ya mhariri. None kama halina pendekezo."""
    if not getattr(k, "mapendekezo", None):
        return None
    pendekezo = k.mapendekezo[0]
    if not pendekezo or pendekezo == k.neno:
        return None
    return {
        "id": 0,
        "start": k.nafasi,
        "end": k.nafasi + k.urefu,
        "original": k.neno,
        "suggestion": pendekezo,
        "category": RAMANI_YA_KATEGORIA.get(k.aina, "sarufi"),
        "explanation": f"[BAKITA] {k.ujumbe}",
        "source": "kanuni",
        "uhakika": "juu",
    }


def kagua_pamoja(maandishi: str, piga_ai=None, piga_ai_kina=None,
                 lugha: str = "Kiswahili") -> dict:
    """
    Kagua kwa BAKITA + mhariri (kanuni + AI + uthibitisho wa Pro).
    Hurudisha dict ile ile ya mhariri.kagua, isipokuwa 'issues' zimeunganishwa
    na kanuni za BAKITA. Kama mhariri.kagua inashindwa, BAKITA bado inarudi.
    """
    bakita_issues = []
    if maandishi and maandishi.strip():
        try:
            makosa = _pata_mkaguzi().kagua(maandishi)
        except Exception as e:
            logger.warning("[sarufi_bridge] BAKITA imeshindwa: %s: %s",
                           type(e).__name__, str(e)[:200])
            makosa = []
        for k in makosa:
            it = _kosa_kwenda_issue(k)
            if it:
                bakita_issues.append(it)

    try:
        matokeo = _mhariri.kagua(maandishi, piga_ai=piga_ai,
                                 piga_ai_kina=piga_ai_kina, lugha=lugha)
    except Exception as e:
        logger.warning("[sarufi_bridge] mhariri.kagua imeshindwa: %s: %s",
                       type(e).__name__, str(e)[:200])
        matokeo = {
            "issues": [], "ai_imetumika": False,
            "ai_kosa": f"{type(e).__name__}: {e}",
            "kina_imetumika": False, "kina_kosa": None, "yaliyokataliwa": [],
            "lugha": lugha, "mwelekeo": "ltr", "onyo_la_lugha": None,
        }

    try:
        matokeo["issues"] = _mhariri.unganisha(matokeo.get("issues") or [], bakita_issues)
    except Exception as e:
        logger.warning("[sarufi_bridge] unganisha imeshindwa: %s: %s",
                       type(e).__name__, str(e)[:200])
        matokeo["issues"] = (matokeo.get("issues") or []) + bakita_issues
    return matokeo
