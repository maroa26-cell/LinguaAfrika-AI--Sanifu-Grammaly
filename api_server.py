"""
AI Lingual Africa Sanifu API v3.3
Gemini (kuu) + Groq (akiba) + Hatua ya Pili ya Ukaguzi + Chujio salama la Python
+ Sheria ya 4B (chujio_4b.py): kuondoa Kiingereza kilichochanganywa kwenye Kiswahili

Njia zilezile: /api/chakata, /hariri, /tafsiri  (extension ya zamani haihitaji kubadilishwa)
Njia za mapendekezo: /pendekezo (au /api/pendekezo) -> orodha ya mapendekezo yenye nafasi (offsets)
MPYA v3.3 (kwa Chrome extension ya Lingual Sanifu):
  GET  /health      -> {"status":"ok"}  (kuamsha seva ya Render; haihitaji ufunguo)
  POST /v1/kagua    -> {"ok":true,"ai":true,"issues":[{original,suggestion,start,end,label,explanation,hiari}]}
                       (pia: /api/kagua na /kagua)

Environment Variables (Render):
  GEMINI_API_KEY   (inapendekezwa)
  GROQ_API_KEY     (akiba)
  API_KEY          (hiari) -> ikiwekwa, extension itume header: X-API-Key (iwe sawa na ufunguo ulio kwenye mipangilio ya extension)
  ALLOWED_ORIGINS  (hiari) -> mfano: chrome-extension://abcdef...,https://tovuti-yako.com  (chaguo-msingi: *)
  HATUA_MBILI      (hiari) -> "1" (chaguo-msingi) au "0" kuzima ukaguzi wa pili (kwa /hariri, /tafsiri, /pendekezo)
  KAGUA_HATUA_MBILI (hiari) -> "0" (chaguo-msingi) kwa /v1/kagua ili ukaguzi wa kuandika uwe wa haraka; "1" kuwasha
  MAX_CHARS        (hiari) -> kikomo cha herufi, chaguo-msingi 15000
  MAX_WORKERS      (hiari) -> uchakataji sambamba, chaguo-msingi 3
  GEMINI_MODEL, GEMINI_FALLBACK_MODEL, GROQ_MODEL (hiari) -> majina ya modeli; badilisha hapa modeli ikistaafishwa
"""
import os
import re
import difflib
import hmac
import time
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from groq import Groq

from chujio_4b import ondoa_kiingereza, ina_kiingereza

# ------------------------------------------------------------------
# 1. MIPANGILIO
# ------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_FALLBACK_MODEL = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash")  # akiba ya Gemini ikijaa
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
API_KEY_YA_HUDUMA = os.environ.get("API_KEY")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").strip()
HATUA_MBILI = os.environ.get("HATUA_MBILI", "1") == "1"
KAGUA_HATUA_MBILI = os.environ.get("KAGUA_HATUA_MBILI", "0") == "1"
MAX_CHARS = int(os.environ.get("MAX_CHARS", "15000"))
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "3"))
MAX_KIPANDE = 1200  # herufi kwa kipande kimoja cha aya ndefu

app = Flask(__name__)

if ALLOWED_ORIGINS == "*":
    CORS(app, allow_headers=["Content-Type", "X-API-Key"])
else:
    CORS(
        app,
        origins=[o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()],
        allow_headers=["Content-Type", "X-API-Key"],
    )

gemini_client = (
    genai.Client(api_key=GEMINI_API_KEY, http_options=types.HttpOptions(timeout=45_000))
    if GEMINI_API_KEY
    else None
)
groq_client = Groq(api_key=GROQ_API_KEY, timeout=45.0) if GROQ_API_KEY else None


@app.before_request
def angalia_ufunguo():
    """Ikiwa API_KEY imewekwa kwenye Render, omba header ya X-API-Key."""
    if not API_KEY_YA_HUDUMA:
        return None
    if request.method == "OPTIONS" or request.path in ("/", "/health", "/uchunguzi"):
        return None
    ulioletwa = request.headers.get("X-API-Key", "")
    if not hmac.compare_digest(ulioletwa, API_KEY_YA_HUDUMA):
        return jsonify({
            "ok": False,
            "kosa": "UFUNGUO_SIO_SAHIHI",   # extension inasoma 'kosa'
            "error": "Huna ruhusa ya kutumia huduma hii.",
        }), 401
    return None


# ------------------------------------------------------------------
# 2. KAMUSI YA ISTILAHI (kwa mipaka ya maneno, si kutafuta ndani ya maneno mengine)
# ------------------------------------------------------------------
KAMUSI_YA_ISTILAHI = {
    # Kutoka kwenye kamusi yako ya awali
    "local languages": "lugha za wenyeji (au lugha za asili)",
    "fraudsters": "walaghai",
    "renewable energy": "nishati jadidifu",
    "market linkages": "miunganiko ya masoko",
    "blue economy": "uchumi wa buluu",
    "aquaculture": "ufugaji wa viumbe maji",
    "coral reefs": "miamba ya matumbawe",
    "mangrove": "mikoko",
    "financial inclusion": "ushirikishwaji wa kifedha",
    "creditworthiness": "ustahili wa mkopo",
    "consumer protection": "ulinzi wa mlaji",
    "signing on the dotted line": "kutia saini mkataba rasmi",
    "work hand in hand": "kufanya kazi bega kwa bega",
    "rock-bottom prices": "bei ya chini kabisa",
    "not only": "si tu ... bali pia",
    "backbone": "mhimili mkuu",
    # Nyongeza (hakiki na mtaalamu wa lugha kabla ya kuziamini kikamilifu)
    "climate change": "mabadiliko ya tabianchi",
    "sustainable development": "maendeleo endelevu",
    "food security": "usalama wa chakula",
    "value chain": "mnyororo wa thamani",
    "supply chain": "mnyororo wa ugavi",
    "smallholder farmers": "wakulima wadogo",
    "irrigation": "umwagiliaji",
    "fertilizer": "mbolea",
    "artificial intelligence": "akili bandia",
    "cybersecurity": "usalama wa mtandao",
    "interest rate": "kiwango cha riba",
    "inflation": "mfumuko wa bei",
    "stakeholders": "wadau",
    "capacity building": "kujenga uwezo",
    "human rights": "haki za binadamu",
    "rule of law": "utawala wa sheria",
    "public health": "afya ya umma",
}

