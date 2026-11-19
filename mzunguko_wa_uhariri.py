"""mzunguko_wa_uhariri.py - Uhariri wa mizunguko mingi (hadi alama lengwa) unaoisha kwa uhakika.

Tatizo lililotatuliwa: kuhariri upya hadi alama ifike 90 kunaweza kuzunguka bila kuisha, kwa sababu:
  - AI hupendekeza A->B kisha B->A (kuyumba);
  - pendekezo lile lile hurudiwa mzunguko baada ya mzunguko bila kutatua kosa;
  - alama haifiki 90 kamwe (kwa mfano mapendekezo ya 'mtindo' ya ladha tu);
  - marekebisho yanazalisha makosa mapya na kuzidisha tatizo.

Mzunguko huu huacha mara moja kila moja ya hayo yanapotokea, na hurudisha SABABU ya kuacha.

Matumizi:
    import mzunguko_wa_uhariri as mz
    r = mz.hariri_hadi_kamili(maandishi, piga_ai=_piga_ai, piga_ai_kina=_piga_ai_kina)
    r["maandishi"]        # maandishi ya mwisho
    r["alama_ya_mwanzo"], r["alama_ya_mwisho"]
    r["sababu"], r["maelezo_ya_sababu"]
    r["yaliyotumika"]     # marekebisho yaliyotumika (original, suggestion, kundi, chanzo, mzunguko)
    r["yaliyobaki"]       # matatizo yaliyobaki (kwa mtumiaji kuamua mwenyewe)
"""
import hashlib
from collections import Counter

import mhariri as mh

LENGO_LA_ALAMA = 90
UPEO_WA_MIZUNGUKO = 3            # kila mzunguko = ukaguzi mmoja kamili (huitwa AI), kwa hiyo usiwe mkubwa
UPEO_KWA_PENDEKEZO = 2           # pendekezo lile lile (original->suggestion) halitumiki zaidi ya mara hii
KUNDI_LA_MTINDO = "mtindo"

MAELEZO_YA_SABABU = {
    "lengo_limefikiwa": "Alama lengwa imefikiwa.",
    "hakuna_makosa": "Hakuna makosa yaliyobaki.",
    "hakuna_marekebisho_salama": ("Yaliyobaki ni ya mtindo, yenye shaka, au yamejaribiwa tayari; "
                                  "yameachwa kwa mtumiaji kuamua."),
    "hakuna_mabadiliko": "Marekebisho hayakubadilisha maandishi.",
    "mzunguko_umegunduliwa": "Marekebisho yangerudisha maandishi yaliyopita; yamesimamishwa.",
    "marekebisho_yalizidisha_makosa": "Mzunguko wa mwisho ulizidisha makosa; maandishi yamerudishwa kama yalivyokuwa.",
    "upeo_wa_mizunguko": "Upeo wa mizunguko umefikiwa.",
}


def _alama_ya(text, matatizo):
    return mh.alama(text, len(matatizo))


def _hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _salama(x, kina_imetumika, ruhusu_mtindo):
    """Pendekezo gani linaweza kutumika moja kwa moja bila mtumiaji kuliona."""
    if x["suggestion"] == x["original"]:
        return False
    if x["category"] == KUNDI_LA_MTINDO and not ruhusu_mtindo:
        return False
    if x["source"] == "ai":
        u = x.get("uhakika", "wastani")
        if u == "chini":
            return False
        if u == "wastani" and not kina_imetumika:      # makadirio bila uthibitisho: usitumie yenyewe
            return False
    return True


def hariri_hadi_kamili(text, piga_ai=None, piga_ai_kina=None, lugha=mh.KISWAHILI,
                       lengo=LENGO_LA_ALAMA, upeo=UPEO_WA_MIZUNGUKO, ruhusu_mtindo=False):
    sasa = text
    r = mh.kagua(sasa, piga_ai, piga_ai_kina, lugha)
    alama_ya_mwanzo = _alama_ya(sasa, r["issues"])

    yaliyotumika, ripoti = [], []
    ameonekana = {_hash(sasa)}
    majaribio = Counter()          # (original, suggestion) -> mara ngapi imetumika
    yaliyotumika_funguo = set()    # (original, suggestion) zilizotumika
    sababu = None

    for mzunguko in range(1, upeo + 1):
        matatizo = r["issues"]
        alama_sasa = _alama_ya(sasa, matatizo)
        if not matatizo:
            sababu = "hakuna_makosa"
            break
        if alama_sasa >= lengo:
            sababu = "lengo_limefikiwa"
            break

        chaguliwa = []
        for x in matatizo:
            if not _salama(x, r["kina_imetumika"], ruhusu_mtindo):
                continue
            ufunguo = (x["original"].lower(), x["suggestion"].lower())
            kinyume = (x["suggestion"].lower(), x["original"].lower())
            if kinyume in yaliyotumika_funguo:          # A->B kisha B->A: kuyumba
                continue
            # Pendekezo linalobaki na 'original' ndani yake (mf. "wanafunzi" -> "wanafunzi wote") lingerudiwa
            # na kukua kila mzunguko: litumike mara moja tu. Mengine mara mbili (mahali pengine pa kosa lilelile).
            kikomo = 1 if ufunguo[0] in ufunguo[1] else UPEO_KWA_PENDEKEZO
            if majaribio[ufunguo] >= kikomo:
                continue
            chaguliwa.append(x)
        if not chaguliwa:
            sababu = "hakuna_marekebisho_salama"
            break

        mpya = mh.tumia_marekebisho(sasa, matatizo, {x["id"] for x in chaguliwa})
        if mpya == sasa:
            sababu = "hakuna_mabadiliko"
            break
        if _hash(mpya) in ameonekana:
            sababu = "mzunguko_umegunduliwa"
            break

        r_mpya = mh.kagua(mpya, piga_ai, piga_ai_kina, lugha)
        alama_mpya = _alama_ya(mpya, r_mpya["issues"])
        if alama_mpya < alama_sasa:                      # kuzidisha makosa: kataa mzunguko huu
            sababu = "marekebisho_yalizidisha_makosa"
            break

        for x in chaguliwa:
            ufunguo = (x["original"].lower(), x["suggestion"].lower())
            majaribio[ufunguo] += 1
            yaliyotumika_funguo.add(ufunguo)
            yaliyotumika.append({"original": x["original"], "suggestion": x["suggestion"],
                                 "kundi": x["category"], "chanzo": x["source"], "mzunguko": mzunguko})
        ripoti.append({"mzunguko": mzunguko, "yaliyotumika": len(chaguliwa),
                       "alama_kabla": alama_sasa, "alama_baada": alama_mpya})
        sasa, r = mpya, r_mpya
        ameonekana.add(_hash(sasa))
    else:
        mwisho = r["issues"]
        if not mwisho:
            sababu = "hakuna_makosa"
        elif _alama_ya(sasa, mwisho) >= lengo:
            sababu = "lengo_limefikiwa"
        else:
            sababu = "upeo_wa_mizunguko"

    return {
        "maandishi": sasa,
        "alama_ya_mwanzo": alama_ya_mwanzo,
        "alama_ya_mwisho": _alama_ya(sasa, r["issues"]),
        "mizunguko": len(ripoti),
        "sababu": sababu,
        "maelezo_ya_sababu": MAELEZO_YA_SABABU[sababu],
        "yaliyotumika": yaliyotumika,
        "yaliyobaki": r["issues"],
        "ripoti": ripoti,
    }
