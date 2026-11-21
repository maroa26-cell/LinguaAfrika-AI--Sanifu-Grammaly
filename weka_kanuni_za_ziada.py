"""weka_kanuni_za_ziada.py - Inaongeza kanuni za ziada kwenye kanuni_ya_sarufi.py (toleo 2.9).

Kanuni zinazowekwa:
  Z1  'Je,' (swali): sentensi inayoanza na 'Je,' ikiisha kwa nukta, pendekeza '?'.
      (hailindi tu nukuu; inaruka vifupisho 'Dkt.', 'k.m.', '3.5', na '...')
  Z2  Nomino ambatani: 'mwana nchi/inchi' -> 'mwananchi', 'wana inchi' -> 'wananchi',
      'mwana ume' -> 'mwanamume', 'mwana mke' -> 'mwanamke' (herufi kubwa inahifadhiwa; nukuu zinalindwa).
  Z3  Marekebisho ya '-ingi': 'mifumo myingi' -> 'mifumo mingi', 'wageni wingi' -> 'wageni wengi',
      'vitabu vyingi' -> 'vitabu vingi', 'kitu chingi' -> 'kitu kingi'.
      Pia inarekebisha kosa lililokuwepo: _umbo_la_kivumishi() ilitoa 'wingi/vyingi/myingi/chingi' (si sahihi)
      na ilipendekeza 'mifumo mingi' -> 'mifumo myingi' (kinyume).

Matumizi:  python weka_kanuni_za_ziada.py            (folda ya sasa)
           python weka_kanuni_za_ziada.py njia\\ya\\folda
Usalama: hakiki kila sehemu kwanza (lazima ipatikane mara moja tu); msimbo ukivunjika hakuna kinachobadilishwa.
Nakala ya akiba: kanuni_ya_sarufi.py.bak2. Unaweza kuiendesha tena bila madhara.
Haigusi sehemu za weka_marekebisho_ya_sanifu.py; unaweza kuiendesha kabla au baada yake.
"""
import pathlib
import shutil
import sys

FAILI = "kanuni_ya_sarufi.py"

# ---------------------------------------------------------------- Z2 + zana za nukuu
MANENO_AMBATA_ZA_ZIADA = '''MANENO_AMBATA = [
    (r"\\bwanyama\\s+pori\\b", "wanyamapori"),
    (r"\\bnguvu\\s+kazi\\b", "nguvukazi"),
    # v2.9: nomino ambatani (herufi kubwa inahifadhiwa na _ambata_kwa_herufi; nukuu zinalindwa)
    (r"\\bmwana\\s+i?nchi\\b", "mwananchi"),
    (r"\\bwana\\s+inchi\\b", "wananchi"),
    (r"\\bmwana\\s+ume\\b", "mwanamume"),
    (r"\\bmwana\\s+mke\\b", "mwanamke"),
]

# v2.9: maandishi yaliyo ndani ya nukuu ("..." au \u201c...\u201d, mstari mmoja) hayabadilishwi na kanuni za ambata.
_NUKUU_RX = re.compile(r'"[^"\\n]*"|\\u201c[^\\u201d\\n]*\\u201d')
_CHANZO_ZENYE_KINGA_YA_NUKUU = {"kanuni_ambata"}


def _spans_za_nukuu(s: str) -> list:
    return [(m.start(), m.end()) for m in _NUKUU_RX.finditer(s)]


def _ndani_ya_nukuu(a: int, b: int, spans: list) -> bool:
    return any(x <= a and b <= y for x, y in spans)
'''