# Funguo ndefu kwanza ili kuepuka mgongano (mfano "local languages" kabla ya "local")
_KAMUSI_REGEX = [
    (re.compile(r"\b" + re.escape(en) + r"s?\b", re.IGNORECASE), en, sw)
    for en, sw in sorted(KAMUSI_YA_ISTILAHI.items(), key=lambda x: -len(x[0]))
]


def pata_vidokezo_vya_kamusi(maandishi: str) -> str:
    vidokezo = [
        f"- '{en}' itafsiriwe kama '{sw}'"
        for rx, en, sw in _KAMUSI_REGEX
        if rx.search(maandishi)
    ]
    if vidokezo:
        return "\nMWONGOZO WA ISTILAHI MAHUSUSI (ZINGATIA HIZI):\n" + "\n".join(vidokezo)
    return ""


# ------------------------------------------------------------------
# 3. CHUJIO SALAMA LA PYTHON
#    Hurekebisha tu mambo yasiyo na utata. Ngeli na sarufi huachiwa AI.
# ------------------------------------------------------------------
# Tahajia zilizothibitishwa. Ongeza mpya hapa baada ya kuzihakiki tu.
_TAHAJIA = {
    "serekali": "serikali",
    "kwasababu": "kwa sababu",
    "maswala": "masuala",
    "wanyama pori": "wanyamapori",
    "nguvu kazi": "nguvukazi",
}
_TAHAJIA_RX = re.compile(
    r"\b(?:serekali|kwasababu|maswala|wanyama\s+pori|nguvu\s+kazi)\b", re.IGNORECASE
)

# Maneno ya kawaida pekee ndiyo yanaondolewa yakijirudia kwa bahati mbaya
# (si "pole pole", "kidogo kidogo", "sana sana" n.k. ambayo ni halali).
_MANENO_YA_KAWAIDA = (
    "kuhusu", "na", "ya", "wa", "za", "kwa", "la", "cha", "vya", "katika", "pia", "kwamba",
)
_RUDIA_RX = re.compile(r"\b(" + "|".join(_MANENO_YA_KAWAIDA) + r")(?:\s+\1\b)+", re.IGNORECASE)

# Marekebisho ya ngeli yenye mipaka kali: yanashika tu maumbo mahususi yaliyothibitishwa kuwa makosa.
# Hakuna "[^.?!]*?" inayoruka maneno ovyo, kwa hiyo sentensi sahihi hazigusiwi.
_NGELI_MAUMBO_MAALUM = [
    (re.compile(r"\bmashirika\s+madogomadogo\s+vya\b", re.IGNORECASE), "mashirika madogomadogo ya"),
    (re.compile(r"\byamekuwa\s+vikichelewa\b", re.IGNORECASE), "yamekuwa yakichelewa"),
    (re.compile(r"\byamekuwa\s+vikisuasua\b", re.IGNORECASE), "yamekuwa yakisuasua"),
    (re.compile(r"\bmafanikio\s+kubwa\b", re.IGNORECASE), "mafanikio makubwa"),
]

# ukosefu/uhaba/upungufu (U-umoja) + "wa" + maneno 1-2 + "imekuwa"  ->  "umekuwa"
# Kikomo cha maneno 1-2 na kutokuwepo kwa alama katikati huzuia kugusa "hali imekuwa", "serikali imekuwa".
_NGELI_U_UMOJA = re.compile(
    r"\b(ukosefu|uhaba|upungufu)(\s+wa\s+\w+(?:\s+\w+)?\s+)imekuwa\b", re.IGNORECASE
)


def _rekebisha_ngeli(maandishi: str) -> str:
    for rx, sahihi in _NGELI_MAUMBO_MAALUM:
        maandishi = rx.sub(
            lambda m, s=sahihi: (s[0].upper() + s[1:]) if m.group(0)[:1].isupper() else s,
            maandishi,
        )
    return _NGELI_U_UMOJA.sub(lambda m: m.group(1) + m.group(2) + "umekuwa", maandishi)


def _badilisha_tahajia(m: "re.Match") -> str:
    asili = m.group(0)
    sahihi = _TAHAJIA[re.sub(r"\s+", " ", asili.lower())]
    return sahihi.capitalize() if asili[:1].isupper() else sahihi


def safisha_maandishi_sanifu(maandishi: str) -> str:
    if not maandishi:
        return ""

    maandishi = _RUDIA_RX.sub(r"\1", maandishi)
    maandishi = _TAHAJIA_RX.sub(_badilisha_tahajia, maandishi)
    maandishi = _rekebisha_ngeli(maandishi)

    maandishi = re.sub(r"[ \t]{2,}", " ", maandishi)              # nafasi mbili au zaidi
    maandishi = re.sub(r"[ \t]+([,.;:!?])", r"\1", maandishi)     # nafasi kabla ya alama
    maandishi = re.sub(r"(?<!\.)\.\.(?!\.)", ".", maandishi)      # ".." -> "." (nukta tatu zinabaki)
    maandishi = maandishi.strip()
    if maandishi.endswith(","):
        maandishi = maandishi[:-1] + "."                          # mkato mwishoni -> nukta
    return maandishi


