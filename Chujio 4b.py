"""
chujio_4b.py - Sheria ya 4B: kuondoa Kiingereza kilichochanganywa kwenye Kiswahili.

Matumizi ndani ya api_server.py:
    from chujio_4b import ondoa_kiingereza, ina_kiingereza

Kinaacha bila kuguswa: URL, barua pepe, msimbo (`...`), nukuu ("..."),
na sentensi zinazoonekana kuwa za Kiingereza kikamilifu.
"""
import re

# Vitenzi: kiambishi + '-' + kitenzi cha Kiingereza  ->  kiambishi + shina la Kiswahili
VITENZI_4B = {
    "launch": "anzisha",
    "post": "chapisha",
    "attract": "vutia",
    "manage": "simamia",
}

# Misemo na nomino. Zingatia: "capital" haibadilishwi ikifuatwa na city/letter n.k.
MANENO_4B = {
    "ku-build brand": "kujenga chapa",
    "digital marketing": "masoko ya kidijitali",
    "business plan": "mpango wa biashara",
    "transactions": "miamala",
    "transaction": "muamala",
    "platforms": "majukwaa",
    "platform": "jukwaa",
    "records": "kumbukumbu",
    "capital": "mtaji",
    "online": "mtandaoni",
    "loans": "mikopo",
    "loan": "mkopo",
}

_VIAMBISHI_VYA_KUEPUKA = {"re", "pre", "e", "non", "co", "self", "x"}

_NOMINO_RX = [
    (
        re.compile(
            rf"(?<![\w-]){re.escape(en)}(?![\w-])"
            + (r"(?!\s+(?:city|letter|letters|punishment|gains?))" if en == "capital" else ""),
            re.IGNORECASE,
        ),
        sw,
    )
    for en, sw in sorted(MANENO_4B.items(), key=lambda x: -len(x[0]))
]

_KITENZI_RX = re.compile(
    r"(?<![\w-])(\w{1,8})-(" + "|".join(VITENZI_4B) + r")(?![\w-])", re.IGNORECASE
)

_LINDA_RX = re.compile(r"https?://\S+|\S+@\S+\.\S+|`[^`]*`|\"[^\"]*\"|“[^”]*”")

_KISWAHILI = {
    "na", "ya", "wa", "kwa", "ni", "la", "za", "katika", "kwamba", "kuwa",
    "hii", "huu", "hiki", "cha", "vya", "pia", "bado", "sana", "au", "lakini",
}
_KIINGEREZA = {
    "the", "and", "of", "is", "are", "to", "for", "with", "in", "on",
    "that", "this", "it", "was", "be", "we", "you", "our", "your",
}


def _sentensi_ya_kiswahili(s: str) -> bool:
    maneno = re.findall(r"[a-zA-Z']+", s.lower())
    sw = sum(w in _KISWAHILI for w in maneno)
    en = sum(w in _KIINGEREZA for w in maneno)
    return en < 2 and (sw >= 1 or en == 0)


def _hifadhi_herufi_kubwa(asili: str, mpya: str) -> str:
    return mpya[:1].upper() + mpya[1:] if asili[:1].isupper() else mpya


def _badilisha_sehemu(t: str) -> str:
    for rx, sw in _NOMINO_RX:
        t = rx.sub(lambda m, s=sw: _hifadhi_herufi_kubwa(m.group(0), s), t)

    def _kitenzi(m):
        kiambishi, kitenzi = m.group(1), m.group(2).lower()
        if kiambishi.lower() in _VIAMBISHI_VYA_KUEPUKA:
            return m.group(0)
        return kiambishi + VITENZI_4B[kitenzi]

    return _KITENZI_RX.sub(_kitenzi, t)


def _badilisha_sentensi(sentensi: str) -> str:
    matokeo, mwisho = [], 0
    for m in _LINDA_RX.finditer(sentensi):
        matokeo.append(_badilisha_sehemu(sentensi[mwisho:m.start()]))
        matokeo.append(m.group(0))
        mwisho = m.end()
    matokeo.append(_badilisha_sehemu(sentensi[mwisho:]))
    return "".join(matokeo)


def ondoa_kiingereza(maandishi: str) -> str:
    if not maandishi:
        return maandishi
    vipande = re.split(r"(?<=[.!?])(\s+)", maandishi)
    for i in range(0, len(vipande), 2):
        if _sentensi_ya_kiswahili(vipande[i]):
            vipande[i] = _badilisha_sentensi(vipande[i])
    return "".join(vipande)


def ina_kiingereza(maandishi: str) -> bool:
    """Kweli kama maandishi yana neno/muundo wa Kiingereza ambao kichujio kinaujua."""
    if _KITENZI_RX.search(maandishi):
        return True
    return any(rx.search(maandishi) for rx, _ in _NOMINO_RX)
