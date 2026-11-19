
 """
mhariri_mkuu.py - Mlango mmoja wa Mhariri wa AI Lingual Africa Sanifu.

Unaunganisha:
  - mhariri_ui.py       (Mhariri wa Lugha Zote: tafsiri + uhariri)
  - mhariri_pro_ui.py   (Mhariri Pro: makosa yaliyopakwa rangi, chagua marekebisho)
  - mfumo_afya.py       (ukaguzi wa moduli, GitHub/Streamlit)

Kila kichupo kinalindwa: hitilafu ya moduli moja haiangushi ukurasa mzima, inaonyesha ujumbe wa wazi.

Matumizi kwenye app.py:
    import mhariri_mkuu
    bill = mhariri_mkuu.onyesha_mhariri_kuu(
        kamusi=KAMUSI_SET, piga_ai=_piga_ai,
        piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
        max_chars=MAX_CHARS, kikomo_maneno=maneno_yaliyobaki,
    )
    if bill and bill.get("ai_imetumika") and bill["text_hash"] != st.session_state.get("mhariri_billed_hash"):
        st.session_state["freemium_words_used"] += bill["maneno"]
        st.session_state["mhariri_billed_hash"] = bill["text_hash"]
        onyesha_rada()
"""

from __future__ import annotations

import importlib

import streamlit as st

import mfumo_afya


def _ingiza(jina: str):
    """Huingiza moduli; hurudisha (moduli, ujumbe_wa_kosa)."""
    try:
        return importlib.import_module(jina), None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def _kichupo_chenye_ulinzi(jina_la_moduli: str, jina_la_kazi: str, **vigezo):
    """Huita kazi ya UI ndani ya try/except ili skrini nyekundu isitokee."""
    moduli, kosa = _ingiza(jina_la_moduli)
    if moduli is None:
        st.error(f"Kichupo hiki hakipatikani: `{jina_la_moduli}` ({kosa}). Angalia kichupo cha Afya ya Mfumo.")
        return None
    kazi = getattr(moduli, jina_la_kazi, None)
    if kazi is None:
        st.error(f"`{jina_la_moduli}` haina `{jina_la_kazi}`. Angalia toleo la faili kwenye GitHub.")
        return None
    try:
        return kazi(**vigezo)
    except Exception as e:
        st.error(f"Hitilafu kwenye `{jina_la_moduli}`: {type(e).__name__}: {str(e)[:200]}")
        return None


def onyesha_mhariri_kuu(kamusi=None, piga_ai=None, piga_ai_kina=None,
                        max_chars=None, kikomo_maneno=None,
                        majaribio_ya_juu=3, hali_ya_msingi="bure",
                        onyesha_afya=True):
    """
    Huonyesha vichupo vitatu. Hurudisha 'bill' ya Mhariri Pro (au None) ili app.py ihesabu maneno.
    onyesha_afya=False huficha kichupo cha afya (mfano kwa watumiaji wa kawaida; onyesha kwa msimamizi tu).
    """
    mfumo_afya.chunguza_na_rekebisha_mifumo_pande_zote()      # kimya, mara moja kwa kikao

    majina = ["✍️ Mhariri wa Lugha Zote", "🔎 Mhariri Pro"]
    if onyesha_afya:
        majina.append("🩺 Afya ya Mfumo")
    vichupo = st.tabs(majina)

    bill = None
    with vichupo[0]:
        _kichupo_chenye_ulinzi("mhariri_ui", "onyesha_mhariri", kamusi=kamusi,
                               majaribio_ya_juu=majaribio_ya_juu, hali_ya_msingi=hali_ya_msingi)
    with vichupo[1]:
        bill = _kichupo_chenye_ulinzi(
            "mhariri_pro_ui", "onyesha_mhariri_pro", kamusi=kamusi, piga_ai=piga_ai,
            piga_ai_kina=piga_ai_kina, max_chars=max_chars, kikomo_maneno=kikomo_maneno)
    if onyesha_afya:
        with vichupo[2]:
            try:
                mfumo_afya.onyesha_afya_ya_mfumo()
            except Exception as e:
                st.error(f"Ukaguzi wa afya umeshindwa: {type(e).__name__}: {str(e)[:200]}")
    return bill   