def _safisha_jibu_la_ai(maandishi: str) -> str:
    """Huondoa uzio wa ``` au nukuu zilizozunguka jibu zima la AI."""
    t = maandishi.strip()
    t = re.sub(r"^```[a-zA-Z]*\s*\n?", "", t)
    t = re.sub(r"\n?```$", "", t)
    return t.strip()


# ------------------------------------------------------------------
# 4. MAELEKEZO YA AI
# ------------------------------------------------------------------
SYSTEM_PROMPT = """
Wewe ni Mhariri Mkuu na Mtafsiri Bingwa wa Kiswahili Sanifu (AI Lingual Africa Sanifu).
Fuata sheria hizi kali bila kukosea:
1. NGELI ZA KISWAHILI:
   - 'matumizi', 'mafanikio', 'maoni' (wingi) huchukua 'ya-' ('yamesababisha', 'yamekuwa'), KAMWE 'i-' wala 'vi-'.
   - 'mtazamo', 'ukosefu', 'mkutano' (U-I umoja) huchukua 'u-' ('umekuwa') na 'm-' ('mkutano mfupi').
   - 'kikwazo' (KI-VI umoja) huchukua 'ki-' ('kikwazo kikubwa').
   - 'mashirika', 'majukwaa', 'mataifa' (wingi) huchukua 'ma-'/'ya-' ('mashirika madogomadogo', 'majukwaa yatakayotoa').
   - Vitenzi-jina ('Kuwekeza...', 'Kupuuza...') hubaki na 'ku-' ('kukilinda', 'kunaweza').
   - Kitenzi lazima kioane na nomino halisi inayotenda, si nomino iliyo karibu tu.
2. KIVUMISHI 'KILA': Sentensi ikianza na 'Kila' + nomino ya umoja ('Kila mkulima'), vitenzi VYOTE na viwakilishi VYOTE viwe UMOJA.
3. SHAMIRISHO NA WAKATI: 'anapojali afya' (siyo 'anapowajali afya'). Kitenzi kikuu baada ya kitenzi-jina kichukue wakati ujao ('kutasaidia') au mazoea ('husaidia').
4. UAMINIFU: Usiongeze sentensi wala maneno mapya (isipokuwa maneno sanifu yanayochukua nafasi ya Kiingereza kwa sheria 4B). Usibadilishe maneno ambayo tayari ni sahihi.
4B. UKALI WA KUONDOA KIINGEREZA (STRICT NO CODE-SWITCHING):
   - Unapohariri Kiswahili, ondoa kila neno la Kiingereza lililochanganywa katikati ya sentensi ya Kiswahili, pamoja na miundo ya kiambishi + '-' + kitenzi cha Kiingereza (mfano: 'ku-launch', 'ana-post', 'nime-manage'). Badilisha kwa neno sanifu la Kiswahili lenye maana ileile, kisha hakikisha ngeli na viambishi vinaoana na neno jipya.
   - Mifano: ku-launch -> kuanzisha; ku-post -> kuchapisha; ku-attract -> kuvutia; ku-manage -> kusimamia; ku-build brand -> kujenga chapa; capital -> mtaji; platforms -> majukwaa; transactions -> miamala; online -> mtandaoni; business plan -> mpango wa biashara; records -> kumbukumbu; loans -> mikopo; digital marketing -> masoko ya kidijitali.
   - USIBADILISHE: majina maalum ya watu, chapa, kampuni na bidhaa (Facebook, WhatsApp, Pesapal); URL na barua pepe; msimbo; nukuu ndani ya alama za nukuu; sentensi zilizoandikwa kwa Kiingereza kikamilifu kwa makusudi.
   - Katika tafsiri (EN -> SW), matokeo yote yawe Kiswahili; usiache neno la Kiingereza isipokuwa jina maalum.
5. TAFSIRI (EN -> SW): Tafsiri maana halisi na misemo kwa ufasaha (si neno kwa neno). Tunza msisitizo wa 'not only... but also' ('si tu... bali pia').
6. MUUNDO: Dumisha vichwa vya habari, orodha na namba kama zilivyo. Hifadhi majina ya watu, vifupisho na nambari.
7. MATOKEO: Toa matokeo yaliyohaririwa/kutafsiriwa PEKEE, bila maelezo ya ziada, bila nukuu, bila alama za ```.
"""

SYSTEM_UKAGUZI = """
Wewe ni Mkaguzi wa Kiswahili Sanifu. Utapewa maandishi ya Kiswahili yaliyokwisha haririwa/tafsiriwa.
Kazi yako ni kurekebisha TU makosa ya wazi ya: ngeli (makubaliano ya nomino na kitenzi/kivumishi), tahajia,
wakati wa kitenzi, na alama za uandishi.
Sheria:
- USIBADILISHE maana, mpangilio wa mawazo, wala msamiati ulio sahihi. Usiongeze wala kupunguza sentensi.
- Kama hakuna kosa, rudisha maandishi yaleyale bila mabadiliko yoyote.
- 'matumizi', 'mafanikio', 'maoni' huchukua 'ya-'; 'kila' + nomino ya umoja huhitaji vitenzi vya umoja.
- Mifano ya makosa ya kurekebisha (kosa -> sahihi):
  * 'mashirika madogomadogo vya wakulima' -> 'mashirika madogomadogo ya wakulima' (mashirika huchukua 'ya')
  * 'malipo yamekuwa vikichelewa' -> 'malipo yamekuwa yakichelewa'
  * 'maendeleo yamekuwa vikisuasua' -> 'maendeleo yamekuwa yakisuasua'
  * 'ukosefu wa ajira imekuwa tatizo' -> 'ukosefu wa ajira umekuwa tatizo' (ukosefu, uhaba, upungufu huchukua 'u-')
- Kama maandishi yana neno la Kiingereza lililochanganywa na Kiswahili (mfano 'ku-launch', 'online'), libadilishe na neno sanifu la Kiswahili, na ulinde majina maalum, URL, barua pepe na nukuu.
- Kitenzi huoana na nomino inayotenda, si nomino iliyo karibu: 'ukosefu wa ajira umeongezeka, na hali imekuwa mbaya' ni SAHIHI (usibadilishe 'hali imekuwa').
- Toa maandishi yaliyokaguliwa PEKEE, bila maelezo, bila nukuu, bila alama za ```.
"""


