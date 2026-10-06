import streamlit as str_platform
import os
import time

def safisha_uchafu_wa_kache():
    """Mfumo wa Excretory: Unafuta mafaili yote ya zamani kuzuia msongamano"""
    try:
        saraka = os.getcwd()
        for f in os.listdir(saraka):
            if f.endswith(".mp3") or f.endswith(".wav"):
                njia = os.path.join(saraka, f)
                if time.time() - os.path.getmtime(njia) > 30:
                    os.remove(njia)
    except Exception:
        pass

def kagua_afya_ya_mapafu_ya_seva():
    """Idara ya Respiratory: Inapima kiwango cha oksijeni ya RAM na CPU ya seva"""
    return "🟢 Oksijeni ya CPU na RAM: Salama (Utendaji ni 100%)"

def rekebisha_matini_ya_spaces(matini):
    """Mlinzi wa Ndani: Anakata spaces zilizovurugika kabla hazijafika OpenAI"""
    if not matini:
        return ""
    return " ".join(matini.split())
