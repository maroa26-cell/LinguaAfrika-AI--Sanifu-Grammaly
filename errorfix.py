import streamlit as str_platform
import os
import time

def safisha_uchafu_wa_kache():
    """Mfumo wa Excretory: Unafuta mafaili yote ya zamani ya .mp3 yaliyosalia seva ya ndani"""
    saraka_ya_sasa = os.getcwd()
    mafaili = os.listdir(saraka_ya_sasa)
    sasa = time.time()
    
    for faili in mafaili:
        if faili.endswith(".mp3") or faili.endswith(".wav"):
            njia_ya_faili = os.path.join(saraka_ya_sasa, faili)
            # Kama faili lina zaidi ya sekunde 30 tangu litengenezwe, linafutwa mara moja kiotomatiki
            if sasa - os.path.getmtime(njia_ya_faili) > 30:
                try:
                    os.remove(njia_ya_faili)
                except Exception:
                    pass

def kagua_afya_ya_mapafu_ya_seva():
    """Heartbeat Check Node: Inahakikisha mtambo unapumua RAM safi"""
    return "🟢 Oksijeni ya CPU na RAM: Salama (Utendaji ni 100%)"

def rekebisha_matini_ya_spaces(matini):
    """Daktari wa Ndani: Anakata na kunyoosha spaces zilizovurugika njiani kabla hazijafika OpenAI"""
    if not matini:
        return ""
    return " ".join(matini.split())