# ------------------------------------------------------------------
# 5. KUITA AI (Gemini kwanza, Groq akiba)
# ------------------------------------------------------------------
def _ni_kosa_la_muda(e: Exception) -> bool:
    """429/500/503/504 au tatizo la mtandao: inafaa kujaribu tena. 400/401/403/404: usijaribu tena."""
    code = getattr(e, "code", None)
    return code is None or code in (429, 500, 502, 503, 504)


def _ita_gemini(system: str, ujumbe: str):
    if not gemini_client:
        print("Gemini: GEMINI_API_KEY haijawekwa kwenye Render.")
        return None
    modeli = [GEMINI_MODEL]
    if GEMINI_FALLBACK_MODEL and GEMINI_FALLBACK_MODEL != GEMINI_MODEL:
        modeli.append(GEMINI_FALLBACK_MODEL)

    for modeli_jina in modeli:
        for jaribio in range(2):
            try:
                jibu = gemini_client.models.generate_content(
                    model=modeli_jina,
                    contents=ujumbe,
                    config=types.GenerateContentConfig(system_instruction=system, temperature=0.0),
                )
                if jibu and jibu.text:
                    return jibu.text.strip()
                print(f"Gemini ({modeli_jina}): jibu tupu (huenda limezuiwa).")
                break  # jibu tupu (mf. limezuiwa): jaribu modeli inayofuata
            except Exception as e:
                print(f"Hitilafu ya Gemini ({modeli_jina}, jaribio {jaribio + 1}): {e}")
                if not _ni_kosa_la_muda(e):
                    break  # mf. modeli haipo (404): nenda modeli inayofuata mara moja
                time.sleep(1.5 * (jaribio + 1))
    return None


def _ita_groq(system: str, ujumbe: str):
    if not groq_client:
        print("Groq: GROQ_API_KEY haijawekwa kwenye Render.")
        return None
    try:
        chat = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=0.0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": ujumbe},
            ],
        )
        maudhui = chat.choices[0].message.content  # choices ni orodha
        return maudhui.strip() if maudhui else None
    except Exception as e:
        print(f"Hitilafu ya Groq: {e}")
        return None


def ita_ai(system: str, ujumbe: str):
    """Hurudisha (maandishi, injini). Kama zote zimeshindwa: (None, None)."""
    jibu = _ita_gemini(system, ujumbe)
    if jibu:
        return _safisha_jibu_la_ai(jibu), "gemini"
    jibu = _ita_groq(system, ujumbe)
    if jibu:
        return _safisha_jibu_la_ai(jibu), "groq"
    return None, None


# ------------------------------------------------------------------
# 6. UCHAKATAJI WA KIPANDE KIMOJA (HATUA YA 1 + HATUA YA 2 + ULINZI)
# ------------------------------------------------------------------
def _uwiano_unakubalika(asili: str, matokeo: str, kitendo: str) -> bool:
    """Ulinzi dhidi ya AI kuongeza maelezo au kukata maneno."""
    if not matokeo.strip():
        return False
    ratio = len(matokeo) / max(len(asili), 1)
    if kitendo == "tafsiri":
        return 0.3 <= ratio <= 3.0
    return 0.6 <= ratio <= 1.8


def chakata_kipande(kipande: str, kitendo: str, hatua_mbili=None) -> dict:
    if hatua_mbili is None:
        hatua_mbili = HATUA_MBILI

    # --- Hatua ya 1: kuhariri / kutafsiri ---
    if kitendo == "tafsiri":
        vidokezo = pata_vidokezo_vya_kamusi(kipande)
        ujumbe = f"Tafsiri aya hii kwenda Kiswahili Sanifu fasaha:{vidokezo}\n\n{kipande}"
    else:
        # Sheria 4B: ondoa Kiingereza kabla ya AI, ili AI ione Kiswahili na irekebishe ngeli.
        kipande_cha_ai = ondoa_kiingereza(kipande)
        ujumbe = (
            "Hariri sarufi, ngeli, tahajia, na alama za uandishi za aya hii ya Kiswahili, "
            "ukiondoa maneno ya Kiingereza yaliyochanganywa (sheria 4B), "
            f"bila kuongeza maneno mengine mapya:\n\n{kipande_cha_ai}"
        )

    hatua1, injini = ita_ai(SYSTEM_PROMPT, ujumbe)
    if not hatua1:
        print(f"Kipande kimeshindwa: Gemini na Groq hazikujibu (herufi {len(kipande)}).")
        return {"text": kipande, "ok": False, "injini": None, "hatua2": False}

    if not _uwiano_unakubalika(kipande, hatua1, kitendo):
        # AI imeongeza/kupunguza kupita kiasi: kwenye uhariri tunarudi kwenye asili
        if kitendo != "tafsiri":
            print(f"Kipande kimekataliwa na kinga ya urefu: asili={len(kipande)}, jibu la {injini}={len(hatua1)}. Jibu: {hatua1[:120]!r}")
            return {"text": kipande, "ok": False, "injini": injini, "hatua2": False}

    matokeo, ilitumia_hatua2 = hatua1, False

    # --- Hatua ya 2: ukaguzi wa ngeli/sarufi bila kubadilisha maana ---
    if hatua_mbili:
        if kitendo == "tafsiri":
            ujumbe2 = (
                f"Maandishi asili (Kiingereza), kwa kumbukumbu ya maana tu:\n{kipande}\n\n"
                f"Tafsiri ya Kiswahili ya kukagua:\n{hatua1}"
            )
        else:
            ujumbe2 = f"Maandishi ya kukagua:\n{hatua1}"
        hatua2, _ = ita_ai(SYSTEM_UKAGUZI, ujumbe2)
        # Kubali ukaguzi tu ikiwa haujabadilisha urefu sana
        if hatua2 and 0.8 <= len(hatua2) / max(len(hatua1), 1) <= 1.25:
            matokeo, ilitumia_hatua2 = hatua2, True

    return {"text": matokeo, "ok": True, "injini": injini, "hatua2": ilitumia_hatua2}


