"""weka_sheria_ya_alama.py - Huongeza sheria ya alama ya kuuliza kwenye mhariri.py.

Sentensi huongezwa mwishoni mwa sheria 3 katika maelekezo yote mawili:
  1. maelekezo ya Kiswahili
  2. maelekezo ya lugha nyingine

Usalama: hakiki kwanza mahali pote; kama kuna tatizo hakuna kinachobadilishwa.
Unaweza kuiendesha tena bila madhara: mahali palipokwisha kuwa na sentensi huruka.

Matumizi: weka faili hili kwenye folda moja na mhariri.py, kisha endesha:
    python weka_sheria_ya_alama.py
(au: python weka_sheria_ya_alama.py njia\\ya\\mhariri.py)
Nakala ya akiba huhifadhiwa kama mhariri.py.bak
"""
import pathlib
import shutil
import sys

SENTENSI = "Alama ya kuuliza mwishoni mwa sentensi usiibadilishe isipokuwa kosa ni wazi kabisa."

# (jina la mahali, mwisho wa sheria 3 unaotafutwa)
MAHALI = [
    ("maelekezo ya Kiswahili",
     "Kama maumbo mawili yanakubalika katika Kiswahili, yaache. "),
    ("maelekezo ya lugha nyingine",
     "Kama maumbo mawili yanakubalika katika lugha hiyo, yaache. "),
]

faili = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "mhariri.py")
if not faili.is_file():
    sys.exit(f"Sioni faili {faili}. Liweke hapa pamoja na hati hii, au toa njia kamili.")

maandishi = faili.read_bytes().decode("utf-8")   # bytes: mistari mipya haibadiliki

# Hatua 1: hakiki kila kitu kabla ya kugusa faili.
kazi = []
for jina, mwisho in MAHALI:
    idadi = maandishi.count(mwisho)
    if idadi != 1:
        sys.exit(f"Sijapata mahali pa kipekee pa kuingiza sentensi ({jina}; nimeona mara {idadi}). "
                 "Faili hili huenda ni toleo tofauti; hakuna kilichobadilishwa.")
    if (mwisho + SENTENSI) in maandishi:
        print(f"- {jina}: sentensi tayari ipo, nimeruka.")
    else:
        kazi.append((jina, mwisho))

if not kazi:
    sys.exit("Sentensi tayari ipo kila mahali. Hakuna kilichobadilishwa.")

# Hatua 2: akiba, kisha mabadiliko.
shutil.copy(faili, str(faili) + ".bak")
mpya = maandishi
for jina, mwisho in kazi:
    mpya = mpya.replace(mwisho, mwisho + SENTENSI + " ", 1)
    print(f"- {jina}: sentensi imeongezwa.")

# Hatua 3: hakikisha matokeo ni msimbo halali wa Python kabla ya kuandika.
try:
    compile(mpya, str(faili), "exec")
except SyntaxError as kosa:
    sys.exit(f"Mabadiliko yangevunja msimbo ({kosa}). Hakuna kilichobadilishwa.")

faili.write_bytes(mpya.encode("utf-8"))
print(f"Imekamilika: {faili} imesasishwa. Akiba: {faili}.bak")
