"""
test_sanifu.py - Majaribio ya kanuni_ya_sarufi.py (toleo 2.8).

Endesha:   pytest test_sanifu.py -v
Kila kosa jipya ulilokutana nalo kwenye app, liongeze kwenye orodha inayofaa hapa chini.
"""

import pytest

from kanuni_ya_sarufi import KanuniZaSarufiKiswahili

K = KanuniZaSarufiKiswahili()


def sahihisha(maandishi: str) -> str:
    return K.kagua_sentensi_nzima(maandishi)["maandishi_yaliyorekebishwa"]


# (ingizo lenye kosa, matokeo sahihi)
INAYOPASWA_KUREKEBISHWA = [
    # Ngeli ya ma-/mi- (kiima <-> kitenzi)
    ("Matumizi mabaya ya mifereji imesababisha hasara.", "Matumizi mabaya ya mifereji yamesababisha hasara."),
    ("Matumizi ya dawa umekuwa mbaya.", "Matumizi ya dawa yamekuwa mbaya."),
    ("Mafanikio vimekuwa mengi.", "Mafanikio yamekuwa mengi."),
    ("Mifano vinaonyesha hali halisi.", "Mifano inaonyesha hali halisi."),
    ("Mifano yanaweza kusaidia.", "Mifano inaweza kusaidia."),
    ("Miti yanakua haraka.", "Miti inakua haraka."),
    ("Mifano mizuri yanasaidia.", "Mifano mizuri inasaidia."),
    # Kivumishi na ngeli
    ("Kikwazo kubwa kimejitokeza.", "Kikwazo kikubwa kimejitokeza."),
    ("Mkutano fupi ulifanyika.", "Mkutano mfupi ulifanyika."),
    ("Mashirika vidogo vidogo yanakua.", "Mashirika madogomadogo yanakua."),
    ("Mashirika vidogovidogo yanakua.", "Mashirika madogomadogo yanakua."),
    # Yambiwa na shamirisho
    ("Watoto anasoma vizuri.", "Watoto wanasoma vizuri."),
    ("Anapowajali afya ya wafanyakazi.", "Anapojali afya ya wafanyakazi."),
    ("Wanapowajali afya yao wanafanikiwa.", "Wanapojali afya yao wanafanikiwa."),
    ("Kila mfugaji wanazingatia kanuni.", "Kila mfugaji anazingatia kanuni."),
    # Tahajia na maneno ambata
    ("Serekali imeanza mradi kwasababu ya maswala mengi.", "Serikali imeanza mradi kwa sababu ya masuala mengi."),
    ("Wanyama pori wanalindwa na nguvu kazi kubwa.", "Wanyamapori wanalindwa na nguvukazi kubwa."),
    ("Anafanya sawa sawa na ndogo ndogo.", "Anafanya sawasawa na ndogondogo."),
    # Alama na barua
    ("Dar es Salaam, 15 Novemba, 2026", "Dar es Salaam, 15 Novemba 2026"),
    ("Kosa moja limetokea; Matokeo yake ni makubwa.", "Kosa moja limetokea. Matokeo yake ni makubwa."),
    ("Hii ni mwisho wa makala..", "Hii ni mwisho wa makala."),
    ("Makala hii ni nzuri sana,", "Makala hii ni nzuri sana."),
    ("Kuhusu: ombi la kazi\nTunaomba nafasi.", "KUHUSU: OMBI LA KAZI\nTunaomba nafasi."),
]

# Sentensi sahihi: injini isizibadilishe hata kidogo (hupima "false positives")
HAZIPASWI_KUGUSWA = [
    "Akina mama wanasoma kitabu kizuri.",
    "Watoto wanasoma vizuri.",
    "Watoto wazuri wanasoma vizuri.",
    "Nyumba kubwa ni nzuri.",
    "Kaka dogo anasoma.",
    "Mkutano mfupi ulifanyika.",
    "Mashirika madogomadogo yanakua.",
    "Nguvukazi kubwa ipo.",
    "Matumizi ya fedha yameongezeka.",
    "Matumizi ya dawa, hali imekuwa mbaya.",
    "Mifano ya mafanikio yameonyesha njia.",
    "Ulinzi wa watu ni muhimu.",
    "Ingawa alikuja; Matokeo yake ni mazuri.",
    "Anafanya polepole polepole.",
    "Tunasubiri...",
    "Kila siku walimu wanafundisha.",
    "Madaktari wamefika. Mtoto mbaya analia.",
    "Mpendwa Bw. Juma,\nTunatanguliza salamu.\nWenu katika ujenzi wa taifa,\nDkt. Maroa",
]


@pytest.mark.parametrize("ingizo, linalotarajiwa", INAYOPASWA_KUREKEBISHWA)
def test_inarekebisha(ingizo, linalotarajiwa):
    assert sahihisha(ingizo) == linalotarajiwa


@pytest.mark.parametrize("sentensi", HAZIPASWI_KUGUSWA)
def test_haiharibu_sentensi_sahihi(sentensi):
    assert sahihisha(sentensi) == sentensi


def test_kagua_tafsiri_msamiati():
    makosa = K.kagua_tafsiri("Kiingereza", "local languages and fraudsters",
                             "lugha za kienyeji na wadanganyifu")
    mapendekezo = {m["mapendekezo"][0] for m in makosa}
    assert {"lugha za wenyeji", "walaghai"} <= mapendekezo


def test_kagua_tafsiri_jozi_nyingine_haifanyi_kitu():
    assert K.kagua_tafsiri("Kifaransa", "fraudsters", "wadanganyifu") == []


def test_ku_ya_kiingereza_inaonyeshwa():
    makosa = K.kagua_sentensi_nzima("Tunataka ku-adopt mfumo mpya.")["makosa"]
    assert any(m["chanzo"] == "kanuni_kiingereza" for m in makosa)


def test_maandishi_tupu():
    assert K.kagua_sentensi_nzima("")["sahihi"] is True