# ------------------------------------------------------------------
# 7. KUGAWA MAANDISHI (hudumisha mistari, orodha na vichwa)
# ------------------------------------------------------------------
def _gawa_mstari_mrefu(mstari: str) -> list:
    if len(mstari) <= MAX_KIPANDE:
        return [mstari]
    sentensi = re.split(r"(?<=[.!?])\s+", mstari)
    vipande, sasa = [], ""
    for s in sentensi:
        if sasa and len(sasa) + len(s) + 1 > MAX_KIPANDE:
            vipande.append(sasa)
            sasa = s
        else:
            sasa = f"{sasa} {s}".strip()
    if sasa:
        vipande.append(sasa)
    return vipande


def _ina_herufi(s: str) -> bool:
    return bool(re.search(r"[^\W\d_]", s))


# ------------------------------------------------------------------
# 8. MSINGI WA UCHAKATAJI (unatumiwa na /hariri, /tafsiri, /pendekezo na /v1/kagua)
# ------------------------------------------------------------------
def chakata_maandishi(maandishi: str, kitendo: str, hatua_mbili=None) -> dict:
    """
    Hugawa maandishi kwa mistari, huchakata kwa sambamba, na kurudisha kila mstari
    pamoja na nafasi yake (mwanzo) kwenye maandishi ya awali.
    """
    mistari = maandishi.split("\n")
    muundo, vipande, mwanzo = [], [], 0
    for mstari in mistari:
        if not mstari.strip() or not _ina_herufi(mstari):
            muundo.append(("kama_ilivyo", 0, mwanzo, mstari))
        else:
            sehemu = _gawa_mstari_mrefu(mstari.strip())
            muundo.append(("chakata", len(sehemu), mwanzo, mstari))
            vipande.extend(sehemu)
        mwanzo += len(mstari) + 1

    majibu = []
    if vipande:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as mtambo:
            majibu = list(mtambo.map(lambda k: chakata_kipande(k, kitendo, hatua_mbili), vipande))

    mistari_matokeo, idx = [], 0
    for aina, idadi, mwanzo_m, asili_m in muundo:
        if aina == "kama_ilivyo":
            matokeo_m = asili_m
        else:
            # Sheria 4B: kichujio baada ya AI kama kinga, kisha chujio salama la sanifu.
            safi = [
                safisha_maandishi_sanifu(ondoa_kiingereza(majibu[idx + i]["text"]))
                for i in range(idadi)
            ]
            idx += idadi
            kichwani = asili_m[: len(asili_m) - len(asili_m.lstrip())]   # hifadhi nafasi za mwanzo (indent)
            mkiani = asili_m[len(asili_m.rstrip()):]
            matokeo_m = kichwani + " ".join(safi) + mkiani
        mistari_matokeo.append(
            {"aina": aina, "asili": asili_m, "matokeo": matokeo_m, "mwanzo": mwanzo_m}
        )

    return {
        "mistari": mistari_matokeo,
        "majibu": majibu,
        "matokeo": "\n".join(m["matokeo"] for m in mistari_matokeo),
    }


def muhtasari_wa_majibu(majibu: list) -> dict:
    return {
        "jumla": len(majibu),
        "zilizoshindwa": sum(1 for j in majibu if not j["ok"]),
        "injini": sorted({j["injini"] for j in majibu if j["injini"]}),
        "hatua2": sum(1 for j in majibu if j["hatua2"]),
    }


# ------------------------------------------------------------------
# 9. MAPENDEKEZO YA KUBALI / PUUZA (kama Grammarly)
#    Tunalinganisha maandishi asili na yaliyohaririwa neno kwa neno, kisha kila
#    tofauti inakuwa pendekezo lenye nafasi kamili (mwanzo, mwisho) kwenye maandishi asili.
# ------------------------------------------------------------------
_TOKENI_RX = re.compile(r"(\s*)(\w+|[^\w\s])", re.UNICODE)
_NENO_RX = re.compile(r"\w+", re.UNICODE)


def _tokeni(s: str) -> list:
    tokeni = []
    for m in _TOKENI_RX.finditer(s):
        tokeni.append({
            "t": m.group(2),
            "s": m.start(2),                                   # mwanzo wa neno
            "e": m.end(2),                                     # mwisho wa neno
            "ws": m.start(1) if m.group(1) else m.start(2),    # mwanzo ikijumuisha nafasi iliyotangulia
            "pengo": bool(m.group(1)),                         # kuna nafasi kabla ya neno?
        })
    return tokeni


def _ni_ngeli(a: str, b: str) -> bool:
    """Maneno mawili yenye mwisho mmoja mrefu na viambishi tofauti vifupi (mf. imekuwa -> umekuwa)."""
    if a.lower() == b.lower():
        return False
    n = 0
    while n < min(len(a), len(b)) and a[-1 - n].lower() == b[-1 - n].lower():
        n += 1
    return n >= 4 and (len(a) - n) <= 4 and (len(b) - n) <= 4


