import streamlit as str_platform

def inject_premium_glassmorphic_skin():
    """🎨 EPITHELIAL MATRIX: Injects the unified ultra-premium glowing neon glassmorphism stylesheet"""
    str_platform.markdown("""
    <style>
        /* Central Radial Background Skin */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
            background: radial-gradient(circle at 50% 50%, #0F172A 0%, #090D1A 100%) !important; 
            font-family: 'Segoe UI', system-ui, sans-serif !important; 
            color: #F8FAFC !important; 
        }
        /* Glassmorphic Sidebar Boundaries */
        [data-testid="stSidebar"] { 
            background-color: #05070F !important; 
            border-right: 2px solid rgba(217, 119, 6, 0.2) !important; 
            box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { 
            color: #E2E8F0 !important; font-weight: 700 !important; 
        }
        /* Custom Input Fields */
        div[data-testid="stRadio"] > label { 
            background: rgba(255, 255, 255, 0.02) !important; 
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 14px 18px !important; border-radius: 12px !important; margin-bottom: 10px !important;
        }
        div[data-testid="stRadio"] div[aria-checked="true"] { 
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important; 
            box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4) !important;
            border-radius: 8px !important; padding: 6px 12px !important; 
        }
        /* Enterprise Glowing Action Buttons */
        div.stButton > button, div.stLinkButton > a { 
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%) !important; 
            color: #FFFFFF !important; font-weight: 800 !important; 
            padding: 16px 32px !important; border-radius: 12px !important; 
            border: 1px solid rgba(59, 131, 246, 0.3) !important; width: 100% !important;
            text-align: center !important; text-decoration: none !important; display: block !important;
        }
        div.stButton > button:hover, div.stLinkButton > a:hover { 
            background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important; 
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.6) !important; transform: translateY(-2px) !important;
            color: white !important;
        }
        /* Monetization Placement Containers */
        .b2b-safe-ad-banner, div[data-testid="stBlock"], .monetize-card {
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
        .stTextArea textarea, .stTextInput input {
            background-color: #0B132B !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_top_revenue_banner():
    """💰 TOP PLACEMENT: Mounts brand-safe contextual top leaderboard ad hooks"""
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner' style='border: 1px solid rgba(217, 119, 6, 0.2) !important;'>
        <p style='color: #D97706; font-size: 11px; margin: 0 0 5px 0; font-weight: 900; letter-spacing: 1px;'>🛡️ BRAND-SAFE REVENUE NODE (TOP MEDIA.NET B2B PLACEMENT)</p>
        <div id="media_net_display_slot_top"></div>
    </div>
    """, unsafe_allow_html=True)

def render_bottom_revenue_banner():
    """💰 BOTTOM PLACEMENT: Mounts brand-safe sticky anchor footer ad hooks"""
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner'>
        🛡️ BOTTOM REVENUE ANCHOR (EZOIC AI BRAND-SAFE PLACEMENT)
        <div id="ezoic-pub-ad-placeholder-102"></div>
    </div>
    """, unsafe_allow_html=True)

