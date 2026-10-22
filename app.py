import streamlit as str_platform
import os
import time
import io
import re
import json
import html
import pandas as pd
import requests
import streamlit.components.v1 as components
from openai import OpenAI
import database
import skin_appearance
from cerebral_cortex import CerebralCortex

muda_mwanzo = time.time()
self_healing_status = "\U0001F7E2 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Lingual Africa Sanifu", page_icon="\U0001F9E0", layout="wide", initial_sidebar_state="expanded")

# URL HALISI ya app yako (ilikuwa 'https://streamlit.app' - si sahihi)
_APP_URL_MSINGI = "https://linguaafrika-ai--sanifu-grammaly-m5xtj9pydnpe2qibp2jezc.streamlit.app"

# Kikomo cha herufi kwa kila ingizo (kuzuia matumizi mabaya / gharama kubwa)
MAX_CHARS = 5000


# ------------------------------------------------------------------ #
#  WASAIDIZI WA USALAMA / UIMARA
# ------------------------------------------------------------------ #
def _secret(jina):
    """Soma siri kwa usalama; haitaanguka kama hakuna faili la secrets."""
    try:
        return str_platform.secrets.get(jina)
    except Exception:
        return None


# Anwani ya app: inasomwa kutoka Secrets (APP_URL), sawa na pesapal_core.py.
APP_URL = str(_secret("APP_URL") or _APP_URL_MSINGI).strip().rstrip("/")


def weka_seo_schema():
    """Weka alama za JSON-LD (schema.org) kwenye <head> ya ukurasa.

    Inaitwa BAADA ya set_page_config. Maelezo yamo ndani ya kamusi ya Python (dict) na
    json.dumps inahakikisha JSON ni sahihi. Kumbuka: Streamlit hujenga ukurasa kwa JavaScript,
    kwa hiyo injini za utafutaji huenda zisiisome; hii ni juhudi ya ziada tu.
    """
    data = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "@id": f"{APP_URL}/#kamusi",
        "url": APP_URL,
        "name": "Kamusi Kuu ya Lingual Africa Sanifu",
        "description": "Kamusi ya kidijitali ya istilahi za Kiswahili na Kiingereza.",
        "inLanguage": ["sw", "en"],
        "provider": {"@type": "Organization", "name": "Lingual Africa Sanifu"},
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    js_literal = json.dumps(payload)
    components.html(
        "<script>(function(){try{var d=window.parent.document;"
        "if(d.getElementById('seo-jsonld'))return;"
        "var s=d.createElement('script');s.type='application/ld+json';s.id='seo-jsonld';"
        f"s.text={js_literal};d.head.appendChild(s);}}catch(e){{}}}})();</script>",
        height=0,
    )


def onyesha_jibu(res, border_color="#10B981", bg="rgba(16,185,129,0.1)"):
    """Onyesha jibu la AI kwa usalama (escape HTML ili kuzuia XSS)."""
    salama = html.escape(str(res or ""))
    str_platform.markdown(
        f"<div style='background:{bg}; border:1px solid {border_color}; padding:20px; "
        f"border-radius:10px; margin-top:15px; white-space:pre-wrap;'>{salama}</div>",
        unsafe_allow_html=True,
    )


def onyesha_hitilafu(muktadha, e):
    """Andika hitilafu halisi kwenye log ya server; mteja aone ujumbe wa kawaida tu."""
    print(f"[hitilafu] {muktadha}: {type(e).__name__}: {e}")
    t = str(e).lower()
    if any(k in t for k in ("billing", "quota", "429", "rate limit", "insufficient")):
        str_platform.error("Huduma ya AI haipatikani kwa sasa. Tafadhali jaribu tena baadaye.")
    else:
        str_platform.error(f"Imeshindikana {muktadha}. Tafadhali jaribu tena.")


