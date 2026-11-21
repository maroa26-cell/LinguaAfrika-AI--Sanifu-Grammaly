"""
sheria_baada_ya_ai.py
Sheria za kurekebisha Kiswahili baada ya AI kutoa jibu (Lingual Africa Sanifu).

Weka faili hii pamoja na kanuni_ya_sarufi.py, kisha iite kutoka cerebral_cortex.py
au app.py. Zinatumika TU pale lugha lengwa ni Kiswahili.
"""
import re

# ---------------------------------------------------------------------------
# 1. ULINZI WA NUKUU
# ---------------------------------------------------------------------------
# Inashika nukuu za kawaida "..." na za kimaandishi “...”
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
    """Hakiki kama AI imerudisha alama zote (na hakuna iliyopotea/kuongezwa)."""
    zilizopo = sorted(int(n) for n in _ALAMA.findall(matokeo_ya_ai))
    return zilizopo == list(range(len(nukuu)))


def rudisha_nukuu(maandishi: str, nukuu: list) -> str:
    """Inarudisha nukuu mahali pake (inavumilia nafasi ndani ya alama)."""
    return _ALAMA.sub(
        lambda m: nukuu[int(m.group(1))] if int(m.group(1)) < len(nukuu) else m.group(0),
        maandishi,
    )


# ---------------------------------------------------------------------------
# 2. SHERIA ZENYEWE
# ---------------------------------------------------------------------------
def _linda_herufi_kubwa(asili: str, mpya: str) -> str:
    return mpya[:1].upper() + mpya[1:] if asili[:1].isupper() else mpya


# (a) Uakifishaji: "Je, ..." huisha na "?"
#     Haigusi sentensi zenye tarakimu (mf. 2.5) wala kuvuka mistari.
_JE = re.compile(r"(\bJe,[^.?!\n\d]+)\.(?=\s|$)", re.IGNORECASE)

# (b) Sintaksia: "hii sekta" -> "sekta hii"
_VIONYESHI = r"(?:hii|huyu|hiki|hili|huu|hawa|hizi|hivi|haya)"
_NOMINO = (
    r"(?:aya|sekta|nyumba|kitabu|mtu|watu|jambo|mambo|swali|maswali|"
    r"mfumo|mifumo|kazi|nchi|siku|wakati|huduma)"
)
_KIONYESHI_KWANZA = re.compile(
    rf"\b({_VIONYESHI})[ \t]+({_NOMINO})\b", re.IGNORECASE
)


def _geuza_kionyeshi(m):
    kionyeshi, nomino = m.group(1).lower(), m.group(2).lower()
    if m.group(1)[:1].isupper():
        nomino = nomino.capitalize()
    return f"{nomino} {kionyeshi}"


# (c) Makosa ya tahajia/ngeli/nomino ambatani. Mpangilio ni muhimu:
#     sheria maalum kwanza. Kila moja inahifadhi herufi kubwa ya mwanzo.
#     TAHADHARI: thibitisha maneno ya "bwana..." kwenye Kamusi ya BAKITA/TUKI
#     kabla ya kuyaachia kwa wateja.
_MAKOSA = [
    (r"\bmyingi\b", "mingi"),
    (r"\bmabwana[ \t]+shamba\b", "mabwanashamba"),
    (r"\bbwana[ \t]+shamba\b", "bwanashamba"),
    (r"\bmabwana[ \t]+afya\b", "mabwanaafya"),
    (r"\bbwana[ \t]+afya\b", "bwanaafya"),
    (r"\bmwana[ \t]+inchi\b", "mwananchi"),
    (r"\bwana[ \t]+inchi\b", "wananchi"),
    (r"\binchi\b", "nchi"),
    # Sentensi mahususi pekee. Sheria pana ya "faili za" -> "mafaili ya"
    # imeondolewa kwa sababu inavunja mwafaka wa kisarufi
    # (mf. "faili za wagonjwa zilizopotea" -> "mafaili ya wagonjwa zilizopotea").
    (
        r"\bfaili[ \t]+za[ \t]+wagonjwa[ \t]+zilikuwa[ \t]+zikipotea\b",
        "mafaili ya wagonjwa yalikuwa yakipotea",
    ),
]
_MAKOSA_ILIYOANDALIWA = [(re.compile(k, re.IGNORECASE), v) for k, v in _MAKOSA]


def rekebisha_kiswahili_sanifu(matokeo_ya_ai: str, nukuu: list = None):
    """
    Inarudisha (maandishi_safi, orodha_ya_mabadiliko).
    Orodha ya mabadiliko inafaa kuonyeshwa kwa mtumiaji / kuhifadhiwa kwenye logi.
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
# 3. MTIRIRIKO KAMILI (hiari): linda -> AI -> hakiki -> rekebisha
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
        # AI imepoteza alama: tumia maandishi asili badala ya kupoteza nukuu
        return maandishi, [("AI imepoteza nukuu - maandishi asili yamerudishwa", 1)]

    return rekebisha_kiswahili_sanifu(jibu, nukuu)


if __name__ == "__main__":
    asili = 'Wakulima hulima "siku moja moja". Je, hii sekta ina mabwana shamba myingi.'
    ulinzi, nk = linda_nukuu_kabla_ya_ai(asili)
    print(rekebisha_kiswahili_sanifu(ulinzi, nk))
