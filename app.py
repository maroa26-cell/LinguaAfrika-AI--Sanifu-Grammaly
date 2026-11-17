
import streamlit as str_platform
import os
import time
import io
import wave
import numpy as np
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
import mhariri_pro_ui
import sarufi_bridge
import skin_appearance
from cerebral_cortex import CerebralCortex, orodha_ya_lahaja, SAUTI_ZA_GEMINI, KASI_ZA_SAUTI

muda_mwanzo = time.time()
self_healing_status = "\U0001F7E2 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Lingual Africa Sanifu", page_icon="\U0001F9E0",
                             layout="wide", initial_sidebar_state="expanded")

_APP_URL_MSINGI = "https://linguaafrika-ai--sanifu-grammaly-m5xtj9pydnpe2qibp2jezc.streamlit.app"
MAX_CHARS = 5000

MISIMBO_YA_IMLA = {
    "Kiswahili": "sw", "Kiingereza (English)": "en", "Kifaransa": "fr", "Kiarabu": "ar",
    "Kichina (Mandarin)": "zh", "Kireno (Portugu\u00eas)": "pt", "Kizulu (isiZulu)": "zu",
    "Setswana (Botswana)": "tn", "Kinyarwanda": "rw", "Kiganda (Luganda)": "lg",
    "Lingala": "ln", "Kichewa": "ny",
}


def _secret(jina):
    try:
        return str_platform.secrets.get(jina)
    except Exception:
        return None


APP_URL = str(_secret("APP_URL") or _APP_URL_MSINGI).strip().rstrip("/")


def weka_seo_schema():
    data = {
        "@context": "https://schema.org", "@type": "DefinedTermSet",
        "@id": f"{APP_URL}/#kamusi", "url": APP_URL,
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


class _FailiLaSauti(io.BytesIO):
    def __init__(self, data, name="sauti.wav", type_="audio/wav"):
        super().__init__(data)
        self.name = name
        self.type = type_


def boresha_sauti_wav(data, lengo_rms=0.12, kikomo_cha_kuongeza=40.0):
    try:
        with wave.open(io.BytesIO(data), "rb") as w:
            ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            raw = w.readframes(n)
        if sw != 2 or n == 0:
            return data, 0.0
        x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
        x = x - x.mean()
        fr = max(int(sr * 0.05) * ch, 1)
        k = len(x) // fr
        if k == 0:
            return data, 0.0
        rms_fr = np.sqrt((x[:k * fr].reshape(k, fr) ** 2).mean(axis=1))
        if rms_fr.max() < 0.002:
            return data, 0.0
        hai = rms_fr[rms_fr > rms_fr.max() * 0.1]
        rms_hai = float(np.sqrt((hai ** 2).mean()))
        gain = min(max(lengo_rms / max(rms_hai, 1e-6), 1.0), kikomo_cha_kuongeza)
        if gain < 1.1:
            return data, 0.0
        y = np.tanh(x * gain)
        out = io.BytesIO()
        with wave.open(out, "wb") as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((y * 32767).astype("<i2").tobytes())
        return out.getvalue(), float(20 * np.log10(gain))
    except Exception:
        return data, 0.0


def gawa_wav_vipande(data, sekunde=300):
    try:
        with wave.open(io.BytesIO(data), "rb") as w:
            ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            raw = w.readframes(n)
        if sw != 2 or n <= sr * sekunde * 1.2:
            return [data]
        x = np.frombuffer(raw, dtype="<i2").reshape(-1, ch)
        blok = int(sr * 0.1)
        mipaka, mwanzo = [], 0
        while len(x) - mwanzo > sr * sekunde * 1.2:
            lengo = mwanzo + sr * sekunde
            dirisha = x[lengo - sr * 8: lengo].astype(np.float32)
            kb = len(dirisha) // blok
            nishati = np.abs(dirisha[:kb * blok]).reshape(kb, blok * ch).mean(axis=1)
            kata = lengo - sr * 8 + int(nishati.argmin()) * blok
            mipaka.append((mwanzo, kata)); mwanzo = kata
        mipaka.append((mwanzo, len(x)))
        vipande = []
        for a, b in mipaka:
            out = io.BytesIO()
            with wave.open(out, "wb") as w:
                w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
                w.writeframes(x[a:b].tobytes())
            vipande.append(out.getvalue())
        return vipande
    except Exception:
        return [data]


def onyesha_jibu(res, border_color="#10B981", bg="rgba(16,185,129,0.1)"):
    salama = html.escape(str(res or ""))
    str_platform.markdown(
        f"<div style='background:{bg}; border:1px solid {border_color}; padding:20px; "
        f"border-radius:10px; margin-top:15px; white-space:pre-wrap;'>{salama}</div>",
        unsafe_allow_html=True)


def _ai_debug_imewashwa():
    return str(_secret("AI_DEBUG") or "").strip().lower() in ("1", "true", "yes", "ndiyo")


def onyesha_hitilafu(muktadha, e):
    print(f"[hitilafu] {muktadha}: {type(e).__name__}: {e}")
    if isinstance(e, ValueError):
        str_platform.error(str(e))
        return
    t = str(e).lower()
    if _ai_debug_imewashwa():
        str_platform.error(f"❌ Kosa la AI ({muktadha}): {type(e).__name__} - {str(e)}")
        return
    if any(k in t for k in ("billing", "quota", "429", "rate limit", "insufficient")):
        str_platform.error("Huduma ya AI haipatikani kwa sasa. Tafadhali jaribu tena baadaye.")
    else:
        str_platform.error(f"Imeshindikana {muktadha}. Tafadhali jaribu tena.")


_HERUFI_ZA_CJK = r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]"


