import streamlit as str_platform

def zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu):
    """🧠 CENTRAL NERVOUS SYSTEM - INTEGRATED MULTI-ROLE CORE VIEW ENGINE"""
    
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1: str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha Kiswahili.")
        with col_m2: str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii.\n\n• Kujenga mitambo ya kulipia ya sauti kwa shule.")

    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v4_direct_link")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi.strip()}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                str_platform.success("Marekebisho Yamekamilika! ✨")
                str_platform.write(jibu.choices.message.content)

    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Kichewa (Chichewa)", "Kiyarabu (Arabic)", "Kifaransa (French)", "Kichina (Chinese)"]
        muktadha_list = ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara", "Fasihi na Ushairi"]
        col1, col2, col3 = str_platform.columns(3)
        with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1)
        with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0)
        with col3: muktadha = str_platform.selectbox("Muktadha wa Tafsiri:", muktadha_list, index=0)
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=150, key="trans_v4_direct_link")
        if str_platform.button("Zindua Tafsiri ya Kitaalamu"):
            if maandishi_t.strip() != "":
                prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha} style:\n\n{maandishi_t.strip()}"
                jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
                str_platform.success("🔮 Matokeo ya Tafsiri Kuu Imekamilika!")
                str_platform.write(jibu_t.choices.message.content)

    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
        msamiati = str_platform.text_input("Andika neno, nahau au methali hapa:")
        if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
            if msamiati.strip() != "":
                prompt_v = f"Toa maana kamili, nahau na mifano ya sentensi kwa Kiswahili: {msamiati.strip()}"
                jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
                str_platform.info("Uchambuzi wa Kitaalamu:")
                str_platform.write(jibu_v.choices.message.content)

    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kifurushi cha Premium Lock. Tafadhali nenda kwenye '🔐 Lango la Kuingia (Login Dashboard)' pembeni ili kufungua akaunti yako.")
        else:
            str_platform.markdown("### 🔊 Mtambo wa Sauti Kuu ya Darasa (UNLOCKED) 🔓", unsafe_allow_html=True)
            v_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"])
            t_mwalimu = str_platform.text_area("Maandishi ya Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_link_v4")
            if str_platform.button("Zalisha Sauti Kuu"):
                res = client.audio.speech.create(model="tts-1", voice=v_mwalimu, input=t_mwalimu)
                open("sauti_mwalimu.mp3", "wb").write(res.content)
                str_platform.audio("sauti_mwalimu.mp3")

    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kipengele hiki kinahitaji Akaunti ya Premium. Tafadhali bofya '🔐 Lango la Kuingia (Login Dashboard)' pembeni.")
        else:
            str_platform.markdown("### 🤖 AI Phonetic Robot Enterprise Suite (UNLOCKED) 🔓", unsafe_allow_html=True)
            sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti hapa:", type=["wav", "mp3"], key="robot_link_v4")
            if sauti_mwanafunzi is not None:
                if str_platform.button("Zindua Ukaguzi Mkuu wa Roboti"):
                    trans_audio = client.audio.transcriptions.create(model="whisper-1", file=(sauti_mwanafunzi.name, sauti_mwanafunzi.read()))
                    str_platform.info(f"🗣️ Robot amekusikia: '{trans_audio.text}'")
                    robot_prompt = f"Wewe ni mtaalamu wa fonetiki ya Kiswahili Sanifu. Sentensi: '{trans_audio.text}'. Toa ripoti rasmi ya fonetiki, mpe alama (0-100%) na ushauri."
                    jibu_robot = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": robot_prompt}])
                    str_platform.success("🔮 Ripoti Kuu ya Ukaguzi wa Roboti:")
                    str_platform.write(jibu_robot.choices.message.content)

    elif chaguo_menyu == "🔐 Lango la Kuingia (Login Dashboard)":
        str_platform.markdown("""
        <div style="background-color: #1E293B; border: 3px solid #D97706; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3); max-width: 500px; margin: 0 auto;">
            <h2 style="color: #D97706; font-family: sans-serif; font-weight: 800; margin-bottom: 5px;">🔐 LOGIN DASHBOARD</h2>
            <p style="color: #94A3B8; font-family: sans-serif; font-size: 14px; margin-top: 0; margin-bottom: 20px;">The Smart Multi-Role Identity Gateway</p>
        </div>
        """, unsafe_allow_html=True)
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
                    str_platform.session_state["active_user_name"] = jina
                    str_platform.rerun()
                elif chaguo_lango == "Premium User" and jina in str_platform.session_state["db_watumiaji"] and str_platform.session_state["db_watumiaji"][jina] == password:
                    str_platform.session_state["user_status"] = "standard_premium"
                    str_platform.session_state["active_user_name"] = jina
                    str_platform.rerun()
                else: str_platform.error("🛑 Hitilafu: Data ulizoingiza si sahihi!")
        with col_lango2:
            str_platform.markdown("### 📝 Jisajili Akaunti Mpya (Sign Up)")
            chaguo_usajili = str_platform.selectbox("Sajili Akaunti Kama:", ["Premium User", "Admin"], key="signup_role_select")
            jina_jipya = str_platform.text_input("Tengeneza Jina (New Username):", key="signup_user")
            siri_mpya = str_platform.text_input("Tengeneza Nenosiri (New Password):", type="password", key="signup_pass")
            if str_platform.button("Kamilisha Usajili wa Akaunti"):
                if jina_jipya.strip() != "" and siri_mpya.strip() != "":
                    if chaguo_usajili == "Admin":
                        str_platform.session_state["db_wasimamizi"][jina_jipya.strip()] = siri_mpya.strip()
                        str_platform.success(f"👑 Hongera Kiongozi {jina_jipya}! Akaunti ya Utawala imeundwa. Weka data hizi upande wa Sign In kuingia.")
                    else:
                        str_platform.session_state["db_watumiaji"][jina_jipya.strip()] = siri_mpya.strip()
                        str_platform.success(f"🎉 Hongera {jina_jipya}! Akaunti ya Premium imeundwa kiofisi. Ingia upande wa kushoto kufungua Mitambo yote!")

    elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        str_platform.markdown("<h2 style='color: #D97706; font-weight: bold;'>📊 Jopo la Msimamizi (System Operations Dashboard)</h2>", unsafe_allow_html=True)
        str_platform.success(f"🔓 Karibu Kiongozi {jina_la_sasa.upper()}! Mfumo mzima umeji-scaling na kujiendesha kwa ufanisi wa 100%.")
        col_stat1, col_stat2, col_stat3 = str_platform.columns(3)
