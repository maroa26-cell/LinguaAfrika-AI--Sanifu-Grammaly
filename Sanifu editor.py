"""
sanifu_editor.py - Mhariri wa AI Lingual Africa: lugha yoyote -> lugha yoyote

Toleo 2.1 (marekebisho ya ukaguzi):
- Timeout: piga_ai ina kikomo cha muda (sekunde 25). TimeoutAI -> mwitaji
  (for m in watoa) anajaribu mtoa anayefuata. Hakuna thread inayokwama.
- Logging: kagua_kwa_kanuni_za_bakita, _hatua_ya_mtafsiri na _kagua_kwa_ai
  zinaandika kila kosa kwenye logi (BILA maandishi ya mtumiaji).
- Usafi: _ni_sawa(jc, jl) is False imebadilishwa kuwa not _ni_sawa(jc, jl).
- Uaminifu: kagua_uaminifu inatumia ulinganisho wa herufi kwa lugha
  zisizo na nafasi (Kichina, Kijapani) badala ya kurudisha False kila mara.

Mtiririko:
  1. Anagram (M-A-L-U-W-I-M) hutatuliwa kwa kamusi, si kwa AI.
  2. AI (Gemini -> Groq -> OpenAI) huhariri kwa System Prompt kali.
  3. Vikagua vya kanuni hukamata makosa ambayo AI huyakosa:
     ngeli ya mahali (darasani yenye), marudio (kubwa kubwa), uaminifu (maneno yaliyodondoshwa).
  4. Jibu baya husababisha kuhamia mtoa huduma anayefuata.

Matumizi kwenye Streamlit:
    from sanifu_editor import hariri_kwa_ubora
    matokeo = hariri_kwa_ubora(maandishi, kamusi=KAMUSI_SET,
                               lugha_chanzo="Kiswahili", lugha_lengwa="Kiingereza")
    st.metric("Ubora wa matokeo", f"{matokeo['alama_ya_matokeo']}/100")
    st.write(matokeo["maandishi_sahihi"])
    for k in matokeo["marekebisho"]:
        st.write(k)

Funguo (st.secrets au environment variables):
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY
"""

import concurrent.futures
import json
import logging
import os
import re
import time
import unicodedata
from collections import Counter

from lugha_za_afrika import KISWAHILI, ni_kiswahili, onyo_la_lugha, pata_lugha

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Mipangilio
# ----------------------------------------------------------------------------

MPANGILIO_WA_WATOA_HUDUMA = ["gemini", "groq", "openai"]   # Gemini -> Groq -> OpenAI

HALI_ZA_AI = ("kawaida", "bure", "gemini_pekee")
WATOA_WA_HALI = {"kawaida": None, "bure": ["gemini", "groq"], "gemini_pekee": ["gemini"]}

KIKOMO_CHA_HERUFI_KWA_BURE = 12000
KUSUBIRI_BAADA_YA_KIKOMO = (2.0, 5.0)

# v2.1: kikomo cha muda kwa kila mwito wa piga_ai (mtoa mmoja kwa wakati).
# 25s inatosha kwa tafsiri ndefu; ikizidi, mwitaji anajaribu mtoa anayefuata.
SANIFU_TIMEOUT_S = 25.0

MODELI = {
    "gemini": "gemini-2.5-flash",
    "groq": "llama-3.3-70b-versatile",
    "openai": "gpt-4o-mini",
}


class TimeoutAI(RuntimeError):
    """AI haikujibu ndani ya muda uliotolewa (SANIFU_TIMEOUT_S)."""


# Executor mmoja wa module: threads zilizoachwa na timeout zinaendelea
# nyuma hadi SDK yake itakapomaliza; hazizuii mwitaji.
_EXECUTOR = concurrent.futures.ThreadPoolExecutor(
    max_workers=8, thread_name_prefix="sanifu"
)


SANIFU_SYSTEM_PROMPT = """
Wewe ni AI Lingual Sanifu, mhariri bingwa na mtaalamu wa sarufi ya Kiswahili Sanifu. Kazi yako ni kurekebisha tahajia, sarufi, mpangilio wa maneno, na alama za uandishi katika maandishi ya Kiswahili.

KANUNI KUU ZA UHARIRI:
1. MUUNDO WA SENTENSI (SVO): Hakikisha sentensi zinafuata mpangilio sahihi wa Kiima + Kitenzi + Shamirisho. Weka vihusishi (kama "kwa", "na", "katika") na vielezi mahali pake sahihi kisarufi. Vielezi vya namna, mahali na wakati huwekwa baada ya shamirisho. Viashiria hufuata nomino. Unapopanga upya sentensi, usibadilishe maana wala kuacha neno lolote.
2. ZUIA URUDIAJI WA MANENO: Kamwe usirudie neno au kifungu cha maneno bila sababu (mfano: epuka "kubwa kubwa" au kurudia shamirisho mara mbili). Marudio ya kisarufi ya kweli (polepole, kidogo kidogo) yabaki.
3. UPATANISHO WA NGELI: Hakiki upatanisho wa umoja na wingi kwa umakini. Nomino za wingi za ngeli ya I-ZI kama "Biashara ndogondogo" huchukua "zinachangia", si "inachangia". Neno la mahali lenye -ni (darasani, sokoni) halichukui "yenye/lenye": tumia "kwenye" ("darasani kwenye ...") au rudisha nomino bila -ni ("darasa lenye ...").
4. UHIFADHI WA TAARIFA: Usidondoshe wala kuondoa maneno muhimu, nomino, au vihusishi vilivyokuwepo kwenye maandishi ya awali. Tunza maana halisi ya mwandishi. Kabla ya kujibu, hakikisha kila nomino na kitenzi cha msingi cha awali bado kipo.
5. TAHAJIA NA HERUFI ZILIZOVURUGWA: Rekebisha makosa ya uandishi (mfano: "Serekali" kuwa "Serikali"). Kwa herufi zilizochanganywa (mfano M-A-L-U-W-I-M), panga upya herufi zilezile tu kupata neno halisi la Kiswahili; usibuni majina wala maneno yasiyotumia herufi zote. Usipopata jibu moja lenye uhakika, liache neno kama lilivyo.
6. ALAMA ZA UANDISHI: Tumia mkato (,), nukta (.), na nukta mkato (;) kwa usahihi. Usiweke mkato kabla ya kiunganishi "ili". Usitumie nukta mkato pale mkato unatosha (mfano "Ingawa mvua inanyesha sana leo, hatuwezi ...").

MIFANO YA MAREKEBISHO:
- "Darasani yenye idadi kubwa kubwa ya wanafunzi" -> "Darasa lenye idadi kubwa ya wanafunzi"
- "Biashara ndogondogo inachangia uchumi" -> "Biashara ndogondogo zinachangia uchumi"
- "kituoni kusafiri abiria walikuwa wakingoja basi" -> "abiria walikuwa wakingoja basi kituoni ili kusafiri"
- "Mvua kubwa sana jana ilinyesha" -> "Jana ilinyesha mvua kubwa sana"
- "katika huo mkutano" -> "katika mkutano huo"; "wenzake wanakijiji" -> "wanakijiji wenzake"
- "kujifunza haraka masomo yao" -> "kujifunza masomo yao haraka"

MUUNDO WA JIBU:
Toa JSON tu, bila maelezo mengine. Sehemu ya "maandishi_sahihi" ina maandishi yaliyorekebishwa PEKEE (bila utangulizi, maelezo wala orodha). Maelezo ya kila marekebisho yawekwe kwenye "marekebisho" pekee, na sababu iwe sahihi kisarufi:
{"maandishi_sahihi": "...",
 "marekebisho": [{"kabla": "", "baada": "", "aina": "", "sababu": ""}]}
"""

