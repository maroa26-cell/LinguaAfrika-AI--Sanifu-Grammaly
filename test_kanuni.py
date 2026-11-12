"""
Majaribio ya moduli ya kanuni_ya_sarufi.
Endesha kwa: pytest test_kanuni.py -v
"""

import pytest
from kanuni_ya_sarufi import (
    KanuniZaSarufiKiswahili,
    KitambuziNgeli,
    MkaguziSarufi,
)


@pytest.fixture
def kanuni():
    return KanuniZaSarufiKiswahili()


@pytest.fixture
def kitambuzi():
    return KitambuziNgeli()


# ============================================================
# MAJARIBIO YA UTAMBUZI WA NGELI
# ============================================================

class TestTambuaNgeli:

    @pytest.mark.parametrize("neno,ngeli_inayotarajiwa", [
        # A-WA umoja
        ("mtoto", "A-WA_SG"),
        ("mwanafunzi", "A-WA_SG"),
        ("mwanamke", "A-WA_SG"),
        ("mwalimu", "A-WA_SG"),
        ("mlevi", "A-WA_SG"),
        # A-WA wingi
        ("watoto", "A-WA_PL"),
        ("wanafunzi", "A-WA_PL"),
        ("walimu", "A-WA_PL"),
        ("watu", "A-WA_PL"),
        # KI-VI umoja
        ("kitabu", "KI-VI_SG"),
        ("kiti", "KI-VI_SG"),
        ("chakula", "KI-VI_SG"),
        ("kikombe", "KI-VI_SG"),
        # KI-VI wingi
        ("vitabu", "KI-VI_PL"),
        ("viti", "KI-VI_PL"),
        ("vyakula", "KI-VI_PL"),
        # U-I umoja
        ("mti", "U-I_SG"),     # ubaguzi!
        ("mkono", "U-I_SG"),   # ubaguzi!
        ("uhuru", "U-I_SG"),
        ("umakini", "U-I_SG"),
        # U-I wingi
        ("miti", "U-I_PL"),
        ("mikono", "U-I_PL"),
        # LI-YA umoja
        ("jicho", "LI-YA_SG"),
        ("gari", "LI-YA_SG"),
        ("shamba", "LI-YA_SG"),
        # LI-YA wingi
        ("macho", "LI-YA_PL"),
        ("magari", "LI-YA_PL"),
        ("mashamba", "LI-YA_PL"),
        # I-ZI (maneno ya kawaida yenye viambishi vya udanganyifu)
        ("chai", "I-ZI_SG"),    # ubaguzi!
        ("shule", "I-ZI_SG"),   # ubaguzi!
        ("saa", "I-ZI_SG"),     # ubaguzi!
        ("nyumba", "I-ZI_SG"),
        ("kazi", "I-ZI_SG"),
        ("simu", "I-ZI_SG"),
    ])
    def test_ngeli_ya_maneno_ya_kawaida(self, kitambuzi, neno, ngeli_inayotarajiwa):
        matokeo = kitambuzi.tambua(neno)
        assert matokeo.ngeli == ngeli_inayotarajiwa, (
            f"'{neno}' ilitarajiwa {ngeli_inayotarajiwa}, ilipatikana {matokeo.ngeli} "
            f"(chanzo: {matokeo.chanzo}, uhakika: {matokeo.uhakika})"
        )

    def test_uhakika_wa_exceptions_ni_kamili(self, kitambuzi):
        matokeo = kitambuzi.tambua("mtoto")
        assert matokeo.uhakika == 1.0
        assert matokeo.chanzo == "exceptions"

    def test_uhakika_wa_ubaguzi_ni_juu(self, kitambuzi):
        matokeo = kitambuzi.tambua("chai")
        assert matokeo.uhakika >= 0.9
        assert matokeo.chanzo == "ubaguzi"

    def test_neno_lisilotambulika_linarudisha_none(self, kitambuzi):
        matokeo = kitambuzi.tambua("xyzabc")
        assert matokeo.ngeli is None
        assert matokeo.uhakika == 0.0

    def test_caching_inafanya_kazi(self, kitambuzi):
        r1 = kitambuzi.tambua("mtoto")
        r2 = kitambuzi.tambua("mtoto")
        # Ni kitu kile kile kilichohifadhiwa
        assert r1 is r2 or (r1.ngeli == r2.ngeli and r1.uhakika == r2.uhakika)


# ============================================================
# MAJARIBIO YA UPATANISHO WA VIVUMISHI
# ============================================================

