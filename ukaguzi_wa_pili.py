"""
ukaguzi_wa_pili.py - Ukaguzi wa pili wa tafsiri na uhariri (muundo na sarufi).

Hufanyika BAADA ya tafsiri/uhariri kukamilika na mtumiaji kuchagua matokeo,
na KABLA mwenye ujumbe hajanakili maandishi.

Matumizi:
    import ukaguzi_wa_pili
    mwisho = ukaguzi_wa_pili.onyesha_ukaguzi_wa_pili(
        chanzo=maandishi_asili, matokeo=tafsiri, aina="tafsiri",
        lugha="Kiswahili", piga_ai=_piga_ai, piga_ai_kina=_piga_ai_kina,
        ufunguo="tafsiri", auto_awali=True)

Kumbuka: ukaguzi wa pili HAUTOZWI salio la maneno la mtumiaji.

Kwa aina="tafsiri", ikiwa ukaguzi_wa_tafsiri.py ipo kwenye folda moja, hutumika kulinganisha
CHANZO na TAFSIRI (nambari, viungo, majina, aya, istilahi + AI). Isipokuwepo, ukaguzi wa
jumla wa muundo na sarufi (ulio ndani ya faili hili) hutumika.
"""

import hashlib
import json
import re

import streamlit as st

try:
    import ukaguzi_wa_tafsiri as _uwt
except Exception as _e:  # faili halipo au lina hitilafu: tumia ukaguzi wa jumla
    _uwt = None
    print(f"[ukaguzi_wa_pili] ukaguzi_wa_tafsiri haujapakiwa: {type(_e).__name__}: {_e}")

# Majina ya lugha (kama kwenye app.py) -> misimbo
_MISIMBO_YA_LUGHA = {
    "Kiswahili": "sw", "Kiingereza (English)": "en", "Kiingereza": "en", "Kifaransa": "fr",
    "Kiarabu": "ar", "Kichina (Mandarin)": "zh", "Kichina": "zh",
    "Kireno (Portugu\u00eas)": "pt", "Kireno": "pt", "Kizulu (isiZulu)": "zu",
    "Setswana (Botswana)": "tn", "Kinyarwanda": "rw", "Kiganda (Luganda)": "lg",
    "Lingala": "ln", "Kichewa": "ny",
}

# ---------------------------------------------------------------------------
# Kanuni za ndani (hazihitaji AI): ngeli na maneno yanayojirudia kwenye makosa
# ---------------------------------------------------------------------------
_KANUNI_ZA_NDANI = [
    (re.compile(r"(?<!akina )\b(mama|baba)\s+wengi\b", re.IGNORECASE),
     r"akina \1 wengi", "sarufi",
     'Tumia "akina mama wengi" / "akina baba wengi".'),
    (re.compile(r"\bakina\s+watoto\b", re.IGNORECASE),
     "watoto", "sarufi",
     '"watoto" ni wingi tayari; usiseme "akina watoto".'),
    (re.compile(r"\b(wakati|muda)\s+mingi\b", re.IGNORECASE),
     r"\1 mwingi", "sarufi",
     'Ngeli sahihi ni "wakati mwingi" / "muda mwingi".'),
]


def _tumia_kanuni_za_ndani(maandishi):
    """Hurudisha (orodha_ya_matatizo, maandishi_yaliyorekebishwa)."""
    matatizo = []
    sasa = maandishi
    for muundo, badala, aina, sababu in _KANUNI_ZA_NDANI:
        for m in muundo.finditer(sasa):
            matatizo.append({
                "aina": aina,
                "lilipo": m.group(0),
                "pendekezo": muundo.sub(badala, m.group(0)),
                "sababu": sababu,
                "chanzo": "kanuni",
            })
        sasa = muundo.sub(badala, sasa)
    return matatizo, sasa


# ---------------------------------------------------------------------------
# Maelekezo kwa AI
# ---------------------------------------------------------------------------
_MAELEKEZO_MSINGI = """Wewe ni mkaguzi mkuu wa pili wa lugha. Umepewa MAANDISHI YA CHANZO na MATOKEO
(tafsiri au toleo lililohaririwa). Kagua MATOKEO tu, kwa mambo haya:
1. MUUNDO: mpangilio wa sentensi, aya, vichwa, orodha na alama za uandishi uwe kama chanzo;
   hakuna sehemu iliyorukwa, kurudiwa au kuongezwa (maandishi yakamilike bila mapengo).
2. SARUFI: upatanisho wa ngeli na viambishi, nyakati, tahajia, mpangilio wa maneno.
3. UAMINIFU: maana ya chanzo isipotee, isiongezwe wala kupunguzwa.
4. Kusiwe na maneno ya lugha nyingine yaliyochanganywa (code-switching), isipokuwa majina maalum.
{kanuni_za_lugha}
Usibadilishe maneno au mtindo usio na kosa. Rekebisha kwa kiwango kidogo kinachohitajika tu.
Jibu JSON tu, bila maelezo mengine wala alama za ```:
{{"sawa": true|false,
 "matatizo": [{{"aina": "muundo|sarufi|maana", "lilipo": "...", "pendekezo": "...", "sababu": "..."}}],
 "toleo_sahihi": "MATOKEO YOTE yaliyosahihishwa"}}
Kama hakuna tatizo: {{"sawa": true, "matatizo": [], "toleo_sahihi": "<matokeo yaleyale>"}}"""

