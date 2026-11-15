"""Majaribio ya mpangilio wa bure (Groq anatafsiri, Gemini anahariri) na Gemini pekee. Endesha: pytest"""
import pytest

import mhariri_pro as mp
import sanifu_editor as se
from kanuni_ya_sarufi import KanuniZaSarufiKiswahili

K = KanuniZaSarufiKiswahili()
EN = "When leaders share clear goals, productivity increases by 20 percent."
RASIMU = "Viongozi wanaposhiriki malengo wazi, uzalishaji huongezeka kwa asilimia 20."
SAHIHI = "Viongozi wanaposhirikisha malengo wazi, tija huongezeka kwa asilimia 20."


class Simu:
    """Mtoa huduma bandia anayerekodi nani aliitwa kwa kazi gani."""

    def __init__(self, monkeypatch, gemini=None, groq=None):
        self.kumbukumbu, self.ujumbe = [], []
        self.gemini, self.groq = gemini, groq
        monkeypatch.setattr(se, "piga_ai", self)

    def __call__(self, mfumo, t, temperature=0.1, mtoa=None):
        kazi = ("mtafsiri" if "fast, faithful translator" in mfumo
                else "ukaguzi" if "UKAGUZI WA PILI" in mfumo else "mhariri")
        self.kumbukumbu.append((mtoa, kazi))
        self.ujumbe.append((mtoa, kazi, mfumo, t))
        tabia = {"gemini": self.gemini, "groq": self.groq}.get(mtoa)
        if tabia is None:
            raise RuntimeError("429 quota exceeded")
        return tabia(kazi, t) if callable(tabia) else tabia


def mtafsiri_na_mhariri(kazi, t):
    return {"rasimu": RASIMU} if kazi == "mtafsiri" else {"maandishi_sahihi": SAHIHI, "marekebisho": []}


# ---------- Mpangilio wa bure ----------
def test_majukumu_yamegawanywa_groq_anatafsiri_gemini_anahariri(monkeypatch):
    s = Simu(monkeypatch, gemini=mtafsiri_na_mhariri, groq=mtafsiri_na_mhariri)
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="bure",
                            majaribio_ya_juu=1)
    assert s.kumbukumbu == [("groq", "mtafsiri"), ("gemini", "mhariri")]
    assert r["mtoa_wa_rasimu"] == "groq" and r["mtoa_huduma"] == "gemini" and r["rasimu"] == RASIMU
    mfumo, ujumbe = s.ujumbe[1][2], s.ujumbe[1][3]
    assert "SOURCE (English)" in ujumbe and "DRAFT (Swahili)" in ujumbe and RASIMU in ujumbe and EN in ujumbe
    assert "ENGLISH-TO-SWAHILI TRANSLATION RULES" in mfumo and "INPUT FORMAT" in mfumo   # kanuni kali kwa mhariri mkuu
    assert "ENGLISH-TO-SWAHILI" not in s.ujumbe[0][2]                                   # mtafsiri ana maelekezo mafupi
    assert "tija huongezeka" in r["maandishi_sahihi"] and r["hali"] == "bure"


def test_groq_akishindwa_gemini_anatafsiri_na_kuhariri_mwenyewe(monkeypatch):
    s = Simu(monkeypatch, gemini=lambda k, t: {"maandishi_sahihi": SAHIHI, "marekebisho": []})   # groq inatupa 429
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="bure",
                            majaribio_ya_juu=1)
    assert s.kumbukumbu == [("groq", "mtafsiri"), ("gemini", "mhariri")]
    assert r["rasimu"] is None and "DRAFT" not in s.ujumbe[1][3] and s.ujumbe[1][3] == EN
    assert any("Groq) ameshindwa" in t for t in r["tahadhari"])


def test_gemini_akishindwa_groq_anahariri_na_onyo(monkeypatch):
    s = Simu(monkeypatch, groq=mtafsiri_na_mhariri)            # gemini inatupa 429
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="bure",
                            majaribio_ya_juu=1)
    assert s.kumbukumbu == [("groq", "mtafsiri"), ("gemini", "mhariri"), ("groq", "mhariri")]
    assert r["mtoa_huduma"] == "groq" and any("Gemini hakupatikana" in t for t in r["tahadhari"])


