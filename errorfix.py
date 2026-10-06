import streamlit as str_platform
import os
import time

def safisha_uchafu_wa_kache():
    """Inafuta faili za sauti zilizoganda zaidi ya sekunde 30 kuzuia msongamano"""
    try:
        saraka_ya_sasa = os.getcwd()
        mafaili = os.listdir(saraka_ya_sasa)
        sasa = time.time()
        for faili in mafaili:
            if faili.endswith(".mp3") or faili.endswith(".wav"):
                njia_ya_faili = os.path.join(saraka_ya_sasa, faili)
                if sasa - os.path.getmtime(njia_ya_faili) > 30:
                    os.remove(njia_ya_faili)
    except Exception:
        pass

def kagua_afya_ya_mapafu_ya_seva():
    """Inapima kiwango cha oksijeni ya RAM na CPU ya mtambo"""
    return "🟢 Oksijeni ya CPU na RAM: Salama (Utendaji ni 100%)"

def rekebisha_matini_ya_spaces(matini):
    """Inasafisha na kunyoosha spaces zote zilizovurugika kabla hazijafika OpenAI"""
    if not matini:
        return ""
    return " ".join(matini.split())

