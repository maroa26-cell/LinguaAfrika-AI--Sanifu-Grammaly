#!/usr/bin/env python3
"""tathmini_mhariri.py — pima ubora wa mhariri kwa namba.

Matumizi (kwenye kompyuta/seva yenye funguo za AI zilizowekwa kama environment variables):
    python tathmini_mhariri.py                 # Flash pekee
    python tathmini_mhariri.py --kina          # Flash + uthibitisho wa Gemini Pro (inahitaji GEMINI_PRO_MODEL)
    python tathmini_mhariri.py --seti faili.json

Vipimo:
  * Kukamata makosa (recall): makosa yanayotarajiwa yaliyopatikana na pendekezo sahihi.
  * Kengele za uongo (false alarms) kwenye sentensi sahihi: mapendekezo yasiyopaswa kuwepo.
  * Ziada: mapendekezo ya ziada kwenye sentensi zenye makosa (yakague kwa macho: yanaweza kuwa sahihi).
"""
import argparse
import json
import os
import sys

import mhariri


def _n(s):
    return " ".join(str(s).lower().split())


def tathmini(kesi, kagua_fn):
    jumla_yaliyotarajiwa = yaliyopatikana = kengele = sentensi_sahihi = ziada = ukiukaji = 0
    mistari = []
    for k in kesi:
        r = kagua_fn(k["maandishi"])
        issues = r["issues"]
        yaliyotarajiwa = k.get("inatarajiwa", [])
        pata = 0
        for e in yaliyotarajiwa:
            if any(_n(i["original"]) == _n(e["original"]) and _n(i["suggestion"]) == _n(e["suggestion"]) for i in issues):
                pata += 1
        nje = [i for i in issues if not any(_n(i["original"]) == _n(e["original"]) for e in yaliyotarajiwa)]
        if not yaliyotarajiwa:
            sentensi_sahihi += 1
            kengele += len(nje)
        else:
            ziada += len(nje)
        if k.get("usiwe") and any(k["usiwe"].lower() in (i["suggestion"] or "").lower() for i in issues):
            ukiukaji += 1
        jumla_yaliyotarajiwa += len(yaliyotarajiwa); yaliyopatikana += pata
        hali = "OK " if pata == len(yaliyotarajiwa) and not (nje and not yaliyotarajiwa) else "XX "
        mistari.append(f"{hali}{k['id']:<12} yamepatikana {pata}/{len(yaliyotarajiwa)}  yasiyotarajiwa {len(nje)}"
                       + (f"  -> {[(i['original'], i['suggestion']) for i in nje]}" if nje else ""))
    return {
        "mistari": mistari,
        "recall": (yaliyopatikana / jumla_yaliyotarajiwa) if jumla_yaliyotarajiwa else 1.0,
        "yaliyotarajiwa": jumla_yaliyotarajiwa, "yaliyopatikana": yaliyopatikana,
        "kengele_za_uongo": kengele, "sentensi_sahihi": sentensi_sahihi, "ziada": ziada,
        "ukiukaji_wa_maagizo": ukiukaji,
    }


def _kagua_halisi(kina):
    import cerebral_cortex
    try:
        from openai import OpenAI
    except Exception:
        OpenAI = None
    k = (os.environ.get("OPENAI_API_KEY") or "").strip()
    ubongo = cerebral_cortex.CerebralCortex(OpenAI(api_key=k) if (OpenAI and k) else None)
    if kina and not ubongo.gemini_pro_modeli:
        sys.exit("Weka GEMINI_PRO_MODEL kwanza ili kutumia --kina.")
    pk = ubongo.piga_json_kina if kina else None
    return lambda t: mhariri.kagua(t, piga_ai=ubongo.piga_json, piga_ai_kina=pk)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seti", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden_set.json"))
    ap.add_argument("--kina", action="store_true")
    a = ap.parse_args()
    kesi = json.load(open(a.seti, encoding="utf-8"))["kesi"]
    m = tathmini(kesi, _kagua_halisi(a.kina))
    print("\n".join(m["mistari"]))
    print(f"\nKukamata makosa: {m['yaliyopatikana']}/{m['yaliyotarajiwa']} ({m['recall']:.0%})")
    print(f"Kengele za uongo: {m['kengele_za_uongo']} kwenye sentensi sahihi {m['sentensi_sahihi']}")
    print(f"Mapendekezo ya ziada kwenye sentensi zenye makosa (yakague): {m['ziada']}")
    print(f"Ukiukaji wa maagizo ya usalama: {m['ukiukaji_wa_maagizo']}")
