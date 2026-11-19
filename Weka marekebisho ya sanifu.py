"""weka_marekebisho_ya_sanifu.py - Marekebisho ya kikaguzi cha "Lingual Sanifu" (makosa kurudiwa/kuharibiwa).

Hurekebisha faili tatu kwenye folda moja: kanuni_ya_sarufi.py, sanifu_editor.py, mhariri_pro.py

  kanuni_ya_sarufi.py
    K1  'Akina mama wengi' ilibadilishwa kuwa 'Akina akina mama wengi' (herufi kubwa haikuzingatiwa).
    K2  Yambiwa ilikosea vitenzi 'ingia'/'tokea' ('Alitokea mtu' -> 'Alimtokea mtu'): kiima si shamirisho.
    K3  Kazi rekebisha_tafsiri() HAIKUWEPO ingawa sanifu_editor.py inaiita (hasattr ilificha kimya kimya),
        kwa hiyo marekebisho ya kanuni hayakutumika kamwe; sasa yanatumika (salama, yakiwa na kinga ya mzunguko).
  sanifu_editor.py
    E1  ondoa_marudio/kagua_marudio ziliharibu 'sawa sawa' -> 'sawa' na 'ndogo ndogo'/'vidogo vidogo' -> 'ndogo'/'vidogo'.
    E2  Jibu la AI lilikataliwa kwa makosa ya MOFOLOJIA/KIROBOTI yaliyokuwepo tayari kwenye maandishi ya chanzo;
        sasa linakataliwa tu kama lina makosa MAPYA kuliko chanzo.
  mhariri_pro.py
    M1  'sawa sawa' na 'ndogo ndogo' havipendekezwi tena kama marudio ya kuondoa.

Matumizi:  python weka_marekebisho_ya_sanifu.py            (folda ya sasa)
           python weka_marekebisho_ya_sanifu.py njia\\ya\\folda
Usalama: hakiki kwanza kila sehemu kwenye kila faili; kukiwa na tatizo hakuna kinachobadilishwa.
Nakala za akiba: <faili>.bak. Unaweza kuiendesha tena bila madhara.
"""
import pathlib
import shutil
import sys

KAZI_YA_REKEBISHA_TAFSIRI = '''    # --- v2.9: marekebisho ya moja kwa moja (inaitwa na sanifu_editor._hariri_mara_moja) ---
    # Vyanzo vya makadirio na aina zisizo salama kutumika bila mtu kuona.
    _CHANZO_CHA_MAKADIRIO = ("ngeli_matrix", "kiima_kitenzi")
    _AINA_ZISIZO_SALAMA = ("TAWALI",)      # marudio na herufi kubwa: yanaweza kuharibu marudio halali

    def rekebisha_tafsiri(self, lugha_chanzo: str, chanzo: str, tafsiri: str, awamu: int = 3) -> Dict[str, Any]:
        """Tumia marekebisho ya kanuni yenye uhakika kwenye `tafsiri` (hadi `awamu` mara).
        Husimama pale hakuna la kurekebisha, au maandishi yanaporudi kuwa yale yaliyokwisha kuonekana (kuyumba).
        Hurudisha {"maandishi": str, "mabadiliko": [ {kabla, baada, aina, sababu} ]}."""
        sasa = tafsiri or ""
        ameonekana = {sasa}
        mabadiliko: List[Dict[str, Any]] = []
        kiingereza = chanzo if (chanzo and lugha_chanzo and ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo)) else None
        for _ in range(max(1, awamu)):
            makosa = self.mkaguzi.kagua(sasa, kagua_alama=False)
            if kiingereza:
                makosa += self.mkaguzi.kagua_msamiati(kiingereza, sasa)
            salama = [k for k in makosa
                      if k.mapendekezo and k.aina not in self._AINA_ZISIZO_SALAMA
                      and k.chanzo not in self._CHANZO_CHA_MAKADIRIO]
            if not salama:
                break
            mpya, hatua = _tumia_makosa(sasa, salama)
            if mpya == sasa or mpya in ameonekana:
                break
            mabadiliko += hatua
            sasa = mpya
            ameonekana.add(sasa)
        return {"maandishi": sasa, "mabadiliko": mabadiliko}

    # Majina mbadala kwa upatanifu
'''

