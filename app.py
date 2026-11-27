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
import muhtasari
import sarufi_bridge
import skin_appearance
import ukaguzi_wa_pili
import youtube_imla
import i18n
from i18n import language_selector, ensure_ready, tr
from cerebral_cortex import CerebralCortex, orodha_ya_lahaja, SAUTI_ZA_GEMINI, KASI_ZA_SAUTI

muda_mwanzo = time.time()
self_healing_status = "\U0001F7E2 autonomous shield: active & healthy"
str_platform.set_page_config(page_title="Lingual Africa Sanifu", page_icon="\U0001F9E0",
                             layout="wide", initial_sidebar_state="expanded")

# --- Kibadilisha lugha ya kiolesura (sidebar). Lazima kiitwe mara moja, mwanzoni. ---
language_selector()
# Kiarabu: herufi zilizounganishwa huharibika kukiwa na letter-spacing, kwa hiyo tunaiondoa
_LS3 = "0" if i18n.is_rtl() else "3px"
_LS1 = "0" if i18n.is_rtl() else "1px"

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
        # components.html pekee: haiachi kipande kinachoonekana kama st.iframe(height=1)
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
    ujumbe = str(e).lower()
    if _ai_debug_imewashwa():
        str_platform.error(f"❌ Kosa la AI ({muktadha}): {type(e).__name__} - {str(e)}")
        return
    if any(k in ujumbe for k in ("billing", "quota", "429", "rate limit", "insufficient")):
        str_platform.error(tr("ai_unavailable"))
    else:
        str_platform.error(tr("op_failed"))


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
        str_platform.success(tr("dict_swahili_word", neno=r["swahili_term"]))
        str_platform.write(tr("dict_english_translation", neno=r["english_term"]))
        if r["category"]:
            str_platform.write(tr("dict_category", neno=r["category"]))
        if r["description_sw"]:
            str_platform.info(tr("dict_description", neno=r["description_sw"]))
        str_platform.markdown("---")


# --- Hifadhidata: inaanzishwa MARA MOJA kwa kila mchakato wa seva (si kila bonyezo) ---
@str_platform.cache_resource(show_spinner=False)
def _anzisha_db():
    database.anzisha_hifadhidata_ya_chuma()
    return True


try:
    _anzisha_db()
except Exception as exc:
    str_platform.error(tr("db_error"))
    print(f"Database initialization failed: {type(exc).__name__}: {exc}")
    str_platform.stop()

skin_appearance.inject_premium_glassmorphic_skin()

# --- CerebralCortex: inaundwa MARA MOJA kwa kila kipindi cha mtumiaji (si kila bonyezo) ---
if "_ubongo_kipindi" not in str_platform.session_state:
    api_key_source = os.environ.get("OPENAI_API_KEY") or _secret("OPENAI_API_KEY")
    client = None
    if isinstance(api_key_source, str) and api_key_source.strip():
        client = OpenAI(api_key=api_key_source.strip())
    str_platform.session_state["_ubongo_kipindi"] = CerebralCortex(client)
ubongo = str_platform.session_state["_ubongo_kipindi"]

if not (ubongo.gemini_client or ubongo.groq_client or ubongo.openai_client):
    # Usihifadhi ubongo usio na funguo: mtumiaji akiongeza Secrets ajaribu tena upya
    str_platform.session_state.pop("_ubongo_kipindi", None)
    str_platform.error(tr("secrets_error"))
    str_platform.stop()


def _piga_ai(mfumo, mtumiaji):
    return ubongo.piga_json(mfumo, mtumiaji)


def _piga_ai_kina(mfumo, mtumiaji):
    return ubongo.piga_json_kina(mfumo, mtumiaji)


_UTHIBITISHO_WA_PRO = bool(getattr(ubongo, "gemini_pro_modeli", ""))

# Tafsiri ya maandishi ya ziada ya kiolesura kwa lugha iliyochaguliwa (mara moja kwa kila lugha)
ensure_ready(_piga_ai)

