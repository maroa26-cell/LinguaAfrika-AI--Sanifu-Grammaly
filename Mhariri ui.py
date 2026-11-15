
"""
mhariri_ui.py - Sehemu ya Streamlit ya Mhariri wa lugha nyingi (AI Lingual Africa).

Matumizi kwenye app.py / mhariri live:
    from mhariri_ui import onyesha_mhariri
    onyesha_mhariri(kamusi=KAMUSI_SET)

Mtumiaji huchagua "Lugha ya maandishi" na "Hariri kwenda lugha". Zikiwa sawa, maandishi huhaririwa tu;
zikitofautiana, hutafsiriwa na kuhaririwa. Lugha isiyo kwenye orodha huandikwa kwa jina lake.
"""

import html

import streamlit as st

from lugha_za_afrika import KISWAHILI, ni_kiswahili, orodha_ya_lugha, pata_lugha
from sanifu_editor import hariri_kwa_ubora

LUGHA_NYINGINE = "Lugha nyingine…"

MAELEZO_YA_ALAMA = {
    "kanuni_za_kiswahili": "Alama inatokana na kanuni za sarufi ya Kiswahili (ngeli, Yambiwa, alama za uandishi n.k.).",
    "uaminifu_tu": ("Alama hapa inapima uaminifu tu (namba, urefu, kutotafsiriwa); haipimi sarufi ya lugha hii. "
                    "Washa 'Mkaguzi wa AI' kwenye chaguo za juu ili sarufi nayo ikaguliwe."),
    "uaminifu_na_ai": "Alama inatokana na ukaguzi wa uaminifu na mkaguzi wa AI; si uhakika kamili wa sarufi.",
}


def _badilisha_lugha():
    """Kitufe cha ⇄: kubadilishana lugha mbili (pamoja na majina ya lugha maalum)."""
    s = st.session_state
    for ufunguo, msingi in (("", KISWAHILI), ("_maalum", "")):
        a = s.get("lugha_chanzo" + ufunguo, msingi)
        b = s.get("lugha_lengwa" + ufunguo, msingi)
        s["lugha_chanzo" + ufunguo], s["lugha_lengwa" + ufunguo] = b, a


def _chagua_lugha(kichwa, ufunguo, chaguo_msingi):
    orodha = orodha_ya_lugha() + [LUGHA_NYINGINE]
    st.session_state.setdefault(ufunguo, chaguo_msingi)
    chaguo = st.selectbox(kichwa, orodha, key=ufunguo)
    if chaguo == LUGHA_NYINGINE:
        jina = st.text_input("Andika jina la lugha", key=ufunguo + "_maalum",
                             placeholder="mfano: Wolof, Kiswati, Tshiluba")
        return (jina or "").strip() or None
    return chaguo


HALI_ZA_UI = {
    "bure": "Bure: Groq anatafsiri, Gemini anahariri",
    "gemini_pekee": "Gemini pekee: ukaguzi mara mbili",
    "kawaida": "Kawaida: Gemini, kisha Groq, kisha OpenAI (akiba)",
}
ONYO_LA_FARAGHA = ("Kiwango cha bure cha Gemini kinaweza kutumia maandishi unayotuma kuboresha bidhaa za Google, "
                   "na wakaguzi wa binadamu wanaweza kuyasoma. Usitume majina wala taarifa za wagonjwa.")


