import streamlit as str_platform
import os
import time

# =====================================================================
# 🧠 CENTRAL_NERVOUS_SYSTEM.PY - CORE BIOMIMETIC BRAIN KERNEL
# =====================================================================
# Inavuta na kuendesha viungo vyote tanzu vya kiumbe hai wa kidijitali
import model
import validate_entries
import errorfix
import search
import sync
import sauti
import robot
import admin
import synapse
import circulatory_transport

def zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu):
    """
    🧠 CENTRAL NERVOUS SYSTEM CORE CONTROL
    Inaratibu, inasimamia na kuendesha kila idara kulingana na amri za app.py
    """
    
    # 🎯 0) DIRA NA MALENGO YA TAASISI (MISSION CONTROL)
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha sarufi na matamshi ya Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure za kusaidia jamii kuhariri.\n\n• Kujenga mitambo ya kulipia ya sauti na ripoti za fonetiki.")

    # 📝 1) MHARIRI WA KISWAHILI SANIFU PRO (MUSCULAR NODE 1)
    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        synapse.chochea_mshipa_wa_fahamu("Mhariri")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Mhariri")
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_core_box_v4")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if validate_entries.kagua_matini(maandishi):
                msafi = errorfix.rekebisha_matini_ya_spaces(maandishi)
                prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{msafi}"
                matokeo = model.piga_gpt4o(client, prompt)
                str_platform.success("Marekebisho Yamekamilika!")
                str_platform.write(matokeo)
                str_platform.caption(synapse.kagua_kasi_ya_ubongo("Mhariri"))
            else:
                str_platform.error("🛑 Ulinzi Umekataa: Maandishi yana herufi haramu au yapo tupu!")

    # 🔀 2) MTAFSIRI WA LUGHA SUITE (CIRCULATORY DATA DISPATCH)
    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        synapse.chochea_mshipa_wa_fahamu("Mtafsiri")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Mtafsiri")
        sync.anzisha_mtafsiri(client)
        str_platform.sidebar.caption(synapse.kagua_kasi_ya_ubongo("Mtafsiri"))

    # 📚 3) MAKTABA YA KAMUSI KUU (MUSCULAR NODE 2)
    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        synapse.chochea_mshipa_wa_fahamu("Kamusi")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Kamusi")
        search.anzisha_kamusi(client)
        str_platform.sidebar.caption(synapse.kagua_kasi_ya_ubongo("Kamusi"))

    # 🔊 4) MTAMBO WA SAUTI (DARASA - PREMIUM PAYWALL SECURITY)
    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        synapse.chochea_mshipa_wa_fahamu("Sauti")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Sauti")
        sauti.onyesha_sauti(client)

    # 🤖 5) AI PHONETIC ROBOT (UKAGUZI - PREMIUM PAYWALL SECURITY)
    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        synapse.chochea_mshipa_wa_fahamu("Robot")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Robot")
        robot.onyesha_robot(client)

    # 🔐 6) MLANGO WA KUJISAJILI/KUINGIA (SIGN IN GATEWAY)
    elif chaguo_menyu == "🔐 Ingia / Jisajili (Sign In)":
        admin.pakia_lango_la_html()
        str_platform.write("---")
        chaguo_lango = str_platform.selectbox("Nia ya Kuingia yako:", ["Premium User", "Admin"], key="lango_select_v4")
        jina = str_platform.text_input("Jina la Mtumiaji (Username):", key="lango_username_v4")
        password = str_platform.text_input("Nenosiri / Password:", type="password", key="lango_password_v4")
        if str_platform.button("Thibitisha Kuingia Mfumo"):
            if chaguo_lango == "Admin" and password == "Maroa2026":
                str_platform.session_state["user_status"] = "admin"
                str_platform.rerun()
            elif chaguo_lango == "Premium User" and jina.strip() != "" and password.strip() != "":
                str_platform.session_state["user_status"] = "standard_premium"
                str_platform.rerun()

    # 📊 7) JOPO LA SIMAMIZI MKUU (FOR EXECUTIVES ONLY)
    elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        admin.onyesha_admin(client, api_key_source)
