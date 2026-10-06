import streamlit as str_platform
import model

def anzisha_kamusi(client):
    """Inafungua darasa la utafiti na msamiati mbele ya ukurasa"""
    str_platform.markdown("<h2 style='color: #1E3A8A; font-weight: bold;'>📚 Maktaba ya Msamiati na Kamusi Kuu</h2>", unsafe_allow_html=True)
    str_platform.write("---")
    msamiati_input = str_platform.text_input("Andika neno, nahau, au methali hapa:", key="vocab_core_box_v4")
    
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="trigger_vocab_search_btn"):
        if msamiati_input.strip() != "":
            str_platform.info("🧠 Ubongo unachambuzi msamiati... Tafadhali subiri sekunde chache.")
            prompt = f"Toa maana kamili, nahau, matumizi na mifano ya sentensi kwa neno hili la Kiswahili: {msamiati_input.strip()}"
            matokeo = model.piga_gpt4o(client, prompt)
            str_platform.success("Uchambuzi Umekamilika! ✨")
            str_platform.info("Uchambuzi wa Kitaalamu wa Kamusi Kuu:")
            str_platform.write(matokeo)
        else:
            str_platform.warning("⚠️ Tafadhali andika msamiati kwanza!")
