"""Tangazo la kijenzi cha kihariri cha moja kwa moja (Streamlit custom component).

Kwa nini faili hili lipo: `declare_component` lazima litangazwe ndani ya module halisi,
yaani module iliyopo kwenye `sys.modules`. Streamlit 1.66 hukimbiza kurasa zilizo kwenye
`pages/` ndani ya module ya muda ambayo haiwekwi kwenye `sys.modules`; ndani ya mazingira
hayo `declare_component` hushindwa na kutupa:

    RuntimeError: module is None. This should never happen.

Kwa hiyo tangazo hilo limehamishwa hapa, kwenye module ya kawaida ya mzizi wa repo, na
ukurasa `pages/1_mhariri_Live.py` unakiingiza tu kwa `from live_editor_component import
kijenzi_cha_mhariri`. Faili hili halina siri yoyote.
"""
import os

import streamlit.components.v1 as components

MZIZI_WA_REPO = os.path.dirname(os.path.abspath(__file__))
NJIA_YA_COMPONENT = os.path.join(MZIZI_WA_REPO, "components", "live_editor")

kijenzi_cha_mhariri = components.declare_component("lingual_live_editor", path=NJIA_YA_COMPONENT)

