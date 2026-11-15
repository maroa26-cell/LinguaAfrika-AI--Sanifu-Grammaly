"""
mhariri_pro.py - Kanuni zako za Kiswahili kwenye njia tatu:

  1. KUHARIRI KISWAHILI        hariri_kiswahili(...)
  2. MHARIRI PRO (Grammarly)   chambua(...), tumia_marekebisho(...), onyesha_kwa_rangi(...)
  3. KUTAFSIRI                 tafsiri_kwenda_kiswahili(...), tafsiri_kutoka_kiswahili(...),
                               rekebisha_tafsiri_ya_kiswahili(...)  (kwa mtafsiri uliopo)

Chanzo cha makosa (kwa mpangilio wa kipaumbele):
  - Kamusi (herufi zilizochanganywa M-A-L-U-W-I-M)           -> Tahajia
  - kanuni_ya_sarufi.py (Yambiwa, ngeli, kiroboti, istilahi) -> Sarufi / Mtindo
  - Alama za uandishi (herufi kubwa, kituo, ';', ', ili')    -> Uakifishaji
  - AI (hiari): makosa ya tahajia/sarufi ambayo kanuni hazioni

Kila suala lina nafasi kamili ndani ya maandishi, kwa hiyo mtumiaji anaweza kuchagua ni yapi yatumike.
Makosa ya AI yanakubaliwa tu kama kipande kilichotajwa kipo hasa kwenye maandishi, na namba hazipotei.
"""

from __future__ import annotations

import html
import re

import sanifu_editor as se
from kanuni_ya_sarufi import (KanuniZaSarufiKiswahili, MAELEKEZO_YA_LUGHA, maelekezo_ya_tafsiri,
                              ni_jozi_ya_kiingereza_kiswahili)

KUNDI = ("Tahajia", "Sarufi", "Uakifishaji", "Mtindo")
RANGI = {"Tahajia": "#ffd6d6", "Sarufi": "#ffe2b8", "Uakifishaji": "#e3d4ff", "Mtindo": "#d3efdc"}

_KUNDI_LA_AINA = {"NGELI": "Sarufi", "MOFOLOJIA": "Sarufi", "MTINDO": "Mtindo",
                  "ISTILAHI": "Mtindo", "KIROBOTI": "Mtindo", "TAHAJIA": "Tahajia",
                  "USAMBAMBA": "Sarufi", "MSAMIATI": "Mtindo"}
_CHANZO_CHA_KUBAHATISHA = {"ngeli_matrix", "kiima_kitenzi"}   # kanuni za makadirio: hazichaguliwi awali

# Semi za kiroboti zenye mbadala wa moja kwa moja (nyingine ni ushauri tu)
UBADILISHAJI_WA_KIROBOTI = {
    "hata ingawa": ["Ingawa", "Ijapokuwa"],
    "fanya maamuzi": ["fanya uamuzi"],
    "mimi ni njaa": ["Nina njaa"],
    "mimi ni baridi": ["Nasikia baridi", "Nahisi baridi"],
    "walikataa kukata tamaa": ["hawakukata tamaa", "walikataa kusalimu amri"],
}

_KANUNI = None


def _kanuni():
    global _KANUNI
    if _KANUNI is None:
        _KANUNI = KanuniZaSarufiKiswahili()
    return _KANUNI


# ----------------------------------------------------------------------------
# Ujenzi wa masuala
# ----------------------------------------------------------------------------

def _suala(kundi, kabla, chaguo, nafasi, urefu, sababu, chanzo, kipaumbele,
           uhakika="juu", chagua_awali=True):
    return {
        "kundi": kundi, "kabla": kabla, "chaguo": list(chaguo),
        "baada": chaguo[0] if chaguo else None,
        "nafasi": nafasi, "urefu": urefu, "sababu": sababu, "chanzo": chanzo,
        "uhakika": uhakika, "kipaumbele": kipaumbele,
        "inaweza_kutumika": bool(chaguo),
        "imechaguliwa_awali": bool(chaguo) and chagua_awali,
    }


def _kama_kabla(kabla, mbadala):
    return mbadala[0].upper() + mbadala[1:] if kabla[:1].isupper() and mbadala else mbadala


