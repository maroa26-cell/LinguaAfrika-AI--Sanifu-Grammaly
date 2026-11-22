"""
weka_marekebisho.py - Huweka marekebisho ya prompt na kichujio kwenye faili la seva (app.py / api_server.py).

Matumizi (kwenye folda ya seva):
    python weka_marekebisho.py app.py
(au jina la faili lako lenye "/v1/kagua", mfano api_server.py)

Inatengeneza nakala ya akiba (jina.bak) kwanza. Kila marekebisho yakikosa mahali pa kuingia,
inakuambia na haibadilishi chochote. Inaweza kuendeshwa tena bila kudubu.
"""
import pathlib
import shutil
import sys

njia = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.py")
if not njia.is_file():
    sys.exit(f"Faili halipo: {njia}")

ghafi = njia.read_bytes().decode("utf-8")
crlf = "\r\n" in ghafi
t = ghafi.replace("\r\n", "\n")

SEHEMU_YA_PROMPT_KUU = """   - Kivumishi '-ingi' huoana na ngeli ya nomino: A-WA 'wateja wengi', 'watu wengi'; U-I 'miti mingi'; LI-YA 'maji mengi', 'mambo mengi'; KI-VI 'vitu vingi'; I-ZI 'biashara nyingi', 'pesa nyingi'. 'wateja myingi' ni kosa; sahihi ni 'wateja wengi'. Usibadilishe 'myingi' kuwa 'mingi' bila kuangalia nomino.
"""
SHERIA_4A = """4A. MARUDIO HALALI: 'wadogo wadogo', 'madogomadogo', 'polepole', 'haraka haraka', 'kidogo kidogo', 'mara kwa mara', 'kimya kimya', 'sawa sawa' ni sahihi na hutoa msisitizo. Usiyaondoe. Usibadilishe 'na', 'ya', 'wa', 'kwa' kuwa maneno mengine (mfano 'na' kuwa 'dhidi ya') isipokuwa kosa liko wazi bila shaka.
"""
UKAGUZI = """- '-ingi' huoana na ngeli: 'wateja wengi', 'miti mingi', 'maji mengi', 'vitu vingi', 'biashara nyingi'. Usibadilishe 'wateja myingi' kuwa 'wateja mingi'; sahihi ni 'wateja wengi'.
- Marudio kama 'wadogo wadogo', 'sawa sawa', 'kidogo kidogo' ni sahihi; usiyaondoe.
"""
SEHEMU_YA_MARUDIO = '''_MARUDIO_HALALI = {
    "wadogo", "wakubwa", "vidogo", "vikubwa", "kidogo", "haraka", "polepole", "taratibu",
    "mbali", "sawa", "kimya", "vizuri", "moja", "mmoja", "pole", "mara", "madogomadogo",
}


'''
PROMPT_NAHAU = """   - Nahau: 'akina mama wengi' (si 'mama wengi'). 'wakati mwingi' na 'muda mwingi' (si 'wakati mingi' wala 'muda mingi'), kwa sababu 'wakati' na 'muda' huchukua 'mwingi'.
"""
UKAGUZI_NAHAU = """- Nahau: 'akina mama wengi' (si 'mama wengi'); 'wakati mwingi', 'muda mwingi' (si 'wakati mingi', 'muda mingi').
"""
PROMPT_BABA = """   - 'akina' hutumika mbele ya nomino za umoja za watu: 'akina mama wengi', 'akina baba wengi'. Nomino ya wingi haipewi 'akina': 'watoto wengi' (si 'akina watoto wengi').
"""
UKAGUZI_BABA = """- 'akina mama wengi', 'akina baba wengi' (si 'mama wengi', 'baba wengi'); 'watoto wengi' ni sahihi, usiongeze 'akina' mbele ya wingi.
"""
KICHUJIO = '''        if p["aina"] == "kujirudia":
            _w = original.lower().split()
            if len(_w) == 2 and _w[0] == _w[1] and _w[0] in _MARUDIO_HALALI:
                continue   # marudio halali (mf. "wadogo wadogo"): si kosa
'''

# (jina, alama, maandishi_mapya, mahali, kitambulisho_cha_kuzuia_kurudia)
MAREKEBISHO = [
    ("Prompt kuu: ngeli ya -ingi",
     "   - Kitenzi lazima kioane na nomino halisi inayotenda, si nomino iliyo karibu tu.\n",
     SEHEMU_YA_PROMPT_KUU, "baada", "Kivumishi '-ingi' huoana"),
    ("Prompt kuu: sheria 4A (marudio)",
     "4B. UKALI WA KUONDOA KIINGEREZA", SHERIA_4A, "kabla", "4A. MARUDIO HALALI"),
    ("Prompt ya ukaguzi wa pili",
     "- Toa maandishi yaliyokaguliwa PEKEE", UKAGUZI, "kabla", "'-ingi' huoana na ngeli: 'wateja wengi'"),
    ("Orodha ya marudio halali",
     "def _u16(s: str, i: int) -> int:", SEHEMU_YA_MARUDIO, "kabla", "_MARUDIO_HALALI = {"),
    ("Kichujio cha marudio halali",
     '        original, suggestion = p["kutoka"], p["kuwa"]\n', KICHUJIO, "baada", "_MARUDIO_HALALI:"),
    ("Prompt kuu: akina mama, wakati/muda mwingi",
     "Usibadilishe 'myingi' kuwa 'mingi' bila kuangalia nomino.\n", PROMPT_NAHAU, "baada",
     "Nahau: 'akina mama wengi' (si 'mama wengi'). 'wakati mwingi'"),
    ("Prompt ya ukaguzi: akina mama, wakati/muda mwingi",
     "- Marudio kama 'wadogo wadogo', 'sawa sawa', 'kidogo kidogo' ni sahihi; usiyaondoe.\n", UKAGUZI_NAHAU, "baada",
     "Nahau: 'akina mama wengi' (si 'mama wengi'); 'wakati mwingi'"),
    ("Prompt kuu: akina baba, watoto wengi",
     "huchukua 'mwingi'.\n", PROMPT_BABA, "baada", "'akina' hutumika mbele ya nomino za umoja za watu"),
    ("Prompt ya ukaguzi: akina baba, watoto wengi",
     "(si 'wakati mingi', 'muda mingi').\n", UKAGUZI_BABA, "baada", "'akina baba wengi' (si 'mama wengi', 'baba wengi')"),
]

jumla_ya_mabadiliko = 0
kushindwa = []
for jina, alama, mpya, mahali, kitambulisho in MAREKEBISHO:
    if kitambulisho in t:
        print(f"IMESHAWEKWA  {jina}")
        continue
    if t.count(alama) != 1:
        print(f"SHIDA        {jina}: mahali pa kuingia hapakupatikana mara moja (zilizopatikana: {t.count(alama)})")
        kushindwa.append(jina)
        continue
    t = t.replace(alama, mpya + alama if mahali == "kabla" else alama + mpya)
    jumla_ya_mabadiliko += 1
    print(f"IMEWEKWA     {jina}")

if kushindwa:
    sys.exit("\\nBaadhi hazikuwekwa; hakuna faili lililobadilishwa. Nitumie matokeo haya.")
if jumla_ya_mabadiliko:
    shutil.copyfile(njia, str(njia) + ".bak")
    njia.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
    print(f"\nImekamilika. Nakala ya akiba: {njia}.bak")
else:
    print("\nHakuna cha kubadilisha.")
