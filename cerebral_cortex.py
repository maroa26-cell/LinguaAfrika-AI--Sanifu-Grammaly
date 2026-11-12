"""
cerebral_cortex.py — App kuu ya Streamlit kwa AI Lingual – Kiswahili Sanifu.

Toleo 2.0 (lililorekebishwa):
- Inatumia moduli ya kanuni_ya_sarufi.py (Toleo 2.0)
- UI imerekebishwa kuonyesha makosa kama dicts (kosa['ujumbe'],
  kosa['mapendekezo'], kosa['nafasi'])
- Vipengele vipya: kurekebisha sentensi kwa kubonyeza kitufe kimoja,
  kupakia faili, na kuchuja makosa kwa aina
"""

# ============================================================
# IMPORTS
# ============================================================
import os
import re
import json
import tempfile
from typing import Dict, List, Any, Optional

import streamlit as st

# Moduli mpya ya sarufi
from kanuni_ya_sarufi import (
    KanuniZaSarufiKiswahili,
    Kosa,
    MatokeoYaNgeli,
    KitambuziNgeli,
    MkaguziSarufi,
    MBAO_ZA_MAKOSA_YA_PARAMETA,
    KIKOMO_CHA_SAUTI_MB,
    KIKOMO_CHA_HERUFI_ZA_SAUTI,
    MAELEKEZO_YA_LUGHA,
)

# ============================================================
# HELPERS
# ============================================================
def _siri(jina: str) -> Optional[str]:
    """Huchukua siri kutoka environment au st.secrets."""
    if os.environ.get(jina):
        return os.environ[jina]
    try:
        return st.secrets.get(jina) if st else None
    except Exception:
        return None


def onyesha_matokeo(matokeo: Dict[str, Any]) -> None:
    """Huonyesha matokeo ya ukaguzi kwa muundo mzuri."""
    if matokeo["sahihi"]:
        st.success("✅ Sentensi ni sahihi kisarufi. Hongera!")
        return

    st.warning(f"⚠️ Makosa {matokeo['idadi_ya_makosa']} yamepatikana.")

    # Panga makosa kwa aina
    kwa_aina: Dict[str, List[Dict]] = {}
    for kosa in matokeo["makosa"]:
        kwa_aina.setdefault(kosa["aina"], []).append(kosa)

    # Onyesha kwa kila aina
    for aina, makosa in kwa_aina.items():
        rangi = {
            "NGELI": "🔴",
            "KIROBOTI": "🟠",
            "MOFOLOJIA": "🟡",
            "ALAMA": "🔵",
            "TAWALI": "⚪",
        }.get(aina, "⚫")

        st.subheader(f"{rangi} {aina} ({len(makosa)})")

        for kosa in makosa:
            kichwa = f"❌ `{kosa['neno']}` (nafasi {kosa['nafasi']}–{kosa['nafasi'] + kosa['urefu']})"
            with st.expander(kichwa):
                st.write(f"**Ujumbe:** {kosa['ujumbe']}")
                if kosa.get("mapendekezo"):
                    st.write("**Mapendekezo:**")
                    for p in kosa["mapendekezo"]:
                        st.code(p, language="")
                if kosa.get("chanzo"):
                    st.caption(f"Chanzo: {kosa['chanzo']}")


def onyesha_marekebisho(matokeo: Dict[str, Any]) -> None:
    """Huonyesha sentensi iliyorekebishwa na mabadiliko."""
    st.subheader("✏️ Sentensi iliyorekebishwa")
    st.success(matokeo["sentensi_iliyorekebishwa"])

    if matokeo["mabadiliko"]:
        st.subheader(f"Mabadiliko {len(matokeo['mabadiliko'])}")
        for i, m in enumerate(matokeo["mabadiliko"], 1):
            st.markdown(
                f"{i}. ~~`{m['kutoka']}`~~ → **`{m['kwenda']}`**"
            )
    else:
        st.info("Hakuna mabadiliko yaliyohitajika.")