# (faili, jina, old, new)
MABADILIKO = [
    ("kanuni_ya_sarufi.py", "K1 akina (herufi kubwa)",
     '(?<!akina )', '(?<![Aa]kina )'),
    ("kanuni_ya_sarufi.py", "K2a Yambiwa: shina za kuachwa",
     '        self.vitenzi_vya_kuachwa = {"kuwa", "kulia", "kushoto", "kwenda", "kuja", "kufika", "kukaa", "kutumia"}\n',
     '        self.vitenzi_vya_kuachwa = {"kuwa", "kulia", "kushoto", "kwenda", "kuja", "kufika", "kukaa", "kutumia"}\n'
     '        # Vitenzi vinavyofuatwa na kiima kilichogeuzwa mahali ("Alitokea mtu", "Aliingia mtoto"): si shamirisho.\n'
     '        self.shina_za_kuachwa = {"ingia", "tokea"}\n'),
    ("kanuni_ya_sarufi.py", "K2b Yambiwa: tumia shina za kuachwa",
     '            p = m.groupdict()\n            if p["obj"]:\n                continue\n',
     '            p = m.groupdict()\n            if p["obj"] or p["stem"] in self.shina_za_kuachwa:\n                continue\n'),
    ("kanuni_ya_sarufi.py", "K3 rekebisha_tafsiri",
     '    # Majina mbadala kwa upatanifu\n', KAZI_YA_REKEBISHA_TAFSIRI),

    ("sanifu_editor.py", "E1a MARUDIO_HALALI + msaidizi",
     'MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara"}\n',
     'MARUDIO_HALALI = {"polepole", "kidogo", "sana", "mbali", "pole", "haraka", "mara", "sawa"}\n'
     '_DOGO_RE = re.compile(r"(?:wa|vi|mi|ma|n)dogo", re.IGNORECASE)\n\n\n'
     'def _ni_marudio_halali(neno):\n'
     '    """Marudio halali: orodha ya MARUDIO_HALALI, na \'ndogo ndogo\', \'vidogo vidogo\' n.k. (kanuni ya sarufi\n'
     '    huyaunganisha kuwa \'ndogondogo\'/\'vidogovidogo\'; usiyaondoe)."""\n'
     '    n = neno.lower()\n'
     '    return n in MARUDIO_HALALI or bool(_DOGO_RE.fullmatch(n))\n'),
    ("sanifu_editor.py", "E1b ondoa_marudio",
     'return m.group(0) if neno.lower() in MARUDIO_HALALI else neno',
     'return m.group(0) if _ni_marudio_halali(neno) else neno'),
    ("sanifu_editor.py", "E1c kagua_marudio",
     'if m.group(1).lower() not in MARUDIO_HALALI:',
     'if not _ni_marudio_halali(m.group(1)):'),
    ("sanifu_editor.py", "E2 _jibu_linakubalika: makosa mapya tu",
     '        makubwa = [k for k in kagua_kwa_kanuni_za_bakita(sahihi) if k["aina"] in ("MOFOLOJIA", "KIROBOTI")]\n'
     '        if makubwa:\n'
     '            return False\n',
     '        aina_kubwa = ("MOFOLOJIA", "KIROBOTI")\n'
     '        makubwa = [k for k in kagua_kwa_kanuni_za_bakita(sahihi) if k["aina"] in aina_kubwa]\n'
     '        if makubwa:\n'
     '            # Makosa yaliyokuwepo tayari kwenye chanzo (au chanya za uongo za kanuni) si kosa la AI:\n'
     '            # kataa jibu tu kama lina makosa MAPYA kuliko chanzo.\n'
     '            yaliyokuwepo = [k for k in kagua_kwa_kanuni_za_bakita(asili) if k["aina"] in aina_kubwa]\n'
     '            if len(makubwa) > len(yaliyokuwepo):\n'
     '                return False\n'),

    ("mhariri_pro.py", "M1 marudio halali",
     '        if m.group(1).lower() not in MARUDIO_HALALI and len(m.group(1)) >= 3:\n',
     '        if (m.group(1).lower() not in MARUDIO_HALALI and len(m.group(1)) >= 3\n'
     '                and not re.fullmatch(r"(?:wa|vi|mi|ma|n)dogo|sawa", m.group(1), re.IGNORECASE)):\n'),
]


def _tayari(t, old, new):
    """Marekebisho yamekwisha wekwa? (new ikiwa na old ndani yake, inatosha new kuwepo.)"""
    if old in new:
        return new in t
    return new in t and old not in t


def main():
    folda = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    faili_zote = sorted({f for f, *_ in MABADILIKO})
    yaliyomo, mistari_mipya = {}, {}
    for f in faili_zote:
        njia = folda / f
        if not njia.is_file():
            sys.exit(f"Sioni {njia}. Weka hati hii kwenye folda ya mradi, au toa njia ya folda.")
        ghafi = njia.read_bytes().decode("utf-8")
        mistari_mipya[f] = "\r\n" if "\r\n" in ghafi else "\n"
        yaliyomo[f] = ghafi

    # Hatua 1: hakiki kila sehemu kabla ya kugusa faili yoyote.
    kazi = []
    for f, jina, old, new in MABADILIKO:
        nl = mistari_mipya[f]
        old_n, new_n = old.replace("\n", nl), new.replace("\n", nl)
        t = yaliyomo[f]
        if _tayari(t, old_n, new_n):
            print(f"- {f}: {jina}: tayari ipo, nimeruka.")
            continue
        idadi = t.count(old_n)
        if idadi != 1:
            sys.exit(f"Sijapata mahali pa kipekee ({f}: {jina}; nimeona mara {idadi}). "
                     "Faili huenda ni toleo tofauti; hakuna kilichobadilishwa.")
        kazi.append((f, jina, old_n, new_n))

    if not kazi:
        sys.exit("Marekebisho yote tayari yapo. Hakuna kilichobadilishwa.")

    # Hatua 2: tumia kwenye nakala za kumbukumbu na hakikisha msimbo ni halali.
    mpya = dict(yaliyomo)
    for f, jina, old_n, new_n in kazi:
        mpya[f] = mpya[f].replace(old_n, new_n, 1)
    for f in faili_zote:
        if mpya[f] != yaliyomo[f]:
            try:
                compile(mpya[f], f, "exec")
            except SyntaxError as kosa:
                sys.exit(f"Mabadiliko yangevunja {f} ({kosa}). Hakuna kilichobadilishwa.")

    # Hatua 3: akiba kisha andika.
    for f in faili_zote:
        if mpya[f] != yaliyomo[f]:
            njia = folda / f
            shutil.copy(njia, str(njia) + ".bak")
            njia.write_bytes(mpya[f].encode("utf-8"))
    for f, jina, _o, _n in kazi:
        print(f"- {f}: {jina}: imewekwa.")
    print("Imekamilika. Akiba: <faili>.bak")


if __name__ == "__main__":
    main()