def _masuala_ya_anagram(t, kamusi):
    if not kamusi:
        return []
    out = []
    for m in re.finditer(r"\b(?:[A-Za-z]-){3,}[A-Za-z]\b", t):
        jibu = se.tatua_anagram(m.group(0), kamusi)
        if len(jibu) == 1:
            out.append(_suala("Tahajia", m.group(0), [jibu[0]], m.start(), len(m.group(0)),
                              f"Herufi zilizochanganywa zimepangwa upya kuwa '{jibu[0]}' (kutoka kamusi).",
                              "kamusi", 0))
    return out


def _masuala_ya_kanuni(t):
    return _masuala_kutoka_kosa(t, _kanuni().kagua_sentensi_nzima(t, kagua_alama=False)["makosa"])


def _masuala_kutoka_kosa(t, makosa):
    out = []
    for k in makosa:
        if k["aina"] == "TAWALI":
            continue
        nafasi, urefu = k["nafasi"], k["urefu"]
        kabla = t[nafasi:nafasi + urefu]
        kundi = _KUNDI_LA_AINA.get(k["aina"], "Sarufi")
        kubahatisha = k.get("chanzo") in _CHANZO_CHA_KUBAHATISHA
        if k["aina"] == "KIROBOTI":
            chaguo = [_kama_kabla(kabla, x) for x in UBADILISHAJI_WA_KIROBOTI.get(kabla.lower(), [])]
            sababu = k["ujumbe"]
        else:
            chaguo = [m for m in k["mapendekezo"] if m]
            sababu = k["ujumbe"]
        out.append(_suala(
            kundi, kabla, chaguo, nafasi, urefu, sababu, k.get("chanzo") or k["aina"],
            2 if kubahatisha else 1,
            uhakika="wastani" if kubahatisha else "juu",
            chagua_awali=not (kubahatisha or k["aina"] == "ISTILAHI"),
        ))
    return out


def _masuala_ya_alama(t, herufi_kubwa_na_kituo=True, kituo_cha_mwisho=None):
    out = []
    for m in re.finditer(r"\b(?:Ingawa|Kwa kuwa|Kwa sababu)\b[^.;!?\n]*(;)", t, re.I):
        out.append(_suala("Uakifishaji", ";", [","], m.start(1), 1,
                          "Nukta mkato (;) imetumika pale mkato (,) inatosha baada ya kishazi hiki.",
                          "alama", 1))
    for m in re.finditer(r"\w+(,)(?=\s+ili\b)", t):
        out.append(_suala("Uakifishaji", ",", [""], m.start(1), 1,
                          "Mkato haiwekwi kabla ya kiunganishi 'ili'.", "alama", 1))
    if kituo_cha_mwisho is None:
        kituo_cha_mwisho = herufi_kubwa_na_kituo
    if len(t.split()) >= 2:
        if herufi_kubwa_na_kituo:
            i = len(t) - len(t.lstrip())
            if t[i:i + 1].isalpha() and not t[i].isupper():
                out.append(_suala("Uakifishaji", t[i], [t[i].upper()], i, 1,
                                  "Sentensi lazima ianze na herufi kubwa.", "alama", 1))
        if kituo_cha_mwisho:
            j = len(t.rstrip()) - 1
            if j >= 0 and t[j].isalnum():
                out.append(_suala("Uakifishaji", t[j], [t[j] + "."], j, 1,
                                  "Sentensi lazima iishie na alama ya kituo (. ! au ?).", "alama", 1))
    return out


MAELEKEZO_YA_PRO = """
MUUNDO WA JIBU (MODI YA UHAKIKI): USIANDIKE UPYA maandishi yote. Orodhesha makosa tu, kama JSON:
{"masuala": [{"kabla": "<kipande halisi kutoka kwenye maandishi, maneno 1 hadi 8>",
              "baada": "<marekebisho ya kipande hicho>",
              "kundi": "Tahajia | Sarufi | Uakifishaji | Mtindo",
              "sababu": "<sababu sahihi ya kisarufi, kwa Kiswahili>"}]}
Sheria: "kabla" linakiliwa KAMA LILIVYO kutoka kwenye maandishi. Kila suala liwe huru, bila kupishana na jingine.
Taja makosa halisi tu, si mapendeleo ya mtindo. Namba, majina na maneno ya msingi visiondolewe kwenye "baada".
Kama hakuna makosa rudisha {"masuala": []}.
"""


