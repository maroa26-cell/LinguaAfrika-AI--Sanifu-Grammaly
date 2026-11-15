"""
mhariri_pro_ui.py - Kiolesura cha Streamlit cha Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode).

Matumizi kwenye app.py:
    from mhariri_pro_ui import onyesha_mhariri_pro
    onyesha_mhariri_pro(kamusi=KAMUSI_SET)

Mtiririko: andika maandishi -> Chambua -> makosa yanaangaziwa kwa rangi -> mtumiaji anachagua
yapi yatumike (na chaguo mbadala pale zipo) -> maandishi yaliyosahihishwa yanaonekana mara moja.
"""

import streamlit as st

import mhariri_pro as mp

MAELEZO_YA_RANGI = ("🟥 Tahajia &nbsp; 🟧 Sarufi &nbsp; 🟪 Uakifishaji &nbsp; 🟩 Mtindo "
                    "— elea juu ya neno lililopakwa rangi kuona sababu.")


def _futa_chaguo_za_zamani():
    for k in [k for k in st.session_state if k.startswith("pro_chagua_") or k.startswith("pro_mbadala_")]:
        del st.session_state[k]


def onyesha_mhariri_pro(kamusi=None):
    st.subheader("Mhariri wa Kiswahili Sanifu Pro")

    maandishi = st.text_area("Andika au bandika maandishi ya Kiswahili", height=220, key="pro_maandishi")
    kutumia_ai = st.checkbox(
        "Mkaguzi wa AI (hukamata tahajia na makosa ambayo kanuni hazioni)", value=True, key="pro_ai",
        help="Bila hii, ni kanuni za Sanifu pekee zinazokagua: haraka na bila gharama, lakini hazioni makosa ya tahajia.",
    )

    if st.button("Chambua", type="primary", key="pro_chambua"):
        if not maandishi.strip():
            st.warning("Andika au bandika maandishi kwanza.")
            return
        with st.spinner("Inachambua..."):
            _futa_chaguo_za_zamani()
            st.session_state["pro_matokeo"] = {
                "maandishi": maandishi,
                "r": mp.chambua(maandishi, kamusi=kamusi, kutumia_ai=kutumia_ai),
            }

    hali = st.session_state.get("pro_matokeo")
    if not hali:
        return
    maandishi, r = hali["maandishi"], hali["r"]
    masuala = r["masuala"]

    cols = st.columns(5)
    cols[0].metric("Alama (makadirio)", f"{r['alama']}/100")
    for c, kundi in zip(cols[1:], mp.KUNDI):
        c.metric(kundi, r["idadi_kwa_kundi"][kundi])
    for t in r["tahadhari"]:
        st.caption(f"ℹ️ {t}")

    if not masuala:
        st.success("Hakuna makosa yaliyoonekana. Kumbuka: ukaguzi huu haoni kila aina ya kosa.")
        st.code(maandishi, language=None)
        return

    st.markdown(MAELEZO_YA_RANGI, unsafe_allow_html=True)
    st.markdown(mp.onyesha_kwa_rangi(maandishi, masuala), unsafe_allow_html=True)

    st.markdown("**Chagua marekebisho ya kutumia:**")
    chaguliwa, mbadala = set(), {}
    for m in masuala:
        ufunguo = f"pro_chagua_{m['id']}"
        if not m["inaweza_kutumika"]:
            st.markdown(f"ℹ️ **{m['kundi']}**: «{m['kabla']}» — {m['sababu']}")
            continue
        st.session_state.setdefault(ufunguo, m["imechaguliwa_awali"])
        baada = m["baada"] if m["baada"] != "" else "(ondoa)"
        alama_ya_tahadhari = " ⚠️ pendekezo la makadirio" if m["uhakika"] == "wastani" else ""
        if st.checkbox(f"**{m['kundi']}**: «{m['kabla']}» → «{baada}» — {m['sababu']}{alama_ya_tahadhari}",
                       key=ufunguo):
            chaguliwa.add(m["id"])
        if len(m["chaguo"]) > 1:
            mbadala[m["id"]] = st.selectbox(
                "Chaguo la marekebisho", range(len(m["chaguo"])),
                format_func=lambda i, m=m: m["chaguo"][i] or "(ondoa)",
                key=f"pro_mbadala_{m['id']}",
            )

    st.markdown("**Maandishi yaliyosahihishwa** (bonyeza ikoni ya kunakili):")
    st.code(mp.tumia_marekebisho(maandishi, masuala, chaguliwa, mbadala), language=None)
