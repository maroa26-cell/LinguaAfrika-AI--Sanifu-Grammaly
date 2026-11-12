"""
kanuni_ya_sarufi.py — Injini Kuu ya Sheria na Kanuni za Sarufi ya Kiswahili Sanifu (BAKITA).
Inatumiwa na cerebral_cortex.py na app.py kwa ajili ya tafsiri za AI Lingual na uhakiki wa maandishi.

Toleo 2.2 (Kanuni Maalum za Mtindo, Istilahi na Ngeli):
- Imeongeza Kanuni L: 'Wakati...po-' -> 'Pale...po-'
- Imeongeza Kanuni M: Istilahi za Kitiba (wajawazito, maambukizi magumu kufahamika)
- Imeongeza Kanuni N: Upatanisho wa I-ZI kwenye ukanushi (isinge-)
"""

from __future__ import annotations

import os
import re
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional

logger = logging.getLogger(__name__)

# ============================================================
# VITHIBITISHO
# ============================================================

MBAO_ZA_MAKOSA_YA_PARAMETA = ("temperature", "response_format", "unsupported", "unknown")
KIKOMO_CHA_SAUTI_MB = 25
KIKOMO_CHA_HERUFI_ZA_SAUTI = 4000

MAELEKEZO_YA_LUGHA = {
    "Kiswahili": (
        "Use natural, eloquent Tanzanian Standard Swahili (Kiswahili Sanifu). "
        "Elevate lexical choice and editorial polish by strictly obeying all rules below: "
        "1) POSSESSIVES: Avoid repeating possessive pronouns in coordinated nouns (write 'uvumilivu na umakini wao ulizaa matunda' instead of 'uvumilivu wao na umakini wao ulizaa matunda'). "
        "2) NOUN-CLASS CONCORD: Maintain strict Swahili noun-class concord (e.g., U-class abstract nouns take 'u-' concord, never 'vi-'). "
        "3) AVOID ROOT REPETITION: Avoid adjacent words sharing the same root or sound (prefer 'hawakukata tamaa' or 'walikataa kusalimu amri' instead of 'walikataa kukata tamaa'). "
        "4) CONJUNCTIONS: Prefer single cohesive conjunctions like 'Ijapokuwa', 'Ingawa', or 'Licha ya kuwa' instead of redundant calques like 'Hata ingawa'. "
        "5) IDIOMS & FORMATTING: Translate idioms naturally (e.g., 'kuzaa matunda' for 'pay off', 'cheti cha dawa' for 'prescription') and strictly preserve exact paragraph breaks. "
        "6) MANDATORY HUMAN OBJECT INFIX (YAMBIWA): Whenever an applicative or transitive verb is followed by a human recipient/beneficiary (e.g., mgonjwa, mtoto, watu), you MUST include '-m-', '-mw-', or '-wa-' before the verb root ('kumwandikia mgonjwa' instead of 'kuandikia mgonjwa'; 'nilimwambia mtoto' instead of 'niliambia mtoto'). "
        "7) ANIMACY & VERB MORPHOLOGY: "
        "(a) All living beings (people, animals, birds, insects) take A-WA concord regardless of noun prefix ('simba amenguruma', 'madaktari wamefika', never 'simba imenguruma' or 'madaktari zimefika'). "
        "(b) Tense negation: '-na-' becomes 'ha-...-i' ('hasomi'), '-li-' becomes 'ha-ku-' ('hakusoma'), '-me-' becomes 'ha-ja-' ('hajasoma'). "
        "(c) Monosyllabic verbs retain '-ku-' in positive tenses ('anakula', 'alikunywa', 'angekuja') and drop it in negation ('hali', 'hakunywa'). "
        "(d) Use 'amba-' for relative clauses in '-me-' tense or negation ('ambaye amefika', 'ambaye hakufika', never 'ameyefika'). "
        "(e) Use 'na' for passive agents ('alipigwa na mwalimu') and 'kwa' for instruments or manner ('aliandika kwa kalamu'). "
        "8) ADVANCED EDITORIAL RULES: "
        "(a) LOCATIVE COPULA: Never use 'ni' for location; use '-po/-ko/-mo' ('Kitabu kipo mezani', 'Wageni wako nyumbani'). Use 'kuwa' for non-present copula ('alikuwa daktari'). "
        "(b) ASSOCIATIVE '-A': Match '-a' strictly to the possessed noun's class ('kitabu cha', 'majina ya', 'uhuru wa'). "
        "(c) HABITUAL 'HU-': Never attach subject prefixes to 'hu-' ('mimi husoma', 'wao husoma', never 'ninahusoma'). "
        "(d) PASSIVE BORROWED VERBS: Arabic-origin verbs ending in -e/-i/-u take '-ewa/-iwa' in passive ('samehewa', 'tafsiriwa', 'jaribiwa', never 'samehwa'). "
        "(e) 'KILA' AGREEMENT: 'Kila' always takes singular nouns and singular verbs ('kila mwanafunzi ana', never 'kila wanafunzi'). "
        "(f) NARRATIVE '-KA-': In sequential past actions, use '-li-' on the first verb and '-ka-' on subsequent verbs ('Aliamka, akanawa, akaenda'). "
        "(g) NEGATIVE INFINITIVE: Use 'kuto-' for multisyllabic verbs ('kutosoma', 'kutofika') and 'kutoku-' only for monosyllabic verbs ('kutokula', 'kutokuja'). "
        "(h) MODAL 'LAZIMA': Follow 'lazima' or 'sharti' with the subjunctive '-e' ('Lazima afike', never 'Lazima atafika')."
    ),
    "Kichina": "Write in Simplified Chinese characters (Mandarin).",
    "Kireno": "Use standard Portuguese as used in Mozambique and Angola (European norms).",
    "Kizulu": "Write in standard isiZulu (South Africa), using correct noun-class concord.",
    "Setswana": "Write in standard Setswana as used in Botswana (Tswana orthography).",
}

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class Kosa:
    """Kosa moja lililopatikana kwenye sentensi."""
    aina: str                    # "NGELI" | "KIROBOTI" | "MOFOLOJIA" | "ALAMA" | "MTINDO" | "ISTILAHI"
    neno: str                    # Neno lenye kosa
    nafasi: int                  # Nafasi (index) kwenye sentensi asili
    urefu: int                   # Urefu wa neno
    ujumbe: str                  # Maelezo ya kosa
    mapendekezo: list[str] = field(default_factory=list)
    chanzo: str = ""             # "exceptions" | "prefix" | "ubaguzi" | "Kanuni Maalum"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MatokeoYaNgeli:
    """Matokeo ya utambuzi wa ngeli."""
    ngeli: Optional[str]
    uhakika: float               # 0.0 – 1.0
    chanzo: str                  # "exceptions" | "ubaguzi" | "prefix" | "none"