def _aina_na_maelezo(asili: str, mpya: str):
    kawaida = re.sub(r"\s+", " ", asili.lower()).strip()
    if kawaida in _TAHAJIA:
        return "tahajia", f"Tahajia sahihi ni '{_TAHAJIA[kawaida]}'."

    if ina_kiingereza(asili) and not ina_kiingereza(mpya):
        return "kiingereza", "Neno la Kiingereza limebadilishwa na neno sanifu la Kiswahili."

    wa, wb = _NENO_RX.findall(asili), _NENO_RX.findall(mpya)
    if wa == wb:
        if re.sub(r"\s+", "", asili) == re.sub(r"\s+", "", mpya):
            return "nafasi", "Nafasi kabla au baada ya alama za uandishi zimerekebishwa."
        return "alama", "Alama za uandishi zimerekebishwa."
    if [w.lower() for w in wa] == [w.lower() for w in wb]:
        return "herufi", "Herufi kubwa au ndogo zimerekebishwa."

    bila_kurudia = [w for i, w in enumerate(wa) if i == 0 or w.lower() != wa[i - 1].lower()]
    if len(wa) > len(wb) and bila_kurudia == wb:
        return "kujirudia", "Neno limejirudia bila sababu; limeondolewa."

    if len(wa) == len(wb):
        tofauti = [(x, y) for x, y in zip(wa, wb) if x != y]
        if tofauti and all(_ni_ngeli(x, y) for x, y in tofauti):
            x, y = tofauti[0]
            return "ngeli", f"Kiambishi cha ngeli kimerekebishwa ('{x}' -> '{y}') ili kioane na nomino husika."
        if len(wa) == 1:
            if difflib.SequenceMatcher(None, wa[0].lower(), wb[0].lower()).ratio() >= 0.75:
                return "tahajia", f"Tahajia imerekebishwa ('{wa[0]}' -> '{wb[0]}')."
            return "msamiati", f"Neno limebadilishwa kwa msamiati unaofaa zaidi ('{wa[0]}' -> '{wb[0]}')."
    return "sarufi", "Sentensi imerekebishwa kisarufi au kimtindo."


def _tengeneza_mapendekezo(asili: str, mpya: str, mwanzo_wa_asili: int = 0) -> list:
    ta, tb = _tokeni(asili), _tokeni(mpya)
    sm = difflib.SequenceMatcher(
        a=[(t["t"], t["pengo"]) for t in ta],
        b=[(t["t"], t["pengo"]) for t in tb],
        autojunk=False,
    )

    spans = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        # Kufuta neno lililorudiwa: onyesha maneno yote mawili
        if j1 == j2 and i2 < len(ta) and j1 < len(tb) and ta[i2]["t"].lower() == ta[i2 - 1]["t"].lower():
            i2, j2 = i2 + 1, j2 + 1
        # Kuongeza/kufuta tupu: panua kwa neno jirani ili pendekezo liwe na msingi
        elif i1 == i2 or j1 == j2:
            if i1 > 0 and j1 > 0:
                i1, j1 = i1 - 1, j1 - 1
            elif i2 < len(ta) and j2 < len(tb):
                i2, j2 = i2 + 1, j2 + 1

        a_s = ta[i1]["s"] if i1 < len(ta) else len(asili)
        b_s = tb[j1]["s"] if j1 < len(tb) else len(mpya)
        if i1 < len(ta) and j1 < len(tb) and ta[i1]["pengo"] != tb[j1]["pengo"]:
            a_s, b_s = ta[i1]["ws"], tb[j1]["ws"]          # badiliko la nafasi mwanzoni mwa pendekezo
        a_e = ta[i2 - 1]["e"] if i2 > i1 else a_s
        b_e = tb[j2 - 1]["e"] if j2 > j1 else b_s
        spans.append([a_s, a_e, b_s, b_e])

    # Unganisha mapendekezo yanayogusana ili nafasi zisigongane
    zilizounganishwa = []
    for sp in spans:
        if zilizounganishwa and (sp[0] <= zilizounganishwa[-1][1] or sp[2] <= zilizounganishwa[-1][3]):
            zilizounganishwa[-1][1] = max(zilizounganishwa[-1][1], sp[1])
            zilizounganishwa[-1][3] = max(zilizounganishwa[-1][3], sp[3])
        else:
            zilizounganishwa.append(sp)

    matokeo = []
    for a_s, a_e, b_s, b_e in zilizounganishwa:
        sa, sb = asili[a_s:a_e], mpya[b_s:b_e]
        if sa == sb:
            continue
        aina, maelezo = _aina_na_maelezo(sa, sb)
        matokeo.append({
            "mwanzo": mwanzo_wa_asili + a_s,
            "mwisho": mwanzo_wa_asili + a_e,
            "asili": sa,                 # ni hasa maandishi yaliyo kati ya mwanzo na mwisho
            "pendekezo": sb,             # yanachukua nafasi ya "asili"
            "kutoka": sa.strip(),        # kwa kuonyesha kwenye pop-up
            "kuwa": sb.strip(),
            "aina": aina,
            "maelezo": maelezo,
        })
    return matokeo


def mapendekezo_ya_maandishi(mistari: list) -> list:
    yote = []
    for m in mistari:
        if m["aina"] != "chakata" or m["asili"].strip() == m["matokeo"].strip():
            continue
        asili = m["asili"]
        kichwani = len(asili) - len(asili.lstrip())
        yote.extend(
            _tengeneza_mapendekezo(asili.strip(), m["matokeo"].strip(), m["mwanzo"] + kichwani)
        )
    for i, p in enumerate(yote):
        p["id"] = i
    return yote


