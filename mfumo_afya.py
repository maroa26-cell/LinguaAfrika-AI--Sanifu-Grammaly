"""
mfumo_afya.py - Ukaguzi wa afya ya mfumo wa AI Lingual Africa (GitHub <-> Streamlit).

Hii ni toleo salama la `chunguza_na_rekebisha_mifumo_pande_zote`. Tofauti na la zamani:
- HAIBADILISHI majina ya mafaili kimya kimya (hiyo ilivunja `import Style` na seva ya Streamlit Cloud
  mara nyingi haikubali kuandika kwenye repo). Inaripoti tu; kubadilisha majina ni hiari (badilisha_majina=True).
- HAISAFISHI kache kila ukurasa unapopakiwa (ingepunguza kasi sana); inasafisha ukibonyeza kitufe tu.
- Inakagua kama kila moduli inaingizwa na ina kazi zinazotumiwa na mafaili mengine (MKATABA),
  kwa hiyo hitilafu kama "kagua_tafsiri haipo" inaonekana mapema badala ya skrini nyekundu.
- Inafanya ukaguzi mara moja kwa kila kikao; usirudie kila rerun.

Matumizi:
    import mfumo_afya
    mfumo_afya.chunguza_na_rekebisha_mifumo_pande_zote()   # kimya, mwanzoni mwa app.py
    mfumo_afya.onyesha_afya_ya_mfumo()                      # jedwali la hali (kwa msimamizi)
"""

from __future__ import annotations

import importlib
import os
import time

import streamlit as str_platform

# Kila moduli na majina ya kazi/madarasa ambayo mafaili mengine yanayategemea.
MKATABA = {
    "kanuni_ya_sarufi": ["KanuniZaSarufiKiswahili", "MAELEKEZO_YA_LUGHA",
                         "maelekezo_ya_tafsiri", "ni_jozi_ya_kiingereza_kiswahili"],
    "sanifu_editor": ["hariri_kwa_ubora", "tatua_anagram", "piga_ai",
                      "SANIFU_SYSTEM_PROMPT", "hesabu_alama"],
    "lugha_za_afrika": ["KISWAHILI", "orodha_ya_lugha"],
    "mhariri_pro": ["chambua", "tumia_marekebisho", "onyesha_kwa_rangi", "KUNDI"],
    "mhariri_pro_ui": ["onyesha_mhariri_pro"],
    "mhariri_ui": ["onyesha_mhariri"],
}

# Majina ya zamani yenye herufi kubwa yanayojulikana kuleta tatizo kwenye seva ya Linux.
MAJINA_YA_ZAMANI = {"Style.py", "Sauti.py", "Robot.py", "Admin.py"}

_UFUNGUO = "devops_telemetry"


def _hali_ya_awali() -> dict:
    return {
        "github_sync": "🟢 Connected & Validated",
        "streamlit_runtime": "🟢 Secure Nodes Stable",
        "last_healing_action": "None (System Clean)",
        "matatizo": [],
        "moduli": {},
        "imekaguliwa_saa": None,
    }


def _kagua_majina_ya_mafaili(saraka: str, badilisha: bool) -> tuple[list[str], str | None]:
    """Hutafuta mafaili .py yenye herufi kubwa yanayogongana na majina ya moduli."""
    matatizo, hatua = [], None
    inayotarajiwa = {m + ".py" for m in MKATABA}
    try:
        mafaili = os.listdir(saraka)
    except OSError as e:
        return [f"Siwezi kusoma saraka: {type(e).__name__}"], None
    for faili in mafaili:
        if not faili.endswith(".py") or faili == faili.lower():
            continue
        if faili in MAJINA_YA_ZAMANI or faili.lower() in inayotarajiwa:
            if badilisha:
                try:
                    os.rename(os.path.join(saraka, faili), os.path.join(saraka, faili.lower()))
                    hatua = f"🛠️ Jina '{faili}' limebadilishwa kuwa herufi ndogo."
                    continue
                except OSError as e:
                    matatizo.append(f"Imeshindwa kubadilisha '{faili}': {type(e).__name__}")
                    continue
            matatizo.append(f"Faili '{faili}' lina herufi kubwa; ibadilishe kuwa '{faili.lower()}' kwenye GitHub.")
    return matatizo, hatua


