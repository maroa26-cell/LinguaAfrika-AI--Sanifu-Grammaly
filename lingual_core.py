"""lingual_core.py — mantiki safi ya API ya AI Lingual (hakuna mtandao, rahisi kujaribu)."""
import collections
import hashlib
import threading
import time


def urefu_utf16(s: str) -> int:
    """Urefu kwa vipimo vya UTF-16 (kama JavaScript), ili emoji zisivuruge nafasi za maneno."""
    return len(s.encode("utf-16-le")) // 2


def _ni_neno_kamili(text: str, pos: int, mwisho: int) -> bool:
    """Kosa lisilingane ndani ya neno refu zaidi (mfano 'shule' ndani ya 'shuleni')."""
    asili = text[pos:mwisho]
    if asili[:1].isalnum() and pos > 0 and text[pos - 1].isalnum():
        return False
    if asili[-1:].isalnum() and mwisho < len(text) and text[mwisho].isalnum():
        return False
    return True


def _tafuta(text: str, asili: str, yaliyochukuliwa: list) -> int:
    pos = text.find(asili)
    while pos != -1:
        mwisho = pos + len(asili)
        if _ni_neno_kamili(text, pos, mwisho) and not any(pos < e and mwisho > s for s, e in yaliyochukuliwa):
            return pos
        pos = text.find(asili, pos + 1)
    return -1


def tengeneza_matatizo(text: str, matokeo: dict, kategoria: dict = None) -> list:
    """Geuza matokeo ya mhariri.kagua kuwa orodha yenye nafasi (start/end) ambazo kiendelezi kinaweza kutumia."""
    kategoria = kategoria or {}
    yaliyochukuliwa = []  # (start, end) kwa vipimo vya herufi za Python, kuzuia kuingiliana
    matatizo = []
    for x in (matokeo or {}).get("issues", []) or []:
        asili = str(x.get("original") or "")
        pendekezo = str(x.get("suggestion") or "")
        if not asili or asili == pendekezo:
            continue
        st, en = x.get("start"), x.get("end")
        if (isinstance(st, int) and isinstance(en, int) and text[st:en] == asili
                and not any(st < e and en > s for s, e in yaliyochukuliwa)):
            pos = st                      # nafasi zilizotolewa na mhariri zinaaminika
        else:
            pos = _tafuta(text, asili, yaliyochukuliwa)
        if pos == -1:
            continue
        yaliyochukuliwa.append((pos, pos + len(asili)))
        kat = str(x.get("category") or "")
        try:
            lebo = kategoria.get(kat, ("Mengineyo", ""))[0]
        except Exception:
            lebo = "Mengineyo"
        anza = urefu_utf16(text[:pos])
        matatizo.append({
            "id": str(x.get("id", len(matatizo) + 1)),
            "start": anza,
            "end": anza + urefu_utf16(asili),
            "original": asili,
            "suggestion": pendekezo,
            "category": kat,
            "label": lebo,
            "explanation": str(x.get("explanation") or ""),
        })
    matatizo.sort(key=lambda m: m["start"])
    return matatizo


class KikomoCha:
    """Kikomo cha maombi kwa kila ufunguo: kwa dakika na kwa siku (kumbukumbu ya seva tu)."""

    def __init__(self, kwa_dakika=20, kwa_siku=400):
        self.kwa_dakika, self.kwa_siku = kwa_dakika, kwa_siku
        self._dakika = collections.defaultdict(collections.deque)
        self._siku = {}
        self._k = threading.Lock()

    def ruhusu(self, ufunguo: str, sasa: float = None):
        """Rudisha (True, 0) au (False, sekunde_za_kusubiri)."""
        sasa = time.time() if sasa is None else sasa
        siku = int(sasa // 86400)
        with self._k:
            d = self._dakika[ufunguo]
            while d and sasa - d[0] >= 60:
                d.popleft()
            if len(d) >= self.kwa_dakika:
                return False, max(1, int(60 - (sasa - d[0])) + 1)
            s_siku, idadi = self._siku.get(ufunguo, (siku, 0))
            if s_siku != siku:
                idadi = 0
            if idadi >= self.kwa_siku:
                return False, int(86400 - (sasa % 86400)) + 1
            d.append(sasa)
            self._siku[ufunguo] = (siku, idadi + 1)
            return True, 0


class Akiba:
    """LRU ndogo: maandishi yale yale hayarudii kutumia AI (kuokoa salio)."""

    def __init__(self, ukubwa=256, maisha=3600):
        self.ukubwa, self.maisha = ukubwa, maisha
        self._d = collections.OrderedDict()
        self._k = threading.Lock()

    @staticmethod
    def _ufunguo(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def pata(self, text, sasa=None):
        sasa = time.time() if sasa is None else sasa
        k = self._ufunguo(text)
        with self._k:
            v = self._d.get(k)
            if not v or sasa - v[0] > self.maisha:
                self._d.pop(k, None)
                return None
            self._d.move_to_end(k)
            return v[1]

    def weka(self, text, thamani, sasa=None):
        sasa = time.time() if sasa is None else sasa
        with self._k:
            self._d[self._ufunguo(text)] = (sasa, thamani)
            while len(self._d) > self.ukubwa:
                self._d.popitem(last=False)