# ------------------------------------------------------------------ #
#  KAMUSI YA DATA (CSV): chanzo cha kwanza cha ukweli kabla ya AI
# ------------------------------------------------------------------ #
# Weka faili la CSV kwenye repo yako, folda moja na app.py, kisha andika jina lake hapa.
KAMUSI_CSV_FILE = "kamusi.csv"
# Mbadala: kiungo kamili cha RAW (https://raw.githubusercontent.com/USER/REPO/main/faili.csv)
# kinaweza kuwekwa kwenye Streamlit Secrets kama KAMUSI_CSV_URL.
KAMUSI_CSV_URL = str(_secret("KAMUSI_CSV_URL") or "").strip()
# Kwa repo ya FARAGHA: weka token ya kusoma tu kwenye Secrets kama KAMUSI_GITHUB_TOKEN.
KAMUSI_GITHUB_TOKEN = str(_secret("KAMUSI_GITHUB_TOKEN") or "").strip()
KAMUSI_SAFU = ["swahili_term", "english_term", "category", "description_sw"]


def _kiungo_cha_api_cha_github(url):
    """raw.githubusercontent.com/OWNER/REPO/REF/PATH -> (api_url, ref), au None."""
    m = re.match(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)(?:\?.*)?$", url)
    if not m:
        return None
    owner, repo, ref, path = m.groups()
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", ref


@str_platform.cache_data(ttl=600, show_spinner=False)
def pakia_kamusi_csv():
    """Hurejesha (DataFrame, kosa). 'kosa' ni None kama yote sawa."""
    tupu = pd.DataFrame(columns=KAMUSI_SAFU)
    njia = os.path.join(os.path.dirname(os.path.abspath(__file__)), KAMUSI_CSV_FILE)
    chanzo = njia if os.path.exists(njia) else (KAMUSI_CSV_URL or None)
    if not chanzo:
        print(f"[kamusi] hakuna chanzo: weka {KAMUSI_CSV_FILE} kwenye repo au KAMUSI_CSV_URL kwenye Secrets")
        return tupu, "no_source"
    try:
        if chanzo == KAMUSI_CSV_URL and KAMUSI_GITHUB_TOKEN:
            # Repo ya faragha: tumia GitHub API (njia rasmi ya token ya fine-grained).
            vichwa = {"Authorization": f"Bearer {KAMUSI_GITHUB_TOKEN}"}
            api = _kiungo_cha_api_cha_github(chanzo)
            if api:
                vichwa.update({"Accept": "application/vnd.github.raw+json", "X-GitHub-Api-Version": "2022-11-28"})
                r = requests.get(api[0], params={"ref": api[1]}, headers=vichwa, timeout=20)
            else:
                r = requests.get(chanzo, headers=vichwa, timeout=20)
            if r.status_code != 200:
                print(f"[kamusi] GitHub ilijibu {r.status_code}: {r.text[:200]}")
                return tupu, "read_error"
            df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")), dtype=str).fillna("")
        else:
            df = pd.read_csv(chanzo, dtype=str, encoding="utf-8-sig").fillna("")
    except Exception as e:
        print(f"[kamusi] imeshindwa kusoma CSV: {type(e).__name__}: {e}")
        return tupu, "read_error"
    if "swahili_term" not in df.columns:
        print(f"[kamusi] safu 'swahili_term' haipo. Safu zilizopo: {list(df.columns)}")
        return tupu, "bad_columns"
    for safu in KAMUSI_SAFU:
        if safu not in df.columns:
            df[safu] = ""
    return df, None


def tafuta_kwenye_kamusi_csv(neno, kikomo=20):
    """Hurejesha (matokeo, kosa). Maneno kamili hutangulia, kisha yanayolingana kwa sehemu."""
    df, kosa = pakia_kamusi_csv()
    if kosa:
        return None, kosa
    q = str(neno).strip().lower()
    istilahi = df["swahili_term"].str.lower().str.strip()
    kamili = df[istilahi == q]
    # regex=False: mtumiaji akiandika alama kama "(" au "*" isilete hitilafu
    sehemu = df[istilahi.str.contains(q, regex=False) & (istilahi != q)]
    return pd.concat([kamili, sehemu]).head(kikomo), None


def onyesha_matokeo_ya_kamusi(matokeo):
    for _, r in matokeo.iterrows():
        str_platform.success(f"**Neno la Kiswahili:** {r['swahili_term']}")
        str_platform.write(f"**Tafsiri ya Kiingereza (English):** *{r['english_term']}*")
        if r["category"]:
            str_platform.write(f"**Kundi (Category):** {r['category']}")
        if r["description_sw"]:
            str_platform.info(f"**Maelezo ya Kiswahili:** {r['description_sw']}")
        str_platform.markdown("---")


