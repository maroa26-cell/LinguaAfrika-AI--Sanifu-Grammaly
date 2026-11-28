"""
imla_sw.py: marekebisho ya imla ya Kiswahili (hayategemei AI, yanafanya kazi kila mara).

Yanatumika na cerebral_cortex.py baada ya injini yoyote (Gemini, Groq Whisper, OpenAI) kunukuu.
Ongeza makosa mapya kwenye MAREKEBISHO kadri unavyoyaona yakijirudia.
"""
import re

# Elekezo fupi la Whisper (alama za uandishi humsaidia kuweka nukta na herufi kubwa).
ELEKEZO_SW = (
    "Hii ni imla ya Kiswahili sanifu. Habari, asante sana. "
    "Nitahakikisha kwamba mfumo unafanya kazi vizuri."
)

# (muundo, mbadala). Mbadala unaweza kutumia \1 kwa vikundi. Ndefu kwanza.
MAREKEBISHO = [
    (r"\bkwa\s+ajil[ai]\s+kwa\s+kisha\s+kwamba\b", "kwa ajili ya kuhakikisha kwamba"),
    (r"\bkwa\s+kisha\s+kwamba\b", "kuhakikisha kwamba"),
    (r"\bniku\s+wapa\b", "nakupa"),
    (r"\bniku\s+hapa\b", "nipo hapa"),
    (r"\bkuakita\b", "kuhakikisha"),
    (r"\bkuakikisha\b", "kuhakikisha"),
    (r"\bnitangalia\b", "nitaangalia"),
    (r"\bkwangalea\b", "kuangalia"),
    (r"\b(ni|u|a|tu|m|wa)naitaji\b", r"\1nahitaji"),
    (r"\bsante\b", "asante"),
    (r"\bmaeno\b", "maneno"),
    (r"\bmfumu\b", "mfumo"),
    (r"\bbizuri\b", "vizuri"),
    (r"\botuba\b", "hotuba"),
    (r"\bjie\b", "wewe"),
    (r"\bajila\b", "ajili"),
    (r"\bnbari\b", "habari"),
    (r"\babari\b", "habari"),
    (r"\biyo\b", "hiyo"),
    (r"\bilo\b", "hilo"),
    (r"\bndo\b", "ndio"),
    (r"\bwezo\b", "uwezo"),
]
_MIFUMO = [(re.compile(m, re.IGNORECASE), b) for m, b in MAREKEBISHO]


def _badilisha(m, mbadala):
    jibu = m.expand(mbadala)
    return jibu[:1].upper() + jibu[1:] if m.group(0)[:1].isupper() else jibu


def sahihisha_imla(maandishi, lugha="sw"):
    """Hurekebisha makosa yanayojirudia. Lugha isiyo Kiswahili haiguswi."""
    if not maandishi or lugha != "sw":
        return maandishi
    for muundo, mbadala in _MIFUMO:
        maandishi = muundo.sub(lambda m, b=mbadala: _badilisha(m, b), maandishi)
    return maandishi