# ============================================================
# KITAMBUZI CHA NGELI
# ============================================================

class KitambuziNgeli:
    """
    Hutambua ngeli ya nomino kwa utaratibu:
      1. Orodha ya 'exceptions' (uhakika 1.0)
      2. Orodha ya 'ubaguzi' – maneno yenye viambishi vya udanganyifu (0.9)
      3. Viambishi halali vya ngeli (0.7 – 0.8)
      4. Hakuna (0.0)
    """

    # Maneno yenye viambishi vinavyodanganya
    UBAGUZI: dict[str, str] = {
        # 'm-' inayoonekana kama A-WA lakini ni U-I
        "mti": "U-I_SG", "mto": "U-I_SG", "mkono": "U-I_SG", "mguu": "U-I_SG",
        "mlima": "U-I_SG", "mkate": "U-I_SG", "mpira": "U-I_SG", "mji": "U-I_SG",
        "mwezi": "U-I_SG", "mwaka": "U-I_SG", "mche": "U-I_SG", "mzigo": "U-I_SG",
        "mkaa": "U-I_SG", "mchanga": "U-I_SG", "moshi": "U-I_SG", "moyo": "U-I_SG",
        # 'm-' halali ya A-WA lakini yenye changamoto
        "mke": "A-WA_SG", "mume": "A-WA_SG", "mzee": "A-WA_SG",
        # 'wa-' inayodanganya
        "waziri": "A-WA_SG", "wakati": "U-I_SG", "waridi": "I-ZI_SG",
        "wasaa": "U-I_SG", "wasifu": "U-I_SG", "wasiwasi": "U-I_SG",
        # 'ch-' inayodanganya (si KI-VI)
        "chai": "I-ZI_SG", "chumvi": "I-ZI_SG", "chuma": "I-ZI_SG",
        "chura": "I-ZI_SG", "cheche": "I-ZI_SG", "chembe": "I-ZI_SG",
        # Maneno ya I-ZI yenye viambishi vya kawaida
        "shule": "I-ZI_SG", "saa": "I-ZI_SG", "barua": "I-ZI_SG",
        "pesa": "I-ZI_SG", "bahasha": "I-ZI_SG", "redio": "I-ZI_SG",
        "televisheni": "I-ZI_SG", "kampuni": "I-ZI_SG", "benki": "I-ZI_SG",
        "akaunti": "I-ZI_SG", "leseni": "I-ZI_SG", "risiti": "I-ZI_SG",
        "simu": "I-ZI_SG", "barabara": "I-ZI_SG", "habari": "I-ZI_SG",
        "kazi": "I-ZI_SG", "safari": "I-ZI_SG", "dawa": "I-ZI_SG",
        "fedha": "I-ZI_SG", "nguo": "I-ZI_SG", "nyumba": "I-ZI_SG",
        "meza": "I-ZI_SG", "kalamu": "I-ZI_SG", "ndizi": "I-ZI_SG",
        "nyota": "I-ZI_SG", "nyuki": "I-ZI_SG", "nyati": "I-ZI_SG",
        "ngoma": "I-ZI_SG", "ndege": "I-ZI_SG",
    }

    def __init__(self):
        self._cache: dict[str, MatokeoYaNgeli] = {}
        self._jenga_matrix()

    def _jenga_matrix(self):
        """Hujenga jedwali la ngeli lenye viambishi, manyumbuliko na vinyume."""
        self.ngeli_matrix = {
            "A-WA_SG": {
                "exceptions": {
                    "mtu", "mtoto", "mgeni", "mwalimu", "mzee", "kijana",
                    "rafiki", "baba", "mama", "kaka", "dada", "daktari",
                    "mnyama", "mbwa", "paka", "simba", "ndege", "samaki",
                    "mwanafunzi", "mwanamke", "mwanamume", "mlevi",
                    "mchungaji", "mvuvi", "mwindaji", "mhudumu",
                    "mfanyakazi", "mwekezaji", "mjasiriamali", "mhandisi",
                    "mwandishi", "mwanasheria", "mwalimu", "mhasibu",
                },
                "verb_pos": ("a", "yu"),
                "verb_neg": ("ha", "hayu"),
                "adj_prefixes": ("m", "mw"),
            },
            "A-WA_PL": {
                "exceptions": {
                    "watu", "watoto", "wageni", "walimu", "wazee", "vijana",
                    "marafiki", "wakulima", "wanyama", "wanafunzi", "wanawake",
                    "wanaume", "walevi", "wafanyakazi", "wawekezaji",
                },
                "verb_pos": ("wa",),
                "verb_neg": ("hawa",),
                "adj_prefixes": ("wa", "w"),
            },
            "KI-VI_SG": {
                "exceptions": {
                    "kitu", "kitabu", "kiti", "chakula", "chombo", "kisu",
                    "kikombe", "kiatu", "cheti", "choo", "chumba", "kijiji",
                    "kizazi", "kipimo", "kifaa", "kioo", "kiongozi",
                },
                "verb_pos": ("ki",),
                "verb_neg": ("haki",),
                "adj_prefixes": ("ki", "ch"),
            },
            "KI-VI_PL": {
                "exceptions": {
                    "vitu", "vitabu", "viti", "vyakula", "vyombo", "visu",
                    "vikombe", "viatu", "vyeti", "vyoo", "vijiji", "vizazi",
                    "vipimo", "vifaa", "viongozi",
                },
                "verb_pos": ("vi",),
                "verb_neg": ("havi",),
                "adj_prefixes": ("vi", "vy"),
            },
            "U-I_SG": {
                "exceptions": {
                    "uvumilivu", "umakini", "uhuru", "umoja", "upendo",
                    "udongo", "ugonjwa", "utoto", "uzee", "usiku", "umri",
                    "ubongo", "utumbo", "ukuta", "ulimi", "uzi", "ubawa",
                },
                "verb_pos": ("u",),
                "verb_neg": ("hau",),
                "adj_prefixes": ("m", "mw", "u"),
            },
            "U-I_PL": {
                "exceptions": {
                    "miti", "mito", "mikono", "miguu", "milima", "miaka",
                    "miezi", "mikate", "mipira", "miji", "mizigo", "mioyo",
                    "mishipa", "mifupa", "misuli",
                },
                "verb_pos": ("i",),
                "verb_neg": ("hai",),
                "adj_prefixes": ("mi", "my"),
            },
            "LI-YA_SG": {
                "exceptions": {
                    "jicho", "jino", "jiwe", "jina", "gari", "shamba", "tunda",
                    "ua", "swali", "jambo", "kasha", "debe", "jani", "jua",
                },
                "verb_pos": ("li",),
                "verb_neg": ("hali",),
                "adj_prefixes": ("ji", "j", ""),
            },
            "LI-YA_PL": {
                "exceptions": {
                    "macho", "meno", "mawe", "majina", "magari", "mashamba",
                    "matunda", "maua", "maswali", "mambo", "makasha", "madebe",
                    "maji", "maziwa", "majani", "mawazo", "maneno",
                },
                "verb_pos": ("ya",),
                "verb_neg": ("haya",),
                "adj_prefixes": ("ma",),
            },
            "I-ZI_SG": {
                "exceptions": {
                    "nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi",
                    "simu", "safari", "kazi", "habari", "fedha", "dawa",
                    "shule", "saa", "barua", "pesa", "bahasha", "redio",
                },
                "verb_pos": ("i",),
                "verb_neg": ("hai",),
                "adj_prefixes": ("n", "ny", "m", ""),
            },
            "I-ZI_PL": {
                "exceptions": {  # Sawa na SG – I-ZI haina tofauti ya umoja/wingi mara nyingi
                    "nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi",
                    "simu", "safari", "kazi", "habari", "fedha", "dawa",
                },
                "verb_pos": ("zi",),
                "verb_neg": ("hazi",),
                "adj_prefixes": ("n", "ny", "m", ""),
            },
        }

    # --------------------------------------------------------
    # API KUU
    # --------------------------------------------------------

    def tambua(self, neno: str) -> MatokeoYaNgeli:
        """Hutambua ngeli ya neno, ikiwa na caching."""
        key = neno.lower().strip(".,!?;:\"'()[]{}…")
        if not key:
            return MatokeoYaNgeli(None, 0.0, "none")
        if key in self._cache:
            return self._cache[key]
        matokeo = self._tambua_impl(key)
        self._cache[key] = matokeo
        return matokeo

    def _tambua_impl(self, w: str) -> MatokeoYaNgeli:
        # 1. Ubaguzi (maneno yenye viambishi vya udanganyifu)
        if w in self.UBAGUZI:
            return MatokeoYaNgeli(self.UBAGUZI[w], 0.9, "ubaguzi")

        # 2. Exceptions za kila ngeli
        for ngeli, sheria in self.ngeli_matrix.items():
            if w in sheria["exceptions"]:
                return MatokeoYaNgeli(ngeli, 1.0, "exceptions")

        # 3. Viambishi halali
        # 'mw-' → A-WA_SG au U-I_SG (kwa mwaka, mwezi)
        if w.startswith("mw") and len(w) > 4:
            if w in {"mwaka", "mwezi", "mwili", "mwilli"}:
                return MatokeoYaNgeli("U-I_SG", 0.8, "prefix")
            return MatokeoYaNgeli("A-WA_SG", 0.7, "prefix")

        # 'wa-' → A-WA_PL (isipokuwa wakati, waziri, etc. – ziko kwenye UBAGUZI)
        if w.startswith("wa") and len(w) > 4:
            return MatokeoYaNgeli("A-WA_PL", 0.7, "prefix")

        # 'ki-' → KI-VI_SG
        if w.startswith("ki") and len(w) > 4:
            return MatokeoYaNgeli("KI-VI_SG", 0.8, "prefix")

        # 'vi-'/'vy-' → KI-VI_PL
        if w.startswith(("vi", "vy")) and len(w) > 4:
            return MatokeoYaNgeli("KI-VI_PL", 0.8, "prefix")

        # 'mi-' → U-I_PL
        if w.startswith("mi") and len(w) > 4:
            return MatokeoYaNgeli("U-I_PL", 0.7, "prefix")

        # 'ma-' → LI-YA_PL
        if w.startswith("ma") and len(w) > 4:
            return MatokeoYaNgeli("LI-YA_PL", 0.8, "prefix")

        # 'm-' → A-WA_SG (tahadhari: nyingi ziko kwenye UBAGUZI)
        if w.startswith("m") and len(w) > 4:
            return MatokeoYaNgeli("A-WA_SG", 0.5, "prefix")

        # 'u-' → U-I_SG
        if w.startswith("u") and len(w) > 4 and w != "ua":
            return MatokeoYaNgeli("U-I_SG", 0.6, "prefix")

        return MatokeoYaNgeli(None, 0.0, "none")