def tumia_mapendekezo(maandishi: str, mapendekezo: list, ids=None) -> str:
    """Tumia mapendekezo yote (Kubali yote) au yale ya ids pekee. Hufanya kazi kutoka mwisho kwenda mwanzo."""
    chaguo = [m for m in mapendekezo if ids is None or m["id"] in ids]
    for m in sorted(chaguo, key=lambda x: x["mwanzo"], reverse=True):
        maandishi = maandishi[: m["mwanzo"]] + m["pendekezo"] + maandishi[m["mwisho"]:]
    return maandishi


# ------------------------------------------------------------------
# 9B. MUUNDO WA CHROME EXTENSION (/v1/kagua)
#     Extension inatarajia: {ok, ai, issues:[{original, suggestion, start, end, label, explanation, hiari}]}
#     start/end ni nafasi za UTF-16 kwenye maandishi yaliyotumwa (lingual_utils.js inazihitaji).
# ------------------------------------------------------------------
_LEBO_ZA_AINA = {
    "tahajia": "Tahajia",
    "ngeli": "Ngeli",
    "kiingereza": "Kiingereza",
    "nafasi": "Nafasi",
    "alama": "Alama za uandishi",
    "herufi": "Herufi kubwa/ndogo",
    "kujirudia": "Neno limejirudia",
    "msamiati": "Msamiati",
    "sarufi": "Sarufi",
}
# Mapendekezo ya mtindo/msamiati ni ya hiari (hayajumuishwi kwenye "Kubali yote")
_AINA_ZA_HIARI = {"msamiati", "sarufi"}


def _u16(s: str, i: int) -> int:
    """Nafasi ya code points (Python) -> nafasi ya UTF-16 (JavaScript). Tofauti hutokea kwa emoji."""
    return len(s[:i].encode("utf-16-le", "surrogatepass")) // 2


def _kwa_extension(maandishi: str, mapendekezo: list) -> list:
    """
    Hubadilisha mapendekezo kuwa muundo wa extension. Kila kosa lina start/end (UTF-16) kwenye
    maandishi yaliyotumwa; lingual_utils.js (hifadhiMajibu) inazihitaji kupanga makosa kwa sentensi.
    """
    issues = []
    for p in mapendekezo:
        original, suggestion = p["kutoka"], p["kuwa"]
        if not original or not suggestion or original == suggestion:
            continue
        anza = p["mwanzo"] + (len(p["asili"]) - len(p["asili"].lstrip()))
        mwisho = anza + len(original)
        if maandishi[anza:mwisho] != original:   # kinga: nafasi lazima ilingane na maandishi
            continue
        issues.append({
            "original": original,
            "suggestion": suggestion,
            "start": _u16(maandishi, anza),
            "end": _u16(maandishi, mwisho),
            "label": _LEBO_ZA_AINA.get(p["aina"], "Mengineyo"),
            "explanation": p["maelezo"],
            "hiari": p["aina"] in _AINA_ZA_HIARI,
        })
    return issues


# ------------------------------------------------------------------
# 10. NJIA (ROUTES)
# ------------------------------------------------------------------
def _soma_ombi():
    data = request.get_json(silent=True) or {}
    maandishi = data.get("text") or data.get("maandishi") or ""
    kitendo = str(data.get("mode") or data.get("kitendo") or "hariri").lower()
    return maandishi, kitendo


def _kagua_maandishi(maandishi):
    if not isinstance(maandishi, str) or not maandishi.strip():
        return jsonify({"ok": False, "kosa": "MAANDISHI_TUPU",
                        "error": "Tafadhali weka maandishi kwanza."}), 400
    if len(maandishi) > MAX_CHARS:
        return jsonify({
            "ok": False,
            "kosa": "MAANDISHI_MAREFU",
            "error": f"Maandishi ni marefu mno (herufi {len(maandishi)}). Kikomo ni {MAX_CHARS}. Yagawe sehemu sehemu.",
        }), 413
    if not any(_ina_herufi(m) for m in maandishi.split("\n")):
        return jsonify({"ok": False, "kosa": "MAANDISHI_TUPU",
                        "error": "Hakuna maandishi ya kuchakata."}), 400
    return None


def _ai_hazipatikani():
    return jsonify({
        "ok": False,
        "kosa": "AI_HAZIPATIKANI",
        "error": "Huduma za AI hazipatikani kwa sasa. Jaribu tena baadaye.",
        "imechakatwa": False,
    }), 502


@app.route("/api/chakata", methods=["POST"])
@app.route("/hariri", methods=["POST"])
@app.route("/tafsiri", methods=["POST"])
def huduma_ya_lugha():
    maandishi, kitendo = _soma_ombi()
    if request.path.endswith("/tafsiri") or kitendo in ("tafsiri", "translate"):
        kitendo = "tafsiri"
    else:
        kitendo = "hariri"

    kosa = _kagua_maandishi(maandishi)
    if kosa:
        return kosa

    r = chakata_maandishi(maandishi, kitendo)
    muh = muhtasari_wa_majibu(r["majibu"])
    if muh["zilizoshindwa"] == muh["jumla"]:
        return _ai_hazipatikani()

    return jsonify({
        "ok": True,
        "matokeo": r["matokeo"],
        "result": r["matokeo"],
        "imechakatwa": muh["zilizoshindwa"] == 0,   # false = baadhi ya vipande vimerudishwa kama vilivyo
        "vipande_vilivyoshindwa": muh["zilizoshindwa"],
        "vipande_jumla": muh["jumla"],
        "injini_iliyotumika": muh["injini"],
        "ukaguzi_wa_pili": muh["hatua2"],
    })