def onyesha_mhariri(kamusi=None, majaribio_ya_juu=3, hali_ya_msingi="bure"):
    st.subheader("Mhariri wa Lugha Zote")

    c1, c2, c3 = st.columns([5, 1, 5])
    with c1:
        lugha_chanzo = _chagua_lugha("Lugha ya maandishi yako", "lugha_chanzo", KISWAHILI)
    with c2:
        st.write("")
        st.write("")
        st.button("⇄", on_click=_badilisha_lugha, help="Badilishana lugha")
    with c3:
        lugha_lengwa = _chagua_lugha("Hariri kwenda lugha", "lugha_lengwa", KISWAHILI)

    if lugha_chanzo and lugha_lengwa:
        if lugha_chanzo.lower() == lugha_lengwa.lower():
            st.caption("Lugha ni zilezile: maandishi yatahaririwa tu (tahajia, sarufi, mpangilio na alama).")
        else:
            st.caption(f"Maandishi ya {lugha_chanzo} yatatafsiriwa kwenda {lugha_lengwa} na kuhaririwa.")

    with st.expander("Chaguo za juu"):
        hali_ya_ai = st.selectbox("Mpangilio wa AI", list(HALI_ZA_UI), format_func=lambda k: HALI_ZA_UI[k],
                                  index=list(HALI_ZA_UI).index(hali_ya_msingi), key="hali_ya_ai")
        if hali_ya_ai != "kawaida":
            st.caption("ℹ️ " + ONYO_LA_FARAGHA)
        lengo = st.slider("Lengo la ubora (rudia kuhariri hadi alama ifike)", 60, 100, 90)
        majaribio = st.slider("Idadi ya juu ya majaribio", 1, 4, majaribio_ya_juu)
        mkaguzi = st.checkbox(
            "Mkaguzi wa AI (polepole kidogo, gharama zaidi)",
            value=False,
            help="Hukagua sarufi ya lugha zisizo Kiswahili kwa kutumia AI ya pili. Bila hii, alama ya lugha hizo "
                 "inapima uaminifu tu.",
        )
        safisha = st.checkbox("Safisha chanzo cha Kiswahili kwanza (kwa kanuni za Sanifu)", value=True)

    maandishi = st.text_area("Maandishi", height=220, key="maandishi_ya_kuhariri")

    if st.button("Hariri", type="primary"):
        if not maandishi.strip():
            st.warning("Andika au bandika maandishi kwanza.")
            return
        if not lugha_chanzo or not lugha_lengwa:
            st.warning("Chagua lugha zote mbili (au andika jina la lugha).")
            return
        with st.spinner("Inahariri..."):
            try:
                st.session_state["matokeo_ya_mhariri"] = hariri_kwa_ubora(
                    maandishi, kamusi=kamusi, lengo=lengo, majaribio_ya_juu=majaribio,
                    lugha_chanzo=lugha_chanzo, lugha_lengwa=lugha_lengwa,
                    mkaguzi_wa_ai=mkaguzi, hariri_chanzo_kwanza=safisha, hali=hali_ya_ai,
                )
            except Exception as e:
                st.session_state.pop("matokeo_ya_mhariri", None)
                st.error(f"Imeshindikana kuhariri: {e}")
                return

    r = st.session_state.get("matokeo_ya_mhariri")
    if not r:
        return

    st.markdown(f"**Matokeo ({r['lugha_lengwa']})**")
    if r["mwelekeo"] == "rtl":
        st.markdown(
            f'<div dir="rtl" style="white-space:pre-wrap;font-size:1.1rem">{html.escape(r["maandishi_sahihi"])}</div>',
            unsafe_allow_html=True,
        )
    st.code(r["maandishi_sahihi"], language=None)   # ikoni ya kunakili

    m1, m2 = st.columns(2)
    m1.metric("Ubora wa matokeo", f"{r['alama_ya_matokeo']}/100")
    if r["alama"] is not None:
        m2.metric("Ubora wa maandishi ya kuingiza", f"{r['alama']}/100")
    st.caption(MAELEZO_YA_ALAMA[r["aina_ya_alama"]] + f" Majaribio: {r['majaribio']}.")
    if r.get("mtoa_wa_rasimu"):
        st.caption(f"Mtafsiri: {r['mtoa_wa_rasimu']} → Mhariri mkuu: {r['mtoa_huduma']}")
    elif r.get("hali") and r["hali"] != "kawaida":
        st.caption(f"Mhariri: {r['mtoa_huduma']}")

    if r["onyo_la_lugha"]:
        st.warning(r["onyo_la_lugha"])
    if not r["lengo_limefikiwa"] and r["makosa_yaliyobaki"]:
        st.warning("Alama haikufikia lengo. Makosa yaliyobaki:")
        for k in r["makosa_yaliyobaki"]:
            st.write(f"- {k.get('aina', '')}: {k.get('kabla', '')} {('→ ' + k['baada']) if k.get('baada') else ''} "
                     f"({k.get('sababu', '')})")
    for t in r["tahadhari"]:
        st.caption(f"ℹ️ {t}")

    if r["chanzo_kilichohaririwa"]:
        with st.expander("Chanzo cha Kiswahili kilichosafishwa kabla ya kutafsiri"):
            st.write(r["chanzo_kilichohaririwa"])
    if r["marekebisho"]:
        with st.expander(f"Marekebisho ({len(r['marekebisho'])})"):
            for k in r["marekebisho"]:
                st.markdown(f"- **{k.get('aina', '')}**: {k.get('kabla', '')} → {k.get('baada', '')}. "
                            f"{k.get('sababu', '')}")
