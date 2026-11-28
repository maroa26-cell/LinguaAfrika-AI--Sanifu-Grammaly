"""
Imla Pro v2: nukuu ya sauti ya Kiswahili.

Hatua: andaa sauti -> nukuu (Groq whisper-large-v3 kwanza) -> kamusi -> usahihishaji wa AI.
Inahitaji: requirements.txt (pydub, groq, openai) na packages.txt (ffmpeg).
Secrets zinazosomwa: GROQ_API_KEY, GROQ_WHISPER_MODEL (si lazima).
"""
import io
import os
import re

import streamlit as str_platform

LUGHA = "sw"
KIPANDE_SEK = 600  # gawa sauti ndefu vipande vya dakika 10

# Elekezo lenye alama za uandishi huisaidia modeli kuweka nukta na herufi kubwa.
ELEKEZO = (
    "Hii ni imla ya Kiswahili sanifu. Habari, asante sana. Nitaangalia maneno "
    "na mfumo, kuhakikisha kwamba wewe unatupa taarifa sahihi. Hilo lilikuwa langu."
)

# Marekebisho ya haraka yasiyotegemea AI. Ongeza makosa mapya yanayojirudia.
MAREKEBISHO = {
    r"\bsante\b": "asante",
    r"\bmaeno\b": "maneno",
    r"\bkuakikisha\b": "kuhakikisha",
    r"\bnitangalia\b": "nitaangalia",
    r"\bniku\s+wapa\b": "nakupa",
    r"\bniku\s+hapa\b": "nipo hapa",
    r"\bmfumu\b": "mfumo",
    r"\bjie\b": "wewe",
    r"\bajila\b": "ajili",
    r"\bkweli\b(?=\s+unandika)": "kweli",
}


def _secret(jina, default=None):
    try:
        return os.environ.get(jina) or str_platform.secrets.get(jina) or default
    except Exception:
        return os.environ.get(jina) or default


def _groq_client():
    try:
        key = _secret("GROQ_API_KEY")
        if not key:
            return None
        from groq import Groq
        return Groq(api_key=key)
    except Exception:
        return None


# ----------------------------- Kuandaa sauti -------------------------------
def andaa_sauti(data, jina):
    try:
        from pydub import AudioSegment, effects
        from pydub.silence import detect_nonsilent

        seg = AudioSegment.from_file(io.BytesIO(data))
        seg = seg.set_channels(1).set_frame_rate(16000)
        seg = effects.normalize(seg)

        vipande = detect_nonsilent(
            seg, min_silence_len=700, silence_thresh=seg.dBFS - 16, seek_step=10
        )
        if vipande:
            kept = AudioSegment.empty()
            for s, e in vipande:
                kept += seg[max(0, s - 200): e + 200]
            if len(kept) > 500:
                seg = kept

        ms = KIPANDE_SEK * 1000
        matokeo = []
        for i in range(0, len(seg), ms):
            buf = io.BytesIO()
            seg[i: i + ms].export(buf, format="wav")
            matokeo.append((f"sehemu_{i // ms + 1}.wav", buf.getvalue()))
        return matokeo
    except Exception:
        return [(jina, data)]


# -------------------------------- Kunukuu ----------------------------------
def nukuu_kipande(client, jina, data):
    """Hurudisha (maandishi, injini)."""
    makosa = []

    gc = _groq_client()
    if gc is not None:
        # Chaguo-msingi ni v3 kamili. Turbo itatumika tu ukiiweka kwenye secrets.
        modeli = _secret("GROQ_WHISPER_MODEL", "whisper-large-v3")
        try:
            r = gc.audio.transcriptions.create(
                model=modeli, file=(jina, data), language=LUGHA,
                prompt=ELEKEZO, temperature=0,
            )
            return r.text.strip(), f"Groq Whisper ({modeli})"
        except Exception as e:
            makosa.append(f"groq: {e}")

    try:
        r = client.audio.transcriptions.create(
            model="gpt-4o-transcribe", file=(jina, data),
            language=LUGHA, prompt=ELEKEZO,
        )
        return r.text.strip(), "OpenAI gpt-4o-transcribe"
    except Exception as e:
        makosa.append(f"gpt-4o-transcribe: {e}")

    try:
        r = client.audio.transcriptions.create(
            model="whisper-1", file=(jina, data),
            language=LUGHA, prompt=ELEKEZO, temperature=0,
        )
        return r.text.strip(), "OpenAI whisper-1"
    except Exception as e:
        makosa.append(f"whisper-1: {e}")

    raise RuntimeError(" | ".join(makosa))