def hesabu_maneno(t):
    t = str(t or "")
    cjk = len(re.findall(_HERUFI_ZA_CJK, t))
    bila_cjk = re.sub(_HERUFI_ZA_CJK, " ", t)
    return len(bila_cjk.split()) + (cjk + 1) // 2


def _ep_md(t):
    return re.sub(r"([\\`*_{}\[\]()#+\-.!~|>$])", r"\\\1", str(t))


KAMUSI_CSV_FILE = "kamusi.csv"
KAMUSI_CSV_URL = str(_secret("KAMUSI_CSV_URL") or "").strip()
KAMUSI_GITHUB_TOKEN = str(_secret("KAMUSI_GITHUB_TOKEN") or "").strip()
KAMUSI_SAFU = ["swahili_term", "english_term", "category", "description_sw"]


def _kiungo_cha_api_cha_github(url):
    m = re.match(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)(?:\?.*)?$", url)
    if not m:
        return None
    owner, repo, ref, path = m.groups()
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", ref


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
                vichwa.update({"Accept": "application/vnd.github.raw+json",
                               "X-GitHub-Api-Version": "2022-11-28"})
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


def _pata_kamusi_set():
    """Seti ya swahili_term kwa utatuzi wa anagram. Huhifadhiwa kwenye session_state."""
    if "_kamusi_set_cache" not in str_platform.session_state:
        try:
            df, _ = pakia_kamusi_csv()
            str_platform.session_state["_kamusi_set_cache"] = (
                set(df["swahili_term"].str.lower().str.strip()) if not df.empty else set()
            )
        except Exception:
            str_platform.session_state["_kamusi_set_cache"] = set()
    return str_platform.session_state["_kamusi_set_cache"]


def tafuta_kwenye_kamusi_csv(neno, kikomo=20):
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
        str_platform.markdown("---")


try:
    database.anzisha_hifadhidata_ya_chuma()
except Exception as exc:
    str_platform.error("Imeshindikana kuanzisha hifadhidata. Kagua usanidi wa database kisha jaribu tena.")
    print(f"Database initialization failed: {type(exc).__name__}: {exc}")
    str_platform.stop()

skin_appearance.inject_premium_glassmorphic_skin()

api_key_source = os.environ.get("OPENAI_API_KEY") or _secret("OPENAI_API_KEY")
client = None
if isinstance(api_key_source, str) and api_key_source.strip():
    client = OpenAI(api_key=api_key_source.strip())
ubongo = CerebralCortex(client)

if not (ubongo.gemini_client or ubongo.groq_client or ubongo.openai_client):
    str_platform.error("\U0001F512 secrets error! Weka angalau ufunguo mmoja kwenye Secrets: "
                       "GEMINI_API_KEY, GROQ_API_KEY au OPENAI_API_KEY.")
    str_platform.stop()


def _piga_ai(mfumo, mtumiaji):
    return ubongo.piga_json(mfumo, mtumiaji)


def _piga_ai_kina(mfumo, mtumiaji):
    return ubongo.piga_json_kina(mfumo, mtumiaji)


_UTHIBITISHO_WA_PRO = bool(getattr(ubongo, "gemini_pro_modeli", ""))


weka_seo_schema()
skin_appearance.render_top_revenue_banner()

str_platform.markdown(
    "<h1 style='text-align: center; color: #D97706; font-size: 46px; margin-bottom: 0; "
    "font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>\U0001F451 Lingual Africa Sanifu</h1>",
    unsafe_allow_html=True)
str_platform.markdown(
    "<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; "
    "margin-top: 5px; letter-spacing: 3px;'>HUDUMA YA OURWORTHLINKS BUSINESS \u2022 "
    "THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>",
    unsafe_allow_html=True)