def _mfumo_wa_pro():
    p = se.SANIFU_SYSTEM_PROMPT
    kichwa = p.split("MUUNDO WA JIBU:")[0]
    k = p.find("KANUNI ZA ZIADA ZA KISWAHILI SANIFU (BAKITA):")
    ziada = ("\n\n" + p[k:]) if k != -1 else ""
    return kichwa + ziada + MAELEKEZO_YA_PRO


def _masuala_ya_ai(t, tahadhari):
    try:
        j = se.piga_ai(_mfumo_wa_pro(), t, temperature=0.1)
    except Exception as e:
        tahadhari.append(f"Mkaguzi wa AI ameshindwa ({e}); matokeo ni ya kanuni pekee.")
        return []
    out = []
    for s in (j or {}).get("masuala", []) or []:
        kabla, baada = (s.get("kabla") or ""), s.get("baada")
        if not kabla.strip() or baada is None or baada == kabla or len(kabla) > 120:
            continue
        if se._namba_za(kabla) - se._namba_za(baada):      # usipoteze namba
            continue
        kundi = s.get("kundi") if s.get("kundi") in KUNDI else "Sarufi"
        for m in re.finditer(re.escape(kabla), t):          # lazima kipo hasa kwenye maandishi
            out.append(_suala(kundi, kabla, [baada], m.start(), len(kabla),
                              s.get("sababu") or "Pendekezo la AI.", "ai", 3,
                              uhakika="wastani", chagua_awali=kundi in ("Tahajia", "Uakifishaji")))
    return out


def _ondoa_mwingiliano(masuala):
    """Kipaumbele kwa kanuni sahihi kuliko AI; kati ya sawa, aliyeanza mapema na mrefu zaidi."""
    zilizokubaliwa = []
    for m in sorted(masuala, key=lambda x: (x["kipaumbele"], x["nafasi"], -x["urefu"])):
        if all(m["nafasi"] + m["urefu"] <= a["nafasi"] or a["nafasi"] + a["urefu"] <= m["nafasi"]
               for a in zilizokubaliwa):
            zilizokubaliwa.append(m)
    zilizokubaliwa.sort(key=lambda x: (x["nafasi"], -x["urefu"]))
    for i, m in enumerate(zilizokubaliwa, 1):
        m["id"] = f"m{i}"
    return zilizokubaliwa


# ----------------------------------------------------------------------------
# API ya Mhariri Pro
# ----------------------------------------------------------------------------

def chambua(maandishi, kamusi=None, kutumia_ai=False, herufi_kubwa_na_kituo=True,
            lugha_chanzo=None, chanzo=None, kituo_cha_mwisho=None):
    """
    Huchambua maandishi na kurudisha masuala yote yenye nafasi kamili.
    Kwa tafsiri: toa lugha_chanzo na chanzo (maandishi ya awali) ili msamiati wa kitaaluma ukaguliwe.
    Hurudisha: masuala, idadi_kwa_kundi, alama (0-100), maneno, tahadhari.
    """
    tahadhari = []
    masuala = (_masuala_ya_anagram(maandishi, kamusi)
               + _masuala_ya_kanuni(maandishi)
               + _masuala_ya_alama(maandishi, herufi_kubwa_na_kituo, kituo_cha_mwisho))
    if lugha_chanzo and chanzo:
        masuala += _masuala_kutoka_kosa(maandishi, _kanuni().kagua_tafsiri(lugha_chanzo, chanzo, maandishi))
    if kutumia_ai and maandishi.strip():
        masuala += _masuala_ya_ai(maandishi, tahadhari)
    masuala = _ondoa_mwingiliano(masuala)

    idadi = {k: 0 for k in KUNDI}
    for m in masuala:
        idadi[m["kundi"]] += 1
    uzito = sum(0.5 if m["uhakika"] == "wastani" else 1 for m in masuala)
    maneno = max(len(re.findall(r"\w+", maandishi)), 1)
    return {"masuala": masuala, "idadi_kwa_kundi": idadi,
            "alama": se.hesabu_alama(uzito, maneno), "maneno": maneno, "tahadhari": tahadhari}


