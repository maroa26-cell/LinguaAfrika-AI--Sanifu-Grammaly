import streamlit as str_platform
import os
import time
import io
import re
import collections
import json
import html
import pandas as pd
import requests
import streamlit.components.v1 as components
from openai import OpenAI
import database
import mhariri
import skin_appearance
from cerebral_cortex import CerebralCortex

muda_mwanzo = time.time()
self_healing_status = "\U0001F7E2 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Lingual Africa Sanifu", page_icon="\U0001F9E0", layout="wide", initial_sidebar_state="expanded")

# URL HALISI ya app yako (ilikuwa 'https://streamlit.app' - si sahihi)
_APP_URL_MSINGI = "https://streamlit.app"

# Kikomo cha herufi kwa kila ingizo (kuzuia matumizi mabaya / gharama kubwa)
MAX_CHARS = 5000

# Kikomo cha maneno ya bure kwa kipindi cha majaribio
FREEMIUM_WORD_LIMIT = 500


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
    """Weka alama za JSON-LD (schema.org) kwenye <head> ya ukurasa."""
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
    kodi_html = (
        "<script>(function(){try{var d=window.parent.document;"
        "if(d.getElementById('seo-jsonld'))return;"
        "var s=d.createElement('script');s.type='application/ld+json';s.id='seo-jsonld';"
        f"s.text={js_literal};d.head.appendChild(s);}}catch(e){{}}}})();</script>"
    )
    try:
        if hasattr(str_platform, "iframe"):
            str_platform.iframe(kodi_html, height=1)
        else:
            components.html(kodi_html, height=0)
    except Exception as e:
        print(f"[seo] imeshindwa kuweka JSON-LD: {type(e).__name__}: {e}")


def onyesha_jibu(res, border_color="#10B981", bg="rgba(16,185,129,0.1)"):
    """Onyesha jibu la AI kwa usalama (escape HTML ili kuzuia XSS)."""
    salama = html.escape(str(res or ""))
    str_platform.markdown(
        f"<div style='background:{bg}; border:1px solid {border_color}; padding:20px; "
        f"border-radius:10px; margin-top:15px; white-space:pre-wrap;'>{salama}</div>",
        unsafe_allow_html=True,
    )


def _ai_debug_imewashwa():
    return str(_secret("AI_DEBUG") or "").strip().lower() in ("1", "true", "yes", "ndiyo")


def onyesha_hitilafu(muktadha, e):
    """Andika hitilafu halisi kwenye log ya server; mteja aone ujumbe wa kawaida tu."""
    print(f"[hitilafu] {muktadha}: {type(e).__name__}: {e}")
    if isinstance(e, ValueError):
        str_platform.error(str(e))
        return
    t = str(e).lower()
    if any(k in t for k in ("billing", "quota", "429", "rate limit", "insufficient")):
        str_platform.error("Huduma ya AI haipatikani kwa sasa. Tafadhali jaribu tena baadaye.")
    else:
        str_platform.error(f"Imeshindikana {muktadha}. Tafadhali jaribu tena.")
    if _ai_debug_imewashwa():
        str_platform.warning(f"[uchunguzi AI] {muktadha} | {type(e).__name__}: {str(e)[:300]}")


_HERUFI_ZA_CJK = r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]"


def hesabu_maneno(t):
    """Maneno ya kukata kwenye salio. Kichina hakina nafasi kati ya maneno, kwa hiyo herufi 2 za CJK = neno 1."""
    t = str(t or "")
    cjk = len(re.findall(_HERUFI_ZA_CJK, t))
    bila_cjk = re.sub(_HERUFI_ZA_CJK, " ", t)
    return len(bila_cjk.split()) + (cjk + 1) // 2


