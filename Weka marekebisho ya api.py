"""weka_marekebisho_ya_api.py - Marekebisho ya api_server.py (AI Lingual Africa Sanifu API v3.2).

  A1  Mapendekezo yaliyochanganywa: "Serekali imesema kwasababu" lilikuwa pendekezo MOJA lenye marekebisho matatu
      (tahajia, kitenzi, 'kwa sababu') na maelezo ya jumla. Sasa kila neno lililobadilika ni pendekezo lake
      (Kubali/Puuza kwa kila moja). Mgawanyo ukishindwa kuwa wa uhakika, linabaki kama lilivyokuwa.
  A2  Aina mpya "wakati": 'imesema' -> 'alisema' haiitwi tena "ngeli"; maelezo yanaonya kwamba wakati umebadilika.
  A3  Kinga ya taasisi: serikali/kampuni/shule/benki/taasisi/mamlaka/wizara... ni I-ZI. AI ikibadilisha
      'Serikali imesema' kuwa 'Serikali alisema', umbo sahihi la asili hurudishwa (au a-/wa- huwa i-/zi-).
  A4  Maelekezo ya AI (SYSTEM_PROMPT na SYSTEM_UKAGUZI): usibadilishe wakati/ngeli ya neno lililo sahihi;
      taasisi ni I-ZI.
  A5  Uchunguzi: AI zikishindwa, jibu la 502 sasa lina "sababu" (aina ya hitilafu na msimbo, bila ujumbe kamili,
      ili funguo zisivuje). Hii inaonyesha kwa nini Gemini haikupatikana.

Matumizi:  python weka_marekebisho_ya_api.py                 (api_server.py kwenye folda ya sasa)
           python weka_marekebisho_ya_api.py njia\\ya\\api_server.py
Hakiki kila sehemu kwanza; kukiwa na tatizo hakuna kinachobadilishwa. Akiba: api_server.py.bak.
Inaweza kuendeshwa tena bila madhara.
"""
import pathlib
import shutil
import sys

MSAIDIZI_WA_MGAWANYO = '''_KITENZI_RX = re.compile(r"^(wa|a|zi|i|u|ya|li|ki|vi|tu|m|ni)(me|li|na|ta)([a-z]{3,})$")


def _sawa(a: str, b: str, kizingiti: float) -> bool:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= kizingiti


def _gawanya_opcodes(ta: list, tb: list, opcodes: list) -> list:
    """Gawa kizuizi cha 'replace' chenye maneno mengi kuwa jozi za neno-kwa-neno (mf. 'kwasababu' -> 'kwa sababu').
    Kikishindwa kugawanywa kwa uhakika (kila neno kupata mwenzake), kinabaki kama kilivyokuwa."""
    out = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag != "replace" or (i2 - i1 <= 1 and j2 - j1 <= 1):
            out.append((tag, i1, i2, j1, j2))
            continue
        i, j, sehemu = i1, j1, []
        while i < i2 and j < j2:
            a, b = ta[i]["t"], tb[j]["t"]
            if j + 1 < j2 and _sawa(a, b + tb[j + 1]["t"], 0.9):        # neno moja -> mawili
                sehemu.append(("replace", i, i + 1, j, j + 2))
                i, j = i + 1, j + 2
            elif i + 1 < i2 and _sawa(a + ta[i + 1]["t"], b, 0.9):      # mawili -> neno moja
                sehemu.append(("replace", i, i + 2, j, j + 1))
                i, j = i + 2, j + 1
            elif a[:1].isalnum() == b[:1].isalnum() and _sawa(a, b, 0.5):  # neno kwa neno
                sehemu.append(("replace", i, i + 1, j, j + 1))
                i, j = i + 1, j + 1
            else:
                break
        if sehemu and i == i2 and j == j2:
            out.extend(sehemu)
        else:
            out.append((tag, i1, i2, j1, j2))
    return out


def _tengeneza_mapendekezo(asili: str, mpya: str, mwanzo_wa_asili: int = 0) -> list:
'''

