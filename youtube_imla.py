"""youtube_imla.py  v1.0
Kipengele cha Lingual Africa Sanifu: mteja anaweka kiungo cha YouTube, mfumo unaandika
maneno yote ya video, UNAYAHARIRI kabla ya kumpa matokeo, kisha anapata kitufe cha kunakili.

Hautozwi salio la maneno 600 (kama Muhtasari na Ukaguzi wa Pili).
Chanzo cha maneno: manukuu (captions) ya YouTube kupitia kifurushi `youtube-transcript-api`.

Matumizi kwenye app.py:
    import youtube_imla
    ...
    with t_youtube:
        youtube_imla.onyesha_youtube_imla(
            piga_ai=_piga_ai,
            piga_ai_kina=_piga_ai_kina if _UTHIBITISHO_WA_PRO else None,
        )
"""
import html
import json
import re

import requests
import streamlit as st
import streamlit.components.v1 as components

LUGHA_ZA_MANUKUU = {
    "Tambua yenyewe": None,
    "Kiswahili": ["sw"],
    "Kiingereza (English)": ["en", "en-US", "en-GB"],
    "Kifaransa": ["fr"],
    "Kiarabu": ["ar"],
    "Kireno (Portugu\u00eas)": ["pt", "pt-BR", "pt-PT"],
}

ORODHA_YA_TAFSIRI = [
    "Kiswahili", "Kiingereza (English)", "Kifaransa", "Kiarabu",
    "Kichina (Mandarin)", "Kireno (Portugu\u00eas)", "Kizulu (isiZulu)", "Setswana (Botswana)",
    "Kinyarwanda", "Kiganda (Luganda)", "Lingala", "Kichewa",
]
_MAJINA_YA_LUGHA = {"sw": "Kiswahili", "en": "Kiingereza (English)", "fr": "Kifaransa",
                    "ar": "Kiarabu", "pt": "Kireno (Portugu\u00eas)", "zh": "Kichina (Mandarin)"}

MANENO_KWA_KIPANDE = 800     # ukubwa wa kipande kimoja cha uhariri (vipande vichache = simu chache za AI)
KIKOMO_CHA_MANENO = 30000     # kinga ya video ndefu mno
_MUHURI = "yt_imla_"


# ----------------------------------------------------------------------------------------
# 1. Kiungo -> video id
# ----------------------------------------------------------------------------------------
_MIFUMO_YA_ID = [
    r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
    r"(?:youtube\.com|youtube-nocookie\.com)/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/|v/)([A-Za-z0-9_-]{11})",
]


def toa_video_id(kiungo):
    k = str(kiungo or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", k):
        return k
    for m in _MIFUMO_YA_ID:
        r = re.search(m, k)
        if r:
            return r.group(1)
    return None


def _kichwa_cha_video(video_id):
    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"},
            timeout=8)
        if r.status_code == 200:
            return r.json().get("title", "")
    except Exception:
        pass
    return ""


# ----------------------------------------------------------------------------------------
# 2. Kuvuta manukuu
# ----------------------------------------------------------------------------------------
class KosaLaYouTube(Exception):
    """Kosa lenye ujumbe tayari wa kumwonyesha mtumiaji."""


def _maandishi_ya_kipande(s):
    if isinstance(s, dict):
        return s.get("text", "")
    return getattr(s, "text", "") or ""


