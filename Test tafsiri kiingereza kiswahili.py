"""Majaribio ya kanuni tano za tafsiri ya Kiingereza -> Kiswahili. Endesha: pytest"""
import pytest

import mhariri_pro as mp
import sanifu_editor as se
from kanuni_ya_sarufi import KanuniZaSarufiKiswahili, maelekezo_ya_tafsiri

K = KanuniZaSarufiKiswahili()

# Tafsiri halisi kutoka kwenye skrini ya Mtafsiri wa Lugha & Muktadha Suite Pro
EN = ("Effective communication is essential for the success of any modern organization. When leaders share clear goals "
      "and listen carefully to the feedback of their team members, productivity increases significantly. Furthermore, "
      "investing in continuous training allows employees to adapt to new technologies and solve complex problems "
      "efficiently. Ultimately, a supportive work environment builds trust, encourages innovation, and ensures "
      "long-term growth for both the company and the community it serves.")
SW = ("Mawasiliano yenye ufanisi ni muhimu kwa mafanikio ya shirika lolote la kisasa. Viongozi wanaposhiriki malengo "
      "wazi na kusikiliza kwa makini maoni ya wanachama wa timu, uzalishaji huongezeka kwa kiasi kikubwa. Aidha, "
      "kuwekeza katika mafunzo endelevu huwasaidia wafanyakazi kuendana na teknolojia mpya na kutatua matatizo magumu "
      "kwa ufanisi. Hatimaye, mazingira ya kazi yenye msaada hujenga imani, kuhamasisha ubunifu, na kuhakikisha ukuaji "
      "wa muda mrefu kwa kampuni na jamii inayohudumiwa.")


def rekebisha(en, sw, kituo=False, lugha="Kiingereza (English)"):
    return K.rekebisha_tafsiri(lugha, en, sw, kituo_cha_mwisho=kituo)["maandishi"]


# ---- Kanuni 1: usambamba wa vitenzi ----
def test_usambamba_wa_hu():
    r = rekebisha(EN, SW)
    assert "hujenga uaminifu, huhamasisha ubunifu, na huhakikisha ukuaji" in r


@pytest.mark.parametrize("sw", [
    "Hupenda kusoma, kuandika, na kuimba.",                 # ku- ni shamirisho la 'hupenda'
    "Anapenda kusoma, kuandika na kuimba.",                 # hakuna hu-
    "Hujenga uaminifu na kuhamasisha ubunifu kunahitaji muda.",   # hakuna mkato kabla ya ku-
])
def test_usambamba_hauharibu_sentensi_sahihi(sw):
    assert rekebisha("x", sw) == sw


# ---- Kanuni 2: nahau ----
def test_nahau_ya_mstari_wa_nukta_inaonywa_bila_kubadilishwa():
    t = "Alitia saini kwenye mstari wa nukta."
    makosa = K.kagua_sentensi_nzima(t)["makosa"]
    assert any(m["aina"] == "KIROBOTI" and "kutia saini mkataba rasmi" in m["ujumbe"] for m in makosa)
    r = mp.chambua(t)
    assert not [m for m in r["masuala"] if "mstari" in m["kabla"]][0]["inaweza_kutumika"]


# ---- Kanuni 3: ku- ya kiima cha kitenzi jina ----
def test_ku_ya_kiima():
    assert rekebisha("x", "Kupuuza dalili za mapema inaweza kusababisha madhara.") == \
        "Kupuuza dalili za mapema kunaweza kusababisha madhara."


def test_ku_haibadilishi_kishazi_kipya_wala_kuna():
    assert rekebisha("x", "Kupuuza dalili, daktari anaweza kusema hapana.") == \
        "Kupuuza dalili, daktari anaweza kusema hapana."
    assert rekebisha("x", "Kuna watu wanaweza kuja.") == "Kuna watu wanaweza kuja."
    assert rekebisha("x", "Kuwekeza katika mafunzo kunaweza kusaidia.") == "Kuwekeza katika mafunzo kunaweza kusaidia."


# ---- Kanuni 4: msamiati wa kitaaluma (hutegemea chanzo cha Kiingereza) ----
def test_msamiati_kutoka_kwenye_tafsiri_ya_picha():
    r = rekebisha(EN, SW)
    assert "tija huongezeka" in r and "uzalishaji" not in r
    assert "hujenga uaminifu" in r and "imani" not in r
    assert "wanaposhirikisha malengo" in r


def test_shirikisha_haiguswi_nomino_washiriki():
    assert rekebisha("Participants share goals.", "Washiriki wanashiriki malengo.") == \
        "Washiriki wanashirikisha malengo."


def test_msamiati_hautumiki_bila_neno_la_chanzo():
    assert rekebisha("Production grew.", "Uzalishaji uliongezeka.") == "Uzalishaji uliongezeka."
    assert rekebisha("Good service builds loyalty.", "Huduma bora hujenga uaminifu.") == "Huduma bora hujenga uaminifu."