KINGA_YA_TAASISI = '''# Taasisi si viumbe hai: huchukua upatanisho wa I-ZI (i-/zi-), si a-/wa-. "serekali" imejumuishwa kwa sababu
# maandishi ya asili yanaweza kuwa na tahajia mbaya.
_TAASISI = ("serikali|serekali|kampuni|shule|benki|taasisi|mamlaka|wizara|idara|halmashauri|tume|bodi|hospitali")
_TAASISI_KITENZI_RX = re.compile(
    r"\\b(" + _TAASISI + r")(\\s+)(a|wa)(me|li|na|ta|ka)([a-z]{3,})\\b", re.IGNORECASE)
_TAASISI_SAHIHI_RX = re.compile(
    r"\\b(" + _TAASISI + r")\\s+((?:i|zi)(?:me|li|na|ta|ka)([a-z]{3,}))\\b", re.IGNORECASE)


def _msingi_wa_taasisi(nomino: str) -> str:
    n = nomino.lower()
    return "serikali" if n == "serekali" else n


def _linda_kiima_cha_taasisi(asili: str, matokeo: str) -> str:
    """AI ikibadilisha 'Serikali imesema' kuwa 'Serikali alisema', rudisha umbo sahihi la asili.
    Kama asili haikuwa na umbo sahihi, geuza a-/wa- kuwa i-/zi- (wakati ubaki kama ulivyo kwenye matokeo)."""
    sahihi = {}
    for m in _TAASISI_SAHIHI_RX.finditer(asili):
        sahihi[(_msingi_wa_taasisi(m.group(1)), m.group(3).lower())] = m.group(2)

    def badilisha(m):
        nomino, nafasi, kiambishi, wakati, shina = m.groups()
        ufunguo = (_msingi_wa_taasisi(nomino), shina.lower())
        if ufunguo in sahihi:
            return nomino + nafasi + sahihi[ufunguo]
        return nomino + nafasi + ("i" if kiambishi.lower() == "a" else "zi") + wakati + shina

    return _TAASISI_KITENZI_RX.sub(badilisha, matokeo)


def chakata_kipande(kipande: str, kitendo: str) -> dict:
'''