NGELI_YENYE = {
    "darasa": "lenye", "soko": "lenye", "shamba": "lenye", "jiji": "lenye",
    "shule": "yenye", "nyumba": "yenye", "barabara": "yenye", "kampuni": "yenye",
    "kitabu": "chenye", "kiti": "chenye", "kijiji": "chenye",
    "mji": "wenye", "mti": "wenye", "mkoa": "wenye",
    "mtu": "mwenye", "mwalimu": "mwenye",
}

MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara"}

NOMINO_ZENYE_NI_ZA_KAWAIDA = {
    "kampuni", "leseni", "televisheni", "nini", "ini", "jini", "kuni", "benki",
    "taasisi", "akaunti", "kiini", "mwanzoni",
}

try:
    from kanuni_ya_sarufi import KanuniZaSarufiKiswahili, MAELEKEZO_YA_LUGHA
    _KANUNI = KanuniZaSarufiKiswahili()
    SANIFU_SYSTEM_PROMPT = (
        SANIFU_SYSTEM_PROMPT
        + "\n\nKANUNI ZA ZIADA ZA KISWAHILI SANIFU (BAKITA):\n"
        + MAELEKEZO_YA_LUGHA["Kiswahili"]
    )
except Exception:
    _KANUNI = None

try:
    from kanuni_ya_sarufi import maelekezo_ya_jozi as _maelekezo_ya_jozi
except Exception:
    _maelekezo_ya_jozi = None


# ----------------------------------------------------------------------------
# Vikagua vya kanuni (hakuna AI)
# ----------------------------------------------------------------------------

def tatua_anagram(herufi, kamusi):
    """'M-A-L-U-W-I-M' -> ['mwalimu'] kwa kutumia kamusi."""
    ufunguo = "".join(sorted(herufi.lower().replace("-", "")))
    return [w for w in kamusi if "".join(sorted(w.lower())) == ufunguo]


def tatua_anagram_kwenye_maandishi(maandishi, kamusi):
    if not kamusi:
        return maandishi

    def badilisha(m):
        chaguo = tatua_anagram(m.group(0), kamusi)
        return chaguo[0] if len(chaguo) == 1 else m.group(0)

    return re.sub(r"\b(?:[A-Za-z]-){3,}[A-Za-z]\b", badilisha, maandishi)


def kagua_ngeli_mahali(maandishi):
    """Hukamata 'darasani yenye' (neno la mahali + kivumishi cha ngeli ya I-ZI/LI-YA n.k.)."""
    makosa = []
    for m in re.finditer(
        r"\b(\w+?)ni\s+(yenye|zenye|lenye|wenye|chenye|vyenye)\b", maandishi, re.IGNORECASE
    ):
        msingi = m.group(1).lower()
        if f"{msingi}ni" in NOMINO_ZENYE_NI_ZA_KAWAIDA:
            continue
        kiambishi = NGELI_YENYE.get(msingi, "lenye")
        herufi_kubwa = m.group(0)[0].isupper()
        baada = f"{msingi} {kiambishi}"
        mbadala = f"{msingi}ni kwenye"
        if herufi_kubwa:
            baada, mbadala = baada.capitalize(), mbadala.capitalize()
        makosa.append({
            "kabla": m.group(0),
            "baada": baada,
            "mbadala": mbadala,
            "aina": "Ngeli ya mahali (PA-KU-MU)",
            "sababu": f"'{msingi}ni' ni neno la mahali; halichukui '{m.group(2)}'. "
                      f"Tumia '{msingi} {kiambishi}' au '{msingi}ni kwenye'.",
            "span": m.span(),
        })
    return makosa


def tumia_marekebisho_ya_ngeli(maandishi):
    for k in sorted(kagua_ngeli_mahali(maandishi), key=lambda x: x["span"][0], reverse=True):
        a, b = k["span"]
        maandishi = maandishi[:a] + k["baada"] + maandishi[b:]
    return maandishi


def ondoa_marudio(maandishi):
    def badilisha(m):
        neno = m.group(1)
        return m.group(0) if neno.lower() in MARUDIO_HALALI else neno

    return re.sub(r"\b(\w+)(?:\s+\1\b)+", badilisha, maandishi, flags=re.IGNORECASE)


def kagua_marudio(maandishi):
    makosa = []
    for m in re.finditer(r"\b(\w+)(?:\s+\1\b)+", maandishi, re.IGNORECASE):
        if m.group(1).lower() not in MARUDIO_HALALI:
            makosa.append({
                "kabla": m.group(0), "baada": m.group(1),
                "aina": "Urudiaji wa neno",
                "sababu": f"Neno '{m.group(1)}' limerudiwa bila sababu.",
            })
    return makosa


