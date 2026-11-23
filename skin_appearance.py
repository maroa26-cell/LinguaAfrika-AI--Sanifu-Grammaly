"""skin_appearance.py — toleo lililorekebishwa (v3).

Mabadiliko makuu dhidi ya v2:

1. [data-testid="stHeader"] HAIPAKWI gradient tena. Header ya Streamlit ni
   position:fixed; ikipewa background isiyo wazi inakuwa ukanda mweusi unao-
   ganda juu na maudhui yanayopita chini yake yanaonekana yamekatwa.

2. Mandhari (gradient) imewekwa kwenye safu MOJA iliyofungwa: body::before
   yenye position:fixed. Safu hiyo haisogei kamwe, kwa hiyo rangi haibadiliki
   unaposcroll. Pia ni salama kwenye iOS/Android ambako
   background-attachment:fixed haitendwi vizuri.

3. Hakuna overflow / height / position inayogusa .stApp, body au main.
   Hizo ndizo zinazovunja scroll.

4. Rangi za maandishi zimewekwa kwa uangalifu: hazigongi st.success,
   st.warning, st.info, st.error wala code blocks.
"""

import streamlit as str_platform

# Weka True TU baada ya kuwa na msimbo halisi wa matangazo (Media.net / Ezoic)
# na domain yako mwenyewe. Ikiwa False, wateja hawaoni maandishi ya mfano.
ONYESHA_VIPANDE_VYA_MATANGAZO = False


_CSS = """
<style>
:root {
    --la-bg:            #090D1A;
    --la-bg-juu:        #0F172A;
    --la-dhahabu:       #D97706;
    --la-dhahabu-nyepesi:#F59E0B;
    --la-blu:           #1D4ED8;
    --la-maandishi:     #F8FAFC;
    --la-maandishi-hafifu: #CBD5E1;
}

/* ==========================================================================
   1. MANDHARI — safu moja iliyofungwa, haisogei unaposcroll
   ========================================================================== */

html {
    background-color: var(--la-bg) !important;
}

body {
    background: transparent !important;
}

/* Safu ya mandhari: position:fixed inamaanisha haishiriki kwenye scroll. */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background:
        radial-gradient(1100px 700px at 50% -10%, rgba(30, 58, 138, 0.38), transparent 65%),
        radial-gradient(900px 600px at 92% 108%, rgba(217, 119, 6, 0.10), transparent 65%),
        linear-gradient(180deg, var(--la-bg-juu) 0%, var(--la-bg) 100%);
}

/* Safu zote za Streamlit ziwe WAZI ili mandhari ya body ionekane.
   Hapa HATUBADILISHI overflow/height — ndiyo kunavunja scroll. */
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
section.main,
.main,
.block-container {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] {
    color: var(--la-maandishi) !important;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
}

/* Mstari wa rangi juu ya ukurasa (decoration) — unaongeza "rangi inabadilika" */
[data-testid="stDecoration"] {
    display: none !important;
}

/* ==========================================================================
   2. SIDEBAR
   ========================================================================== */

[data-testid="stSidebar"] {
    background-color: #05070F !important;
    border-right: 2px solid rgba(217, 119, 6, 0.20) !important;
    box-shadow: 10px 0 30px rgba(0, 0, 0, 0.50) !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #E2E8F0 !important;
    font-weight: 700 !important;
}

/* ==========================================================================
   3. LEBU ZA WIDGET (Kutoka Lugha, Kwenda Lugha, Muktadha, n.k.)
   ========================================================================== */

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] span {
    color: var(--la-maandishi-hafifu) !important;
    font-weight: 600 !important;
}

/* ==========================================================================
   4. RADIO — kila chaguo ni kadi
   ========================================================================== */

div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    padding: 12px 16px !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
    transition: background .15s ease, border-color .15s ease, box-shadow .15s ease;
}

div[role="radiogroup"] > label:hover {
    border-color: rgba(217, 119, 6, 0.35) !important;
}

/* Chaguo lililochaguliwa */
div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
    border-color: rgba(217, 119, 6, 0.60) !important;
    box-shadow: 0 4px 15px rgba(217, 119, 6, 0.40) !important;
}

div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
}

/* Matoleo ya zamani ya Streamlit */
div[data-testid="stRadio"] div[aria-checked="true"] {
    background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
    box-shadow: 0 4px 15px rgba(217, 119, 6, 0.40) !important;
    border-radius: 8px !important;
}

/* ==========================================================================
   5. VITUFE
   ========================================================================== */

div.stButton > button,
div[data-testid="stButton"] > button,
div.stLinkButton > a,
[data-testid="stLinkButton"] a,
[data-testid="stBaseLinkButton-primary"],
[data-testid="stBaseLinkButton-secondary"],
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1E3A8A 0%, var(--la-blu) 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(59, 131, 246, 0.30) !important;
    width: 100% !important;
    text-align: center !important;
    text-decoration: none !important;
    /* transition huzuia kuruka-ruka wakati wa hover/scroll */
    transition: background .20s ease, box-shadow .20s ease, transform .15s ease;
}

div.stButton > button:hover,
div[data-testid="stButton"] > button:hover,
div.stLinkButton > a:hover,
[data-testid="stLinkButton"] a:hover,
[data-testid="stBaseLinkButton-primary"]:hover,
[data-testid="stBaseLinkButton-secondary"]:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.60) !important;
    transform: translateY(-1px) !important;
    color: #FFFFFF !important;
}

/* ==========================================================================
   6. KADI / MAKONTENA
   ========================================================================== */

.b2b-safe-ad-banner,
.monetize-card {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin: 20px 0 !important;
}

/* backdrop-filter ni nzito; weka tu kwenye kadi ndogo zenye maandishi */
.monetize-card {
    backdrop-filter: blur(10px) !important;
}

.pricing-card {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    border: 3px solid var(--la-dhahabu) !important;
    border-radius: 16px !important;
    padding: 35px !important;
    text-align: center;
    margin: 20px auto !important;
    max-width: 450px !important;
}

/* ==========================================================================
   7. VISANDUKU VYA KUANDIKA
   ========================================================================== */

[data-testid="stTextArea"] textarea,
.stTextArea textarea,
[data-testid="stTextInput"] input,
.stTextInput input {
    background-color: #0B132B !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}

/* ==========================================================================
   KUMBUKA: USIONGEZE hapa chini
   overflow:hidden | height:100vh | position:fixed  kwenye .stApp/body/main.
   Hizo ndizo zinazovunja scroll.
   ========================================================================== */
</style>
"""


