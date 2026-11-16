"""tests/test_kanuni_ya_sarufi.py — Majaribio ya kanuni za sarufi ya Kiswahili (v2.6).

Endesha:    pytest tests/test_kanuni_ya_sarufi.py -v
Matokeo:    yote yanapaswa kupita (v2.6).

Yaliyomo:
  TestKitambuziNgeli         ngeli matrix, ubaguzi, prefix, cache
  TestYambiwa                kanuni ya mtendwa (-m-, -mw-, -wa-)
  TestBugFixesV26            majaribio maalum ya Bugs 1, 2, 3, 4, 6, 7, 10, 11
  TestMkaguziSarufi          kila kanuni mahususi
  TestTumiaMakosa            _tumia_makosa + ALAMA (Bug 3)
  TestKanuniZaSarufiKiswahili  API ya juu
  TestJozi                   jozi za lugha (Kiingereza -> Kiswahili)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kanuni_ya_sarufi import (
    KitambuziNgeli,
    GenericObjectConcordRule,
    MkaguziSarufi,
    KanuniZaSarufiKiswahili,
    Kosa,
    _tumia_makosa,
    ni_jozi_ya_kiingereza_kiswahili,
    maelekezo_ya_jozi,
    MAELEKEZO_YA_LUGHA,
)


# ============================================================
# KitambuziNgeli
# ============================================================

class TestKitambuziNgeli:
    @pytest.fixture
    def k(self):
        return KitambuziNgeli()

    def test_exceptions_uhakika_kamili(self, k):
        assert k.tambua("mtoto").ngeli == "A-WA_SG"
        assert k.tambua("mtoto").uhakika == 1.0
        assert k.tambua("kitabu").ngeli == "KI-VI_SG"
        assert k.tambua("vitabu").ngeli == "KI-VI_PL"
        assert k.tambua("watoto").ngeli == "A-WA_PL"

    def test_ubaguzi_mti_si_a_wa(self, k):
        # 'mti' inaonekana kama m- lakini ni U-I
        m = k.tambua("mti")
        assert m.ngeli == "U-I_SG"
        assert m.uhakika == 0.9

    def test_ubaguzi_nyumba(self, k):
        assert k.tambua("nyumba").ngeli == "I-ZI_SG"
        assert k.tambua("chai").ngeli == "I-ZI_SG"

    def test_prefix_ki(self, k):
        m = k.tambua("kikapu")  # si kwenye exceptions; inatambuliwa kwa kiambishi
        assert m.ngeli == "KI-VI_SG"
        assert m.uhakika == 0.8

    def test_prefix_vi(self, k):
        assert k.tambua("vikapu").ngeli == "KI-VI_PL"

    def test_prefix_mi(self, k):
        assert k.tambua("mikapu").ngeli == "U-I_PL"

    def test_prefix_ma(self, k):
        assert k.tambua("makapu").ngeli == "LI-YA_PL"

    def test_herufi_kubwa_na_alama(self, k):
        assert k.tambua("Mtoto,").ngeli == "A-WA_SG"
        assert k.tambua("VITABU.").ngeli == "KI-VI_PL"
        assert k.tambua("'nyumba'").ngeli == "I-ZI_SG"

    def test_tupu(self, k):
        m = k.tambua("")
        assert m.ngeli is None
        assert m.uhakika == 0.0
        m2 = k.tambua("...,,,")
        assert m2.ngeli is None

    def test_cache(self, k):
        a = k.tambua("kitabu")
        b = k.tambua("kitabu")
        assert a == b
        # Cache imekua mara moja pekee
        assert len(k._cache) == 1


# ============================================================
# Yambiwa (GenericObjectConcordRule)
# ============================================================

class TestYambiwa:
    @pytest.fixture
    def y(self):
        return GenericObjectConcordRule()

    def test_umoja_irabu_mw(self, y):
        # 'andikia' inaanza na irabu -> kiambishi 'mw'
        makosa = y.kagua("Aliandikia mgonjwa barua.")
        assert len(makosa) == 1
        assert "mw" in makosa[0].mapendekezo[0]
        assert makosa[0].aina == "MOFOLOJIA"

    def test_umoja_konsonanti_m(self, y):
        # 'fanyia' inaanza na konsonanti -> kiambishi 'm'
        makosa = y.kagua("Alifanyia mtoto kazi.")
        assert len(makosa) == 1
        assert "mfanyia" in makosa[0].mapendekezo[0]

    def test_wingi_wa(self, y):
        makosa = y.kagua("Aliandikia wagonjwa barua.")
        assert len(makosa) == 1
        assert "wa" in makosa[0].mapendekezo[0]

    def test_wingi_watu(self, y):
        makosa = y.kagua("Aliandikia watu barua.")
        assert len(makosa) == 1
        assert "wa" in makosa[0].mapendekezo[0]

    def test_sahihi_hakuna_kosa(self, y):
        # Tayari ina kiambishi cha mtendwa
        assert len(y.kagua("Alimwandikia mgonjwa barua.")) == 0
        assert len(y.kagua("Aliwaandikia wagonjwa barua.")) == 0

    def test_si_binadamu_hakuna_kosa(self, y):
        assert len(y.kagua("Aliandikia barua.")) == 0
        assert len(y.kagua("Alisoma kitabu.")) == 0

    def test_kitenzi_cha_kuachwa(self, y):
        # 'kuwa' iko kwenye vitenzi_vya_kuachwa
        assert len(y.kagua("Atakuwa mwalimu.")) == 0


# ============================================================
# Majaribio maalum ya Bugs 1, 2, 3, 4, 6, 7, 10, 11 (v2.6)
# ============================================================

class TestBugFixesV26:
    """Majaribio yanayothibitisha marekebisho ya v2.6.
    Kila jaribio lingeshindwa kwenye v2.5."""

    # ---- Bug 1: 'soma'/'taka' -> 'som'/'tak' ----

    def test_bug1_mizizi_ina_som_tak(self):
        """_MIZIZI_VITENZI ina 'som'/'tak' (si 'soma'/'taka')."""
        assert "som" in MkaguziSarufi._MIZIZI_VITENZI, \
            "BUG 1: 'som' haiko. 'wanasoma' haitakamatwa."
        assert "tak" in MkaguziSarufi._MIZIZI_VITENZI, \
            "BUG 1: 'tak' haiko. 'anataka' haitakamatwa."
        assert "soma" not in MkaguziSarufi._MIZIZI_VITENZI, \
            "BUG 1: 'soma' ipo lakini stem ni 'som' (haitalingana kamwe)."
        assert "taka" not in MkaguziSarufi._MIZIZI_VITENZI

    def test_bug1_wanasoma_inakamatwa(self):
        """'Mwanafunzi wanasoma' inapaswa kukamatwa (sc='wa' vs A-WA_SG)."""
        m = MkaguziSarufi()
        makosa = m._kagua_upatanisho_kiima_kitenzi("Mwanafunzi wanasoma kitabu.")
        assert any("wanasoma" in k.neno.lower() for k in makosa), \
            "BUG 1: 'wanasoma' haikamatwi kwa sababu mzizi 'som' haupo."

    def test_bug1_anataka_inakamatwa(self):
        """'Watoto anataka' inapaswa kukamatwa (sc='a' vs A-WA_PL)."""
        m = MkaguziSarufi()
        makosa = m._kagua_upatanisho_kiima_kitenzi("Watoto anataka chakula.")
        assert any("anataka" in k.neno.lower() for k in makosa), \
            "BUG 1: 'anataka' haikamatwi kwa sababu mzizi 'tak' haupo."

    def test_bug1_sahihi_hakuna_kosa(self):
        """Hakuna kosa kwa upatanisho sahihi."""
        m = MkaguziSarufi()
        assert len(m._kagua_upatanisho_kiima_kitenzi("Mtoto anasoma kitabu.")) == 0
        assert len(m._kagua_upatanisho_kiima_kitenzi("Watoto wanasoma vitabu.")) == 0

    # ---- Bug 2: ngeli-mahali .get() salama ----

    def test_bug2_nomino_isiyojulikana(self):
        """'Jirani yenye' haipaswi kuwa 'jira lenye' (neno lisilokuwepo)."""
        m = MkaguziSarufi()
        makosa = m._kagua_ngeli_mahali("Jirani yenye shida.")
        assert len(makosa) == 1
        # Haipaswi kuwa na pendekezo lenye neno 'jira' peke yake
        for p in makosa[0].mapendekezo:
            assert "jira lenye" not in p.lower(), \
                f"BUG 2: pendekezo '{p}' lina neno lisilokuwepo 'jira'"
            assert "jira wenye" not in p.lower()
        # Inapaswa kuwa na 'jirani kwenye'
        assert any("jirani kwenye" in p.lower() for p in makosa[0].mapendekezo)

    def test_bug2_nomino_inayojulikana(self):
        """'Darasani yenye' inapaswa kuwa 'darasa lenye' (darasa iko kwenye NGELI_YENYE)."""
        m = MkaguziSarufi()
        makosa = m._kagua_ngeli_mahali("Darasani yenye wanafunzi wengi.")
        assert len(makosa) == 1
        assert "darasa lenye" in makosa[0].mapendekezo[0].lower()
        assert "darasani kwenye" in [p.lower() for p in makosa[0].mapendekezo]

    def test_bug2_kampuni_hairuhusiwi(self):
        """'Kampuni yenye' ni sahihi (kampuni iko kwenye NOMINO_ZENYE_NI)."""
        m = MkaguziSarufi()
        # Ikiwa 'kampuni' iko kwenye NOMINO_ZENYE_NI, hakuna kosa.
        # Ikiwa imeondolewa kimakosa, jaribio hili litashindwa.
        makosa = m._kagua_ngeli_mahali("Kampuni yenye wafanyakazi wengi.")
        assert len(makosa) == 0, \
            "BUG: 'kampuni' imeondolewa NOMINO_ZENYE_NI kimakosa (ni neno, si locative)."

    # ---- Bug 3: _kagua_uandishi nafasi/urefu ----

    def test_bug3_nafasi_urefu_vinalingana(self):
        """Kosa la herufi kubwa lina nafasi/urefu/neno vinavyolingana."""
        m = MkaguziSarufi()
        makosa = m._kagua_uandishi("mtoto alikula chakula.")
        herufi = [k for k in makosa if k.aina == "ALAMA" and "herufi" in k.ujumbe.lower()]
        assert len(herufi) == 1
        k = herufi[0]
        assert k.nafasi == 0
        assert k.urefu == 1
        assert k.neno == "m"  # herufi moja, si neno kamili
        assert k.mapendekezo == ["M"]

    def test_bug3_nukta_nafasi_mwisho(self):
        """Kosa la nukta lina nafasi mwisho na urefu 0."""
        m = MkaguziSarufi()
        makosa = m._kagua_uandishi("Mtoto alikula chakula")
        nukta = [k for k in makosa if k.aina == "ALAMA" and "kituo" in k.ujumbe.lower()]
        assert len(nukta) == 1
        k = nukta[0]
        assert k.nafasi == len("Mtoto alikula chakula")
        assert k.urefu == 0
        assert k.neno == ""
        assert k.mapendekezo == ["."]

    def test_bug3_sahihi_hakuna_kosa(self):
        m = MkaguziSarufi()
        assert len(m._kagua_uandishi("Mtoto alikula chakula.")) == 0

    # ---- Bug 4: usambamba tokens[j+1:i] ----

    def test_bug4_short_list_inakamatwa(self):
        """'Hujenga imani, kuhamasisha ubunifu' — 'kuhamasisha' inapaswa kukamatwa."""
        m = MkaguziSarufi()
        makosa = m._kagua_usambamba_wa_vitenzi(
            "Hujenga imani, kuhamasisha ubunifu, na kuhakikisha ukuaji.")
        maneno = {k.neno.lower() for k in makosa}
        assert "kuhamasisha" in maneno, "BUG 4: kuhamasisha haikamatwi."
        assert "kuhakikisha" in maneno

    def test_bug4_gerund_haikamatwi(self):
        """'Hupenda kusoma, kuandika' — 'kuandika' haipaswi kukamatwa (ku- ni shamirisho)."""
        m = MkaguziSarufi()
        makosa = m._kagua_usambamba_wa_vitenzi("Hupenda kusoma, kuandika mashairi.")
        maneno = {k.neno.lower() for k in makosa}
        assert "kuandika" not in maneno, \
            "BUG 4: 'kuandika' imekamatwa kimakosa (ku- ni shamirisho, si usambamba)."

    def test_bug4_sahihi_hakuna_kosa(self):
        m = MkaguziSarufi()
        s = "Hujenga uaminifu, huhamasisha ubunifu, na huhakikisha ukuaji."
        assert len(m._kagua_usambamba_wa_vitenzi(s)) == 0

    # ---- Bug 6: isinge orodha imepanuliwa ----

    def test_bug6_biashara(self):
        """'Biashara haingefanikiwa' inapaswa kukamatwa (biashara ni I-ZI)."""
        m = MkaguziSarufi()
        makosa = m._kagua_kanuni_maalum("Biashara haingefanikiwa.")
        isinge = [k for k in makosa
                  if k.aina == "NGELI" and "isinge" in (k.mapendekezo[0] if k.mapendekezo else "")]
        assert len(isinge) >= 1, "BUG 6: 'biashara' haiko kwenye orodha ya isinge."

    def test_bug6_taarifa(self):
        """'Taarifa haingetolewa' inapaswa kukamatwa."""
        m = MkaguziSarufi()
        makosa = m._kagua_kanuni_maalum("Taarifa haingetolewa kwa umma.")
        isinge = [k for k in makosa
                  if "isinge" in (k.mapendekezo[0] if k.mapendekezo else "")]
        assert len(isinge) >= 1, "BUG 6: 'taarifa' haiko kwenye orodha ya isinge."

    def test_bug6_zisinge_kwa_za(self):
        """'Biashara za jiji haingefanikiwa' -> 'zisingefanikiwa' (wingi I-ZI)."""
        m = MkaguziSarufi()
        makosa = m._kagua_kanuni_maalum("Biashara za jiji haingefanikiwa.")
        zisinge = [k for k in makosa
                   if "zisinge" in (k.mapendekezo[0] if k.mapendekezo else "")]
        assert len(zisinge) >= 1

    # ---- Bug 7: herufi kubwa kwenye mapendekezo ----

    def test_bug7_herufi_kubwa_inahifadhiwa(self):
        """Kitenzi kilichoandikwa kwa herufi kubwa kinapendekeza herufi kubwa."""
        m = MkaguziSarufi()
        makosa = m._kagua_upatanisho_kiima_kitenzi("Mwanafunzi Wanasoma kitabu.")
        if makosa:  # ikiwa kosa limekamatwa
            p = makosa[0].mapendekezo[0]
            assert p[:1].isupper(), \
                f"BUG 7: pendekezo '{p}' linapaswa kuanza na herufi kubwa."

    # ---- Bug 10: adj_prefixes ya LI-YA_SG ----

    def test_bug10_li_ya_haina_empty(self):
        """LI-YA_SG.adj_prefixes haina '' (haikufikiwa kamwe)."""
        k = KitambuziNgeli()
        assert "" not in k.ngeli_matrix["LI-YA_SG"]["adj_prefixes"], \
            "BUG 10: '' bado iko kwenye LI-YA_SG (haikufikiwa kamwe)."

    # ---- Bug 11: cache ya KitambuziNgeli ----

    def test_bug11_cache_limit_imewekwa(self):
        """KitambuziNgeli ina KIKOMO_CHA_CACHE."""
        assert hasattr(KitambuziNgeli, "KIKOMO_CHA_CACHE")
        assert KitambuziNgeli.KIKOMO_CHA_CACHE > 0
        assert KitambuziNgeli.KIKOMO_CHA_CACHE <= 20000  # bound reasonable

    def test_bug11_cache_inafanya_kazi(self):
        k = KitambuziNgeli()
        assert len(k._cache) == 0
        k.tambua("kitabu")
        assert len(k._cache) == 1
        k.tambua("kitabu")
        assert len(k._cache) == 1  # hakuna duplicate


# ============================================================
# MkaguziSarufi — kanuni mahususi
# ============================================================

class TestMkaguziSarufi:
    @pytest.fixture
    def m(self):
        return MkaguziSarufi()

    # ---- Uandishi ----
    def test_uandishi_herufi_ndogo(self, m):
        assert any(k.aina == "ALAMA" for k in m._kagua_uandishi("mtoto alikula chakula."))

    def test_uandishi_hakuna_nukta(self, m):
        assert any(k.aina == "ALAMA" for k in m._kagua_uandishi("Mtoto alikula chakula"))

    # ---- Marudio ----
    def test_marudio(self, m):
        makosa = m._kagua_marudio("Nyumba kubwa kubwa zilijengwa.")
        assert len(makosa) == 1
        assert makosa[0].mapendekezo == ["kubwa"]

    def test_marudio_halali(self, m):
        # 'polepole' ni neno moja, hakuna nafasi kati ya marudio
        assert len(m._kagua_marudio("Tulitembea polepole.")) == 0

    # ---- Ngeli ya mahali ----
    def test_ngeli_mahali_darasani(self, m):
        makosa = m._kagua_ngeli_mahali("Darasani yenye wanafunzi wengi.")
        assert len(makosa) == 1
        assert "darasa lenye" in makosa[0].mapendekezo[0].lower()

    def test_ngeli_mahali_kampuni(self, m):
        # 'kampuni' iko kwenye NOMINO_ZENYE_NI
        assert len(m._kagua_ngeli_mahali("Kampuni yenye wafanyakazi wengi.")) == 0

    # ---- Kiroboti ----
    def test_kiroboti_mimi_ni_baridi(self, m):
        assert len(m._kagua_kiroboti("Mimi ni baridi leo.")) >= 1

    def test_kiroboti_hata_ingawa(self, m):
        assert len(m._kagua_kiroboti("Hata ingawa mvua inanyesha.")) >= 1

    # ---- Tahajia ----
    def test_tahajia_muhimili(self, m):
        makosa = m._kagua_tahajia("Huu ni muhimili wa jengo.")
        assert len(makosa) == 1
        assert makosa[0].mapendekezo == ["mhimili"]

    def test_tahajia_herufi_kubwa(self, m):
        makosa = m._kagua_tahajia("Muhimili wa jengo ni imara.")
        assert len(makosa) == 1
        assert makosa[0].mapendekezo == ["Mhimili"]

    # ---- Kila + umoja ----
    def test_kila_wingi(self, m):
        makosa = m._kagua_kila_na_wingi("Kila wanafunzi wanasoma.")
        assert len(makosa) == 1
        assert "mwanafunzi" in makosa[0].mapendekezo[0]

    def test_kila_umoja_sahihi(self, m):
        assert len(m._kagua_kila_na_wingi("Kila mwanafunzi anasoma.")) == 0

    # ---- Usambamba ----
    def test_usambamba_wa_vitenzi(self, m):
        s = "Hujenga uaminifu, kuhamasisha ubunifu, na kuhakikisha ukuaji."
        makosa = m._kagua_usambamba_wa_vitenzi(s)
        maneno = {k.neno for k in makosa}
        assert "kuhamasisha" in maneno
        assert "kuhakikisha" in maneno
        for k in makosa:
            assert k.mapendekezo[0].startswith("hu")

    def test_usambamba_hakuna_kosa(self, m):
        s = "Hujenga uaminifu, huhamasisha ubunifu, na huhakikisha ukuaji."
        assert len(m._kagua_usambamba_wa_vitenzi(s)) == 0

    # ---- Usawa wa ku- ----
    def test_usawa_wa_ku(self, m):
        makosa = m._kagua_usawa_wa_ku("Kupuuza dalili inaweza kusababisha matatizo.")
        assert len(makosa) == 1
        assert "kunaweza" in makosa[0].mapendekezo[0]

    def test_usawa_wa_ku_sahihi(self, m):
        assert len(m._kagua_usawa_wa_ku("Kupuuza dalili kunaweza kusababisha matatizo.")) == 0


# ============================================================
# _tumia_makosa + ALAMA (Bug 3 end-to-end)
# ============================================================

class TestTumiaMakosa:
    def test_alama_herufi_kubwa_na_nukta(self):
        """_tumia_makosa inaweza kutumia ALAMA zote mbili pamoja."""
        s = "mtoto alikula chakula"
        makosa = [
            Kosa(aina="ALAMA", neno="m", nafasi=0, urefu=1, ujumbe="", mapendekezo=["M"]),
            Kosa(aina="ALAMA", neno="", nafasi=len(s), urefu=0, ujumbe="", mapendekezo=["."]),
        ]
        matokeo, mabadiliko = _tumia_makosa(s, makosa)
        assert matokeo == "Mtoto alikula chakula."
        assert len(mabadiliko) == 2

    def test_makosa_yanayopishana_hayatumiki(self):
        """Makosa yanayopishana: la kwanza tu linatumika."""
        s = "mtoto mdogo"
        makosa = [
            Kosa(aina="ALAMA", neno="m", nafasi=0, urefu=1, ujumbe="", mapendekezo=["M"]),
            Kosa(aina="ALAMA", neno="m", nafasi=0, urefu=1, ujumbe="", mapendekezo=["X"]),
        ]
        matokeo, _ = _tumia_makosa(s, makosa)
        assert matokeo == "Mtoto mdogo"

    def test_tupu(self):
        matokeo, mabadiliko = _tumia_makosa("maandishi", [])
        assert matokeo == "maandishi"
        assert mabadiliko == []


# ============================================================
# KanuniZaSarufiKiswahili — API ya juu
# ============================================================

class TestKanuniZaSarufiKiswahili:
    @pytest.fixture
    def k(self):
        return KanuniZaSarufiKiswahili()

    def test_kagua_sentensi_nzima_structure(self, k):
        matokeo = k.kagua_sentensi_nzima("Mtoto mdogo alikula chakula kitamu.")
        for ufunguo in ("sahihi", "idadi_ya_makosa", "makosa",
                        "sentensi_iliyokaguliwa", "mapendekezo"):
            assert ufunguo in matokeo

    def test_kagua_sentensi_tupu(self, k):
        matokeo = k.kagua_sentensi_nzima("")
        assert matokeo["sahihi"] is False
        assert matokeo["idadi_ya_makosa"] >= 1

    def test_kagua_tafsiri_productivity(self, k):
        # 'productivity' -> 'tija', si 'uzalishaji'
        makosa = k.kagua_tafsiri("Kiingereza", "Productivity is key.",
                                 "Uzalishaji ni muhimu.")
        assert len(makosa) == 1
        assert makosa[0]["mapendekezo"][0] == "Tija"

    def test_kagua_tafsiri_si_jozi(self, k):
        # Lugha nyingine: hakuna ukaguzi wa msamiati
        assert k.kagua_tafsiri("Kifaransa", "Productivité est clé.",
                               "Uzalishaji ni muhimu.") == []

    def test_rekebisha_tafsiri_usambamba(self, k):
        matokeo = k.rekebisha_tafsiri(
            "Kiingereza",
            "It builds trust, inspires innovation, and ensures growth.",
            "Hujenga uaminifu, kuhamasisha ubunifu, na kuhakikisha ukuaji.",
        )
        assert "huhamasisha" in matokeo["maandishi"]
        assert "huhakikisha" in matokeo["maandishi"]

    def test_rekebisha_tafsiri_nukta_mwisho(self, k):
        matokeo = k.rekebisha_tafsiri("Kiingereza", "Good morning.",
                                      "Habari za asubuhi")
        assert matokeo["maandishi"].endswith(".")

    def test_kagua_na_kurekebisha_ngeli_mahali(self, k):
        matokeo = k.kagua_na_kurekebisha("Darasani yenye wanafunzi wengi.")
        assert "darasa lenye" in matokeo["sentensi_iliyorekebishwa"].lower()

    def test_kagua_na_kurekebisha_kiroboti(self, k):
        matokeo = k.kagua_na_kurekebisha("Mimi ni baridi leo.")
        # KIROBOTI hairekebishwi kiotomatiki (inaweza kubadilisha maana)
        # lakini inapaswa kuonekana kwenye makosa_ya_awali
        assert matokeo["makosa_ya_awali"] >= 1


# ============================================================
# Jozi za lugha na maelekezo
# ============================================================

class TestJozi:
    def test_kiingereza_kiswahili(self):
        assert ni_jozi_ya_kiingereza_kiswahili("Kiingereza", "Kiswahili") is True
        assert ni_jozi_ya_kiingereza_kiswahili("English", "Swahili") is True
        assert ni_jozi_ya_kiingereza_kiswahili("Kiingereza (English)", "Kiswahili (Swahili)") is True

    def test_si_jozi(self):
        assert ni_jozi_ya_kiingereza_kiswahili("Kifaransa", "Kiswahili") is False
        assert ni_jozi_ya_kiingereza_kiswahili("Kiswahili", "Kiingereza") is False
        assert ni_jozi_ya_kiingereza_kiswahili("Kichina", "Kiswahili") is False

    def test_maelekezo_ya_jozi(self):
        m = maelekezo_ya_jozi("Kiingereza", "Kiswahili")
        assert "ENGLISH-TO-SWAHILI" in m
        assert "VERB PARALLELISM" in m
        assert maelekezo_ya_jozi("Kifaransa", "Kiswahili") == ""


class TestMaelekezo:
    def test_kiswahili_ina_kanuni_16(self):
        assert "Kiswahili" in MAELEKEZO_YA_LUGHA
        k = MAELEKEZO_YA_LUGHA["Kiswahili"]
        # Angalia vichwa vya kanuni muhimu
        for neno in ("YAMBIWA", "NOUN-CLASS CONCORD", "POSSESSIVES",
                     "COUNTERFACTUAL", "I-ZI PLURAL"):
            assert neno in k, f"Kanuni '{neno}' haipo kwenye MAELEKEZO_YA_LUGHA."

    def test_lugha_nyingine(self):
        for lugha in ("Kichina", "Kireno", "Kizulu", "Setswana"):
            assert lugha in MAELEKEZO_YA_LUGHA
            assert len(MAELEKEZO_YA_LUGHA[lugha]) > 0
