import streamlit as str_platform
import database
import synapse

def zindua_mifumo_ya_fahamu_ya_mwili(client, chaguo_menyu):
    """🧠 CENTRAL NERVOUS SYSTEM - INTEGRATED MULTI-ROLE CORE VIEW ENGINE"""
    
    if chaguo_menyu == "🎯 Malengo na Dira ya Taasisi":
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🎯 Malengo na Dira ya Taasisi</h3>", unsafe_allow_html=True)
        str_platform.info("Kuwa kitovu namba moja duniani cha Akili Mnemba (AI) kinachosanifisha Kiswahili.")

    elif chaguo_menyu == "📝 Mhariri wa Kiswahili Sanifu Pro":
        synapse.chochea_mshipa_wa_fahamu("Mhariri")
        str_platform.markdown("<h3 style='color: #1E3A8A;'>📝 Mhariri wa Kiswahili Sanifu Pro</h3>", unsafe_allow_html=True)
        maandishi = str_platform.text_area("Andika maandishi hapa:", key="editor_v5_box")
        if str_platform.button("Zindua Ukaguzi wa Sarufi"):
            if maandishi.strip() != "":
                prompt = f"Sahihisha sarufi ya Kiswahili hapa:\n\n{maandishi.strip()}"
                jibu = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                str_platform.success("Marekebisho Yamekamilika! ✨")
                str_platform.write(jibu.choices[0].message.content)
                str_platform.caption(synapse.kagua_kasi_ya_ubongo("Mhariri"))

    elif chaguo_menyu == "🔀 Mtafsiri wa Lugha Suite":
        synapse.chochea_mshipa_wa_fahamu("Mtafsiri")
        str_platform.markdown("<h3 style='color: #1E3A8A;'>🔀 Mtafsiri wa Lugha & Muktadha Suite</h3>", unsafe_allow_html=True)
        maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri:", key="trans_v5_box")
        if str_platform.button("Zindua Tafsiri"):
            if json_data := maandishi_t.strip():
                jibu_t = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Translate to English: {maandishi_t}"}])
                str_platform.success("🔮 Matokeo ya Tafsiri Kuu:")
                str_platform.write(jibu_t.choices[0].message.content)
                str_platform.caption(synapse.kagua_kasi_ya_ubongo("Mtafsiri"))

    elif chaguo_menyu == "🔐 Lango la Kuingia (Login Dashboard)":
        str_platform.markdown("### 🔐 LOGIN DASHBOARD (Multi-Role Gateway)")
        col1, col2 = str_platform.columns(2)
        with col1:
            str_platform.markdown("#### 🔑 Sign In")
            role = str_platform.selectbox("Hadhi:", ["Premium User", "Admin"], key="login_role")
            jina = str_platform.text_input("Username:", key="login_user")
            siri = str_platform.text_input("Password:", type="password", key="login_pass")
            if str_platform.button("Ingia Mfumo"):
                if database.thibitisha_utambulisho_wa_siri(jina, siri, role):
                    str_platform.session_state["user_status"] = "admin" if role == "Admin" else "standard_premium"
                    str_platform.session_state["active_user_name"] = jina
                    str_platform.rerun()
                else:
                    str_platform.error("🛑 Data si sahihi!")
        with col2:
            str_platform.markdown("#### 📝 Sign Up")
            role_s = str_platform.selectbox("Sajili Kama:", ["Premium User", "Admin"], key="sign_role")
            jina_s = str_platform.text_input("Username Mpya:", key="sign_user")
            siri_s = str_platform.text_input("Password Mpya:", type="password", key="sign_pass")
            if str_platform.button("Kamilisha Usajili"):
                if jina_s.strip() != "" and siri_s.strip() != "":
                    if database.sajili_mtumiaji_mpya(jina_s.strip(), siri_s.strip(), role_s):
                        str_platform.success("🎉 Akaunti imeundwa kiofisi kwenye chuma! Ingia upande wa kushoto.")
                    else:
                        str_platform.error("⚠️ Username tayari ipo!")

