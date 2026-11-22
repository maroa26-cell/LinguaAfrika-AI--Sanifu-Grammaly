
#!/usr/bin/env python3
"""
weka_maboresho.py: huweka maboresho ya v2.9 kwenye kanuni_ya_sarufi.py
  1. 'tabia nchi' -> 'tabianchi'  (MANENO_AMBATA, huhifadhi herufi kubwa)
  2. 'vikundi vya ... wanakabiliwa' -> 'vinakabiliwa' (njia mpya _kagua_kiima_vikundi)

Matumizi:   python weka_maboresho.py kanuni_ya_sarufi.py
Nakala ya akiba huhifadhiwa kama kanuni_ya_sarufi.py.bak
"""
import shutil
import sys

NJIA = sys.argv[1] if len(sys.argv) > 1 else "kanuni_ya_sarufi.py"

NJIA_MPYA = '''    # ------------------------------------------------------------
    # v2.9: 'vikundi vya ... wanakabiliwa' -> 'vinakabiliwa'
    # ------------------------------------------------------------
    _MIPAKA_YA_VIKUNDI = {"na", "ambao", "ambavyo", "vilivyo", "vinavyo", "wenye",
                          "kwa", "hata", "au", "kama", "ni", "katika", "kwenye"}
    UMBALI_WA_VIKUNDI = 5

    def _kagua_kiima_vikundi(self, s: str, tokens: list) -> List[Kosa]:
        """'Vikundi vya wanawake wajasiriamali wanakabiliwa' -> 'vinakabiliwa' (kiima ni 'vikundi', KI-VI)."""
        makosa = []
        for i in range(len(tokens) - 1):
            if tokens[i][0].lower() != "vikundi" or tokens[i + 1][0].lower() != "vya":
                continue
            if not self._hakuna_alama(s, tokens, i, i + 1):
                continue
            for j in range(i + 2, min(i + 2 + self.UMBALI_WA_VIKUNDI, len(tokens))):
                if not self._hakuna_alama(s, tokens, j - 1, j):
                    break
                tok = tokens[j]
                w = tok[0].lower()
                if w == "wanakabiliwa":
                    pendekezo = "vinakabiliwa"
                    if tok[0][0].isupper():
                        pendekezo = pendekezo.capitalize()
                    makosa.append(self._kosa_la_tokeni(
                        s, tok, "UPATANISHO",
                        f"Kitenzi '{tok[0]}' hakipatani na kiima '{tokens[i][0]}' (KI-VI); tumia '{pendekezo}'.",
                        [pendekezo], "kiima_vikundi"))
                    break
                if w in self._MIPAKA_YA_VIKUNDI:
                    break
        return makosa

'''

ANCHOR_YA_ALAMA = ("    # ------------------------------------------------------------\n"
                   "    # v2.8: alama za uandishi")

MABADILIKO = [
    ("maneno ambata",
     '    (r"\\bnguvu\\s+kazi\\b", "nguvukazi"),\n]',
     '    (r"\\bnguvu\\s+kazi\\b", "nguvukazi"),\n    (r"\\btabia\\s+nchi\\b", "tabianchi"),\n]'),
    ("njia mpya ya vikundi",
     ANCHOR_YA_ALAMA,
     NJIA_MPYA + ANCHOR_YA_ALAMA),
    ("usajili kwenye kagua()",
     "            lambda: self._kagua_dogodogo(sentensi, tokens),\n",
     "            lambda: self._kagua_dogodogo(sentensi, tokens),\n"
     "            lambda: self._kagua_kiima_vikundi(sentensi, tokens),   # v2.9\n"),
    ("maelekezo ya AI (kanuni 18)",
     "'nguvukazi', 'vidogovidogo'",
     "'nguvukazi', 'tabianchi', 'vidogovidogo'"),
    ("maelezo ya toleo",
     "Toleo 2.8 (sheria kutoka safisha_maandishi_sanifu):",
     "Toleo 2.9:\n"
     "- Mpya: 'tabia nchi' -> 'tabianchi' (maneno ambata, herufi kubwa huhifadhiwa).\n"
     "- Mpya: 'vikundi vya ... wanakabiliwa' -> 'vinakabiliwa' (_kagua_kiima_vikundi; hubadilisha kitenzi pekee).\n\n"
     "Toleo 2.8 (sheria kutoka safisha_maandishi_sanifu):"),
]


def main():
    with open(NJIA, encoding="utf-8", newline="") as f:
        asili = f.read()
    crlf = "\r\n" in asili
    maandishi = asili.replace("\r\n", "\n")

    if "_kagua_kiima_vikundi" in maandishi or "tabianchi\"),\n]" in maandishi:
        print("Maboresho yanaonekana kuwepo tayari; sibadilishi chochote.")
        return 0

    for jina, zamani, mpya in MABADILIKO:
        n = maandishi.count(zamani)
        if n != 1:
            print(f"KOSA: sehemu '{jina}' imepatikana mara {n} (inatakiwa mara 1). Hakuna kilichobadilishwa.")
            return 1
    for jina, zamani, mpya in MABADILIKO:
        maandishi = maandishi.replace(zamani, mpya, 1)

    compile(maandishi, NJIA, "exec")           # hakikisha msimbo bado ni sahihi kabla ya kuandika
    shutil.copyfile(NJIA, NJIA + ".bak")
    with open(NJIA, "w", encoding="utf-8", newline="") as f:
        f.write(maandishi.replace("\n", "\r\n") if crlf else maandishi)
    print(f"Imekamilika: sehemu {len(MABADILIKO)} zimewekwa. Nakala ya akiba: {NJIA}.bak")
    return 0


if __name__ == "__main__":
    sys.exit(main())
