"""
sheria_baada_ya_ai.py  (v2)
Sheria za kurekebisha Kiswahili baada ya AI kutoa jibu (Lingual Africa Sanifu).

Inatumiwa na api_server.py (v3.4+): kiendelezi cha Chrome na tovuti hupata marekebisho
haya kupitia /v1/kagua, /hariri na /pendekezo.

Mabadiliko v2:
- _JE inashika pia sentensi zenye nukuu zilizolindwa ([[NUKUU_n]] ina tarakimu)
- bila_nukuu(): kutambua kipande kilicho na nukuu tupu
- sheria za "bwana shamba/afya" zimehamishwa kwenye _MAKOSA_ZA_MAJARIBIO; zinawashwa
  kwa SHERIA_ZA_MAJARIBIO=1 tu, hadi uzithibitishe kwenye Kamusi ya BAKITA/TUKI
"""
import os
import re

# ---------------------------------------------------------------------------
# 1. ULINZI WA NUKUU
# ---------------------------------------------------------------------------
_NUKUU = re.compile(r'"[^"\n]*"|“[^”\n]*”')
_ALAMA = re.compile(r"\[\[\s*NUKUU_(\d+)\s*\]\]")


def linda_nukuu_kabla_ya_ai(maandishi_asili: str):
    """Inatoa nukuu na kuweka alama [[NUKUU_n]] kabla ya kutuma kwa AI."""
    hifadhi = []

    def weka(m):
        hifadhi.append(m.group(0))
        return f"[[NUKUU_{len(hifadhi) - 1}]]"

    return _NUKUU.sub(weka, maandishi_asili), hifadhi


def nukuu_zote_zipo(matokeo_ya_ai: str, nukuu: list) -> bool:
    """Hakiki kama alama zote zimerudi (hakuna iliyopotea, kurudiwa au kuongezwa)."""
    zilizopo = sorted(int(n) for n in _ALAMA.findall(matokeo_ya_ai))
    return zilizopo == list(range(len(nukuu)))


def rudisha_nukuu(maandishi: str, nukuu: list) -> str:
    """Inarudisha nukuu mahali pake (inavumilia nafasi ndani ya alama)."""
    return _ALAMA.sub(
        lambda m: nukuu[int(m.group(1))] if int(m.group(1)) < len(nukuu) else m.group(0),
        maandishi,
    )


def bila_nukuu(maandishi: str) -> str:
    """Maandishi bila alama za nukuu (kuangalia kama kuna kitu cha kuhariri nje ya nukuu)."""
    return _ALAMA.sub("", maandishi)


# ---------------------------------------------------------------------------
# 2. SHERIA ZENYEWE
# ---------------------------------------------------------------------------
def _linda_herufi_kubwa(asili: str, mpya: str) -> str:
    return mpya[:1].upper() + mpya[1:] if asili[:1].isupper() else mpya


# (a) Uakifishaji: "Je, ..." huisha na "?"
#     Haigusi sentensi zenye tarakimu (mf. 2.5) wala kuvuka mistari;
#     inaruhusu alama za nukuu zilizolindwa ([[NUKUU_0]]).
_JE = re.compile(r"(\bJe,(?:\[\[NUKUU_\d+\]\]|[^.?!\n\d])+)\.(?=\s|$)", re.IGNORECASE)

# (b) Sintaksia: "hii sekta" -> "sekta hii"
_VIONYESHI = r"(?:hii|huyu|hiki|hili|huu|hawa|hizi|hivi|haya)"
_NOMINO = (
    r"(?:aya|sekta|nyumba|kitabu|mtu|watu|jambo|mambo|swali|maswali|"
    r"mfumo|mifumo|kazi|nchi|siku|wakati|huduma|"
    r"elimu|uchumi|ajira|serikali|fursa|jamii|biashara|changamoto|tatizo|"
    r"mradi|miradi|taarifa)"
)
_KIONYESHI_KWANZA = re.compile(
    rf"\b({_VIONYESHI})[ \t]+({_NOMINO})\b", re.IGNORECASE
)


def _geuza_kionyeshi(m):
    kionyeshi, nomino = m.group(1).lower(), m.group(2).lower()
    if m.group(1)[:1].isupper():
        nomino = nomino.capitalize()
    return f"{nomino} {kionyeshi}"


