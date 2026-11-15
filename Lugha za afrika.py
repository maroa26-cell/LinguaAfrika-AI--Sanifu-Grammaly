"""
lugha_za_afrika.py - Orodha ya lugha za AI Lingual Africa.

Kila lugha ina: jina la Kiingereza (kwa maelekezo ya AI), msimbo, mwelekeo wa uandishi,
mwongozo wa tahajia/sarufi, na makadirio ya jinsi AI inavyoimudu.

'ubora_wa_ai' ni MAKADIRIO ya jumla ya upatikanaji wa data za lugha kwa modeli za AI
(juu / wastani / chini). Si kipimo kilichofanyiwa majaribio; litumie kama onyo tu.
Lugha yoyote isiyo kwenye orodha inaweza kuongezwa kwa jina kupitia pata_lugha("Jina").
"""

from __future__ import annotations

KISWAHILI = "Kiswahili"

LUGHA: dict[str, dict] = {
    "Kiswahili": {
        "kiingereza": "Swahili", "msimbo": "sw", "mwelekeo": "ltr", "ubora_wa_ai": "juu",
        "mwongozo": "Use Standard Swahili (Kiswahili Sanifu, BAKITA norms) with correct noun-class concord.",
    },
    "Kiingereza": {
        "kiingereza": "English", "msimbo": "en", "mwelekeo": "ltr", "ubora_wa_ai": "juu",
        "mwongozo": "Use clear, standard English with consistent British spelling.",
    },
    "Kifaransa": {
        "kiingereza": "French", "msimbo": "fr", "mwelekeo": "ltr", "ubora_wa_ai": "juu",
        "mwongozo": "Use standard French with correct accents and agreement, as written in francophone Africa.",
    },
    "Kireno": {
        "kiingereza": "Portuguese", "msimbo": "pt", "mwelekeo": "ltr", "ubora_wa_ai": "juu",
        "mwongozo": "Use standard Portuguese as written in Mozambique and Angola (European norms).",
    },
    "Kiarabu": {
        "kiingereza": "Arabic", "msimbo": "ar", "mwelekeo": "rtl", "ubora_wa_ai": "juu",
        "mwongozo": "Use Modern Standard Arabic with correct punctuation; the text is right-to-left.",
    },
    "Kichina": {
        "kiingereza": "Chinese", "msimbo": "zh", "mwelekeo": "ltr", "ubora_wa_ai": "juu",
        "mwongozo": "Write in Simplified Chinese characters (Mandarin).",
    },
    "Kiafrikana": {
        "kiingereza": "Afrikaans", "msimbo": "af", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Use standard Afrikaans orthography.",
    },
    "Kihausa": {
        "kiingereza": "Hausa", "msimbo": "ha", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Use standard Hausa (Boko) orthography, including the hooked letters ɓ, ɗ and ƙ.",
    },
    "Kiyoruba": {
        "kiingereza": "Yoruba", "msimbo": "yo", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Use standard Yoruba orthography with tone marks and subdotted letters (ẹ, ọ, ṣ).",
    },
    "Kiigbo": {
        "kiingereza": "Igbo", "msimbo": "ig", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Use standard Igbo orthography with dot-below letters (ị, ọ, ụ) and ṅ.",
    },
    "Kizulu": {
        "kiingereza": "isiZulu", "msimbo": "zu", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Write in standard isiZulu (South Africa) with correct noun-class concord.",
    },
    "Kixhosa": {
        "kiingereza": "isiXhosa", "msimbo": "xh", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard isiXhosa with correct noun-class concord.",
    },
    "Kishona": {
        "kiingereza": "Shona (chiShona)", "msimbo": "sn", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard chiShona orthography with correct noun-class concord.",
    },
    "Kisetswana": {
        "kiingereza": "Setswana", "msimbo": "tn", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Setswana as used in Botswana (Tswana orthography).",
    },
    "Kisesotho": {
        "kiingereza": "Sesotho", "msimbo": "st", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Sesotho (Lesotho orthography) with correct noun-class concord.",
    },
    "Kinyarwanda": {
        "kiingereza": "Kinyarwanda", "msimbo": "rw", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Kinyarwanda orthography with correct noun-class concord.",
    },
    "Kirundi": {
        "kiingereza": "Kirundi", "msimbo": "rn", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Kirundi orthography with correct noun-class concord.",
    },
    "Kiganda": {
        "kiingereza": "Luganda", "msimbo": "lg", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Luganda orthography with correct noun-class concord.",
    },
    "Kilingala": {
        "kiingereza": "Lingala", "msimbo": "ln", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Lingala orthography.",
    },
    "Kichichewa": {
        "kiingereza": "Chichewa (Chewa)", "msimbo": "ny", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in standard Chichewa as used in Malawi.",
    },
    "Kisomali": {
        "kiingereza": "Somali", "msimbo": "so", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Use standard Somali Latin orthography.",
    },
    "Kioromo": {
        "kiingereza": "Afaan Oromoo (Oromo)", "msimbo": "om", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Use standard Afaan Oromoo (Qubee) orthography.",
    },
    "Kiamhari": {
        "kiingereza": "Amharic", "msimbo": "am", "mwelekeo": "ltr", "ubora_wa_ai": "wastani",
        "mwongozo": "Write in Ge'ez (Fidel) script using standard Amharic spelling.",
    },
    "Kitigrinya": {
        "kiingereza": "Tigrinya", "msimbo": "ti", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Write in Ge'ez script using standard Tigrinya spelling.",
    },
    "Kimalagasi": {
        "kiingereza": "Malagasy", "msimbo": "mg", "mwelekeo": "ltr", "ubora_wa_ai": "chini",
        "mwongozo": "Use standard Malagasy orthography.",
    },
}

ONYO_LA_UBORA = (
    "Lugha hii ina data chache za mafunzo kwenye modeli za AI, kwa hiyo makosa ni mengi zaidi. "
    "Hakiki matokeo na mzungumzaji wa lugha hiyo kabla ya kuyatumia."
)


def orodha_ya_lugha() -> list[str]:
    """Majina ya lugha kwa ajili ya kisanduku cha kuchagua (Kiswahili kwanza)."""
    return list(LUGHA.keys())


def ni_kiswahili(jina: str) -> bool:
    return (jina or "").strip().lower() == KISWAHILI.lower()


def pata_lugha(jina: str) -> dict:
    """
    Hurudisha taarifa za lugha. Lugha isiyo kwenye orodha (mfano 'Kiswati', 'Wolof')
    inakubaliwa kama lugha maalum, na ubora wake hukadiriwa 'chini'.
    """
    jina = (jina or KISWAHILI).strip()
    for kitufe, v in LUGHA.items():
        if kitufe.lower() == jina.lower() or v["kiingereza"].lower() == jina.lower():
            return {"jina": kitufe, **v, "maalum": False}
    return {
        "jina": jina, "kiingereza": jina, "msimbo": "", "mwelekeo": "ltr",
        "ubora_wa_ai": "chini", "maalum": True,
        "mwongozo": f"Use the standard written form and orthography of {jina}.",
    }


def onyo_la_lugha(jina: str) -> str | None:
    return ONYO_LA_UBORA if pata_lugha(jina)["ubora_wa_ai"] == "chini" else None
