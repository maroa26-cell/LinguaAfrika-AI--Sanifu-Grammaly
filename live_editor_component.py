"""Tangazo la kijenzi cha kihariri cha moja kwa moja (Streamlit custom component).

Kwa nini faili hili lipo: `declare_component` lazima litangazwe ndani ya module halisi,
yaani module iliyopo kwenye `sys.modules`. Streamlit hukimbiza kurasa zilizo kwenye
`pages/` ndani ya module ya muda ambayo haiwekwi kwenye `sys.modules`; ndani ya mazingira
hayo `declare_component` hushindwa na kutupa:

    RuntimeError: module is None. This should never happen.

Kwa hiyo tangazo hilo limehamishwa hapa, kwenye module ya kawaida ya mzizi wa repo, na
ukurasa `pages/1_mhariri_Live.py` unakiingiza tu kwa:

    from live_editor_component import kijenzi

Faili hili halina siri yoyote.
"""
import os

import streamlit.components.v1 as components

# Mzizi wa repo = folda lenye faili hili (sambamba na app.py).
MZIZI_WA_REPO = os.path.dirname(os.path.abspath(__file__))

# Frontend ya kijenzi iko ndani ya: <mzizi>/components/live_editor/
# (folda hili lenye index.html / build lazima liwe-commit kwenye GitHub.)
NJIA_YA_KIJENZI = os.path.join(MZIZI_WA_REPO, "components", "live_editor")

kijenzi = components.declare_component(
    "lingual_live_editor",
    path=NJIA_YA_KIJENZI,
)

# Jina mbadala kwa upatanifu wa nyuma (kama sehemu nyingine bado zinatumia jina refu).
kijenzi_cha_mhariri = kijenzi