str_platform.write("---")

kasi_ya_radi = (time.time() - muda_mwanzo) * 1000

if "freemium_words_used" not in str_platform.session_state:
    str_platform.session_state["freemium_words_used"] = 0

maneno_yaliyotumika = str_platform.session_state["freemium_words_used"]
maneno_yaliyobaki = max(0, 600 - maneno_yaliyotumika)
rada_nafasi = str_platform.sidebar.empty()


def onyesha_rada():
    baki = max(0, 600 - str_platform.session_state["freemium_words_used"])
    kodi = f"""
    <div style='background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #D97706; padding: 18px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(217,119,6,0.15);'>
        <p style='color: #D97706; font-size: 13px; margin: 0 0 10px 0; text-align: center; font-weight: 900; letter-spacing: 1px;'>\U0001F4CA RADA YA UBONGO (CNS METRICS)</p>
        <p style='color: #F59E0B; font-size: 13px; margin: 0;'>\U0001F381 <b>Salio la Bure:</b> {baki}/600 Maneno</p>
        <p style='color: #34D399; font-size: 13px; margin: 6px 0 0 0;'>\U0001F6E1\uFE0F <b>OWTHS Filter:</b> \U0001F7E2 100% Active</p>
        <p style='color: #34D399; font-size: 13px; margin: 6px 0;'>\u26A1 <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
        <hr style='border-color: rgba(255,255,255,0.05); margin: 8px 0;'>
        <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: {self_healing_status}</p>
    </div>
    """
    rada_nafasi.markdown("".join(l.strip() for l in kodi.splitlines()), unsafe_allow_html=True)


onyesha_rada()

str_platform.sidebar.markdown(
    "<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: 1px; "
    "margin-bottom: 5px;'>\U0001F310 HUDUMA ZOTE NNE ZA BIASHARA:</p>",
    unsafe_allow_html=True)

menyu_kamili = {
    "mhariri": "\U0001F4DD Mhariri wa Kiswahili Sanifu Pro & Real-Time Prompt",
    "mtafsiri": "\U0001F500 Mtafsiri wa Lugha & Muktadha Suite",
    "kamusi": "\U0001F4DA Maktaba ya Kamusi Kuu",
    "sauti": "\U0001F399\uFE0F Roboti wa Sauti, Imla (Transcription) & TTS",
}

chaguo_display = str_platform.sidebar.radio(
    label="Chagua huduma",
    options=list(menyu_kamili.values()),
    key="portal_radio_gate",
    label_visibility="collapsed",
)
chaguo_menyu = [k for k, v in menyu_kamili.items() if v == chaguo_display]

str_platform.sidebar.write("---")
str_platform.sidebar.link_button(
    label="\U0001F510 Lango la Malipo na Usajili Mteja \u2500\u2500\u25BA",
    url=f"{APP_URL}/dashboard", type="primary",
    use_container_width=True, key="client_dashboard_btn_v4")
str_platform.sidebar.markdown(
    "<p style='text-align: center; color: #64748B; font-size: 11px; margin-top: 6px;'>"
    "\U0001F512 Malipo yanachakatwa salama na <b>Ourworthlinks Business</b> kupitia Pesapal.</p>",
    unsafe_allow_html=True)
str_platform.sidebar.write("---")
str_platform.sidebar.link_button(
    label="\U0001F39B\uFE0F Fungua Lango la Utawala (Admin) \u2500\u2500\u25BA",
    url=f"{APP_URL}/admin", type="secondary",
    use_container_width=True, key="admin_dashboard_btn_v4")


def _futa_pc():
    for k in [k for k in list(str_platform.session_state.keys()) if str(k).startswith("pc_")]:
        del str_platform.session_state[k]


def _fanya_tafsiri(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo):
    maneno = hesabu_maneno(maandishi_t)
    baki = max(0, 600 - str_platform.session_state["freemium_words_used"])
    if maneno > baki:
        str_platform.warning(
            f"Maandishi yana maneno {maneno}, lakini salio lako ni {baki}. "
            "Punguza maandishi au fungua Lango la Mteja.")
        return
    with str_platform.spinner("Processing..."):
        try:
            res = ubongo.chakata_tafsiri_pacha(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)
        except Exception as e:
            res = None
            onyesha_hitilafu("kutafsiri", e)
    if res:
        str_platform.session_state["freemium_words_used"] += maneno
        str_platform.session_state["tafsiri_ya_mwisho"] = {
            "chanzo": lugha_chanzo, "lengo": lugha_lengwa,
            "asili": maandishi_t, "tafsiri": res,
        }
        str_platform.session_state.pop("tafsiri_sauti_lengo", None)
        str_platform.session_state.pop("tafsiri_sauti_asili", None)
        onyesha_rada()


