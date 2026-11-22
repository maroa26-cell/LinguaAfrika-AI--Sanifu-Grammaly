#!/usr/bin/env python3
"""
Kipimo cha ubora cha AI Lingual Africa Sanifu.

Matumizi:
  # 1. Bila AI na bila mtandao: hupima chujio la Python pekee (kesi zenye chujio_peke=true)
  python tests/pima_mfumo.py --chujio-tu

  # 2. Mfumo mzima kwenye seva yako (Render au local)
  python tests/pima_mfumo.py --url https://jina-lako.onrender.com
  python tests/pima_mfumo.py --url http://localhost:10000 --kategoria ngeli
  (kama umeweka API_KEY kwenye Render: set API_KEY=... kwenye mazingira yako kabla ya kuendesha)

  # 3. Linganisha matokeo ya mara mbili (kabla na baada ya badiliko)
  python tests/pima_mfumo.py --linganisha tests/matokeo/a.json tests/matokeo/b.json

Matokeo huhifadhiwa kwenye tests/matokeo/ kila unapoendesha, ili uweze kulinganisha baadaye.
Msimbo wa kutoka (exit code) ni 1 kama kuna sentensi sahihi iliyoharibiwa (regression)
au kiwango cha kufaulu kiko chini ya --kizingiti.
"""
import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime

MAHALI = os.path.dirname(os.path.abspath(__file__))
SETI_YA_KAWAIDA = os.path.join(MAHALI, "seti_ya_majaribio.json")
FOLDA_YA_MATOKEO = os.path.join(MAHALI, "matokeo")
MANENO_YA_KIINGEREZA = {"the", "and", "of", "is", "are", "for", "with", "that"}


# ------------------------------------------------------------------
# Zana
# ------------------------------------------------------------------
def norm(s: str) -> str:
    mistari = [re.sub(r"\s+", " ", m).strip() for m in s.strip().split("\n")]
    return "\n".join(mistari)


def pakia_api_server():
    """Hupakia api_server.py (kwa --chujio-tu). Vifurushi visivyopo vinabadilishwa na vibandia."""
    from unittest.mock import MagicMock
    sys.path.insert(0, os.path.dirname(MAHALI))
    for jina in ["flask", "flask_cors", "google", "google.genai", "google.genai.types", "groq"]:
        try:
            __import__(jina)
        except ImportError:
            sys.modules[jina] = MagicMock()
    import api_server
    return api_server


def chujio_nje_ya_mtandao(maandishi: str, mod) -> str:
    return "\n".join(
        mod.safisha_maandishi_sanifu(m) if m.strip() else m for m in maandishi.split("\n")
    )


def ita_api(url: str, kesi: dict, ufunguo: str, muda: int):
    njia = "/tafsiri" if kesi["aina"] == "tafsiri" else "/hariri"
    mwili = json.dumps({"text": kesi["ingizo"], "mode": kesi["aina"]}).encode("utf-8")
    vichwa = {"Content-Type": "application/json"}
    if ufunguo:
        vichwa["X-API-Key"] = ufunguo
    ombi = urllib.request.Request(url.rstrip("/") + njia, data=mwili, headers=vichwa, method="POST")
    mwanzo = time.time()
    try:
        with urllib.request.urlopen(ombi, timeout=muda) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode("utf-8"))
        except Exception:
            data = {"ok": False, "error": f"HTTP {e.code}"}
    except Exception as e:
        data = {"ok": False, "error": str(e)}
    return data, time.time() - mwanzo