def _kagua_moduli() -> tuple[dict, list[str]]:
    """Huingiza kila moduli na kuthibitisha kazi zinazotarajiwa zipo."""
    hali, matatizo = {}, []
    for jina, kazi in MKATABA.items():
        try:
            m = importlib.import_module(jina)
        except ModuleNotFoundError as e:
            hali[jina] = f"🔴 haipo ({e.name})"
            matatizo.append(f"Moduli '{jina}' haipatikani: {e}")
            continue
        except Exception as e:                      # hitilafu ndani ya moduli yenyewe
            hali[jina] = f"🔴 {type(e).__name__}"
            matatizo.append(f"Moduli '{jina}' imeshindwa kuingizwa: {type(e).__name__}: {str(e)[:150]}")
            continue
        pungufu = [k for k in kazi if not hasattr(m, k)]
        if pungufu:
            hali[jina] = "🟠 pungufu: " + ", ".join(pungufu)
            matatizo.append(f"Moduli '{jina}' haina: {', '.join(pungufu)}")
        else:
            hali[jina] = "🟢 sawa"
    # kagua_tafsiri ni darasa-mbinu; ikose, mhariri_pro itashindwa kimya kimya.
    try:
        kn = importlib.import_module("kanuni_ya_sarufi").KanuniZaSarufiKiswahili
        if not hasattr(kn, "kagua_tafsiri"):
            matatizo.append("KanuniZaSarufiKiswahili haina 'kagua_tafsiri' (tumia kanuni_ya_sarufi.py v2.7).")
    except Exception:
        pass
    return hali, matatizo


def safisha_kache() -> str:
    """Husafisha kache za Streamlit (st.cache_data na st.cache_resource)."""
    try:
        str_platform.cache_data.clear()
        str_platform.cache_resource.clear()
        return "🧹 Kache zimesafishwa."
    except Exception as e:
        return f"Kache hazikusafishwa: {type(e).__name__}"


def chunguza_na_rekebisha_mifumo_pande_zote(lazimisha: bool = False,
                                            badilisha_majina: bool = False) -> dict:
    """
    PROPRIOCEPTION ENGINE: BRIDGE MONITOR (toleo salama).
    Hurudisha telemetry dict yenye funguo za zamani (github_sync, streamlit_runtime, last_healing_action)
    pamoja na 'matatizo' na 'moduli'. Hufanya kazi mara moja kwa kikao isipokuwa lazimisha=True.
    """
    ss = str_platform.session_state
    if _UFUNGUO not in ss:
        ss[_UFUNGUO] = _hali_ya_awali()
    t = ss[_UFUNGUO]
    if t.get("imekaguliwa_saa") and not lazimisha:
        return t

    matatizo, hatua = _kagua_majina_ya_mafaili(os.getcwd(), badilisha_majina)
    moduli, matatizo_ya_moduli = _kagua_moduli()
    matatizo += matatizo_ya_moduli

    t["moduli"] = moduli
    t["matatizo"] = matatizo
    t["imekaguliwa_saa"] = time.strftime("%H:%M:%S")
    t["github_sync"] = "🟢 Connected & Validated" if not matatizo else f"🟠 Matatizo {len(matatizo)}"
    t["streamlit_runtime"] = ("🟢 Secure Nodes Stable"
                              if all(v.startswith("🟢") for v in moduli.values()) else "🟠 Moduli zina tatizo")
    if hatua:
        t["last_healing_action"] = hatua
    ss[_UFUNGUO] = t
    return t


def onyesha_afya_ya_mfumo() -> None:
    """Jedwali dogo la hali ya mfumo, vitufe vya kuchunguza upya na kusafisha kache."""
    t = chunguza_na_rekebisha_mifumo_pande_zote()
    c1, c2, c3 = str_platform.columns(3)
    c1.metric("GitHub", t["github_sync"])
    c2.metric("Streamlit", t["streamlit_runtime"])
    c3.metric("Ukaguzi wa mwisho", t.get("imekaguliwa_saa") or "-")
    str_platform.caption(f"Hatua ya mwisho: {t['last_healing_action']}")

    for jina, hali in t.get("moduli", {}).items():
        str_platform.write(f"`{jina}` — {hali}")
    for tatizo in t.get("matatizo", []):
        str_platform.warning(tatizo)

    b1, b2 = str_platform.columns(2)
    if b1.button("🔄 Chunguza upya", key="afya_upya"):
        chunguza_na_rekebisha_mifumo_pande_zote(lazimisha=True)
        str_platform.rerun()
    if b2.button("🧹 Safisha kache", key="afya_kache"):
        t["last_healing_action"] = safisha_kache()
        str_platform.session_state[_UFUNGUO] = t
        str_platform.rerun()