try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception as exc:
    str_platform.error("Imeshindikana kuanzisha hifadhidata. Kagua usanidi wa database kisha jaribu tena.")
    # Maelezo ya kiufundi yanaonyeshwa kwenye log ya server, si kwa mtumiaji.
    print(f"Database initialization failed: {type(exc).__name__}: {exc}")
    str_platform.stop()

skin_appearance.inject_premium_glassmorphic_skin()

# DOSARI 3 IMEREKEBISHWA: soma secrets kwa usalama (haitaanguka ukiwa local)
api_key_source = os.environ.get("OPENAI_API_KEY") or _secret("OPENAI_API_KEY")

if isinstance(api_key_source, str) and api_key_source.strip():
    client = OpenAI(api_key=api_key_source.strip())
    ubongo = CerebralCortex(client)
else:
    str_platform.error("\U0001F512 secrets error! Weka OPENAI_API_KEY kwenye Secrets."); str_platform.stop()

weka_seo_schema()
skin_appearance.render_top_revenue_banner()

str_platform.markdown("<h1 style='text-align: center; color: #D97706; font-size: 46px; margin-bottom: 0; font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>\U0001F451 Lingual Africa Sanifu</h1>", unsafe_allow_html=True)
str_platform.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; margin-top: 5px; letter-spacing: 3px;'>HUDUMA YA OURWORTHLINKS BUSINESS \u2022 THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>", unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

if "freemium_words_used" not in str_platform.session_state:
    str_platform.session_state["freemium_words_used"] = 0

maneno_yaliyotumika = str_platform.session_state["freemium_words_used"]
maneno_yaliyobaki = max(0, 50 - maneno_yaliyotumika)

str_platform.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #D97706; padding: 18px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(217,119,6,0.15);'>
    <p style='color: #D97706; font-size: 13px; margin: 0 0 10px 0; text-align: center; font-weight: 900; letter-spacing: 1px;'>\U0001F4CA RADA YA UBONGO (CNS METRICS)</p>
    <p style='color: #F59E0B; font-size: 13px; margin: 0;'>\U0001F381 <b>Salio la Bure:</b> {maneno_yaliyobaki}/50 Maneno</p>
    <p style='color: #34D399; font-size: 13px; margin: 6px 0 0 0;'>\U0001F6E1\uFE0F <b>OWTHS Filter:</b> \U0001F7E2 100% Active</p>
    <p style='color: #34D399; font-size: 13px; margin: 6px 0;'>\u26A1 <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
    <hr style='border-color: rgba(255,255,255,0.05); margin: 8px 0;'>
    <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: {self_healing_status}</p>
