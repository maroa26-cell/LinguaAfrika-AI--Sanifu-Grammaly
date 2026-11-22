"""
sheria_baada_ya_ai.py  (v2.4)
Sheria za kurekebisha Kiswahili baada ya AI kutoa jibu (Lingual Africa Sanifu).

Inatumiwa na api_server.py (v3.4+): kiendelezi cha Chrome na tovuti hupata marekebisho
haya kupitia /v1/kagua, /hariri na /pendekezo.

Mabadiliko v2.4:
- "baba wengi" -> "akina baba wengi" (kama mama). "watoto wengi" haiguswi: "watoto" ni wingi tayari,
  kwa hiyo "akina" haitumiki.

Mabadiliko v2.3:
- "mama wengi" -> "akina mama wengi" (haiguswi ikiwa "akina" ipo tayari).
- "wakati/muda" + mingi/myingi/wengi/mengi... -> "wakati mwingi", "muda mwingi".

Mabadiliko v2.2:
- Sheria ya zamani "myingi" -> "mingi" imeondolewa: ilikuwa inabadilisha kila "myingi" bila
  kuangalia nomino ("wateja myingi" ikawa "wateja mingi", kosa jipya). Badala yake kuna sheria
  ya ngeli (_INGI_RX): kiambishi cha "-ingi" kinachaguliwa kwa nomino inayotangulia
  (wa- -> wengi, vi-/vy- -> vingi, ma- -> mengi, mi-/my- -> mingi, nomino za N -> nyingi).
  Nomino isiyotambulika haiguswi (inaachiwa AI).

Mabadiliko v2.1:
- Sheria pana ya "inchi" -> "nchi" imeondolewa, kwa sababu "inchi" pia ni kipimo
  (mf. "televisheni ya inchi 55"). Zimebaki sheria mahususi za "mwana inchi" na "wana inchi".

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


# (b2) Ngeli ya "-ingi": "wateja myingi" -> "wateja wengi", "vitu mingi" -> "vitu vingi".
#      Inashika tu "myingi"/"mingi" baada ya nomino inayotambulika kwa kiambishi chake.
#      Nomino isiyotambulika, au iliyo sahihi tayari, haiguswi.
_INGI_RX = re.compile(r"\b([^\W\d_]+)([ \t]+)(myingi|mingi)\b", re.IGNORECASE)
_NOMINO_ZA_N = {  # ngeli ya I-ZI (N): nyingi
    "biashara", "pesa", "nchi", "fursa", "changamoto", "huduma", "taarifa", "kazi", "siku",
    "sekta", "jamii", "shule", "familia", "habari", "faida", "hasara", "benki", "kampuni",
    "taasisi", "bidhaa", "sababu", "nafasi", "njia", "ndege", "ng'ombe", "mbuzi", "kuku",
}
_NOMINO_ZISIZO_NGELI_YAKE = {  # zinaanza na "wa" lakini si wingi wa watu
    "wakati", "wali", "wazo", "wasiwasi", "wanja", "wavu", "waya", "wadi",
}


def _ingi_kwa_ngeli(m):
    nomino, pengo, sasa = m.group(1).lower(), m.group(2), m.group(3)
    if nomino in _NOMINO_ZISIZO_NGELI_YAKE:
        return m.group(0)
    if nomino in _NOMINO_ZA_N:
        sahihi = "nyingi"
    elif nomino.startswith("wa"):
        sahihi = "wengi"
    elif nomino.startswith(("vi", "vy")):
        sahihi = "vingi"
    elif nomino.startswith("ma"):
        sahihi = "mengi"
    elif nomino.startswith(("mi", "my")):
        sahihi = "mingi"
    else:
        return m.group(0)
    if sahihi == sasa.lower():
        return m.group(0)
    return m.group(1) + pengo + _linda_herufi_kubwa(sasa, sahihi)


# (b3) Nahau: "mama/baba wengi" -> "akina mama/baba wengi" (haiguswi ikiwa "akina" ipo tayari).
_AKINA_MAMA_RX = re.compile(r"(?<![Aa]kina )\b(mama|baba)([ \t]+)(wengi)\b", re.IGNORECASE)


def _akina_mama(m):
    akina = "Akina" if m.group(1)[:1].isupper() else "akina"
    return f"{akina} {m.group(1).lower()}{m.group(2)}{m.group(3)}"


# (b4) "wakati mwingi", "muda mwingi" (si "wakati mingi", "muda mingi").
_MUDA_RX = re.compile(
    r"\b(wakati|muda)([ \t]+)(myingi|mingi|wengi|mengi|vingi|nyingi)\b", re.IGNORECASE
)


def _muda_mwingi(m):
    return m.group(1) + m.group(2) + _linda_herufi_kubwa(m.group(3), "mwingi")


# (c) Makosa ya tahajia/nomino ambatani. Sheria maalum kwanza.
#     ("myingi" -> "mingi" imeondolewa v2.2: ngeli inashughulikiwa na _INGI_RX hapo juu.)
_MAKOSA = [
    (r"\bmwana[ \t]+inchi\b", "mwananchi"),
    (r"\bwana[ \t]+inchi\b", "wananchi"),
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
    tumia("akina mama wengi", _AKINA_MAMA_RX, _akina_mama)
    tumia("wakati/muda mwingi", _MUDA_RX, _muda_mwingi)
    tumia("-ingi kwa ngeli", _INGI_RX, _ingi_kwa_ngeli)
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