def test_wote_wa_hatua_ya_pili_wakishindwa_rasimu_inarekebishwa_kwa_kanuni(monkeypatch):
    class TafsiriTu(Simu):
        def __call__(self, mfumo, t, temperature=0.1, mtoa=None):
            if "fast, faithful translator" in mfumo:
                self.kumbukumbu.append((mtoa, "mtafsiri"))
                return {"rasimu": RASIMU}
            self.kumbukumbu.append((mtoa, "mhariri"))
            raise RuntimeError("503 unavailable")

    s = TafsiriTu(monkeypatch)
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="bure",
                            majaribio_ya_juu=1)
    assert r["mtoa_huduma"] == "rasimu" and any("rasimu ya mtafsiri" in t for t in r["tahadhari"])
    assert "tija huongezeka" in r["maandishi_sahihi"] and "wanaposhirikisha" in r["maandishi_sahihi"]   # kanuni zimeitumia


@pytest.mark.parametrize("hali", ["bure", "gemini_pekee"])
def test_openai_haitumiki_kamwe_katika_hali_za_bure(monkeypatch, hali):
    s = Simu(monkeypatch)          # kila mtoa huduma anashindwa
    with pytest.raises(RuntimeError):
        se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali=hali)
    assert "openai" not in {m for m, _ in s.kumbukumbu}


def test_mkaguzi_wa_ai_katika_hali_ya_bure_hamtumii_openai(monkeypatch):
    seen = []

    def bandia(mfumo, t, temperature=0.1, mtoa=None):
        seen.append((mtoa, "strict proofreader" in mfumo))
        if "strict proofreader" in mfumo:
            return {"makosa": []}
        return {"rasimu": RASIMU} if "fast, faithful translator" in mfumo else \
            {"maandishi_sahihi": SAHIHI, "marekebisho": []}

    monkeypatch.setattr(se, "piga_ai", bandia)
    se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="bure",
                        mkaguzi_wa_ai=True, majaribio_ya_juu=1)
    assert "openai" not in {m for m, _ in seen}
    assert [m for m, mkaguzi in seen if mkaguzi] == ["groq"]       # mkaguzi ni mtoa huduma tofauti na mhariri (Gemini)


def test_chanzo_cha_kiswahili_kinasafishwa_kwa_kanuni_bila_kuita_ai(monkeypatch):
    s = Simu(monkeypatch, gemini=lambda k, t: {"maandishi_sahihi": "The class is noisy.", "marekebisho": []},
             groq=lambda k, t: {"rasimu": "The class is noisy."})
    r = se.hariri_kwa_ubora("Darasani yenye wanafunzi wengi kuna kelele kubwa kubwa.", kamusi=set(),
                            lugha_chanzo="Kiswahili", lugha_lengwa="Kiingereza", hali="bure", majaribio_ya_juu=1)
    assert len(s.kumbukumbu) == 2                                    # Groq + Gemini tu; hakuna simu ya usafishaji
    assert r["chanzo_kilichohaririwa"] == "Darasa lenye wanafunzi wengi kuna kelele kubwa."
    assert s.ujumbe[0][3] == "Darasa lenye wanafunzi wengi kuna kelele kubwa."


def test_maandishi_marefu_yanaonywa(monkeypatch):
    Simu(monkeypatch, gemini=mtafsiri_na_mhariri, groq=mtafsiri_na_mhariri)
    r = se.hariri_kwa_ubora(EN + " " + "x" * 13000, kamusi=set(), lugha_chanzo="Kiingereza",
                            lugha_lengwa="Kiswahili", hali="bure", majaribio_ya_juu=1)
    assert any("marefu" in t for t in r["tahadhari"])


def test_hali_isiyojulikana():
    with pytest.raises(ValueError):
        se.hariri_kwa_ubora("x", hali="openai_pekee")


# ---------- Gemini pekee: ukaguzi wa pili wa lazima ----------
def test_gemini_pekee_hufanya_ukaguzi_wa_pili_hata_alama_ikiwa_nzuri(monkeypatch):
    def gemini(kazi, t):
        if kazi == "ukaguzi":
            return {"maandishi_sahihi": "Viongozi wanaposhirikisha malengo wazi, tija huongezeka kwa asilimia 20.", "marekebisho": []}
        return {"maandishi_sahihi": "Viongozi wanaposhirikisha malengo wazi, tija huongezeka kwa asilimia 20", "marekebisho": []}

    s = Simu(monkeypatch, gemini=gemini)
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili",
                            hali="gemini_pekee", majaribio_ya_juu=1)       # 1 inapandishwa kuwa 2
    assert [k for _, k in s.kumbukumbu] == ["mhariri", "ukaguzi"] and {m for m, _ in s.kumbukumbu} == {"gemini"}
    assert r["majaribio"] == 2 and r["maandishi_sahihi"].endswith("asilimia 20.")
    assert "'Kila' hufuatwa na umoja" in s.ujumbe[1][2]            # orodha ya ukaguzi imetumwa kwa Gemini