def _orodha_ya_manukuu(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        return YouTubeTranscriptApi().list(video_id)          # toleo jipya (>=1.0)
    except (TypeError, AttributeError):
        return YouTubeTranscriptApi.list_transcripts(video_id)  # toleo la zamani


def vuta_manukuu(video_id, lugha=None):
    """Hurudisha (matini, msimbo_wa_lugha, ni_ya_kutengenezwa_na_mashine)."""
    try:
        import youtube_transcript_api  # noqa: F401
    except ImportError:
        raise KosaLaYouTube(
            "Kifurushi cha youtube-transcript-api hakijawekwa. "
            "Ongeza `youtube-transcript-api>=1.0.0` kwenye requirements.txt.")
    try:
        orodha = _orodha_ya_manukuu(video_id)
        wote = list(orodha)
        if not wote:
            raise KosaLaYouTube("Video hii haina manukuu (captions).")
        chaguo = None
        if lugha:
            for t in wote:  # manukuu ya mtu kwanza, kisha ya mashine
                if not t.is_generated and t.language_code in lugha:
                    chaguo = t; break
            if chaguo is None:
                for t in wote:
                    if t.language_code in lugha:
                        chaguo = t; break
            if chaguo is None:
                raise KosaLaYouTube(
                    "Video haina manukuu ya lugha uliyochagua. Chagua 'Tambua yenyewe'.")
        else:
            chaguo = next((t for t in wote if not t.is_generated), wote[0])
        vipande = chaguo.fetch()
        matini = " ".join(_maandishi_ya_kipande(s).replace("\n", " ") for s in vipande)
        matini = re.sub(r"\[[^\]]{0,25}\]", " ", matini)   # [Muziki], [Applause]
        matini = re.sub(r"\s+", " ", matini).strip()
        if not matini:
            raise KosaLaYouTube("Manukuu yamepatikana lakini hayana maneno.")
        return matini, chaguo.language_code, bool(chaguo.is_generated)
    except KosaLaYouTube:
        raise
    except Exception as e:
        jina = type(e).__name__
        if jina in ("RequestBlocked", "IpBlocked"):
            raise KosaLaYouTube(
                "YouTube imezuia seva hii kuvuta manukuu (inatokea kwenye seva za cloud). "
                "Suluhisho: pakua sauti ya video, kisha tumia kichupo cha 'Imla na Nakala' kuipakia.")
        if jina in ("TranscriptsDisabled", "NoTranscriptFound"):
            raise KosaLaYouTube("Video hii haina manukuu au mmiliki ameyazima.")
        if jina in ("VideoUnavailable", "VideoUnplayable"):
            raise KosaLaYouTube("Video haipatikani (imefutwa, ni ya faragha au imezuiwa).")
        if jina == "AgeRestricted":
            raise KosaLaYouTube("Video ina kikomo cha umri, siwezi kuvuta manukuu yake.")
        print(f"[youtube_imla] {jina}: {e}")
        raise KosaLaYouTube(f"Imeshindikana kuvuta manukuu ({jina}). Jaribu tena au tumia kiungo kingine.")


# ----------------------------------------------------------------------------------------
# 2b. Akiba: Gemini isikilize video moja kwa moja (inafanya kazi hata YouTube ikizuia seva)
# ----------------------------------------------------------------------------------------
def _secret(jina):
    try:
        return str(st.secrets.get(jina) or "").strip()
    except Exception:
        return ""


def _gemini_key_ya_youtube():
    """Ufunguo wa pekee wa YouTube (salio lake lenyewe). Tupu kama haujawekwa."""
    return _secret("GEMINI_API_KEY_YOUTUBE")


def _gemini_key():
    # Ufunguo wa YouTube ukiwekwa, ndio pekee unaotumika (hakuna kurudi kwenye ufunguo mkuu).
    return _gemini_key_ya_youtube() or _secret("GEMINI_API_KEY")


def _gemini_modeli():
    try:
        m = str(st.secrets.get("GEMINI_MODEL_YOUTUBE") or "").strip()
    except Exception:
        m = ""
    return m or "gemini-2.5-flash"


def _debug_imewashwa():
    try:
        return str(st.secrets.get("AI_DEBUG") or "").strip().lower() in ("1", "true", "yes", "ndiyo")
    except Exception:
        return False


def _modeli_ya_flash_ya_hivi_karibuni(client):
    """Inatafuta modeli ya 'gemini-X.Y-flash' ya toleo la juu kabisa inayopatikana kwenye akaunti."""
    bora, toleo_bora = None, -1.0
    for m in client.models.list():
        jina = str(getattr(m, "name", "") or "")
        r = re.fullmatch(r"(?:models/)?(gemini-(\d+(?:\.\d+)?)-flash)", jina)
        if r and float(r.group(2)) > toleo_bora:
            bora, toleo_bora = r.group(1), float(r.group(2))
    return bora


def _ni_kikomo(t):
    return "429" in t or "quota" in t or "resource_exhausted" in t


def _ni_ufikiaji(t):
    return any(x in t for x in ("private", "unlisted", "permission", "invalid_argument", "failed_precondition"))


def _piga_ai_ya_youtube(mfumo, mtumiaji):
    """Uhariri kwa ufunguo wa YouTube pekee. Hurudisha maandishi ya JSON. Ikishindwa, hutupa kosa
    (hariri_kipande kisha hurudisha kipande asili; hakuna matumizi ya ufunguo mkuu)."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=_gemini_key_ya_youtube())
    config = types.GenerateContentConfig(system_instruction=mfumo,
                                         response_mime_type="application/json")
    modeli = _gemini_modeli()
    try:
        jibu = client.models.generate_content(model=modeli, contents=mtumiaji, config=config)
    except Exception as e:
        t = str(e).lower()
        if _ni_kikomo(t) or not any(x in t for x in ("404", "not found", "no longer", "deprecat", "not supported")):
            raise
        mbadala = _modeli_ya_flash_ya_hivi_karibuni(client)
        if not mbadala or mbadala == modeli:
            raise
        jibu = client.models.generate_content(model=mbadala, contents=mtumiaji, config=config)
    return jibu.text


def nakili_kwa_gemini(video_id, lugha_jina="Tambua yenyewe"):
    """Gemini inapokea kiungo cha video ya umma na kuandika maneno yote. Hurudisha (matini, msimbo_wa_lugha)."""
    key = _gemini_key()
    if not key:
        raise KosaLaYouTube("Ufunguo wa Gemini wa YouTube (GEMINI_API_KEY_YOUTUBE) haupo kwenye Secrets, kwa hiyo siwezi kusikiliza video moja kwa moja.")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise KosaLaYouTube("Kifurushi cha google-genai hakijawekwa kwenye requirements.txt.")

    url = f"https://www.youtube.com/watch?v={video_id}"
    kidokezo_cha_lugha = (f"Lugha inayozungumzwa inatarajiwa kuwa {lugha_jina}. "
                          if lugha_jina and lugha_jina != "Tambua yenyewe" else "")
    maelekezo = (
        "Andika neno kwa neno maneno yote yanayosemwa kwenye video hii (transcription kamili). "
        + kidokezo_cha_lugha +
        "USIFUPISHE, USITAFSIRI, na USIONGEZE maelezo yako. Baki kwenye lugha ile ile inayozungumzwa. "
        "Weka vituo na aya. Usiandike muziki, makofi wala maelezo ya picha. Usitaje majina ya wasemaji. "
        "Mstari wa kwanza wa jibu lako uwe huu tu: LUGHA=<msimbo wa ISO 639-1 wa lugha kuu, mfano sw au en>. "
        "Kisha acha mstari mtupu na uandike maandishi yote."
    )
    try:
        client = genai.Client(api_key=key)
        maudhui = types.Content(parts=[
            types.Part(file_data=types.FileData(file_uri=url)),
            types.Part(text=maelekezo),
        ])
        try:  # azimio la chini: tunahitaji sauti tu, inapunguza gharama
            config = types.GenerateContentConfig(
                media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW)
        except Exception:
            config = None
        modeli = _gemini_modeli()
        jibu, kosa_la_mwisho = None, None
        for jaribio in range(3):
            try:
                kw = {"config": config} if config is not None else {}
                jibu = client.models.generate_content(model=modeli, contents=maudhui, **kw)
                break
            except Exception as e:
                kosa_la_mwisho = e
                t = str(e).lower()
                print(f"[youtube_imla] jaribio {jaribio + 1} (modeli={modeli}, config={config is not None}) "
                      f"limeshindwa: {type(e).__name__}: {e}")
                if _ni_kikomo(t):
                    raise
                if config is not None:      # jaribu tena bila mpangilio wa azimio
                    config = None
                    continue
                if any(x in t for x in ("404", "not found", "no longer", "deprecat", "not supported")):
                    mbadala = _modeli_ya_flash_ya_hivi_karibuni(client)
                    if mbadala and mbadala != modeli:
                        print(f"[youtube_imla] naajaribu modeli mbadala: {mbadala}")
                        modeli = mbadala
                        continue
                raise
        if jibu is None:
            raise kosa_la_mwisho
        maandishi = (jibu.text or "").strip()
    except KosaLaYouTube:
        raise
    except Exception as e:
        t = str(e).lower()
        print(f"[youtube_imla] Gemini imeshindwa: {type(e).__name__}: {e}")
        ziada = f" [{type(e).__name__}: {str(e)[:300]}]" if _debug_imewashwa() else ""
        if _ni_kikomo(t):
            raise KosaLaYouTube("Kikomo cha matumizi ya Gemini kimefikiwa kwa sasa. Jaribu tena baadaye." + ziada)
        if _ni_ufikiaji(t):
            raise KosaLaYouTube("Gemini haikuweza kufikia video hii. Video lazima iwe ya umma "
                                "(si ya faragha wala unlisted) na isiwe na kikomo cha umri." + ziada)
        raise KosaLaYouTube("Imeshindikana kusikiliza video kupitia Gemini "
                            f"(aina ya kosa: {type(e).__name__}). Jaribu tena au tumia video nyingine." + ziada)

    if not maandishi:
        raise KosaLaYouTube("Gemini haikurudisha maandishi kwa video hii (huenda haina hotuba au maudhui yamezuiwa).")
    msimbo = "und"
    mstari1 = re.match(r"^\s*LUGHA\s*=\s*([A-Za-z]{2,3})\b[^\n]*\n?", maandishi)
    if mstari1:
        msimbo = mstari1.group(1).lower()
        maandishi = maandishi[mstari1.end():].strip()
    maandishi = re.sub(r"\n{3,}", "\n\n", maandishi)
    if len(maandishi.split()) < 3:
        raise KosaLaYouTube("Gemini haikupata hotuba ya kutosha kwenye video hii.")
    return maandishi, msimbo

# ----------------------------------------------------------------------------------------
# 3. Uhariri wa AI (kwa vipande, bila kufupisha)
# ----------------------------------------------------------------------------------------
def gawa_vipande(matini, ukubwa=MANENO_KWA_KIPANDE):
    maneno = matini.split()
    return [" ".join(maneno[i:i + ukubwa]) for i in range(0, len(maneno), ukubwa)]


def _mfumo_wa_uhariri(msimbo_lugha, sanifu):
    kiswahili = (msimbo_lugha or "").lower().startswith("sw")
    msingi = (
        "Wewe ni mhariri wa maandishi yaliyotolewa kwenye manukuu ya video. "
        "Maandishi hayana vituo wala herufi kubwa. KAZI YAKO: weka vituo (. , ? !), herufi kubwa, "
        "na aya; rekebisha makosa dhahiri ya tahajia na maneno yaliyosikika vibaya; ondoa marudio ya "
        "kigugumizi (kama 'ee ee', 'yaani yaani'). "
        "USIFUPISHE, USIONGEZE mawazo mapya, USIBADILISHE maana, na USITAFSIRI: baki kwenye lugha ile ile. "
        "Maneno yote muhimu ya mzungumzaji lazima yabaki. "
    )
    if kiswahili and sanifu:
        msingi += ("Kwa kuwa ni Kiswahili, tumia Kiswahili Sanifu: sahihisha ngeli, viambishi na tahajia; "
                   "badilisha maneno ya Sheng/lahaja kuwa ya kawaida pale maana ni ileile. ")
    msingi += ('Jibu kwa JSON tu, bila maelezo mengine: {"maandishi": "<maandishi yaliyohaririwa>"}')
    return msingi


def _toa_maandishi(jibu):
    if isinstance(jibu, dict):
        return str(jibu.get("maandishi") or "").strip()
    if isinstance(jibu, str):
        s = jibu.strip()
        try:
            d = json.loads(re.sub(r"^```(?:json)?|```$", "", s, flags=re.M).strip())
            if isinstance(d, dict):
                return str(d.get("maandishi") or "").strip()
        except Exception:
            return s
    return ""


def hariri_kipande(kipande, msimbo_lugha, sanifu, piga_ai):
    """Hurudisha (maandishi, yamehaririwa_kweli). Kipande kikiharibika au kufupishwa mno, kinarudi asili."""
    try:
        jibu = piga_ai(_mfumo_wa_uhariri(msimbo_lugha, sanifu),
                       f"Hariri maandishi haya:\n\n{kipande}")
        mpya = _toa_maandishi(jibu)
    except Exception as e:
        print(f"[youtube_imla] uhariri umeshindwa: {type(e).__name__}: {e}")
        return kipande, False
    if not mpya or len(mpya.split()) < 0.7 * len(kipande.split()):
        return kipande, False   # kinga dhidi ya AI kufupisha maudhui
    return mpya, True


# ----------------------------------------------------------------------------------------
# 4. Kitufe cha kunakili
# ----------------------------------------------------------------------------------------
def kitufe_cha_kunakili(matini, ufunguo):
    data = json.dumps(matini).replace("</", "<\\/")
    components.html(f"""
    <button id="b{ufunguo}" style="background:#D97706;color:#fff;border:0;border-radius:8px;
      padding:10px 18px;font-weight:700;cursor:pointer;font-size:15px;">\U0001F4CB Nakili maandishi yote</button>
    <script>
    const t={data};
    const b=document.getElementById("b{ufunguo}");
    b.onclick=async()=>{{
      try{{await navigator.clipboard.writeText(t);}}
      catch(e){{const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);
               a.select();document.execCommand("copy");document.body.removeChild(a);}}
      b.textContent="\u2705 Yamenakiliwa!";setTimeout(()=>b.textContent="\U0001F4CB Nakili maandishi yote",2500);
    }};
    </script>""", height=55)


# ----------------------------------------------------------------------------------------
# 5. Kiolesura
# ----------------------------------------------------------------------------------------
def onyesha_youtube_imla(piga_ai, piga_ai_kina=None, tafsiri_fn=None, ufunguo="yt"):
    k = lambda n: f"{_MUHURI}{ufunguo}_{n}"
    # Ufunguo wa YouTube ukiwekwa, uhariri nao unatumia salio lake (si la ufunguo mkuu)
    ai_hariri = _piga_ai_ya_youtube if _gemini_key_ya_youtube() else piga_ai
    st.caption("Weka kiungo cha video ya YouTube. Mfumo utaandika maneno yote ya video, "
               "utayahariri, kisha utakupa nafasi ya kunakili. Hautozwi salio la maneno.")

    kiungo = st.text_input("\U0001F517 Kiungo cha YouTube:", key=k("kiungo"),
                           placeholder="https://www.youtube.com/watch?v=...")
    c1, c2 = st.columns(2)
    with c1:
        lugha_jina = st.selectbox("Lugha ya manukuu:", list(LUGHA_ZA_MANUKUU.keys()), key=k("lugha"))
    with c2:
        hariri_wazi = st.checkbox("Hariri maandishi kabla ya kunipa (inapendekezwa)",
                                  value=True, key=k("hariri"))
    sanifu = st.checkbox("Kama ni Kiswahili: andika kwa Kiswahili Sanifu", value=True, key=k("sanifu"))

    if st.button("\u25B6\uFE0F Andika maneno yote ya video", type="primary", key=k("kitufe")):
        vid = toa_video_id(kiungo)
        st.session_state.pop(k("matokeo"), None)
        if not vid:
            if "list=" in str(kiungo) and "youtu" in str(kiungo):
                st.warning("Hiki ni kiungo cha orodha (playlist), si cha video moja. "
                           "Fungua video unayotaka kwenye YouTube, kisha nakili kiungo chake "
                           "(kinachoonekana kama youtube.com/watch?v=... au youtu.be/...).")
            else:
                st.warning("Kiungo hakionekani kuwa cha video ya YouTube. Angalia kisha ujaribu tena.")
        else:
            upau = st.progress(0.0, text="Inavuta maneno ya video...")
            asili, chanzo = None, "manukuu"
            try:
                asili, msimbo, ya_mashine = vuta_manukuu(vid, LUGHA_ZA_MANUKUU[lugha_jina])
            except KosaLaYouTube as e1:
                print(f"[youtube_imla] manukuu hayakupatikana: {e1}")
                upau.progress(0.1, text="Manukuu hayapatikani. Inasikiliza sauti ya video kupitia Gemini "
                                        "(inaweza kuchukua dakika chache kwa video ndefu)...")
                try:
                    asili, msimbo = nakili_kwa_gemini(vid, lugha_jina)
                    ya_mashine, chanzo = False, "gemini"
                except KosaLaYouTube as e2:
                    upau.empty()
                    st.error(str(e2))
                    asili = None
            if asili:
                maneno = len(asili.split())
                if maneno > KIKOMO_CHA_MANENO:
                    asili = " ".join(asili.split()[:KIKOMO_CHA_MANENO])
                    st.info(f"Video ni ndefu sana; nimeandika maneno {KIKOMO_CHA_MANENO} ya kwanza.")
                vipande = gawa_vipande(asili)
                matokeo, yaliyohaririwa = [], 0
                for n, kp in enumerate(vipande, start=1):
                    if hariri_wazi:
                        upau.progress((n - 1) / len(vipande),
                                      text=f"Inahariri kipande {n} kati ya {len(vipande)}...")
                        mpya, sawa = hariri_kipande(kp, msimbo, sanifu, ai_hariri)
                        yaliyohaririwa += int(sawa)
                    else:
                        mpya = kp
                    matokeo.append(mpya)
                upau.progress(1.0, text="Imekamilika")
                upau.empty()
                st.session_state[k("matokeo")] = {
                    "vid": vid, "kichwa": _kichwa_cha_video(vid), "lugha": msimbo,
                    "mashine": ya_mashine, "chanzo": chanzo, "asili": asili,
                    "mhariri": "\n\n".join(matokeo),
                    "vipande": len(vipande), "vimehaririwa": yaliyohaririwa,
                    "ilihaririwa": hariri_wazi,
                }
                st.session_state[k("eneo")] = st.session_state[k("matokeo")]["mhariri"]

    m = st.session_state.get(k("matokeo"))
    if not m:
        return

    st.markdown("---")
    if m["kichwa"]:
        st.markdown(f"**\U0001F3AC {html.escape(m['kichwa'])}**")
    if m.get("chanzo") == "gemini":
        maelezo_ya_chanzo = ("imeandikwa kwa kusikiliza sauti ya video (Gemini); "
                             "inaweza kuwa na makosa madogo")
        lugha_txt = f"Lugha: {m['lugha']}" if m["lugha"] != "und" else "Lugha: imetambuliwa kiotomatiki"
    else:
        maelezo_ya_chanzo = ("manukuu yametengenezwa na mashine ya YouTube (yanaweza kuwa na makosa)"
                             if m["mashine"] else "manukuu yameandikwa na mmiliki wa video")
        lugha_txt = f"Lugha ya manukuu: {m['lugha']}"
    st.caption(f"{lugha_txt} \u2022 {maelezo_ya_chanzo} \u2022 maneno {len(m['asili'].split())}")
    if m["ilihaririwa"]:
        if m["vimehaririwa"] == m["vipande"]:
            st.success("\u2728 Maandishi yamehaririwa. Pitia hapa chini kisha unakili.")
        elif m["vimehaririwa"] == 0:
            st.warning("Uhariri wa AI haukufanikiwa; unaona maandishi ya asili. "
                       "Unaweza kuyahariri mwenyewe hapa chini.")
        else:
            st.warning(f"Vipande {m['vimehaririwa']} kati ya {m['vipande']} ndivyo vimehaririwa; "
                       "vingine vimebaki vya asili.")

    if st.button("\u270F\uFE0F Hariri tena kwa AI", key=k("hariri_tena"),
                 help="Inahariri tena maandishi yaliyo kwenye kisanduku hapa chini."):
        _sasa = st.session_state.get(k("eneo"), m["mhariri"])
        with st.spinner("Inahariri..."):
            _vp = [hariri_kipande(v, m["lugha"], sanifu, ai_hariri)[0] for v in gawa_vipande(_sasa)]
        st.session_state[k("eneo")] = "\n\n".join(_vp)

    toleo = st.text_area("Maandishi (unaweza kuyarekebisha moja kwa moja):",
                         key=k("eneo"), height=380)
    kb1, kb2 = st.columns([1, 1])
    with kb1:
        kitufe_cha_kunakili(toleo, ufunguo)
    with kb2:
        st.download_button("\u2B07\uFE0F Pakua (.txt)", toleo,
                           file_name=f"youtube_{m['vid']}.txt", key=k("pakua"))
    with st.expander("Angalia maandishi ya asili (kabla ya uhariri)"):
        st.text_area("Asili:", m["asili"], height=200, key=k("asili_eneo"), disabled=True)


    # --- Tafsiri ---
    st.markdown("---")
    st.markdown("**\U0001F500 Tafsiri maandishi haya**")
    if tafsiri_fn is None:
        st.caption("Tafsiri haijaunganishwa (pitisha tafsiri_fn kwenye app.py).")
        return
    jina_la_chanzo = next((j for kd, j in _MAJINA_YA_LUGHA.items()
                           if str(m["lugha"]).lower().startswith(kd)), "Kiswahili")
    lengo_msingi = "Kiingereza (English)" if jina_la_chanzo == "Kiswahili" else "Kiswahili"
    t1, t2 = st.columns(2)
    with t1:
        st.text_input("Kutoka lugha:", jina_la_chanzo, disabled=True, key=k("t_chanzo"))
    with t2:
        lengo = st.selectbox("Kwenda lugha:", ORODHA_YA_TAFSIRI,
                             index=ORODHA_YA_TAFSIRI.index(lengo_msingi), key=k("t_lengo"))
    st.caption("Tafsiri inakata salio la maneno 600 (kama Mtafsiri wa kawaida).")
    if st.button("\U0001F500 Tafsiri sasa", key=k("t_kitufe")):
        with st.spinner("Inatafsiri..."):
            try:
                st.session_state[k("tafsiri")] = tafsiri_fn(toleo, jina_la_chanzo, lengo)
                st.session_state[k("tafsiri_lengo")] = lengo
            except Exception as e:
                st.session_state.pop(k("tafsiri"), None)
                st.error(str(e))
    if st.session_state.get(k("tafsiri")):
        st.text_area(f"Tafsiri ({st.session_state.get(k('tafsiri_lengo'), '')}):",
                     st.session_state[k("tafsiri")], height=300, key=k("t_eneo"))
        tb1, tb2 = st.columns(2)
        with tb1:
            kitufe_cha_kunakili(st.session_state[k("tafsiri")], "t" + ufunguo)
        with tb2:
            st.download_button("\u2B07\uFE0F Pakua tafsiri (.txt)", st.session_state[k("tafsiri")],
                               file_name=f"youtube_{m['vid']}_tafsiri.txt", key=k("t_pakua"))