# ============================================================
# UI YA STREAMLIT
# ============================================================
def ukurasa_mkuu() -> None:
    st.set_page_config(
        page_title="AI Lingual – Kiswahili Sanifu",
        page_icon="🗣️",
        layout="wide",
    )

    st.title("🗣️ AI Lingual – Kiswahili Sanifu")
    st.markdown(
        "Ukaguzi wa sarufi ya **Kiswahili Sanifu cha Tanzania (BAKITA)** "
        "kwa ajili ya kamusi ya mtandaoni na mafunzo ya AI."
    )

    # ---- Sidebar ----
    with st.sidebar:
        st.header("⚙️ Mipangilio")
        lugha = st.selectbox(
            "Lugha ya maelekezo",
            list(MAELEKEZO_YA_LUGHA.keys()),
            index=0,
        )
        st.caption(MAELEKEZO_YA_LUGHA[lugha])

        st.divider()
        st.header("📊 Kuhusu")
        st.markdown(
            f"""
            - **Kikomo cha sauti**: {KIKOMO_CHA_SAUTI_MB} MB
            - **Kikomo cha herufi**: {KIKOMO_CHA_HERUFI_ZA_SAUTI}
            - **Ngeli zinazotambulika**: A-WA, KI-VI, U-I, LI-YA, I-ZI
            """
        )

    # ---- Sehemu kuu ----
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Maandishi ya kukagua")
        sentensi = st.text_area(
            "Weka au bandika sentensi ya Kiswahili:",
            height=180,
            placeholder="Mfano: Mtoto mdogo alikula chakula kitamu.",
            key="sentensi_input",
        )

    with col2:
        st.subheader("🎯 Vitendo")
        kagua_btn = st.button(
            "🔍 Kagua Sarufi",
            type="primary",
            use_container_width=True,
        )
        rekebisha_btn = st.button(
            "✏️ Rekebisha",
            use_container_width=True,
        )

    # ---- Kupakia faili ----
    with st.expander("📂 Au pakia faili (.txt)"):
        faili = st.file_uploader(
            "Chagua faili la maandishi",
            type=["txt"],
            help=f"Ukubwa usizidi {KIKOMO_CHA_SAUTI_MB} MB",
        )
        if faili is not None:
            maudhui = faili.read().decode("utf-8", errors="replace")
            if len(maudhui) > KIKOMO_CHA_HERUFI_ZA_SAUTI:
                st.error(
                    f"Faili ni kubwa mno. Kikomo ni {KIKOMO_CHA_HERUFI_ZA_SAUTI} "
                    f"herufi; faili lako lina {len(maudhui)}."
                )
            else:
                sentensi = maudhui
                st.text_area(
                    "Maudhui ya faili:",
                    maudhui,
                    height=150,
                    disabled=True,
                )

    # ---- Ukaguzi ----
    if sentensi and sentensi.strip():
        kanuni = KanuniZaSarufiKiswahili()

        if kagua_btn:
            with st.spinner("Inakagua..."):
                matokeo = kanuni.kagua_sentensi_nzima(sentensi)
            onyesha_matokeo(matokeo)

        if rekebisha_btn:
            with st.spinner("Inarekebisha..."):
                matokeo = kanuni.kagua_na_kurekebisha(sentensi)
            onyesha_marekebisho(matokeo)

    # ---- Mfano wa haraka ----
    with st.expander("💡 Mifano ya haraka"):
        mifano = [
            "Mtoto mdogo alikula chakula kitamu.",
            "Vitabu vizuri viko mezani.",
            "Mimi ni baridi leo asubuhi.",
            "Shule yetu ni nzuri sana.",
            "mtoto alikuja",
        ]
        for mfano in mifano:
            if st.button(mfano, key=f"mfano_{hash(mfano)}"):
                st.session_state["sentensi_input"] = mfano
                st.rerun()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    ukurasa_mkuu()
