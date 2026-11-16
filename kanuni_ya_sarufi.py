"""
kanuni_ya_sarufi.py — Injini Kuu ya Sheria na Kanuni za Sarufi ya Kiswahili Sanifu (BAKITA).
Inatumiwa na cerebral_cortex.py na app.py kwa ajili ya tafsiri za AI Lingual na uhakiki wa maandishi.

Toleo 2.6 (marekebisho ya ukaguzi):
- Bug 1: _MIZIZI_VITENZI ina "som"/"tak" badala ya "soma"/"taka" — vitenzi vya
         kawaida (wanasoma, anasoma, alisoma, anataka, alitaka) sasa vinakaguliwa.
- Bug 2: _kagua_ngeli_mahali inatumia .get() salama — haitengenezi maneno yasiyokuwepo
         (jira, mtiha, steshe) kwa nomino isiyojulikana; inatoa "kwenye" pekee.
- Bug 3: _kagua_uandishi inarudisha nafasi/urefu/neno vinavyolingana — _tumia_makosa
         inaweza kutumia ALAMA sasa (kabla haikufanya kazi kimya kimya).
- Bug 4: _kagua_usambamba_wa_vitenzi inakagua tokens[j+1:i] (si tokens[j+1] pekee) —
         "hujenga, kuhamasisha" sasa inakamatwa.
- Bug 6: _isinge_kwa_nomino imepanuliwa (biashara, shirika, taarifa, sekta, ...).
- Bug 7: _kagua_upatanisho_kiima_kitenzi inahifadhi herufi kubwa kwenye mapendekezo.
- Bug 10: adj_prefixes ya LI-YA_SG haina "" (haikufikiwa kamwe).
- Bug 11: KitambuziNgeli ina kikomo cha cache (5000) — haikui bila mwisho.
- Usafi: NOMINO_ZENYE_NI imeondolewa maingizo yasiyoweza kufikika (benki, taasisi, akaunti).

Toleo 2.5 (Kanuni Kamili 1-16, Yambiwa, na Kanuni Maalum) — historia:
- Imeunganisha sheria zote 16 za lugha kwenye MAELEKEZO_YA_LUGHA
- Imeboresha GenericObjectConcordRule (Kanuni ya Yambiwa) na kurekebisha bug ya stem[0]
- Imeongeza Kanuni L, M, N za mtindo, istilahi za kitiba, na ngeli I-ZI kwenye MkaguziSarufi
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

    # v2.6 (Bug 11): kikomo cha cache ili seva ndefu isikue bila mwisho.
    KIKOMO_CHA_CACHE = 5000

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
                # v2.6 (Bug 10): "" imeondolewa — haikufikiwa kamwe kwa sababu VIAMBISHI_VYA_VIVUMISHI haina "".
                "adj_prefixes": ("ji", "j"),
            },
            "LI-YA_PL": {
                "exceptions": {"macho", "meno", "mawe", "majina", "magari", "mashamba", "matunda", "maua", "maswali", "mambo", "makasha", "madebe", "maji", "maziwa", "majani", "mawazo", "maneno",
                           "matumizi", "mafanikio", "maendeleo", "mazingira", "mapato", "matokeo", "mahitaji",
                           "maelezo", "maamuzi", "makubaliano", "mabadiliko", "maarifa", "mawasiliano",
                           "mahusiano", "malengo", "matatizo", "mafunzo", "madhara", "matukio", "manufaa"},
                "verb_pos": ("ya",),
                "verb_neg": ("haya",),
                "adj_prefixes": ("ma",),
            },
            "I-ZI_SG": {
                "exceptions": {"nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi", "simu", "safari", "kazi", "habari", "fedha", "dawa", "shule", "saa", "barua", "pesa", "bahasha", "redio"},
                "verb_pos": ("i",),
                "verb_neg": ("hai",),
                "adj_prefixes": ("n", "ny", "m"),
            },
            "I-ZI_PL": {
                "exceptions": {"nyumba", "nguo", "meza", "kalamu", "barabara", "ndizi", "simu", "safari", "kazi", "habari", "fedha", "dawa"},
                "verb_pos": ("zi",),
                "verb_neg": ("hazi",),
                "adj_prefixes": ("n", "ny", "m"),
            },
        }

    def tambua(self, neno: str) -> MatokeoYaNgeli:
        key = neno.lower().strip(".,!?;:\"'()[]{}…")
        if not key:
            return MatokeoYaNgeli(None, 0.0, "none")
        if key in self._cache:
            return self._cache[key]
        # v2.6 (Bug 11): safisha cache ikifika kikomo.
        if len(self._cache) >= self.KIKOMO_CHA_CACHE:
            self._cache.clear()
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

MAKOSA_YA_TAHAJIA = {"muhimili": "mhimili"}

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

UMOJA_WA_NOMINO_ZA_WINGI = {
    "watoto": "mtoto", "watu": "mtu", "wanafunzi": "mwanafunzi", "walimu": "mwalimu", "wagonjwa": "mgonjwa",
    "wafanyakazi": "mfanyakazi", "wakulima": "mkulima", "wageni": "mgeni", "wadau": "mdau", "wananchi": "mwananchi",
    "wazazi": "mzazi", "madaktari": "daktari", "wauguzi": "muuguzi", "wateja": "mteja", "viongozi": "kiongozi",
    "vitabu": "kitabu", "vijana": "kijana", "wanawake": "mwanamke", "wanaume": "mwanamume",
}


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

    VIAMBISHI_VYA_VIVUMISHI = {"m", "mw", "wa", "w", "mi", "my", "ki", "ch",
                               "vi", "vy", "ma", "n", "ny", "u", "ji", "j"}
    MANENO_YA_KURUKA = {"ukubwa", "wazee", "mzee"}

    NGELI_YENYE = {
        "darasa": "lenye", "soko": "lenye", "shamba": "lenye", "jiji": "lenye",
        "shule": "yenye", "nyumba": "yenye", "barabara": "yenye",
        "kitabu": "chenye", "kijiji": "chenye", "mji": "wenye", "mkoa": "wenye",
    }
    # v2.6 (usafi): imeondolewa maingizo yasiyoweza kufikika (benki, taasisi, akaunti
    # hazishi "-ni"; "mwanzoni" haiwezi kugawanywa kama "msingi + ni").
    NOMINO_ZENYE_NI = {"jini", "kuni", "kiini", "ini", "nini"}
    MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara"}

    UMBALI_KIVUMISHI = 2
    UMBALI_KITENZI = 1

    WANYAMA_WA_I_ZI = {"ny