# ------------------------------------------------------------------
# Tathmini ya kesi moja
# ------------------------------------------------------------------
def tathmini(kesi: dict, jibu):
    """Hurudisha hali: pita | shindwa | imeharibiwa (sentensi sahihi imebadilishwa) | hakuna_jibu."""
    if jibu is None:
        return {"hali": "hakuna_jibu", "sababu": ["seva haikurudisha matokeo"], "ulinganifu": None}

    n = norm(jibu)
    sababu = []
    inatarajiwa = kesi["ingizo"] if kesi["kategoria"] == "usigusiwe" else kesi.get("inatarajiwa")

    ulinganifu = None
    if inatarajiwa is not None:
        ulinganifu = round(difflib.SequenceMatcher(None, norm(inatarajiwa), n).ratio(), 3)
        if n != norm(inatarajiwa):
            sababu.append("tofauti na kinachotarajiwa")
    for s in kesi.get("lazima_iwe_na", []):
        if s.lower() not in n.lower():
            sababu.append(f"haina '{s}'")
    for s in kesi.get("isiwe_na", []):
        if s.lower() in n.lower():
            sababu.append(f"ina '{s}' (haitakiwi)")
    if kesi["aina"] == "tafsiri":
        bakia = sorted(MANENO_YA_KIINGEREZA & set(re.findall(r"[a-z]+", n.lower())))
        if bakia:
            sababu.append("maneno ya Kiingereza yamebaki: " + ", ".join(bakia))

    if not sababu:
        hali = "pita"
    elif kesi["kategoria"] == "usigusiwe":
        hali = "imeharibiwa"
    else:
        hali = "shindwa"
    return {"hali": hali, "sababu": sababu, "ulinganifu": ulinganifu}


# ------------------------------------------------------------------
# Ripoti
# ------------------------------------------------------------------
def chapisha_ripoti(matokeo: list, jina_la_hali: str):
    print("\n" + "=" * 70)
    print(f"RIPOTI YA UBORA  ({jina_la_hali})")
    print("=" * 70)

    kwa_kategoria = defaultdict(lambda: {"jumla": 0, "pita": 0})
    for m in matokeo:
        k = kwa_kategoria[m["kategoria"]]
        k["jumla"] += 1
        k["pita"] += m["hali"] == "pita"

    print(f"\n{'Kategoria':<16}{'Pita':>6}{'Jumla':>7}{'Asilimia':>10}")
    for jina, k in sorted(kwa_kategoria.items()):
        print(f"{jina:<16}{k['pita']:>6}{k['jumla']:>7}{100 * k['pita'] / k['jumla']:>9.0f}%")

    jumla = len(matokeo)
    pita = sum(m["hali"] == "pita" for m in matokeo)
    zimeharibiwa = [m for m in matokeo if m["hali"] == "imeharibiwa"]
    hakuna = [m for m in matokeo if m["hali"] == "hakuna_jibu"]
    nyakati = [m["sekunde"] for m in matokeo if m.get("sekunde") is not None]

    print(f"\nJUMLA: {pita}/{jumla} ({100 * pita / max(jumla, 1):.0f}%)")
    print(f"Sentensi sahihi zilizoharibiwa (regression): {len(zimeharibiwa)}")
    print(f"Kesi zisizo na jibu (API imeshindwa): {len(hakuna)}")
    if nyakati:
        print(f"Wastani wa muda: {sum(nyakati) / len(nyakati):.1f}s kwa kesi (juu zaidi: {max(nyakati):.1f}s)")

    shindwa = [m for m in matokeo if m["hali"] != "pita"]
    if shindwa:
        print("\n--- KESI ZILIZOSHINDWA ---")
        for m in shindwa:
            alama = "!!" if m["hali"] == "imeharibiwa" else "xx"
            print(f"\n[{alama}] {m['id']}  ({m['hali']})")
            print(f"  ingizo     : {m['ingizo']!r}")
            if m.get("inatarajiwa") is not None:
                print(f"  inatarajiwa: {m['inatarajiwa']!r}")
            print(f"  ilipatikana: {m.get('jibu')!r}")
            print(f"  sababu     : {'; '.join(m['sababu'])}")
    return pita / max(jumla, 1), len(zimeharibiwa)


def linganisha(faili_a: str, faili_b: str):
    a = {m["id"]: m for m in json.load(open(faili_a, encoding="utf-8"))["matokeo"]}
    b = {m["id"]: m for m in json.load(open(faili_b, encoding="utf-8"))["matokeo"]}
    imeboreka, imeharibika = [], []
    for id_ in sorted(set(a) & set(b)):
        if a[id_]["hali"] != "pita" and b[id_]["hali"] == "pita":
            imeboreka.append(id_)
        elif a[id_]["hali"] == "pita" and b[id_]["hali"] != "pita":
            imeharibika.append(id_)
    pa = sum(m["hali"] == "pita" for m in a.values())
    pb = sum(m["hali"] == "pita" for m in b.values())
    print(f"A: {pa}/{len(a)} pita   |   B: {pb}/{len(b)} pita")
    print(f"\nZilizoboreka ({len(imeboreka)}): {', '.join(imeboreka) or '-'}")
    print(f"Zilizoharibika ({len(imeharibika)}): {', '.join(imeharibika) or '-'}")
    return 1 if imeharibika else 0


