"""weka_kanuni_kwenye_api.py - Inaunganisha kanuni_ya_sarufi.py kwenye api_server.py (v3.4) ili Chrome extension
ipate makosa ya kanuni za Python kupitia /v1/kagua.

Inachofanya:
  - Baada ya makosa ya AI + sheria_baada_ya_ai, inaongeza makosa kutoka kwa MkaguziSarufi (ngeli, Yambiwa,
    ma-/mi-, marudio ya 'dogo', 'Je,' n.k.), kila moja likiwa na start/end za UTF-16 kama extension inavyotaka.
  - Makosa yanayopishana na ya AI hayarudiwi; nukuu ("..." na “...”) hazikaguliwi; kanuni za TAWALI zinarukwa.
  - Kanuni zenye hatari kubwa ya kukosea (Yambiwa, ngeli, mtindo) zinakuwa "hiari" (hazijumuishwi kwenye "Kubali yote").
  - Hata AI ikishindwa, extension bado inapata makosa haya (ai=false).
  - Kinga ya kujipima: seva ikianza hupima kanuni kwa sentensi 3 sahihi; zikitoa makosa, kanuni zinazimwa
    na onyo linaandikwa kwenye Logs (kanuni_ya_sarufi.py ya zamani isiharibu maandishi sahihi).
  - Zima/washa kwa Render: KANUNI_ZA_PYTHON=0 (zima) au 1 (washa, chaguo-msingi).
  - Kanuni ya Yambiwa (kiambishi cha mtendwa: 'itasaidia wakulima' -> 'itawasaidia wakulima') IMEZIMWA kwenye extension
    kwa chaguo-msingi, kwa sababu inapendekeza mabadiliko kwenye sentensi sahihi pia. Iwashe kwa KANUNI_YAMBIWA=1.

Masharti: endesha kwanza weka_marekebisho_ya_sanifu.py na weka_kanuni_za_ziada.py kwenye kanuni_ya_sarufi.py.
Matumizi:  python weka_kanuni_kwenye_api.py            (folda ya sasa)
           python weka_kanuni_kwenye_api.py njia\\ya\\folda
Nakala ya akiba: api_server.py.bak3. Unaweza kuiendesha tena bila madhara.
"""
import pathlib
import shutil
import sys

FAILI = "api_server.py"
FAILI_YA_KANUNI = "kanuni_ya_sarufi.py"

# Alama zinazothibitisha kwamba kanuni_ya_sarufi.py imekwisha rekebishwa (vinginevyo kuna makosa ya uongo).
ALAMA_ZA_KANUNI = [
    ("_kagua_swali_je", "weka_kanuni_za_ziada.py (Je, nomino ambatani, -ingi)"),
    ("shina_za_kuachwa", "weka_marekebisho_ya_sanifu.py (K2: ingia/tokea)"),
    ("(?<![Aa]kina )", "weka_marekebisho_ya_sanifu.py (K1: Akina)"),
]