def test_ukaguzi_wa_pili_unaopoteza_namba_unakataliwa(monkeypatch):
    def gemini(kazi, t):
        if kazi == "ukaguzi":
            return {"maandishi_sahihi": "Viongozi wanaposhirikisha malengo wazi, tija huongezeka sana.", "marekebisho": []}
        return {"maandishi_sahihi": SAHIHI, "marekebisho": []}

    Simu(monkeypatch, gemini=gemini)
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", hali="gemini_pekee")
    assert r["maandishi_sahihi"] == SAHIHI and "20" in r["maandishi_sahihi"]


def test_ukaguzi_wa_lazima_unaweza_kuzimwa(monkeypatch):
    s = Simu(monkeypatch, gemini=lambda k, t: {"maandishi_sahihi": SAHIHI, "marekebisho": []})
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili",
                            hali="gemini_pekee", ukaguzi_wa_lazima=False)
    assert r["majaribio"] == 1 and len(s.kumbukumbu) == 1


# ---------- Kikomo cha matumizi (429) ----------
def test_kosa_la_429_linarudiwa_kwa_kusubiri(monkeypatch):
    kusubiri = []
    monkeypatch.setattr(se.time, "sleep", kusubiri.append)
    idadi = {"n": 0}

    def kazi(x):
        idadi["n"] += 1
        if idadi["n"] < 3:
            raise RuntimeError("429 RESOURCE_EXHAUSTED")
        return "sawa"

    assert se._piga_na_kusubiri(kazi, 1) == "sawa" and idadi["n"] == 3 and kusubiri == [2.0, 5.0]


def test_kosa_lingine_halirudiwi(monkeypatch):
    monkeypatch.setattr(se.time, "sleep", lambda s: pytest.fail("haipaswi kusubiri"))
    with pytest.raises(ValueError):
        se._piga_na_kusubiri(lambda: (_ for _ in ()).throw(ValueError("ufunguo si sahihi")))


# ---------- Njia za huduma ----------
def test_njia_za_huduma(monkeypatch):
    s = Simu(monkeypatch, gemini=mtafsiri_na_mhariri, groq=mtafsiri_na_mhariri)
    assert mp.tafsiri_na_hariri_bure(EN, majaribio_ya_juu=1)["hali"] == "bure"
    assert mp.hariri_kwa_gemini_pekee("Darasa lina kelele.", majaribio_ya_juu=2)["hali"] == "gemini_pekee"


# ---------- Kanuni mpya: 'kila' + umoja, na nomino za ma- ----------
def kosa(sentensi):
    return K.kagua_sentensi_nzima(sentensi, kagua_alama=False)["makosa"]


def test_kila_na_umoja():
    m = [x for x in kosa("Kila wanafunzi ana kitabu.") if x["chanzo"] == "kila_umoja"]
    assert m and m[0]["mapendekezo"] == ["Kila mwanafunzi"]
    assert mp.rekebisha_kiotomatiki("Kila wanafunzi ana kitabu.", herufi_kubwa_na_kituo=False)["maandishi"] \
        == "Kila mwanafunzi ana kitabu."
    for sahihi in ("Kila mdau anatimiza wajibu wake.", "Kila siku tunasoma.", "Kila mmoja atachukua kitabu."):
        assert not [x for x in kosa(sahihi) if x["chanzo"] == "kila_umoja"]


def test_nomino_za_ma_zinachukua_ya():
    m = [x for x in kosa("Matumizi imesaidia wanafunzi.") if x["chanzo"] == "kiima_kitenzi"]
    assert m and m[0]["mapendekezo"][0] == "yamesaidia"
    for sahihi in ("Matumizi yamesaidia wanafunzi.", "Mafanikio yamekuja.", "Mazingira yamebadilika."):
        assert not [x for x in kosa(sahihi) if x["aina"] == "NGELI"]