# ---------------------------------------------------------------- Z1 (njia mpya)
KAZI_YA_SWALI_JE = '''    # ------------------------------------------------------------
    # v2.9: 'Je,' ni swali -> alama ya kuuliza
    # ------------------------------------------------------------
    _VIFUPISHO_VYA_NUKTA = {"dkt", "bw", "bi", "mf", "nk", "km", "mh", "prof", "mb", "mhe"}

    def _kagua_swali_je(self, s: str) -> List[Kosa]:
        """Sentensi inayoanza na 'Je,' ni swali: ikiisha kwa nukta pendekeza '?'. Nukuu zinalindwa."""
        makosa = []
        nukuu = _spans_za_nukuu(s)
        for m in re.finditer(r"\\bJe,", s):
            if _ndani_ya_nukuu(m.start(), m.end(), nukuu):
                continue
            k = m.end()
            while k < len(s) and s[k] not in ".?!\\n":
                k += 1
            if k >= len(s) or s[k] != ".":
                continue                                   # tayari ina '?', '!' au haina nukta
            if _ndani_ya_nukuu(k, k + 1, nukuu):
                continue
            baada = s[k + 1:]
            if baada and baada[0] not in "\\n \\t":
                continue                                   # '...', '3.5', 'k.m.' n.k.
            if baada and baada[0] in " \\t" and not re.match(r"[ \\t]+[\\"\\u201c(\\[]?[A-Z0-9]", baada):
                continue                                   # nukta ikifuatiwa na herufi ndogo: huenda ni kifupisho
            neno_kabla = re.search(r"([A-Za-z]+)$", s[:k])
            if neno_kabla and neno_kabla.group(1).lower() in self._VIFUPISHO_VYA_NUKTA:
                continue
            makosa.append(Kosa(
                aina="ALAMA", neno=".", nafasi=k, urefu=1,
                ujumbe="Sentensi inayoanza na 'Je,' ni swali; huisha kwa alama ya kuuliza (?).",
                mapendekezo=["?"], chanzo="kanuni_je"))
        return makosa

'''

# ---------------------------------------------------------------- Z3 ('-ingi')
UMBO_LA_INGI = '''        vokali = mzizi[0] in "aeiou"
        if mzizi == "ingi":
            # v2.9: '-ingi' huungana na kiambishi: wa+ingi=wengi, mi+ingi=mingi, vi+ingi=vingi, ki+ingi=kingi.
            return {"A-WA_SG": "mwingi", "U-I_SG": "mwingi", "A-WA_PL": "wengi", "KI-VI_SG": "kingi",
                    "KI-VI_PL": "vingi", "U-I_PL": "mingi", "LI-YA_PL": "mengi"}.get(ngeli)
        if ngeli in ("A-WA_SG", "U-I_SG"):
'''

NGELI_KIVUMISHI_INGI = '''                kiambishi, mzizi = g
                if mzizi == "ingi" and j == i + 1:
                    # v2.9: 'myingi', 'vyingi', 'chingi', 'wingi' si sahihi; 'mingi', 'vingi', 'kingi', 'wengi' ni sahihi.
                    sahihi_ingi = self._umbo_la_kivumishi(ngeli, mzizi)
                    if sahihi_ingi:
                        if tok[0].lower() == sahihi_ingi:
                            break                            # tayari sahihi
                        if tok[0][0].isupper():
                            sahihi_ingi = sahihi_ingi[0].upper() + sahihi_ingi[1:]
                        makosa.append(self._kosa_la_tokeni(
                            s, tok, "NGELI",
                            f"Kivumishi '{tok[0]}' si sahihi kwa nomino '{neno}' ({ngeli}); tumia '{sahihi_ingi}'.",
                            [sahihi_ingi], "ngeli_matrix"))
                        break
                if kiambishi in ruhusa:
                    break
'''

