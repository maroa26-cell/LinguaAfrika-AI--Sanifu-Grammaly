"""
sanifu_editor.py - Msingi wa Mhariri wa Kiswahili Sanifu (AI Lingual Africa Sanifu)

Mtiririko:
  1. Anagram (M-A-L-U-W-I-M) hutatuliwa kwa kamusi, si kwa AI.
  2. AI (Gemini -> Groq -> OpenAI) huhariri kwa System Prompt kali.
  3. Vikagua vya kanuni hukamata makosa ambayo AI huyakosa:
     ngeli ya mahali (darasani yenye), marudio (kubwa kubwa), uaminifu (maneno yaliyodondoshwa).
  4. Jibu baya husababisha kuhamia mtoa huduma anayefuata.

Matumizi kwenye Streamlit:
    from sanifu_editor import hariri_kwa_ubora
    matokeo = hariri_kwa_ubora(maandishi, kamusi=KAMUSI_SET)
    st.metric("Alama", f"{matokeo['alama']}/100")
    st.write(matokeo["maandishi_sahihi"])
    for k in matokeo["marekebisho"]:
        st.write(k)

Funguo (st.secrets au environment variables):
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY
"""

import json
import os
import re
from collections import Counter

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
# Mhariri mkuu
# ----------------------------------------------------------------------------

def _jibu_linakubalika(asili, jibu):
    sahihi = (jibu or {}).get("maandishi_sahihi", "")
    if not sahihi or not kagua_uaminifu(asili, sahihi) or kagua_ngeli_mahali(sahihi):
        return False
    makubwa = [k for k in kagua_kwa_kanuni_za_bakita(sahihi) if k["aina"] in ("MOFOLOJIA", "KIROBOTI")]
    return not makubwa


def _makosa_yaliyobaki(maandishi):
    """Makosa yanayogundulika kwenye matokeo (baada ya marekebisho ya kiotomatiki)."""
    return (kagua_ngeli_mahali(maandishi) + kagua_marudio(maandishi)
            + kagua_nukta_mkato(maandishi) + kagua_mkato_kabla_ya_ili(maandishi)
            + kagua_kwa_kanuni_za_bakita(maandishi))


def hesabu_alama_ya_matokeo(asili, sahihi):
    """
    Ubora wa MATOKEO ya mhariri (0-100): msongamano wa makosa yaliyobaki,
    na haizidi 85 ikiwa maneno ya msingi yamedondoshwa.
    Inapima makosa ambayo vikagua vinaweza kuyaona tu, si kila kosa linalowezekana.
    """
    alama = hesabu_alama(len(_makosa_yaliyobaki(sahihi)), len(re.findall(r"\w+", asili)))
    if not kagua_uaminifu(asili, sahihi):
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


def _hariri_mara_moja(maandishi, asili, mfumo, maoni=""):
    """
    Jaribio moja la kuhariri: watoa huduma kwa mpangilio, lango la ubora, kisha marekebisho ya kanuni.
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
        if _jibu_linakubalika(asili, j):
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

    # Makosa ya kanuni yaliyokuwa kwenye jibu la AI (kabla ya kurekebisha)
    for k in kagua_ngeli_mahali(sahihi) + kagua_marudio(sahihi):
        marekebisho.append({kk: v for kk, v in k.items() if kk != "span"})

    sahihi = ondoa_mkato_kabla_ya_ili(
        ondoa_marudio(tumia_marekebisho_ya_ngeli(tumia_marekebisho_ya_nukta_mkato(sahihi)))
    )
    return {"maandishi_sahihi": sahihi, "marekebisho": marekebisho,
            "mtoa_huduma": mtoa_aliyetumika, "tahadhari": tahadhari}


def hariri_kwa_ubora(maandishi, kamusi=None, mfumo=SANIFU_SYSTEM_PROMPT,
                     lengo=90, majaribio_ya_juu=3):
    """
    Huhariri maandishi na kurudia mpaka alama ya matokeo ifikie `lengo` (chaguo-msingi 90)
    au majaribio yafikie `majaribio_ya_juu` (chaguo-msingi 3). Kwa kasi (Mhariri Live)
    tumia majaribio_ya_juu=1.

    Hurudisha:
      maandishi_sahihi, marekebisho, mtoa_huduma, tahadhari,
      alama               - ubora wa maandishi ya KUINGIZA (makosa yaliyokuwepo),
      alama_ya_matokeo    - ubora wa MATOKEO baada ya kuhariri,
      lengo_limefikiwa, majaribio, historia_ya_alama, makosa_yaliyobaki
    """
    asili = tatua_anagram_kwenye_maandishi(maandishi, kamusi or [])

    jaribio = _hariri_mara_moja(asili, asili, mfumo)
    marekebisho_ya_awali = list(jaribio["marekebisho"])
    marekebisho = list(marekebisho_ya_awali)
    tahadhari = list(jaribio["tahadhari"])

    bora = jaribio
    makosa_baki = _makosa_yaliyobaki(bora["maandishi_sahihi"])
    alama_bora = hesabu_alama_ya_matokeo(asili, bora["maandishi_sahihi"])
    historia = [alama_bora]
    idadi = 1

    while alama_bora < lengo and idadi < max(1, majaribio_ya_juu):
        maoni = _maoni_ya_kurudia(
            makosa_baki, kagua_uaminifu(asili, bora["maandishi_sahihi"])
        )
        try:
            jaribio = _hariri_mara_moja(bora["maandishi_sahihi"], asili, mfumo, maoni)
        except Exception as e:
            tahadhari.append(f"Jaribio la {idadi + 1} limeshindwa ({e}); nimebaki na matokeo bora zaidi.")
            break
        idadi += 1
        marekebisho += jaribio["marekebisho"]
        tahadhari += jaribio["tahadhari"]
        alama_j = hesabu_alama_ya_matokeo(asili, jaribio["maandishi_sahihi"])
        historia.append(alama_j)
        if alama_j > alama_bora:
            bora, alama_bora = jaribio, alama_j
            makosa_baki = _makosa_yaliyobaki(bora["maandishi_sahihi"])
        else:
            tahadhari.append(f"Jaribio la {idadi} halikuboresha alama; nimebaki na matokeo bora zaidi.")
            break

    # Makosa yaliyokuwa kwenye maandishi ya awali ambayo AI haikuyataja
    makosa_ya_asili = (kagua_ngeli_mahali(asili) + kagua_marudio(asili)
                       + kagua_nukta_mkato(asili) + kagua_mkato_kabla_ya_ili(asili)
                       + kagua_kwa_kanuni_za_bakita(asili))
    for orodha in (marekebisho_ya_awali, marekebisho):
        taarifa = {(k.get("kabla") or "").strip() for k in orodha}
        for k in makosa_ya_asili:
            if (k.get("kabla") or "").strip() not in taarifa:
                orodha.append({kk: v for kk, v in k.items() if kk != "span"})
                taarifa.add((k.get("kabla") or "").strip())

    idadi_ya_maneno = len(re.findall(r"\w+", asili))
    return {
        "maandishi_sahihi": bora["maandishi_sahihi"],
        "marekebisho": marekebisho,
        "mtoa_huduma": bora["mtoa_huduma"],
        "tahadhari": tahadhari,
        "alama": hesabu_alama(len(marekebisho_ya_awali), idadi_ya_maneno),
        "alama_ya_matokeo": alama_bora,
        "lengo_limefikiwa": alama_bora >= lengo,
        "majaribio": idadi,
        "historia_ya_alama": historia,
        "makosa_yaliyobaki": [{kk: v for kk, v in k.items() if kk != "span"} for k in makosa_baki],
    }
