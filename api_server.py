"""
AI Lingual Africa Sanifu API v3.1
Gemini 2.5 Flash (kuu) + Groq Llama 3.3 70B (akiba) + Hatua ya Pili ya Ukaguzi + Chujio salama la Python

Njia zilezile: /api/chakata, /hariri, /tafsiri  (extension haihitaji kubadilishwa)
Funguo za JSON zilezile: ok, matokeo, result

Environment Variables (Render):
  GEMINI_API_KEY   (inapendekezwa)
  GROQ_API_KEY     (akiba)
  API_KEY          (hiari) -> ikiwekwa, extension itume header: X-API-Key
  ALLOWED_ORIGINS  (hiari) -> mfano: chrome-extension://abcdef...,https://tovuti-yako.com  (chaguo-msingi: *)
  HATUA_MBILI      (hiari) -> "1" (chaguo-msingi) au "0" kuzima ukaguzi wa pili
  MAX_CHARS        (hiari) -> kikomo cha herufi, chaguo-msingi 15000
  MAX_WORKERS      (hiari) -> uchakataji sambamba, chaguo-msingi 3
  GEMINI_MODEL, GROQ_MODEL (hiari)
"""
import os
import re
import hmac
import time
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from groq import Groq

# ------------------------------------------------------------------
# 1. MIPANGILIO
# ------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
API_KEY_YA_HUDUMA = os.environ.get("API_KEY")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").strip()
HATUA_MBILI = os.environ.get("HATUA_MBILI", "1") == "1"
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
    if request.method == "OPTIONS" or request.path == "/":
        return None
    ulioletwa = request.headers.get("X-API-Key", "")
    if not hmac.compare_digest(ulioletwa, API_KEY_YA_HUDUMA):
        return jsonify({"ok": False, "error": "Huna ruhusa ya kutumia huduma hii."}), 401
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
4. UAMINIFU: Usiongeze sentensi wala maneno mapya. Usibadilishe maneno ambayo tayari ni sahihi. Ondoa maneno ya Kiingereza yaliyochanganywa ('ku-export' -> 'kuuza nje').
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
- Kitenzi huoana na nomino inayotenda, si nomino iliyo karibu: 'ukosefu wa ajira umeongezeka, na hali imekuwa mbaya' ni SAHIHI (usibadilishe 'hali imekuwa').
- Toa maandishi yaliyokaguliwa PEKEE, bila maelezo, bila nukuu, bila alama za ```.
"""


# ------------------------------------------------------------------
# 5. KUITA AI (Gemini kwanza, Groq akiba)
# ------------------------------------------------------------------
def _ita_gemini(system: str, ujumbe: str):
    if not gemini_client:
        return None
    for jaribio in range(2):
        try:
            jibu = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=ujumbe,
                config=types.GenerateContentConfig(system_instruction=system, temperature=0.0),
            )
            if jibu and jibu.text:
                return jibu.text.strip()
            return None  # jibu tupu (mf. limezuiwa): nenda Groq
        except Exception as e:
            print(f"Hitilafu ya Gemini (jaribio {jaribio + 1}): {e}")
            time.sleep(1.5 * (jaribio + 1))
    return None


def _ita_groq(system: str, ujumbe: str):
    if not groq_client:
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


def chakata_kipande(kipande: str, kitendo: str) -> dict:
    # --- Hatua ya 1: kuhariri / kutafsiri ---
    if kitendo == "tafsiri":
        vidokezo = pata_vidokezo_vya_kamusi(kipande)
        ujumbe = f"Tafsiri aya hii kwenda Kiswahili Sanifu fasaha:{vidokezo}\n\n{kipande}"
    else:
        ujumbe = (
            "Hariri sarufi, ngeli, tahajia, na alama za uandishi za aya hii ya Kiswahili "
            f"bila kuongeza maneno mapya:\n\n{kipande}"
        )

    hatua1, injini = ita_ai(SYSTEM_PROMPT, ujumbe)
    if not hatua1:
        return {"text": kipande, "ok": False, "injini": None, "hatua2": False}

    if not _uwiano_unakubalika(kipande, hatua1, kitendo):
        # AI imeongeza/kupunguza kupita kiasi: kwenye uhariri tunarudi kwenye asili
        if kitendo != "tafsiri":
            return {"text": kipande, "ok": False, "injini": injini, "hatua2": False}

    matokeo, ilitumia_hatua2 = hatua1, False

    # --- Hatua ya 2: ukaguzi wa ngeli/sarufi bila kubadilisha maana ---
    if HATUA_MBILI:
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
# 8. NJIA (ROUTES)
# ------------------------------------------------------------------
@app.route("/api/chakata", methods=["POST"])
@app.route("/hariri", methods=["POST"])
@app.route("/tafsiri", methods=["POST"])
def huduma_ya_lugha():
    data = request.get_json(silent=True) or {}
    maandishi = data.get("text") or data.get("maandishi") or ""
    kitendo = str(data.get("mode") or data.get("kitendo") or "hariri").lower()

    if request.path.endswith("/tafsiri") or kitendo in ("tafsiri", "translate"):
        kitendo = "tafsiri"
    else:
        kitendo = "hariri"

    if not isinstance(maandishi, str) or not maandishi.strip():
        return jsonify({"ok": False, "error": "Tafadhali weka maandishi kwanza."}), 400

    if len(maandishi) > MAX_CHARS:
        return jsonify({
            "ok": False,
            "error": f"Maandishi ni marefu mno (herufi {len(maandishi)}). Kikomo ni {MAX_CHARS}. Yagawe sehemu sehemu.",
        }), 413

    # Gawa kwa mistari; hifadhi mistari tupu na mistari isiyo na herufi (mf. "---", "1.")
    mistari = maandishi.splitlines()
    muundo = []   # kila kipengele: None (mstari tupu/usiobadilishwa) au idadi ya vipande
    vipande = []  # orodha bapa ya vipande vya kuchakata
    for mstari in mistari:
        if not mstari.strip() or not _ina_herufi(mstari):
            muundo.append(("kama_ilivyo", mstari))
            continue
        sehemu = _gawa_mstari_mrefu(mstari.strip())
        muundo.append(("chakata", len(sehemu)))
        vipande.extend(sehemu)

    if not vipande:
        return jsonify({"ok": False, "error": "Hakuna maandishi ya kuchakata."}), 400

    # Uchakataji sambamba, mpangilio unahifadhiwa na map()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as mtambo:
        majibu = list(mtambo.map(lambda k: chakata_kipande(k, kitendo), vipande))

    # Unganisha tena kwa mpangilio wa awali
    matokeo_mistari, idx = [], 0
    for aina, thamani in muundo:
        if aina == "kama_ilivyo":
            matokeo_mistari.append(thamani)
        else:
            sehemu_safi = [safisha_maandishi_sanifu(majibu[idx + i]["text"]) for i in range(thamani)]
            idx += thamani
            matokeo_mistari.append(" ".join(sehemu_safi))

    matokeo_kamili = "\n".join(matokeo_mistari)

    zilizoshindwa = sum(1 for j in majibu if not j["ok"])
    injini = sorted({j["injini"] for j in majibu if j["injini"]})
    hatua2 = sum(1 for j in majibu if j["hatua2"])

    if zilizoshindwa == len(majibu):
        return jsonify({
            "ok": False,
            "error": "Huduma za AI hazipatikani kwa sasa. Jaribu tena baadaye.",
            "imechakatwa": False,
        }), 502

    return jsonify({
        "ok": True,
        "matokeo": matokeo_kamili,
        "result": matokeo_kamili,
        "imechakatwa": zilizoshindwa == 0,         # false = baadhi ya vipande vimerudishwa kama vilivyo
        "vipande_vilivyoshindwa": zilizoshindwa,
        "vipande_jumla": len(majibu),
        "injini_iliyotumika": injini,
        "ukaguzi_wa_pili": hatua2,
    })


@app.route("/", methods=["GET"])
def afya_ya_seva():
    return jsonify({
        "status": "Live",
        "mfumo": "AI Lingual Africa Sanifu API v3.1",
        "injini": f"{GEMINI_MODEL} + Groq Fallback + Ukaguzi wa Pili + Chujio salama",
        "gemini": bool(gemini_client),
        "groq": bool(groq_client),
        "hatua_mbili": HATUA_MBILI,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