class TestUpatanishoVivumishi:

    def test_kivumishi_sahihi_hakitoi_kosa(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto mdogo alikula chakula.")
        makosa_ya_ngeli = [k for k in matokeo["makosa"] if k["aina"] == "NGELI"]
        assert len(makosa_ya_ngeli) == 0

    def test_kivumishi_kibaya_kinatoa_kosa(self, kanuni):
        # "Mtoto wakubwa" – kivumishi cha A-WA_PL kinatumika kwa A-WA_SG
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto wakubwa alikuja.")
        makosa_ya_ngeli = [k for k in matokeo["makosa"] if k["aina"] == "NGELI"]
        assert len(makosa_ya_ngeli) >= 1
        kosa = makosa_ya_ngeli[0]
        assert "mdogo" in " ".join(kosa["mapendekezo"]) or "mkubwa" in " ".join(kosa["mapendekezo"])

    def test_ngeli_ya_karibu_inaheshimiwa(self, kanuni):
        # Maneno mawili ya ngeli tofauti; kivumishi kinapaswa kupatana na la karibu
        matokeo = kanuni.kagua_sentensi_nzima("Vitabu vizuri viko mezani.")
        makosa_ya_ngeli = [k for k in matokeo["makosa"] if k["aina"] == "NGELI"]
        assert len(makosa_ya_ngeli) == 0

    def test_ngeli_ya_karibu_ikikosewa(self, kanuni):
        # "Vitabu kikubwa" – KI-VI_SG kwa KI-VI_PL
        matokeo = kanuni.kagua_sentensi_nzima("Vitabu kikubwa viko mezani.")
        makosa_ya_ngeli = [k for k in matokeo["makosa"] if k["aina"] == "NGELI"]
        assert len(makosa_ya_ngeli) >= 1


# ============================================================
# MAJARIBIO YA KIROBOTI
# ============================================================

class TestKiroboti:

    def test_kiroboti_kinagundulika(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mimi ni baridi leo asubuhi.")
        makosa_ya_kiroboti = [k for k in matokeo["makosa"] if k["aina"] == "KIROBOTI"]
        assert len(makosa_ya_kiroboti) == 1
        assert "mimi ni baridi" in makosa_ya_kiroboti[0]["neno"].lower()

    def test_kiroboti_ndani_ya_sentensi_ndefu(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Yeye husema kila mara kwamba mimi ni njaa.")
        makosa_ya_kiroboti = [k for k in matokeo["makosa"] if k["aina"] == "KIROBOTI"]
        assert len(makosa_ya_kiroboti) == 1

    def test_sentensi_safi_haina_kiroboti(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Nina njaa sana leo.")
        makosa_ya_kiroboti = [k for k in matokeo["makosa"] if k["aina"] == "KIROBOTI"]
        assert len(makosa_ya_kiroboti) == 0


# ============================================================
# MAJARIBIO YA UANDISHI
# ============================================================

class TestUandishi:

    def test_herufi_kubwa_inahitajika(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("mtoto alikuja.")
        makosa = [k for k in matokeo["makosa"] if k["aina"] == "ALAMA"]
        assert any("herufi kubwa" in k["ujumbe"].lower() for k in makosa)

    def test_alama_ya_kituo_inahitajika(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto alikuja")
        makosa = [k for k in matokeo["makosa"] if k["aina"] == "ALAMA"]
        assert any("kituo" in k["ujumbe"].lower() for k in makosa)

    def test_sentensi_sahihi_haina_makosa_ya_alama(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto alikuja.")
        makosa_ya_alama = [k for k in matokeo["makosa"] if k["aina"] == "ALAMA"]
        assert len(makosa_ya_alama) == 0


# ============================================================
# MAJARIBIO YA API
# ============================================================

class TestAPI:

    def test_dict_ina_vipengele_vinavyotarajiwa(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto mdogo alikuja.")
        assert "sahihi" in matokeo
        assert "makosa" in matokeo
        assert "idadi_ya_makosa" in matokeo

    def test_nafasi_ya_kosa_ni_sahihi(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("Mtoto wakubwa alikuja.")
        makosa_ya_ngeli = [k for k in matokeo["makosa"] if k["aina"] == "NGELI"]
        assert len(makosa_ya_ngeli) >= 1
        kosa = makosa_ya_ngeli[0]
        # Nafasi inapaswa kuwa 6 (baada ya "Mtoto ")
        assert kosa["nafasi"] == 6

    def test_kurekebisha_kinatoa_sentensi_mpya(self, kanuni):
        matokeo = kanuni.kagua_na_kurekebisha("mtoto mdogo alikuja")
        assert "sentensi_iliyorekebishwa" in matokeo
        assert matokeo["sentensi_iliyorekebishwa"][0].isupper()

    def test_sentensi_tupu_inatoa_kosa(self, kanuni):
        matokeo = kanuni.kagua_sentensi_nzima("")
        assert matokeo["sahihi"] is False
        assert len(matokeo["makosa"]) == 1
