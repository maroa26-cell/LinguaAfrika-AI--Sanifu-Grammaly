"""
mhariri_ui.py - Sehemu ya Streamlit ya Mhariri wa lugha nyingi (AI Lingual Africa).

Matumizi kwenye app.py / mhariri live:
    from mhariri_ui import onyesha_mhariri
    onyesha_mhariri(kamusi=KAMUSI_SET)

Mtumiaji huchagua "Lugha ya maandishi" na "Hariri kwenda lugha". Zikiwa sawa, maandishi huhaririwa tu;
zikitofautiana, hutafsiriwa na kuhaririwa. Lugha isiyo kwenye orodha huandikwa kwa jina lake.
"""

import collections
import html
import re

import streamlit as st

import mhariri
from lugha_za_afrika import KISWAHILI, ni_kiswahili, onyo_la_lugha, orodha_ya_lugha, pata_lugha
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


def onyesha_mhariri(kamusi=None, majaribio_ya_juu=3):
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
                    mkaguzi_wa_ai=mkaguzi, hariri_chanzo_kwanza=safisha,
                )
            except Exception as e:
                st.session_state.pop("matokeo_ya_mhariri", None)
                st.error(f"Imeshindikana kuhariri: {e}")
                return

    r = st.session_state.get("matokeo_ya_mhariri")
    if r:
        _onyesha_matokeo_ya_hariri(r)


def _onyesha_matokeo_ya_hariri(r):

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


# ----------------------------------------------------------------------------
# LIVE EDITOR: kuhariri na kukagua maandishi ya lugha yoyote iliyoorodheshwa
# ----------------------------------------------------------------------------

