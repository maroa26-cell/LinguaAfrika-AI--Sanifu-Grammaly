"""Live Editor: mhariri wa moja kwa moja (mtindo wa Grammarly) kwa lugha zote zilizoorodheshwa.

Kihariri kiko kwenye components/live_editor/index.html. Mtumiaji huchagua lugha ya kuhariri:
- Kiswahili: makosa ya kanuni (majina, tahajia, alama) huonekana papo hapo ndani ya kivinjari.
- Lugha nyingine: ukaguzi wa jumla papo hapo (mf. nafasi nyingi); sarufi na tahajia hukaguliwa na AI.
Ukiacha kuandika kwa sekunde ~1, maandishi hutumwa hapa kwa ukaguzi wa AI wa lugha husika.
Mhariri Pro kwenye app.py unabaki Kiswahili pekee.
"""
import os

import streamlit as st
from openai import OpenAI

import mhariri
import mhariri_ui
from cerebral_cortex import CerebralCortex
from lugha_za_afrika import ni_kiswahili, onyo_la_lugha, pata_lugha

st.set_page_config(page_title="Live Editor", page_icon="\u270D\uFE0F", layout="wide")

from live_editor_component import kijenzi  # noqa: E402  (lazima ije baada ya set_page_config)

KIKOMO_CHA_HERUFI = 3000
KIKOMO_CHA_MAOMBI = 60  # ukaguzi wa AI kwa kila session (lugha zote), kudhibiti gharama


def _siri(jina):
    if os.environ.get(jina):
        return os.environ[jina]
    try:
        return st.secrets.get(jina)
    except Exception:
        return None


@st.cache_resource
def _ubongo():
    ufunguo = str(_siri("OPENAI_API_KEY") or "").strip()
    return CerebralCortex(OpenAI(api_key=ufunguo) if ufunguo else None)   # mnyororo: Gemini -> Groq -> OpenAI


ubongo = _ubongo()
if not (ubongo.gemini_client or ubongo.groq_client or ubongo.openai_client):
    st.error("Hakuna ufunguo wa AI uliowekwa. Weka GEMINI_API_KEY, GROQ_API_KEY au OPENAI_API_KEY kwenye Secrets.")
    st.stop()

kina = ubongo.piga_json_kina if getattr(ubongo, "gemini_pro_modeli", "") else None


@st.cache_data(ttl=3600, show_spinner=False)
def _matatizo_ya_ai(maandishi, lugha):
    """Ukaguzi wa AI wa lugha husika. Hitilafu hazihifadhiwi kwenye cache; ni mafanikio tu."""
    t = mhariri.ukaguzi_wa_ai(maandishi, ubongo.piga_json, 0, lugha)
    if kina:                                    # uthibitisho wa Pro (hiari); id za muda tu kwa uthibitisho
        kopi = [dict(x, id=n) for n, x in enumerate(t)]
        try:
            bora, _ = mhariri.thibitisha_na_kina(maandishi, kopi, kina, lugha)
            salama = {x["id"] for x in bora}
            return [x for n, x in enumerate(t) if n in salama]
        except Exception:
            pass                                # Pro imeshindwa: tumia kichujio cha uhakika hapa chini
    return [x for x in t if x.get("uhakika") != "chini"]


st.title("\u270D\uFE0F Live Editor")

lugha = mhariri_ui.chagua_lugha_ya_kuhariri()
if not lugha:
    st.info("Andika jina la lugha kwanza.")
    st.stop()
info = pata_lugha(lugha)
jina = info["jina"]
if onyo_la_lugha(jina):
    st.warning(onyo_la_lugha(jina))

if ni_kiswahili(jina):
    st.caption("Andika, na makosa yataonekana yakiwa yamepigiwa mstari. Bonyeza neno lenye mstari kuona pendekezo. "
               "Baada ya kusimama kuandika kwa sekunde moja, maandishi hutumwa kwa AI kwa ukaguzi wa sarufi.")
else:
    st.caption(f"Andika kwa {jina}. Makosa ya sarufi na tahajia hukaguliwa na AI baada ya kusimama kuandika kwa "
               "sekunde moja; mistari ya papo hapo ni ya jumla tu (mf. nafasi nyingi).")

s = st.session_state
s.setdefault("ai_issues", [])
s.setdefault("ai_text", "")
s.setdefault("ai_lugha", "")
s.setdefault("ai_error", "")
s.setdefault("ai_calls", 0)

thamani = kijenzi(ai_issues=s["ai_issues"], ai_text=s["ai_text"], ai_error=s["ai_error"], ai_lugha=s["ai_lugha"],
                  lugha=jina, msimbo=info["msimbo"], mwelekeo=info["mwelekeo"], kanuni_sw=ni_kiswahili(jina),
                  key="mhariri_live", default=None)

# Jibu la zamani la kijenzi (lugha tofauti na iliyochaguliwa sasa) linapuuzwa; kijenzi hutuma maandishi upya lugha ikibadilika.
lugha_ya_thamani = (thamani or {}).get("lugha", "Kiswahili")
if (thamani and thamani.get("text") and lugha_ya_thamani == jina
        and (thamani["text"], lugha_ya_thamani) != (s["ai_text"], s["ai_lugha"])):
    maandishi = thamani["text"]
    if s["ai_calls"] >= KIKOMO_CHA_MAOMBI:
        s["ai_text"], s["ai_lugha"], s["ai_issues"] = maandishi, jina, []
        s["ai_error"] = "Kikomo cha ukaguzi wa AI kwa session hii kimefikiwa. Ukaguzi wa msingi unaendelea."
    else:
        s["ai_calls"] += 1
        try:
            s["ai_issues"] = _matatizo_ya_ai(maandishi[:KIKOMO_CHA_HERUFI], jina)
            s["ai_error"] = "" if len(maandishi) <= KIKOMO_CHA_HERUFI else f"AI imekagua herufi {KIKOMO_CHA_HERUFI} za kwanza tu."
        except Exception as e:
            print(f"[live_editor] {type(e).__name__}: {e}")
            s["ai_issues"] = []
            s["ai_error"] = "AI haipatikani kwa sasa; ukaguzi wa msingi unaendelea."
        s["ai_text"], s["ai_lugha"] = maandishi, jina
    st.rerun()

st.caption(f"Maombi ya AI yaliyotumika kwenye session hii: {s['ai_calls']}/{KIKOMO_CHA_MAOMBI}")