def tumia_marekebisho(maandishi, masuala, vilivyochaguliwa=None, mbadala=None):
    """
    Hutumia marekebisho. vilivyochaguliwa = seti ya id (None = yaliyochaguliwa awali).
    mbadala = {id: nambari ya chaguo} pale suala lina chaguo zaidi ya moja.
    """
    mbadala = mbadala or {}
    chaguo = [m for m in masuala if m["inaweza_kutumika"] and
              ((m["id"] in vilivyochaguliwa) if vilivyochaguliwa is not None else m["imechaguliwa_awali"])]
    chaguo.sort(key=lambda m: (m["nafasi"], -m["urefu"]))
    safi, mwisho = [], 0
    for m in chaguo:
        if m["nafasi"] >= mwisho and maandishi[m["nafasi"]:m["nafasi"] + m["urefu"]] == m["kabla"]:
            safi.append(m)
            mwisho = m["nafasi"] + m["urefu"]
    for m in reversed(safi):
        i = min(max(mbadala.get(m["id"], 0), 0), len(m["chaguo"]) - 1)
        maandishi = maandishi[:m["nafasi"]] + m["chaguo"][i] + maandishi[m["nafasi"] + m["urefu"]:]
    return maandishi


def onyesha_kwa_rangi(maandishi, masuala):
    """HTML ya maandishi yenye makosa yaliyoangaziwa kwa rangi kulingana na kundi."""
    sehemu, mwisho = [], 0
    for m in sorted(masuala, key=lambda x: x["nafasi"]):
        if m["nafasi"] < mwisho:
            continue
        sehemu.append(html.escape(maandishi[mwisho:m["nafasi"]]))
        kipande = html.escape(maandishi[m["nafasi"]:m["nafasi"] + m["urefu"]])
        kidokezo = html.escape(f'{m["kundi"]}: {m["sababu"]}', quote=True)
        sehemu.append(f'<mark style="background:{RANGI[m["kundi"]]};padding:0 3px;border-radius:3px" '
                      f'title="{kidokezo}">{kipande}</mark>')
        mwisho = m["nafasi"] + m["urefu"]
    sehemu.append(html.escape(maandishi[mwisho:]))
    return '<div style="white-space:pre-wrap;line-height:1.8">' + "".join(sehemu) + "</div>"


def rekebisha_kiotomatiki(maandishi, kamusi=None, kutumia_ai=False, herufi_kubwa_na_kituo=True, awamu=3, **ziada):
    """
    Hutumia marekebisho yaliyochaguliwa awali tu (yenye uhakika wa juu), kwa awamu hadi yasibadilike.
    Yale ya makadirio (ngeli ya kivumishi/kiima-kitenzi, istilahi) hayatumiki; yanarudishwa kama 'yaliyobaki'.
    """
    yaliyotumika = []
    for _ in range(max(1, awamu)):
        r = chambua(maandishi, kamusi, kutumia_ai, herufi_kubwa_na_kituo, **ziada)
        mpya = tumia_marekebisho(maandishi, r["masuala"])
        yaliyotumika += [m for m in r["masuala"] if m["imechaguliwa_awali"]]
        if mpya == maandishi:
            break
        maandishi = mpya
    r = chambua(maandishi, kamusi, kutumia_ai, herufi_kubwa_na_kituo, **ziada)
    return {"maandishi": maandishi, "yaliyotumika": yaliyotumika,
            "yaliyobaki": [m for m in r["masuala"] if not m["imechaguliwa_awali"]],
            "alama": r["alama"]}


# ----------------------------------------------------------------------------
# Njia za huduma: kuhariri na kutafsiri (zinatumia kanuni zako kwenye maelekezo na ukaguzi)
# ----------------------------------------------------------------------------

