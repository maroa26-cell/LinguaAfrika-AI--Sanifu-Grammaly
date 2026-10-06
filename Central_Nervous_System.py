
import streamlit as str_platform
import os
import time

# Kuvuta idara tanzu zilizopo tayari kwenye GitHub yako
import errorfix
import circulatory_transport
import admin

def zindua_mifumo_ya_fahamu_ya_mwili(client, api_key_source, chaguo_menyu):
    """
    🧠 CENTRAL NERVOUS SYSTEM CORE ENGINE
    Inaratibu na kuamrisha idara zote kufanya kazi kwa ufasaha kibiashara
    """
    # Kusafisha kache kiotomatiki nyuma ya pazia
    try:
        errorfix.safisha_uchafu_wa_kache()
    except Exception:
        pass
    
    # 1) Dira na Malengo ya Taasisi
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo, Dira na Kimkakati ya Kikazi</h3>", unsafe_allow_html=True)
        str_platform.write("LinguaAfrika AI imesajiliwa kuwa chombo kikuu cha kimkakati cha kidijitali barani Afrika kusanifisha na kuongeza thamani ya matumizi ya lugha ya Kiswahili kibiashara, kiakademia, na kiofisi.")
        col_m1, col_m2 = str_platform.columns(2)
        with col_m1:
            str_platform.info("🚀 **Dira Yetu (Our Vision)**\n\nKuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha sarufi na matamshi ya Kiswahili.")
        with col_m2:
            str_platform.info("📈 **Malengo ya Kikazi (Our Objectives)**\n\n• Kutoa zana za bure za kusaidia jamii kuhariri na kutafsiri lugha.\n\n• Kujenga mitambo ya kulipia ya sauti na ripoti za fonetiki kwa ajili ya shule.")

    # 2) Mhariri wa Kiswahili Sanifu Pro (Bure kwa Wote)
    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi yako hapa:", key="editor_core_box")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                prompt = f"Wewe ni mtaalamu wa Kiswahili Sanifu. Kagua na usahihishe sarufi hapa:\n\n{maandishi}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                str_platform.success("Marekebisho Yamekamilika!")
                str_platform.write(jibu.choices.message.content)
            else:
                str_platform.warning("⚠️ Tafadhali ingiza maandishi kwanza!")

    # 3) Mtafsiri wa Lugha Suite (Bure kwa Wote)
    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite (Lugha 14)</h3>", unsafe_allow_html=True)
        orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Kichewa (Chichewa)", "Kifaransa (French)", "Kiarabu (Arabic)"]
        col1, col2 = str_platform.columns(2)
        with col1:
            lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1)
        with col2:
            lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0)
            
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:", height=120)
        if str_platform.button("Zindua Tafsiri ya Kitaalamu"):
            if maandishi_t.strip() != "":
                prompt_t = f"Translate from {lugha_chanzo} to {lugha_lengwa}:\n\n{maandishi_t}"
                jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_t}])
                str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
                str_platform.write(jibu_t.choices.message.content)

    # 4) Maktaba ya Kamusi Kuu (Bure kwa Wote)
    elif chaguo_menyu == "📚 Maktaba ya Kamusi Kuu":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
        msamiati = str_platform.text_input("Andika neno au nahau:")
        if str_platform.button("Tafuta Kwenye Kamusi Kuu"):
            if msamiati.strip() != "":
                prompt_v = f"Toa maana na mifano ya sentensi kwa kutumia msamiati huu: {msamiati}"
                jibu_v = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_v}])
                str_platform.info("Uchambuzi wa Kamusi Kuu:")
                str_platform.write(jibu_v.choices.message.content)

    # 5) Mtambo wa Sauti (Premium Paywall Security)
    elif chaguo_menyu == "🔊 Mtambo wa Sauti (Darasa)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kifurushi cha Premium Lock. Tafadhali nenda kwenye kipengele cha '🔐 Ingia / Jisajili (Sign In)' pembeni ili kufungua kiofisi.")
        else:
            str_platform.success("🟢 Mtambo wa Sauti Umevifungua! (Premium Active)")

    # 6) AI Phonetic Robot (Premium Paywall Security)
    elif chaguo_menyu == "🤖 AI Phonetic Robot (Ukaguzi)":
        if str_platform.session_state["user_status"] == "guest":
            str_platform.warning("👑 Kipengele hiki kinahitaji Akaunti ya Premium. Tafadhali bofya '🔐 Ingia / Jisajili (Sign In)' pembeni.")
        else:
            str_platform.success("🟢 AI Phonetic Robot Ipo Tayari! (Premium Active)")

    # 7) Mlango wa Kujisajili/Kuingia (Sign In Gateway)
    elif chaguo_menyu == "🔐 Ingia / Jisajili (Sign In)":
        try:
            admin.pakia_lango_la_html()
        except Exception:
            str_platform.markdown("### 🔐 Langa la Kuingia Mfumo")
            
        str_platform.write("---")
        chaguo_lango = str_platform.selectbox("Nia ya Kuingia yako:", ["Premium User", "Admin"], key="lango_select")
        jina = str_platform.text_input("Jina la Mtumiaji (Username):", key="lango_username")
        password = str_platform.text_input("Nenosiri / Password:", type="password", key="lango_password")
        if str_platform.button("Thibitisha Kuingia Mfumo"):
            if chaguo_lango == "Admin" and password == "Maroa2026":
                str_platform.session_state["user_status"] = "admin"
                str_platform.rerun()
            elif chaguo_lango == "Premium User" and jina.strip() != "" and password.strip() != "":
                str_platform.session_state["user_status"] = "standard_premium"
                str_platform.rerun()

    # 8) Jopo la Siri la Admin (Dashboard)
    elif chaguo_menyu == "📊 Ripoti Kuu ya Utendaji" and str_platform.session_state["user_status"] == "admin":
        try:
            admin.onyesha_admin(client, api_key_source)
        except Exception:
            str_platform.write("📊 Dashboard ipo salama.")
