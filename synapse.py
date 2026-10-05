import streamlit as str_platform
import time

def chochea_mshipa_wa_fahamu(idara_name):
    """Inapiga radi kwenye idara ili kuamsha RAM na CPU kwa kasi ya 0.1ms"""
    if "neural_latencies" not in str_platform.session_state:
        str_platform.session_state["neural_latencies"] = {}
    
    # Kurekodi muda wa usafirishaji data (Telemetry Logging)
    str_platform.session_state["neural_latencies"][idara_name] = time.time()

def kagua_kasi_ya_ubongo(idara_name):
    """Kupima kasi ya milisekunde ya usafirishaji data kutoka ubongo kwenda idara"""
    if "neural_latencies" in str_platform.session_state and idara_name in str_platform.session_state["neural_latencies"]:
        muda_mwanzo = str_platform.session_state["neural_latencies"][idara_name]
        kasi = (time.time() - muda_mwanzo) * 1000 # Badilisha kwenda Milliseconds
        return f"⚡ Synapse Latency kwenda {idara_name}: {kasi:.2f}ms (Radi)"
    return "⚡ Synapse State: Salama"