def _pc_endelea(sahihisha):
    pc = str_platform.session_state.pop("tafsiri_precheck", None)
    if not pc:
        return
    text = pc["text"]
    if sahihisha:
        chaguliwa = {x["id"] for x in pc["issues"]
                     if str_platform.session_state.get(f"pc_{x['id']}", True)}
        text = mhariri.tumia_marekebisho(text, pc["issues"], chaguliwa)[:MAX_CHARS]
        str_platform.session_state["trans_v14_clean_box"] = text
    str_platform.session_state["tafsiri_inasubiri"] = {
        "text": text, "chanzo": pc["chanzo"], "lengo": pc["lengo"], "muktadha": pc["muktadha"]}
    _futa_pc()


def _pc_ghairi():
    str_platform.session_state.pop("tafsiri_precheck", None)
    _futa_pc()


def _onyesha_precheck(pc):
    str_platform.markdown("---")
    str_platform.warning(
        f"Nimeona makosa {len(pc['issues'])} kwenye maandishi yako ya {pc['chanzo']} kabla ya kutafsiri. "
        "Tafsiri haijaanza, na hakuna maneno yaliyokatwa bado.")
    if pc.get("onyo"):
        str_platform.caption(f"\u26A0\uFE0F {pc['onyo']}")
    if not pc["ai"]:
        str_platform.info("Ukaguzi wa msingi tu (AI haikupatikana kwa sasa).")
    str_platform.markdown(
        mhariri.html_ya_kuonyesha(pc["text"], pc["issues"], rtl=(pc.get("mwelekeo") == "rtl")),
        unsafe_allow_html=True)
    str_platform.markdown("**Chagua marekebisho ya kutumia kabla ya kutafsiri:**")
    for x in pc["issues"]:
        jina = mhariri.KATEGORIA.get(x["category"], ("Mengineyo", ""))[0]
        lebo = (f'{jina}: "{_ep_md(x["original"])}" \u2192 "{_ep_md(x["suggestion"])}". '
                f'{_ep_md(x["explanation"])}')
        str_platform.checkbox(lebo, value=True, key=f"pc_{x['id']}")
    c1, c2, c3 = str_platform.columns(3)
    c1.button("Sahihisha kisha utafsiri", type="primary",
              on_click=_pc_endelea, args=(True,), key="pc_btn_sahihisha")
    c2.button("Tafsiri bila kusahihisha", on_click=_pc_endelea, args=(False,), key="pc_btn_bila")
    c3.button("Ghairi (nitahariri mwenyewe)", on_click=_pc_ghairi, key="pc_btn_ghairi")


if "mhariri" in chaguo_menyu:
    str_platform.markdown(
        "<h3 style='color: #D97706;'>\U0001F4DD Mhariri wa Kiswahili Sanifu Pro (Grammarly Mode)</h3>",
        unsafe_allow_html=True)

    if maneno_yaliyobaki <= 0:
        str_platform.error("\U0001F512 Salio LIMEISHA! Tafadhali fungua Lango la Mteja kulipia.")
    else:
        try:
            matokeo_pro = mhariri_pro_ui.onyesha_mhariri_pro(
                kamusi=_pata_kamusi_set(),
                piga_ai=_piga_ai,
                piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
                max_chars=MAX_CHARS,
                kikomo_maneno=maneno_yaliyobaki,
            )
            if (matokeo_pro and matokeo_pro.get("text_hash")
                    and matokeo_pro.get("ai_imetumika")):
                h = matokeo_pro["text_hash"]
                if h != str_platform.session_state.get("mhariri_billed_hash"):
                    str_platform.session_state["freemium_words_used"] += matokeo_pro["maneno"]
                    str_platform.session_state["mhariri_billed_hash"] = h
                    onyesha_rada()
        except Exception as e:
            onyesha_hitilafu("kuendesha Mhariri Pro", e)


elif "mtafsiri" in chaguo_menyu:
    str_platform.markdown(
        "<h3 style='color: #D97706;'>\U0001F500 Mtafsiri wa Lugha & Muktadha Suite Pro</h3>",
        unsafe_allow_html=True)

    orodha_lugha = [
        "Kiswahili", "Kiingereza (English)", "Kifaransa", "Kiarabu",
        "Kichina (Mandarin)", "Kireno (Portugu\u00eas)", "Kizulu (isiZulu)", "Setswana (Botswana)",
        "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa",
    ]
    lugha_za_majaribio = {"K