def _md(t):
    """Epuka alama za markdown ndani ya maandishi ya mtumiaji."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!~|>$])", r"\\\1", str(t))


def _onyesha_ukaguzi(m):
    """Matokeo ya ukaguzi (mhariri.kagua) kwa lugha yoyote, yenye chaguo za kukubali kila marekebisho."""
    text, matatizo = m["text"], m["issues"]
    st.markdown("---")
    if m.get("onyo_la_lugha"):
        st.warning(m["onyo_la_lugha"])
    if not m["ai_imetumika"]:
        st.info("Ukaguzi wa msingi tu (AI haipatikani kwa sasa). Salio lako halikukatwa.")
    if not matatizo:
        st.success("✅ Hakuna makosa yaliyoonekana kwenye maandishi haya.")
        return
    idadi = collections.Counter(x["category"] for x in matatizo)
    safu = st.columns(len(mhariri.KATEGORIA) + 1)
    safu[0].metric("Alama (makadirio)", f"{mhariri.alama(text, len(matatizo))}/100")
    for n, (kat, (jina, _)) in enumerate(mhariri.KATEGORIA.items(), 1):
        safu[n].metric(jina, idadi.get(kat, 0))
    st.caption("Maandishi yaliyokaguliwa. Elea juu ya sehemu iliyoalamishwa kuona maelezo.")
    st.markdown(mhariri.html_ya_kuonyesha(text, matatizo, rtl=(m.get("mwelekeo") == "rtl")), unsafe_allow_html=True)
    st.markdown("**Chagua marekebisho ya kutumia:**")
    chaguliwa = set()
    for x in matatizo:
        jina = mhariri.KATEGORIA.get(x["category"], ("Mengineyo", ""))[0]
        lebo = f'{jina}: "{_md(x["original"])}" → "{_md(x["suggestion"])}". {_md(x["explanation"])}'
        if st.checkbox(lebo, value=True, key=f"lv_{x['id']}"):
            chaguliwa.add(x["id"])
    st.markdown("**Maandishi yaliyosahihishwa** (bonyeza ikoni ya kunakili):")
    st.code(mhariri.tumia_marekebisho(text, matatizo, chaguliwa), language=None)


def _futa_chaguo_za_zamani():
    for k in [k for k in list(st.session_state.keys()) if str(k).startswith("lv_")]:
        del st.session_state[k]


def onyesha_live_editor(piga_ai, piga_ai_kina=None, kamusi=None, ruhusu=None, tumia=None, max_chars=5000):
    """
    Live Editor: mtumiaji huchagua lugha ya kuhariri, kisha anakagua makosa (Grammarly) au anahariri kiotomatiki.
    Kiswahili hutumia kanuni zako zote; lugha nyingine hutumia ukaguzi wa jumla na AI yenye maelekezo ya lugha hiyo.

    piga_ai(mfumo, mtumiaji)      - kazi ya AI ya haraka (mf. ubongo.piga_json)
    piga_ai_kina                  - hiari: uthibitisho wa Gemini Pro
    ruhusu(maneno) -> str | None  - hiari: ujumbe wa kosa kama salio halitoshi (None = endelea)
    tumia(maneno)                 - hiari: kata maneno kwenye salio baada ya AI kutumika
    """
    st.subheader("Live Editor")
    st.caption("Chagua lugha ya kuhariri, andika au bandika maandishi, kisha ukague au uhariri kiotomatiki.")
    lugha = _chagua_lugha("Lugha ya kuhariri", "live_lugha", KISWAHILI)
    if not lugha:
        st.info("Andika jina la lugha kwanza.")
        return
    info = pata_lugha(lugha)
    jina_la_lugha = info["jina"]
    if onyo_la_lugha(jina_la_lugha):
        st.warning(onyo_la_lugha(jina_la_lugha))

    maandishi = st.text_area("Maandishi", height=220, key="live_maandishi", max_chars=max_chars)
    kiotomatiki = st.checkbox(
        "Kagua kiotomatiki ninapomaliza kuandika (Ctrl+Enter au bonyeza nje ya kisanduku)",
        value=False, key="live_kiotomatiki",
        help="Kila ukaguzi hutumia AI na hukata maneno kwenye salio lako.")
    with st.expander("Chaguo za juu (Hariri kiotomatiki)"):
        lengo = st.slider("Lengo la ubora", 60, 100, 90, key="live_lengo")
        majaribio = st.slider("Idadi ya juu ya majaribio", 1, 4, 3, key="live_majaribio")
        mkaguzi = False
        if not ni_kiswahili(jina_la_lugha):
            mkaguzi = st.checkbox("Mkaguzi wa AI (polepole kidogo, gharama zaidi)", value=False, key="live_mkaguzi",
                                  help="Hukagua sarufi ya lugha hii kwa AI ya pili.")

    c1, c2 = st.columns(2)
    kagua = c1.button("Kagua makosa", type="primary", key="live_kagua")
    hariri = c2.button("Hariri kiotomatiki", key="live_hariri_btn")
    maneno = len(maandishi.split())

    def kuruhusiwa():
        if not maandishi.strip():
            st.warning("Andika au bandika maandishi kwanza.")
            return False
        kosa = ruhusu(maneno) if ruhusu else None
        if kosa:
            st.warning(kosa)
            return False
        return True

    ishara = (jina_la_lugha, maandishi)
    if kagua or (kiotomatiki and maandishi.strip() and st.session_state.get("live_ishara") != ishara):
        st.session_state["live_ishara"] = ishara
        if kuruhusiwa():
            with st.spinner("Nakagua maandishi..."):
                try:
                    m = mhariri.kagua(maandishi, piga_ai=piga_ai, piga_ai_kina=piga_ai_kina, lugha=jina_la_lugha)
                except Exception as e:
                    m = None
                    st.error(f"Ukaguzi umeshindikana: {e}")
            if m:
                if m["ai_imetumika"] and tumia:
                    tumia(maneno)
                _futa_chaguo_za_zamani()
                st.session_state["live_ukaguzi"] = {"text": maandishi, **m}
    if hariri and kuruhusiwa():
        with st.spinner("Inahariri..."):
            try:
                r = hariri_kwa_ubora(maandishi, kamusi=kamusi, lengo=lengo, majaribio_ya_juu=majaribio,
                                     lugha_chanzo=jina_la_lugha, lugha_lengwa=jina_la_lugha,
                                     mkaguzi_wa_ai=mkaguzi, hariri_chanzo_kwanza=False)
            except Exception as e:
                r = None
                st.session_state.pop("live_hariri", None)
                st.error(f"Imeshindikana kuhariri: {e}")
        if r:
            if tumia:
                tumia(maneno)
            st.session_state["live_hariri"] = r

    m = st.session_state.get("live_ukaguzi")
    if m and m.get("lugha") == jina_la_lugha:
        _onyesha_ukaguzi(m)
    r = st.session_state.get("live_hariri")
    if r and r.get("lugha_lengwa") == jina_la_lugha:
        st.markdown("---")
        _onyesha_matokeo_ya_hariri(r)
