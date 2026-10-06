import streamlit as str_platform
import time

def chochea_mshipa_wa_fahamu(idara_name):
    """7) NERVOUS SYSTEM: Inatuma pigo la umeme kwenye idara kwa kasi ya radi"""
    if "neural_latencies" not in str_platform.session_state:
        str_platform.session_state["neural_latencies"] = {}
    str_platform.session_state["neural_latencies"][idara_name] = time.time()

def kagua_kasi_ya_ubongo(idara_name):
    """Kupima kasi ya mawasiliano kutoka kwenye Ubongo kwenda kwenye viungo"""
    if "neural_latencies" in str_platform.session_state and idara_name in str_platform.session_state["neural_latencies"]:
        muda_mwanzo = str_platform.session_state["neural_latencies"][idara_name]
        kasi = (time.time() - muda_mwanzo) * 1000
        return f"⚡ Synapse Latency kwenda {idara_name}: {kasi:.2f}ms (Radi)"
    return "⚡ Synapse State: Salama"
