"""
kanuni_ya_sarufi.py — Injini Kuu ya Sheria na Kanuni za Sarufi ya Kiswahili Sanifu (BAKITA).
Inatumiwa na cerebral_cortex.py, mhariri_pro.py na app.py kwa tafsiri za AI Lingual na uhakiki wa maandishi.

Toleo 2.7 (marekebisho ya ukaguzi wa pili):
- Mpya: KanuniZaSarufiKiswahili.kagua_tafsiri() — mhariri_pro.py ilikuwa inaiita lakini haikuwepo
        (ilianguka kimya kimya na kuonyesha "Ukaguzi wa tafsiri umeshindwa").
- Mpya: Kanuni 17-19 kwenye MAELEKEZO_YA_LUGHA (ngeli ya ma-/mi-, tahajia na maneno ambata,
        alama za uandishi na barua rasmi) kutoka KANUNI_KUU_ZA_SARUFI.
- Mpya: Tahajia zaidi (serekali, maswala, kwasababu, kikipuuzia).
- Mpya: Maneno ambata (wanyamapori, nguvukazi, sawasawa, vidogovidogo, ndogondogo, midogomidogo).
- Mpya: Kila + wingi ("Kila mfugaji wanazingatia" -> "anazingatia") na maneno ya "ku-adopt".
- Mpya: Msamiati wa tafsiri (lugha za wenyeji, walaghai, gharama nafuu, kukichukulia kilimo).
- Marekebisho: "akina mama wanasoma" haikamatwi tena kimakosa kama kosa la kiima-kitenzi.
- Marekebisho: 'Watoto wanasoma vizuri' haibadilishwi tena kuwa 'wazuri' (kitenzi kinakata utafutaji wa kivumishi).
- Marekebisho: Yambiwa haivuki mstari mpya (aya mbili tofauti hazichanganywi).

Toleo 2.6: Bug 1-11 (mizizi ya vitenzi, .get() salama, nafasi za makosa, usambamba, cache n.k.)
Toleo 2.5: Kanuni Kamili 1-16, Yambiwa, na Kanuni Maalum.
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
        "(e) 'KILA' AGREEMENT: 'Kila' always takes singular nouns and singular verbs ('kila mwanafunzi ana'); every verb and pronoun in that sentence stays singular. "
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
        "16) DIGITAL & INTERACTIVE EDUCATION TERMINOLOGY: Translate 'digital learning tools' as 'zana za kujifunza kupitia njia za kidijitali' (NEVER 'zana za kujifunza kidijitali'), and translate 'interactive lessons' as 'masomo kupitia njia shirikishi' (NEVER 'masomo ya mwingiliano'). "
        "17) MA- AND MI- NOUN CONCORD: Plural 'ma-' nouns such as 'matumizi', 'mafanikio', 'maoni', 'majukwaa', 'masuala', 'masharti' take 'ya-' concord ('matumizi yamesababisha', 'majukwaa yatakayosaidia'), never 'i-' or 'vi-', even when another noun stands between the subject and its verb ('matumizi mabaya ya mifereji yamesababisha'). Plural 'mi-' nouns such as 'mifano', 'mifumo', 'miradi' take 'i-' ('mifumo inaweza', 'miradi imeanza'). Verbal nouns starting a sentence ('Kupuuza...', 'Kuwekeza...') keep 'ku-' on their dependent verbs ('Kupuuza ... kunaweza'). "
        "18) FIDELITY, SPELLING & COMPOUNDS: Never invent or add words absent from the source, never change an author's already-correct wording, never repeat adjacent words, and never delete a correct preposition (move a misplaced 'kwa' in front of its noun instead). Remove every English fragment such as 'ku-adopt'. Use 'mhimili', 'serikali', 'masuala', 'kwa sababu', and write 'sawasawa', 'wanyamapori', 'nguvukazi', 'vidogovidogo', 'ndogondogo', 'midogomidogo' as single words. Keep the object infix matched to the direct object ('anapojali afya ya wafanyakazi', never 'anapowajali afya'). A verbal-noun subject ('Kuelimisha jamii...') takes the future ('kutasaidia') or habitual ('husaidia'), and a list of parallel actions keeps one structure ('hujenga uaminifu, huhamasisha ubunifu, na huhakikisha ukuaji'). "
        "19) PUNCTUATION & FORMAL LETTERS: Replace a semicolon followed by a capital letter with a full stop. End every article with exactly one full stop (never a comma or double full stop). In formal letters write headings in CAPITAL LETTERS, write dates without a comma ('15 Novemba 2026'), use first-person plural for an office ('Tunatanguliza...') and close with 'Wenu katika ujenzi wa taifa,'."
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
        "sentence with a proper period (.). "
        "6) PRECISE EQUIVALENTS: 'local languages' -> 'lugha za wenyeji' or 'lugha za asili' (NEVER 'lugha za kienyeji'); "
        "'fraudsters' -> 'walaghai' (NOT 'wadanganyifu'); 'affordable' -> 'yenye gharama nafuu' (NEVER 'inayoweza kumudu'); "
        "'treating farming as a business' -> 'kukichukulia kilimo kama biashara' (NEVER 'kutibu kilimo'); "
        "'thrift' -> 'ubana matumizi'; 'not only... but also' -> 'si tu... bali pia'."
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
                "exceptions": {"mtu", "mtoto", "mgeni", "mwalimu", "mzee", "kijana", "rafiki", "baba", "mama", "kaka", "dada", "daktari", "mnyama", "mbwa", "paka", "simba", "ndege", "samaki", "mwanafunzi", "mwanamke", "mwanamume", "mlevi", "mchungaji", "mvuvi", "mwindaji", "mhudumu", "mfanyakazi", "mwekezaji", "mjasiriamali", "mhandisi", "mwandishi", "mwanasheria", "mhasibu"},
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
                           "mahusiano", "malengo", "matatizo", "mafunzo", "madhara", "matukio", "manufaa",
                           "masuala", "masharti", "majukwaa", "maoni"},
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
        # v2.7: [ \t]+ badala ya \s+ — neno la mwisho wa aya moja halioanishwi na la kwanza la aya inayofuata.
        for match in re.finditer(r"\b([a-zA-Z]+)(?=[ \t]+([a-zA-Z]+)\b)", sentensi):
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

MAKOSA_YA_TAHAJIA = {
    "muhimili": "mhimili",
    "serekali": "serikali",
    "maswala": "masuala",
    "kwasababu": "kwa sababu",
    "kikipuuzia": "kikipuuza",
}

# Marudio yanayopaswa kuandikwa kama neno moja (v2.7): "sawa sawa" -> "sawasawa".
MARUDIO_YA_KUUNGANISHA = {"sawa", "vidogo", "ndogo", "midogo"}

# Maneno ambata yaliyoandikwa kwa nafasi (v2.7): (muundo, umbo sahihi)
MANENO_AMBATA = [
    (r"\bwanyama\s+pori\b", "wanyamapori"),
    (r"\bnguvu\s+kazi\b", "nguvukazi"),
]

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
    {"jina": "local languages -> lugha za wenyeji", "chanzo": r"\blocal\s+languages?\b",
     "makosa": [(r"\blugha\s+za\s+kienyeji\b", "lugha za wenyeji")],
     "ujumbe": "'Local languages' hutafsiriwa 'lugha za wenyeji' au 'lugha za asili', si 'lugha za kienyeji'."},
    {"jina": "fraudsters -> walaghai", "chanzo": r"\bfraudsters?\b",
     "makosa": [(r"\bwadanganyifu\b", "walaghai")],
     "ujumbe": "'Fraudsters' hutafsiriwa 'walaghai', si 'wadanganyifu'."},
    {"jina": "affordable -> yenye gharama nafuu", "chanzo": r"\baffordable\b",
     "makosa": [(r"\binayoweza\s+kumudu\b", "yenye gharama nafuu")],
     "ujumbe": "'Affordable' hutafsiriwa 'yenye gharama nafuu'; angalia upatanisho wa ngeli ya nomino husika."},
    {"jina": "treating farming as a business", "chanzo": r"\btreat(?:ing|s|ed)?\s+farming\s+as\s+a\s+business\b",
     "makosa": [(r"\bkutibu\s+kilimo\b", "kukichukulia kilimo")],
     "ujumbe": "'Treating farming as a business' ni 'kukichukulia kilimo kama biashara', si 'kutibu kilimo'."},
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


def _ambata_kwa_herufi(umbo: str):
    """Hubadilisha maneno yenye nafasi kuwa neno moja, ikihifadhi herufi kubwa ya mwanzo."""
    def f(m):
        return umbo[0].upper() + umbo[1:] if m.group(0)[:1].isupper() else umbo
    return f


def _kila_umoja(m: "re.Match") -> str:
    """Kanuni 8(e)/2: 'Kila mfugaji wanazingatia' -> 'Kila mfugaji anazingatia'."""
    kitenzi_cha_wingi = "wa" + m.group(3)
    if kitenzi_cha_wingi.lower() in UMOJA_WA_NOMINO_ZA_WINGI:
        return m.group(0)                      # ni nomino ya wingi, si kitenzi
    return f"{m.group(1)} {m.group(2)} a{m.group(3)}"


class MkaguziSarufi:
    """
    Hukagua sentensi kwa:
      - Upatanisho wa ngeli (nomino ↔ kivumishi kilicho karibu)
      - Nahau/methali zilizokopwa vibaya (kiroboti)
      - Uandishi (herufi kubwa, alama ya kituo)
      - Umoja wa kisintaksia wa sentensi
      - Kanuni maalum za mtindo, istilahi, na upatanisho wa I-ZI
      - Ngeli ya mahali ('darasani yenye') na urudiaji wa maneno ('kubwa kubwa')
      - Maneno ambata, 'Kila' + wingi, na maneno ya Kiingereza yaliyochanganywa (v2.7)
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

    # Wanyama wenye umbo la I-ZI lakini wanaochukua upatanisho wa A-WA (kanuni 7a).
    WANYAMA_WA_I_ZI = {
        "nyoka", "nyani", "nyati", "nyuki", "nyumbu", "ng'ombe", "ndege", "njiwa",
        "nzige", "nzi", "mbuzi", "kondoo", "punda", "farasi", "simba", "chui", "fisi",
        "tembo", "twiga", "paka", "samaki", "kuku", "bata", "swala", "kobe", "chura",
        "mbu", "konokono", "kenge", "papa", "pweza", "nguruwe", "sungura", "panya",
        "bundi", "kanga", "kasuku", "tausi", "kiboko", "nyamera",
    }

    # Maneno yanayoonekana kama kivumishi lakini ni nomino (hayakaguliwi).
    MANENO_YA_KURUKA_ZIADA = {"wema", "ubaya", "uzuri", "ukubwa", "uzee"}

    # Viunganishi vinavyoonyesha kwamba nomino iliyotangulia si kiima cha kitenzi kinachofuata.
    # v2.7: "akina" imeongezwa — "akina mama wanasoma" ni sahihi (wingi wa heshima).
    VIUNGANISHI = {"wa", "ya", "za", "la", "cha", "vya", "pa", "kwa", "na", "kwenye",
                   "katika", "hata", "au", "kama", "kila", "akina"}

    VIWAKILISHI_VYA_YENYE = {"yenye", "lenye", "chenye", "wenye", "zenye", "vyenye", "penye"}

    # Mizizi ya vitenzi vya kawaida (v2.6 Bug 1: "soma"/"taka" kamili, si "som"/"tak").
    _MIZIZI_VITENZI = {
        "soma", "taka", "andika", "fanya", "sema", "leta", "pika", "fika", "enda", "pata",
        "penda", "ona", "sikia", "jenga", "lima", "fundisha", "hudumia", "amua", "anza",
        "maliza", "ruka", "cheza", "lala", "amka", "ingia", "toka", "rudi", "simama",
        "tembea", "angalia", "saidia", "tibu", "ugua", "pona", "nguruma", "imba",
        "kimbia", "jibu", "uliza", "ita", "tumia", "kamata", "badilisha", "elewa",
    }

    # Watu wenye umbo moja kwa umoja na wingi (haziwezi kukaguliwa kwa kiima).
    _WATU_WENYE_UMBO_MOJA = {"askari", "wenzake", "mwenzake", "dereva"}

    def __init__(self):
        self.kitambuzi = KitambuziNgeli()
        self.yambiwa = GenericObjectConcordRule()
        self._viambishi = sorted(self.VIAMBISHI_VYA_VIVUMISHI, key=len, reverse=True)
        mizizi = "|".join(sorted(self._MIZIZI_VITENZI, key=len, reverse=True))
        self._kitenzi_re = re.compile(
            r"^(?P<s>wa|a|zi|i)(?P<t>nge|ngali|na|li|me|ta|ka|ki)(?P<r>" + mizizi + r")$"
        )
        self._kitenzi_kamili_re = re.compile(
            r"^(?:ha)?(?:wa|a|u|i|zi|tu|m|ni|ki|vi|li|ya|hu)(?:nge|ngali|na|li|me|ta|ka|ki|ku)?[a-z]{3,}$"
        )
        self._kitenzi_wazi_re = re.compile(
            r"^(?:ha)?(?:wa|a|u|i|zi|tu|m|ni|ki|vi|li|ya)(?:nge|ngali|na|li|me|ta|ka|ki)[a-z]{2,}$"
        )
        self._kanuni_za_mtindo = self._jenga_kanuni_za_mtindo()

    # ------------------------------------------------------------
    # Zana za ndani
    # ------------------------------------------------------------
    @staticmethod
    def _tokeni(s: str) -> list:
        return [(m.group(0), m.start(), m.end())
                for m in re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)?", s)]

    @staticmethod
    def _hakuna_alama(s: str, tokens: list, a: int, b: int) -> bool:
        """Kweli kama kati ya tokeni a na b hakuna alama ya kituo/koma wala mstari mpya."""
        return not re.search(r"[.!?;:,\n]", s[tokens[a][2]:tokens[b][1]])

    @staticmethod
    def _kosa_la_tokeni(s: str, tokeni: tuple, aina: str, ujumbe: str,
                        mapendekezo: list, chanzo: str) -> Kosa:
        neno, a, b = tokeni
        return Kosa(aina=aina, neno=neno, nafasi=a, urefu=b - a, ujumbe=ujumbe,
                    mapendekezo=mapendekezo, chanzo=chanzo)

    def _ni_mtu_umoja(self, n: str) -> bool:
        return (n in self.yambiwa.watu_umoja or n in self.kitambuzi.ngeli_matrix["A-WA_SG"]["exceptions"]) \
            and n not in self._WATU_WENYE_UMBO_MOJA and n not in self.yambiwa.watu_wingi

    def _ni_mtu_wingi(self, n: str) -> bool:
        return (n in self.yambiwa.watu_wingi or n in self.kitambuzi.ngeli_matrix["A-WA_PL"]["exceptions"]) \
            and n not in self._WATU_WENYE_UMBO_MOJA and n not in self.yambiwa.watu_umoja

    def _ngeli_ya(self, n: str) -> Optional[str]:
        """Ngeli ya nomino kwa uhakika wa juu pekee; None kama haina uhakika au ni mnyama wa I-ZI."""
        if n in self.WANYAMA_WA_I_ZI:
            return None
        if self._ni_mtu_wingi(n):
            return "A-WA_PL"
        if self._ni_mtu_umoja(n):
            return "A-WA_SG"
        t = self.kitambuzi.tambua(n)
        if t.ngeli and t.uhakika >= 0.9:
            return t.ngeli
        return None

    def _gawanya_kivumishi(self, neno: str) -> Optional[tuple]:
        """'mzuri' -> ('m', 'zuri'); None kama si kivumishi chenye kiambishi."""
        n = neno.lower()
        if n in self.MANENO_YA_KURUKA or n in self.MANENO_YA_KURUKA_ZIADA:
            return None
        for p in self._viambishi:
            if p == "u":
                continue                       # 'u-' hutoa nomino (uzuri, ubaya), si kivumishi
            if n.startswith(p):
                mzizi = n[len(p):]
                if mzizi in self.VIVUMISHI_MIZIZI and mzizi not in self.MANENO_YENYE_MAANA_MBILI:
                    return p, mzizi
        return None

    @staticmethod
    def _umbo_la_kivumishi(ngeli: str, mzizi: str) -> Optional[str]:
        """Umbo sahihi la kivumishi kwa ngeli; None kama halina kanuni rahisi (mfano I-ZI)."""
        vokali = mzizi[0] in "aeiou"
        if ngeli in ("A-WA_SG", "U-I_SG"):
            return ("mw" if vokali else "m") + mzizi
        if ngeli == "A-WA_PL":
            return ("w" if vokali else "wa") + mzizi
        if ngeli == "KI-VI_SG":
            return ("ch" if vokali else "ki") + mzizi
        if ngeli == "KI-VI_PL":
            return ("vy" if vokali else "vi") + mzizi
        if ngeli == "U-I_PL":
            return ("my" if vokali else "mi") + mzizi
        if ngeli == "LI-YA_PL":
            if mzizi[0] in "ei":
                return "me" + mzizi[1:]
            return None if vokali else "ma" + mzizi
        return None

    # ------------------------------------------------------------
    # Ukaguzi wa ngeli: nomino <-> kivumishi
    # ------------------------------------------------------------
    def _kagua_ngeli_kivumishi(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        for i, (neno, _a, _b) in enumerate(tokens):
            ngeli = self._ngeli_ya(neno.lower())
            if not ngeli:
                continue
            ruhusa = self.kitambuzi.ngeli_matrix[ngeli]["adj_prefixes"]
            for j in range(i + 1, min(i + 1 + self.UMBALI_KIVUMISHI, len(tokens))):
                if not self._hakuna_alama(s, tokens, j - 1, j):
                    break
                tok = tokens[j]
                g = self._gawanya_kivumishi(tok[0])
                if g is None:
                    # v2.7: kitenzi chenye wakati kinakata utafutaji ('Watoto wanasoma vizuri': 'vizuri' si kivumishi cha 'watoto').
                    if (tok[0].lower() in self.VIUNGANISHI or self._ngeli_ya(tok[0].lower())
                            or self._kitenzi_wazi_re.match(tok[0].lower())):
                        break
                    continue
                kiambishi, mzizi = g
                if kiambishi in ruhusa:
                    break
                sahihi = self._umbo_la_kivumishi(ngeli, mzizi)
                if sahihi and tok[0][0].isupper():
                    sahihi = sahihi[0].upper() + sahihi[1:]
                makosa.append(self._kosa_la_tokeni(
                    s, tok, "NGELI",
                    f"Kivumishi '{tok[0]}' hakipatani na ngeli ya nomino '{neno}' ({ngeli}).",
                    [sahihi] if sahihi else [], "ngeli_matrix"))
                break
        return makosa

    # ------------------------------------------------------------
    # Upatanisho wa kiima na kitenzi (v2.6 Bug 7: herufi kubwa huhifadhiwa)
    # ------------------------------------------------------------
    def _kagua_upatanisho_kiima_kitenzi(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        for i in range(len(tokens) - 1):
            neno = tokens[i][0]
            n = neno.lower()
            if i > 0 and tokens[i - 1][0].lower() in self.VIUNGANISHI:
                continue
            if not self._hakuna_alama(s, tokens, i, i + 1):
                continue
            kitenzi = tokens[i + 1]
            m = self._kitenzi_re.match(kitenzi[0].lower())
            if not m:
                continue
            kiima = m.group("s")
            mpya = None
            if n in self.WANYAMA_WA_I_ZI:
                if kiima == "i":
                    mpya = "a"
                elif kiima == "zi":
                    mpya = "wa"
            elif self._ni_mtu_umoja(n) and kiima == "wa":
                mpya = "a"
            elif self._ni_mtu_wingi(n) and kiima == "a":
                mpya = "wa"
            if mpya is None:
                continue
            pendekezo = mpya + kitenzi[0][len(kiima):]
            if kitenzi[0][0].isupper():
                pendekezo = pendekezo[0].upper() + pendekezo[1:]
            makosa.append(self._kosa_la_tokeni(
                s, kitenzi, "UPATANISHO",
                f"Kitenzi '{kitenzi[0]}' hakipatani na kiima '{neno}'.",
                [pendekezo], "kiima_kitenzi"))
        return makosa

    # ------------------------------------------------------------
    # Ngeli ya mahali (v2.6 Bug 2: .get() salama; hakuna maneno yanayobuniwa)
    # ------------------------------------------------------------
    def _kagua_ngeli_mahali(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        for i in range(len(tokens) - 1):
            n = tokens[i][0].lower()
            if len(n) < 5 or not n.endswith("ni") or n in self.NOMINO_ZENYE_NI:
                continue
            if not self._hakuna_alama(s, tokens, i, i + 1):
                continue
            ifuatayo = tokens[i + 1]
            if ifuatayo[0].lower() not in self.VIWAKILISHI_VYA_YENYE:
                continue
            msingi = n[:-2]
            sahihi = self.NGELI_YENYE.get(msingi)
            if sahihi is None or sahihi == ifuatayo[0].lower():
                continue                 # nomino haijulikani au tayari sahihi: usibuni neno
            if ifuatayo[0][0].isupper():
                sahihi = sahihi[0].upper() + sahihi[1:]
            makosa.append(self._kosa_la_tokeni(
                s, ifuatayo, "NGELI",
                f"Baada ya '{tokens[i][0]}' (nomino ya mahali '{msingi}'), tumia '{sahihi}', si '{ifuatayo[0]}'.",
                [sahihi], "ngeli_mahali"))
        return makosa

    # ------------------------------------------------------------
    # Marudio ya maneno ('kubwa kubwa'); v2.7: 'sawa sawa' -> 'sawasawa'
    # ------------------------------------------------------------
    def _kagua_marudio(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        for i in range(len(tokens) - 1):
            a, b = tokens[i], tokens[i + 1]
            if a[0].lower() != b[0].lower() or len(a[0]) < 3:
                continue
            if s[a[2]:b[1]].strip() != "":          # kati yao kuna alama: si marudio
                continue
            # 'sawa sawa', 'ndogo ndogo' n.k. ni neno moja (kanuni 5); aina TAHAJIA ili ionekane kwenye mhariri_pro.
            if a[0].lower() in MARUDIO_YA_KUUNGANISHA:
                umbo = s[a[1]:a[2]] + s[b[1]:b[2]].lower()
                makosa.append(Kosa(
                    aina="TAHAJIA", neno=s[a[1]:b[2]], nafasi=a[1], urefu=b[2] - a[1],
                    ujumbe=f"Marudio '{a[0].lower()} {b[0].lower()}' huandikwa kama neno moja: '{umbo.lower()}'.",
                    mapendekezo=[umbo], chanzo="maneno_ambata"))
                continue
            if a[0].lower() in self.MARUDIO_HALALI:
                continue
            urefu = b[2] - a[1]
            makosa.append(Kosa(
                aina="TAWALI", neno=s[a[1]:b[2]], nafasi=a[1], urefu=urefu,
                ujumbe=f"Neno '{a[0]}' limerudiwa mfululizo; huenda ni kosa la kuandika.",
                mapendekezo=[a[0]], chanzo="marudio"))
        return makosa

    # ------------------------------------------------------------
    # Usambamba wa vitenzi (v2.6 Bug 4: tokens[j+1:i], si tokens[j+1] pekee)
    # ------------------------------------------------------------
    def _kagua_usambamba_wa_vitenzi(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        si_vitenzi = {"huduma", "hukumu", "huzuni", "hudhurio", "hutuba", "husuda"}
        j = None
        for i, tok in enumerate(tokens):
            n = tok[0].lower()
            if j is not None and re.search(r"[.!?\n]", s[tokens[i - 1][2]:tok[1]]):
                j = None                          # sentensi mpya
            if n.startswith("hu") and len(n) >= 5 and n not in si_vitenzi and n[-1] == "a" \
                    and not n.startswith(("huu", "hii")):
                j = i
                continue
            if j is None or not n.startswith("ku") or len(n) < 6:
                continue
            kati = tokens[j + 1:i]
            if any(self._kitenzi_kamili_re.match(t[0].lower()) and not t[0].lower().startswith("ku")
                   for t in kati if len(t[0]) > 4 and t[0].lower().startswith(("hu", "wa", "a", "tu"))):
                continue
            tangulizi = s[tokens[i - 1][2]:tok[1]]
            if "," not in tangulizi and " na " not in tangulizi:
                continue
            pendekezo = "hu" + tok[0][2:]
            makosa.append(self._kosa_la_tokeni(
                s, tok, "SINTAKSIA",
                f"Usambamba wa vitenzi: '{tok[0]}' linapaswa kufuata wakati wa kawaida ('hu-') kama vitenzi vilivyotangulia.",
                [pendekezo], "usambamba"))
        return makosa

    # ------------------------------------------------------------
    # Tahajia
    # ------------------------------------------------------------
    def _kagua_tahajia(self, s: str, tokens: list) -> List[Kosa]:
        makosa = []
        for tok in tokens:
            sahihi = MAKOSA_YA_TAHAJIA.get(tok[0].lower())
            if sahihi:
                if tok[0][0].isupper():
                    sahihi = sahihi[0].upper() + sahihi[1:]
                makosa.append(self._kosa_la_tokeni(
                    s, tok, "TAHAJIA", f"Tahajia sanifu ni '{sahihi}', si '{tok[0]}'.", [sahihi], "tahajia"))
        return makosa

    # ------------------------------------------------------------
    # Uandishi (v2.6 Bug 3: nafasi/urefu/neno vinalingana)
    # ------------------------------------------------------------
    def _kagua_uandishi(self, s: str) -> List[Kosa]:
        makosa = []
        vifupisho = ("dkt.", "bw.", "bi.", "mf.", "k.m.", "n.k.", "nk.", "km.", "mh.", "prof.")
        for m in re.finditer(r"(?:^|(?<=[.!?])[ \t]+)([a-z][A-Za-z']*)", s, re.M):
            kabla = s[:m.start(1)].rstrip()
            if kabla and (re.search(r"\d\.$", kabla) or kabla.lower().endswith(vifupisho)):
                continue
            neno = m.group(1)
            makosa.append(Kosa(
                aina="TAWALI", neno=neno, nafasi=m.start(1), urefu=len(neno),
                ujumbe="Sentensi inapaswa kuanza kwa herufi kubwa.",
                mapendekezo=[neno[0].upper() + neno[1:]], chanzo="uandishi"))
        mwisho = re.search(r"(\S+)\s*\Z", s)
        if mwisho and len(self._tokeni(s)) >= 3:
            neno = mwisho.group(1)
            if neno[-1] not in ".!?:…\"')”’)]}" and not neno.startswith(("-", "*", "#")):
                makosa.append(Kosa(
                    aina="TAWALI", neno=neno, nafasi=mwisho.start(1), urefu=len(neno),
                    ujumbe="Sentensi ya mwisho haina alama ya kituo.",
                    mapendekezo=[neno + "."], chanzo="uandishi"))
        return makosa

    # ------------------------------------------------------------
    # Kanuni za mtindo na istilahi (L, M, N na nyinginezo)
    # ------------------------------------------------------------
    def _jenga_kanuni_za_mtindo(self) -> list:
        jamaa = r"(?:mama|baba|dada|kaka|bibi|babu|shangazi|mjomba)"

        def _akina_moja(m):
            kichwa = "Akina" if m.group(1)[0].isupper() else "akina"
            return f"{kichwa} {m.group(1).lower()} {m.group(2)}"

        def _kama(m):
            return "Kama" if m.group(1)[0].isupper() else "kama"

        def _ingawa(m):
            return "Ingawa" if m.group(1)[0].isupper() else "ingawa"

        def _isinge_au_zisinge(m):
            r = _isinge_kwa_nomino(m)
            if "hazinge" in m.group(0).lower():
                r = r.replace(" isinge", " zisinge", 1)
            return r

        kanuni = [
            (re.compile(r"\b[Ww]akati\s+([A-Za-z']+)\s+([A-Za-z']*?(?:na|li|me|ta)po[A-Za-z']*)"),
             "Kanuni 11: kishazi cha wakati chenye '-po-' huanza na 'Pale', si 'Wakati'.",
             "kanuni_l", _pale_kwa_herufi),
            (re.compile(r"(?<!akina )\b([Mm]ama|[Bb]aba|[Dd]ada|[Kk]aka|[Bb]ibi|[Bb]abu|[Ss]hangazi|[Mm]jomba)"
                        r"\s+(wengi|wote|wengine|wapendwa|wajawazito|wawili|watatu|wazuri)\b"),
             "Kanuni 9/12: wingi wa jamaa na heshima hutumia 'akina' (mfano 'akina mama wajawazito').",
             "kanuni_m", _akina_moja),
            (re.compile(r"\bakina\s+(" + jamaa + r")\s+na\s+(?!akina\b)(" + jamaa + r")\b"),
             "Kanuni 9: rudia 'akina' kabla ya kila nomino iliyounganishwa kwa 'na'.",
             "kanuni_m", lambda m: f"akina {m.group(1)} na akina {m.group(2)}"),
            (re.compile(r"\b(mamlaka|taasisi|shule|kampuni|biashara|shirika|taarifa|sekta|serikali|huduma|"
                        r"nyumba|kanuni|sera|benki)(?:\s+((?:za|ya)\s+[A-Za-z']+))?\s+ha(?:zi|i)nge([A-Za-z']+)", re.IGNORECASE),
             "Kanuni 15: kanusho la sharti la nomino za I-ZI hutumia 'isinge-/zisinge-', si 'hainge-/hazinge-'.",
             "kanuni_n", _isinge_au_zisinge),
            (re.compile(r"\b([Ii](?:wapo|kiwa))\b(?=[^.!?]{0,120}?\b[a-z]{1,4}(?:singe|singali|ngali|nge)[a-z]{3,}\b)"),
             "Kanuni 10: sharti la kinyume (-nge-/-ngali-) hutumia 'Kama', si 'Iwapo/Ikiwa'.",
             "kanuni_kama", _kama),
            (re.compile(r"\b([Hh]ata)\s+[Ii]ngawa\b"),
             "Kanuni 4: tumia kiunganishi kimoja ('Ingawa'), si 'Hata ingawa'.",
             "kanuni_ingawa", _ingawa),
            (re.compile(r"\bzana\s+za\s+kujifunza\s+kidijitali\b"),
             "Kanuni 16: 'digital learning tools' ni 'zana za kujifunza kupitia njia za kidijitali'.",
             "kanuni_istilahi", lambda m: "zana za kujifunza kupitia njia za kidijitali"),
            (re.compile(r"\bmasomo\s+ya\s+mwingiliano\b"),
             "Kanuni 16: 'interactive lessons' ni 'masomo kupitia njia shirikishi'.",
             "kanuni_istilahi", lambda m: "masomo kupitia njia shirikishi"),
            (re.compile(r"\bmaambukizi\s+changamano\b"),
             "Kanuni 12: 'complex infections' ni 'maambukizi magumu kufahamika'.",
             "kanuni_istilahi", lambda m: "maambukizi magumu kufahamika"),
            (re.compile(r"\b(h[a-z]{1,4})zii\b"),
             "Kanuni 14: hifadhi vokali ya shina kabla ya '-i' ya kanusho ('hakuzuii').",
             "kanuni_zui", lambda m: m.group(1) + "zuii"),
            (re.compile(r"\bwangekuwa\s+wame[a-z]+"),
             "Kanuni 13: epuka 'wangekuwa wame-'; tumia 'wangeweza ku-' au hali ya masharti ya moja kwa moja.",
             "kanuni_wangeweza", None),
            # --- v2.7 ---
            (re.compile(r"\b([Kk]ila)\s+([A-Za-z']+)\s+wa((?:na|li|ta|me|ka|ki)[a-z]{3,})\b"),
             "Kanuni 8(e)/17: 'Kila' + nomino ya umoja huchukua kitenzi cha umoja ('Kila mfugaji anazingatia').",
             "kanuni_kila", _kila_umoja),
            (re.compile(r"\b[Kk]u-[A-Za-z]{3,}\b"),
             "Kanuni 18: neno la Kiingereza limeunganishwa na 'ku-'; liandike kwa Kiswahili sanifu.",
             "kanuni_kiingereza", None),
        ]
        for muundo, umbo in MANENO_AMBATA:
            kanuni.append((
                re.compile(muundo, re.IGNORECASE),
                f"Kanuni 18: '{umbo}' huandikwa kama neno moja.",
                "kanuni_ambata", _ambata_kwa_herufi(umbo)))
        return kanuni

    def _kagua_mtindo(self, s: str) -> List[Kosa]:
        makosa = []
        for muundo, ujumbe, chanzo, kitendo in self._kanuni_za_mtindo:
            for m in muundo.finditer(s):
                neno = m.group(0)
                pendekezo = kitendo(m) if kitendo else None
                if pendekezo is not None and pendekezo == neno:
                    continue
                makosa.append(Kosa(
                    aina="MTINDO", neno=neno, nafasi=m.start(), urefu=len(neno), ujumbe=ujumbe,
                    mapendekezo=[pendekezo] if pendekezo else [], chanzo=chanzo))
        return makosa

    # ------------------------------------------------------------
    # Msamiati wa Kiingereza -> Kiswahili
    # ------------------------------------------------------------
    def kagua_msamiati(self, kiingereza: str, kiswahili: str) -> List[Kosa]:
        makosa = []
        for kanuni in MSAMIATI_WA_KIINGEREZA:
            if not re.search(kanuni["chanzo"], kiingereza or "", re.IGNORECASE):
                continue
            for muundo, badala in kanuni["makosa"]:
                for m in re.finditer(muundo, kiswahili or "", re.IGNORECASE):
                    makosa.append(Kosa(
                        aina="MSAMIATI", neno=m.group(0), nafasi=m.start(), urefu=len(m.group(0)),
                        ujumbe=kanuni["ujumbe"], mapendekezo=[m.expand(badala)],
                        chanzo="msamiati"))
        return makosa

    # ------------------------------------------------------------
    # Mlango mkuu
    # ------------------------------------------------------------
    def kagua(self, sentensi: str, kagua_alama: bool = True) -> List[Kosa]:
        """Hurudisha orodha ya Kosa. kagua_alama=False huruka ukaguzi wa herufi kubwa/alama ya kituo."""
        if not sentensi or not sentensi.strip():
            return []
        tokens = self._tokeni(sentensi)
        ukaguzi = [
            lambda: self.yambiwa.kagua(sentensi),
            lambda: self._kagua_ngeli_kivumishi(sentensi, tokens),
            lambda: self._kagua_upatanisho_kiima_kitenzi(sentensi, tokens),
            lambda: self._kagua_ngeli_mahali(sentensi, tokens),
            lambda: self._kagua_marudio(sentensi, tokens),
            lambda: self._kagua_usambamba_wa_vitenzi(sentensi, tokens),
            lambda: self._kagua_tahajia(sentensi, tokens),
            lambda: self._kagua_mtindo(sentensi),
        ]
        if kagua_alama:
            ukaguzi.append(lambda: self._kagua_uandishi(sentensi))
        makosa: List[Kosa] = []
        for hatua in ukaguzi:
            try:
                makosa.extend(hatua())
            except Exception as e:               # ukaguzi mmoja kushindwa kusiangushe mengine
                logger.warning("Ukaguzi wa sarufi umeshindwa: %s: %s", type(e).__name__, str(e)[:120])
        makosa.sort(key=lambda k: (k.nafasi, -k.urefu))
        return makosa


# ============================================================
# MLANGO MKUU WA APP: KanuniZaSarufiKiswahili
# ============================================================

class KanuniZaSarufiKiswahili:
    """Kiolesura kinachotumiwa na cerebral_cortex.py na mhariri_pro.py."""

    def __init__(self):
        self.mkaguzi = MkaguziSarufi()

    def kagua_sentensi_nzima(self, maandishi: str, kagua_alama: bool = True,
                             chanzo_kiingereza: Optional[str] = None) -> Dict[str, Any]:
        """
        Hurudisha:
          sahihi (bool)                    - kweli kama hakuna kosa lisilo la 'TAWALI'
          makosa (list[dict])              - kila kosa kama Kosa.to_dict()
          maandishi_yaliyorekebishwa (str) - maandishi baada ya kutumia mapendekezo ya kwanza
          mabadiliko (list[dict])          - kabla/baada/aina/sababu
          idadi_ya_makosa (int)            - makosa yasiyo ya 'TAWALI'
        """
        maandishi = maandishi or ""
        makosa = self.mkaguzi.kagua(maandishi, kagua_alama=kagua_alama)
        if chanzo_kiingereza:
            makosa += self.mkaguzi.kagua_msamiati(chanzo_kiingereza, maandishi)
        makosa.sort(key=lambda k: (k.nafasi, -k.urefu))
        yaliyorekebishwa, mabadiliko = _tumia_makosa(maandishi, makosa)
        halisi = [k for k in makosa if k.aina != "TAWALI"]
        return {
            "sahihi": not halisi,
            "makosa": [k.to_dict() for k in makosa],
            "maandishi_yaliyorekebishwa": yaliyorekebishwa,
            "mabadiliko": mabadiliko,
            "idadi_ya_makosa": len(halisi),
        }

    def kagua_tafsiri(self, lugha_chanzo: str, chanzo: str, tafsiri: str) -> List[Dict[str, Any]]:
        """
        v2.7: inatumiwa na mhariri_pro.chambua(). Hukagua msamiati wa tafsiri kwa kulinganisha chanzo na
        matokeo (mfano 'fraudsters' -> 'walaghai'). Hurudisha orodha ya Kosa.to_dict(); tupu kwa jozi
        zisizo Kiingereza -> Kiswahili au kama chanzo hakipo.
        """
        if not (tafsiri and chanzo and lugha_chanzo):
            return []
        if not ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo):
            return []
        return [k.to_dict() for k in self.mkaguzi.kagua_msamiati(chanzo, tafsiri)]

    # Majina mbadala kwa upatanifu
    kagua = kagua_sentensi_nzima


if __name__ == "__main__":
    _k = KanuniZaSarufiKiswahili()
    for _t in ("Watoto anasoma kitabu kizuri. Mtoto wanasoma vizuri.", "Hujenga uaminifu, kuhamasisha ubunifu."):
        print(_k.kagua_sentensi_nzima(_t)["maandishi_yaliyorekebishwa"])