# ------------------------------- Kusahihisha -------------------------------
def sahihisha_kamusi(maandishi):
    for muundo, sahihi in MAREKEBISHO.items():
        maandishi = re.sub(muundo, sahihi, maandishi, flags=re.IGNORECASE)
    return maandishi


MAELEKEZO_MHARIRI = (
    "Wewe ni mhariri wa Kiswahili sanifu. Maandishi yafuatayo yalinukuliwa kutoka "
    "sauti, yana makosa ya tahajia, maneno yaliyokatwakatwa, na hayana alama za "
    "uandishi. Rekebisha tahajia, weka nukta, koma na herufi kubwa mwanzo wa "
    "sentensi. USIONGEZE wala kupunguza maana, wala usibuni maneno. Sehemu ambayo "
    "huielewi kabisa, iache kama ilivyo. Rudisha maandishi yaliyosahihishwa pekee, "
    "bila maelezo."
)


def sahihisha_kwa_ai(client, maandishi):
    """Hurudisha (maandishi, injini_au_None). Groq (bure) kwanza, kisha OpenAI."""
    ujumbe = [
        {"role": "system", "content": MAELEKEZO_MHARIRI},
        {"role": "user", "content": maandishi},
    ]

    def _sawa(jibu):
        return bool(maandishi) and 0.7 <= len(jibu) / len(maandishi) <= 1.5

    gc = _groq_client()
    if gc is not None:
        try:
            modeli = _secret("GROQ_EDITOR_MODEL", "llama-3.3-70b-versatile")
            r = gc.chat.completions.create(model=modeli, temperature=0, messages=ujumbe)
            jibu = r.choices[0].message.content.strip()
            if _sawa(jibu):
                return jibu, f"Groq {modeli}"
        except Exception:
            pass

    try:
        r = client.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=ujumbe)
        jibu = r.choices[0].message.content.strip()
        if _sawa(jibu):
            return jibu, "OpenAI gpt-4o-mini"
    except Exception:
        pass

    return maandishi, None


# ------------------------------- Kazi kuu ----------------------------------
def execute_phonetic_muscle(client, sauti_faili, sahihisha=True, return_engine=False):
    """
    Nukuu sauti ya Kiswahili.
    Chaguo-msingi hurudisha str (inaendana na msimbo wa zamani).
    Ukiweka return_engine=True hurudisha (maandishi, maelezo_ya_injini).
    """
    try:
        data = sauti_faili.getvalue() if hasattr(sauti_faili, "getvalue") else sauti_faili.read()
        jina = getattr(sauti_faili, "name", "sauti.wav")

        sehemu = andaa_sauti(data, jina)
        matokeo = [nukuu_kipande(client, j, d) for j, d in sehemu]
        maandishi = " ".join(m for m, _ in matokeo).strip()
        injini = matokeo[0][1] if matokeo else "haijulikani"

        if not maandishi:
            ujumbe = "🛑 Hakuna maneno yaliyosikika. Rekodi tena karibu na maikrofoni."
            return (ujumbe, injini) if return_engine else ujumbe

        maandishi = sahihisha_kamusi(maandishi)
        if sahihisha:
            maandishi, mhariri = sahihisha_kwa_ai(client, maandishi)
            maandishi = sahihisha_kamusi(maandishi)
            injini += f" + usahihishaji ({mhariri})" if mhariri else " (usahihishaji haukufanya kazi)"

        return (maandishi, injini) if return_engine else maandishi
    except Exception as e:
        ujumbe = f"🛑 Fracture: {str(e)}"
        return (ujumbe, "hitilafu") if return_engine else ujumbe
