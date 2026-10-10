import streamlit as str_platform
import database
import pespal_core  # Mfumo wa homoni wa kibenki uliopo hai mlangoni!
import time

# 👑 SANIFU MIPANGILIO YA SEVA TANZU YANAYO JITEGEMEA
str_platform.set_page_config(page_title="Ourworthlinks Operations Dashboard", page_icon="🔐", layout="wide")

try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception:
    pass

# 🎨 DIRECT ENTERPRISE LUXURY SKIN INJECTION (DARK HIGH-TECH STYLE)
str_platform.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0F172A !important; font-family: 'Segoe UI', sans-serif !important; color: #ffffff !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .stTextInput label, .stSelectbox label, .stRadio label { color: #E2E8F0 !important; font-weight: bold !important; font-size: 15px !important; }
    div.stButton > button { background-color: #D97706 !important; color: white !important; font-weight: bold !important; padding: 12px 24px !important; border-radius: 8px !important; width: 100% !important; border: none !important; }
    div.stButton > button:hover { background-color: #B45309 !important; color: white !important; }
    .stTable { background-color: #1E293B !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-weight: 900; margin-bottom: 0;'>🔐 OURWORTHLINKS OPERATIONS JOPO</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px;'>Administrative Secure Identity Portal & B2B Analytics</p>", unsafe_allow_html=True)
str_platform.write("---")

# Kuvunja kurasa katika vyumba viwili vilivyonyooka kibaolojia
col_lango1, col_lango2 = str_platform.columns(2)

with col_lango1:
    str_platform.markdown("<h3 style='color: #D97706;'>🔑 Kuingia Mfumo (Sign In Admin)</h3>", unsafe_allow_html=True)
    chaguo_lango = str_platform.selectbox("Hadhi Yako Mfumo (Role):", ["Admin", "Premium User"], key="v14_pages_role_sel")
    jina = str_platform.text_input("Ingiza Jina (Username):", key="v14_pages_user_in")
    password = str_platform.text_input("Ingiza Nenosiri (Password):", type="password", key="v14_pages_pass_in")
    
    if str_platform.button("Thibitisha Kuingia Mfumo", key="v14_pages_btn_login"):
        if database.thibitisha_utambulisho_wa_siri(jina, password, chaguo_lango):
            str_platform.success(f"🔓 Karibu Kiongozi {jina.upper()}! Mifumo yote ya B2B Token Channels ipo hai.")
            str_platform.write("---")
            str_platform.markdown("### 🏢 Enterprise B2B Active Client Tokens")
            
            data_b2b = [{"Client Token Key": "owl-live-secret-enterprise-key-2026", "Company Name": "Global Tech Client v1", "Currency": "USD", "Rate Per Word": "$0.00200", "Status": "🟢 ACTIVE"}]
            str_platform.table(data_b2b)
            
            col_b1, col_b2 = str_platform.columns(2)
            with col_b1: 
                str_platform.info("💰 **Total B2B Revenue Logged**\n\nAccumulated: **$1,240.50 USD**")
            with col_b2: 
                str_platform.info("📈 **Traffic Volume Analytics**\n\nTotal Words API Streams: **620,250 Words**")
        else:
            str_platform.error("🛑 Hitilafu: Jina au Nenosiri uliloingiza si sahihi!")

with col_lango2:
    str_platform.markdown("<h3 style='color: #D97706;'>📝 Jisajili Akaunti Mpya (Sign Up)</h3>", unsafe_allow_html=True)
    
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
    
    chaguo_usajili = str_platform.selectbox("Sajili Akaunti Kama:", ["Premium User", "Admin"], key="v14_pages_signup_sel")
    jina_jipya = str_platform.text_input("Tengeneza Jina (New Username):", key="v14_pages_new_user")
    siri_mpya = str_platform.text_input("Tengeneza Nenosiri (New Password):", type="password", key="v14_pages_new_pass")
    
    str_platform.write("---")
    str_platform.markdown("<p style='color: #D97706; font-weight: bold; margin-bottom: 2px;'>💳 Kifurushi cha Premium ($5.00 USD / Mwezi)</p>", unsafe_allow_html=True)
    njia_malipo = str_platform.radio("Chagua Njia ya Malipo:", ["Mobile Money (M-Pesa/Tigo Pesa)", "Kadi ya Benki (Visa / Mastercard)"], key="v14_pages_pay_radio")
    
    if njia_malipo == "Mobile Money (M-Pesa/Tigo Pesa)":
        mtandao_simu = str_platform.selectbox("Chagua Mtandao wa Malipo:", ["M-Pesa (Vodacom)", "Tigo Pesa (Tigo)", "Airtel Money (Airtel)"], key="v14_pages_carrier")
        namba_simu = str_platform.text_input("Ingiza Namba ya Simu (Mfano: 07XXXXXXXX):", key="v14_pages_phone_no")
    else:
        jina_kadi = str_platform.text_input("Jina Linalosomeka Kwenye Kadi (Cardholder Name):", key="v14_pages_cardname")
        namba_kadi = str_platform.text_input("Namba ya Kadi (Card Number - 16 Digits):", max_chars=16, key="v14_pages_cardno")
        col_k1, col_k2 = str_platform.columns(2)
        with col_k1: tarehe_kadi = str_platform.text_input("Tarehe ya Kuisha (MM/YY):", max_chars=5, key="v14_pages_expiry")
        with col_k2: cvv_kadi = str_platform.text_input("Namba ya Siri (CVV):", type="password", max_chars=3, key="v14_pages_cvv")
        
    if str_platform.button("Kamilisha Usajili na Lipia Kifurushi", key="v14_pages_btn_signup"):
        if jina_jipya.strip() != "" and siri_mpya.strip() != "":
            try:
                # 👑 SPINNER GATEWAY: Inafungua kasiki kuzuia mkwamo wakati miamala ikichakatwa Live!
                with str_platform.spinner("🧠 Inawasiliana na Lango Kuu la Pesapal..."):
                    matokeo_p = pespal_core.anzisha_muamala_wa_pesapal(jina_jipya.strip(), f"{jina_jipya.strip()}@ourworthlinks.com", 5.00)
                
                if matokeo_p.get("status") == "success":
                    str_platform.success("📲 ODA IMESAJILIWA: Lango la malipo limefunguka!")
                    str_platform.markdown(f"👉 [BOFYA HAPA KUFUNGUA FOMU HALISI YA PESAPAL]({matokeo_p.get('redirect_url')})")
                    
                    if database.sajili_mtumiaji_mpya(jina_jipya.strip(), siri_mpya.strip(), chaguo_usajili):
                        str_platform.markdown("""
                        <div style='background-color: rgba(37, 211, 102, 0.1); border: 2px solid #25D366; padding: 15px; border-radius: 8px; text-align: center; margin-top: 15px;'>
                            <h4 style='color: #25D366; margin: 0 0 5px 0;'>✅ Usajili Umekamilika Kwenye SQLite!</h4>
                            <p style='color: #E2E8F0; font-size: 13px; margin: 0;'>Ukishamaliza malipo kwenye dirisha la juu, tumia fomu ya kushoto <b>(🔑 Kuingia Mfumo)</b> kuingia hewani papo hapo!</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    str_platform.error(matokeo_p.get("message"))
            except Exception as e:
                str_platform.error(f"🛑 Hitilafu ya Lango la Malipo: {str(e)}")
        else:
            str_platform.warning("⚠️ Tafadhali jaza Username na Password kwanza!")

str_platform.write("---")
# Kitufe kiofisi cha kurejea mlangoni mwa Portal ya Wageni
if str_platform.button("← Rudi Kwenye Portal Kuu ya Kiswahili AI", key="v14_pages_btn_back"):
    str_platform.markdown("<p style='color: #94A3B8; text-align: center;'>Tumia menu ya Streamlit au bofya App jina kurudi mlangoni.</p>", unsafe_allow_html=True)
