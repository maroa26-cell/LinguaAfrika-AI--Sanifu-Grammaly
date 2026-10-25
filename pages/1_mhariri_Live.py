
"""Mhariri wa Kiswahili wa moja kwa moja (mtindo wa Grammarly).

Kihariri kiko kwenye components/live_editor/index.html. Makosa ya kanuni huonekana papo hapo ndani ya
kivinjari; ukiacha kuandika kwa sekunde ~1, maandishi hutumwa hapa kwa ukaguzi wa AI.
"""
import os
import sys

import streamlit as st
from openai import OpenAI

# Faili hili liko kwenye pages/, hivyo ongeza mzizi wa repo kwenye sys.path ili
# `import mhariri` na `from cerebral_cortex import ...` vifanye kazi.
MZIZI_WA_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if MZIZI_WA_REPO not in sys.path:
    sys.path.insert(0, MZIZI_WA_REPO)

import mhariri
from cerebral_cortex import CerebralCortex

st.set_page_config(page_title="Mhariri wa Moja kwa Moja", page_icon="\u270D\uFE0F", layout="wide")

KIKOMO_CHA_HERUFI = 3000
KIKOMO_CHA_MAOMBI = 60  # ukaguzi wa AI kwa kila session, kudhibiti gharama


def _siri(jina):
    if os.environ.get(jina):
        return os.environ[jina]
    try:
        return st.secrets.get(jina)
    except Exception:
        return None


funguo = str(_siri("OPENAI_API_KEY") or "").strip()
if not funguo:
    st.error("OPENAI_API_KEY haipo kwenye Secrets.")
    st.stop()


@st.cache_resource
def _ubongo():
    return CerebralCortex(OpenAI(api_key=funguo))


def _matatizo_ya_ai(maandishi):
    # Bila @st.cache_data: cache ya Streamlit ni ya mchakato mzima na hushirikiwa na
    # kila session, hivyo maandishi ya mtumiaji mmoja yangehifadhiwa na kuonekana kwa
    # watumiaji wengine. Kila session hukagua maandishi yake yenyewe; ukaguzi huu
    # huitwa mara moja tu kwa kila mabadiliko ya maandishi (tazama ulinzi hapa chini).
    return mhariri.ukaguzi_wa_ai(maandishi, _ubongo().piga_json)


st.title("\u270D\uFE0F Mhariri wa Kiswahili wa Moja kwa Moja")
st.caption("Andika, na makosa yataonekana yakiwa yamepigiwa mstari. Bonyeza neno lenye mstari kuona pendekezo. "
           "Baada ya kusimama kuandika kwa sekunde moja, maandishi hutumwa kwa OpenAI kwa ukaguzi wa sarufi.")

s = st.session_state
s.setdefault("ai_issues", [])
s.setdefault("ai_text", "")
s.setdefault("ai_error", "")
s.setdefault("ai_calls", 0)

# Kijenzi kinatanganzwa kwenye live_editor_component.py (module halisi); hapa tunakiingiza tu.
from live_editor_component import kijenzi_cha_mhariri as _kijenzi_cha_mhariri

thamani = _kijenzi_cha_mhariri(
    ai_issues=s["ai_issues"], ai_text=s["ai_text"], ai_error=s["ai_error"], key="mhariri_live", default=None
)

if thamani and thamani.get("text") and thamani["text"] != s["ai_text"]:
    maandishi = thamani["text"]
    if s["ai_calls"] >= KIKOMO_CHA_MAOMBI:
        s["ai_text"], s["ai_issues"] = maandishi, []
        s["ai_error"] = "Kikomo cha ukaguzi wa AI kwa session hii kimefikiwa. Ukaguzi wa msingi unaendelea."
    else:
        s["ai_calls"] += 1
        try:
            s["ai_issues"] = _matatizo_ya_ai(maandishi[:KIKOMO_CHA_HERUFI])
            s["ai_error"] = "" if len(maandishi) <= KIKOMO_CHA_HERUFI else f"AI imekagua herufi {KIKOMO_CHA_HERUFI} za kwanza tu."
        except Exception as e:
            print(f"[mhariri_live] {type(e).__name__}: {e}")
            s["ai_issues"] = []
            s["ai_error"] = "AI haipatikani kwa sasa; ukaguzi wa msingi unaendelea."
        s["ai_text"] = maandishi
    st.rerun()

st.caption(f"Maombi ya AI yaliyotumika kwenye session hii: {s['ai_calls']}/{KIKOMO_CHA_MAOMBI}")