# ============================================================
# KANUNI YA YAMBIWA (KIAMBISHI CHA MTENDWA WA BINADAMU)
# ============================================================

class KanuniYaYambiwa:
    """
    Hukamata vitenzi vya kutendea/kutendwa (-ia, -ea) vinavyofuatiwa na nomino ya
    binadamu bila kiambishi cha mtendwa (-m-, -mw-, -wa-).
    Mfano: 'aliandikia mgonjwa' -> 'alimwandikia mgonjwa'.
    """

    VOWELS = set("aeiou")

    WATU_UMOJA = {
        "mgonjwa", "mtoto", "mwanafunzi", "mwalimu", "daktari", "muuguzi",
        "mzazi", "baba", "mama", "kaka", "dada", "rafiki", "mgeni", "mtu",
        "kiongozi", "mfanyakazi", "mkulima", "mteja", "mwenzake", "askari",
        "dereva", "mhandisi", "hakimu", "msichana", "mvulana", "mwanamke", "mwanamume",
    }
    WATU_WINGI = {
        "wagonjwa", "watoto", "wanafunzi", "walimu", "madaktari", "wauguzi",
        "wazazi", "marafiki", "wageni", "watu", "viongozi", "wafanyakazi",
        "wakulima", "wateja", "wenzake", "maaskari", "madereva", "wahandisi",
        "mahakimu", "wasichana", "wavulana", "wanawake", "wanaume",
    }

    # Vitenzi vya -ea/-ia vinavyokubali nomino ya binadamu bila kiambishi cha mtendwa
    MASHINA_YA_KUACHWA = {"pokea", "tembelea", "ngojea", "tazamia", "ingilia"}
    VITENZI_VYA_KUACHWA = {"kuwa", "kulia", "kushoto", "kwenda", "kuja", "kufika", "kukaa", "kutumia"}

    MUUNDO = re.compile(
        r"^(?P<prefix>ku|kw|hatu|hawa|ham|ha|hu|si|ni|u|a|tu|m|wa|ki|vi|li|ya|i|zi)"
        r"(?P<tense>ngali|ngeli|nge|na|li|ta|me|ka|ki)?"
        r"(?P<rel>ye|o|lo|yo|cho|vyo|wo|zo|ko|po|mo)?"
        r"(?P<obj>mw|m|wa|ni|ku|tu|ji)?"
        r"(?P<stem>[a-z]{2,}?(?:li|le|i|e)a)$"
    )

    def kagua(self, sentensi: str) -> list[Kosa]:
        makosa: list[Kosa] = []
        tokeni = list(re.finditer(r"\w+", sentensi))
        for i in range(len(tokeni) - 1):
            t1, t2 = tokeni[i], tokeni[i + 1]
            if sentensi[t1.end():t2.start()].strip():
                continue  # kuna alama ya uakifishaji kati ya maneno
            kitenzi_asili, nomino_asili = t1.group(0), t2.group(0)
            kitenzi, nomino = kitenzi_asili.lower(), nomino_asili.lower()

            umoja = nomino in self.WATU_UMOJA
            wingi = nomino in self.WATU_WINGI
            if not (umoja or wingi) or kitenzi in self.VITENZI_VYA_KUACHWA:
                continue

            m = self.MUUNDO.match(kitenzi)
            if not m:
                continue
            p = m.groupdict()
            if p["obj"] or p["stem"] in self.MASHINA_YA_KUACHWA:
                continue  # tayari kina kiambishi cha mtendwa, au kitenzi cha kuachwa

            stem = p["stem"]
            if umoja:
                kiambishi = "mw" if stem[0] in self.VOWELS else "m"
                chanzo = "Kanuni ya Yambiwa (Human Object Concord)"
                ujumbe = (f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' "
                          f"kinakosa kiambishi cha mtendwa '-{kiambishi}-'.")
            else:
                kiambishi = "wa"
                chanzo = "Kanuni ya Yambiwa (Plural Object Concord)"
                ujumbe = (f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' (wingi) "
                          f"kinakosa kiambishi cha mtendwa '-wa-'.")

            kitenzi_kipya = f"{p['prefix']}{p['tense'] or ''}{p['rel'] or ''}{kiambishi}{stem}"
            if kitenzi_asili[0].isupper():
                kitenzi_kipya = kitenzi_kipya[0].upper() + kitenzi_kipya[1:]

            makosa.append(Kosa(
                aina="MOFOLOJIA",
                neno=sentensi[t1.start():t2.end()],
                nafasi=t1.start(),
                urefu=t2.end() - t1.start(),
                ujumbe=ujumbe,
                mapendekezo=[f"{kitenzi_kipya} {nomino_asili}"],
                chanzo=chanzo,
            ))
        return makosa