def test_msamiati_unahitaji_jozi_ya_kiingereza():
    assert rekebisha("la productivité", "uzalishaji huongezeka", lugha="Kifaransa") == "uzalishaji huongezeka"


def test_maambukizi_yaliyokwisha_komaa():
    r = rekebisha("Treating advanced infections is hard.", "Kutibu maambukizi ya hali ya juu ni vigumu.")
    assert "maambukizi yaliyokwisha komaa" in r


# ---- Kanuni 5: tahajia na nukta ya mwisho ----
def test_tahajia_mhimili():
    assert rekebisha("x", "Mfupa wa muhimili ni muhimu.") == "Mfupa wa mhimili ni muhimu."


def test_nukta_ya_mwisho_kwa_jozi_ya_kiingereza_pekee():
    assert rekebisha("Many people", "Watu wengi", kituo=True).endswith("Watu wengi.")
    assert not rekebisha("Many people", "Watu wengi", kituo=False).endswith(".")
    assert not K.rekebisha_tafsiri("Kifaransa", "Beaucoup", "Watu wengi")["maandishi"].endswith(".")


# ---- Maelekezo kwa AI ----
def test_maelekezo_yanajumuisha_kanuni_za_jozi_kwa_kiingereza_pekee():
    for jina in ("Kiingereza", "Kiingereza (English)", "English"):
        assert "ENGLISH-TO-SWAHILI TRANSLATION RULES" in maelekezo_ya_tafsiri(jina, "Kiswahili")
        assert "ENGLISH-TO-SWAHILI TRANSLATION RULES" in se.jenga_mfumo(jina, "Kiswahili")
    assert "ENGLISH-TO-SWAHILI" not in maelekezo_ya_tafsiri("Kifaransa", "Kiswahili")
    assert "ENGLISH-TO-SWAHILI" not in se.jenga_mfumo("Kifaransa", "Kiswahili")
    assert "YAMBIWA" in maelekezo_ya_tafsiri("Kiingereza", "Kiswahili")     # kanuni 16 za awali zimebaki
    assert "ENGLISH-TO-SWAHILI" not in se.jenga_mfumo("Kiswahili", "Kiswahili")


def test_majina_ya_orodha_ya_app_yanatambuliwa():
    from lugha_za_afrika import pata_lugha
    l = pata_lugha("Kiingereza (English)")
    assert l["jina"] == "Kiingereza" and not l["maalum"]


# ---- Mhariri Pro na huduma ----
def test_pro_inaonyesha_masuala_ya_tafsiri_na_kuyatumia():
    r = mp.chambua(SW, lugha_chanzo="Kiingereza", chanzo=EN, herufi_kubwa_na_kituo=False, kituo_cha_mwisho=True)
    chanzo = {m["chanzo"] for m in r["masuala"]}
    assert "Usambamba wa vitenzi" in chanzo and any("Msamiati" in c for c in chanzo)
    out = mp.tumia_marekebisho(SW, r["masuala"])
    assert "tija huongezeka" in out and "huhamasisha ubunifu" in out and out.endswith("jamii inayohudumiwa.")


def test_rekebisha_tafsiri_ya_kiswahili_kwa_mtafsiri_uliopo():
    r = mp.rekebisha_tafsiri_ya_kiswahili(SW, lugha_chanzo="Kiingereza (English)", chanzo=EN)
    assert "tija huongezeka" in r["maandishi"] and r["maandishi"].endswith(".")
    assert "wanaposhirikisha malengo" in r["maandishi"] and "huhakikisha ukuaji" in r["maandishi"]
    # bila chanzo: hakuna nukta wala msamiati
    r2 = mp.rekebisha_tafsiri_ya_kiswahili("watu wengi")
    assert r2["maandishi"] == "watu wengi"


# ---- Mfumo mzima ----
def test_mfumo_mzima_unarekebisha_tafsiri_ya_ai(monkeypatch):
    simu = []

    def bandia(mfumo, t, temperature=0.1, mtoa=None):
        simu.append(mfumo)
        return {"maandishi_sahihi": SW, "marekebisho": []}

    monkeypatch.setattr(se, "piga_ai", bandia)
    r = se.hariri_kwa_ubora(EN, kamusi=set(), lugha_chanzo="Kiingereza", lugha_lengwa="Kiswahili", majaribio_ya_juu=1)
    assert "ENGLISH-TO-SWAHILI TRANSLATION RULES" in simu[0]
    assert "tija huongezeka" in r["maandishi_sahihi"] and "hujenga uaminifu, huhamasisha" in r["maandishi_sahihi"]
    assert r["maandishi_sahihi"].endswith(".")
    assert not r["makosa_yaliyobaki"]