def kagua_nukta_mkato(maandishi):
    return [{
        "kabla": m.group(0), "baada": m.group(0).replace(";", ","),
        "aina": "Alama za uandishi",
        "sababu": "Nukta mkato (;) imetumika pale koma (,) inatosha.",
    } for m in re.finditer(r"[^.;!?]*\b(?:Ingawa|Kwa kuwa|Kwa sababu)\b[^.;!?]*;", maandishi)]


def tumia_marekebisho_ya_nukta_mkato(maandishi):
    return re.sub(r"([^.;!?]*\b(?:Ingawa|Kwa kuwa|Kwa sababu)\b[^.;!?]*);", r"\1,", maandishi)


def kagua_mkato_kabla_ya_ili(maandishi):
    return [{
        "kabla": m.group(0), "baada": m.group(0).replace(",", "", 1),
        "aina": "Alama za uandishi",
        "sababu": "Mkato haiwekwi kabla ya kiunganishi 'ili'.",
    } for m in re.finditer(r"\w+,\s+ili\b", maandishi)]


def ondoa_mkato_kabla_ya_ili(maandishi):
    return re.sub(r"(\w+),(\s+ili\b)", r"\1\2", maandishi)


def kagua_uaminifu(asili, matokeo, kizingiti=0.75):
    """Hakikisha AI haikudondosha maneno ya msingi.
    v2.1: kwa lugha zisizo na nafasi (Kichina, Kijapani), tumia ulinganisho wa herufi
    badala ya kurudisha False kila mara (ambayo ilizuia uhariri wa Kichina kabisa)."""
    toka = lambda s: Counter(w for w in re.findall(r"\w+", s.lower()) if len(w) > 3)
    a, b = toka(asili), toka(matokeo)
    if a:
        jumla = sum(a.values()) or 1
        yaliyobaki = sum(min(a[w], b[w]) for w in a)
        if jumla < 12:
            kizingiti = min(kizingiti, 0.5)
        return yaliyobaki / jumla >= kizingiti
    # Hakuna maneno yanayogawanyika: tumia herufi (Kichina, Kijapani, n.k.)
    char_a = Counter(c for c in asili if c.isalnum())
    char_b = Counter(c for c in matokeo if c.isalnum())
    jumla = sum(char_a.values()) or 1
    yaliyobaki = sum(min(char_a[c], char_b[c]) for c in char_a)
    if jumla < 20:
        kizingiti = min(kizingiti, 0.5)
    return yaliyobaki / jumla >= kizingiti


def kagua_kwa_kanuni_za_bakita(maandishi):
    """Hutumia MkaguziSarufi (kanuni_ya_sarufi.py) kama inapatikana. Hurudisha orodha ya makosa."""
    if _KANUNI is None or not maandishi.strip():
        return []
    try:
        matokeo = _KANUNI.kagua_sentensi_nzima(maandishi, kagua_alama=False)
    except Exception as e:
        # v2.1: andika kosa (BILA maandishi) ili bug kwenye kanuni isifichwe.
        logger.warning("kagua_kwa_kanuni_za_bakita imeshindwa: %s: %s", type(e).__name__, str(e)[:120])
        return []
    return [{
        "kabla": k["neno"],
        "baada": (k["mapendekezo"] or [""])[0],
        "aina": k["aina"],
        "sababu": k["ujumbe"],
    } for k in matokeo["makosa"]]


def hesabu_alama(idadi_ya_makosa, idadi_ya_maneno):
    if idadi_ya_maneno == 0:
        return 100
    adhabu = (idadi_ya_makosa / idadi_ya_maneno) * 100 * 2.5
    return max(0, round(100 - adhabu))


# ----------------------------------------------------------------------------
# Watoa huduma wa AI
# ----------------------------------------------------------------------------

def _siri(jina):
    try:
        import streamlit as st
        if jina in st.secrets:
            return st.secrets[jina]
    except Exception:
        pass
    return os.environ.get(jina)


def _toa_json(maandishi):
    maandishi = re.sub(r"^```(?:json)?|```$", "", maandishi.strip(), flags=re.MULTILINE).strip()
    return json.loads(maandishi)


def _gemini(mfumo, maandishi, temperature):
    from google import genai
    from google.genai import types

    mteja = genai.Client(api_key=_siri("GEMINI_API_KEY"))
    cfg = dict(system_instruction=mfumo, temperature=temperature,
               response_mime_type="application/json")
    try:
        r = mteja.models.generate_content(
            model=MODELI["gemini"], contents=maandishi,
            config=types.GenerateContentConfig(frequency_penalty=0.4, **cfg))
    except Exception:
        r = mteja.models.generate_content(
            model=MODELI["gemini"], contents=maandishi,
            config=types.GenerateContentConfig(**cfg))
    return _toa_json(r.text)


def _openai_style(mteja, modeli, mfumo, maandishi, temperature):
    vigezo = dict(
        model=modeli, temperature=temperature,
        messages=[{"role": "system", "content": mfumo},
                  {"role": "user", "content": maandishi}],
        response_format={"type": "json_object"},
        frequency_penalty=0.4,
    )
    try:
        r = mteja.chat.completions.create(**vigezo)
    except Exception as e:
        if "penalty" in str(e).lower():
            vigezo.pop("frequency_penalty", None)
            r = mteja.chat.completions.create(**vigezo)
        else:
            raise
    return _toa_json(r.choices[0].message.content)


def _groq(mfumo, maandishi, temperature):
    from groq import Groq
    return _openai_style(Groq(api_key=_siri("GROQ_API_KEY")), MODELI["groq"],
                         mfumo, maandishi, temperature)


def _openai(mfumo, maandishi, temperature):
    from openai import OpenAI
    return _openai_style(OpenAI(api_key=_siri("OPENAI_API_KEY")), MODELI["openai"],
                         mfumo, maandishi, temperature)


_WATOA = {"gemini": _gemini, "groq": _groq, "openai": _openai}