KAZI_ZA_KANUNI = '''# ------------------------------------------------------------------
# 9C. KANUNI ZA SARUFI ZA PYTHON (kanuni_ya_sarufi.py) -> makosa ya ziada kwa extension
#     Zinaongezwa baada ya makosa ya AI; zinafanya kazi hata AI ikishindwa.
# ------------------------------------------------------------------
KANUNI_ZA_PYTHON = os.environ.get("KANUNI_ZA_PYTHON", "1") == "1"
KANUNI_YAMBIWA = os.environ.get("KANUNI_YAMBIWA", "0") == "1"   # kiambishi cha mtendwa (-m-/-wa-): imezimwa kwa chaguo-msingi
_NUKUU_ZA_KANUNI_RX = re.compile(r'"[^"\\n]*"|\\u201c[^\\u201d\\n]*\\u201d')

# Aina za Kosa -> lebo ya extension
_LEBO_ZA_KANUNI = {
    "TAHAJIA": "Tahajia", "NGELI": "Ngeli", "UPATANISHO": "Upatanisho wa kiima na kitenzi",
    "MOFOLOJIA": "Kiambishi cha mtendwa", "ALAMA": "Alama za uandishi", "MTINDO": "Mtindo",
    "SINTAKSIA": "Sintaksia", "MSAMIATI": "Msamiati",
}
# Vyanzo vya kanuni zisizo na utata (hazihitaji "hiari"); vingine vyote ni vya hiari.
_CHANZO_SALAMA_CHA_KANUNI = {
    "tahajia", "maneno_ambata", "kanuni_ambata", "alama", "kanuni_je", "kanuni_ingawa",
    "kanuni_tarehe", "kanuni_zui",
}

# Sentensi sahihi: kanuni lazima zisizipatie kosa lolote (kinga dhidi ya kanuni_ya_sarufi.py ya zamani).
_SENTENSI_ZA_KUPIMA = (
    "Akina mama wengi wanakuja.",
    "Mifumo mingi inatumika.",
    "Alitokea mtu na aliingia mtoto.",
)


def _jenga_mkaguzi_wa_kanuni():
    if not KANUNI_ZA_PYTHON:
        print("Kanuni za Python: zimezimwa (KANUNI_ZA_PYTHON=0).")
        return None
    try:
        from kanuni_ya_sarufi import KanuniZaSarufiKiswahili
        mkaguzi = KanuniZaSarufiKiswahili().mkaguzi
        for s in _SENTENSI_ZA_KUPIMA:
            makosa = mkaguzi.kagua(s, kagua_alama=False)
            if makosa:
                print(f"Kanuni za Python zimezimwa: kipimo cha usalama kimeshindwa kwa {s!r} -> "
                      f"{[(k.neno, k.mapendekezo[:1]) for k in makosa]}. "
                      "Endesha weka_marekebisho_ya_sanifu.py na weka_kanuni_za_ziada.py kwenye kanuni_ya_sarufi.py.")
                return None
        return mkaguzi
    except Exception as e:  # noqa: BLE001
        print(f"Kanuni za Python hazikupakiwa: {type(e).__name__}: {str(e)[:200]}")
        return None


_MKAGUZI_WA_KANUNI = _jenga_mkaguzi_wa_kanuni()


def _ongeza_makosa_ya_kanuni(maandishi: str, issues: list) -> list:
    """Huongeza makosa ya kanuni_ya_sarufi.py kwenye `issues` (hayarudii wala kupishana na yaliyopo)."""
    if _MKAGUZI_WA_KANUNI is None:
        return issues
    try:
        makosa = _MKAGUZI_WA_KANUNI.kagua(maandishi, kagua_alama=False)
    except Exception as e:  # noqa: BLE001
        print(f"Kanuni za Python zimeshindwa: {type(e).__name__}: {str(e)[:200]}")
        return issues

    nukuu = [(m.start(), m.end()) for m in _NUKUU_ZA_KANUNI_RX.finditer(maandishi)]
    zilizopo = [(i["start"], i["end"]) for i in issues]
    mpya = []
    for k in makosa:
        if k.aina == "TAWALI" or not k.mapendekezo:
            continue
        if k.aina == "MOFOLOJIA" and not KANUNI_YAMBIWA:
            continue
        pendekezo = k.mapendekezo[0]
        a, b = k.nafasi, k.nafasi + k.urefu
        if not pendekezo or pendekezo == k.neno or maandishi[a:b] != k.neno:
            continue
        if any(x <= a and b <= y for x, y in nukuu):      # nukuu hazikaguliwi
            continue
        s16, e16 = _u16(maandishi, a), _u16(maandishi, b)
        if any(s16 < ze and zs < e16 for zs, ze in zilizopo):   # inapishana na kosa lililopo
            continue
        mpya.append({
            "original": k.neno,
            "suggestion": pendekezo,
            "start": s16,
            "end": e16,
            "label": _LEBO_ZA_KANUNI.get(k.aina, "Mengineyo"),
            "explanation": k.ujumbe,
            "hiari": k.chanzo not in _CHANZO_SALAMA_CHA_KANUNI,
        })
        zilizopo.append((s16, e16))
    return sorted(issues + mpya, key=lambda i: i["start"])


'''

# (jina, old, new)
MABADILIKO = [
    ("A1 kazi za kanuni (sehemu 9C)",
     '# ------------------------------------------------------------------\n'
     '# 10. NJIA (ROUTES)\n',
     KAZI_ZA_KANUNI +
     '# ------------------------------------------------------------------\n'
     '# 10. NJIA (ROUTES)\n'),

    ("A2 itumie kwenye /v1/kagua",
     '    issues = _kwa_extension(maandishi, mapendekezo_ya_maandishi(r["mistari"]))\n',
     '    issues = _kwa_extension(maandishi, mapendekezo_ya_maandishi(r["mistari"]))\n'
     '    issues = _ongeza_makosa_ya_kanuni(maandishi, issues)   # kanuni_ya_sarufi.py\n'),
]


def _tayari(t, old, new):
    if old in new:
        return new in t
    return new in t and old not in t


def main():
    folda = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    njia = folda / FAILI
    if not njia.is_file():
        sys.exit(f"Sioni {njia}. Weka hati hii kwenye folda ya mradi, au toa njia ya folda.")

    # Hakikisha kanuni_ya_sarufi.py imerekebishwa kwanza (vinginevyo kuna makosa ya uongo).
    kn = folda / FAILI_YA_KANUNI
    if kn.is_file():
        maandishi_ya_kanuni = kn.read_bytes().decode("utf-8")
        yaliyokosekana = [maelezo for alama, maelezo in ALAMA_ZA_KANUNI if alama not in maandishi_ya_kanuni]
        if yaliyokosekana:
            sys.exit("kanuni_ya_sarufi.py bado haijarekebishwa kikamilifu. Endesha kwanza:\n  - "
                     + "\n  - ".join(yaliyokosekana) + "\nHakuna kilichobadilishwa.")
    else:
        print(f"Onyo: sioni {kn}; nimeendelea, lakini hakikisha faili hiyo ipo kwenye repo ileile ya Render.")

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
        sys.exit("Kila kitu tayari kipo. Hakuna kilichobadilishwa.")

    mpya = ghafi
    for jina, old_n, new_n in kazi:
        mpya = mpya.replace(old_n, new_n, 1)
    try:
        compile(mpya, FAILI, "exec")
    except SyntaxError as kosa:
        sys.exit(f"Mabadiliko yangevunja {FAILI} ({kosa}). Hakuna kilichobadilishwa.")

    shutil.copy(njia, str(njia) + ".bak3")
    njia.write_bytes(mpya.encode("utf-8"))
    for jina, _o, _n in kazi:
        print(f"- {jina}: imewekwa.")
    print("Imekamilika. Akiba: api_server.py.bak3")


if __name__ == "__main__":
    main()
