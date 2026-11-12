"""
kanuni_ya_sarufi.py — Injini Kuu ya Sheria na Kanuni za Sarufi ya Kiswahili Sanifu (BAKITA).
Inatumiwa na cerebral_cortex.py na app.py kwa ajili ya tafsiri za AI Lingual na uhakiki wa maandishi.

Toleo 2.3 (Kanuni Kamili 1-14 na Kanuni Maalum za Mtindo/Istilahi):
- Imeboresha MAELEKEZO_YA_LUGHA (Kiswahili Sanifu) hadi kanuni 14
- Imeunganisha GenericObjectConcordRule (Kanuni ya Yambiwa)
- Imeongeza Kanuni L, M, N za mtindo, istilahi za kitiba, na ngeli I-ZI
"""

from __future__ import annotations

import os
import re
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any, Tuple

logger = logging.getLogger(__name__)

# ============================================================
# VITHIBITISHO NA MAELEKEZO YA LUGHA
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
        "(h) MODAL 'LAZIMA': Follow 'lazima' or 'sharti' with the subjunctive '-e' ('Lazima afike', never 'Lazima atafika'). "
        "9) KINSHIP & HONORIFIC PLURALS (SINGLE & COORDINATED 'AKINA'): Kinship and honorific nouns with zero plural prefixes (mama, baba, dada, kaka, bibi, babu, shangazi, mjomba) MUST take 'akina' in the plural. When two such nouns are coordinated with 'na', repeat 'akina' before EACH noun (write 'akina baba na akina mama wengi' instead of 'baba na mama wengi' or 'akina baba na mama wengi'). "
        "10) COUNTERFACTUAL CONDITIONALS ('KAMA' vs 'IWAPO'): Never use 'Iwapo' or 'Ikiwa' with counterfactual/unreal conditional verbs containing '-nge-', '-ngali-', or '-ngeli-'. Always use 'Kama' (write 'Kama majukwaa yasingeanzishwa...' instead of 'Iwapo majukwaa yasingeanzishwa...'). Reserve 'Iwapo/Ikiwa' strictly for real future possibilities. "
        "11) TEMPORAL CLAUSES ('PALE ... -PO-'): When translating English 'When [subject] [verb]...' using the Swahili '-po-' temporal infix (e.g., 'anapowaelezea'), NEVER start the sentence with a literal 'Wakati'. Use 'Pale' (e.g., 'Pale muuguzi anapowaelezea...') or start directly with the subject ('Muuguzi anapowaelezea...'). "
        "12) MEDICAL & CLINICAL IDIOMATIC PRECISION: Translate 'expectant mothers' strictly as 'akina mama wajawazito' (NEVER 'akina mama wanaotarajia'). Translate 'complex infections' as 'maambukizi magumu kufahamika' or 'maambukizi tata' (NEVER 'maambukizi magumu'). "
        "13) COUNTERFACTUAL MODAL VERBS ('WANGEWEZA KU-' vs 'WANGEKUWA WAME-'): When translating English 'would have [past participle]' (e.g., 'would have stolen', 'would have collapsed') in conditional sentences, NEVER use the calque 'wangekuwa wame-' / 'ungekuwa ume-'. Use the natural modal form 'wangeweza ku-' (e.g., 'wangeweza kuiba') or the direct conditional form ('wangeiba'). "
        "14) DOUBLE-VOWEL VERB NEGATION ('-ZUI-I', '-TII-I', '-JUI-I'): For verb stems ending in '-ui' or '-ii' (such as '-zuia', '-tii', '-jua'), preserve the stem vowel before adding the negative present suffix '-i' (write 'hakuzuii' instead of 'hakuzii', 'hatii' instead of 'hati')."
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
    aina: str                    
    neno: str                    
    nafasi: int                  
    urefu: int                   
    ujumbe: str                  
    mapendekezo: list[str] = field(default_factory=list)
    chanzo: str = ""             

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MatokeoYaNgeli:
    """Matokeo ya utambuzi wa ngeli."""
    ngeli: Optional[str]
    uhakika: float               
    chanzo: str                  


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

    UBAGUZI: dict[str, str] = {
        "mti": "U-I_SG", "mto": "U-I_SG", "mkono": "U-I_SG", "mguu": "U-I_SG",
        "mlima": "U-I_SG", "mkate": "U-I_SG", "mpira": "U-I_SG", "mji": "U-I_SG",
        "mwezi": "U-I_SG", "mwaka": "U-I_SG", "mche": "U-I_SG", "mzigo": "U-I_SG",
        "mkaa": "U-I_SG", "mchanga": "U-I_SG", "moshi": "U-I_SG", "moyo": "U-I_SG",
        "mke": "A-WA_SG", "mume": "A-WA_SG", "mzee": "A-WA_SG",
        "waziri": "A-WA_SG", "wakati": "U-I_SG", "waridi": "I-ZI_SG",
        "wasaa": "U-I_SG", "wasifu": "U-I_SG", "wasiwasi": "U-I_SG",
        "chai": "I-ZI_SG", "chumvi": "I-ZI_SG", "chuma": "I-ZI_SG",
        "chura": "I-ZI_SG", "cheche": "I-ZI_SG", "chembe": "I-ZI_SG",
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
        self.ngeli_matrix = {
            "A-WA_SG": {
                "exceptions": {"mtu", "mtoto", "mgeni", "mwalimu", "mzee", "kijana", "rafiki", "baba", "mama", "kaka", "dada", "daktari", "mnyama", "mbwa", "paka", "simba", "ndege", "samaki", "mwanafunzi", "mwanamke", "mwanamume", "mlevi", "mchungaji", "mvuvi", "mwindaji", "mhudumu", "mfanyakazi", "mwekezaji", "mjasiriamali", "mhandisi", "mwandishi", "mwanasheria", "mwalimu", "mhasibu"},
                "verb_pos": ("a", "yu"),
                "verb_neg": ("ha", "hayu"),
                "adj_prefixes": ("m", "mw"),
            },
            "A-WA_PL": {
                "exceptions": {"watu", "watoto", "wageni", "walimu", "wazee", "vijana", "marafiki", "wakulima", "wanyama", "wanafunzi", "wanawake", "wanaume", "walevi", "wafanyakazi", "wawekezaji"},
                "verb_pos": ("wa",),
                "verb_neg": ("hawa",),
                "adj_prefixes": ("wa", "w"),
            },
            "KI-VI_SG": {
                "exceptions": {"kitu", "kitabu", "kiti", "chakula", "chombo", "kisu", "kikombe", "kiatu", "cheti", "choo", "chumba", "kijiji", "kizazi", "kipimo", "kifaa", "kioo", "kiongozi"},
                "verb_pos": ("ki",),
                "verb_neg": ("haki",),
                "adj_prefixes": ("ki", "ch"),
            },
            "KI-VI_PL": {
                "exceptions": {"vitu", "vitabu", "viti", "vyakula", "vyombo", "visu", "vikombe", "viatu", "vyeti", "vyoo", "vijiji", "vizazi", "vipimo", "vifaa", "viongozi"},
                "verb_pos": ("vi",),
                "verb_neg": ("havi",),
                "adj_prefixes": ("vi", "vy"),
            },
            "U-I_SG": {
                "exceptions": {"uvumilivu", "umakini", "uhuru", "umoja", "upendo", "udongo", "ugonjwa", "utoto", "uzee", "usiku", "umri", "ubongo", "utumbo", "ukuta", "ulimi", "uzi", "ubawa"},
                "verb_pos": ("u",),
                "verb_neg": ("hau",),
                "adj_prefixes": ("m", "mw", "u"),
            },
            "U-I_PL": {
                "exceptions": {"miti", "mito", "mikono", "miguu", "milima", "miaka", "miezi", "mikate", "mipira", "miji", "mizigo", "mioyo", "mishipa", "mifupa", "misuli"},
                "verb_pos": ("i",),
                "verb_neg": ("hai",),
                "adj_prefixes": ("mi", "my"),
            },
            "LI-YA_SG": {
                "exceptions": {"jicho", "jino", "jiwe", "jina", "gari", "shamba", "tunda", "ua", "swali", "jambo", "kasha", "debe", "jani", "jua"},
                "verb_pos": ("li",),
                "verb_neg": ("hali",),
                "adj_prefixes": ("ji", "j", ""),
            },
            "LI-YA_PL": {
                "exceptions": {"macho", "meno", "mawe", "majina", "magari", "mashamba", "matunda", "maua", "maswali", "mambo", "makasha", "madebe", "maji", "maziwa", "majani", "mawazo", "maneno"},
                "verb_pos": ("ya",),
                "verb_neg": ("haya",),
                "adj_prefixes": ("ma",),
            },
            "I-ZI_SG": {
                "exceptions": {"nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi", "simu", "safari", "kazi", "habari", "fedha", "dawa", "shule", "saa", "barua", "pesa", "bahasha", "redio"},
                "verb_pos": ("i",),
                "verb_neg": ("hai",),
                "adj_prefixes": ("n", "ny", "m", ""),
            },
            "I-ZI_PL": {
                "exceptions": {"nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi", "simu", "safari", "kazi", "habari", "fedha", "dawa"},
                "verb_pos": ("zi",),
                "verb_neg": ("hazi",),
                "adj_prefixes": ("n", "ny", "m", ""),
            },
        }

    def tambua(self, neno: str) -> MatokeoYaNgeli:
        key = neno.lower().strip(".,!?;:\"'()[]{}…")
        if not key:
            return MatokeoYaNgeli(None, 0.0, "none")
        if key in self._cache:
            return self._cache[key]
        matokeo = self._tambua_impl(key)
        self._cache[key] = matokeo
        return matokeo

    def _tambua_impl(self, w: str) -> MatokeoYaNgeli:
        if w in self.UBAGUZI:
            return MatokeoYaNgeli(self.UBAGUZI[w], 0.9, "ubaguzi")

        for ngeli, sheria in self.ngeli_matrix.items():
            if w in sheria["exceptions"]:
                return MatokeoYaNgeli(ngeli, 1.0, "exceptions")

        if w.startswith("mw") and len(w) > 4:
            if w in {"mwaka", "mwezi", "mwili", "mwilli"}:
                return MatokeoYaNgeli("U-I_SG", 0.8, "prefix")
            return MatokeoYaNgeli("A-WA_SG", 0.7, "prefix")
        if w.startswith("wa") and len(w) > 4:
            return MatokeoYaNgeli("A-WA_PL", 0.7, "prefix")
        if w.startswith("ki") and len(w) > 4:
            return MatokeoYaNgeli("KI-VI_SG", 0.8, "prefix")
        if w.startswith(("vi", "vy")) and len(w) > 4:
            return MatokeoYaNgeli("KI-VI_PL", 0.8, "prefix")
        if w.startswith("mi") and len(w) > 4:
            return MatokeoYaNgeli("U-I_PL", 0.7, "prefix")
        if w.startswith("ma") and len(w) > 4:
            return MatokeoYaNgeli("LI-YA_PL", 0.8, "prefix")
        if w.startswith("m") and len(w) > 4:
            return MatokeoYaNgeli("A-WA_SG", 0.5, "prefix")
        if w.startswith("u") and len(w) > 4 and w != "ua":
            return MatokeoYaNgeli("U-I_SG", 0.6, "prefix")

        return MatokeoYaNgeli(None, 0.0, "none")


# ============================================================
# KANUNI YA YAMBIWA (KIAMBISHI CHA MTENDWA WA BINADAMU)
# ============================================================

class GenericObjectConcordRule:
    """
    Kanuni ya jumla (Generic Morphological Rule) inayokamata vitenzi vinavyofuatiwa na
    nomino ya binadamu (Yambiwa) bila kubeba kiambishi cha mtendwa (-m-, -mw-, -wa-).
    """

    def __init__(self):
        self.watu_umoja = {
            "mgonjwa", "mtoto", "mwanafunzi", "mwalimu", "daktari", "muuguzi",
            "mzazi", "baba", "mama", "kaka", "dada", "rafiki", "mgeni", "mtu",
            "kiongozi", "mfanyakazi", "mkulima", "mteja", "mwenzake", "askari",
            "dereva", "mhandisi", "hakimu", "msichana", "mvulana", "mwanamke", "mwanamume"
        }
        self.watu_wingi = {
            "wagonjwa", "watoto", "wanafunzi", "walimu", "madaktari", "wauguzi",
            "wazazi", "marafiki", "wageni", "watu", "viongozi", "wafanyakazi",
            "wakulima", "wateja", "wenzake", "maaskari", "madereva", "wahandisi",
            "mahakimu", "wasichana", "wavulana", "wanawake", "wanaume"
        }

        self.generic_applicative_regex = re.compile(
            r"^(?P<prefix>ku|kw|hatu|hawa|ham|ha|hu|si|ni|u|a|tu|m|wa|ki|vi|li|ya|i|zi)"
            r"(?P<tense>ngali|ngeli|nge|na|li|ta|me|ka|ki)?"
            r"(?P<rel>ye|o|lo|yo|cho|vyo|wo|zo|ko|po|mo)?"
            r"(?P<obj>mw|m|wa|ni|ku|tu|ji)?"
            r"(?P<stem>[a-z]{2,}?(?:li|le|i|e)a)$"
        )

        self.vitenzi_vya_kuachwa = {"kuwa", "kulia", "kushoto", "kwenda", "kuja", "kufika", "kukaa", "kutumia"}

    def kagua(self, sentensi: str) -> List[Kosa]:
        makosa = []
        for match in re.finditer(r"\b([a-zA-Z]+)\s+([a-zA-Z]+)\b", sentensi):
            kitenzi_asili = match.group(1)
            nomino_asili = match.group(2)
            kitenzi = kitenzi_asili.lower()
            nomino = nomino_asili.lower()

            if nomino not in self.watu_umoja and nomino not in self.watu_wingi:
                continue
            if kitenzi in self.vitenzi_vya_kuachwa:
                continue

            m = self.generic_applicative_regex.match(kitenzi)
            if not m:
                continue

            p = m.groupdict()
            if p["obj"]:
                continue

            prefix = p["prefix"] or ""
            tense = p["tense"] or ""
            rel = p["rel"] or ""
            stem = p["stem"]

            if nomino in self.watu_umoja:
                # BUG ILIYOREKEBISHWA: Kukagua herufi ya kwanza ya stem (stem[0])
                kiambishi = "mw" if stem and stem[0] in "aeiou" else "m"
                pendekezo = f"{prefix}{tense}{rel}{kiambishi}{stem}"
                if kitenzi_asili.isupper():
                    pendekezo = pendekezo.capitalize()
                makosa.append(Kosa(
                    aina="MOFOLOJIA",
                    neno=f"{kitenzi_asili} {nomino_asili}",
                    nafasi=match.start(),
                    urefu=len(match.group(0)),
                    ujumbe=f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' kinakosa kiambishi cha mtendwa '-{kiambishi}-'.",
                    mapendekezo=[f"{pendekezo} {nomino_asili}"],
                    chanzo="Kanuni ya Yambiwa (Human Object Concord)"
                ))
            elif nomino in self.watu_wingi:
                pendekezo = f"{prefix}{tense}{rel}wa{stem}"
                if kitenzi_asili.isupper():
                    pendekezo = pendekezo.capitalize()
                makosa.append(Kosa(
                    aina="MOFOLOJIA",
                    neno=f"{kitenzi_asili} {nomino_asili}",
                    nafasi=match.start(),
                    urefu=len(match.group(0)),
                    ujumbe=f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' (wingi) kinakosa kiambishi cha mtendwa '-wa-'.",
                    mapendekezo=[f"{pendekezo} {nomino_asili}"],
                    chanzo="Kanuni ya Yambiwa (Plural Object Concord)"
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
        self.yambiwa = GenericObjectConcordRule()

    def kagua(self, sentensi: str, kagua_alama: bool = True) -> list[Kosa]:
        makosa: list[Kosa] = []

        if not sentensi or not sentensi.strip():
            return [Kosa("TAWALI", "", 0, 0, "Sentensi ni tupu.")]

        if kagua_alama:
            makosa.extend(self._kagua_uandishi(sentensi))

        makosa.extend(self._kagua_upatanisho_vivumishi(sentensi))
        makosa.extend(self._kagua_kiroboti(sentensi))
        makosa.extend(self._kagua_upatanisho_kiima_kitenzi(sentensi))
        makosa.extend(self.yambiwa.kagua(sentensi))
        makosa.extend(self._kagua_kanuni_maalum(sentensi))

        makosa.sort(key=lambda k: k.nafasi)
        return makosa

    def _kagua_kanuni_maalum(self, sentensi: str) -> list[Kosa]:
        makosa: list[Kosa] = []
        for muundo, badala, aina, ujumbe, chanzo in self.KANUNI_MAALUM:
            for m in muundo.finditer(sentensi):
                neno_lililokosewa = m.group(0)
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

    _MUUNDO_WA_KITENZI = re.compile(r"^(wa|ki|vi|ya|li|zi)(na|li|me|ta|ka|nge|ngali|ngeli)[a-z]{2,}$")

    def _ni_nomino_ya_kuaminika(self, neno: str, uhakika_wa_chini: float) -> Optional[str]:
        m = self.kitambuzi.tambua(neno)
        if not m.ngeli or m.uhakika < uhakika_wa_chini:
            return None
        if m.uhakika < 0.9:
            n = neno.lower()
            if self._MUUNDO_WA_KITENZI.match(n):
                return None
            if any(n.endswith(z) and n != z for z in self.VIVUMISHI_MIZIZI):
                return None
        return m.ngeli

    @staticmethod
    def _kuna_mpaka(sentensi: str, mwisho_wa_kwanza: int, mwanzo_wa_pili: int) -> bool:
        return any(c in ",;:.!?" for c in sentensi[mwisho_wa_kwanza:mwanzo_wa_pili])

    def _kagua_upatanisho_vivumishi(self, sentensi: str) -> list[Kosa]:
        makosa: list[Kosa] = []
        tokens = list(re.finditer(r"\b[\w']+\b", sentensi))

        for i, m in enumerate(tokens):
            t_lower = m.group(0).lower()

            kivumishi_mzizi = None
            for mzizi in self.VIVUMISHI_MIZIZI:
                if t_lower.endswith(mzizi) and t_lower != mzizi:
                    kivumishi_mzizi = mzizi
                    break

            if not kivumishi_mzizi or t_lower in self.MANENO_YENYE_MAANA_MBILI:
                continue

            kiambishi = t_lower[: -len(kivumishi_mzizi)]
            nomino, ngeli = None, None
            for j in range(i - 1, -1, -1):
                if self._kuna_mpaka(sentensi, tokens[j].end(), tokens[j + 1].start()):
                    break
                ngeli_j = self._ni_nomino_ya_kuaminika(tokens[j].group(0), 0.5)
                if ngeli_j:
                    nomino = tokens[j].group(0)
                    ngeli = ngeli_j
                    break
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
                    ujumbe=f"Kivumishi '{m.group(0)}' hakitoshani na nomino '{nomino}' ({ngeli}). Kiambishi kinachotakiwa ni mojawapo ya: {sheria['adj_prefixes']}.",
                    mapendekezo=mapendekezo,
                    chanzo="ngeli_matrix",
                ))
        return makosa

    def _kagua_upatanisho_kiima_kitenzi(self, sentensi: str) -> list[Kosa]:
        makosa: list[Kosa] = []
        tokens = list(re.finditer(r"\b[\w']+\b", sentensi))
        mizizi_vitenzi = {"kuj", "fany", "pend", "sik", "end", "let", "it", "sem", "nun", "uz", "fung", "kal", "chez", "imb", "andik", "soma", "nyw", "la", "f", "w", "ja", "taka", "wez", "ju", "on", "sik"}

        for i, m in enumerate(tokens):
            t_lower = m.group(0).lower()
            if len(t_lower) < 3:
                continue

            m_kitenzi = re.match(
                r"^(?P<sc>ha|hu|si|ni|a|u|tu|m|wa|ki|vi|li|ya|i|zi)?"
                r"(?P<tense>na|li|ta|me|ka|ki|nge|ngali|ngeli)?"
                r"(?P<stem>[a-z]{2,}?)"
                r"(?P<fv>[aei])$",
                t_lower,
            )
            if not m_kitenzi:
                continue

            if self._ni_nomino_ya_kuaminika(t_lower, 0.0):
                continue

            stem = m_kitenzi.group("stem")
            if not any(mzizi in stem for mzizi in mizizi_vitenzi):
                continue
            if any(rel in t_lower for rel in ("ye", "lo", "cho", "vyo", "zo", "ko", "po", "mo")):
                continue

            sc = m_kitenzi.group("sc")
            if not sc:
                continue

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
                    ujumbe=f"Kitenzi '{m.group(0)}' hakitoshi kiima '{nomino}' ({ngeli}). Kiambishi cha kiima kinachotakiwa ni mojawapo ya: {sheria['verb_pos']}.",
                    mapendekezo=[f"{p}{t_lower[len(sc):]}" for p in sheria["verb_pos"][:2]],
                    chanzo="kiima_kitenzi",
                ))
        return makosa

    def _kagua_kiroboti(self, sentensi: str) -> list[Kosa]:
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
    def __init__(self):
        self._kaguzi = MkaguziSarufi()

    def tambua_ngeli(self, neno: str) -> Optional[str]:
        return self._kaguzi.kitambuzi.tambua(neno).ngeli

    def tambua_ngeli_kwa_uhakika(self, neno: str) -> MatokeoYaNgeli:
        return self._kaguzi.kitambuzi.tambua(neno)

    def kagua_sentensi_nzima(self, sentensi: str, kagua_alama: bool = True) -> dict:
        makosa = self._kaguzi.kagua(sentensi, kagua_alama=kagua_alama)
        return {
            "sahihi": len(makosa) == 0,
            "idadi_ya_makosa": len(makosa),
            "makosa": [k.to_dict() for k in makosa],
            "sentensi_iliyokaguliwa": sentensi,
            "mapendekezo": [m for k in makosa for m in k.mapendekezo],
        }

    def kagua_na_kurekebisha(self, sentensi: str) -> dict:
        matokeo = self.kagua_sentensi_nzima(sentensi)
        iliyorekebishwa = sentensi
        mabadiliko = []

        makosa_ya_kurekebisha = sorted(
            [k for k in matokeo["makosa"] if k["aina"] in ("NGELI", "MOFOLOJIA", "MTINDO", "ISTILAHI") and k["mapendekezo"]],
            key=lambda k: k["nafasi"],
            reverse=True,
        )
        mwisho_wa_awali = len(sentensi) + 1
        for k in makosa_ya_kurekebisha:
            n, u = k["nafasi"], k["urefu"]
            if n + u > mwisho_wa_awali:
                continue
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