def _ni_kosa_la_kikomo(e):
    t = str(e).lower()
    return any(x in t for x in ("429", "rate limit", "rate_limit", "resource_exhausted", "quota",
                                "too many requests", "503", "overloaded", "unavailable"))


def _piga_na_kusubiri(kitendakazi, *hoja):
    for jaribio in range(len(KUSUBIRI_BAADA_YA_KIKOMO) + 1):
        try:
            return kitendakazi(*hoja)
        except Exception as e:
            if jaribio < len(KUSUBIRI_BAADA_YA_KIKOMO) and _ni_kosa_la_kikomo(e):
                time.sleep(KUSUBIRI_BAADA_YA_KIKOMO[jaribio])
                continue
            raise


def _piga_ai_bila_muda(mfumo, maandishi, temperature=0.1, mtoa=None):
    """(Awali 'piga_ai', bila kikomo cha muda.)"""
    kosa_la_mwisho = None
    for m in ([mtoa] if mtoa else MPANGILIO_WA_WATOA_HUDUMA):
        try:
            return _piga_na_kusubiri(_WATOA[m], mfumo, maandishi, temperature)
        except Exception as e:
            kosa_la_mwisho = e
    raise RuntimeError(f"Watoa huduma wote wameshindwa: {kosa_la_mwisho}")


def piga_ai(mfumo, maandishi, temperature=0.1, mtoa=None):
    """Hujaribu watoa huduma kwa mpangilio hadi mmoja afanikiwe.
    v2.1: kila jaribio lina kikomo cha muda (SANIFU_TIMEOUT_S).
    TimeoutAI -> mwitaji (for m in watoa) anajaribu mtoa anayefuata."""
    fut = _EXECUTOR.submit(_piga_ai_bila_muda, mfumo, maandishi, temperature, mtoa)
    try:
        return fut.result(timeout=SANIFU_TIMEOUT_S)
    except concurrent.futures.TimeoutError:
        raise TimeoutAI(f"piga_ai haikujibu ndani ya sekunde {SANIFU_TIMEOUT_S}")


# ----------------------------------------------------------------------------
# Maelekezo kwa AI kulingana na lugha
# ----------------------------------------------------------------------------

MFUMO_WA_JUMLA = """
You are AI Lingual Africa, an expert multilingual editor and translator for African and world languages.

TASK: The input text is written in <<CHANZO>>. Produce the final text in <<LENGO>>.
- If the input language and the output language are the same: EDIT ONLY. Fix spelling, grammar, agreement, word order and punctuation. Do not rewrite the author's style unnecessarily.
- If they differ: translate faithfully into <<LENGO>>, then polish it so it reads as natural, native <<LENGO>> (not a word-for-word calque).

RULES:
1. PRESERVE INFORMATION: keep every fact, number, date, unit, dose, name and quotation. Never add or drop content. Keep paragraph breaks and lists exactly.
2. NO UNNECESSARY REPETITION of words or phrases.
3. ORTHOGRAPHY AND GRAMMAR: <<MWONGOZO>>
4. IDIOMS: translate meaning, not words. Keep proper names and brand names; transliterate only when the output script differs.
5. TERMS WITHOUT A STANDARD EQUIVALENT: use the commonly accepted form or a loanword. Never invent words. If truly unsure, keep the original term.
6. Do not leave <<CHANZO>> words in the output (except names and unavoidable technical terms).
7. No greetings, comments or explanations inside "maandishi_sahihi".

OUTPUT: JSON only, no other text:
{"maandishi_sahihi": "<the final text in <<LENGO>> only>",
 "marekebisho": [{"kabla": "", "baada": "", "aina": "", "sababu": ""}]}
In "marekebisho" list the important corrections or translation decisions. Write "sababu" in <<MAELEZO>>.
"""

MFUMO_WA_MKAGUZI = """
You are a strict proofreader and translation reviewer for <<LENGO>>.
You receive a SOURCE text (<<CHANZO>>) and an EDITED text (<<LENGO>>). List only REAL remaining problems in the EDITED text:
spelling, grammar, agreement, unnatural wording, mistranslation, information added or omitted. Ignore pure style preferences.
"kabla" must be an exact snippet copied from the EDITED text. If there are no real problems, return an empty list.
JSON only: {"makosa": [{"kabla": "", "baada": "", "aina": "", "sababu": ""}]}
Write "sababu" in <<MAELEZO>>.
"""


MFUMO_WA_MTAFSIRI = """
You are a fast, faithful translator and first-draft writer. Input language: <<CHANZO>>. Output language: <<LENGO>>.
- Different languages: translate naturally and idiomatically (meaning first, not word-for-word).
- Same language: lightly clean the text only (obvious typos, scrambled letters, missing spaces); do not restyle it.
- Keep every fact, number, date, unit, dose and name. Keep paragraph breaks and lists.
- No comments or explanations. A senior editor will polish your draft afterwards, so do not worry about fine grammar rules.
JSON only, no other text: {"rasimu": "<the text in <<LENGO>>>"}
"""

MAELEKEZO_YA_RASIMU = (
    "\n\nINPUT FORMAT: You receive a SOURCE text and a DRAFT produced by a fast translator. "
    "Verify the DRAFT against the SOURCE: fix mistranslations, omissions and additions, then apply ALL the rules "
    "above to produce the final text. The final text must stay faithful to the SOURCE."
)

MAELEKEZO_YA_UKAGUZI_WA_PILI = """

UKAGUZI WA PILI (KAGUA UPYA): Maandishi haya yamekwisha kuhaririwa mara moja. Yakague tena kwa makini na urekebishe
makosa yote yaliyobaki, hasa:
1. Upatanisho wa ngeli: LI-YA ('matumizi yamesaidia', 'mafanikio yamekuja', 'mazingira yamebadilika'); U-I ('mradi
   umekamilika', 'miradi imekamilika'); KI-VI ('kitabu kimefika', 'vitabu vimefika'); I-ZI ('biashara ndogondogo zinachangia').
2. 'Kila' hufuatwa na umoja, na kitenzi chake pia ni cha umoja ('kila mwanafunzi ana', 'kila mdau anatimiza').
3. Usambamba wa vitenzi kwenye orodha ('itaimarika, itatoa, na itaimarisha'; 'hujenga, huhamasisha, na huhakikisha').
4. Alama za uandishi (mkato, nukta, nukta mkato) na nukta ya mwisho.
5. Usipoteze wala usiongeze taarifa; namba na majina visibadilike. Usiguse sehemu zilizo sahihi.
"""