</div>
""", unsafe_allow_html=True)

str_platform.sidebar.markdown("<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: 1px; margin-bottom: 5px;'>\U0001F310 HUDUMA ZOTE NNE ZA BIASHARA:</p>", unsafe_allow_html=True)

menyu_kamili = {
    "mhariri": "\U0001F4DD Mhariri wa Kiswahili Sanifu Pro & Real-Time Prompt",
    "mtafsiri": "\U0001F500 Mtafsiri wa Lugha & Muktadha Suite",
    "kamusi": "\U0001F4DA Maktaba ya Kamusi Kuu",
    "sauti": "\U0001F399\uFE0F Roboti wa Sauti, Imla (Transcription) & TTS"
}

# DOSARI 4 IMEREKEBISHWA: label halisi + label_visibility badala ya label=""
chaguo_display = str_platform.sidebar.radio(
    label="Chagua huduma",
    options=list(menyu_kamili.values()),
    key="portal_radio_gate",
    label_visibility="collapsed",
)
chaguo_menyu = [k for k, v in menyu_kamili.items() if v == chaguo_display]

str_platform.sidebar.write("---")

# IMEREKEBISHWA: viungo halisi (kama ni multipage app, hakikisha kurasa zipo kwenye pages/)
str_platform.sidebar.link_button(
    label="\U0001F510 Lango la Malipo na Usajili Mteja \u2500\u2500\u25BA",
    url=f"{APP_URL}/dashboard",
    type="primary",
    use_container_width=True,
    key="client_dashboard_btn_v4"
)
str_platform.sidebar.markdown("<p style='text-align: center; color: #64748B; font-size: 11px; margin-top: 6px;'>\U0001F512 Malipo yanachakatwa salama na <b>Ourworthlinks Business</b> kupitia Pesapal.</p>", unsafe_allow_html=True)

str_platform.sidebar.write("---")

str_platform.sidebar.link_button(
    label="\U0001F39B\uFE0F Fungua Lango la Utawala (Admin) \u2500\u2500\u25BA",
    url=f"{APP_URL}/admin",
    type="secondary",
    use_container_width=True,
    key="admin_dashboard_btn_v4"
)

if "mhariri" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>\U0001F4DD Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode)</h3>", unsafe_allow_html=True)
    maandishi = str_platform.text_area("Andika au bandika maandishi ya Kiswahili hapa:", key="editor_v14_clean_box", height=150, max_chars=MAX_CHARS)
    heabu_maneno = len(maandishi.strip().split()) if maandishi.strip() else 0
    if maneno_yaliyobaki <= 0:
        str_platform.error("\U0001F512 Salio LIMEISHA! Tafadhali fungua Lango la Mteja kulipia.")
    else:
        if str_platform.button("Zindua Ukaguzi wa Sarufi Pro", key="v14_btn_ed_clean"):
            if not maandishi.strip():
                str_platform.warning("Tafadhali andika maandishi kwanza.")
            elif heabu_maneno > maneno_yaliyobaki:
                str_platform.warning(
                    f"Maandishi yana maneno {heabu_maneno}, lakini salio lako ni {maneno_yaliyobaki}. "
                    "Punguza maandishi au fungua Lango la Mteja."
                )
            else:
                with str_platform.spinner("Chakata sarufi..."):
                    try:
                        res = ubongo.chakata_sarufi_pro(maandishi)
                    except Exception as e:
                        res = None
                        onyesha_hitilafu("kuchakata sarufi", e)
                # DOSARI 1 IMEREKEBISHWA: hesabu maneno TU baada ya mafanikio
                if res:
                    str_platform.session_state["freemium_words_used"] += heabu_maneno
                    onyesha_jibu(res)  # DOSARI 2 & 5: escape + str()

elif "mtafsiri" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>\U0001F500 Mtafsiri wa Lugha & Muktadha Suite Pro</h3>", unsafe_allow_html=True)
    orodha_lugha = ["Kiswahili", "Kiingereza (English)", "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa", "Kifaransa", "Kiarabu"]
    col1, col2 = str_platform.columns(2)
    with col1: lugha_chanzo = str_platform.selectbox("Kutoka Lugha:", orodha_lugha, index=1, key="src_v14_clean")
    with col2: lugha_lengwa = str_platform.selectbox("Kwenda Lugha:", orodha_lugha, index=0, key="trg_v14_clean")
    muktadha_chaguo = str_platform.selectbox("\U0001F3AF Chagua Muktadha:", ["Kawaida", "Kibiashara", "Kisheria", "Kitiba", "Kielimu"], key="context_v14_clean")
    maandishi_t = str_platform.text_area("Ingiza maandishi ya kutafsiri hapa:", key="trans_v14_clean_box", height=150, max_chars=MAX_CHARS)
    heabu_maneno_t = len(maandishi_t.strip().split()) if maandishi_t.strip() else 0
    if maneno_yaliyobaki <= 0:
        str_platform.error("\U0001F512 Salio LIMEISHA! Tafadhali fungua Lango la Mteja kulipia.")
    else:
        if str_platform.button("Zindua Tafsiri Pro", key="v14_btn_tr_clean"):
            if not maandishi_t.strip():
                str_platform.warning("Tafadhali ingiza maandishi ya kutafsiri kwanza.")
            elif heabu_maneno_t > maneno_yaliyobaki:
                str_platform.warning(
                    f"Maandishi yana maneno {heabu_maneno_t}, lakini salio lako ni {maneno_yaliyobaki}. "
                    "Punguza maandishi au fungua Lango la Mteja."
                )
            else:
                with str_platform.spinner("Processing..."):
                    try:
                        res = ubongo.chakata_tafsiri_pacha(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)
                    except Exception as e:
                        res = None
                        onyesha_hitilafu("kutafsiri", e)
                if res:
                    str_platform.session_state["freemium_words_used"] += heabu_maneno_t
                    onyesha_jibu(res, border_color="rgba(255,255,255,0.1)", bg="rgba(255,255,255,0.02)")

elif "kamusi" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>\U0001F4DA Maktaba ya Msamiati na Kamusi Kuu</h3>", unsafe_allow_html=True)
    msamiati = str_platform.text_input("Andika neno la Kiswahili hapa:", key="kamusi_input_v14_clean", max_chars=100)
    if str_platform.button("Tafuta Kwenye Kamusi Kuu", key="v14_btn_kam_clean"):
        if msamiati.strip() != "":
            matokeo_csv, kosa_csv = tafuta_kwenye_kamusi_csv(msamiati)
            if matokeo_csv is not None and not matokeo_csv.empty:
                str_platform.caption("Chanzo: Kamusi ya Lingual Africa")
                onyesha_matokeo_ya_kamusi(matokeo_csv)
            else:
                if kosa_csv:
                    str_platform.info("Kamusi ya Lingual Africa haipatikani kwa sasa. Hapa chini ni pendekezo la AI (halijahakikiwa).")
                else:
                    str_platform.warning("Neno hilo halijapatikana kwenye Kamusi ya Lingual Africa. Hapa chini ni pendekezo la AI (halijahakikiwa).")
                with str_platform.spinner("Searching..."):
                    try:
                        res = ubongo.chakata_kamusi_kuu(msamiati, database)
                    except Exception as e:
                        res = None
                        onyesha_hitilafu("kutafuta kwenye kamusi", e)
                if res:
                    onyesha_jibu(res, border_color="#D97706", bg="rgba(255,255,255,0.02)")

elif "sauti" in chaguo_menyu:
    str_platform.markdown("<h3 style='color: #D97706;'>\U0001F399\uFE0F Roboti wa Sauti, Imla (Transcription) & Jifunze Lugha Suite</h3>", unsafe_allow_html=True)
    t_imla, t_jifunze = str_platform.tabs(["\U0001F399\uFE0F Imla na Nakala (Transcription)", "\U0001F50A Jifunze Lugha kwa Sauti"])
    with t_imla:
        audio_file = str_platform.file_uploader("Pakia Faili la Sauti (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"], key="whisper_audio_uploader")
        if audio_file is not None:
            aina_sauti = audio_file.type or "audio/mpeg"
            str_platform.audio(audio_file, format=aina_sauti)
            if str_platform.button("Zindua Whisper-v3 Imla Pro", key="zindua_whisper_v3_btn"):
                with str_platform.spinner("Auditory Cortex inasoma sauti..."):
                    try:
                        res_sauti = ubongo.chakata_sauti_na_imla(audio_file)
                    except Exception as e:
                        res_sauti = None
                        onyesha_hitilafu("kuandika imla", e)
                if res_sauti:
                    str_platform.success("\u2728 Imla Imekamilika!")
                    onyesha_jibu(res_sauti)
    with t_jifunze:
        maandishi_sauti = str_platform.text_area("Ingiza maandishi unayotaka kusikia:", value="Karibu kwenye chombo cha Ourworthlinks Business.", key="tts_input_box", max_chars=MAX_CHARS)
        lugha_tutorial = str_platform.selectbox("Lugha ya Matamshi:", ["Kiswahili", "Kiingereza", "Kifaransa"], key="tts_lang_select")
        if str_platform.button("Zalisha Sauti Pro", key="zalisha_tts_btn"):
            with str_platform.spinner("Generating..."):
                try:
                    audio_bytes = ubongo.zindua_jifunze_lugha_audio(maandishi_sauti, lugha_tutorial)
                except Exception as e:
                    audio_bytes = None
                    onyesha_hitilafu("kuzalisha sauti", e)
            if audio_bytes:
                str_platform.audio(audio_bytes, format="audio/mp3")

str_platform.write("---")
skin_appearance.render_bottom_revenue_banner()