# (jina, old, new)
MABADILIKO = [
    ("Z2 maneno ambata + zana za nukuu",
     'MANENO_AMBATA = [\n'
     '    (r"\\bwanyama\\s+pori\\b", "wanyamapori"),\n'
     '    (r"\\bnguvu\\s+kazi\\b", "nguvukazi"),\n'
     ']\n',
     MANENO_AMBATA_ZA_ZIADA),

    ("Z2 kinga ya nukuu kwenye _kagua_mtindo",
     '        makosa = []\n'
     '        for muundo, ujumbe, chanzo, kitendo in self._kanuni_za_mtindo:\n'
     '            for m in muundo.finditer(s):\n'
     '                neno = m.group(0)\n',
     '        makosa = []\n'
     '        nukuu = _spans_za_nukuu(s)\n'
     '        for muundo, ujumbe, chanzo, kitendo in self._kanuni_za_mtindo:\n'
     '            for m in muundo.finditer(s):\n'
     '                if chanzo in _CHANZO_ZENYE_KINGA_YA_NUKUU and _ndani_ya_nukuu(m.start(), m.end(), nukuu):\n'
     '                    continue\n'
     '                neno = m.group(0)\n'),

    ("Z3a _umbo_la_kivumishi: '-ingi'",
     '        vokali = mzizi[0] in "aeiou"\n'
     '        if ngeli in ("A-WA_SG", "U-I_SG"):\n',
     UMBO_LA_INGI),

    ("Z3b _kagua_ngeli_kivumishi: '-ingi'",
     '                kiambishi, mzizi = g\n'
     '                if kiambishi in ruhusa:\n'
     '                    break\n',
     NGELI_KIVUMISHI_INGI),

    ("Z1a njia ya _kagua_swali_je",
     '        return makosa\n'
     '\n'
     '    # ------------------------------------------------------------\n'
     '    # Usambamba wa vitenzi (v2.6 Bug 4: tokens[j+1:i], si tokens[j+1] pekee)\n',
     '        return makosa\n\n' + KAZI_YA_SWALI_JE +
     '    # ------------------------------------------------------------\n'
     '    # Usambamba wa vitenzi (v2.6 Bug 4: tokens[j+1:i], si tokens[j+1] pekee)\n'),

    ("Z1b sajili ukaguzi kwenye kagua()",
     '            lambda: self._kagua_alama_nyingine(sentensi),\n',
     '            lambda: self._kagua_alama_nyingine(sentensi),\n'
     '            lambda: self._kagua_swali_je(sentensi),\n'),
]


def _tayari(t, old, new):
    """Marekebisho yamekwisha wekwa? (new ikiwa na old ndani yake, inatosha new kuwepo.)"""
    if old in new:
        return new in t
    return new in t and old not in t


def main():
    folda = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    njia = folda / FAILI
    if not njia.is_file():
        sys.exit(f"Sioni {njia}. Weka hati hii kwenye folda ya mradi, au toa njia ya folda.")
    ghafi = njia.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in ghafi else "\n"

    kazi = []
    for jina, old, new in MABADILIKO:
        old_n, new_n = old.replace("\n", nl), new.replace("\n", nl)
        if _tayari(ghafi, old_n, new_n):
            print(f"- {jina}: tayari ipo, nimeruka.")
            continue
        idadi = ghafi.count(old_n)
        if idadi != 1:
            sys.exit(f"Sijapata mahali pa kipekee ({jina}; nimeona mara {idadi}). "
                     "Faili huenda ni toleo tofauti; hakuna kilichobadilishwa.")
        kazi.append((jina, old_n, new_n))

    if not kazi:
        sys.exit("Kanuni zote tayari zipo. Hakuna kilichobadilishwa.")

    mpya = ghafi
    for jina, old_n, new_n in kazi:
        mpya = mpya.replace(old_n, new_n, 1)
    try:
        compile(mpya, FAILI, "exec")
    except SyntaxError as kosa:
        sys.exit(f"Mabadiliko yangevunja {FAILI} ({kosa}). Hakuna kilichobadilishwa.")

    shutil.copy(njia, str(njia) + ".bak2")
    njia.write_bytes(mpya.encode("utf-8"))
    for jina, _o, _n in kazi:
        print(f"- {jina}: imewekwa.")
    print("Imekamilika. Akiba: kanuni_ya_sarufi.py.bak2")


if __name__ == "__main__":
    main()
