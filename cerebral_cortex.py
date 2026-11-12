"""
cerebral_cortex.py — Moduli ya ukurasa wa Kiswahili Sanifu.
Inatumiwa na app.py kama sehemu ya mfumo wa kurasa nyingi (multi-page).
"""

import os
from typing import Dict, Any, Optional
import streamlit as st

# Moduli ya sarufi
from kanuni_ya_sarufi import (
    KanuniZaSarufiKiswahili,
    MAELEKEZO_YA_LUGHA,
    KIKOMO_CHA_SAUTI_MB,
    KIKOMO_CHA_HERUFI_ZA_SAUTI,
)

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
    kwa_aina: Dict[str, list] = {}
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
            st.markdown(f"{i}. ~~`{m['kutoka']}`~~ → **`{m['kwenda']}`**")
    else:
        st.info("Hakuna mabadiliko yaliyohitajika.")


# ============================================================
# CLASS KUU (Inayotumiwa na app.py)
# ============================================================
class CerebralCortex:
    def __init__(self):
        # Anzisha injini ya sarufi
        self.kanuni = KanuniZaSarufiKiswahili()

    def render(self) -> None:
        """Hii ndiyo inayotengeneza UI ya ukurasa huu."""
        
        # Kumbuka: st.set_page_config() imeondolewa hapa kwa sababu
        # app.py yako ina uwezekano mkubwa imeshaweka.

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
                key="cerebral_lugha"
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
                key="cerebral_sentensi_input",
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
                    st.text_area("Maudhui ya faili:", maudhui, height=150, disabled=True)

        # ---- Ukaguzi ----
        if sentensi and sentensi.strip():
            if kagua_btn:
                with st.spinner("Inakagua..."):
                    matokeo = self.kanuni.kagua_sentensi_nzima(sentensi)
                onyesha_matokeo(matokeo)

            if rekebisha_btn:
                with st.spinner("Inarekebisha..."):
                    matokeo = self.kanuni.kagua_na_kurekebisha(sentensi)
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
                if st.button(mfano, key=f"cerebral_mfano_{hash(mfano)}"):
                    st.session_state["cerebral_sentensi_input"] = mfano
                    st.rerun()

    def run(self) -> None:
        """Alias ya render() ikiwa app.py inaita run() badala ya render()."""
        self.render()
