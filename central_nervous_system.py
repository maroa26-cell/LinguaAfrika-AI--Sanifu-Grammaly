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
    
    # 🎯 1. DIRA NA MALENGO YA TAASISI
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha lugha ya Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure kusaidia jamii kuhariri.\n\n• Kujenga mitambo ya kiasili ya mtafsiri na kamusi.")

    # 📝 2. MHARIRI WA KISWAHILI SANIFU PRO
    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_cns_box")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                try:
                    prompt = f"Sahihisha sarufi ya matini haya kitalaalamu:\n\n{maandishi.strip()}"
                    jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                    str_platform.success("Marekebisho Yamekamilika! ✨")
                    str_platform.write(jibu.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🔀 3. MTAFSIRI WA LUGHA SUITE (LUGHA 14 TIMILIFU)
    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa (Chewa)", "Kinyanja", "Kiafrikana (Afrikana)", "Kifaransa (French)", "Kiarabu (Arabic)", "Kihindi (Hindi)", "Kireno (Portuguese)", "Kichina (Chinese)"]
        col1, col2 = str_platform.columns(2)
        with col1:
            lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_cns_v6")
        with col2:
            lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_cns_v6")
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_cns_box")
        if str_platform.button("Zindua Tafsiri"):
            if maandishi_t.strip() != "":
                try:
                    jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate from {lugha_chanzo} to {lugha_lengwa}: {maandishi_t}"}])
                    str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
                    str_platform.write(jibu_t.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 📚 4. MAKTABA YA KAMUSI KUU
    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
        msamiati = str_platform.text_input("Andika neno, nahau au methali hapa ya Kiswahili:", key="kamusi_cns_input")
        if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
            if msamiati.strip() != "":
                try:
                    prompt_v = f"Wewe ni Kamusi Kuu ya Lugha za Kiafrika. Toa ufafanuzi wa kina na mifano ya sentensi kwa neno hili la Kiswahili: {msamiati.strip()}"
                    jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
                    str_platform.info("✨ Uchambuzi wa Kitaalamu vya Kamusi Kuu:")
                    str_platform.write(jibu_v.choices.message.content)
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🔊 5. MTAMBO WA SAUTI (DARASA)
    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        str_platform.markdown("### 🔊 Mtambo wa Sauti Kuu ya Darasa (UNLOCKED) 🔓", unsafe_allow_html=True)
        v_mwalimu = str_platform.selectbox("Sauti ya Mwalimu:", ["onyx", "echo", "alloy"], key="voice_cns_select")
        t_mwalimu = str_platform.text_area("Maandishi ya Mwalimu:", "Karibu darasani mwanafunzi wangu.", key="teacher_cns_txt")
        if str_platform.button("Zalisha Sauti"):
            if t_mwalimu.strip() != "":
                try:
                    res = client.audio.speech.create(model="tts-1", voice=v_mwalimu, input=t_mwalimu)
                    open("sauti_mwalimu.mp3", "wb").write(res.content)
                    str_platform.audio("sauti_mwalimu.mp3")
                except Exception as api_err:
                    str_platform.error(f"🛑 OpenAI API Exception: {str(api_err)}")

    # 🤖 6. AI PHONETIC ROBOT (UKAGUZI)
    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        str_platform.markdown("### 🤖 AI Phonetic Robot Enterprise Suite (UNLOCKED) 🔓", unsafe_allow_html=True)
        sauti_mwanafunzi = str_platform.file_uploader("Pakia faili la sauti hapa:", type=["wav", "mp3"], key="robot_cns_upload")
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

    # 🔐 7. LANGO LA KUINGIA NA USASISHAJI WA REDIRECT LINKS
    elif chaguo_menyu == "🔐 Lango la Kuingia (Login Dashboard)":
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
            chaguo_lango = str_platform.selectbox("Chagua Hadhi Yako (Role):", ["Premium User", "Admin"], key="lango_cns_select")
            jina = str_platform.text_input("Ingiza Jina (Username):", key="lango_cns_user")
            password = str_platform.text_input("Ingiza Nenosiri (Password):", type="password", key="lango_cns_pass")
            if str_platform.button("Thibitisha Kuingia Mfumo"):
                if database.thibitisha_utambulisho_wa_siri(jina, password, chaguo_lango):
                    str_platform.session_state["user_status"] = "admin" if chaguo_lango == "Admin" else "standard_premium"
                    str_platform.session_state["active_user_name"] = jina
                    str_platform.rerun()
                else:
                    str_platform.error("🛑 Hitilafu: Jina au Nenosiri uliloingiza si sahihi!")
        with col_lango2:
            str_platform.markdown("### 📝 Jisajili Akaunti Mpya (Sign Up)")
            
            # 👑 BANDO LA MAELEKOZO: Maelekezo rasmi ya kiwanda kuzuia makosa ya wateja!
            str_platform.markdown("""
            <div style='background-color: rgba(217, 119, 6, 0.1); border-left: 5px solid #D97706; padding: 12px; border-radius: 6px; margin-bottom: 15px;'>
                <p style='color: #D97706; font-size: 14px; margin: 0 0 5px 0; font-weight: bold;'>📝 MWONGOZO WA USAJILI SALAMA:</p>
                <ul style='color: #E2E8F0; font-size: 12.5px; margin: 0; padding-left: 18px;'>
                    <li>Unda Jina (Username) bila nafasi au herufi kubwa.</li>
                    <li>Namba ya simu ianze na <b>07</b> au <b>06</b> (Mfano: 07XXXXXXXX).</li>
                    <li>Ukishabofya kitufe, subiri masekunde 5 ili mfumo wa kibenki ukujibu.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            chaguo_usajili = str_platform.selectbox("Sajili Akaunti Kama:", ["Premium User", "Admin"], key="signup_cns_role")
            jina_jipya = str_platform.text_input("Tengeneza Jina (New Username):", key="signup_cns_user")
            siri_mpya = str_platform.text_input("Tengeneza Nenosiri (New Password):", type="password", key="signup_cns_pass")
            
            str_platform.write("---")
            str_platform.markdown("<p style='color: #D97706; font-weight: bold; margin-bottom: 2px;'>💳 Kifurushi cha Premium ($5.00 USD / Mwezi)</p>", unsafe_allow_html=True)
