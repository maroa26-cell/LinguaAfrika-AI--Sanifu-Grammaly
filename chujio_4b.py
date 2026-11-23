"""
chujio_4b.py - Sheria ya 4B: kuondoa Kiingereza kilichochanganywa kwenye Kiswahili.

Matumizi ndani ya api_server.py (Render) na kwenye Streamlit:
    from chujio_4b import ondoa_kiingereza, ina_kiingereza

Kinaacha bila kuguswa: URL, barua pepe, msimbo (`...`), nukuu ("..."),
maneno yaliyo ndani ya mabano ( ... ) na [ ... ], majina ya chapa (mf. "Capital One"),
na sentensi zinazoonekana kuwa za Kiingereza kikamilifu.

MABADILIKO v2 (majina ya vitendakazi na ishara zake hazijabadilika):
  1. Maneno ndani ya mabano yanalindwa: "(records)" hubaki "(records)". Hii inalinda istilahi asili
     inayowekwa makusudi baada ya tafsiri (Kitiba, Kisheria).
  2. Maumbo bila kistari yanashikwa: "kulaunch", "kupost", "alipost", "nimemanage", "ukiattract".
  3. Majina ya chapa hayabadilishwi: herufi kubwa katikati ya sentensi ("Tunatumia Platform ya X"),
     neno lenye herufi kubwa likifuatiwa na neno lingine lenye herufi kubwa ("Capital One"), na
     maneno ya HERUFI KUBWA ZOTE. Neno la mwanzo wa sentensi ("Online ni muhimu") bado linabadilishwa.
  4. Sentensi ya Kiingereza isiyo na maneno ya kawaida ("Platform records online.") haichukuliwi tena
     kuwa Kiswahili: sentensi isiyo na neno la kawaida la Kiswahili inahitaji maneno mengi yanayoishia
     kwa irabu ndipo ichukuliwe kuwa ya Kiswahili.
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

# Maumbo bila kistari: kiambishi halali cha kitenzi cha Kiswahili + kitenzi cha Kiingereza.
# kiambishi = ku / hu / (kiwakilishi cha nafsi + wakati), mf. ku-, ali-, nime-, uki-, tuta-.
_VIWAKILISHI_VYA_NAFSI = "ni|u|a|tu|m|wa"
_NYAKATI = "na|me|li|ta|ki|ka"
_VIAMBISHI_VYA_KITENZI = rf"ku|hu|(?:{_VIWAKILISHI_VYA_NAFSI})(?:{_NYAKATI})"
_KITENZI_BILA_KISTARI_RX = re.compile(
    rf"(?<![\w-])({_VIAMBISHI_VYA_KITENZI})(" + "|".join(VITENZI_4B) + r")(?![\w-])",
    re.IGNORECASE,
)

# Sehemu zinazolindwa dhidi ya mabadiliko: URL, barua pepe, msimbo, nukuu, na maandishi ya mabano.
_LINDA_RX = re.compile(
    r"https?://\S+|\S+@\S+\.\S+|`[^`]*`|\"[^\"]*\"|“[^”]*”"
    r"|\([^()\n]*\)|\[[^\[\]\n]*\]"
)

_KISWAHILI = {
    "na", "ya", "wa", "kwa", "ni", "la", "za", "katika", "kwamba", "kuwa",
    "hii", "huu", "hiki", "cha", "vya", "pia", "bado", "sana", "au", "lakini",
}
_KIINGEREZA = {
    "the", "and", "of", "is", "are", "to", "for", "with", "in", "on",
    "that", "this", "it", "was", "be", "we", "you", "our", "your",
}

_ALAMA_ZA_MWANZO_WA_SENTENSI = ".!?:;-–—•*#>"


def _sentensi_ya_kiswahili(s: str) -> bool:
    maneno = re.findall(r"[a-zA-Z']+", s.lower())
    sw = sum(w in _KISWAHILI for w in maneno)
    en = sum(w in _KIINGEREZA for w in maneno)
    if en >= 2:
        return False
    if sw >= 1:
        return True
    if en == 1:
        return False
    # Hakuna neno la kawaida la lugha yoyote: Kiswahili huishia kwa irabu karibu kila neno,
    # Kiingereza mara nyingi huishia kwa konsonanti ("platform", "records").
    if not maneno:
        return True
    irabu = sum(w[-1] in "aeiou" for w in maneno)
    return irabu / len(maneno) >= 0.75


def _hifadhi_herufi_kubwa(asili: str, mpya: str) -> str:
    return mpya[:1].upper() + mpya[1:] if asili[:1].isupper() else mpya


def _ni_jina_la_chapa(t: str, m: "re.Match") -> bool:
    """Kweli kama neno lililopatikana linaonekana kuwa jina la kampuni/chapa, si neno la kawaida la Kiingereza."""
    neno = m.group(0)
    if not neno[:1].isupper():
        return False                                    # neno dogo: si jina
    if len(neno) > 1 and neno.isupper():
        return True                                     # HERUFI KUBWA ZOTE: kifupi au chapa
    if re.match(r"\s+[A-Z]\w", t[m.end():]):
        return True                                     # "Capital One": likifuatwa na neno lenye herufi kubwa
    kabla = t[:m.start()].rstrip()
    mwanzo_wa_sentensi = (not kabla) or (kabla[-1] in _ALAMA_ZA_MWANZO_WA_SENTENSI)
    return not mwanzo_wa_sentensi                       # herufi kubwa katikati ya sentensi: jina


def _badilisha_sehemu(t: str) -> str:
    for rx, sw in _NOMINO_RX:
        def _badili(m, s=sw, tt=t):
            if _ni_jina_la_chapa(tt, m):
                return m.group(0)
            return _hifadhi_herufi_kubwa(m.group(0), s)
        t = rx.sub(_badili, t)

    def _kitenzi(m):
        kiambishi, kitenzi = m.group(1), m.group(2).lower()
        if kiambishi.lower() in _VIAMBISHI_VYA_KUEPUKA:
            return m.group(0)
        return kiambishi + VITENZI_4B[kitenzi]

    t = _KITENZI_RX.sub(_kitenzi, t)

    def _kitenzi_bila_kistari(m):
        return m.group(1) + VITENZI_4B[m.group(2).lower()]

    return _KITENZI_BILA_KISTARI_RX.sub(_kitenzi_bila_kistari, t)


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


def _sehemu_zisizolindwa(maandishi: str) -> list:
    """Vipande vya maandishi nje ya URL, nukuu, msimbo na mabano."""
    vipande, mwisho = [], 0
    for m in _LINDA_RX.finditer(maandishi):
        vipande.append(maandishi[mwisho:m.start()])
        mwisho = m.end()
    vipande.append(maandishi[mwisho:])
    return vipande


def ina_kiingereza(maandishi: str) -> bool:
    """Kweli kama maandishi yana neno/muundo wa Kiingereza ambao kichujio kinaujua
    (nje ya nukuu, mabano na majina ya chapa)."""
    for sehemu in _sehemu_zisizolindwa(maandishi or ""):
        if _KITENZI_RX.search(sehemu) or _KITENZI_BILA_KISTARI_RX.search(sehemu):
            return True
        for rx, _ in _NOMINO_RX:
            for m in rx.finditer(sehemu):
                if not _ni_jina_la_chapa(sehemu, m):
                    return True
    return False