def _ep_md(t):
    """Epuka alama za markdown ndani ya maandishi ya mtumiaji."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!~|>$])", r"\\\1", str(t))


def onyesha_matokeo_ya_mhariri():
    """Onyesha matokeo ya ukaguzi (yamehifadhiwa kwenye session ili vitufe vya kuchagua vidumu)."""
    m = str_platform.session_state.get("mhariri_matokeo")
    if not m:
        return
    text, matatizo = m["text"], m["issues"]
    str_platform.markdown("---")
    if not m["ai_imetumika"]:
        str_platform.info("Ukaguzi wa msingi tu (AI haipatikani kwa sasa). Salio lako halikukatwa.")
    if not matatizo:
        str_platform.success("\u2705 Hakuna makosa yaliyoonekana kwenye maandishi haya.")
        return
    idadi = collections.Counter(x["category"] for x in matatizo)
    safu = str_platform.columns(len(mhariri.KATEGORIA) + 1)
    safu[0].metric("Alama (makadirio)", f"{mhariri.alama(text, len(matatizo))}/100")
    for n, (kat, (jina, _)) in enumerate(mhariri.KATEGORIA.items(), 1):
        safu[n].metric(jina, idadi.get(kat, 0))
    str_platform.caption("Maandishi yaliyokaguliwa. Elea juu ya sehemu iliyoalamishwa kuona maelezo.")
    str_platform.markdown(mhariri.html_ya_kuonyesha(text, matatizo), unsafe_allow_html=True)
    str_platform.markdown("**Chagua marekebisho ya kutumia:**")
    chaguliwa = set()
    for x in matatizo:
        jina = mhariri.KATEGORIA.get(x["category"], ("Mengineyo", ""))[0]
        lebo = f'{jina}: "{_ep_md(x["original"])}" \u2192 "{_ep_md(x["suggestion"])}". {_ep_md(x["explanation"])}'
        if str_platform.checkbox(lebo, value=True, key=f"mh_{x['id']}"):
            chaguliwa.add(x["id"])
    str_platform.markdown("**Maandishi yaliyosahihishwa** (bonyeza ikoni ya kunakili):")
    str_platform.code(mhariri.tumia_marekebisho(text, matatizo, chaguliwa), language=None)


# ------------------------------------------------------------------ #
#  KAMUSI YA DATA (CSV): chanzo cha kwanza cha ukweli kabla ya AI
# ------------------------------------------------------------------ #
KAMUSI_CSV_FILE = "kamusi.csv"
KAMUSI_CSV_URL = str(_secret("KAMUSI_CSV_URL") or "").strip()
KAMUSI_GITHUB_TOKEN = str(_secret("KAMUSI_GITHUB_TOKEN") or "").strip()
KAMUSI_SAFU = ["swahili_term", "english_term", "category", "description_sw"]


def _kiungo_cha_api_cha_github(url):
    """://githubusercontent.com -> (api_url, ref), au None."""
    m = re.match(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)(?:\?.*)?$", url)
    if not m:
        return None
    owner, repo, ref, path = m.groups()
    return f"https://github.com{owner}/{repo}/contents/{path}", ref


def pakia_kamusi_csv():
    try:
        return _pakia_kamusi_iliyofanikiwa(), None
    except RuntimeError as e:
        return pd.DataFrame(columns=KAMUSI_SAFU), str(e)


@str_platform.cache_data(ttl=600, show_spinner=False)
def _pakia_kamusi_iliyofanikiwa():
    df, kosa = _soma_kamusi_csv()
    if kosa:
        raise RuntimeError(kosa)
    return df


def _soma_kamusi_csv():
    """Husoma CSV (faili la repo au kiungo). Hurejesha (DataFrame, kosa)."""
    tupu = pd.DataFrame(columns=KAMUSI_SAFU)
    njia = os.path.join(os.path.dirname(os.path.abspath(__file__)), KAMUSI_CSV_FILE)
    chanzo = njia if os.path.exists(njia) else (KAMUSI_CSV_URL or None)
    if not chanzo:
        print(f"[kamusi] hakuna chanzo: weka {KAMUSI_CSV_FILE} kwenye repo au KAMUSI_CSV_URL kwenye Secrets")
        return tupu, "no_source"
    try:
        if chanzo == KAMUSI_CSV_URL and KAMUSI_GITHUB_TOKEN:
            vichwa = {"Authorization": f"Bearer {KAMUSI_GITHUB_TOKEN}"}
            api = _kiungo_cha_api_cha_github(chanzo)
            if api:
                vichwa.update({"Accept": "application/vnd.github.raw+json", "X-GitHub-Api-Version": "2022-11-28"})
                r = requests.get(api[0], params={"ref": api[1]}, headers=vichwa, timeout=20)
            else:
                r = requests.get(chanzo, headers=vichwa, timeout=20)
            if r.status_code != 200:
                print(f"[kamusi] GitHub ilijibu {r.status_code}: {r.text[:200]}")
                return tupu, f"read_error:HTTP_{r.status_code}"
            df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")), dtype=str).fillna("")
        else:
            df = pd.read_csv(chanzo, dtype=str, encoding="utf-8-sig").fillna("")
    except Exception as e:
        print(f"[kamusi] imeshindwa kusoma CSV: {type(e).__name__}: {e}")
        return tupu, f"read_error:{type(e).__name__}"
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