def inject_premium_glassmorphic_skin():
    """Injects the unified premium glassmorphism stylesheet (v3).

    Tofauti na v2: header haipakwi rangi, na mandhari iko kwenye safu
    iliyofungwa — kwa hiyo scroll na rangi hazibadiliki.
    """
    str_platform.markdown(_CSS, unsafe_allow_html=True)


def render_top_revenue_banner():
    """Sehemu ya juu ya matangazo. Haionyeshi chochote hadi flag = True."""
    if not ONYESHA_VIPANDE_VYA_MATANGAZO:
        return
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner' style='border: 1px solid rgba(217, 119, 6, 0.2) !important;'>
        <p style='color: #D97706; font-size: 11px; margin: 0 0 5px 0; font-weight: 900; letter-spacing: 1px;'>BRAND-SAFE REVENUE NODE (TOP MEDIA.NET B2B PLACEMENT)</p>
        <div id="media_net_display_slot_top"></div>
    </div>
    """, unsafe_allow_html=True)


def render_bottom_revenue_banner():
    """Sehemu ya chini ya matangazo. Haionyeshi chochote hadi flag = True."""
    if not ONYESHA_VIPANDE_VYA_MATANGAZO:
        return
    str_platform.markdown("""
    <div class='b2b-safe-ad-banner'>
        BOTTOM REVENUE ANCHOR (EZOIC AI BRAND-SAFE PLACEMENT)
        <div id="ezoic-pub-ad-placeholder-102"></div>
    </div>
    """, unsafe_allow_html=True)