MABADILIKO = [
    ("A1a msaidizi wa kugawanya mapendekezo",
     'def _tengeneza_mapendekezo(asili: str, mpya: str, mwanzo_wa_asili: int = 0) -> list:\n',
     MSAIDIZI_WA_MGAWANYO),
    ("A1b tumia mgawanyo",
     '    for tag, i1, i2, j1, j2 in sm.get_opcodes():\n        if tag == "equal":\n            continue\n',
     '    for tag, i1, i2, j1, j2 in _gawanya_opcodes(ta, tb, sm.get_opcodes()):\n        if tag == "equal":\n            continue\n'),
    ("A2 aina 'wakati'",
     '    if len(wa) == len(wb):\n        tofauti = [(x, y) for x, y in zip(wa, wb) if x != y]\n',
     '    if len(wa) == len(wb) == 1:\n'
     '        ma, mb = _KITENZI_RX.match(wa[0].lower()), _KITENZI_RX.match(wb[0].lower())\n'
     '        if ma and mb and ma.group(3) == mb.group(3) and ma.group(2) != mb.group(2):\n'
     '            return "wakati", (f"Wakati wa kitenzi umebadilishwa (\'-{ma.group(2)}-\' -> \'-{mb.group(2)}-\'): "\n'
     '                              "hakikisha kweli unataka maana hii.")\n'
     '    if len(wa) == len(wb):\n        tofauti = [(x, y) for x, y in zip(wa, wb) if x != y]\n'),
    ("A3a kinga ya taasisi (kazi)",
     'def chakata_kipande(kipande: str, kitendo: str) -> dict:\n',
     KINGA_YA_TAASISI),
    ("A3b kinga ya taasisi (matumizi)",
     '    return {"text": matokeo, "ok": True, "injini": injini, "hatua2": ilitumia_hatua2}',
     '    matokeo = _linda_kiima_cha_taasisi(kipande, matokeo)\n'
     '    return {"text": matokeo, "ok": True, "injini": injini, "hatua2": ilitumia_hatua2}'),
    ("A4a maelekezo ya AI (hatua ya 1)",
     '7. MATOKEO: Toa matokeo yaliyohaririwa/kutafsiriwa PEKEE',
     '7. USIGUSE KILICHO SAHIHI: Usibadilishe wakati (-me-, -li-, -na-, -ta-), kiambishi cha kiima wala ngeli ya neno '
     'lililo sahihi tayari. Rekebisha kosa halisi tu (mfano \'Serekali imesema kwasababu\' -> \'Serikali imesema kwa sababu\', '
     'si \'Serikali alisema\').\n'
     '8. TAASISI NI NGELI YA I-ZI: serikali, kampuni, shule, benki, taasisi, mamlaka, wizara, idara na halmashauri '
     'huchukua i-/zi-, si a-/wa- (\'Serikali imesema\', \'Kampuni zimetangaza\').\n'
     '9. MATOKEO: Toa matokeo yaliyohaririwa/kutafsiriwa PEKEE'),
    ("A4b maelekezo ya AI (ukaguzi)",
     "- Kitenzi huoana na nomino inayotenda, si nomino iliyo karibu:",
     "- Taasisi (serikali, kampuni, shule, benki, taasisi, mamlaka, wizara) ni ngeli ya I-ZI: 'Serikali imesema' ni SAHIHI; "
     "usiibadilishe kuwa 'Serikali alisema'.\n"
     "- Usibadilishe wakati (-me-, -li-, -na-, -ta-) wa kitenzi kilicho sahihi tayari.\n"
     "- Kitenzi huoana na nomino inayotenda, si nomino iliyo karibu:"),
    ("A5a orodha ya makosa ya mwisho",
     'def _ni_kosa_la_muda(e: Exception) -> bool:\n',
     '_MAKOSA_YA_MWISHO = []   # aina ya hitilafu na msimbo tu (si ujumbe kamili: unaweza kuwa na funguo)\n\n\n'
     'def _rekodi_kosa(injini: str, e: Exception) -> None:\n'
     '    _MAKOSA_YA_MWISHO.append(f"{injini}:{type(e).__name__}:{getattr(e, \'code\', \'\') or getattr(e, \'status_code\', \'\')}")\n'
     '    del _MAKOSA_YA_MWISHO[:-8]\n\n\n'
     'def _ni_kosa_la_muda(e: Exception) -> bool:\n'),
    ("A5b rekodi hitilafu ya Gemini",
     '                print(f"Hitilafu ya Gemini ({modeli_jina}, jaribio {jaribio + 1}): {e}")\n',
     '                print(f"Hitilafu ya Gemini ({modeli_jina}, jaribio {jaribio + 1}): {e}")\n'
     '                _rekodi_kosa(f"gemini[{modeli_jina}]", e)\n'),
    ("A5c rekodi hitilafu ya Groq",
     '        print(f"Hitilafu ya Groq: {e}")\n',
     '        print(f"Hitilafu ya Groq: {e}")\n        _rekodi_kosa("groq", e)\n'),
    ("A5d onyesha sababu kwenye 502",
     '        "imechakatwa": False,\n    }), 502',
     '        "imechakatwa": False,\n        "sababu": list(_MAKOSA_YA_MWISHO[-4:]),\n    }), 502'),
]


def _tayari(t, old, new):
    if old in new:
        return new in t
    return new in t and old not in t


def main():
    njia = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "api_server.py")
    if not njia.is_file():
        sys.exit(f"Sioni {njia}. Liweke hati hii kwenye folda ya api_server.py, au toa njia kamili.")
    t = njia.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"

    kazi = []
    for jina, old, new in MABADILIKO:
        old_n, new_n = old.replace("\n", nl), new.replace("\n", nl)
        if _tayari(t, old_n, new_n):
            print(f"- {jina}: tayari ipo, nimeruka.")
            continue
        idadi = t.count(old_n)
        if idadi != 1:
            sys.exit(f"Sijapata mahali pa kipekee ({jina}; nimeona mara {idadi}). "
                     "Faili huenda ni toleo tofauti; hakuna kilichobadilishwa.")
        kazi.append((jina, old_n, new_n))
    if not kazi:
        sys.exit("Marekebisho yote tayari yapo. Hakuna kilichobadilishwa.")

    mpya = t
    for jina, old_n, new_n in kazi:
        mpya = mpya.replace(old_n, new_n, 1)
    try:
        compile(mpya, str(njia), "exec")
    except SyntaxError as kosa:
        sys.exit(f"Mabadiliko yangevunja msimbo ({kosa}). Hakuna kilichobadilishwa.")

    shutil.copy(njia, str(njia) + ".bak")
    njia.write_bytes(mpya.encode("utf-8"))
    for jina, _o, _n in kazi:
        print(f"- {jina}: imewekwa.")
    print(f"Imekamilika: {njia}. Akiba: {njia}.bak")


if __name__ == "__main__":
    main()