def _jaza(kiolezo, chanzo, lengo, mwongozo="", maelezo=KISWAHILI):
    return (kiolezo.replace("<<CHANZO>>", chanzo).replace("<<LENGO>>", lengo)
            .replace("<<MWONGOZO>>", mwongozo).replace("<<MAELEZO>>", maelezo))


def jenga_mfumo(lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, lugha_ya_maelezo=KISWAHILI):
    chanzo, lengwa = pata_lugha(lugha_chanzo), pata_lugha(lugha_lengwa)
    if ni_kiswahili(lengwa["jina"]):
        if ni_kiswahili(chanzo["jina"]):
            return SANIFU_SYSTEM_PROMPT
        utangulizi = (
            f"MAANDISHI YA KUINGIZA YAMEANDIKWA KWA {chanzo['jina'].upper()} ({chanzo['kiingereza']}). "
            "Yatafsiri kwa Kiswahili Sanifu kwa uaminifu (usiache wala kuongeza taarifa yoyote, wala namba), "
            "kisha tumia kanuni zote zilizo hapa chini kwenye tafsiri hiyo. "
            "Kwenye 'marekebisho' taja maamuzi muhimu ya tafsiri na istilahi.\n"
        )
        jozi = _maelekezo_ya_jozi(chanzo["jina"], lengwa["jina"]) if _maelekezo_ya_jozi else ""
        ziada = ("\n\nKANUNI ZA TAFSIRI ZA JOZI HII (ZINALAZIMA):\n" + jozi) if jozi else ""
        return utangulizi + SANIFU_SYSTEM_PROMPT + ziada
    return _jaza(MFUMO_WA_JUMLA, chanzo["kiingereza"], lengwa["kiingereza"],
                 lengwa["mwongozo"], pata_lugha(lugha_ya_maelezo)["kiingereza"])


# ----------------------------------------------------------------------------
# Ukaguzi wa jumla (unafanya kazi kwa lugha yoyote)
# ----------------------------------------------------------------------------

def _ni_sawa(lugha_a, lugha_b):
    return pata_lugha(lugha_a)["jina"].lower() == pata_lugha(lugha_b)["jina"].lower()


