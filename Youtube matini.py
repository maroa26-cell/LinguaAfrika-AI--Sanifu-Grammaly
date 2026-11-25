
"""
youtube_matini.py - Kuchukua matini (manukuu/subtitles) ya video ya YouTube kwa kiungo au msimbo wa video.

Hutumia maktaba ya `youtube-transcript-api` (ongeza kwenye requirements.txt):
    youtube-transcript-api>=1.0.0

Tahadhari muhimu: YouTube huzuia anwani za IP za seva za kampuni za cloud (kama Streamlit Cloud),
kwa hiyo kuchukua matini kunaweza kushindwa na kosa la RequestBlocked/IpBlocked. Suluhisho:
  1. Mtumiaji abandike matini mwenyewe (YouTube > "Show transcript" > nakili), au
  2. Weka proxy kwenye Streamlit Secrets: YOUTUBE_PROXY_URL = "http://mtumiaji:nenosiri@mwenyeji:bandari"

Moduli hii haitegemei Streamlit, kwa hiyo inajaribika peke yake.
"""

import html
import re
from urllib.parse import parse_qs, urlparse

LUGHA_ZINAZOPENDELEWA = ("sw", "en")

JINA_LA_LUGHA = {
    "sw": "Kiswahili", "en": "Kiingereza (English)", "fr": "Kifaransa", "ar": "Kiarabu",
    "zh": "Kichina (Mandarin)", "pt": "Kireno (Portugu\u00eas)", "zu": "Kizulu (isiZulu)",
    "tn": "Setswana (Botswana)", "rw": "Kinyarwanda", "lg": "Kiganda (Luganda)",
    "ln": "Lingala", "ny": "Kichewa",
}

_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
_ALAMA_ZA_SAUTI = re.compile(r"\[[^\]]{1,30}\]")   # [Music], [Applause], [Muziki]...


def toa_video_id(kiungo):
    """Toa msimbo wa video (herufi 11) kutoka kiungo cha YouTube au msimbo wenyewe. None kama si sahihi."""
    k = (kiungo or "").strip()
    if not k:
        return None
    if _ID.match(k):
        return k
    if "://" not in k and "." in k:
        k = "https://" + k   # mf. "youtu.be/abc..." bila https
    try:
        u = urlparse(k)
    except ValueError:
        return None
    mwenyeji = (u.hostname or "").lower()
    for kiambishi in ("www.", "m."):
        if mwenyeji.startswith(kiambishi):
            mwenyeji = mwenyeji[len(kiambishi):]
    vid = None
    if mwenyeji == "youtu.be":
        sehemu = [s for s in u.path.split("/") if s]
        vid = sehemu[0] if sehemu else None
    elif mwenyeji in ("youtube.com", "music.youtube.com", "youtube-nocookie.com"):
        if u.path == "/watch":
            vid = (parse_qs(u.query).get("v") or [None])[0]
        else:
            m = re.match(r"^/(?:shorts|embed|live|v)/([^/?#]+)", u.path)
            vid = m.group(1) if m else None
    return vid if vid and _ID.match(vid) else None


def safisha_matini(vipande):
    """Unganisha vipande vya manukuu kuwa matini moja safi."""
    t = " ".join(str(v) for v in vipande)
    t = html.unescape(t)
    t = _ALAMA_ZA_SAUTI.sub(" ", t)
    t = t.replace(">>", " ")
    return re.sub(r"\s+", " ", t).strip()


def jina_la_lugha(msimbo):
    return JINA_LA_LUGHA.get((msimbo or "").split("-")[0].lower(), msimbo or "")


def _kosa(ujumbe, aina):
    return {"ok": False, "video_id": None, "matini": "", "lugha_msimbo": None, "lugha_jina": None,
            "ni_ya_kiotomatiki": None, "lugha_zilizopo": [], "maneno": 0,
            "kosa": ujumbe, "aina_ya_kosa": aina}