weka_seo_schema()
skin_appearance.render_top_revenue_banner()

str_platform.markdown(
    "<h1 style='text-align: center; color: #D97706; font-size: 46px; margin-bottom: 0; "
    "font-weight: 900; text-shadow: 0 0 40px rgba(217,119,6,0.3);'>\U0001F451 Lingual Africa Sanifu</h1>",
    unsafe_allow_html=True)
str_platform.markdown(
    f"<p style='text-align: center; color: #94A3B8; font-size: 14px; font-weight: 700; "
    f"margin-top: 5px; letter-spacing: {_LS3};'>{html.escape(tr('tagline_service'))} \u2022 "
    f"THE AUTONOMOUS BIOMIMETIC WEB APPLICATION</p>",
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
    rada_kichwa = html.escape(tr("rada_title"))
    rada_salio = html.escape(tr("free_balance"))
    rada_maneno = html.escape(tr("words_unit"))
    kodi = f"""
    <div style='background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #D97706; padding: 18px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(217,119,6,0.15);'>
        <p style='color: #D97706; font-size: 13px; margin: 0 0 10px 0; text-align: center; font-weight: 900; letter-spacing: {_LS1};'>{rada_kichwa}</p>
        <p style='color: #F59E0B; font-size: 13px; margin: 0;'>\U0001F381 <b>{rada_salio}:</b> {baki}/600 {rada_maneno}</p>
        <p style='color: #34D399; font-size: 13px; margin: 6px 0 0 0;'>\U0001F6E1\uFE0F <b>OWTHS Filter:</b> \U0001F7E2 100% Active</p>
        <p style='color: #34D399; font-size: 13px; margin: 6px 0;'>\u26A1 <b>Synapse Latency:</b> {kasi_ya_radi:.3f}ms</p>
        <hr style='border-color: rgba(255,255,255,0.05); margin: 8px 0;'>
        <p style='color: #94A3B8; font-size: 11px; margin: 0; text-align: center;'>Status: {self_healing_status}</p>
    </div>
    """
    rada_nafasi.markdown("".join(l.strip() for l in kodi.splitlines()), unsafe_allow_html=True)


onyesha_rada()

str_platform.sidebar.markdown(
    f"<p style='color: #94A3B8; font-size: 12px; font-weight: 800; letter-spacing: {_LS1}; "
    f"margin-bottom: 5px;'>{html.escape(tr('services_heading'))}</p>",
    unsafe_allow_html=True)

# Huduma zinatambuliwa kwa majina ya ndani yasiyobadilika (mhariri, mtafsiri, kamusi, sauti);
# lebo inayoonekana inatafsiriwa kwa lugha iliyochaguliwa.
MENYU_IDS = ["mhariri", "mtafsiri", "kamusi", "sauti"]
MENYU_EMOJI = {
    "mhariri": "\U0001F4DD", "mtafsiri": "\U0001F500",
    "kamusi": "\U0001F4DA", "sauti": "\U0001F399\uFE0F",
}

chaguo_id = str_platform.sidebar.radio(
    label=tr("choose_service"),
    options=MENYU_IDS,
    format_func=lambda k: f"{MENYU_EMOJI[k]} {tr('svc_' + k)}",
    key="portal_radio_v2",
    label_visibility="collapsed",
)
chaguo_menyu = [chaguo_id]

str_platform.sidebar.write("---")
str_platform.sidebar.link_button(
    label=tr("pay_btn"),
    url=f"{APP_URL}/dashboard", type="primary",
    use_container_width=True, key="client_dashboard_btn_v4")
str_platform.sidebar.markdown(
    f"<p style='text-align: center; color: #64748B; font-size: 11px; margin-top: 6px;'>"
    f"{tr('pay_note')}</p>",
    unsafe_allow_html=True)
str_platform.sidebar.write("---")
str_platform.sidebar.link_button(
    label=tr("admin_btn"),
    url=f"{APP_URL}/admin", type="secondary",
    use_container_width=True, key="admin_dashboard_btn_v4")


def _futa_pc():
    for k in [k for k in list(str_platform.session_state.keys()) if str(k).startswith("pc_")]:
        del str_platform.session_state[k]


def _tafsiri_ya_video(maandishi, kutoka, kwenda):
    """Tafsiri ya matini ya video ya YouTube kutoka kwenye sehemu ya Muhtasari. Inakata salio la maneno."""
    maneno = hesabu_maneno(maandishi)
    baki = max(0, 600 - str_platform.session_state["freemium_words_used"])
    if maneno > baki:
        raise ValueError(tr("video_balance_error", maneno=maneno, baki=baki))
    vipande = muhtasari.gawa_kwa_maneno(maandishi, 400)
    matokeo = [ubongo.chakata_tafsiri_pacha(v, kutoka, kwenda, "Kawaida") for v in vipande]
    str_platform.session_state["freemium_words_used"] += maneno
    onyesha_rada()
    return "\n\n".join(matokeo)


def _fanya_tafsiri(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo):
    maneno = hesabu_maneno(maandishi_t)
    baki = max(0, 600 - str_platform.session_state["freemium_words_used"])
    if maneno > baki:
        str_platform.warning(tr("words_exceed", maneno=maneno, baki=baki))
        return
    with str_platform.spinner(tr("processing")):
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
    str_platform.warning(tr("pc_found", n=len(pc["issues"]), lugha=pc["chanzo"]))
    if pc.get("onyo"):
        str_platform.caption(f"\u26A0\uFE0F {pc['onyo']}")
    if not pc["ai"]:
        str_platform.info(tr("pc_basic_only"))
    str_platform.markdown(
        mhariri.html_ya_kuonyesha(pc["text"], pc["issues"], rtl=(pc.get("mwelekeo") == "rtl")),
        unsafe_allow_html=True)
    str_platform.markdown(tr("pc_choose"))
    for x in pc["issues"]:
        jina = mhariri.KATEGORIA.get(x["category"], ("Mengineyo", ""))[0]
        lebo = (f'{jina}: "{_ep_md(x["original"])}" \u2192 "{_ep_md(x["suggestion"])}". '
                f'{_ep_md(x["explanation"])}')
        str_platform.checkbox(lebo, value=True, key=f"pc_{x['id']}")
    c1, c2, c3 = str_platform.columns(3)
    c1.button(tr("pc_fix_translate"), type="primary",
              on_click=_pc_endelea, args=(True,), key="pc_btn_sahihisha")
    c2.button(tr("pc_translate_anyway"), on_click=_pc_endelea, args=(False,), key="pc_btn_bila")
    c3.button(tr("pc_cancel"), on_click=_pc_ghairi, key="pc_btn_ghairi")


if "mhariri" in chaguo_menyu:
    str_platform.markdown(
        f"<h3 style='color: #D97706;'>{html.escape(tr('title_mhariri'))}</h3>",
        unsafe_allow_html=True)

    if maneno_yaliyobaki <= 0:
        str_platform.error(tr("balance_over"))
    else:
        try:
            # Ukaguzi wa pili (kabla ya kunakili) umo ndani ya mhariri_pro_ui (hautozwi salio)
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

        # Muhtasari wa maandishi ya mwisho (yaliyosahihishwa/kuhaririwa); kama hayapo bado, wa yaliyoandikwa (hautozwi salio)
        muhtasari.onyesha_muhtasari(
            str_platform.session_state.get("pro_maandishi_ya_mwisho")
            or str_platform.session_state.get("pro_maandishi", ""),
            piga_ai=_piga_ai,
            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
            ufunguo="mhariri",
            tafsiri_fn=_tafsiri_ya_video)


elif "mtafsiri" in chaguo_menyu:
    str_platform.markdown(
        f"<h3 style='color: #D97706;'>{html.escape(tr('title_mtafsiri'))}</h3>",
        unsafe_allow_html=True)

    orodha_lugha = [
        "Kiswahili", "Kiingereza (English)", "Kifaransa", "Kiarabu",
        "Kichina (Mandarin)", "Kireno (Portugu\u00eas)", "Kizulu (isiZulu)", "Setswana (Botswana)",
        "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa",
    ]
    lugha_za_majaribio = {"Kizulu (isiZulu)", "Setswana (Botswana)", "Kinyarwanda",
                          "Kiganda (Luganda)", "Lingala", "Kichewa"}

    col1, col2 = str_platform.columns(2)
    with col1:
        lugha_chanzo = str_platform.selectbox(tr("source_language"), orodha_lugha, index=1,
                                              key="src_v14_clean")
    with col2:
        lugha_lengwa = str_platform.selectbox(tr("target_language"), orodha_lugha, index=0,
                                              key="trg_v14_clean")
    if lugha_chanzo in lugha_za_majaribio or lugha_lengwa in lugha_za_majaribio:
        str_platform.caption(tr("beta_caption"))
    # Thamani za muktadha zinabaki za Kiswahili (zinatumika na injini); lebo pekee ndiyo inatafsiriwa
    muktadha_chaguo = str_platform.selectbox(
        tr("context_label"),
        ["Kawaida", "Kibiashara", "Kisheria", "Kitiba", "Kielimu", "Kidini", "Kilimo"],
        format_func=lambda c: tr("ctx_" + c),
        key="context_v14_clean")

    with str_platform.expander(tr("dictation_expander")):
        str_platform.caption(tr("speak_in", lugha=lugha_chanzo))
        if hasattr(str_platform, "audio_input"):
            sauti_imla = str_platform.audio_input(tr("record_prompt"), key="imla_rekodi_v14")
        else:
            sauti_imla = str_platform.file_uploader(tr("upload_audio_label"),
                                                   type=["mp3", "wav", "m4a"], key="imla_pakia_v14")
        _orodha_lahaja_imla = orodha_ya_lahaja(lugha_chanzo)
        lahaja_imla = None
        if len(_orodha_lahaja_imla) > 1:
            lahaja_imla = str_platform.selectbox(tr("dialect_label"), _orodha_lahaja_imla,
                                                key=f"imla_lahaja_v14_{lugha_chanzo}")
        sanifisha_imla = False
        if lugha_chanzo == "Kiswahili":
            sanifisha_imla = str_platform.checkbox(
                tr("sanifisha_label"), key="imla_sanifisha_v14")
        if sauti_imla is not None and str_platform.button(tr("dictate_btn"),
                                                         key="imla_btn_v14"):
            with str_platform.spinner(tr("listening_spinner")):
                try:
                    imla_matini = ubongo.chakata_sauti_na_imla(
                        sauti_imla, MISIMBO_YA_IMLA.get(lugha_chanzo, "sw"),
                        lahaja=lahaja_imla, muktadha=muktadha_chaguo, sanifisha=sanifisha_imla,
                    )
                except Exception as e:
                    imla_matini = None
                    onyesha_hitilafu("kuandika imla", e)
            if imla_matini:
                str_platform.session_state["trans_v14_clean_box"] = imla_matini[:MAX_CHARS]
                str_platform.success(tr("dictation_done"))
                _inj = getattr(ubongo, "injini_ya_imla", None)
                if _inj:
                    str_platform.caption(tr("imla_engine", injini=_inj))

    maandishi_t = str_platform.text_area(
        tr("translate_input"), key="trans_v14_clean_box",
        height=150, max_chars=MAX_CHARS)
    heabu_maneno_t = hesabu_maneno(maandishi_t)

    if maneno_yaliyobaki <= 0:
        str_platform.error(tr("balance_over"))
    else:
        kagua_kwanza = str_platform.checkbox(
            tr("precheck_checkbox"), value=True, key="tr_precheck_v15",
            help=tr("precheck_help"))
        if str_platform.button(tr("launch_translate"), key="v14_btn_tr_clean"):
            str_platform.session_state.pop("tafsiri_precheck", None)
            _futa_pc()
            if not maandishi_t.strip():
                str_platform.warning(tr("empty_warning"))
            elif heabu_maneno_t > maneno_yaliyobaki:
                str_platform.warning(tr("words_exceed", maneno=heabu_maneno_t, baki=maneno_yaliyobaki))
            elif not kagua_kwanza:
                _fanya_tafsiri(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)
            else:
                pk = None
                with str_platform.spinner(tr("precheck_spinner")):
                    try:
                        pk = sarufi_bridge.kagua_pamoja(
                            maandishi_t, piga_ai=_piga_ai,
                            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
                            lugha=lugha_chanzo)
                    except Exception as e:
                        print(f"[tafsiri] ukaguzi wa awali umeshindwa: {type(e).__name__}")
                if pk and pk["issues"]:
                    str_platform.session_state["tafsiri_precheck"] = {
                        "text": maandishi_t, "chanzo": lugha_chanzo, "lengo": lugha_lengwa,
                        "muktadha": muktadha_chaguo,
                        "issues": pk["issues"], "ai": pk["ai_imetumika"],
                        "mwelekeo": pk.get("mwelekeo", "ltr"), "onyo": pk.get("onyo_la_lugha"),
                    }
                else:
                    _fanya_tafsiri(maandishi_t, lugha_chanzo, lugha_lengwa, muktadha_chaguo)

    _inasubiri = str_platform.session_state.pop("tafsiri_inasubiri", None)
    if _inasubiri:
        _fanya_tafsiri(_inasubiri["text"], _inasubiri["chanzo"],
                       _inasubiri["lengo"], _inasubiri["muktadha"])
    _pc = str_platform.session_state.get("tafsiri_precheck")
    if _pc:
        if (_pc["text"], _pc["chanzo"], _pc["lengo"]) != (maandishi_t, lugha_chanzo, lugha_lengwa):
            str_platform.session_state.pop("tafsiri_precheck", None)
            _futa_pc()
        else:
            _onyesha_precheck(_pc)

    _t_mwisho = str_platform.session_state.get("tafsiri_ya_mwisho")
    if _t_mwisho:
        onyesha_jibu(_t_mwisho["tafsiri"], border_color="rgba(255,255,255,0.1)",
                     bg="rgba(255,255,255,0.02)")

        # === UKAGUZI WA PILI === (baada ya tafsiri, kabla mwenye ujumbe hajanakili)
        # Hurudisha tafsiri ya sasa ya mwisho (huenda imesahihishwa); ndiyo inayotumika kwa matamshi.
        _tafsiri_ya_kusema = ukaguzi_wa_pili.onyesha_ukaguzi_wa_pili(
            chanzo=_t_mwisho["asili"],
            matokeo=_t_mwisho["tafsiri"],
            aina="tafsiri",
            lugha=_t_mwisho["lengo"],
            lugha_chanzo=_t_mwisho["chanzo"],
            piga_ai=_piga_ai,
            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
            ufunguo="tafsiri",
            auto_awali=True,
        )

        # Muhtasari (hautozwi salio): wa tafsiri ya mwisho au wa maandishi asili
        # Thamani za radio zinabaki "Tafsiri"/"Maandishi asili" (zinatumika kwenye mantiki); lebo ndiyo inatafsiriwa
        _muh_chanzo = str_platform.radio(
            tr("summary_source_label"), ["Tafsiri", "Maandishi asili"],
            format_func=lambda v: tr("opt_translation") if v == "Tafsiri" else tr("opt_original"),
            key="muh_mtafsiri_chanzo", horizontal=True)
        muhtasari.onyesha_muhtasari(
            _tafsiri_ya_kusema if _muh_chanzo == "Tafsiri" else _t_mwisho["asili"],
            piga_ai=_piga_ai,
            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
            ufunguo="mtafsiri_" + ("t" if _muh_chanzo == "Tafsiri" else "a"),
            tafsiri_fn=_tafsiri_ya_video)

        str_platform.caption(tr("listen_caption"))
        with str_platform.expander(tr("speech_settings")):
            _lh_lengo = orodha_ya_lahaja(_t_mwisho["lengo"])
            _lh_asili = orodha_ya_lahaja(_t_mwisho["chanzo"])
            mk1, mk2 = str_platform.columns(2)
            with mk1:
                lahaja_lengo = (str_platform.selectbox(tr("dialect_translation"), _lh_lengo,
                                                       key=f"lahaja_lengo_{_t_mwisho['lengo']}")
                                if len(_lh_lengo) > 1 else None)
                sauti_chaguo = str_platform.selectbox(tr("voice_label"), SAUTI_ZA_GEMINI,
                                                     key="sauti_chaguo_tafsiri")
            with mk2:
                lahaja_asili = (str_platform.selectbox(tr("dialect_original"), _lh_asili,
                                                       key=f"lahaja_asili_{_t_mwisho['chanzo']}")
                                if len(_lh_asili) > 1 else None)
                kasi_chaguo = str_platform.selectbox(tr("speed_label"), list(KASI_ZA_SAUTI.keys()),
                                                    key="kasi_chaguo_tafsiri")
        sc1, sc2 = str_platform.columns(2)
        with sc1:
            if str_platform.button(tr("listen_translation", lugha=_t_mwisho["lengo"]),
                                   key="sikiliza_tafsiri_btn"):
                with str_platform.spinner(tr("generating_audio")):
                    try:
                        str_platform.session_state["tafsiri_sauti_lengo"] = ubongo.zindua_jifunze_lugha_audio(
                            _tafsiri_ya_kusema, _t_mwisho["lengo"], lahaja=lahaja_lengo,
                            sauti=sauti_chaguo, kasi=kasi_chaguo)
                    except Exception as e:
                        onyesha_hitilafu("kuzalisha sauti ya tafsiri", e)
        with sc2:
            if str_platform.button(tr("listen_original", lugha=_t_mwisho["chanzo"]),
                                   key="sikiliza_asili_btn"):
                with str_platform.spinner(tr("generating_audio")):
                    try:
                        str_platform.session_state["tafsiri_sauti_asili"] = ubongo.zindua_jifunze_lugha_audio(
                            _t_mwisho["asili"], _t_mwisho["chanzo"], lahaja=lahaja_asili,
                            sauti=sauti_chaguo, kasi=kasi_chaguo)
                    except Exception as e:
                        onyesha_hitilafu("kuzalisha sauti ya maandishi asili", e)
        if str_platform.session_state.get("tafsiri_sauti_lengo"):
            str_platform.caption(tr("pron_translation", lugha=_t_mwisho["lengo"]))
            str_platform.audio(str_platform.session_state["tafsiri_sauti_lengo"], format="audio/wav")
        if str_platform.session_state.get("tafsiri_sauti_asili"):
            str_platform.caption(tr("pron_original", lugha=_t_mwisho["chanzo"]))
            str_platform.audio(str_platform.session_state["tafsiri_sauti_asili"], format="audio/wav")


elif "kamusi" in chaguo_menyu:
    str_platform.markdown(
        f"<h3 style='color: #D97706;'>{html.escape(tr('title_kamusi'))}</h3>",
        unsafe_allow_html=True)
    msamiati = str_platform.text_input(tr("dict_input"),
                                       key="kamusi_input_v14_clean", max_chars=100)
    if str_platform.button(tr("dict_search_btn"), key="v14_btn_kam_clean"):
        if msamiati.strip() != "":
            matokeo_csv, kosa_csv = tafuta_kwenye_kamusi_csv(msamiati)
            if kosa_csv and str(_secret("KAMUSI_DEBUG") or "").strip().lower() in ("1", "true", "yes", "ndiyo"):
                _njia = os.path.join(os.path.dirname(os.path.abspath(__file__)), KAMUSI_CSV_FILE)
                str_platform.warning(
                    f"[uchunguzi] kosa: {kosa_csv} | KAMUSI_CSV_URL imewekwa: {bool(KAMUSI_CSV_URL)} | "
                    f"token imewekwa: {bool(KAMUSI_GITHUB_TOKEN)} (urefu: {len(KAMUSI_GITHUB_TOKEN)}, "
                    f"inaanza na github_pat_: {KAMUSI_GITHUB_TOKEN.startswith('github_pat_')}) | "
                    f"faili {KAMUSI_CSV_FILE} kwenye repo: {os.path.exists(_njia)}")
            if matokeo_csv is not None and not matokeo_csv.empty:
                str_platform.caption(tr("dict_source"))
                onyesha_matokeo_ya_kamusi(matokeo_csv)
            else:
                if kosa_csv:
                    str_platform.info(tr("dict_unavailable"))
                else:
                    str_platform.warning(tr("dict_not_found"))
                with str_platform.spinner(tr("searching")):
                    try:
                        res = ubongo.chakata_kamusi_kuu(msamiati, database)
                    except Exception as e:
                        res = None
                        onyesha_hitilafu("kutafuta kwenye kamusi", e)
                if res:
                    onyesha_jibu(res, border_color="#D97706", bg="rgba(255,255,255,0.02)")


elif "sauti" in chaguo_menyu:
    str_platform.markdown(
        f"<h3 style='color: #D97706;'>{html.escape(tr('title_sauti'))}</h3>",
        unsafe_allow_html=True)
    t_imla, t_youtube, t_jifunze = str_platform.tabs([
        tr("tab_imla"), tr("tab_youtube"), tr("tab_learn")])

    with t_imla:
        _lugha_imla_tab = str_platform.selectbox(tr("audio_language"),
                                                 list(MISIMBO_YA_IMLA.keys()),
                                                 key="sauti_imla_lugha")
        _lh_imla_tab = orodha_ya_lahaja(_lugha_imla_tab)
        lahaja_imla_tab = (str_platform.selectbox(tr("dialect_label"), _lh_imla_tab,
                                                  key=f"sauti_imla_lahaja_{_lugha_imla_tab}")
                           if len(_lh_imla_tab) > 1 else None)
        sanifisha_imla_tab = False
        if _lugha_imla_tab == "Kiswahili":
            sanifisha_imla_tab = str_platform.checkbox(
                tr("sanifisha_label"),
                key="sauti_imla_sanifisha")
        boresha_kwa_mbali = str_platform.checkbox(
            tr("boost_audio"),
            value=True, key="sauti_imla_boresha")
        str_platform.markdown(tr("record_live"))
        if hasattr(str_platform, "audio_input"):
            sauti_iliyorekodiwa = str_platform.audio_input(tr("record_start"),
                                                          key="sauti_imla_rekodi_tab")
        else:
            sauti_iliyorekodiwa = None
            str_platform.warning(tr("old_streamlit"))
        str_platform.markdown(tr("upload_audio_md"))
        sauti_iliyopakiwa = str_platform.file_uploader(
            tr("upload_audio_file"), type=["mp3", "wav", "m4a"],
            key="whisper_audio_uploader")
        str_platform.caption(tr("seminar_caption"))

        audio_file = sauti_iliyorekodiwa if sauti_iliyorekodiwa is not None else sauti_iliyopakiwa
        if audio_file is not None:
            aina_sauti = getattr(audio_file, "type", None) or "audio/wav"
            str_platform.audio(audio_file.getvalue(), format=aina_sauti)
            if str_platform.button(tr("whisper_btn"), key="zindua_whisper_v3_btn"):
                res_sauti = None
                injini_za_imla = []
                try:
                    data_sauti = audio_file.getvalue()
                    jina_sauti = getattr(audio_file, "name", "sauti.wav") or "sauti.wav"
                    ni_wav = jina_sauti.lower().endswith(".wav") or "wav" in aina_sauti.lower()
                    if ni_wav:
                        if boresha_kwa_mbali:
                            data_sauti, db_zilizoongezwa = boresha_sauti_wav(data_sauti)
                            if db_zilizoongezwa > 0:
                                str_platform.info(tr("boosted_info", db=f"{db_zilizoongezwa:.0f}"))
                        vipande = gawa_wav_vipande(data_sauti)
                    else:
                        vipande = [data_sauti]
                    matini_zote = []
                    upau = str_platform.progress(0.0, text=tr("progress_start"))
                    for n, kipande in enumerate(vipande, start=1):
                        faili_kipande = _FailiLaSauti(
                            kipande,
                            jina_sauti if len(vipande) == 1 else f"sauti_{n}.wav",
                            aina_sauti if len(vipande) == 1 else "audio/wav")
                        matini_zote.append(ubongo.chakata_sauti_na_imla(
                            faili_kipande, MISIMBO_YA_IMLA.get(_lugha_imla_tab, "sw"),
                            lahaja=lahaja_imla_tab, sanifisha=sanifisha_imla_tab))
                        _inj = getattr(ubongo, "injini_ya_imla", None)
                        if _inj and _inj not in injini_za_imla:
                            injini_za_imla.append(_inj)
                        upau.progress(n / len(vipande),
                                     text=tr("chunk_done", n=n, jumla=len(vipande)))
                    upau.empty()
                    res_sauti = "\n\n".join(m for m in matini_zote if m)
                except Exception as e:
                    res_sauti = None
                    onyesha_hitilafu("kuandika imla", e)
                if res_sauti:
                    str_platform.success(tr("dictation_complete"))
                    if injini_za_imla:
                        str_platform.caption(tr("imla_engine", injini=", ".join(injini_za_imla)))
                    onyesha_jibu(res_sauti)
                    str_platform.download_button(tr("download_notes"), res_sauti,
                                                file_name="imla_notes.txt", key="pakua_imla_notes")

    with t_youtube:
        youtube_imla.onyesha_youtube_imla(
            piga_ai=_piga_ai,
            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
            tafsiri_fn=_tafsiri_ya_video,
        )

    with t_jifunze:
        maandishi_sauti = str_platform.text_area(
            tr("tts_input"),
            value="Karibu kwenye chombo cha Ourworthlinks Business.",
            key="tts_input_box", max_chars=MAX_CHARS)
        lugha_tutorial = str_platform.selectbox(
            tr("tts_language"),
            ["Kiswahili", "Kiingereza", "Kifaransa", "Kiarabu", "Kireno", "Kichina"],
            key="tts_lang_select")
        _lh_tts = orodha_ya_lahaja(lugha_tutorial)
        tc1, tc2, tc3 = str_platform.columns(3)
        with tc1:
            lahaja_tts = (str_platform.selectbox(tr("dialect_short"), _lh_tts,
                                                key=f"tts_lahaja_{lugha_tutorial}")
                          if len(_lh_tts) > 1 else None)
        with tc2:
            sauti_tts = str_platform.selectbox(tr("voice_label"), SAUTI_ZA_GEMINI, key="tts_sauti_select")
        with tc3:
            kasi_tts = str_platform.selectbox(tr("speed_label"), list(KASI_ZA_SAUTI.keys()),
                                              key="tts_kasi_select")
        if str_platform.button(tr("gen_btn"), key="zalisha_tts_btn"):
            with str_platform.spinner(tr("generating_audio")):
                try:
                    audio_bytes = ubongo.zindua_jifunze_lugha_audio(
                        maandishi_sauti, lugha_tutorial, lahaja=lahaja_tts,
                        sauti=sauti_tts, kasi=kasi_tts)
                except Exception as e:
                    audio_bytes = None
                    onyesha_hitilafu("kuzalisha sauti", e)
            if audio_bytes:
                str_platform.audio(audio_bytes, format="audio/wav")
                _injini = getattr(ubongo, "injini_ya_sauti", None)
                if _injini:
                    str_platform.caption(tr("voice_engine", injini=_injini))


str_platform.write("---")
skin_appearance.render_bottom_revenue_banner()
