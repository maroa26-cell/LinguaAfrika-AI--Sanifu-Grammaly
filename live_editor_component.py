"""Kijenzi cha mhariri wa moja kwa moja.

declare_component lazima itangazwe kwenye module halisi: Streamlit 1.66 hukimbiza
kurasa za pages/ ndani ya module ya muda isiyo kwenye sys.modules, hivyo kuitangaza
ndani ya ukurasa hutoa RuntimeError "module is None. This should never happen."
"""
import os

import streamlit.components.v1 as components

MZIZI_WA_REPO = os.path.dirname(os.path.abspath(__file__))
NJIA_YA_COMPONENT = os.path.join(MZIZI_WA_REPO, "components", "live_editor")

kijenzi_cha_mhariri = components.declare_component(
    "lingual_live_editor", path=NJIA_YA_COMPONENT
)
