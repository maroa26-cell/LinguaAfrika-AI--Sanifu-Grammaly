import streamlit as str_platform
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
    """🧠 CENTRAL NERVOUS SYSTEM - THE DECENTRALIZED INNER BRAIN INTER-PROCESS LINK"""
    
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii.\n\n• Kujenga mitambo ya kulipia ya sauti kwa shule.")

    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        synapse.chochea_mshipa_wa_fahamu("Mhariri")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Mhariri")
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v4_direct")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if validate_entries.kagua_matini(maandishi):
                msafi = errorfix.rekebisha_matini_ya_spaces(maandishi)
                prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{msafi}"
                matokeo = model.piga_gpt4o(client, prompt)
                str_platform.success("Marekebisho Yamekamilika! ✨")
                str_platform.write(matokeo)
                str_platform.caption(synapse.kagua_kasi_ya_ubongo("Mhariri"))

    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        synapse.chochea_mshipa_wa_fahamu("Mtafsiri")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Mtafsiri")
        sync.anzisha_mtafsiri(client)
        str_platform.sidebar.caption(synapse.kagua_kasi_ya_ubongo("Mtafsiri"))

    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        synapse.chochea_mshipa_wa_fahamu("Kamusi")
        circulatory_transport.anzisha_mzunguko_wa_data(True, "Kamusi")
        search.anzisha_kamusi(client)
        str_platform.sidebar.caption(synapse.kagua_kasi_ya_ubongo("Kamusi"))

    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kifurushi cha Premium Lock. Tafadhali nenda kwenye '🔐 Ingia / Jisajili (Sign In)' pembeni.")
        else:
            synapse.chochea_mshipa_wa_fahamu("Sauti")
            circulatory_transport.anzisha_mzunguko_wa_data(True, "Sauti")
            sauti.onyesha_sauti(client)

    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kipengele hiki kinahitaji Akaunti ya Premium. Tafadhali bofya '🔐 Ingia / Jisajili' pembeni.")
        else:
            synapse.chochea_mshipa_wa_fahamu("Robot")
            circulatory_transport.anzisha_mzunguko_wa_data(True, "Robot")
            robot.onyesha_robot(client)

    elif chaguo_menyu == "🔐 Ingia / Jisajili (Sign In)":
        admin.pakia_lango_la_html()
        str_platform.write("---")
        col_lango1, col_lango2 = str_platform.columns(2)
        with col_lango1:
            str_platform.markdown("### 🔑 Kuingia Mfumo (Sign In)")
            chaguo_lango = str_platform.selectbox("Chagua Hadhi Yako (Role):", ["Premium User", "Admin"], key="lango_select_v4")
            jina = str_platform.text_input("Ingiza Jina (Username):", key="lango_username_v4")
            password = str_platform.text_input("Ingiza Nenosiri (Password):", type="password", key="lango_password_v4")
            if str_platform.button("Thibitisha Kuingia Mfumo"):
                if chaguo_lango == "Admin" and jina in str_platform.session_state["db_wasimamizi"] and str_platform.session_state["db_wasimamizi"][jina] == password:
                    str_platform.session_state["user_status"] = "admin"
                    str_platform.rerun()
                elif jina in str_platform.session_state["db_watumiaji"] and str_platform.session_state["db_watumiaji"][jina] == password:
                    str_platform.session_state["user_status"] = "standard_premium"
                    str_platform.rerun()
                else: str_platform.error("🛑 Hitilafu: Data si sahihi!")
        with col_lango2:
            str_platform.markdown("### 📝 Jisajili Akaunti Mpya (Sign Up)")
            chaguo_usajili = str_platform.selectbox("Sajili Akaunti Kama:", ["Premium User", "Admin"], key="signup_role_select")
            jina_jipya = str_platform.text_input("Tengeneza Jina (New Username):", key="signup_user")
            siri_mpya = str_platform.text_input("Tengeneza Nenosiri (New Password):", type="password", key="signup_pass")
            if str_platform.button("Kamilisha Usajili wa Akaunti"):
                if jina_jipya.strip() != "" and siri_mpya.strip() != "":
                    if chaguo_usajili == "Admin":
                        str_platform.session_state["db_wasimamizi"][jina_jipya.strip()] = siri_mpya.strip()
                        str_platform.success(f"👑 Hongera Mkuu {jina_jipya}! Akaunti ya Msimamizi imeundwa.")
                    else:
                        str_platform.session_state["db_watumiaji"][jina_jipya.strip()] = siri_mpya.strip()
                        str_platform.success(f"🎉 Hongera {jina_jipya}! Akaunti yako ya Premium imeundwa.")

    elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        admin.onyesha_admin(client, api_key_source)
