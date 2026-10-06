
import streamlit as str_platform

def zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu):
    """
    🧠 CENTRAL NERVOUS SYSTEM - THE DECENTRALIZED INNER BRAIN
    Inaratibu na kuendesha viungo tanzu kulingana na amri za app.py
    """
    
    # 🎯 DIRA NA MALENGO YA TAASISI
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii.\n\n• Kujenga mitambo ya kulipia ya sauti kwa shule.")

    # 📝 MHARIRI WA KISWAHILI SANIFU PRO
    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_v4_direct")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi.strip()}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                str_platform.success("Marekebisho Yamekamilika! ✨")
                str_platform.write(jibu.choices.message.content)

    # 🔀 MTAFSIRI WA LUGHA SUITE (LUGHA 14 & MIKTADHA 6)
    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Kichewa (Chichewa)", "Kifaransa", "Kiarabu"]
        muktadha_list = ["Mazungumzo ya Kawaida", "Kiakademia", "Kidini na Kiimani", "Kisheria", "Kibiashara"]
        col1, col2, col3 = str_platform.columns(3)
        with col1:
            lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1)
        with col2:
            lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0)
        with col3:
            muktadha = str_platform.selectbox("Muktadha wa Tafsiri:", muktadha_list, index=0)
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=150, key="trans_v4_direct")
        if str_platform.button("Zindua Tafsiri ya Kitaalamu"):
            if maandishi_t.strip() != "":
                prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa} in a {muktadha} style:\n\n{maandishi_t.strip()}"
                jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
                str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
                str_platform.write(jibu_t.choices.message.content)

    # 📚 MAKTABA YA KAMUSI KUU
    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
        msamiati = str_platform.text_input("Andika neno, nahau au methali hapa:")
        if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
            if msamiati.strip() != "":
                prompt_v = f"Toa maana kamili na mifano ya sentensi kwa Kiswahili: {msamiati.strip()}"
                jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
                str_platform.info("Uchambuzi wa Kitaalamu:")
                str_platform.write(jibu_v.choices.message.content)

    # 🔊 MTAMBO WA SAUTI (PREMIUM LOCK)
    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kifurushi cha Premium Lock. Tafadhali nenda kwenye '🔐 Ingia / Jisajili (Sign In)' pembeni.")
        else:
            str_platform.markdown("🔊 Mtambo wa Sauti Umefunguka kiofisi.")

    # 🤖 AI PHONETIC ROBOT (PREMIUM LOCK)
    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        str_platform.warning("👑 Kipengele hiki kinahitaji Akaunti ya Premium.")

    # 🔐 LANGO LA USURUHISHO (SIGN IN)
    elif chaguo_menyu == "🔐 Ingia / Jisajili (Sign In)":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔐 Lango la Kuingia Mfumo</h3>", unsafe_allow_html=True)
        chaguo_lango = str_platform.selectbox("Nia ya Kuingia yako:", ["Premium User", "Admin"], key="lango_select_v4")
        jina = str_platform.text_input("Username:", key="lango_username_v4")
        password = str_platform.text_input("Password:", type="password", key="lango_password_v4")
        if str_platform.button("Thibitisha Kuingia Mfumo"):
            if chaguo_lango == "Admin" and password == "Maroa2026":
                str_platform.session_state["user_status"] = "admin"
                str_platform.rerun()
            elif chaguo_lango == "Premium User" and jina.strip() != "" and password.strip() != "":
                str_platform.session_state["user_status"] = "standard_premium"
                str_platform.rerun()

    # 📊 JOPO LA ADMIN
    elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        str_platform.success("🔓 Karibu Mkuu Maroa! Jopo Kuu la Usimamizi lipo salama.")