@app.route("/pendekezo", methods=["POST"])
@app.route("/api/pendekezo", methods=["POST"])
def huduma_ya_mapendekezo():
    """
    Hurudisha mapendekezo ya Kubali / Puuza. Kila pendekezo:
      {id, mwanzo, mwisho, asili, pendekezo, kutoka, kuwa, aina, maelezo}
    mwanzo/mwisho ni nafasi (code points) kwenye maandishi yaliyotumwa; maandishi[mwanzo:mwisho] == asili.
    "Kubali" = badilisha asili kwa pendekezo. "Kubali yote" = tumia maandishi_yaliyohaririwa.
    """
    maandishi, _ = _soma_ombi()
    kosa = _kagua_maandishi(maandishi)
    if kosa:
        return kosa

    r = chakata_maandishi(maandishi, "hariri")
    muh = muhtasari_wa_majibu(r["majibu"])
    if muh["zilizoshindwa"] == muh["jumla"]:
        return _ai_hazipatikani()

    mapendekezo = mapendekezo_ya_maandishi(r["mistari"])
    return jsonify({
        "ok": True,
        "mapendekezo": mapendekezo,
        "idadi": len(mapendekezo),
        "maandishi_yaliyohaririwa": r["matokeo"],
        "imechakatwa": muh["zilizoshindwa"] == 0,
        "vipande_vilivyoshindwa": muh["zilizoshindwa"],
        "injini_iliyotumika": muh["injini"],
        "ukaguzi_wa_pili": muh["hatua2"],
    })


@app.route("/v1/kagua", methods=["POST"])
@app.route("/api/kagua", methods=["POST"])
@app.route("/kagua", methods=["POST"])
def huduma_ya_extension():
    """
    Njia ya Chrome extension ya Lingual Sanifu (background.js).
    Ombi:  {"text": "..."}  + header X-API-Key
    Jibu:  {"ok": true, "ai": true, "issues": [{original, suggestion, start, end, label, explanation, hiari}]}
    Kwa kasi, hatua ya pili ya ukaguzi imezimwa hapa kwa chaguo-msingi (KAGUA_HATUA_MBILI=0).
    """
    maandishi, _ = _soma_ombi()
    kosa = _kagua_maandishi(maandishi)
    if kosa:
        return kosa

    r = chakata_maandishi(maandishi, "hariri", hatua_mbili=KAGUA_HATUA_MBILI)
    muh = muhtasari_wa_majibu(r["majibu"])
    if muh["zilizoshindwa"] == muh["jumla"]:
        return _ai_hazipatikani()

    issues = _kwa_extension(maandishi, mapendekezo_ya_maandishi(r["mistari"]))
    return jsonify({
        "ok": True,
        # ai=false ikiwa baadhi ya vipande vimeshindwa: extension isihifadhi jibu hili kwenye akiba
        "ai": muh["zilizoshindwa"] == 0,
        "issues": issues,
        "idadi": len(issues),
        "injini_iliyotumika": muh["injini"],
    })


@app.route("/uchunguzi", methods=["GET"])
def uchunguzi():
    """
    Hujaribu Gemini na Groq kwa ombi dogo na kuonyesha kosa halisi (bila kuonyesha funguo).
    Fungua kwenye kivinjari: /uchunguzi  (au /uchunguzi?ufunguo=API_KEY yako, ikiwa umeweka API_KEY).
    """
    if API_KEY_YA_HUDUMA and not hmac.compare_digest(request.args.get("ufunguo", ""), API_KEY_YA_HUDUMA):
        return jsonify({"ok": False, "error": "Weka ?ufunguo=<API_KEY> mwishoni mwa anwani."}), 401

    def jaribu(fn):
        t0 = time.time()
        try:
            out = fn()
            return {"ok": bool(out), "sekunde": round(time.time() - t0, 1), "jibu": (out or "")[:80]}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "sekunde": round(time.time() - t0, 1),
                    "kosa": f"{type(e).__name__}: {str(e)[:300]}", "code": getattr(e, "code", None)}

    ujumbe = "Jibu kwa neno moja tu: sawa"
    matokeo = {"gemini": {}, "groq": None}

    if gemini_client:
        for jina in dict.fromkeys([GEMINI_MODEL, GEMINI_FALLBACK_MODEL]):
            if not jina:
                continue
            matokeo["gemini"][jina] = jaribu(
                lambda j=jina: gemini_client.models.generate_content(model=j, contents=ujumbe).text
            )
    else:
        matokeo["gemini"] = {"kosa": "GEMINI_API_KEY haijawekwa kwenye Render"}

    if groq_client:
        matokeo["groq"] = {GROQ_MODEL: jaribu(
            lambda: groq_client.chat.completions.create(
                model=GROQ_MODEL, messages=[{"role": "user", "content": ujumbe}]
            ).choices[0].message.content
        )}
    else:
        matokeo["groq"] = {"kosa": "GROQ_API_KEY haijawekwa kwenye Render"}

    return jsonify(matokeo)


@app.route("/health", methods=["GET"])
def afya_nyepesi():
    """Nyepesi sana: extension huitumia kuamsha seva ya Render iliyolala."""
    return jsonify({"status": "ok"})


@app.route("/", methods=["GET"])
def afya_ya_seva():
    return jsonify({
        "status": "Live",
        "mfumo": "AI Lingual Africa Sanifu API v3.3",
        "injini": f"{GEMINI_MODEL} (akiba: {GEMINI_FALLBACK_MODEL}) + Groq {GROQ_MODEL} + Ukaguzi wa Pili + Chujio salama",
        "njia": ["/api/chakata", "/hariri", "/tafsiri", "/pendekezo", "/v1/kagua", "/health"],
        "gemini": bool(gemini_client),
        "groq": bool(groq_client),
        "hatua_mbili": HATUA_MBILI,
        "kagua_hatua_mbili": KAGUA_HATUA_MBILI,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
