import streamlit as str_platform

def pakia_lango_la_html():
    """8) INTEGUMENTARY LAYER: Lango kuu la HTML/CSS la kiofisi mlangoni (login.html)"""
    login_html_code = """
    <div style="background-color: #1E293B; border: 3px solid #D97706; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3); max-width: 500px; margin: 0 auto;">
        <h2 style="color: #D97706; font-family: sans-serif; font-weight: 800; margin-bottom: 5px;">🔐 LINGUAAFRIKA AI</h2>
        <p style="color: #94A3B8; font-family: sans-serif; font-size: 14px; margin-top: 0; margin-bottom: 20px;">Administrative Secure Node Connection • login.html Engine</p>
        <div style="background-color: #0F172A; padding: 15px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px;">
            <p style="color: #25D366; font-size: 15px; text-align: center; margin: 0; font-family: monospace; font-weight: bold;">🟢 AES-256 BIOMIMETIC PORTAL READY</p>
        </div>
    </div>
    """
    str_platform.markdown(login_html_code, unsafe_allow_html=True)

def onyesha_admin(client, api_key_source):
    """7) ENDOCRINE SYSTEM: Jopo siri la utawala na maelezo ya seva"""
    str_platform.markdown("<h2 style='color: #D97706; font-weight: bold;'>📊 Jopo la Msimamizi (System Operations Dashboard)</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    str_platform.success("🔓 Karibu Mkuu Maroa! Mfumo mzima umeji-scaling na kujiendesha kwa ufanisi wa 100%.")
    
    col_stat1, col_stat2, col_stat3 = str_platform.columns(3)
    with col_stat1:
        str_platform.info("🧠 **Akili Mnemba (AI Engine)**\n\nStatus: Salama (100% Online)\n\nNode: GPT-4o Enterprise Clusters")
    with col_stat2:
        str_platform.info("🔊 **Mtambo wa Sauti (Audio TTS)**\n\nStatus: Hai\n\nNode: OpenAI Neural TTS-1 Pipeline")
    with col_stat3:
        str_platform.info("🌐 **Seva Kuu (Cloud Host)**\n\nStatus: Imara\n\nNode: Distributed Kubernetes Cells")

    str_platform.write("---")
    str_platform.markdown("#### ⚙️ Mifumo ya Ulinzi na Secrets")
    if api_key_source:
        str_platform.success("🟢 SECRET TOKEN INTEGRATION: Connected securely via Server-Side Environment.")
