# ukaguzi_wa_pili.py
import json
import re

MAELEKEZO = """Wewe ni mkaguzi wa pili wa Kiswahili sanifu. Umepewa MAANDISHI YA CHANZO
na MATOKEO (tafsiri au toleo lililohaririwa). Kagua MATOKEO tu:
1. MUUNDO: mpangilio wa sentensi, aya, vichwa na orodha uwe kama chanzo; kusiwe na pengo au sehemu iliyorukwa.
2. SARUFI: upatanisho wa ngeli, viambishi, nyakati, tahajia, alama za uandishi.
   Kanuni: "akina mama wengi", "akina baba wengi", "watoto wengi" (si "akina watoto"),
   "wakati mwingi", "muda mwingi".
3. UAMINIFU: maana ya chanzo isipotee, isiongezwe wala kupunguzwa.
4. Hakuna maneno ya Kiingereza yaliyochanganywa (code-switching) isipokuwa majina maalum.
Usibadilishe maneno yasiyo na kosa wala mtindo wa mwandishi.
Jibu JSON tu, bila maelezo mengine:
{"sawa": true|false,
 "matatizo": [{"aina": "muundo|sarufi|maana", "lilipo": "...", "pendekezo": "...", "sababu": "..."}],
 "toleo_sahihi": "matokeo yote yaliyosahihishwa"}
Kama hakuna tatizo: {"sawa": true, "matatizo": [], "toleo_sahihi": "<matokeo yaleyale>"}"""


def _safisha_json(maandishi: str) -> dict:
    maandishi = re.sub(r"```json|```", "", maandishi).strip()
    return json.loads(maandishi)


def kagua_mara_ya_pili(chanzo: str, matokeo: str, aina: str, piga_ai) -> dict:
    """
    piga_ai(mfumo: str, ujumbe: str) -> str
    Tumia kitendakazi kilekile cha cerebral_cortex.py (Gemini -> Groq -> OpenAI),
    ili mnyororo wa funguo uendelee kufanya kazi.
    """
    ujumbe = f"AINA: {aina}\n\nCHANZO:\n{chanzo}\n\nMATOKEO:\n{matokeo}"
    try:
        jibu = piga_ai(MAELEKEZO, ujumbe)
        data = _safisha_json(jibu)
        data.setdefault("matatizo", [])
        data.setdefault("toleo_sahihi", matokeo)
        return data
    except Exception as e:
        return {"sawa": None, "matatizo": [], "toleo_sahihi": matokeo, "kosa": str(e)}
