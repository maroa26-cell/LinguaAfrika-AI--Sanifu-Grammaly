"""weka_sheria_ya_alama.py - Huongeza sheria ya alama ya kuuliza kwenye mhariri.py (mwishoni mwa sheria 3).

Matumizi: weka faili hili kwenye folda moja na mhariri.py, kisha endesha:
    python weka_sheria_ya_alama.py
(au: python weka_sheria_ya_alama.py njia\\ya\\mhariri.py)
Nakala ya akiba huhifadhiwa kama mhariri.py.bak
"""
import pathlib
import shutil
import sys

SENTENSI = "Alama ya kuuliza mwishoni mwa sentensi usiibadilishe isipokuwa kosa ni wazi kabisa."
MWISHO_WA_SHERIA_3 = "Kama maumbo mawili yanakubalika katika Kiswahili, yaache. "

faili = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "mhariri.py")
if not faili.is_file():
    sys.exit(f"Sioni faili {faili}. Liweke hapa pamoja na hati hii, au toa njia kamili.")

maandishi = faili.read_bytes().decode("utf-8")   # bytes: mistari mipya haibadiliki
if SENTENSI in maandishi:
    sys.exit("Sentensi hii tayari ipo. Hakuna kilichobadilishwa.")
if maandishi.count(MWISHO_WA_SHERIA_3) != 1:
    sys.exit("Sijapata mahali pa kuingiza sentensi (sheria 3 ya MAELEKEZO_YA_MFUMO). "
             "Faili hili huenda ni toleo tofauti; hakuna kilichobadilishwa.")

shutil.copy(faili, str(faili) + ".bak")
mpya = maandishi.replace(MWISHO_WA_SHERIA_3, MWISHO_WA_SHERIA_3 + SENTENSI + " ", 1)
faili.write_bytes(mpya.encode("utf-8"))
print(f"Imekamilika: sentensi imeongezwa kwenye {faili}. Akiba: {faili}.bak")