def hariri_kiswahili(maandishi, kamusi=None, **vigezo):
    """Kiswahili -> Kiswahili (AI + kanuni + kurudia hadi alama ifike lengo)."""
    return se.hariri_kwa_ubora(maandishi, kamusi=kamusi, lugha_chanzo="Kiswahili",
                               lugha_lengwa="Kiswahili", **vigezo)


def tafsiri_kwenda_kiswahili(maandishi, lugha_chanzo, kamusi=None, **vigezo):
    """Lugha yoyote -> Kiswahili Sanifu. Kanuni zako 16 ziko kwenye maelekezo, na matokeo yanakaguliwa kwa kanuni."""
    return se.hariri_kwa_ubora(maandishi, kamusi=kamusi, lugha_chanzo=lugha_chanzo,
                               lugha_lengwa="Kiswahili", **vigezo)


def tafsiri_kutoka_kiswahili(maandishi, lugha_lengwa, kamusi=None, **vigezo):
    """Kiswahili -> lugha nyingine. Chanzo kinasafishwa kwanza kwa kanuni zako kabla ya kutafsiriwa."""
    return se.hariri_kwa_ubora(maandishi, kamusi=kamusi, lugha_chanzo="Kiswahili",
                               lugha_lengwa=lugha_lengwa, **vigezo)


def tafsiri_na_hariri_bure(maandishi, lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", kamusi=None, **vigezo):
    """
    Mpangilio wa bure: Groq anatafsiri (rasimu ya haraka), Gemini anahariri kwa kanuni kali; hakuna OpenAI.
    Kwa api_server.py: `tafsiri_na_hariri_bure(maandishi)["maandishi_sahihi"]`.
    """
    return se.hariri_kwa_ubora(maandishi, kamusi=kamusi, lugha_chanzo=lugha_chanzo,
                               lugha_lengwa=lugha_lengwa, hali="bure", **vigezo)


def hariri_kwa_gemini_pekee(maandishi, lugha_chanzo="Kiswahili", lugha_lengwa="Kiswahili", kamusi=None, **vigezo):
    """Gemini pekee, kwa ukaguzi wa pili wa lazima (Two-Pass Verification). Hakuna Groq wala OpenAI."""
    return se.hariri_kwa_ubora(maandishi, kamusi=kamusi, lugha_chanzo=lugha_chanzo,
                               lugha_lengwa=lugha_lengwa, hali="gemini_pekee", **vigezo)


def rekebisha_tafsiri_ya_kiswahili(tafsiri, kamusi=None, lugha_chanzo=None, chanzo=None):
    """
    Kwa mtafsiri uliopo (mf. cerebral_cortex.py): pitisha tafsiri ya Kiswahili hapa baada ya AI kuitoa.

    Toa lugha_chanzo na chanzo (maandishi ya awali) ili kanuni za jozi zitumike: kwa Kiingereza -> Kiswahili
    msamiati wa kitaaluma (tija, uaminifu, shirikisha malengo...) hukaguliwa na nukta ya mwisho huongezwa.
    Bila hivyo, haiongezi alama ya kituo wala herufi kubwa (vichwa vya habari vinabaki salama).
    """
    jozi = bool(lugha_chanzo) and ni_jozi_ya_kiingereza_kiswahili(lugha_chanzo, "Kiswahili")
    return rekebisha_kiotomatiki(tafsiri, kamusi=kamusi, herufi_kubwa_na_kituo=False,
                                 lugha_chanzo=lugha_chanzo, chanzo=chanzo, kituo_cha_mwisho=jozi)


def maelekezo_ya_tafsiri_ya_kiswahili(lugha_chanzo=None):
    """
    Kanuni zako 16 (MAELEKEZO_YA_LUGHA['Kiswahili']) kwa mtafsiri wako mwenyewe. Ukitoa lugha_chanzo
    ("Kiingereza (English)"), kanuni za jozi hiyo (ENGLISH-TO-SWAHILI TRANSLATION RULES) zinaongezwa.
    """
    if lugha_chanzo:
        return maelekezo_ya_tafsiri(lugha_chanzo, "Kiswahili")
    return MAELEKEZO_YA_LUGHA["Kiswahili"]