_KANUNI_ZA_KISWAHILI = (
    'Kanuni maalum za Kiswahili: "akina mama wengi", "akina baba wengi" (si "mama wengi"); '
    '"watoto wengi" (si "akina watoto"); "wakati mwingi", "muda mwingi" (si "wakati mingi").'
)


def _kama_dict(jibu):
    """Pokea jibu la AI (dict au maandishi ya JSON) na urudishe dict."""
    if isinstance(jibu, dict):
        return jibu
    t = re.sub(r"```(?:json)?", "", str(jibu or "")).strip()
    a, b = t.find("{"), t.rfind("}")
    if a == -1 or b <= a:
        raise ValueError("Jibu la AI halina JSON.")
    return json.loads(t[a:b + 1])


def _ita_ai_ya_moduli(piga_ai, piga_ai_kina):
    """Badilisha piga_ai(mfumo, ujumbe) iwe ita_ai(system, ujumbe) -> (maandishi, injini)."""
    def ita(mfumo, ujumbe):
        for piga in [p for p in (piga_ai_kina, piga_ai) if p]:
            try:
                jibu = piga(mfumo, ujumbe)
                if isinstance(jibu, (dict, list)):
                    jibu = json.dumps(jibu, ensure_ascii=False)
                return str(jibu or ""), "ubongo"
            except Exception as e:  # jaribu mkaguzi anayefuata
                print(f"[ukaguzi_wa_pili] ita_ai imeshindwa: {type(e).__name__}: {e}")
        return "", None
    return ita


def _tumia_mapendekezo(maandishi, matatizo):
    """Weka mapendekezo yenye nafasi (start/end) kwenye maandishi, bila kuvuka mipaka."""
    wagombea = sorted(
        (x for x in matatizo
         if x.get("start") is not None and x.get("end") is not None and x.get("suggestion")
         and maandishi[x["start"]:x["end"]] == x.get("original")),
        key=lambda x: x["start"])
    chaguliwa, mwisho = [], -1
    for x in wagombea:
        if x["start"] >= mwisho:
            chaguliwa.append(x)
            mwisho = x["end"]
    for x in reversed(chaguliwa):
        maandishi = maandishi[:x["start"]] + x["suggestion"] + maandishi[x["end"]:]
    return maandishi


def _kwa_muundo_wa_ukaguzi(x):
    return {
        "aina": x.get("lebo") or x.get("aina") or "tatizo",
        "lilipo": x.get("original") or x.get("chanzo_kipande") or "",
        "pendekezo": x.get("suggestion") or "",
        "sababu": x.get("maelezo") or "",
        "ukali": x.get("ukali") or "kati",
        "chanzo": x.get("na") or "kanuni",
    }


def _kagua_tafsiri_kwa_moduli(chanzo, matokeo, lugha, lugha_chanzo,
                              piga_ai, piga_ai_kina, matatizo_ndani, rekebishwa):
    r = _uwt.kagua_tafsiri(
        chanzo, matokeo, _ita_ai_ya_moduli(piga_ai, piga_ai_kina),
        lugha_chanzo=_MISIMBO_YA_LUGHA.get(lugha_chanzo or "", "en"),
        lugha_lengwa=_MISIMBO_YA_LUGHA.get(lugha, "sw"),
        max_workers=1)   # mfululizo: salama zaidi ndani ya Streamlit

    toleo = _tumia_mapendekezo(matokeo, r["matatizo"])
    if lugha == "Kiswahili":
        toleo = _tumia_kanuni_za_ndani(toleo)[1]

    ndani = {x["lilipo"].lower() for x in matatizo_ndani}
    yote = list(matatizo_ndani) + [
        t for t in map(_kwa_muundo_wa_ukaguzi, r["matatizo"]) if t["lilipo"].lower() not in ndani]
    makubwa = [t for t in yote if t.get("ukali") != "chini"]
    madogo = [t for t in yote if t.get("ukali") == "chini"]

    ai_ilifanya = r.get("ai") is True
    ripoti = {
        "matatizo": yote if makubwa else [],
        "maelezo_madogo": madogo if not makubwa else [],
        "toleo_sahihi": toleo if makubwa else matokeo,
        "alama": r.get("alama"), "hukumu": r.get("hukumu"),
        "ukaguzi_umekatwa": r.get("ukaguzi_umekatwa", False),
        "ai_imetumika": ai_ilifanya, "kosa": None,
    }
    if makubwa:
        ripoti["sawa"] = False
    elif ai_ilifanya:
        ripoti["sawa"] = True
    else:   # AI imeshindwa na kanuni za msingi hazikuona kitu: usitoe uhakika wa uongo
        ripoti["sawa"] = None
        ripoti["kosa"] = "AI haikupatikana; kanuni za msingi tu ndizo zilizokagua."
    return ripoti


