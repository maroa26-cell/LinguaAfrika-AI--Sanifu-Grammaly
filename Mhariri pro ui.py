"""
mhariri_pro_ui.py - Kiolesura cha Streamlit cha Mhariri Pro v3.

Matumizi kwenye app.py:
    import mhariri_pro_ui
    r = mhariri_pro_ui.onyesha_mhariri_pro(
        kamusi=KAMUSI_SET, piga_ai=_piga_ai,
        piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
        max_chars=MAX_CHARS, kikomo_maneno=maneno_yaliyobaki,
    )
    if r and r.get("ai_imetumika") and r["text_hash"] != st.session_state.get("mhariri_billed_hash"):
        st.session_state["freemium_words_used"] += r["maneno"]
        st.session_state["mhariri_billed_hash"] = r["text_hash"]
        onyesha_rada()
"""

import hashlib
import re

import streamlit as st

import mhariri_pro as mp

MAELEZO_YA_RANGI = ("🟥 Tahajia &nbsp; 🟧 Sarufi &nbsp; 🟪 Uakifishaji &nbsp; 🟩 Mtindo "
                    "— elea juu ya neno lililopakwa rangi kuona sababu.")


def _futa_chaguo_za_zamani():
    for k in [k for k in st.session_state
              if k.startswith("pro_chagua_") or k.startswith("pro_mbadala_")]:
        del st.session_state[k]


def onyesha_mhariri_pro(kamusi=None, piga_ai=None, piga_ai_kina=None,
                        max_chars=None, kikomo_maneno=None):
    """Onyesha UI. Hurudisha bill dict au None."""
    st.subheader("Mhariri wa Kiswahili Sanifu Pro")

    maandishi = st.text_area("Andika au bandika maandishi ya Kiswahili",
                             height=220, key="pro_maandishi", max_chars=max_chars)
    kutumia_ai = st.checkbox(
        "Mkaguzi wa AI (hukamata tahajia na makosa ambayo kanuni hazioni)",
        value=True, key="pro_ai",
        help="Bila hii, ni kanuni za Sanifu pekee zinazokagua: haraka, lakini hazioni tahajia.",
    )

    hesabu = len(re.findall(r"\w+", maandishi or ""))
    kikomo = kikomo_maneno if kikomo_maneno is not None else 10**9
    zidi = hesabu > kikomo
    if zidi:
        st.warning(f"Maandishi yana maneno {hesabu}, lakini salio lako ni {kikomo}. "
                   "Punguza maandishi au fungua Lango la Mteja.")

    if st.button("Chambua", type="primary", key="pro_chambua", disabled=zidi):
        if not maandishi.strip():
            st.warning("Andika au bandika maandishi kwanza.")
        else:
            with st.spinner("Inachambua..."):
                _futa_chaguo_za_zamani()
                st.session_state.pop("pro_matokeo", None)
                try:
                    r = mp.chambua(
                        maandishi, kamusi=kamusi, kutumia_ai=kutumia_ai,
                        piga_ai=piga_ai, piga_ai_kina=piga_ai_kina,
                    )
                    st.session_state["pro_matokeo"] = {"maandishi": maandishi, "r": r}
                except Exception as e:
                    st.error(f"Hitilafu ya uchambuzi: {type(e).__name__}: {e}")

    hali = st.session_state.get("pro_matokeo")
    if not hali:
        return None

    maandishi, r = hali["maandishi"], hali["r"]
    masuala = r["masuala"]

    cols = st.columns(5)
    cols[0].metric("Alama (makadirio)", f"{r['alama']}/100")
    for c, kundi in zip(cols[1:], mp.KUNDI):
        c.metric(kundi, r["idadi_kwa_kundi"][kundi])
    for t in r["tahadhari"]:
        st.caption(f"ℹ️ {t}")
    if r.get("kina_imetumika"):
        st.caption("🔍 Uthibitisho wa Pro umefanyika.")
        if r.get("yaliyokataliwa"):
            with st.expander(f"Mapendekezo {len(r['yaliyokataliwa'])} yaliyokataliwa na Pro"):
                for k in r["yaliyokataliwa"][:10]:
                    st.write(f"- «{k['kabla']}» → «{k['baada']}»: {k['sababu']}")

    bill = {
        "maneno": r["maneno"],
        "text_hash": hashlib.sha256(maandishi.encode("utf-8")).hexdigest(),
        "alama": r["alama"],
        "masuala_idadi": len(masuala),
        "ai_imetumika": r.get("ai_imetumika", False),
    }

    if not masuala:
        st.success("Hakuna makosa yaliyoonekana. Kumbuka: ukaguzi huu haoni kila aina ya kosa.")
        st.code(maandishi, language=None)
        return bill

    st.markdown(MAELEZO_YA_RANGI, unsafe_allow_html=True)
    st.markdown(mp.onyesha_kwa_rangi(maandishi, masuala), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ Chagua zote", key="pro_all"):
            for m in masuala:
                if m["inaweza_kutumika"]:
                    st.session_state[f"pro_chagua_{m['id']}"] = True
            st.rerun()
    with col_b:
        if st.button("❌ Ondoa zote", key="pro_none"):
            for m in masuala:
                if m["inaweza_kutumika"]:
                    st.session_state[f"pro_chagua_{m['id']}"] = False
            st.rerun()

    st.markdown("**Chagua marekebisho ya kutumia:**")
    chaguliwa, mbadala = set(), {}
    for m in masuala:
        ufunguo = f"pro_chagua_{m['id']}"
        if not m["inaweza_kutumika"]:
            st.markdown(f"ℹ️ **{m['kundi']}**: «{m['kabla']}» — {m['sababu']}")
            continue
        st.session_state.setdefault(ufunguo, m["imechaguliwa_awali"])
        baada = m["baada"] if m["baada"] != "" else "(ondoa)"
        tahadhari_ya_uhakika = " ⚠️ pendekezo la makadirio" if m["uhakika"] == "wastani" else ""
        if st.checkbox(
            f"**{m['kundi']}**: «{m['kabla']}» → «{baada}» — {m['sababu']}{tahadhari_ya_uhakika}",
            key=ufunguo,
        ):
            chaguliwa.add(m["id"])
        if len(m["chaguo"]) > 1:
            mbadala[m["id"]] = st.selectbox(
                "Chaguo la marekebisho", range(len(m["chaguo"])),
                format_func=lambda i, m=m: m["chaguo"][i] or "(ondoa)",
                key=f"pro_mbadala_{m['id']}",
            )

    st.markdown("**Maandishi yaliyosahihishwa** (bonyeza ikoni ya kunakili):")
    st.code(mp.tumia_marekebisho(maandishi, masuala, chaguliwa, mbadala), language=None)

    return bill
   