# ============================================================
# MKAGUZI WA SARUFI
# ============================================================

class MkaguziSarufi:
    """
    Hukagua sentensi kwa:
      - Upatanisho wa ngeli (nomino ↔ kivumishi kilicho karibu)
      - Nahau/methali zilizokopwa vibaya (kiroboti)
      - Uandishi (herufi kubwa, alama ya kituo)
      - Umoja wa kisintaksia wa sentensi
      - Kanuni maalum za mtindo, istilahi, na upatanisho wa I-ZI
    """

    VIVUMISHI_MIZIZI = {
        "zuri", "baya", "kubwa", "dogo", "refu", "fupi", "pya", "zee",
        "gumu", "laini", "eupe", "eusi", "ekundu", "ingi", "chache",
        "ema", "kali", "pole", "vivu", "zito", "epesi", "tamu", "chungu",
    }

    # Maneno ambayo yanaweza kuwa nomino AU kivumishi – usiyakague kama kivumishi
    MANENO_YENYE_MAANA_MBILI = {"kali", "pole", "tamu", "chungu", "zito"}

    MAKOSA_YA_KIROBOTI = {
        "mimi ni baridi": "Tumia 'Nasikia baridi' au 'Nahisi baridi'",
        "mimi ni njaa": "Tumia 'Nina njaa'",
        "fanya akili": "Tumia 'Leta maana' au 'Kuwa na mantiki'",
        "hata ingawa": "Tumia neno moja tu: 'Ingawa' au 'Ijapokuwa'",
        "walikataa kukata tamaa": "Epuka urudiaji wa mzizi; tumia 'hawakukata tamaa' au 'walikataa kusalimu amri'",
        "fanya maamuzi": "Tumia 'fanya uamuzi'",
    }

    # Orodha ya Kanuni Maalum (Regex, Badala, Aina, Ujumbe, Chanzo)
    KANUNI_MAALUM = [
        # L. 'Wakati [nomino] ana-po-' -> 'Pale [nomino] ana-po-'
        (
            re.compile(r"\bWakati\s+([a-z]+)\s+([a-z]*(?:na|li|taka)po[a-z]+)\b", re.I),
            r"Pale \1 \2",
            "MTINDO",
            "Kitenzi chenye '-po-' tayari kinaonyesha wakati. Tumia 'Pale' badala ya tafsiri sisisi 'Wakati'.",
            "Mtindo wa Kiswahili Sanifu"
        ),
        # M1. Istilahi za Kitiba zilizotafsiriwa sisisi
        (
            re.compile(r"\b(akina\s+mama|mama)\s+wanaotarajia\b", re.I),
            "akina mama wajawazito",
            "ISTILAHI",
            "Tafsiri sisisi ya 'expectant mothers'. Tumia msamiati wa kitiba 'akina mama wajawazito'.",
            "Istilahi za Tiba"
        ),
        # M2. Maambukizi magumu
        (
            re.compile(r"\bmaambukizi\s+magumu\b(?!\s+kufahamika)", re.I),
            "maambukizi magumu kufahamika",
            "ISTILAHI",
            "Kwa muktadha wa uchunguzi wa maabara ('complex infections'), tumia 'maambukizi magumu kufahamika'.",
            "Istilahi za Tiba"
        ),
        # N. Upatanisho wa Ngeli ya I-ZI kwenye Ukanushi wa Masharti
        (
            re.compile(r"\b(kliniki|zahanati|hospitali|kampuni|serikali|taasisi|benki|shule)\s+ya\s+eneo\s+hilo\s+hainge([a-z]+)\b", re.I),
            r"\1 ya eneo hilo isinge\2",
            "NGELI",
            "Nomino ya ngeli ya I-ZI inachukua ukanushi 'isinge-' badala ya 'hainge-'.",
            "Upatanisho wa Ngeli I-ZI"
        ),
    ]

    NAHAU_NA_METHALI = {
        "kula chumvi nyingi": {"aina": "NAHAU", "maana": "kuishi miaka mingi", "en": "to live a long life"},
        "piga moyo konde": {"aina": "NAHAU", "maana": "jipa moyo / vumilia", "en": "take courage"},
        "aga dunia": {"aina": "NAHAU", "maana": "fariki dunia", "en": "pass away"},
        "shika mkia": {"aina": "NAHAU", "maana": "kuwa wa mwisho", "en": "come in last"},
        "kufa kuzikana": {"aina": "NAHAU", "maana": "urafiki wa dhati", "en": "lifelong friendship"},
        "kuzaa matunda": {"aina": "NAHAU", "maana": "kuleta mafanikio", "en": "pay off"},
        "haraka haraka haina baraka": {"aina": "METHALI", "maana": "pupa halifanikiwi", "en": "haste makes waste"},
        "haba na haba hujaza kibaba": {"aina": "METHALI", "maana": "vitu vidogo hukusanyika", "en": "little by little"},
        "mvumilivu hula mbivu": {"aina": "METHALI", "maana": "mwenye subira hufanikiwa", "en": "patience pays"},
        "asiyesikia la mkuu huvunjika guu": {"aina": "METHALI", "maana": "asiyetii ushauri hupata madhara", "en": "ignoring advice has consequences"},
    }

    def __init__(self):
        self.kitambuzi = KitambuziNgeli()
        self.yambiwa = KanuniYaYambiwa()

    # --------------------------------------------------------
    # API KUU
    # --------------------------------------------------------

    def kagua(self, sentensi: str, kagua_alama: bool = True) -> list[Kosa]:
        """Hukagua sentensi na kurudisha orodha ya makosa yaliyopatikana.

        kagua_alama=False huruka ukaguzi wa herufi kubwa na nukta ya mwisho
        (inafaa kwa vichwa vya habari, orodha, na maandishi ya tafsiri).
        """
        makosa: list[Kosa] = []

        if not sentensi or not sentensi.strip():
            return [Kosa("TAWALI", "", 0, 0, "Sentensi ni tupu.")]

        # 1. Uandishi (herufi kubwa, alama ya kituo)
        if kagua_alama:
            makosa.extend(self._kagua_uandishi(sentensi))

        # 2. Upatanisho wa ngeli kwa vivumishi
        makosa.extend(self._kagua_upatanisho_vivumishi(sentensi))

        # 3. Kiroboti na calques
        makosa.extend(self._kagua_kiroboti(sentensi))

        # 4. Upatanisho wa kiima-kitenzi
        makosa.extend(self._kagua_upatanisho_kiima_kitenzi(sentensi))

        # 5. Yambiwa (kiambishi cha mtendwa wa binadamu)
        makosa.extend(self.yambiwa.kagua(sentensi))

        # 6. Kanuni Maalum za Mtindo/Istilahi/Ngeli (MPYA)
        makosa.extend(self._kagua_kanuni_maalum(sentensi))

        # Panga kwa nafasi
        makosa.sort(key=lambda k: k.nafasi)
        return makosa

    # --------------------------------------------------------
    # UKAGUZI WA KANUNI MAALUM
    # --------------------------------------------------------

    def _kagua_kanuni_maalum(self, sentensi: str) -> list[Kosa]:
        """Hukagua kwa kutumia orodha ya KANUNI_MAALUM (Regex)."""
        makosa: list[Kosa] = []
        
        for muundo, badala, aina, ujumbe, chanzo in self.KANUNI_MAALUM:
            for m in muundo.finditer(sentensi):
                neno_lililokosewa = m.group(0)
                # Tengeneza pendekezo kwa kutumia muundo huo huo wa re.sub
                pendekezo = muundo.sub(badala, neno_lililokosewa)
                
                makosa.append(Kosa(
                    aina=aina,
                    neno=neno_lililokosewa,
                    nafasi=m.start(),
                    urefu=len(neno_lililokosewa),
                    ujumbe=ujumbe,
                    mapendekezo=[pendekezo],
                    chanzo=chanzo
                ))
        return makosa

    # --------------------------------------------------------
    # UKAGUZI WA UANDISHI
    # --------------------------------------------------------

    def _kagua_uandishi(self, sentensi: str) -> list[Kosa]:
        makosa = []
        stripped = sentensi.strip()

        if stripped and not stripped[0].isupper() and stripped[0].isalpha():
            makosa.append(Kosa(
                aina="ALAMA",
                neno=stripped.split()[0] if stripped.split() else "",
                nafasi=0,
                urefu=1,
                ujumbe="Sentensi lazima ianze na herufi kubwa.",
                mapendekezo=[stripped[0].upper() + stripped[1:50]],
            ))

        mwisho = stripped.rstrip("\"'\u201d\u2019\u00bb)]}")
        if mwisho and mwisho[-1] not in ".!?\u2026":
            makosa.append(Kosa(
                aina="ALAMA",
                neno=stripped[-20:],
                nafasi=len(sentensi) - 1,
                urefu=1,
                ujumbe="Sentensi lazima iishie na alama ya kituo (. ! au ?).",
                mapendekezo=[stripped + "."],
            ))

        return makosa

    # --------------------------------------------------------
    # MSAADA: KITENZI AU NOMINO? / MPAKA WA KISHAZI
    # --------------------------------------------------------

    _MUUNDO_WA_KITENZI = re.compile(r"^(wa|ki|vi|ya|li|zi)(na|li|me|ta|ka|nge|ngali|ngeli)[a-z]{2,}$")

    def _ni_nomino_ya_kuaminika(self, neno: str, uhakika_wa_chini: float) -> Optional[str]:
        """Hurudisha ngeli ikiwa neno ni nomino ya kuaminika; vinginevyo None.
        Maneno yanayofanana na kitenzi (mf. 'wanasoma', 'walifika') hayahesabiwi nomino
        isipokuwa yamo kwenye orodha ya uhakika."""
        m = self.kitambuzi.tambua(neno)
        if not m.ngeli or m.uhakika < uhakika_wa_chini:
            return None
        if m.uhakika < 0.9:
            n = neno.lower()
            if self._MUUNDO_WA_KITENZI.match(n):
                return None
            # Kivumishi (mf. 'vizuri') si nomino; kisikosewe kuwa kiima cha kitenzi
            if any(n.endswith(z) and n != z for z in self.VIVUMISHI_MIZIZI):
                return None
        return m.ngeli

    @staticmethod
    def _kuna_mpaka(sentensi: str, mwisho_wa_kwanza: int, mwanzo_wa_pili: int) -> bool:
        """Kweli ikiwa kuna alama ya kishazi (, ; : . ! ?) kati ya maneno mawili."""
        return any(c in ",;:.!?" for c in sentensi[mwisho_wa_kwanza:mwanzo_wa_pili])

    # --------------------------------------------------------
    # UKAGUZI WA UPATANISHO WA VIVUMISHI
    # --------------------------------------------------------

    def _kagua_upatanisho_vivumishi(self, sentensi: str) -> list[Kosa]:
        """
        Kwa kila kivumishi, hutafuta nomino ILIYO KARIBU (nyuma yake)
        na kuhakikisha viambishi vyao vinapatana.
        """
        makosa: list[Kosa] = []
        tokens = list(re.finditer(r"\b[\w']+\b", sentensi))

        for i, m in enumerate(tokens):
            t_lower = m.group(0).lower()

            # Tafuta kivumishi
            kivumishi_mzizi = None
            for mzizi in self.VIVUMISHI_MIZIZI:
                if t_lower.endswith(mzizi) and t_lower != mzizi:
                    kivumishi_mzizi = mzizi
                    break

            if not kivumishi_mzizi:
                continue

            # Ruka maneno yenye maana mbili (kali, pole, n.k.) – si kivumishi hakika
            if t_lower in self.MANENO_YENYE_MAANA_MBILI:
                continue

            kiambishi = t_lower[: -len(kivumishi_mzizi)]

            # Tafuta nomino iliyo karibu (nyuma)
            nomino, ngeli = None, None
            for j in range(i - 1, -1, -1):
                if self._kuna_mpaka(sentensi, tokens[j].end(), tokens[j + 1].start()):
                    break
                ngeli_j = self._ni_nomino_ya_kuaminika(tokens[j].group(0), 0.5)
                if ngeli_j:
                    nomino = tokens[j].group(0)
                    ngeli = ngeli_j
                    break
                # Acha kutafuta ikiwa tumepita alama ya kituo au kiunganishi
                if tokens[j].group(0).lower() in {"na", "au", "lakini", "kwani"}:
                    break

            if not ngeli or ngeli not in self.kitambuzi.ngeli_matrix:
                continue

            sheria = self.kitambuzi.ngeli_matrix[ngeli]
            if kiambishi not in sheria["adj_prefixes"]:
                mapendekezo = [f"{p}{kivumishi_mzizi}" for p in sheria["adj_prefixes"][:3]]
                makosa.append(Kosa(
                    aina="NGELI",
                    neno=m.group(0),
                    nafasi=m.start(),
                    urefu=len(m.group(0)),
                    ujumbe=(
                        f"Kivumishi '{m.group(0)}' hakitoshani na nomino "
                        f"'{nomino}' ({ngeli}). Kiambishi kinachotakiwa ni "
                        f"mojawapo ya: {sheria['adj_prefixes']}."
                    ),
                    mapendekezo=mapendekezo,
                    chanzo="ngeli_matrix",
                ))

        return makosa

    # --------------------------------------------------------
    # UKAGUZI WA UPATANISHO WA KIIMA-KITENZI
    # --------------------------------------------------------

    def _kagua_upatanisho_kiima_kitenzi(self, sentensi: str) -> list[Kosa]:
        """
        Kwa kila kitenzi rahisi, hutafuta nomino ILIYO KARIBU (nyuma)
        na kuhakikisha kiambishi cha kiima (SC) kinapatana.
        Huruka vitenzi vyenye relative marker (ye, o, lo...).
        """
        makosa: list[Kosa] = []
        tokens = list(re.finditer(r"\b[\w']+\b", sentensi))

        # Vitenzi vya kawaida – mizizi inayojulikana
        mizizi_vitenzi = {
            "kuj", "fany", "pend", "sik", "end", "let", "it", "sem", "nun",
            "uz", "fung", "kal", "chez", "imb", "andik", "soma", "nyw",
            "la", "f", "w", "ja", "taka", "wez", "ju", "on", "sik",
        }

        for i, m in enumerate(tokens):
            t_lower = m.group(0).lower()
            if len(t_lower) < 3:
                continue

            # Tambua kama neno linaweza kuwa kitenzi
            # (kiambishi cha kiima + tense + mzizi + FV)
            m_kitenzi = re.match(
                r"^(?P<sc>ha|hu|si|ni|a|u|tu|m|wa|ki|vi|li|ya|i|zi)?"
                r"(?P<tense>na|li|ta|me|ka|ki|nge|ngali|ngeli)?"
                r"(?P<stem>[a-z]{2,}?)"
                r"(?P<fv>[aei])$",
                t_lower,
            )
            if not m_kitenzi:
                continue

            # Ruka ikiwa neno ni nomino inayojulikana
            if self._ni_nomino_ya_kuaminika(t_lower, 0.0):
                continue

            # Hakikisha mzizi unajulikana
            stem = m_kitenzi.group("stem")
            if not any(mzizi in stem for mzizi in mizizi_vitenzi):
                continue

            # Ruka vitenzi vyenye relative (aliyekuja, nilichokiona)
            if any(rel in t_lower for rel in ("ye", "lo", "cho", "vyo", "zo", "ko", "po", "mo")):
                continue

            sc = m_kitenzi.group("sc")
            if not sc:
                continue

            # Tafuta nomino ya karibu (nyuma) kama kiima
            nomino, ngeli = None, None
            for j in range(i - 1, -1, -1):
                if self._kuna_mpaka(sentensi, tokens[j].end(), tokens[j + 1].start()):
                    break
                ngeli_j = self._ni_nomino_ya_kuaminika(tokens[j].group(0), 0.7)
                if ngeli_j:
                    nomino = tokens[j].group(0)
                    ngeli = ngeli_j
                    break

            if not ngeli or ngeli not in self.kitambuzi.ngeli_matrix:
                continue

            sheria = self.kitambuzi.ngeli_matrix[ngeli]
            if sc not in sheria["verb_pos"] and sc not in sheria["verb_neg"]:
                makosa.append(Kosa(
                    aina="NGELI",
                    neno=m.group(0),
                    nafasi=m.start(),
                    urefu=len(m.group(0)),
                    ujumbe=(
                        f"Kitenzi '{m.group(0)}' hakitoshi kiima '{nomino}' ({ngeli}). "
                        f"Kiambishi cha kiima kinachotakiwa ni mojawapo ya: "
                        f"{sheria['verb_pos']}."
                    ),
                    mapendekezo=[f"{p}{t_lower[len(sc):]}" for p in sheria["verb_pos"][:2]],
                    chanzo="kiima_kitenzi",
                ))

        return makosa

    # --------------------------------------------------------
    # UKAGUZI WA KIROBOTI
    # --------------------------------------------------------

    def _kagua_kiroboti(self, sentensi: str) -> list[Kosa]:
        """Hutafuta misemo ya kiroboti kwa mipaka ya maneno."""
        makosa: list[Kosa] = []
        sentensi_lower = sentensi.lower()

        for kosa, ushauri in self.MAKOSA_YA_KIROBOTI.items():
            pattern = r"\b" + re.escape(kosa) + r"\b"
            for m in re.finditer(pattern, sentensi_lower):
                makosa.append(Kosa(
                    aina="KIROBOTI",
                    neno=sentensi[m.start(): m.end()],
                    nafasi=m.start(),
                    urefu=m.end() - m.start(),
                    ujumbe=f"Usemi wa kiroboti umegundulika: '{kosa}'. {ushauri}",
                    mapendekezo=[ushauri],
                    chanzo="kiroboti",
                ))

        return makosa