# ------------------------------------------------------------------
# Mwanzo
# ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Pima ubora wa AI Lingual Africa Sanifu")
    ap.add_argument("--url", help="Anwani ya seva (mf. https://jina.onrender.com au http://localhost:10000)")
    ap.add_argument("--chujio-tu", action="store_true", help="Pima chujio la Python pekee (bila AI, bila mtandao)")
    ap.add_argument("--seti", default=SETI_YA_KAWAIDA, help="Njia ya faili ya JSON ya majaribio")
    ap.add_argument("--kategoria", help="Pima kategoria moja tu (mf. ngeli, tahajia, usigusiwe, istilahi)")
    ap.add_argument("--pumzika", type=float, default=0.5, help="Sekunde za kusubiri kati ya maombi (kuepuka kikomo cha API)")
    ap.add_argument("--muda", type=int, default=120, help="Muda wa juu wa ombi moja (sekunde)")
    ap.add_argument("--hifadhi", help="Faili la kuhifadhi matokeo (chaguo-msingi: tests/matokeo/<tarehe>.json)")
    ap.add_argument("--kizingiti", type=float, default=0.0, help="Kiwango cha chini cha kufaulu (0-1); ukishuka exit code = 1")
    ap.add_argument("--linganisha", nargs=2, metavar=("A", "B"), help="Linganisha faili mbili za matokeo")
    a = ap.parse_args()

    if a.linganisha:
        sys.exit(linganisha(*a.linganisha))

    if not a.url and not a.chujio_tu:
        ap.error("Weka --url ya seva yako, au tumia --chujio-tu.")

    seti = json.load(open(a.seti, encoding="utf-8"))
    visa = seti["visa"]
    if a.kategoria:
        visa = [k for k in visa if k["kategoria"] == a.kategoria]
    if a.chujio_tu:
        visa = [k for k in visa if k.get("chujio_peke")]
    if not visa:
        print("Hakuna kesi zilizochaguliwa.")
        sys.exit(2)

    mod = pakia_api_server() if a.chujio_tu else None
    ufunguo = os.environ.get("API_KEY", "")
    matokeo = []
    print(f"Inapima kesi {len(visa)} ...")
    for i, kesi in enumerate(visa, 1):
        if a.chujio_tu:
            jibu, sekunde = chujio_nje_ya_mtandao(kesi["ingizo"], mod), 0.0
        else:
            data, sekunde = ita_api(a.url, kesi, ufunguo, a.muda)
            jibu = data.get("matokeo") if data.get("ok") else None
            if jibu is None:
                print(f"  ! {kesi['id']}: {data.get('error', 'hakuna jibu')}")
            time.sleep(a.pumzika)
        t = tathmini(kesi, jibu)
        matokeo.append({
            "id": kesi["id"], "kategoria": kesi["kategoria"], "aina": kesi["aina"],
            "ingizo": kesi["ingizo"], "inatarajiwa": kesi.get("inatarajiwa"),
            "jibu": jibu, "sekunde": round(sekunde, 2), **t,
        })
        print(f"  [{i:>2}/{len(visa)}] {'OK ' if t['hali'] == 'pita' else 'XX '} {kesi['id']}")

    hali = "chujio la Python pekee" if a.chujio_tu else f"seva: {a.url}"
    kiwango, zimeharibiwa = chapisha_ripoti(matokeo, hali)

    os.makedirs(FOLDA_YA_MATOKEO, exist_ok=True)
    njia = a.hifadhi or os.path.join(FOLDA_YA_MATOKEO, datetime.now().strftime("%Y%m%d_%H%M%S") + (".chujio" if a.chujio_tu else "") + ".json")
    json.dump({"wakati": datetime.now().isoformat(), "hali": hali, "kiwango": kiwango, "matokeo": matokeo},
              open(njia, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nMatokeo yamehifadhiwa: {njia}")

    sys.exit(1 if (zimeharibiwa > 0 or kiwango < a.kizingiti) else 0)


if __name__ == "__main__":
    main()
