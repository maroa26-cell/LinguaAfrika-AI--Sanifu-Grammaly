"""
sanifu_editor.py - Mhariri wa AI Lingual Africa: lugha yoyote -> lugha yoyote

Mtumiaji huchagua lugha ya maandishi aliyonayo (lugha_chanzo) na lugha anayotaka kuyapata
(lugha_lengwa). Zikiwa sawa: huhaririwa tu. Zikitofautiana: hutafsiriwa na kuhaririwa.
Kanuni za sarufi za Kiswahili (ngeli, Yambiwa, n.k.) hutumika Kiswahili kinapohusika;
kwa lugha nyingine kuna ukaguzi wa jumla (namba, urefu, maneno ya lugha ya chanzo yaliyobaki)
na mkaguzi wa AI wa hiari (mkaguzi_wa_ai=True).

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

import json
import os
import re
import unicodedata
from collections import Counter

from lugha_za_afrika import KISWAHILI, ni_kiswahili, onyo_la_lugha, pata_lugha

# ----------------------------------------------------------------------------
# Mipangilio
# ----------------------------------------------------------------------------

MPANGILIO_WA_WATOA_HUDUMA = ["gemini", "groq", "openai"]   # Gemini -> Groq -> OpenAI

MODELI = {
    "gemini": "gemini-2.5-flash",
    "groq": "llama-3.3-70b-versatile",
    "openai": "gpt-4o-mini",
}

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

# Ngeli ya kivumishi -yenye kwa nomino za kawaida (panua kadiri unavyohitaji)
NGELI_YENYE = {
    "darasa": "lenye", "soko": "lenye", "shamba": "lenye", "jiji": "lenye",
    "shule": "yenye", "nyumba": "yenye", "barabara": "yenye", "kampuni": "yenye",
    "kitabu": "chenye", "kiti": "chenye", "kijiji": "chenye",
    "mji": "wenye", "mti": "wenye", "mkoa": "wenye",
    "mtu": "mwenye", "mwalimu": "mwenye",
}

# Marudio ya kisarufi yanayoruhusiwa
MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara"}

# Nomino zinazoishia -ni lakini si maneno ya mahali ('kampuni yenye' ni sahihi)
NOMINO_ZENYE_NI_ZA_KAWAIDA = {
    "kampuni", "leseni", "televisheni", "nini", "ini", "jini", "kuni", "benki",
    "taasisi", "akaunti", "kiini", "mwanzoni",
}

# Muunganisho na kanuni_ya_sarufi.py (ikiwepo kwenye repo). Bila hiyo, mhariri hufanya kazi kwa vikagua vya ndani.
try:
    from kanuni_ya_sarufi import KanuniZaSarufiKiswahili, MAELEKEZO_YA_LUGHA
    _KANUNI = KanuniZaSarufiKiswahili()
    SANIFU_SYSTEM_PROMPT = (
        SANIFU_SYSTEM_PROMPT
        + "\n\nKANUNI ZA ZIADA ZA KISWAHILI SANIFU (BAKITA):\n"
        + MAELEKEZO_YA_LUGHA["Kiswahili"]
    )
except Exception:  # ImportError au hitilafu nyingine ya kupakia
    _KANUNI = None


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
        if herufi_kubwa:  # hifadhi herufi kubwa mwanzoni mwa sentensi
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
    """Hurekebisha makosa ya ngeli ya mahali kwa kanuni (kutoka mwisho kwenda mwanzo)."""
    for k in sorted(kagua_ngeli_mahali(maandishi), key=lambda x: x["span"][0], reverse=True):
        a, b = k["span"]
        maandishi = maandishi[:a] + k["baada"] + maandishi[b:]
    return maandishi


def ondoa_marudio(maandishi):
    """'kubwa kubwa' -> 'kubwa', isipokuwa maneno halali ya kurudiwa."""
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
    """';' ndani ya sentensi (mf. 'Ingawa mvua inanyesha; hatuwezi')."""
    return [{
        "kabla": m.group(0), "baada": m.group(0).replace(";", ","),
        "aina": "Alama za uandishi",
        "sababu": "Nukta mkato (;) imetumika pale koma (,) inatosha.",
    } for m in re.finditer(r"[^.;!?]*\b(?:Ingawa|Kwa kuwa|Kwa sababu)\b[^.;!?]*;", maandishi)]


def tumia_marekebisho_ya_nukta_mkato(maandishi):
    """'Ingawa mvua inanyesha; hatuwezi' -> 'Ingawa mvua inanyesha, hatuwezi'."""
    return re.sub(r"([^.;!?]*\b(?:Ingawa|Kwa kuwa|Kwa sababu)\b[^.;!?]*);", r"\1,", maandishi)


def kagua_mkato_kabla_ya_ili(maandishi):
    """Kanuni ya 6: usiweke mkato kabla ya kiunganishi 'ili'."""
    return [{
        "kabla": m.group(0), "baada": m.group(0).replace(",", "", 1),
        "aina": "Alama za uandishi",
        "sababu": "Mkato haiwekwi kabla ya kiunganishi 'ili'.",
    } for m in re.finditer(r"\w+,\s+ili\b", maandishi)]


def ondoa_mkato_kabla_ya_ili(maandishi):
    return re.sub(r"(\w+),(\s+ili\b)", r"\1\2", maandishi)


def kagua_uaminifu(asili, matokeo, kizingiti=0.75):
    """
    Hakikisha AI haikudondosha maneno ya msingi.
    Ni tahadhari tu: marekebisho halali hubadilisha maneno mengine.
    """
    toka = lambda s: Counter(w for w in re.findall(r"\w+", s.lower()) if len(w) > 3)
    a, b = toka(asili), toka(matokeo)
    jumla = sum(a.values()) or 1
    yaliyobaki = sum(min(a[w], b[w]) for w in a)
    if jumla < 12:   # maandishi mafupi: marekebisho mawili tu hubadilisha sehemu kubwa ya maneno
        kizingiti = min(kizingiti, 0.5)
    return yaliyobaki / jumla >= kizingiti


def kagua_kwa_kanuni_za_bakita(maandishi):
    """Hutumia MkaguziSarufi (kanuni_ya_sarufi.py) kama inapatikana. Hurudisha orodha ya makosa."""
    if _KANUNI is None or not maandishi.strip():
        return []
    try:
        matokeo = _KANUNI.kagua_sentensi_nzima(maandishi, kagua_alama=False)
    except Exception:
        return []
    return [{
        "kabla": k["neno"],
        "baada": (k["mapendekezo"] or [""])[0],
        "aina": k["aina"],
        "sababu": k["ujumbe"],
    } for k in matokeo["makosa"]]


def hesabu_alama(idadi_ya_makosa, idadi_ya_maneno):
    """Alama inayotokana na msongamano wa makosa, si makadirio ya AI."""
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


def piga_ai(mfumo, maandishi, temperature=0.1, mtoa=None):
    """Hujaribu watoa huduma kwa mpangilio hadi mmoja afanikiwe."""
    kosa_la_mwisho = None
    for m in ([mtoa] if mtoa else MPANGILIO_WA_WATOA_HUDUMA):
        try:
            return _WATOA[m](mfumo, maandishi, temperature)
        except Exception as e:
            kosa_la_mwisho = e
    raise RuntimeError(f"Watoa huduma wote wameshindwa: {kosa_la_mwisho}")


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


def _jaza(kiolezo, chanzo, lengo, mwongozo="", maelezo=KISWAHILI):
    return (kiolezo.replace("<<CHANZO>>", chanzo).replace("<<LENGO>>", lengo)
            .replace("<<MWONGOZO>>", mwongozo).replace("<<MAELEZO>>", maelezo))


def jenga_mfumo(lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, lugha_ya_maelezo=KISWAHILI):
    """System prompt inayolingana na jozi ya lugha. Kiswahili->Kiswahili hurudisha prompt ya Sanifu."""
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
        return utangulizi + SANIFU_SYSTEM_PROMPT
    return _jaza(MFUMO_WA_JUMLA, chanzo["kiingereza"], lengwa["kiingereza"],
                 lengwa["mwongozo"], pata_lugha(lugha_ya_maelezo)["kiingereza"])


# ----------------------------------------------------------------------------
# Ukaguzi wa jumla (unafanya kazi kwa lugha yoyote)
# ----------------------------------------------------------------------------

def _ni_sawa(lugha_a, lugha_b):
    return pata_lugha(lugha_a)["jina"].lower() == pata_lugha(lugha_b)["jina"].lower()


def _idadi_ya_maneno(t):
    """Maneno kwa lugha zenye nafasi; kwa Kichina n.k. makadirio kwa herufi."""
    return max(len(re.findall(r"\w+", t)), len(t) // 6, 1)


def _namba_za(t):
    """Namba zilizomo (tarakimu za lugha yoyote hubadilishwa kuwa 0-9; vitenganishi huondolewa)."""
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
    """
    Ukaguzi usiotegemea lugha: matokeo matupu, namba zilizopotea, urefu usio wa kawaida,
    na maneno ya lugha ya chanzo yaliyobaki bila kutafsiriwa. 'uzito' wa 3 au zaidi hufeli lango la ubora.
    """
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


def _kagua_kwa_ai(asili, sahihi, lugha_chanzo, lugha_lengwa, lugha_ya_maelezo, mtoa_wa_mhariri, tahadhari):
    """Mkaguzi wa AI (hiari): hutoa makosa yaliyobaki kwa lugha yoyote. Mtoa huduma tofauti na mhariri hupendelewa."""
    mfumo = _jaza(MFUMO_WA_MKAGUZI, pata_lugha(lugha_chanzo)["kiingereza"], pata_lugha(lugha_lengwa)["kiingereza"],
                  maelezo=pata_lugha(lugha_ya_maelezo)["kiingereza"])
    ujumbe = f"SOURCE:\n{asili}\n\nEDITED:\n{sahihi}"
    watoa = list(MPANGILIO_WA_WATOA_HUDUMA)
    if mtoa_wa_mhariri in watoa:
        i = watoa.index(mtoa_wa_mhariri)
        watoa = watoa[i + 1:] + watoa[:i + 1]          # mhariri mwenyewe mwisho
    for m in watoa:
        try:
            j = piga_ai(mfumo, ujumbe, temperature=0, mtoa=m)
        except Exception:
            continue
        makosa = []
        for k in j.get("makosa", []) or []:
            kabla = (k.get("kabla") or "").strip()
            if kabla and kabla in sahihi:               # ondoa madai yasiyo na ushahidi kwenye maandishi
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
    """Makosa yanayogundulika kwenye matokeo (baada ya marekebisho ya kiotomatiki)."""
    baki = []
    if ni_kiswahili(lugha_lengwa):
        baki += (kagua_ngeli_mahali(maandishi) + kagua_marudio(maandishi)
                 + kagua_nukta_mkato(maandishi) + kagua_mkato_kabla_ya_ili(maandishi)
                 + kagua_kwa_kanuni_za_bakita(maandishi))
    if asili is not None:
        baki += _makosa_ya_jumla(asili, maandishi, lugha_chanzo, lugha_lengwa)
    return baki + list(makosa_ya_ai or [])


def hesabu_alama_ya_matokeo(asili, sahihi, lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, makosa_ya_ai=None):
    """
    Ubora wa MATOKEO ya mhariri (0-100): msongamano wa makosa yaliyobaki.
    Kwa Kiswahili inatumia kanuni za sarufi; kwa lugha nyingine inapima uaminifu (namba, urefu, kutotafsiriwa)
    na makosa ya mkaguzi wa AI (ikiwa umewashwa). Haipimi kila kosa linalowezekana.
    """
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


def _hariri_mara_moja(maandishi, asili, mfumo, maoni="", lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI):
    """
    Jaribio moja: watoa huduma kwa mpangilio, lango la ubora, kisha marekebisho ya kanuni (Kiswahili pekee).
    `maandishi` ndiyo yanayotumwa kwa AI; `asili` ndiyo kigezo cha uaminifu.
    """
    tahadhari = []
    jibu, mtoa_aliyetumika, jibu_la_akiba, mtoa_wa_akiba = None, None, None, None
    for m in MPANGILIO_WA_WATOA_HUDUMA:
        try:
            j = piga_ai(mfumo + maoni, maandishi, temperature=0.1, mtoa=m)
        except Exception as e:
            tahadhari.append(f"{m}: imeshindwa ({e})")
            continue
        if jibu_la_akiba is None:
            jibu_la_akiba, mtoa_wa_akiba = j, m
        if _jibu_linakubalika(asili, j, lugha_chanzo, lugha_lengwa):
            jibu, mtoa_aliyetumika = j, m
            break
        tahadhari.append(f"{m}: jibu halikupita ukaguzi wa ubora; najaribu mtoa huduma anayefuata.")

    if jibu is None:
        if jibu_la_akiba is None:
            raise RuntimeError("Hakuna mtoa huduma aliyetoa jibu. " + " | ".join(tahadhari))
        jibu, mtoa_aliyetumika = jibu_la_akiba, mtoa_wa_akiba
        tahadhari.append("Hakuna jibu lililopita ukaguzi wote; nimetumia la kwanza na kulirekebisha kwa kanuni.")

    sahihi = jibu.get("maandishi_sahihi", maandishi)
    marekebisho = list(jibu.get("marekebisho", []))

    if ni_kiswahili(lugha_lengwa):
        # Makosa ya kanuni yaliyokuwa kwenye jibu la AI (kabla ya kurekebisha)
        for k in kagua_ngeli_mahali(sahihi) + kagua_marudio(sahihi):
            marekebisho.append({kk: v for kk, v in k.items() if kk != "span"})
        sahihi = ondoa_mkato_kabla_ya_ili(
            ondoa_marudio(tumia_marekebisho_ya_ngeli(tumia_marekebisho_ya_nukta_mkato(sahihi)))
        )
    return {"maandishi_sahihi": sahihi, "marekebisho": marekebisho,
            "mtoa_huduma": mtoa_aliyetumika, "tahadhari": tahadhari}


def hariri_kwa_ubora(maandishi, kamusi=None, mfumo=None, lengo=90, majaribio_ya_juu=3,
                     lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI, lugha_ya_maelezo=KISWAHILI,
                     mkaguzi_wa_ai=False, hariri_chanzo_kwanza=True):
    """
    Huhariri (au hutafsiri na kuhariri) maandishi na kurudia hadi alama ya matokeo ifikie `lengo`
    (chaguo-msingi 90) au majaribio yafikie `majaribio_ya_juu` (chaguo-msingi 3).

    lugha_chanzo        - lugha ya maandishi uliyonayo (mf. "Kiswahili", "Kiingereza", au jina lolote).
    lugha_lengwa        - lugha unayotaka kuyapata. Zikiwa sawa: huhaririwa tu.
    lugha_ya_maelezo    - lugha ya maelezo ya marekebisho.
    mkaguzi_wa_ai       - washa mkaguzi wa AI (simu moja zaidi kwa kila jaribio); unahitajika
                          ili alama iseme chochote kuhusu sarufi ya lugha zisizo Kiswahili.
    hariri_chanzo_kwanza- chanzo cha Kiswahili kikitafsiriwa kwenda lugha nyingine, kwanza
                          kisafishwe kwa kanuni za Kiswahili (simu moja zaidi).

    Hurudisha: maandishi_sahihi, marekebisho, mtoa_huduma, tahadhari,
      alama (ubora wa maandishi ya kuingiza; None kwa chanzo kisicho Kiswahili),
      alama_ya_matokeo, aina_ya_alama, lengo_limefikiwa, majaribio, historia_ya_alama,
      makosa_yaliyobaki, lugha_chanzo, lugha_lengwa, mwelekeo, onyo_la_lugha, chanzo_kilichohaririwa
    """
    chanzo, lengwa = pata_lugha(lugha_chanzo), pata_lugha(lugha_lengwa)
    jc, jl = chanzo["jina"], lengwa["jina"]
    sw_chanzo, sw_lengwa = ni_kiswahili(jc), ni_kiswahili(jl)
    mfumo = mfumo or jenga_mfumo(jc, jl, lugha_ya_maelezo)
    tahadhari, chanzo_kilichohaririwa, awali = [], None, None

    # Chanzo cha Kiswahili kinachokwenda lugha nyingine: kisafishwe kwanza kwa kanuni za Kiswahili
    if sw_chanzo and not sw_lengwa and hariri_chanzo_kwanza:
        awali = hariri_kwa_ubora(maandishi, kamusi=kamusi, lengo=lengo, majaribio_ya_juu=1,
                                 lugha_chanzo=KISWAHILI, lugha_lengwa=KISWAHILI,
                                 lugha_ya_maelezo=lugha_ya_maelezo)
        chanzo_kilichohaririwa = awali["maandishi_sahihi"]
        tahadhari += awali["tahadhari"]
        maandishi = chanzo_kilichohaririwa

    asili = tatua_anagram_kwenye_maandishi(maandishi, kamusi or []) if sw_chanzo else maandishi

    def tathmini(j):
        makosa_ai = []
        if mkaguzi_wa_ai:
            makosa_ai = _kagua_kwa_ai(asili, j["maandishi_sahihi"], jc, jl, lugha_ya_maelezo,
                                      j["mtoa_huduma"], tahadhari)
        alama = hesabu_alama_ya_matokeo(asili, j["maandishi_sahihi"], jc, jl, makosa_ai)
        return alama, _makosa_yaliyobaki(j["maandishi_sahihi"], asili, jc, jl, makosa_ai)

    jaribio = _hariri_mara_moja(asili, asili, mfumo, "", jc, jl)
    marekebisho_ya_awali = list(jaribio["marekebisho"])
    marekebisho = list(marekebisho_ya_awali)
    tahadhari += jaribio["tahadhari"]

    bora = jaribio
    alama_bora, makosa_baki = tathmini(bora)
    historia = [alama_bora]
    idadi = 1

    while alama_bora < lengo and idadi < max(1, majaribio_ya_juu):
        maoni = _maoni_ya_kurudia(
            makosa_baki,
            _ni_sawa(jc, jl) is False or kagua_uaminifu(asili, bora["maandishi_sahihi"]),
        )
        try:
            jaribio = _hariri_mara_moja(bora["maandishi_sahihi"], asili, mfumo, maoni, jc, jl)
        except Exception as e:
            tahadhari.append(f"Jaribio la {idadi + 1} limeshindwa ({e}); nimebaki na matokeo bora zaidi.")
            break
        idadi += 1
        marekebisho += jaribio["marekebisho"]
        tahadhari += jaribio["tahadhari"]
        alama_j, baki_j = tathmini(jaribio)
        historia.append(alama_j)
        if alama_j > alama_bora:
            bora, alama_bora, makosa_baki = jaribio, alama_j, baki_j
        else:
            tahadhari.append(f"Jaribio la {idadi} halikuboresha alama; nimebaki na matokeo bora zaidi.")
            break

    # Makosa ya Kiswahili yaliyokuwa kwenye maandishi ya kuingiza ambayo AI haikuyataja
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
    }
