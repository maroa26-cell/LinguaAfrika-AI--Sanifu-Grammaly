"""
kanuni_ya_sarufi.py — Injini Kuu ya Sheria na Kanuni za Sarufi ya Kiswahili Sanifu (BAKITA).
Inatumiwa na cerebral_cortex.py na app.py kwa ajili ya tafsiri za AI Lingual na uhakiki wa maandishi.

Toleo 2.5 (Kanuni Kamili 1-16, Yambiwa, na Kanuni Maalum):
- Imeunganisha sheria zote 16 za lugha kwenye MAELEKEZO_YA_LUGHA
- Imeboresha GenericObjectConcordRule (Kanuni ya Yambiwa) na kurekebisha bug ya stem[0]
- Imeongeza Kanuni L, M, N za mtindo, istilahi za kitiba, na ngeli I-ZI kwenye MkaguziSarufi

Marekebisho ya 2.5 (kutokana na ukaguzi):
- Kivumishi: viambishi halali pekee (alisema/kusema/anasema hazichukuliwi tena kama kivumishi)
- Yambiwa: jozi za maneno zinapishana sasa (kitenzi katikati ya sentensi kinakamatwa)
- Kanuni M2 (maambukizi magumu) haibadilishi 'magumu kutibu'; ISTILAHI si ya kiotomatiki tena
- I-ZI wingi (nyumba zimejengwa) na wanyama wa I-ZI (ndege wamefika) havikamatwi kimakosa
- Kanuni L inahifadhi herufi ndogo katikati ya sentensi ('pale')
- Kanuni N inafanya kazi kwa vifungu vingi, si kimoja tu
- Kichujio cha mizizi ya vitenzi hakina tena maingizo ya herufi moja/mbili
- Kanuni mpya: ngeli ya mahali ('darasani yenye') na urudiaji wa maneno ('kubwa kubwa')
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
        "6) MANDATORY HUMAN OBJECT INFIX (YAMBIWA): Whenever an applicative or transitive verb is followed directly by a human recipient/beneficiary (e.g., mgonjwa, mtoto, watu), include '-m-', '-mw-', or '-wa-' before the verb root ('kumwandikia mgonjwa', 'nilimwambia mtoto'). EXCEPTION: When explaining a topic/guideline ('explain guidelines'), prefer 'aeleze kuhusu miongozo' instead of 'awaelezee miongozo'. "
        "7) ANIMACY & VERB MORPHOLOGY: "
        "(a) All living beings (people, animals, birds, insects) take A-WA concord regardless of noun prefix ('simba amenguruma', 'madaktari wamefika'). "
        "(b) Tense negation: '-na-' becomes 'ha-...-i' ('hasomi'), '-li-' becomes 'ha-ku-' ('hakusoma'), '-me-' becomes 'ha-ja-' ('hajasoma'). "
        "(c) Monosyllabic verbs retain '-ku-' in positive tenses ('anakula', 'alikunywa', 'angekuja') and drop it in negation ('hali', 'hakunywa'). "
        "(d) Use 'amba-' for relative clauses in '-me-' tense or negation ('ambaye amefika', 'ambaye hakufika'). "
        "(e) Use 'na' for passive agents ('alipigwa na mwalimu') and 'kwa' for instruments or manner ('aliandika kwa kalamu'). "
        "8) ADVANCED EDITORIAL RULES: "
        "(a) LOCATIVE COPULA: Never use 'ni' for location; use '-po/-ko/-mo' ('Kitabu kipo mezani', 'Wageni wako nyumbani'). Use 'kuwa' for non-present copula ('alikuwa daktari'). "
        "(b) ASSOCIATIVE '-A': Match '-a' strictly to the possessed noun's class ('kitabu cha', 'majina ya', 'uhuru wa'). "
        "(c) HABITUAL 'HU-': Never attach subject prefixes to 'hu-' ('mimi husoma', 'wao husoma'). "
        "(d) PASSIVE BORROWED VERBS: Arabic-origin verbs ending in -e/-i/-u take '-ewa/-iwa' in passive ('samehewa', 'tafsiriwa', 'jaribiwa'). "
        "(e) 'KILA' AGREEMENT: 'Kila' always takes singular nouns and singular verbs ('kila mwanafunzi ana'). "
        "(f) NARRATIVE '-KA-': In sequential past actions, use '-li-' on the first verb and '-ka-' on subsequent verbs ('Aliamka, akanawa, akaenda'). "
        "(g) NEGATIVE INFINITIVE: Use 'kuto-' for multisyllabic verbs ('kutosoma', 'kutofika') and 'kutoku-' only for monosyllabic verbs ('kutokula', 'kutokuja'). "
        "(h) MODAL 'LAZIMA': Follow 'lazima' or 'sharti' with the subjunctive '-e' ('Lazima afike'). "
        "9) KINSHIP & HONORIFIC PLURALS (SINGLE & COORDINATED 'AKINA'): Kinship and honorific nouns with zero plural prefixes (mama, baba, dada, kaka, bibi, babu, shangazi, mjomba) MUST take 'akina' in the plural. When two such nouns are coordinated with 'na', repeat 'akina' before EACH noun ('akina baba na akina mama wengi'). "
        "10) COUNTERFACTUAL CONDITIONALS ('KAMA' vs 'IWAPO'): Never use 'Iwapo' or 'Ikiwa' with counterfactual conditional verbs containing '-nge-', '-ngali-', or '-ngeli-'. Always use 'Kama' ('Kama majukwaa yasingeanzishwa...'). "
        "11) TEMPORAL CLAUSES ('PALE ... -PO-'): When translating English 'When [subject] [verb]...' using the Swahili '-po-' temporal infix, NEVER start with a literal 'Wakati'. Use 'Pale' ('Pale muuguzi anapowaelezea...'). "
        "12) MEDICAL & CLINICAL IDIOMATIC PRECISION: Translate 'expectant mothers' strictly as 'akina mama wajawazito' and 'complex infections' as 'maambukizi magumu kufahamika'. "
        "13) COUNTERFACTUAL MODAL VERBS ('WANGEWEZA KU-'): Never use the calque 'wangekuwa wame-' for 'would have + verb'. Use 'wangeweza ku-' ('wangeweza kuiba') or direct conditional ('wangeiba'). "
        "14) DOUBLE-VOWEL VERB NEGATION ('-ZUI-I'): Preserve stem vowels before adding negative '-i' ('hakuzuii', 'hauzuii', never 'hakuzii'). "
        "15) I-ZI PLURAL CONDITIONAL NEGATION ('ZISINGE-'): Plural I-ZI nouns (such as 'mamlaka za...', 'taasisi za...', 'shule za...') take 'zisinge-' in negative conditionals ('mamlaka za eneo zisingejenga', NEVER 'hazingejenga'). "
        "16) DIGITAL & INTERACTIVE EDUCATION TERMINOLOGY: Translate 'digital learning tools' as 'zana za kujifunza kupitia njia za kidijitali' (NEVER 'zana za kujifunza kidijitali'), and translate 'interactive lessons' as 'masomo kupitia njia shirikishi' (NEVER 'masomo ya mwingiliano')."
    ),
    "Kichina": "Write in Simplified Chinese characters (Mandarin).",
    "Kireno": "Use standard Portuguese as used in Mozambique and Angola (European norms).",
    "Kizulu": "Write in standard isiZulu (South Africa), using correct noun-class concord.",
    "Setswana": "Write in standard Setswana as used in Botswana (Tswana orthography).",
}

# Kanuni zinazotumika kwa jozi maalum ya lugha (chanzo, lengwa), majina yakiwa herufi ndogo
MAELEKEZO_YA_JOZI = {
    ("kiingereza", "kiswahili"): (
        "ENGLISH-TO-SWAHILI TRANSLATION RULES: "
        "1) VERB PARALLELISM: Maintain consistent tense markers across lists of actions in a sentence. "
        "If the first verb uses the habitual tense ('hu-'), all subsequent parallel verbs must also use 'hu-' "
        "(e.g., 'hujenga uaminifu, huhamasisha ubunifu, na huhakikisha ukuaji', NOT 'hujenga... kuhamasisha...'). "
        "2) NATURAL IDIOMS: Translate English idioms and legal/business expressions by their contextual meaning, "
        "never word-for-word (e.g., 'sign on the dotted line' -> 'kutia saini mkataba rasmi', NOT 'mstari wa nukta'). "
        "3) GERUND (KU- CLASS) AGREEMENT: When a sentence starts with a verbal noun (e.g., 'Kupuuza...'), ensure all "
        "dependent verbs in the sentence retain the 'ku-' prefix ('kunaweza'), regardless of intermediate nouns. "
        "4) DOMAIN-SPECIFIC VOCABULARY: Use precise professional Swahili terms: translate 'productivity' in workplaces "
        "as 'tija', 'trust' as 'uaminifu', 'share goals' as 'shirikisha malengo', and 'advanced infections' as "
        "'maambukizi yaliyokwisha komaa'. "
        "5) SPELLING & PUNCTUATION: Ensure standard spelling ('mhimili', not 'muhimili') and always end the final "
        "sentence with a proper period (.)."
    ),
}

_MAJINA_MBADALA = {"english": "kiingereza", "swahili": "kiswahili"}


def _jina_la_msingi(lugha: str) -> str:
    """'Kiingereza (English)' -> 'kiingereza'; 'English' -> 'kiingereza'."""
    j = re.sub(r"\s*\(.*?\)", "", lugha or "").strip().lower()
    return _MAJINA_MBADALA.get(j, j)


def ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo: str, lugha_lengwa: str = "Kiswahili") -> bool:
    return (_jina_la_msingi(lugha_chanzo), _jina_la_msingi(lugha_lengwa)) == ("kiingereza", "kiswahili")


def maelekezo_ya_jozi(lugha_chanzo: str, lugha_lengwa: str) -> str:
    """Kanuni za jozi hiyo pekee (mfano Kiingereza -> Kiswahili); tupu kama hakuna."""
    return MAELEKEZO_YA_JOZI.get((_jina_la_msingi(lugha_chanzo), _jina_la_msingi(lugha_lengwa)), "")


def maelekezo_ya_tafsiri(lugha_chanzo: str, lugha_lengwa: str) -> str:
    """Kanuni za lugha lengwa (MAELEKEZO_YA_LUGHA) pamoja na kanuni za jozi. Itumie kwenye mtafsiri wako."""
    msingi = next((v for k, v in MAELEKEZO_YA_LUGHA.items()
                   if _jina_la_msingi(k) == _jina_la_msingi(lugha_lengwa)), "")
    return (msingi + " " + maelekezo_ya_jozi(lugha_chanzo, lugha_lengwa)).strip()


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
# KANUNI YA YAMBIWA (GENERIC OBJECT CONCORD RULE)
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
            r"(?P<tense>singali|singeli|singe|ngali|ngeli|nge|na|li|ta|me|ka|ki)?"
            r"(?P<rel>ye|o|lo|yo|cho|vyo|wo|zo|ko|po|mo)?"
            r"(?P<obj>mw|m|wa|ni|ku|tu|ji)?"
            r"(?P<stem>[a-z]{2,}?(?:li|le|i|e)a)$"
        )

        self.vitenzi_vya_kuachwa = {"kuwa", "kulia", "kushoto", "kwenda", "kuja", "kufika", "kukaa", "kutumia"}

    def kagua(self, sentensi: str) -> List[Kosa]:
        makosa = []
        # Lookahead: jozi zinapishana, kwa hiyo kitenzi popote kwenye sentensi kinakaguliwa
        for match in re.finditer(r"\b([a-zA-Z]+)(?=\s+([a-zA-Z]+)\b)", sentensi):
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

            nafasi = match.start(1)
            urefu = match.end(2) - match.start(1)
            neno_asili = sentensi[nafasi: nafasi + urefu]

            if nomino in self.watu_umoja:
                kiambishi = "mw" if stem and stem[0] in "aeiou" else "m"
                pendekezo = f"{prefix}{tense}{rel}{kiambishi}{stem}"
                if kitenzi_asili[0].isupper():
                    pendekezo = pendekezo.capitalize()
                makosa.append(Kosa(
                    aina="MOFOLOJIA",
                    neno=neno_asili,
                    nafasi=nafasi,
                    urefu=urefu,
                    ujumbe=f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' kinakosa kiambishi cha mtendwa '-{kiambishi}-'.",
                    mapendekezo=[f"{pendekezo} {nomino_asili}"],
                    chanzo="Kanuni ya Yambiwa (Human Object Concord)"
                ))
            elif nomino in self.watu_wingi:
                pendekezo = f"{prefix}{tense}{rel}wa{stem}"
                if kitenzi_asili[0].isupper():
                    pendekezo = pendekezo.capitalize()
                makosa.append(Kosa(
                    aina="MOFOLOJIA",
                    neno=neno_asili,
                    nafasi=nafasi,
                    urefu=urefu,
                    ujumbe=f"Kitenzi '{kitenzi_asili}' kinapofuatiwa na '{nomino_asili}' (wingi) kinakosa kiambishi cha mtendwa '-wa-'.",
                    mapendekezo=[f"{pendekezo} {nomino_asili}"],
                    chanzo="Kanuni ya Yambiwa (Plural Object Concord)"
                ))

        return makosa


# ============================================================
# MKAGUZI WA SARUFI
# ============================================================

# Tahajia: makosa ya kawaida -> sahihi
MAKOSA_YA_TAHAJIA = {"muhimili": "mhimili"}

# Msamiati wa kitaaluma Kiingereza -> Kiswahili. Hukaguliwa tu kama maandishi ya Kiingereza yana 'chanzo'.
# 'makosa': (muundo wa tafsiri isiyo sahihi, mbadala). Mbadala unaweza kutumia \g<0> kwa neno lililopatikana.
MSAMIATI_WA_KIINGEREZA = [
    {"jina": "productivity -> tija", "chanzo": r"\bproductivity\b",
     "makosa": [(r"\buzalishaji\b", "tija")],
     "ujumbe": "Kwa mahali pa kazi, 'productivity' hutafsiriwa 'tija', si 'uzalishaji'."},
    {"jina": "trust -> uaminifu", "chanzo": r"\btrust\b",
     "makosa": [(r"\bimani\b", "uaminifu")],
     "ujumbe": "'Trust' hutafsiriwa 'uaminifu', si 'imani'."},
    {"jina": "share goals -> shirikisha malengo", "chanzo": r"\bshar(?:e|es|ed|ing)\b[^.!?]{0,30}\bgoals?\b",
     "makosa": [(r"\b(?:[a-z]{1,3}(?:na|li|ta|me|ki|ka)(?:po|o|ye|yo|lo|cho)?|ku|hu)shiriki"
                 r"(?=\s+(?:\w+\s+)?malengo\b)", r"\g<0>sha")],
     "ujumbe": "'Share goals' hutafsiriwa 'shirikisha malengo' ('shiriki' ni kujiunga, si kuwapa wengine)."},
    {"jina": "advanced infections", "chanzo": r"\badvanced\s+infections?\b",
     "makosa": [(r"\bmaambukizi\s+(?:ya\s+(?:hali|hatua)\s+ya\s+juu|ya\s+juu|yaliyoendelea|makali)\b",
                 "maambukizi yaliyokwisha komaa")],
     "ujumbe": "'Advanced infections' hutafsiriwa 'maambukizi yaliyokwisha komaa'."},
]


def _tumia_makosa(maandishi: str, makosa: list) -> tuple[str, list]:
    """Hutumia pendekezo la kwanza la kila kosa lisilopishana na jingine. Hurudisha (maandishi, mabadiliko)."""
    safi, mwisho = [], 0
    for k in sorted(makosa, key=lambda x: (x.nafasi, -x.urefu)):
        if k.mapendekezo and k.nafasi >= mwisho and maandishi[k.nafasi:k.nafasi + k.urefu] == k.neno:
            safi.append(k)
            mwisho = k.nafasi + k.urefu
    mabadiliko = []
    for k in reversed(safi):
        maandishi = maandishi[:k.nafasi] + k.mapendekezo[0] + maandishi[k.nafasi + k.urefu:]
        mabadiliko.append({"kabla": k.neno, "baada": k.mapendekezo[0], "aina": k.aina, "sababu": k.ujumbe})
    mabadiliko.reverse()
    return maandishi, mabadiliko


def _pale_kwa_herufi(m: "re.Match") -> str:
    """Kanuni L: huhifadhi herufi kubwa/ndogo ya 'Wakati' -> 'Pale'/'pale'."""
    pale = "Pale" if m.group(0)[0].isupper() else "pale"
    return f"{pale} {m.group(1)} {m.group(2)}"


def _isinge_kwa_nomino(m: "re.Match") -> str:
    """Kanuni N: '<nomino> [ya/za ...] hainge-X' -> '<nomino> [ya/za ...] isinge-X' (zisinge- kwa 'za')."""
    nomino, kishazi, shina = m.group(1), m.group(2), m.group(3)
    kiambishi = "zisinge" if kishazi and kishazi.lower().startswith("za") else "isinge"
    kati = f" {kishazi}" if kishazi else ""
    return f"{nomino}{kati} {kiambishi}{shina}"


class MkaguziSarufi:
    """
    Hukagua sentensi kwa:
      - Upatanisho wa ngeli (nomino ↔ kivumishi kilicho karibu)
      - Nahau/methali zilizokopwa vibaya (kiroboti)
      - Uandishi (herufi kubwa, alama ya kituo)
      - Umoja wa kisintaksia wa sentensi
      - Kanuni maalum za mtindo, istilahi, na upatanisho wa I-ZI
      - Ngeli ya mahali ('darasani yenye') na urudiaji wa maneno ('kubwa kubwa')
    """

    VIVUMISHI_MIZIZI = {
        "zuri", "baya", "kubwa", "dogo", "refu", "fupi", "pya", "zee",
        "gumu", "laini", "eupe", "eusi", "ekundu", "ingi", "chache",
        "ema", "kali", "pole", "vivu", "zito", "epesi", "tamu", "chungu",
    }

    MANENO_YENYE_MAANA_MBILI = {"kali", "pole", "tamu", "chungu", "zito"}

    # Viambishi halali vya kivumishi. Neno kama 'alisema' (kiambishi 'alis') si kivumishi.
    VIAMBISHI_VYA_VIVUMISHI = {"m", "mw", "wa", "w", "mi", "my", "ki", "ch",
                               "vi", "vy", "ma", "n", "ny", "u", "ji", "j"}
    # Maneno yanayoishia kama kivumishi lakini ni nomino
    MANENO_YA_KURUKA = {"ukubwa", "wazee", "mzee"}

    # Ngeli ya mahali: 'darasani yenye' -> 'darasa lenye'
    NGELI_YENYE = {
        "darasa": "lenye", "soko": "lenye", "shamba": "lenye", "jiji": "lenye",
        "shule": "yenye", "nyumba": "yenye", "barabara": "yenye",
        "kitabu": "chenye", "kijiji": "chenye", "mji": "wenye", "mkoa": "wenye",
    }
    # Nomino zinazoishia -ni lakini si maneno ya mahali ('kampuni yenye' ni sahihi)
    NOMINO_ZENYE_NI = {"kampuni", "leseni", "televisheni", "benki", "taasisi",
                       "akaunti", "nini", "ini", "jini", "kuni", "kiini"}
    MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara"}

    # Nomino ya karibu pekee ndiyo inayoaminika: 'Kampuni yenye wafanyakazi wengi imefungua'
    # ina kiima 'Kampuni', si 'wafanyakazi'. Umbali mdogo hupunguza tahadhari za uongo.
    UMBALI_KIVUMISHI = 2
    UMBALI_KITENZI = 1

    # Wanyama wa umbo la I-ZI wanaochukua upatanisho wa A-WA (sheria 7a)
    WANYAMA_WA_I_ZI = {"nyuki", "nyati", "ndege", "samaki", "simba", "paka", "mbwa"}

    MAKOSA_YA_KIROBOTI = {
        "mimi ni baridi": "Tumia 'Nasikia baridi' au 'Nahisi baridi'",
        "mimi ni njaa": "Tumia 'Nina njaa'",
        "fanya akili": "Tumia 'Leta maana' au 'Kuwa na mantiki'",
        "hata ingawa": "Tumia neno moja tu: 'Ingawa' au 'Ijapokuwa'",
        "walikataa kukata tamaa": "Epuka urudiaji wa mzizi; tumia 'hawakukata tamaa' au 'walikataa kusalimu amri'",
        "fanya maamuzi": "Tumia 'fanya uamuzi'",
        "mstari wa nukta": "Tafsiri nahau kwa maana yake: 'kutia saini mkataba rasmi' (si neno kwa neno)",
    }

    # Orodha ya Kanuni Maalum (Regex, Badala (kamba au kazi), Aina, Ujumbe, Chanzo)
    KANUNI_MAALUM = [
        # L. 'Wakati [nomino] ana-po-' -> 'Pale [nomino] ana-po-'
        (
            re.compile(r"\bWakati\s+([a-z]+)\s+([a-z]*(?:na|li|taka)po[a-z]+)\b", re.I),
            _pale_kwa_herufi,
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
        # M2. Maambukizi magumu (haigusi 'magumu kutibu', 'magumu kudhibiti')
        (
            re.compile(r"\bmaambukizi\s+magumu\b(?!\s+(?:kufahamika|kutibu|kutibika|kudhibiti|kuzuia))", re.I),
            "maambukizi magumu kufahamika",
            "ISTILAHI",
            "Kwa muktadha wa uchunguzi wa maabara ('complex infections'), tumia 'maambukizi magumu kufahamika'.",
            "Istilahi za Tiba"
        ),
        # N. Upatanisho wa Ngeli ya I-ZI kwenye Ukanushi wa Masharti
        (
            re.compile(
                r"\b(kliniki|zahanati|hospitali|kampuni|serikali|taasisi|benki|shule|mamlaka)"
                r"(?:\s+((?:ya|za)\s+[a-z]+(?:\s+hilo)?))?\s+hainge([a-z]+)\b",
                re.I,
            ),
            _isinge_kwa_nomino,
            "NGELI",
            "Nomino ya ngeli ya I-ZI inachukua ukanushi 'isinge-' (wingi: 'zisinge-') badala ya 'hainge-'.",
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
        makosa.extend(self._kagua_ngeli_mahali(sentensi))
        makosa.extend(self._kagua_marudio(sentensi))
        makosa.extend(self._kagua_usambamba_wa_vitenzi(sentensi))
        makosa.extend(self._kagua_usawa_wa_ku(sentensi))
        makosa.extend(self._kagua_tahajia(sentensi))

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

    def _kagua_ngeli_mahali(self, sentensi: str) -> list[Kosa]:
        """'darasani yenye' -> 'darasa lenye' (neno la mahali halichukui yenye/lenye/zenye)."""
        makosa: list[Kosa] = []
        for m in re.finditer(r"\b(\w+?)ni\s+(yenye|zenye|lenye|wenye|chenye|vyenye)\b", sentensi, re.I):
            msingi = m.group(1).lower()
            if f"{msingi}ni" in self.NOMINO_ZENYE_NI:
                continue
            baada = f"{msingi} {self.NGELI_YENYE.get(msingi, 'lenye')}"
            mbadala = f"{msingi}ni kwenye"
            if m.group(0)[0].isupper():
                baada, mbadala = baada.capitalize(), mbadala.capitalize()
            makosa.append(Kosa(
                aina="NGELI",
                neno=m.group(0),
                nafasi=m.start(),
                urefu=len(m.group(0)),
                ujumbe=f"'{msingi}ni' ni neno la mahali (PA-KU-MU); halichukui '{m.group(2)}'.",
                mapendekezo=[baada, mbadala],
                chanzo="Ngeli ya mahali",
            ))
        return makosa

    def _kagua_marudio(self, sentensi: str) -> list[Kosa]:
        """'kubwa kubwa' -> 'kubwa', isipokuwa marudio halali (polepole, kidogo kidogo)."""
        makosa: list[Kosa] = []
        for m in re.finditer(r"\b(\w+)(?:\s+\1\b)+", sentensi, re.I):
            if m.group(1).lower() in self.MARUDIO_HALALI:
                continue
            makosa.append(Kosa(
                aina="MTINDO",
                neno=m.group(0),
                nafasi=m.start(),
                urefu=len(m.group(0)),
                ujumbe=f"Neno '{m.group(1)}' limerudiwa bila sababu.",
                mapendekezo=[m.group(1)],
                chanzo="Urudiaji",
            ))
        return makosa

    # Maneno yanayoanza na hu-/ku- lakini si vitenzi vya hali ya kawaida au vya kuendelea
    _SI_VITENZI_VYA_HU = {"huduma", "hukumu", "huzuni", "huruma", "huko", "huku", "huyu", "hujambo", "hudhuria"}
    _SI_VITENZI_VYA_KU = {"kuhusu", "kutoka", "kutokana", "kulingana", "kuliko", "kupitia", "kuanzia",
                          "kuelekea", "kufuatia", "kuhusiana"}
    _VITENZI_VYA_KIIMA_CHA_KU = ("weza|leta|sababisha|changia|athiri|ongeza|punguza|hatarisha|zuia|"
                                 "saidia|ruhusu|chelewesha")

    def _kagua_usambamba_wa_vitenzi(self, s: str) -> list[Kosa]:
        """Kanuni T1: 'hujenga imani, kuhamasisha ubunifu, na kuhakikisha ukuaji' -> 'huhamasisha', 'huhakikisha'."""
        makosa: list[Kosa] = []
        for sen in re.finditer(r"[^.!?\n]+", s):
            t, msingi = sen.group(0), sen.start()
            tokens = list(re.finditer(r"[^\W\d_]+", t))
            for i, tok in enumerate(tokens):
                w = tok.group(0).lower()
                if not w.startswith("ku") or len(w) < 6 or w in self._SI_VITENZI_VYA_KU:
                    continue
                kabla_ya = t[:tok.start()].rstrip()
                if not (kabla_ya.endswith(",") or re.search(r",\s*na$", kabla_ya)):
                    continue                      # lazima aje baada ya mkato (au ', na') kwenye orodha
                j = next((k for k in range(i - 1, -1, -1)
                          if re.fullmatch(r"hu[a-z]{3,}", tokens[k].group(0).lower())
                          and tokens[k].group(0).lower() not in self._SI_VITENZI_VYA_HU), None)
                if j is None:
                    continue
                if j + 1 < i and tokens[j + 1].group(0).lower().startswith("ku"):
                    continue                      # 'hupenda kusoma, kuandika': ku- ni shamirisho, si usambamba
                makosa.append(Kosa(
                    aina="USAMBAMBA", neno=tok.group(0), nafasi=msingi + tok.start(), urefu=len(tok.group(0)),
                    ujumbe=f"Kitenzi '{tokens[j].group(0)}' kinatumia 'hu-', kwa hiyo vitenzi sambamba vinavyofuata "
                           f"vitumie 'hu-' pia ('{tok.group(0)}' -> 'hu{tok.group(0)[2:]}').",
                    mapendekezo=["hu" + tok.group(0)[2:]], chanzo="Usambamba wa vitenzi"))
        return makosa

    def _kagua_usawa_wa_ku(self, s: str) -> list[Kosa]:
        """Kanuni T3: 'Kupuuza dalili inaweza kusababisha...' -> 'kunaweza' (kiima cha ku- kinabaki ku-)."""
        makosa: list[Kosa] = []
        for sen in re.finditer(r"[^.!?\n]+", s):
            t, msingi = sen.group(0), sen.start()
            m0 = re.match(r"\s*(Ku[a-z]{3,})\b", t)
            if not m0 or m0.group(1).lower() in self._SI_VITENZI_VYA_KU:
                continue
            baada = t[m0.end():]
            eneo = baada.split(",")[0]            # mkato huanza kishazi kipya
            m = re.search(rf"\b(?:i|u|li|ya|a|zi|wa|ki|vi)(na|ta|me|li)({self._VITENZI_VYA_KIIMA_CHA_KU})\b", eneo)
            if m:
                makosa.append(Kosa(
                    aina="USAMBAMBA", neno=m.group(0), nafasi=msingi + m0.end() + m.start(), urefu=len(m.group(0)),
                    ujumbe=f"Sentensi inaanza na kitenzi jina '{m0.group(1)}', kwa hiyo kitenzi tegemezi kibaki na 'ku-'.",
                    mapendekezo=["ku" + m.group(1) + m.group(2)], chanzo="Usawa wa ku-"))
        return makosa

    def _kagua_tahajia(self, s: str) -> list[Kosa]:
        """Kanuni T5: 'muhimili' -> 'mhimili' n.k."""
        makosa: list[Kosa] = []
        for kosa_lake, sahihi in MAKOSA_YA_TAHAJIA.items():
            for m in re.finditer(rf"\b{re.escape(kosa_lake)}\b", s, re.I):
                badala = sahihi[0].upper() + sahihi[1:] if m.group(0)[0].isupper() else sahihi
                makosa.append(Kosa(
                    aina="TAHAJIA", neno=m.group(0), nafasi=m.start(), urefu=len(m.group(0)),
                    ujumbe=f"Tahajia sahihi ni '{sahihi}', si '{kosa_lake}'.",
                    mapendekezo=[badala], chanzo="Tahajia"))
        return makosa

    def kagua_msamiati(self, chanzo: str, tafsiri: str) -> list[Kosa]:
        """Kanuni T4: msamiati wa kitaaluma. Unahitaji maandishi ya Kiingereza ya chanzo."""
        makosa: list[Kosa] = []
        for ingizo in MSAMIATI_WA_KIINGEREZA:
            if not re.search(ingizo["chanzo"], chanzo or "", re.I):
                continue
            for muundo, sahihi in ingizo["makosa"]:
                for m in re.finditer(muundo, tafsiri, re.I):
                    badala = m.expand(sahihi)
                    if m.group(0)[:1].isupper():
                        badala = badala[:1].upper() + badala[1:]
                    makosa.append(Kosa(
                        aina="MSAMIATI", neno=m.group(0), nafasi=m.start(), urefu=len(m.group(0)),
                        ujumbe=ingizo["ujumbe"], mapendekezo=[badala],
                        chanzo=f"Msamiati wa kitaaluma ({ingizo['jina']})"))
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
                mapendekezo=[stripped[0].upper() + stripped[1:]],
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

            # Kiambishi lazima kiwe halali cha kivumishi; vinginevyo ni kitenzi/nomino (alisema, ukubwa)
            if kiambishi not in self.VIAMBISHI_VYA_VIVUMISHI or t_lower in self.MANENO_YA_KURUKA:
                continue

            nomino, ngeli = None, None
            for j in range(i - 1, max(i - 1 - self.UMBALI_KIVUMISHI, -1), -1):
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

    # Mizizi ya vitenzi (maingizo ya herufi moja/mbili yameondolewa ili kupunguza tahadhari za uongo)
    _MIZIZI_VITENZI = {"kuj", "fany", "pend", "sik", "end", "let", "sem", "nun", "fung", "kal",
                       "chez", "imb", "andik", "soma", "nyw", "taka", "wez", "fik", "jeng"}

    def _kagua_upatanisho_kiima_kitenzi(self, sentensi: str) -> list[Kosa]:
        makosa: list[Kosa] = []
        tokens = list(re.finditer(r"\b[\w']+\b", sentensi))
        mizizi_vitenzi = self._MIZIZI_VITENZI

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
            for j in range(i - 1, max(i - 1 - self.UMBALI_KITENZI, -1), -1):
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
            sc_halali = set(sheria["verb_pos"]) | set(sheria["verb_neg"])
            if ngeli.startswith("I-ZI"):
                # Nomino za I-ZI zina umbo moja kwa umoja na wingi
                sc_halali |= {"i", "zi", "hai", "hazi"}
                if nomino.lower() in self.WANYAMA_WA_I_ZI:
                    sc_halali |= {"a", "wa", "ha", "hawa", "yu", "hayu"}
            if sc not in sc_halali:
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

    def kagua_tafsiri(self, lugha_chanzo: str, chanzo: str, tafsiri: str) -> list:
        """Makosa ya msamiati wa kitaaluma kwenye tafsiri ya Kiingereza -> Kiswahili (inahitaji maandishi ya chanzo)."""
        if not ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo, "Kiswahili"):
            return []
        return [k.to_dict() for k in self._kaguzi.kagua_msamiati(chanzo, tafsiri)]

    def rekebisha_tafsiri(self, lugha_chanzo: str, chanzo: str, tafsiri: str, kituo_cha_mwisho: bool = True) -> dict:
        """
        Marekebisho ya kuaminika ya kanuni za tafsiri: tahajia, usambamba wa vitenzi (hu-), usawa wa ku-,
        msamiati wa kitaaluma (Kiingereza -> Kiswahili) na nukta ya mwisho. Hurudisha {'maandishi', 'mabadiliko'}.
        """
        jozi = ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo, "Kiswahili")
        maandishi, mabadiliko = tafsiri, []
        for _ in range(3):
            makosa = [k for k in self._kaguzi.kagua(maandishi, kagua_alama=False)
                      if k.aina in ("TAHAJIA", "USAMBAMBA")]
            if jozi and chanzo:
                makosa += self._kaguzi.kagua_msamiati(chanzo, maandishi)
            mpya, badiliko = _tumia_makosa(maandishi, makosa)
            if mpya == maandishi:
                break
            maandishi, mabadiliko = mpya, mabadiliko + badiliko
        if jozi and kituo_cha_mwisho and len(maandishi.split()) >= 2:
            t = maandishi.rstrip()
            if t and t[-1].isalnum():
                maandishi = t + "." + maandishi[len(t):]
                mabadiliko.append({"kabla": t[-1], "baada": t[-1] + ".", "aina": "ALAMA",
                                   "sababu": "Sentensi ya mwisho lazima iishie na nukta (.)."})
        return {"maandishi": maandishi, "mabadiliko": mabadiliko}

    def kagua_na_kurekebisha(self, sentensi: str) -> dict:
        matokeo = self.kagua_sentensi_nzima(sentensi)
        iliyorekebishwa = sentensi
        mabadiliko = []

        # ISTILAHI haijumuishwi: ni pendekezo tu, si la kiotomatiki (linaweza kubadilisha maana).
        # Marekebisho yanayopishana: lile linaloanza mapema (na refu zaidi) hupewa kipaumbele;
        # mengine hushughulikiwa awamu inayofuata, baada ya maandishi kubadilika.
        aina_za_kurekebisha = ("NGELI", "MOFOLOJIA", "MTINDO", "TAHAJIA", "USAMBAMBA")
        for _awamu in range(3):
            makosa_ya_awamu = self.kagua_sentensi_nzima(iliyorekebishwa)["makosa"]
            kandidati = sorted(
                [k for k in makosa_ya_awamu if k["aina"] in aina_za_kurekebisha and k["mapendekezo"]],
                key=lambda k: (k["nafasi"], -k["urefu"]),
            )
            chaguo, mwisho_wa_awali = [], 0
            for k in kandidati:
                if k["nafasi"] >= mwisho_wa_awali:
                    chaguo.append(k)
                    mwisho_wa_awali = k["nafasi"] + k["urefu"]
            if not chaguo:
                break
            kabla = iliyorekebishwa
            for k in reversed(chaguo):
                n, u = k["nafasi"], k["urefu"]
                pendekezo = k["mapendekezo"][0]
                iliyorekebishwa = iliyorekebishwa[:n] + pendekezo + iliyorekebishwa[n + u:]
                mabadiliko.append({"kutoka": k["neno"], "kwenda": pendekezo})
            if iliyorekebishwa == kabla:
                break

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

# ============================================================
# MAJARIBIO YA HARAKA
# ============================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    kanuni = KanuniZaSarufiKiswahili()

    sentensi_za_majaribio = [
        "Mtoto mdogo alikula chakula kitamu.",
        "Wakati muuguzi anapowaelezea wagonjwa, ni muhimu kusikiliza.",
        "Akina mama wanaotarajia wanahitaji huduma maalum.",
        "Kliniki ya eneo hilo haingepokea wagonjwa wengi.",
        "Mimi ni baridi leo asubuhi.",
        "Aliandikia mgonjwa barua."
    ]

    for s in sentensi_za_majaribio:
        matokeo = kanuni.kagua_sentensi_nzima(s)
        print(f"\n➤ {s}")
        print(f"   Sahihi: {matokeo['sahihi']}  |  Makosa: {matokeo['idadi_ya_makosa']}")
        for k in matokeo["makosa"]:
            print(f"   - [{k['aina']}] {k['ujumbe']}")
            if k["mapendekezo"]:
                print(f"     ↳ Mapendekezo: {k['mapendekezo'][:2]}")
