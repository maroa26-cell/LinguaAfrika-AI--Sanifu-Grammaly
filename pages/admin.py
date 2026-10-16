import streamlit as str_platform
import sqlite3
import os
import sys
import pandas as pd
import numpy as np

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import database
import skin_appearance

str_platform.set_page_config(page_title="Ourworthlinks Business - Admin Matrix", layout="wide")
skin_appearance.inject_premium_glassmorphic_skin()

if "admin_authenticated" not in str_platform.session_state:
    str_platform.session_state["admin_authenticated"] = False

if not str_platform.session_state["admin_authenticated"]:
    str_platform.markdown("<h2 style='text-align: center; color: #D97706;'>🔐 ADMIN MATRIX CONTROL PANEL</h2>", unsafe_allow_html=True)
    col1, col2, col3 = str_platform.columns([1, 2, 1])
    with col2:
        adm_user = str_platform.text_input("Ingiza Admin Username:", key="admin_panel_u")
        adm_pass = str_platform.text_input("Ingiza Admin Password:", type="password", key="admin_panel_p")
        if str_platform.button("Zindua Utawala na Mapato", use_container_width=True):
            if database.thibitisha_utambulisho_wa_siri(adm_user, adm_pass, "admin"):
                str_platform.session_state["admin_authenticated"] = True
                str_platform.rerun()
            else:
                str_platform.error("Mtumiaji au Password si sahihi!")
    str_platform.stop()

str_platform.markdown("<h1 style='color: #34D399;'>📊 OURWORTHLINKS BUSINESS - ADMIN HUB</h1>", unsafe_allow_html=True)
str_platform.write("---")

c1, c2, c3, c4 = str_platform.columns(4)
with c1:
    str_platform.metric(label="💵 Jumla ya Mapato", value="$1,450.00 USD", delta="+12% Wiki hii")
with c2:
    str_platform.metric(label="💳 Malipo ya Pesapal Live", value="TZS 2,600,000", delta="🟢 Active")
with c3:
    str_platform.metric(label="👥 Watumiaji wa Premium", value="142 Active", delta="+8 Leo")
with c4:
    str_platform.metric(label="🎁 Freemium Sessions", value="1,105 Users", delta="-3%")

str_platform.write("---")

str_platform.markdown("### 📉 Mwenendo wa Shughuli za Mradi na Malipo (Operational Analytics)")
Muda_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Tafsiri Pro', 'Ukaguzi Sarufi', 'Malipo ya Simu']
)
str_platform.line_chart(Muda_data)

str_platform.write("---")

str_platform.markdown("### 📚 COGNITIVE DATASET INGESTION Mainframe")
uploaded_file = str_platform.file_uploader("Upload Swahili Vocabulary Matrix (CSV Format):", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'keyword' in df.columns and 'semantic_meaning' in df.columns:
            conn = database.pata_muunganisho_wa_chuma()
            cursor = conn.cursor()
            success_count = 0
            for index_row, row in df.iterrows():
                try:
                    cursor.execute("INSERT INTO kamusi_dataset (keyword, semantic_meaning) VALUES (?, ?)", (str(row['keyword']).strip().lower(), str(row['semantic_meaning']).strip()))
                    success_count += 1
                except sqlite3.IntegrityError: pass
            conn.commit()
            conn.close()
            str_platform.success(f"Loaded {success_count} terms into the system spinal cord!")
        else:
            str_platform.error("CSV requires 'keyword' and 'semantic_meaning' columns.")
    except Exception as e:
        str_platform.error(f"Anomaly caught: {str(e)}")

if str_platform.button("🚪 Funga Lango la Utawala (Log Out)", type="primary"):
    str_platform.session_state["admin_authenticated"] = False
    str_platform.rerun()