def kagua_mara_ya_pili(chanzo, matokeo, aina="tafsiri", lugha="Kiswahili",
                       piga_ai=None, piga_ai_kina=None, lugha_chanzo=None):
    """
    Hurudisha dict: {"sawa": True|False|None, "matatizo": [...], "toleo_sahihi": str,
                     "ai_imetumika": bool, "kosa": str|None}
    sawa=None humaanisha ukaguzi umeshindikana (hakuna jibu la AI).
    """
    matatizo_ndani, rekebishwa = [], matokeo
    if lugha == "Kiswahili":
        matatizo_ndani, rekebishwa = _tumia_kanuni_za_ndani(matokeo)

    if aina == "tafsiri" and _uwt is not None and (piga_ai or piga_ai_kina):
        try:
            return _kagua_tafsiri_kwa_moduli(chanzo, matokeo, lugha, lugha_chanzo,
                                             piga_ai, piga_ai_kina, matatizo_ndani, rekebishwa)
        except Exception as e:  # moduli ikishindwa, tumia ukaguzi wa jumla hapa chini
            print(f"[ukaguzi_wa_pili] ukaguzi_wa_tafsiri umeshindwa: {type(e).__name__}: {e}")

    mfumo = _MAELEKEZO_MSINGI.format(
        kanuni_za_lugha=(_KANUNI_ZA_KISWAHILI if lugha == "Kiswahili"
                         else f"Kagua kwa kanuni sanifu za lugha ya {lugha}."))
    ujumbe = (f"AINA: {aina}\nLUGHA YA MATOKEO: {lugha}\n\n"
              f"MAANDISHI YA CHANZO:\n{chanzo}\n\nMATOKEO:\n{matokeo}")

    data, kosa = None, None
    for piga in [p for p in (piga_ai_kina, piga_ai) if p]:
        try:
            data = _kama_dict(piga(mfumo, ujumbe))
            break
        except Exception as e:  # jaribu mkaguzi anayefuata
            kosa = f"{type(e).__name__}: {e}"
            print(f"[ukaguzi_wa_pili] imeshindwa: {kosa}")

    if data is None:
        if matatizo_ndani:
            return {"sawa": False, "matatizo": matatizo_ndani, "toleo_sahihi": rekebishwa,
                    "ai_imetumika": False, "kosa": None}
        return {"sawa": None, "matatizo": [], "toleo_sahihi": matokeo,
                "ai_imetumika": False, "kosa": kosa or "AI haikupatikana"}

    matatizo_ai = [t for t in (data.get("matatizo") or []) if isinstance(t, dict)]
    toleo = str(data.get("toleo_sahihi") or "").strip() or rekebishwa
    if lugha == "Kiswahili":
        toleo = _tumia_kanuni_za_ndani(toleo)[1]

    # Kinga: ikiwa toleo la AI limepungua au kuongezeka sana, usilitumie
    if len(toleo) < 0.5 * len(matokeo) or len(toleo) > 2 * len(matokeo) + 20:
        toleo = rekebishwa

    matatizo = matatizo_ndani + matatizo_ai
    return {
        "sawa": not matatizo,
        "matatizo": matatizo,
        "toleo_sahihi": toleo if matatizo else matokeo,
        "ai_imetumika": True,
        "kosa": None,
    }


# ---------------------------------------------------------------------------
# Kiolesura cha Streamlit
# ---------------------------------------------------------------------------
def _hash(*vipande):
    return hashlib.sha256("\x1f".join(str(v) for v in vipande).encode("utf-8")).hexdigest()


def _ep_md(t):
    return re.sub(r"([\\`*_{}\[\]()#+\-.!~|>$])", r"\\\1", str(t))