_UJUMBE_WA_MAKOSA = {
    "TranscriptsDisabled": ("Video hii imezima manukuu (subtitles), kwa hiyo hakuna matini ya kuchukua.", "hakuna_manukuu"),
    "NoTranscriptFound": ("Hakuna manukuu yanayopatikana kwa video hii.", "hakuna_manukuu"),
    "VideoUnavailable": ("Video haipatikani (huenda imefutwa au ni ya faragha).", "video"),
    "VideoUnplayable": ("Video haiwezi kuchezwa (huenda ina kikomo cha umri au nchi).", "video"),
    "AgeRestricted": ("Video ina kikomo cha umri, kwa hiyo matini hayawezi kuchukuliwa.", "video"),
    "InvalidVideoId": ("Msimbo wa video si sahihi. Weka kiungo kamili cha video.", "kiungo"),
    "RequestBlocked": ("YouTube imezuia seva ya programu hii kuchukua matini (kawaida kwa seva za cloud). "
                       "Bandika matini mwenyewe: kwenye YouTube bonyeza «Show transcript», nakili maandishi, "
                       "kisha yabandike kwenye kisanduku hapa chini.", "imezuiwa"),
    "IpBlocked": ("YouTube imezuia seva ya programu hii kuchukua matini (kawaida kwa seva za cloud). "
                  "Bandika matini mwenyewe: kwenye YouTube bonyeza «Show transcript», nakili maandishi, "
                  "kisha yabandike kwenye kisanduku hapa chini.", "imezuiwa"),
}


def _proxy(proxy_url):
    from youtube_transcript_api.proxies import GenericProxyConfig
    return GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)


def _orodha_ya_manukuu(YT, video_id, proxy_url):
    if hasattr(YT, "list_transcripts"):       # toleo la zamani (0.x): njia tuli
        return YT.list_transcripts(video_id)
    api = YT(proxy_config=_proxy(proxy_url)) if proxy_url else YT()
    return api.list(video_id)                 # toleo jipya (1.x)


def _chagua(orodha, lugha):
    """Pendelea manukuu yaliyoandikwa na binadamu, kisha ya kiotomatiki, kisha yoyote yaliyopo."""
    for kitafuta in ("find_manually_created_transcript", "find_generated_transcript"):
        try:
            return getattr(orodha, kitafuta)(list(lugha))
        except Exception:
            continue
    vyote = list(orodha)
    if vyote:
        return vyote[0]
    raise LookupError("NoTranscriptFound")


def _maandishi_ya_kipande(s):
    return s.get("text", "") if isinstance(s, dict) else getattr(s, "text", "")


def pata_matini(kiungo, lugha=LUGHA_ZINAZOPENDELEWA, proxy_url=None):
    """
    Hurudisha dict: {ok, video_id, matini, lugha_msimbo, lugha_jina, ni_ya_kiotomatiki,
                     lugha_zilizopo, maneno, kosa, aina_ya_kosa}
    aina_ya_kosa: kiungo | maktaba | hakuna_manukuu | video | imezuiwa | mengineyo
    """
    vid = toa_video_id(kiungo)
    if not vid:
        return _kosa("Kiungo au msimbo wa video si sahihi. Mfano: https://www.youtube.com/watch?v=XXXXXXXXXXX",
                     "kiungo")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception:
        return _kosa("Maktaba ya youtube-transcript-api haijasakinishwa. "
                     "Ongeza «youtube-transcript-api» kwenye requirements.txt, au bandika matini mwenyewe.",
                     "maktaba")
    try:
        orodha = _orodha_ya_manukuu(YouTubeTranscriptApi, vid, proxy_url)
        zilizopo = [f"{getattr(t, 'language_code', '?')} ({getattr(t, 'language', '')})" for t in orodha]
        manukuu = _chagua(orodha, lugha)
        vipande = [_maandishi_ya_kipande(s) for s in manukuu.fetch()]
        matini = safisha_matini(vipande)
        if not matini:
            return _kosa("Manukuu yamepatikana lakini hayana maandishi.", "hakuna_manukuu")
        msimbo = getattr(manukuu, "language_code", "") or ""
        return {"ok": True, "video_id": vid, "matini": matini,
                "lugha_msimbo": msimbo, "lugha_jina": jina_la_lugha(msimbo),
                "ni_ya_kiotomatiki": bool(getattr(manukuu, "is_generated", False)),
                "lugha_zilizopo": zilizopo, "maneno": len(matini.split()),
                "kosa": None, "aina_ya_kosa": None}
    except Exception as e:
        jina = type(e).__name__
        if jina in _UJUMBE_WA_MAKOSA:
            ujumbe, aina = _UJUMBE_WA_MAKOSA[jina]
        elif isinstance(e, LookupError):
            ujumbe, aina = _UJUMBE_WA_MAKOSA["NoTranscriptFound"]
        else:
            print(f"[youtube_matini] {jina}: {str(e)[:160]}")
            ujumbe, aina = (f"Imeshindikana kuchukua matini ({jina}). Jaribu tena au bandika matini mwenyewe.",
                            "mengineyo")
        return _kosa(ujumbe, aina)
