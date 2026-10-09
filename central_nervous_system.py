import streamlit as str_platform
import database
import synapse
import time

try:
    import pesapal_core
    pesapal_tayari = True
except Exception:
    pesapal_tayari = False

def zindua_mifumo_ya_fahamu_ya_mwili(client, chaguo_menyu):
    """🧠 CENTRAL NERVOUS SYSTEM - THE DECENTRALIZED INNER BRAIN VIEW ENGINE"""
    
    # Jina la Lango la Kuingia lililofungwa kufuli sambamba na app.py core router
    jina_lango_dashboard = "🔐 Lango la Kuingia (Login Dashboard)"
    
    # 📊 1. JOPO LA ADMIN - RIPOTI KUU YA UTENDAJI (OURWORTHLINKS)
    if chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        str_platform.markdown("<h2 style='color: #D97706; font-weight: bold;'>📊 Ourworthlinks Operations Jopo</h2>", unsafe_allow_html=True)
        str_platform.success(f"🔓 Karibu Kiongozi {str_platform.session_state['active_user_name'].upper()}! Mifumo yote ya B2B API Token Channels ipo hai kwenye SQLite chuma.")
        str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
        data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
        str_platform.table(data_b2b)
        col_b1, col_b2 = str_platform.columns(2)
        with col_b1:
            str_platform.info("💰 **Total B2B Revenue Logged**\n\nAccumulated: **$1,240.50 USD**")
        with col_b2:
            str_platform.info("📈 **Traffic Volume Analytics**\n\nTotal Words API Streams: **620,250 Words**")

    # 🎯 2. DIRA NA MALENGO YA TAASISI
    elif chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii kuhariri.\n\n• Kujenga mitambo ya kiasili ya mtafsiri na kamusi.")

    # 📝 3. MHARIRI WA KISWAHILI SANIFU PRO
    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_cns_box_v13")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                try:
                    prompt = f"Sahihisha sarufi ya matini haya kitalaalamu:\n\n{maandishi.strip()}"
                    jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                    str_platform.success("Marekebisho Yamekamilika! ✨")
                    str_platform.write(jibu.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🔀 4. MTAFSIRI WA LUGHA SUITE (LUGHA 14 TIMILIFU)
    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)", "Kihindi (Hindi)", "Kireno (Portuguese)", "Kichina (Chinese)"]
        col1, col2 = str_platform.columns(2)
        with col1:
            lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_cns_v13")
        with col2:
            lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_cns_v13")
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_cns_box_v13")
        if str_platform.button("Zindua Tafsiri"):
            if maandishi_t.strip() != "":
                try:
                    jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate from {lugha_chanzo} to {lugha_lengwa}: {maandishi_t}"}])
                    str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
                    str_platform.write(jibu_t.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 📚 5. MAKTABA YA KAMUSI KUU
    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
        msamiati = str_platform.text_input("Andika neno, nahau au methali hapa ya Kiswahili:", key="kamusi_cns_input_v13")
        if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
            if msamiati.strip() != "":
                try:
                    prompt_v = f"Wewe ni Kamusi Kuu ya Lugha za Kiafrika. Toa ufafanuzi wa kina na mifano ya sentensi kwa neno hili la Kiswahili: {msamiati.strip()}"
                    jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
                    str_platform.info("✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:")
                    str_platform.write(jibu_v.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🔊 6. MTAMBO WA SAUTI (DARASA)
    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        str_platform.markdown("### 🔊 Mtambo wa Sauti Kuu ya Darasa (UNLOCKED) 🔓", unsafe_allow_html=True)
        v_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"], key="voice_cns_v13")
        t_mwalimu = str_platform.text_area("Maandishi ya Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_cns_v13")
        if str_platform.button("Zalisha Sauti"):
            if t_mwalimu.strip() != "":
                try:
                    res = client.audio.speech.create(model="tts-1", voice=v_mwalimu, input=t_mwalimu)
                    open("sauti_mwalimu.mp3", "wb").write(res.content)
                    str_platform.audio("sauti_mwalimu.mp3")
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🤖 7. AI PHONETIC ROBOT (UKAGUZI)
    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        str_platform.markdown("### 🤖 AI Phonetic Robot Enterprise Suite (UNLOCKED) 🔓", unsafe_allow_html=True)
        sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti hapa:", type=["wav", "mp3"], key="robot_cns_v13")
        if sauti_mwanafunzi is not None:
            if str_platform.button("Zindua Ukaguzi Mkuu wa Roboti"):
                try:
                    trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read()))
                    str_platform.info(f"🗣️ Robot amekusikia: '{trans_audio.text}'")
                    robot_prompt = f"Wewe ni mtaalamu wa fonetiki ya Kiswahili Sanifu. Sentensi: '{trans_audio.text}'."
                    jibu_robot = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": robot_prompt}])
                    str_platform.success(jibu_robot.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🔐 8. LANGO LA KUINGIA NA MAPINDUZI YA REDIRECT LAYOUTS (LUGHA YA USHINDI)
    elif chaguo_menyu == jina_lango_dashboard:
        str_platform.markdown("""
        <div style="background-color: #1E293B; border: 3px solid #D97706; padding: 30px; border-radius: 15px; text-align: center; max-width: 500px; margin: 0 auto;">
            <h2 style="color: #D97706; font-family: sans-serif; font-weight: 800; margin-bottom: 5px;">🔐 LOGIN DASHBOARD</h2>
            <p style="color: #94A3B8; font-family: sans-serif; font-size: 14px; margin: 0;">Ourworthlinks • Administrative Secure Identity Port</p>
        </div>
        """, unsafe_allow_html=True)
        str_platform.write("---")
        col_lango1, col_lango2 = str_platform.columns(2)
        with col_lango1:
            str_platform.markdown("### 🔑 Kuingia Mfumo (Sign In)")
            chaguo_lango = str_platform.selectbox("Chagua Hadhi Yako (Role):", ["Premium User", "Admin"], key="lango_cns_role_v13")
            jina = str_platform.text_input("Ingiza Jina (Username):", key="lango_cns_user_v13")
            password = str_platform.text_input("Ingiza Nenosiri (Password):", type="password", key="lango_cns_pass_v13")
            if str_platform.button("Thibitisha Kuingia Mfumo"):
                if database.thibitisha_utambulisho_wa_siri(jina, password, chaguo_lango):
                    str_platform.session_state["user_status"] = "admin" if chaguo_lango == "Admin" else "standard_premium"
                    str_platform.session_state["active_user_name"] = jina
                    str_platform.rerun()
                else:
                    str_platform.error("🛑 Hitilafu: Jina au Nenosiri uliloingiza si sahihi!")
        with col_lango2:
            str_platform.markdown("### 📝 Jisajili Akaunti Mpya (Sign Up)")
            
            str_platform.markdown("""
            <div style='background-color: rgba(217, 119, 6, 0.1); border-left: 5px solid #D97706; padding: 12px; border-radius: 6px; margin-bottom: 15px;'>