def _idadi_ya_maneno(t):
    return max(len(re.findall(r"\w+", t)), len(t) // 6, 1)


def _namba_za(t):
    t = "".join(
        str(unicodedata.digit(c)) if c.isdigit() and unicodedata.digit(c, None) is not None else c
        for c in t
    )
    t = re.sub(r"(?<=\d)[.,](?=\d)", "", t)
    t = re.sub(r"(?<=\d)[ \u00a0](?=\d{3}(?!\d))", "", t)
    return Counter(re.findall(r"\d+", t))


def _ni_kilatini(t):
    herufi = [c for c in t if c.isalpha()]
    if not herufi:
        return True
    kilatini = sum(1 for c in herufi if unicodedata.name(c, "").startswith("LATIN"))
    return kilatini / len(herufi) > 0.8


def _makosa_ya_jumla(asili, sahihi, lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI):
    if not (sahihi or "").strip():
        return [{"kabla": "", "baada": "", "aina": "Matokeo matupu",
                 "sababu": "Hakuna maandishi yaliyotolewa.", "uzito": 10}]
    makosa = []

    chanzo_namba, lengo_namba = _namba_za(asili), _namba_za(sahihi)
    for namba, idadi in chanzo_namba.items():
        if lengo_namba[namba] < idadi:
            makosa.append({"kabla": namba, "baada": "", "aina": "Namba imepotea",
                           "sababu": f"Namba '{namba}' iliyokuwa kwenye maandishi ya awali haipo kwenye matokeo.",
                           "uzito": 3})
            if len(makosa) >= 5:
                break

    if not _ni_sawa(lugha_chanzo, lugha_lengwa):
        a = len(re.sub(r"\s+", "", asili))
        b = len(re.sub(r"\s+", "", sahihi))
        if a >= 20 and not (0.25 <= b / a <= 4.0):
            makosa.append({"kabla": "", "baada": "", "aina": "Urefu usio wa kawaida",
                           "sababu": "Matokeo ni mafupi au marefu kupita kiasi ukilinganisha na maandishi ya awali "
                                     "(huenda sehemu imeachwa au imeongezwa).", "uzito": 3})
        if _ni_kilatini(asili) and _ni_kilatini(sahihi):
            chanzo_maneno = {w for w in re.findall(r"[^\W\d_]{4,}", asili.lower())}
            lengo_maneno = re.findall(r"[^\W\d_]{4,}", sahihi.lower())
            if len(lengo_maneno) >= 8:
                uvujaji = sum(1 for w in lengo_maneno if w in chanzo_maneno) / len(lengo_maneno)
                if uvujaji > 0.6:
                    makosa.append({"kabla": "", "baada": "", "aina": "Haikutafsiriwa",
                                   "sababu": f"{round(uvujaji * 100)}% ya maneno ya matokeo yanafanana na ya lugha ya chanzo; "
                                             "huenda maandishi hayakutafsiriwa.", "uzito": 3})
    return makosa


def _kagua_kwa_ai(asili, sahihi, lugha_chanzo, lugha_lengwa, lugha_ya_maelezo, mtoa_wa_mhariri, tahadhari,
                  ruhusiwa=None):
    """Mkaguzi wa AI (hiari): hutoa makosa yaliyobaki kwa lugha yoyote. Mtoa huduma tofauti na mhariri hupendelewa."""
    mfumo = _jaza(MFUMO_WA_MKAGUZI, pata_lugha(lugha_chanzo)["kiingereza"], pata_lugha(lugha_lengwa)["kiingereza"],
                  maelezo=pata_lugha(lugha_ya_maelezo)["kiingereza"])
    ujumbe = f"SOURCE:\n{asili}\n\nEDITED:\n{sahihi}"
    watoa = list(ruhusiwa or MPANGILIO_WA_WATOA_HUDUMA)
    if mtoa_wa_mhariri in watoa:
        i = watoa.index(mtoa_wa_mhariri)
        watoa = watoa[i + 1:] + watoa[:i + 1]
    for m in watoa:
        try:
            j = piga_ai(mfumo, ujumbe, temperature=0, mtoa=m)
        except Exception as e:
            # v2.1: andika kosa (BILA maandishi) ili debugging iwezekane.
            logger.warning("_kagua_kwa_ai (%s) imeshindwa: %s: %s", m, type(e).__name__, str(e)[:120])
            continue
        makosa = []
        for k in j.get("makosa", []) or []:
            kabla = (k.get("kabla") or "").strip()
            if kabla and kabla in sahihi:
                makosa.append({"kabla": kabla, "baada": k.get("baada", ""), "aina": k.get("aina", "AI"),
                               "sababu": k.get("sababu", ""), "uzito": 1})
        return makosa[:10]
    tahadhari.append("Mkaguzi wa AI ameshindwa; alama haijumuishi ukaguzi wa AI.")
    return []


# ----------------------------------------------------------------------------
# Mhariri mkuu
# ----------------------------------------------------------------------------

def _jibu_linakubalika(asili, jibu, lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI):
    sahihi = (jibu or {}).get("maandishi_sahihi", "")
    if not sahihi or not sahihi.strip():
        return False
    if _ni_sawa(lugha_chanzo, lugha_lengwa) and not kagua_uaminifu(asili, sahihi):
        return False
    if any(k.get("uzito", 1) >= 3 for k in _makosa_ya_jumla(asili, sahihi, lugha_chanzo, lugha_lengwa)):
        return False
    if ni_kiswahili(lugha_lengwa):
        if kagua_ngeli_mahali(sahihi):
            return False
        makubwa = [k for k in kagua_kwa_kanuni_za_bakita(sahihi) if k["aina"] in ("MOFOLOJIA", "KIROBOTI")]
        if makubwa:
            return False
    return True


def _makosa_yaliyobaki(maandishi, asili=None, lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, makosa_ya_ai=None):
    baki = []
    if ni_kiswahili(lugha_lengwa):
        baki += (kagua_ngeli_mahali(maandishi) + kagua_marudio(maandishi)
                 + kagua_nukta_mkato(maandishi) + kagua_mkato_kabla_ya_ili(maandishi)
                 + kagua_kwa_kanuni_za_bakita(maandishi))
    if asili is not None:
        baki += _makosa_ya_jumla(asili, maandishi, lugha_chanzo, lugha_lengwa)
        if ni_kiswahili(lugha_lengwa) and _KANUNI is not None and hasattr(_KANUNI, "kagua_tafsiri"):
            try:
                baki += [{"kabla": k["neno"], "baada": (k["mapendekezo"] or [""])[0],
                          "aina": k["aina"], "sababu": k["ujumbe"]}
                         for k in _KANUNI.kagua_tafsiri(lugha_chanzo, asili, maandishi)]
            except Exception as e:
                logger.warning("_makosa_yaliyobaki: kagua_tafsiri imeshindwa: %s: %s", type(e).__name__, str(e)[:120])
    return baki + list(makosa_ya_ai or [])


def hesabu_alama_ya_matokeo(asili, sahihi, lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, makosa_ya_ai=None):
    sawa = _ni_sawa(lugha_chanzo, lugha_lengwa)
    baki = _makosa_yaliyobaki(sahihi, asili, lugha_chanzo, lugha_lengwa, makosa_ya_ai)
    uzito = sum(k.get("uzito", 1) for k in baki)
    alama = hesabu_alama(uzito, _idadi_ya_maneno(asili if sawa else sahihi))
    if sawa and not kagua_uaminifu(asili, sahihi):
        alama = min(alama, 85)
    return alama


def _maoni_ya_kurudia(makosa, uaminifu_ni_sawa):
    mistari = []
    for k in makosa[:12]:
        mistari.append(
            f'- "{k.get("kabla", "")}" -> "{k.get("baada", "")}" '
            f'({k.get("aina", "")}: {k.get("sababu", "")})'
        )
    if not uaminifu_ni_sawa:
        mistari.append("- Maneno ya msingi ya maandishi asilia yamedondoshwa; yarudishe yote.")
    return ("\n\nMAKOSA YALIYOBAKI KWENYE MAANDISHI HAYA. Yarekebishe yote "
            "na usiguse sehemu zilizo sahihi:\n" + "\n".join(mistari))


def _hatua_ya_mtafsiri(asili, lugha_chanzo, lugha_lengwa, tahadhari):
    mfumo = _jaza(MFUMO_WA_MTAFSIRI, pata_lugha(lugha_chanzo)["kiingereza"], pata_lugha(lugha_lengwa)["kiingereza"])
    if ni_kiswahili(lugha_lengwa):
        mfumo += "\nUse Standard Swahili (Kiswahili Sanifu)."
    try:
        j = piga_ai(mfumo, asili, temperature=0.2, mtoa="groq")
    except Exception as e:
        # v2.1: log pia (BILA maandishi).
        logger.warning("_hatua_ya_mtafsiri (Groq) imeshindwa: %s: %s", type(e).__name__, str(e)[:120])
        tahadhari.append(f"Mtafsiri (Groq) ameshindwa ({e}); Gemini atatafsiri na kuhariri mwenyewe.")
        return None, None
    rasimu = ((j or {}).get("rasimu") or (j or {}).get("maandishi_sahihi") or "").strip()
    if not rasimu:
        tahadhari.append("Mtafsiri (Groq) hakutoa maandishi; Gemini atatafsiri na kuhariri mwenyewe.")
        return None, None
    return rasimu, "groq"


def _safisha_chanzo_kwa_kanuni(maandishi):
    makosa = (kagua_ngeli_mahali(maandishi) + kagua_marudio(maandishi) + kagua_nukta_mkato(maandishi)
              + kagua_mkato_kabla_ya_ili(maandishi) + kagua_kwa_kanuni_za_bakita(maandishi))
    safi = ondoa_mkato_kabla_ya_ili(
        ondoa_marudio(tumia_marekebisho_ya_ngeli(tumia_marekebisho_ya_nukta_mkato(maandishi))))
    orodha = [{kk: v for kk, v in k.items() if kk != "span"} for k in makosa]
    return {"maandishi_sahihi": safi, "tahadhari": [], "marekebisho": orodha,
            "alama": hesabu_alama(len(orodha), _idadi_ya_maneno(maandishi))}


def _hariri_mara_moja(maandishi, asili, mfumo, maoni="", lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI,
                      watoa=None, rasimu=None):
    tahadhari = []
    jibu, mtoa_aliyetumika, jibu_la_akiba, mtoa_wa_akiba = None, None, None, None
    mfumo_wa_wito = mfumo + (MAELEKEZO_YA_RASIMU if rasimu is not None else "") + maoni
    ujumbe = maandishi
    if rasimu is not None:
        ujumbe = (f"SOURCE ({pata_lugha(lugha_chanzo)['kiingereza']}):\n{asili}\n\n"
                  f"DRAFT ({pata_lugha(lugha_lengwa)['kiingereza']}) by a fast translator:\n{rasimu}")
    for m in (watoa or MPANGILIO_WA_WATOA_HUDUMA):
        try:
            j = piga_ai(mfumo_wa_wito, ujumbe, temperature=0.1, mtoa=m)
        except TimeoutAI as e:
            # v2.1: timeout inashughulikiwa tofauti ili kujaribu mtoa anayefuata haraka.
            logger.warning("_hariri_mara_moja (%s): %s", m, type(e).__name__)
            tahadhari.append(f"{m}: imechelewa; najaribu mtoa anayefuata.")
            continue
        except Exception as e:
            logger.warning("_hariri_mara_moja (%s) imeshindwa: %s: %s", m, type(e).__name__, str(e)[:120])
            tahadhari.append(f"{m}: imeshindwa ({e})")
            continue
        if jibu_la_akiba is None:
            jibu_la_akiba, mtoa_wa_akiba = j, m
        if _jibu_linakubalika(asili, j, lugha_chanzo, lugha_lengwa):
            jibu, mtoa_aliyetumika = j, m
            break
        tahadhari.append(f"{m}: jibu halikupita ukaguzi wa ubora; najaribu mtoa huduma anayefuata.")

    if jibu is None and jibu_la_akiba is None and rasimu is not None:
        jibu_la_akiba, mtoa_wa_akiba = {"maandishi_sahihi": rasimu, "marekebisho": []}, "rasimu"
        tahadhari.append("Mhariri mkuu ameshindwa; nimetumia rasimu ya mtafsiri na kuirekebisha kwa kanuni.")
    if jibu is None:
        if jibu_la_akiba is None:
            raise RuntimeError("Hakuna mtoa huduma aliyetoa jibu. " + " | ".join(tahadhari))
        jibu, mtoa_aliyetumika = jibu_la_akiba, mtoa_wa_akiba
        tahadhari.append("Hakuna jibu lililopita ukaguzi wote; nimetumia la kwanza na kulirekebisha kwa kanuni.")

    sahihi = jibu.get("maandishi_sahihi", maandishi)
    marekebisho = list(jibu.get("marekebisho", []))

    if ni_kiswahili(lugha_lengwa):
        for k in kagua_ngeli_mahali(sahihi) + kagua_marudio(sahihi):
            marekebisho.append({kk: v for kk, v in k.items() if kk != "span"})
        sahihi = ondoa_mkato_kabla_ya_ili(
            ondoa_marudio(tumia_marekebisho_ya_ngeli(tumia_marekebisho_ya_nukta_mkato(sahihi)))
        )
        if _KANUNI is not None and hasattr(_KANUNI, "rekebisha_tafsiri"):
            try:
                r = _KANUNI.rekebisha_tafsiri(lugha_chanzo, asili, sahihi)
                sahihi = r["maandishi"]
                marekebisho += r["mabadiliko"]
            except Exception as e:
                logger.warning("rekebisha_tafsiri imeshindwa: %s: %s", type(e).__name__, str(e)[:120])
    return {"maandishi_sahihi": sahihi, "marekebisho": marekebisho,
            "mtoa_huduma": mtoa_aliyetumika, "tahadhari": tahadhari}


def hariri_kwa_ubora(maandishi, kamusi=None, mfumo=None, lengo=90, majaribio_ya_juu=3,
                     lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, lugha_ya_maelezo=KISWAHILI,
                     mkaguzi_wa_ai=False, hariri_chanzo_kwanza=True,
                     hali="kawaida", ukaguzi_wa_lazima=None):
    """(Kama ilivyokuwa — API haijabadilika.)"""
    chanzo, lengwa = pata_lugha(lugha_chanzo), pata_lugha(lugha_lengwa)
    jc, jl = chanzo["jina"], lengwa["jina"]
    sw_chanzo, sw_lengwa = ni_kiswahili(jc), ni_kiswahili(jl)
    mfumo = mfumo or jenga_mfumo(jc, jl, lugha_ya_maelezo)
    tahadhari, chanzo_kilichohaririwa, awali = [], None, None
    if hali not in HALI_ZA_AI:
        raise ValueError(f"hali isiyojulikana: {hali!r}; chagua kati ya {HALI_ZA_AI}")
    watoa = WATOA_WA_HALI[hali]
    if ukaguzi_wa_lazima is None:
        ukaguzi_wa_lazima = hali == "gemini_pekee"
    if ukaguzi_wa_lazima:
        majaribio_ya_juu = max(majaribio_ya_juu, 2)
    if hali != "kawaida" and len(maandishi) > KIKOMO_CHA_HERUFI_KWA_BURE:
        tahadhari.append("Maandishi ni marefu; viwango vya bure vinaweza kukataa (kikomo cha tokeni kwa dakika). "
                         "Yagawanye kwa aya na uyatume kwa awamu.")

    if sw_chanzo and not sw_lengwa and hariri_chanzo_kwanza:
        if hali == "kawaida":
            awali = hariri_kwa_ubora(maandishi, kamusi=kamusi, lengo=lengo, majaribio_ya_juu=1,
                                     lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI,
                                     lugha_ya_maelezo=lugha_ya_maelezo)
        else:
            awali = _safisha_chanzo_kwa_kanuni(maandishi)
        chanzo_kilichohaririwa = awali["maandishi_sahihi"]
        tahadhari += awali["tahadhari"]
        maandishi = chanzo_kilichohaririwa

    asili = tatua_anagram_kwenye_maandishi(maandishi, kamusi or []) if sw_chanzo else maandishi

    def tathmini(j):
        makosa_ai = []
        if mkaguzi_wa_ai:
            makosa_ai = _kagua_kwa_ai(asili, j["maandishi_sahihi"], jc, jl, lugha_ya_maelezo,
                                      j["mtoa_huduma"], tahadhari, ruhusiwa=watoa)
        alama = hesabu_alama_ya_matokeo(asili, j["maandishi_sahihi"], jc, jl, makosa_ai)
        return alama, _makosa_yaliyobaki(j["maandishi_sahihi"], asili, jc, jl, makosa_ai)

    rasimu, mtoa_wa_rasimu = None, None
    if hali == "bure":
        rasimu, mtoa_wa_rasimu = _hatua_ya_mtafsiri(asili, jc, jl, tahadhari)
    jaribio = _hariri_mara_moja(asili, asili, mfumo, "", jc, jl, watoa, rasimu)
    marekebisho_ya_awali = list(jaribio["marekebisho"])
    marekebisho = list(marekebisho_ya_awali)
    tahadhari += jaribio["tahadhari"]
    if hali == "bure" and jaribio["mtoa_huduma"] == "groq":
        tahadhari.append("Gemini hakupatikana; Groq amehariri. Ubora wa ngeli za Kiswahili unaweza kuwa chini kuliko kawaida.")

    bora = jaribio
    alama_bora, makosa_baki = tathmini(bora)
    historia = [alama_bora]
    idadi = 1

    ukaguzi_bado = bool(ukaguzi_wa_lazima)
    while idadi < max(1, majaribio_ya_juu) and (alama_bora < lengo or ukaguzi_bado):
        maoni = ""
        if makosa_baki or alama_bora < lengo:
            # v2.1: 'not _ni_sawa(...)' wazi zaidi kuliko 'is False'.
            maoni = _maoni_ya_kurudia(
                makosa_baki,
                not _ni_sawa(jc, jl) or kagua_uaminifu(asili, bora["maandishi_sahihi"]),
            )
        if ukaguzi_bado and ni_kiswahili(jl):
            maoni += MAELEKEZO_YA_UKAGUZI_WA_PILI
        ilikuwa_ukaguzi, ukaguzi_bado = ukaguzi_bado, False
        try:
            jaribio = _hariri_mara_moja(bora["maandishi_sahihi"], asili, mfumo, maoni, jc, jl, watoa)
        except Exception as e:
            logger.warning("hariri_kwa_ubora jaribio %d: %s: %s", idadi + 1, type(e).__name__, str(e)[:120])
            tahadhari.append(f"Jaribio la {idadi + 1} limeshindwa ({e}); nimebaki na matokeo bora zaidi.")
            break
        idadi += 1
        marekebisho += jaribio["marekebisho"]
        tahadhari += jaribio["tahadhari"]
        alama_j, baki_j = tathmini(jaribio)
        historia.append(alama_j)
        kubali = alama_j > alama_bora or (
            ilikuwa_ukaguzi and alama_j >= alama_bora
            and _jibu_linakubalika(asili, {"maandishi_sahihi": jaribio["maandishi_sahihi"]}, jc, jl))
        if kubali:
            bora, alama_bora, makosa_baki = jaribio, alama_j, baki_j
        else:
            tahadhari.append(f"Jaribio la {idadi} halikuboresha alama; nimebaki na matokeo bora zaidi.")
            break

    alama_ya_kuingiza = None
    if awali is not None:
        marekebisho_ya_awali = list(awali["marekebisho"]) + marekebisho_ya_awali
        marekebisho = list(awali["marekebisho"]) + marekebisho
        alama_ya_kuingiza = awali["alama"]
    elif sw_chanzo:
        makosa_ya_asili = (kagua_ngeli_mahali(asili) + kagua_marudio(asili)
                           + kagua_nukta_mkato(asili) + kagua_mkato_kabla_ya_ili(asili)
                           + kagua_kwa_kanuni_za_bakita(asili))
        for orodha in (marekebisho_ya_awali, marekebisho):
            taarifa = {(k.get("kabla") or "").strip() for k in orodha}
            for k in makosa_ya_asili:
                if (k.get("kabla") or "").strip() not in taarifa:
                    orodha.append({kk: v for kk, v in k.items() if kk != "span"})
                    taarifa.add((k.get("kabla") or "").strip())
        alama_ya_kuingiza = hesabu_alama(len(marekebisho_ya_awali), _idadi_ya_maneno(asili))

    if sw_lengwa:
        aina_ya_alama = "kanuni_za_kiswahili"
    else:
        aina_ya_alama = "uaminifu_na_ai" if mkaguzi_wa_ai else "uaminifu_tu"

    return {
        "maandishi_sahihi": bora["maandishi_sahihi"],
        "marekebisho": marekebisho,
        "mtoa_huduma": bora["mtoa_huduma"],
        "tahadhari": tahadhari,
        "alama": alama_ya_kuingiza,
        "alama_ya_matokeo": alama_bora,
        "aina_ya_alama": aina_ya_alama,
        "lengo_limefikiwa": alama_bora >= lengo,
        "majaribio": idadi,
        "historia_ya_alama": historia,
        "makosa_yaliyobaki": [{kk: v for kk, v in k.items() if kk != "span"} for k in makosa_baki],
        "lugha_chanzo": jc,
        "lugha_lengwa": jl,
        "mwelekeo": lengwa["mwelekeo"],
        "onyo_la_lugha": onyo_la_lugha(jl) or (onyo_la_lugha(jc) if not _ni_sawa(jc, jl) else None),
        "chanzo_kilichohaririwa": chanzo_kilichohaririwa,
        "hali": hali,
        "mtoa_wa_rasimu": mtoa_wa_rasimu,
        "rasimu": rasimu,
    }