# (c) Makosa ya tahajia/ngeli/nomino ambatani. Sheria maalum kwanza.
_MAKOSA = [
    (r"\bmyingi\b", "mingi"),
    (r"\bmwana[ \t]+inchi\b", "mwananchi"),
    (r"\bwana[ \t]+inchi\b", "wananchi"),
    (r"\binchi\b", "nchi"),
    # Sentensi mahususi pekee. Sheria pana ya "faili za" -> "mafaili ya" imeondolewa
    # kwa sababu inavunja mwafaka wa kisarufi.
    (
        r"\bfaili[ \t]+za[ \t]+wagonjwa[ \t]+zilikuwa[ \t]+zikipotea\b",
        "mafaili ya wagonjwa yalikuwa yakipotea",
    ),
]

# Hazijathibitishwa kwenye kamusi: ziko ZIMA kwa chaguo-msingi.
# Ziwashe kwa SHERIA_ZA_MAJARIBIO=1 ukishazithibitisha (BAKITA/TUKI).
_MAKOSA_ZA_MAJARIBIO = [
    (r"\bmabwana[ \t]+shamba\b", "mabwanashamba"),
    (r"\bbwana[ \t]+shamba\b", "bwanashamba"),
    (r"\bmabwana[ \t]+afya\b", "mabwanaafya"),
    (r"\bbwana[ \t]+afya\b", "bwanaafya"),
]

_orodha = list(_MAKOSA)
if os.environ.get("SHERIA_ZA_MAJARIBIO", "0") == "1":
    _orodha = _MAKOSA_ZA_MAJARIBIO + _orodha
_MAKOSA_ILIYOANDALIWA = [(re.compile(k, re.IGNORECASE), v) for k, v in _orodha]


def rekebisha_kiswahili_sanifu(matokeo_ya_ai: str, nukuu: list = None):
    """
    Inarudisha (maandishi_safi, orodha_ya_mabadiliko). Nukuu (ikiwa zimetolewa)
    zinarudishwa mahali pake mwishoni, bila kuguswa na sheria yoyote.
    """
    nukuu = nukuu or []
    mabadiliko = []
    m = matokeo_ya_ai

    def tumia(jina, regex, badilisha):
        nonlocal m
        mpya, n = regex.subn(badilisha, m)
        if n:
            mabadiliko.append((jina, n))
        m = mpya

    tumia("Je -> ?", _JE, r"\1?")
    tumia("kionyeshi baada ya nomino", _KIONYESHI_KWANZA, _geuza_kionyeshi)
    for regex, sahihi in _MAKOSA_ILIYOANDALIWA:
        tumia(
            regex.pattern,
            regex,
            lambda mm, s=sahihi: _linda_herufi_kubwa(mm.group(0), s),
        )

    return rudisha_nukuu(m, nukuu), mabadiliko


# ---------------------------------------------------------------------------
# 3. MTIRIRIKO KAMILI (hiari, kwa matumizi nje ya api_server.py)
# ---------------------------------------------------------------------------
def sanifisha(maandishi: str, piga_ai, lugha_lengwa: str = "sw", jaribio_la_juu: int = 2):
    """
    piga_ai(maandishi_yenye_alama) -> str   (kazi yako ya Gemini/Groq/OpenAI)
    Sheria hizi zinatumika TU kama lugha_lengwa == "sw".
    """
    if lugha_lengwa != "sw":
        return piga_ai(maandishi), []

    ulinzi, nukuu = linda_nukuu_kabla_ya_ai(maandishi)
    jibu = ""
    for _ in range(jaribio_la_juu):
        jibu = piga_ai(ulinzi)  # prompt iseme: "Usibadilishe alama [[NUKUU_n]]"
        if nukuu_zote_zipo(jibu, nukuu):
            break
    else:
        return maandishi, [("AI imepoteza nukuu - maandishi asili yamerudishwa", 1)]

    return rekebisha_kiswahili_sanifu(jibu, nukuu)


if __name__ == "__main__":
    asili = 'Wakulima hulima "siku moja moja". Je, hii sekta ina wana inchi wengi.'
    ulinzi, nk = linda_nukuu_kabla_ya_ai(asili)
    print(rekebisha_kiswahili_sanifu(ulinzi, nk))
