"""kagua_marekebisho.py - Hakiki kama marekebisho ya Sanifu yamewekwa na yanafanya kazi (hakuna simu za AI).

Matumizi (kwenye folda ya mradi, ile yenye kanuni_ya_sarufi.py na sanifu_editor.py):
    python kagua_marekebisho.py
Inachapisha OK / SHIDA kwa kila kipengee. Ukiona SHIDA, niletee matokeo yote.
"""
import importlib
import pathlib
import sys

folda = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(folda))
matokeo = []


def kagua(jina, hali, maelezo=""):
    matokeo.append(hali)
    print(("OK    " if hali else "SHIDA ") + jina + (f"  ({maelezo})" if maelezo and not hali else ""))


def maandishi_ya(faili):
    p = folda / faili
    return p.read_text(encoding="utf-8") if p.is_file() else None


print(f"Folda: {folda}\n--- 1. Faili zina marekebisho?")
alama = [
    ("kanuni_ya_sarufi.py", "def rekebisha_tafsiri", "rekebisha_tafsiri (K3)"),
    ("kanuni_ya_sarufi.py", "(?<![Aa]kina )", "Akina herufi kubwa (K1)"),
    ("kanuni_ya_sarufi.py", "shina_za_kuachwa", "Yambiwa ingia/tokea (K2)"),
    ("kanuni_ya_sarufi.py", "TAASISI_ZA_I_ZI", "taasisi za I-ZI (K4)"),
    ("sanifu_editor.py", "_ni_marudio_halali", "marudio halali (E1)"),
    ("sanifu_editor.py", "yaliyokuwepo = [k for k in kagua_kwa_kanuni_za_bakita(asili)", "jibu la AI: makosa mapya tu (E2)"),
    ("sanifu_editor.py", "TAASISI NI NGELI YA I-ZI", "maelekezo ya AI (E3)"),
    ("mhariri_pro.py", "(?:wa|vi|mi|ma|n)dogo|sawa", "marudio halali kwenye Pro (M1)"),
]
for faili, kipande, jina in alama:
    t = maandishi_ya(faili)
    kagua(f"{faili}: {jina}", t is not None and kipande in t, "faili halipo" if t is None else "bado haijawekwa")

print("\n--- 2. Tabia (bila AI)")
try:
    ks = importlib.import_module("kanuni_ya_sarufi")
    se = importlib.import_module("sanifu_editor")
    K = ks.KanuniZaSarufiKiswahili()
    kagua("rekebisha_tafsiri ipo", hasattr(K, "rekebisha_tafsiri"))
    if hasattr(K, "rekebisha_tafsiri"):
        r = lambda t: K.rekebisha_tafsiri("Kiswahili", "", t)["maandishi"]
        kagua("'Akina mama wengi' haidubwi", "Akina akina" not in r("Akina mama wengi walifika."), r("Akina mama wengi walifika."))
        kagua("'Alitokea mtu' haiguswi", "Alitokea mtu" in r("Alitokea mtu mlangoni."), r("Alitokea mtu mlangoni."))
        kagua("'Serikali alisema' -> 'ilisema'", "Serikali ilisema" in r("Serikali alisema leo."), r("Serikali alisema leo."))
        kagua("'Kampuni walitaka' -> 'zilitaka'", "Kampuni zilitaka" in r("Kampuni walitaka kununua."), r("Kampuni walitaka kununua."))
        kagua("'Serikali imesema' haiguswi", "Serikali imesema" in r("Serikali imesema leo."), r("Serikali imesema leo."))
    kagua("'sawa sawa' haiondolewi", "sawa sawa" in se.ondoa_marudio("Hii ni sawa sawa na ile."), se.ondoa_marudio("Hii ni sawa sawa na ile."))
    kagua("'ndogo ndogo' haiondolewi", "ndogo ndogo" in se.ondoa_marudio("Biashara ndogo ndogo zinakua."))
    kagua("marudio ya kweli yanaondolewa", se.ondoa_marudio("Alikwenda sokoni sokoni.").count("sokoni") == 1)
except Exception as e:
    kagua("kuingiza moduli na kujaribu tabia", False, f"{type(e).__name__}: {str(e)[:150]}")

print(f"\nMatokeo: {sum(matokeo)}/{len(matokeo)} OK")
sys.exit(0 if all(matokeo) else 1)
