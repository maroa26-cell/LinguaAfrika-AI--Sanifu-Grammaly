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

Kumbuka: ukaguzi huu hautumii salio la maneno la mtumiaji.
"""

import hashlib
import json
import re

import streamlit as st

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


def kagua_mara_ya_pili(chanzo, matokeo, aina="tafsiri", lugha="Kiswahili",
                       piga_ai=None, piga_ai_kina=None):
    """
    Hurudisha dict: {"sawa": True|False|None, "matatizo": [...], "toleo_sahihi": str,
                     "ai_imetumika": bool, "kosa": str|None}
    sawa=None humaanisha ukaguzi umeshindikana (hakuna jibu la AI).
    """
    matatizo_ndani, rekebishwa = [], matokeo
    if lugha == "Kiswahili":
        matatizo_ndani, rekebishwa = _tumia_kanuni_za_ndani(matokeo)

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


def _tumia_toleo(ufunguo_toleo, maandishi):
    st.session_state[ufunguo_toleo] = maandishi


def onyesha_ukaguzi_wa_pili(chanzo, matokeo, aina="tafsiri", lugha="Kiswahili",
                            piga_ai=None, piga_ai_kina=None,
                            ufunguo="ukp", auto_awali=False):
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
                                      piga_ai=piga_ai, piga_ai_kina=piga_ai_kina)
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
            nakili = True
        else:
            st.warning(f"⚠️ Matatizo {len(d['matatizo'])} yamepatikana:")
            for t in d["matatizo"]:
                aina_t = _ep_md(t.get("aina", "tatizo"))
                st.markdown(f"- **{aina_t}**: \"{_ep_md(t.get('lilipo', ''))}\" → "
                            f"\"{_ep_md(t.get('pendekezo', ''))}\". {_ep_md(t.get('sababu', ''))}")
            st.button("✔ Tumia toleo lililosahihishwa", type="primary", key=k("tumia"),
                      on_click=_tumia_toleo, args=(k("toleo"), d["toleo_sahihi"]))
            nakili = st.checkbox("Nakili bila kurekebisha", key=k("ruka"))

    if nakili:
        st.markdown("**Maandishi ya mwisho** (bonyeza ikoni ya kunakili):")
        st.code(toleo, language=None)
    return toleo