def _onyesha_tatizo(t):
    aina_t = _ep_md(t.get("aina", "tatizo"))
    lilipo, pendekezo = _ep_md(t.get("lilipo", "")), _ep_md(t.get("pendekezo", ""))
    kati = f"\"{lilipo}\" → \"{pendekezo}\"" if lilipo and pendekezo else (
        f"\"{lilipo}\"" if lilipo else "")
    st.markdown(f"- **{aina_t}**: {kati}. {_ep_md(t.get('sababu', ''))}".replace(": . ", ": "))


def _tumia_toleo(ufunguo_toleo, maandishi):
    st.session_state[ufunguo_toleo] = maandishi


def onyesha_ukaguzi_wa_pili(chanzo, matokeo, aina="tafsiri", lugha="Kiswahili",
                            piga_ai=None, piga_ai_kina=None,
                            ufunguo="ukp", auto_awali=False, lugha_chanzo=None):
    """
    Onyesha sehemu ya ukaguzi wa pili na kisanduku cha kunakili.
    Kisanduku cha kunakili kinaonekana tu baada ya ukaguzi kukamilika,
    au mtumiaji akichagua kuruka, au ukaguzi ukizimwa.
    Hurudisha maandishi ya sasa ya mwisho (yanayoweza kuwa yamesahihishwa).
    """
    def k(s):
        return f"ukp_{ufunguo}_{s}"

    msingi = _hash(chanzo, matokeo, aina, lugha)
    if st.session_state.get(k("msingi")) != msingi:
        for s in ("toleo", "ripoti", "ruka"):
            st.session_state.pop(k(s), None)
        st.session_state[k("msingi")] = msingi
    toleo = st.session_state.get(k("toleo"), matokeo)

    st.markdown("---")
    st.markdown("**\U0001F50D Ukaguzi wa Pili (muundo na sarufi)**")
    washa = st.checkbox("Washa ukaguzi wa pili kabla ya kunakili", value=True, key=k("washa"))
    if not washa:
        st.markdown("**Maandishi ya mwisho** (bonyeza ikoni ya kunakili):")
        st.code(toleo, language=None)
        return toleo

    auto = st.checkbox("Kagua moja kwa moja", value=auto_awali, key=k("auto"))
    h = _hash(chanzo, toleo, aina, lugha)
    ripoti = st.session_state.get(k("ripoti"))
    if ripoti and ripoti["h"] != h:
        ripoti = None
    bonyeza = st.button("\U0001F50D Kagua Tena", key=k("kagua"))

    if bonyeza or (auto and ripoti is None):
        with st.spinner("Inakagua muundo na sarufi..."):
            data = kagua_mara_ya_pili(chanzo, toleo, aina=aina, lugha=lugha,
                                      piga_ai=piga_ai, piga_ai_kina=piga_ai_kina,
                                      lugha_chanzo=lugha_chanzo)
        ripoti = {"h": h, "data": data}
        st.session_state[k("ripoti")] = ripoti

    nakili = False
    if ripoti is None:
        st.info("Bonyeza «Kagua Tena» kabla ya kunakili maandishi.")
        nakili = st.checkbox("Ruka ukaguzi na nakili moja kwa moja", key=k("ruka"))
    else:
        d = ripoti["data"]
        if d.get("sawa") is None:
            st.warning("Ukaguzi wa pili umeshindikana kwa sasa. Unaweza kunakili bila ukaguzi "
                       "au ujaribu tena.")
            nakili = True
        elif d["sawa"]:
            st.success("✅ Muundo na sarufi viko sawa.")
            if d.get("hukumu"):
                st.caption(f"{d['hukumu']} (alama {d.get('alama')}/100)")
            if d.get("maelezo_madogo"):
                with st.expander(f"Mambo madogo ya kuzingatia ({len(d['maelezo_madogo'])})"):
                    for t in d["maelezo_madogo"]:
                        _onyesha_tatizo(t)
            nakili = True
        else:
            st.warning(f"⚠️ Matatizo {len(d['matatizo'])} yamepatikana:")
            if d.get("hukumu"):
                st.caption(f"{d['hukumu']} (alama {d.get('alama')}/100)")
            for t in d["matatizo"]:
                _onyesha_tatizo(t)
            st.button("✔ Tumia toleo lililosahihishwa", type="primary", key=k("tumia"),
                      on_click=_tumia_toleo, args=(k("toleo"), d["toleo_sahihi"]))
            nakili = st.checkbox("Nakili bila kurekebisha", key=k("ruka"))

    if ripoti is not None and ripoti["data"].get("ukaguzi_umekatwa"):
        st.caption("Maandishi ni marefu: sehemu ya kwanza tu ndiyo iliyokaguliwa na AI.")
    if nakili:
        st.markdown("**Maandishi ya mwisho** (bonyeza ikoni ya kunakili):")
        st.code(toleo, language=None)
    return toleo
