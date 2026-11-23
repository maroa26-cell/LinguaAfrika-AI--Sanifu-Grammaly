import streamlit as str_platform

# Weka True TU baada ya kuwa na msimbo halisi wa matangazo (Media.net / Ezoic)
# na domain yako mwenyewe. Ikiwa False, wateja hawaoni maandishi ya mfano.
ONYESHA_VIPANDE_VYA_MATANGAZO = False


def inject_premium_glassmorphic_skin():
    """Injects the unified premium glassmorphism stylesheet (v2: selectors za Streamlit mpya)."""
    str_platform.markdown("""
    <style>
        /* Background kuu */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: radial-gradient(circle at 50% 50%, #0F172A 0%, #090D1A 100%) !important;
            font-family: 'Segoe UI', system-ui, sans-serif !important;
            color: #F8FAFC !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #05070F !important;
            border-right: 2px solid rgba(217, 119, 6, 0.2) !important;
            box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #E2E8F0 !important; font-weight: 700 !important;
        }

        /* Lebo za visanduku (Kutoka Lugha, Kwenda Lugha, Muktadha, n.k.) */
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] span {
            color: #CBD5E1 !important; font-weight: 600 !important;
        }

        /* Radio: kila chaguo ni kadi */
        div[role="radiogroup"] > label {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            padding: 12px 16px !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
        }
        /* Chaguo lililochaguliwa (toleo jipya) */
        div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
            border-color: rgba(217, 119, 6, 0.6) !important;
            box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4) !important;
        }
        /* Chaguo lililochaguliwa (matoleo ya zamani) */
        div[data-testid="stRadio"] div[aria-checked="true"] {
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
            box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4) !important;
            border-radius: 8px !important;
        }

        /* Vitufe */
        div.stButton > button,
        div.stLinkButton > a,
        [data-testid="stLinkButton"] a,
        [data-testid="stBaseLinkButton-primary"],
        [data-testid="stBaseLinkButton-secondary"] {
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important; font-weight: 800 !important;
            padding: 14px 28px !important; border-radius: 12px !important;
            border: 1px solid rgba(59, 131, 246, 0.3) !important; width: 100% !important;
            text-align: center !important; text-decoration: none !important;
        }
        div.stButton > button:hover,
        div.stLinkButton > a:hover,
        [data-testid="stLinkButton"] a:hover,
        [data-testid="stBaseLinkButton-primary"]:hover,
        [data-testid="stBaseLinkButton-secondary"]:hover {
            background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.6) !important;
            transform: translateY(-2px) !important;
            color: white !important;
        }

        /* Makontena ya matangazo / kadi (stBlock imeondolewa: ilivunja mpangilio) */
        .b2b-safe-ad-banner, .monetize-card {
            background: rgba(255, 255, 255, 0.02) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important; padding: 20px !important; margin: 20px 0 !important;
        }
        .pricing-card {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
            border: 3px solid #D97706 !important; border-radius: 16px !important;
            padding: 35px !important; text-align: center; margin: 20px auto !important; max-width: 450px !important;
        }

        /* Visanduku vya kuandika */
        .stTextArea textarea, .stTextInput input {
            background-color: #0B132B !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_top_revenue_banner():
    """Sehemu ya juu ya matangazo. Haionyeshi chochote hadi ONYESHA_VIPANDE_VYA_MATANGAZO = True."""
    if not ONYESHA_VIPANDE_VYA_MATANGAZO:
        return
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner' style='border: 1px solid rgba(217, 119, 6, 0.2) !important;'>
        <p style='color: #D97706; font-size: 11px; margin: 0 0 5px 0; font-weight: 900; letter-spacing: 1px;'>BRAND-SAFE REVENUE NODE (TOP MEDIA.NET B2B PLACEMENT)</p>
        <div id="media_net_display_slot_top"></div>
    </div>
    """, unsafe_allow_html=True)


def render_bottom_revenue_banner():
    """Sehemu ya chini ya matangazo. Haionyeshi chochote hadi ONYESHA_VIPANDE_VYA_MATANGAZO = True."""
    if not ONYESHA_VIPANDE_VYA_MATANGAZO:
        return
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner'>
        BOTTOM REVENUE ANCHOR (EZOIC AI BRAND-SAFE PLACEMENT)
        <div id="ezoic-pub-ad-placeholder-102"></div>
    </div>
    """, unsafe_allow_html=True)