# ============================================================
# API YA NYUMA (inatumika na Streamlit)
# ============================================================

class KanuniZaSarufiKiswahili:
    """
    Injini ya Sheria za Kiisimu (Deterministic Linguistic Guardrails).
    Inatoa API ya nyuma inayofanana na toleo la 1.x.
    """

    def __init__(self):
        self._kaguzi = MkaguziSarufi()

    def tambua_ngeli(self, neno: str) -> Optional[str]:
        """Hutambua ngeli ya neno moja."""
        return self._kaguzi.kitambuzi.tambua(neno).ngeli

    def tambua_ngeli_kwa_uhakika(self, neno: str) -> MatokeoYaNgeli:
        """Hutambua ngeli pamoja na kiwango cha uhakika."""
        return self._kaguzi.kitambuzi.tambua(neno)

    def kagua_sentensi_nzima(self, sentensi: str, kagua_alama: bool = True) -> dict:
        """Hukagua sentensi na kurudisha dict (API ya nyuma).
        kagua_alama=False huruka ukaguzi wa herufi kubwa/nukta ya mwisho."""
        makosa = self._kaguzi.kagua(sentensi, kagua_alama=kagua_alama)
        return {
            "sahihi": len(makosa) == 0,
            "idadi_ya_makosa": len(makosa),
            "makosa": [k.to_dict() for k in makosa],
            "sentensi_iliyokaguliwa": sentensi,
            "mapendekezo": [m for k in makosa for m in k.mapendekezo],
        }

    def kagua_na_kurekebisha(self, sentensi: str) -> dict:
        """
        Hurekebisha kiotomatiki makosa ya kuaminika tu:
          - upatanisho wa ngeli (NGELI), Yambiwa (MOFOLOJIA), na Kanuni Maalum: hubadilisha neno lenye kosa
            kwa pendekezo la kwanza
          - herufi kubwa mwanzoni na nukta mwishoni (ALAMA)
        Makosa ya KIROBOTI hayarekebishwi kiotomatiki (mapendekezo yake ni ushauri, si maneno).
        """
        matokeo = self.kagua_sentensi_nzima(sentensi)
        iliyorekebishwa = sentensi
        mabadiliko = []

        # Tunajumuisha NGELI, MOFOLOJIA, MTINDO, na ISTILAHI hapa
        makosa_ya_kurekebisha = sorted(
            [k for k in matokeo["makosa"] if k["aina"] in ("NGELI", "MOFOLOJIA", "MTINDO", "ISTILAHI") and k["mapendekezo"]],
            key=lambda k: k["nafasi"],
            reverse=True,  # kuanzia mwisho ili nafasi zisibadilike
        )
        mwisho_wa_awali = len(sentensi) + 1
        for k in makosa_ya_kurekebisha:
            n, u = k["nafasi"], k["urefu"]
            if n + u > mwisho_wa_awali:
                continue  # epuka makosa yanayopishana
            pendekezo = k["mapendekezo"][0]
            iliyorekebishwa = iliyorekebishwa[:n] + pendekezo + iliyorekebishwa[n + u:]
            mabadiliko.append({"kutoka": k["neno"], "kwenda": pendekezo})
            mwisho_wa_awali = n

        if any(k["aina"] == "ALAMA" for k in matokeo["makosa"]):
            t = iliyorekebishwa.strip()
            if t and t[0].isalpha() and not t[0].isupper():
                iliyorekebishwa = iliyorekebishwa.replace(t[0], t[0].upper(), 1)
                mabadiliko.append({"kutoka": t[0], "kwenda": t[0].upper()})
            t = iliyorekebishwa.rstrip()
            if t and t.rstrip("\"'\u201d\u2019\u00bb)]}")[-1:] not in (".", "!", "?", "\u2026"):
                iliyorekebishwa = t + "." + iliyorekebishwa[len(t):]
                mabadiliko.append({"kutoka": "", "kwenda": "."})

        return {
            "sentensi_asili": sentensi,
            "sentensi_iliyorekebishwa": iliyorekebishwa,
            "makosa_ya_awali": matokeo["idadi_ya_makosa"],
            "mabadiliko": mabadiliko,
        }
