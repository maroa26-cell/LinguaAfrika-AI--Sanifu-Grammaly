import streamlit as str_platform

def weka_mandhari_ya_kifalme():
    str_platform.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F8FAFC !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        [data-testid="stSidebar"] {
            background-color: #0F172A !important; /* Obsidian Dark */
            color: #ffffff !important;
            border-right: 4px solid #D97706 !important; /* Gold Border */
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-size: 16px !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] > label {
            background-color: rgba(255, 255, 255, 0.04) !important;
            padding: 12px 15px !important;
            border-radius: 8px !important;
            margin-bottom: 8px !important;
            transition: all 0.3s ease-in-out !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        div[data-testid="stRadio"] div[aria-checked="true"] {
            background-color: #D97706 !important;
            border-radius: 6px !important;
            padding: 4px 10px !important;
        }
        div.stButton > button {
            background-color: #1E3A8A !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 14px 28px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(30, 58, 138, 0.2) !important;
            width: 100% !important;
        }
        textarea, input {
            border: 2px solid #E2E8F0 !important;
            border-radius: 10px !important;
            background-color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
