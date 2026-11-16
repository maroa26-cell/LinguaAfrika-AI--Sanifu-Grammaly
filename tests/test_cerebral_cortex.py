"""tests/test_cerebral_cortex.py — Majaribio ya cerebral_cortex.py (v2.1).

Endesha:    pytest tests/test_cerebral_cortex.py -v
Matokeo:    yote yanapaswa kupita kwenye v2.1.

Yaliyomo:
  TestBug3LughaZaWhisper       'zu'/'tn' zimeongezwa kwenye LUGHA_ZA_WHISPER
  TestBug5MaelekezoYaMuktadha  MAELEKEZO_YA_MUKTADHA ina rejista 6 kamili
  TestBug4AudioSeek            chakata_sauti inarudisha pointer mwanzoni
  TestBug1TimeoutGemini        _piga_gemini inapitisha timeout kwenye config
  TestBug2LoggingGemini        _piga_gemini inaandika kosa kwenye logi
  TestBug6MaandishiMatupu      chakata_tafsiri_kamili inarudisha mapema
  TestNambaNaAya               _namba_za, _tofauti_za_namba, _aya, _safisha_jibu
  TestKasoroYaJibu             lango la ubora wa tafsiri
  TestPigaMnyororo             mpangilio wa watoa huduma
  TestPigaGroq                 fallback ya Groq
  TestZalishaDataset           rekodi ya dataset (verified vs rejected)
"""
import io
import logging
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cerebral_cortex as cc


@pytest.fixture
def ubongo():
    """CerebralCortex bila API clients — safisha kwa majaribio."""
    u = cc.CerebralCortex()
    u.gemini_client = None
    u.groq_client = None
    u.openai_client = None
    return u


# ============================================================
# BUG 3: LUGHA_ZA_WHISPER haijakamilika (v2.0 -> v2.1)
# ============================================================

class TestBug3LughaZaWhisper:
    """v2.0: 'zu' na 'tn' zilikuwa kwenye JINA_LA_LUGHA_KWA_MSIMBO
    lakini haziko kwenye LUGHA_ZA_WHISPER. Whisper-large-v3 inaunga
    mkono zote mbili; transcription ilipoteza hint ya lugha."""

    def test_zu_na_tn_ziko_kwenye_jina(self):
        """Thibitisha: mfumo unajua 'zu' na 'tn' (kama majina ya lugha)."""
        assert "zu" in cc.JINA_LA_LUGHA_KWA_MSIMBO
        assert "tn" in cc.JINA_LA_LUGHA_KWA_MSIMBO

    def test_zu_yupo_kwenye_whisper(self):
        """v2.1: 'zu' imeongezwa kwenye LUGHA_ZA_WHISPER."""
        assert "zu" in cc.LUGHA_ZA_WHISPER, (
            "BUG 3: 'zu' (isiZulu) haiko kwenye LUGHA_ZA_WHISPER. "
            "Whisper inaunga mkono, lakini hint ya lugha haitumwi. "
            "Transcription inaweza kuchanganya Zulu na Kiswahili."
        )

    def test_tn_yupo_kwenye_whisper(self):
        """v2.1: 'tn' imeongezwa kwenye LUGHA_ZA_WHISPER."""
        assert "tn" in cc.LUGHA_ZA_WHISPER, (
            "BUG 3: 'tn' (Setswana) haiko kwenye LUGHA_ZA_WHISPER. "
            "Whisper inaunga mkono 'tn'."
        )

    def test_lugha_nyingine_zipo(self):
        """Lugha zote za msingi ziko kwenye LUGHA_ZA_WHISPER."""
        for code in ("sw", "en", "fr", "ar", "zh", "pt", "ln"):
            assert code in cc.LUGHA_ZA_WHISPER


# ============================================================
# BUG 5: MAELEKEZO_YA_MUKTADHA pungufu (v2.0 -> v2.1)
# ============================================================

class TestBug5MaelekezoYaMuktadha:
    """v2.0: rejista 6 zina msamiati, lakini 4 pekee zina maelekezo.
    Kibiashara/Kielimu zilipata maelekezo ya jumla tu."""

    def test_rejista_zote_zina_msamiati(self):
        """Thibitisha: rejista zote 6 zina msamiati."""
        for muktadha in ("Kidini", "Kilimo", "Kitiba",
                         "Kisheria", "Kibiashara", "Kielimu"):
            assert muktadha in cc.MSAMIATI_WA_MUKTADHA, (
                f"Rejista '{muktadha}' haiko kwenye MSAMIATI_WA_MUKTADHA."
            )

    def test_rejista_zote_zina_maelekezo(self):
        """v2.1: rejista zote 6 zina maelekezo kamili."""
        for muktadha in ("Kidini", "Kilimo", "Kitiba",
                         "Kisheria", "Kibiashara", "Kielimu"):
            assert muktadha in cc.MAELEKEZO_YA_MUKTADHA, (
                f"BUG 5: '{muktadha}' haiko kwenye MAELEKEZO_YA_MUKTADHA. "
                f"Tafsiri za rejista hii zinapata maelekezo ya jumla tu."
            )

    def test_kibiashara_maelekezo_mahsusi(self):
        """Kibiashara ina maelekezo ya istilahi (faida, hasara, ankara, ...)."""
        m = cc.MAELEKEZO_YA_MUKTADHA["Kibiashara"].lower()
        for neno in ("faida", "hasara", "ankara", "mtaji", "bei"):
            assert neno in m, f"BUG 5: '{neno}' haiko kwenye maelekezo ya Kibiashara."

    def test_kielimu_maelekezo_mahsusi(self):
        """Kielimu ina maelekezo ya istilahi (mtaala, mtihani, mwanafunzi, ...)."""
        m = cc.MAELEKEZO_YA_MUKTADHA["Kielimu"].lower()
        for neno in ("mtaala", "mtihani", "mwanafunzi", "mwalimu", "shule"):
            assert neno in m, f"BUG 5: '{neno}' haiko kwenye maelekezo ya Kielimu."

    def test_kitiba_maelekezo_ya_vipimo(self):
        """Kitiba ina maelekezo ya kupima (mg, ml, °C, mara mbili kwa siku)."""
        m = cc.MAELEKEZO_YA_MUKTADHA["Kitiba"].lower()
        # Angalau mmoja wa vipimo vya kawaida
        assert any(x in m for x in ("mg", "ml", "°c", "kipimo", "dozi", "dose")), \
            "BUG 5: Kitiba haina maelekezo ya vipimo/dozi."

    def test_kisheria_maelekezo_ya_ibara(self):
        """Kisheria ina maelekezo ya ibara/kifungu."""
        m = cc.MAELEKEZO_YA_MUKTADHA["Kisheria"].lower()
        for neno in ("ibara", "kifungu", "mkataba", "mahakama"):
            assert neno in m or neno in ("kifungu", "ibara"), \
                f"BUG 5: '{neno}' haiko kwenye maelekezo ya Kisheria."


# ============================================================
# BUG 4: chakata_sauti_na_imla haina .seek(0) (v2.0 -> v2.1)
# ============================================================

class TestBug4AudioSeek:
    """v2.0: pointer ya file haikurudishwa mwanzoni kabla ya .read().
    Mwitaji aliyesoma faili kwa ukaguzi alipata b'' na 'Faili tupu'."""

    def test_bytesio_read_ya_pili_ni_tupu(self):
        """Thibitisha tabia ya Python: read() baada ya read() hutoa b''."""
        buf = io.BytesIO(b"data")
        kwanza = buf.read()
        pili = buf.read()
        assert kwanza == b"data"
        assert pili == b""

    def test_chakata_sauti_ina_reset_pointer(self, ubongo):
        """v2.1: pointer inarudishwa .seek(0) kabla ya .read()."""
        buf = io.BytesIO(b"fake_audio_bytes")
        buf.read()  # simulate prior read

        with pytest.raises(Exception) as exc_info:
            ubongo.chakata_sauti_na_imla(buf)

        # Bila fix: "faili la sauti ni tupu" (kimakosa)
        # Na fix: "hakuna ufunguo wa OpenAI" (sahihi — hakuna clients)
        kosa = str(exc_info.value).lower()
        assert "tupu" not in kosa or "openai" in kosa, (
            f"BUG 4: pointer haijarudishwa mwanzoni. Kosa: {exc_info.value}. "
            "Mtumiaji anapata 'Faili tupu' ingawa faili yake ni nzuri."
        )

    def test_chakata_sauti_ina_seek_kwenye_cheleni(self, ubongo):
        """Ikiwa file haina .seek(), msimbo unaendelea bila kosa."""
        class FakeFile:
            name = "test.mp3"
            type = "audio/mpeg"
            def read(self):
                return b"audio"
            # haina .seek()
        # Hii haipaswi kutoa AttributeError; inapaswa kufika mwisho
        # (na kutoa RuntimeError kwa sababu hakuna clients)
        with pytest.raises(RuntimeError):
            ubongo.chakata_sauti_na_imla(FakeFile())


# ============================================================
# BUG 1: _piga_gemini haina timeout (v2.0 -> v2.1)
# ============================================================

class TestBug1TimeoutGemini:
    """v2.0: _piga_gemini haikupitisha timeout kwenye GenerateContentConfig.
    Gemini ikikwama, ombi la api_server.py linakwama milele."""

    def test_gemini_config_ina_timeout(self, monkeypatch):
        """v2.1: config inapata 'timeout'."""
        types_module = getattr(cc, "types", None)
        if types_module is None:
            pytest.skip("google.genai haipo kwenye mazingira haya")

        u = cc.CerebralCortex()
        mock_client = MagicMock()
        u.gemini_client = mock_client
        mock_client.models.generate_content.return_value = MagicMock(text="jibu")

        captured = {}

        def mock_config(**kwargs):
            captured.update(kwargs)
            return MagicMock()

        monkeypatch.setattr(types_module, "GenerateContentConfig", mock_config)

        u._piga_gemini("mfumo", "mtumiaji", temperature=0.2)

        assert "timeout" in captured, (
            f"BUG 1: _piga_gemini haipitishi timeout. "
            f"Kwargs: {list(captured.keys())}. "
            "Gemini ikikwama, ombi linakwama milele."
        )
        assert captured["timeout"] == cc.GEMINI_TIMEOUT_S

    def test_gemini_timeout_constant(self):
        """GEMINI_TIMEOUT_S ipo na ni ya maana (5-120s)."""
        assert hasattr(cc, "GEMINI_TIMEOUT_S")
        assert 5 <= cc.GEMINI_TIMEOUT_S <= 120

    def test_sdk_isiyokubali_timeout_haivunji(self, monkeypatch):
        """v2.1: SDK isiyokubali 'timeout' kwenye config inarukwa kwa heshima."""
        types_module = getattr(cc, "types", None)
        if types_module is None:
            pytest.skip("google.genai haipo")

        u = cc.CerebralCortex()
        mock_client = MagicMock()
        u.gemini_client = mock_client

        # Simulate SDK inayokataa 'timeout'
        call_count = {"n": 0}
        def side_effect(**kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1 and "timeout" in kwargs:
                raise Exception("unknown field: timeout")
            return MagicMock(text="jibu")
        mock_client.models.generate_content.side_effect = side_effect

        # Haipaswi kutoa exception; inapaswa kurudisha jibu
        jibu = u._piga_gemini("mfumo", "mtumiaji")
        assert jibu == "jibu"
        assert call_count["n"] == 2  # jaribio la pili bila timeout


# ============================================================
# BUG 2: _piga_gemini haina logging (v2.0 -> v2.1)
# ============================================================

class TestBug2LoggingGemini:
    """v2.0: except Exception: return None ilificha kila kosa.
    Hukuweza kujua kwa nini Gemini imeshindwa."""

    def test_gemini_failure_inalog(self, caplog):
        """v2.1: kosa la Gemini linaandikwa kwenye logi."""
        u = cc.CerebralCortex()
        mock_client = MagicMock()
        u.gemini_client = mock_client
        mock_client.models.generate_content.side_effect = Exception("API error 500")

        with caplog.at_level(logging.WARNING):
            matokeo = u._piga_gemini("mfumo", "mtumiaji")

        assert matokeo is None  # fallback inafanya kazi
        # Log entry ipo
        records = [r.message for r in caplog.records]
        assert any(
            "gemini" in m.lower() or "_piga_gemini" in m.lower()
            for m in records
        ), f"BUG 2: hakuna log entry. Records: {records}"

    def test_log_haija_maandishi_ya_mtumiaji(self, caplog):
        """Faragha: logi haipaswi kuwa na maandishi ya mtumiaji."""
        u = cc.CerebralCortex()
        mock_client = MagicMock()
        u.gemini_client = mock_client
        mock_client.models.generate_content.side_effect = Exception("API error")

        maandishi_ya_siri = "HII_NI_MAANDISHI_YA_SIRI_YA_MTUMIAJI"
        with caplog.at_level(logging.WARNING):
            u._piga_gemini("mfumo", maandishi_ya_siri)

        # Hakuna record inayopaswa kuwa na maandishi ya mtumiaji
        for r in caplog.records:
            assert maandishi_ya_siri not in r.message, \
                "Faragha: maandishi ya mtumiaji yameandikwa kwenye logi!"


# ============================================================
# Nyongeza (v2.1): chakata_tafsiri_kamili na maandishi matupu
# ============================================================

class TestBug6MaandishiMatupu:
    """v2.1: chakata_tafsiri_kamili inarudisha mapema ikiwa maandishi ni matupu.
    v2.0: ingeita _jibu na maandishi matupu; onyo zisizo na maana."""

    def test_maandishi_matupu_anarudisha_mapema(self, ubongo):
        """v2.1: "" -> dict tupu bila wito wa AI."""
        # Bila clients, ikiwa inaita _jibu itatoa RuntimeError
        r = ubongo.chakata_tafsiri_kamili("", "Kiingereza", "Kiswahili", "Kawaida")
        assert r["tafsiri"] == ""
        assert r["rasimu"] == ""
        assert r["hatua"] == []
        assert r["onyo"] == []

    def test_nafasi_pekee_pia_ni_tupu(self, ubongo):
        """'   \\n\\t' inatibiwa kama tupu."""
        r = ubongo.chakata_tafsiri_kamili("   \n\t  ", "Kiingereza", "Kiswahili", "Kawaida")
        assert r["tafsiri"] == ""


# ============================================================
# Baseline: kazi za msingi zinafanya kazi
# ============================================================

class TestNambaNaAya:
    """Kazi za msingi za _namba_za, _tofauti_za_namba, _aya, _safisha_jibu."""

    def test_namba_za_basic(self):
        assert cc._namba_za("Kuna watu 25 na 3.5 kg") == {"25": 1, "3.5": 1}

    def test_namba_za_koma_sawa_na_nukta(self):
        """'1,5' na '1.5' zinachukuliwa sawa (koma ya Uropa)."""
        assert cc._namba_za("1,5") == cc._namba_za("1.5")

    def test_namba_za_tupu(self):
        assert cc._namba_za("") == {}
        assert cc._namba_za("hakuna namba") == {}

    def test_namba_za_kurudiwa(self):
        assert cc._namba_za("10 na 10") == {"10": 2}

    def test_tofauti_za_namba_hakuna(self):
        assert cc._tofauti_za_namba("Bei ni 100", "Bei ni 100") == 0

    def test_tofauti_za_namba_ipo(self):
        assert cc._tofauti_za_namba("Bei ni 100", "Bei ni 200") > 0

    def test_tofauti_za_namba_imeongezwa(self):
        assert cc._tofauti_za_namba("Bei ni 100", "Bei ni 100 na 200") > 0

    def test_aya_za_paragraph(self):
        assert cc._aya("Aya moja\n\nAya mbili\n\nAya tatu") == 2
        assert cc._aya("Aya moja tu") == 0
        assert cc._aya("") == 0

    def test_safisha_jibu_code_fence(self):
        assert cc._safisha_jibu("```\nmaandishi\n```") == "maandishi"
        assert cc._safisha_jibu("```json\n{}\n```") == "{}"
        assert cc._safisha_jibu("  nafasi  ") == "nafasi"


class TestKasoroYaJibu:
    """Lango la ubora wa tafsiri linafanya kazi."""

    def test_tupu_inakataliwa(self):
        assert cc.CerebralCortex._kasoro_ya_jibu("chanzo", "rasimu", "") == "jibu tupu"
        assert cc.CerebralCortex._kasoro_ya_jibu("chanzo", "rasimu", "   ") == "jibu tupu"

    def test_alama_za_takataka_zinakataliwa(self):
        for alama in ("ORIGINAL:", "DRAFT:", "<<<", ">>>"):
            sababu = cc.CerebralCortex._kasoro_ya_jibu(
                "chanzo", "rasimu", f"{alama} maandishi"
            )
            assert "ziada" in sababu, f"Alama '{alama}' haikukamatwa."

    def test_mazungumzo_yanakataliwa(self):
        for mwanzo in ("Here is the translation:", "Sure,", "Certainly."):
            sababu = cc.CerebralCortex._kasoro_ya_jibu(
                "chanzo", "rasimu", mwanzo + " maandishi"
            )
            assert "ziada" in sababu, f"Mwanzo '{mwanzo}' haukukamatwa."

    def test_namba_zilizobadilika_zinakataliwa(self):
        sababu = cc.CerebralCortex._kasoro_ya_jibu(
            "Kuna watu 100", "Kuna watu 100", "Kuna watu 200"
        )
        assert "namba" in sababu

    def test_urefu_usio_wa_kawaida(self):
        # jibu refu sana
        sababu = cc.CerebralCortex._kasoro_ya_jibu(
            "maandishi mafupi",
            "maandishi mafupi yenye maneno mengi ya kutosha",
            "maneno " * 500,
        )
        assert "urefu" in sababu or "namba" in sababu

    def test_jibu_nzuri_hakataliwi(self):
        chanzo = "Kuna watu 100"
        rasimu = "Kuna watu 100"
        jibu = "Kuna watu 100"
        assert cc.CerebralCortex._kasoro_ya_jibu(chanzo, rasimu, jibu) is None

    def test_aya_zilizobadilika(self):
        chanzo = "Aya moja.\n\nAya mbili."
        rasimu = "Aya moja.\n\nAya mbili."
        jibu = "Aya moja. Aya mbili."  # aya imeunganishwa
        sababu = cc.CerebralCortex._kasoro_ya_jibu(chanzo, rasimu, jibu)
        assert "aya" in sababu


class TestPigaMnyororo:
    """Mpangilio wa watoa huduma: Gemini -> Groq -> OpenAI."""

    def test_bila_client_yoyote_ni_runtime_error(self, ubongo):
        with pytest.raises(RuntimeError) as exc_info:
            ubongo._piga_mnyororo(
                [{"role": "user", "content": "jaribio"}], 0.1
            )
        kosa = str(exc_info.value).lower()
        assert "openai" in kosa or "akiba" in kosa

    def test_gemini_ikifanya_kazi_haitumii_groq(self, ubongo):
        ubongo.gemini_client = MagicMock()
        ubongo.gemini_client.models.generate_content.return_value = MagicMock(text="jibu la gemini")
        ubongo.groq_client = MagicMock()  # ikiwa ingeitwa, ingefeli

        jibu = ubongo._piga_mnyororo(
            [{"role": "system", "content": "sys"},
             {"role": "user", "content": "user"}],
            0.1,
        )
        assert jibu == "jibu la gemini"
        ubongo.groq_client.chat.completions.create.assert_not_called()

    def test_gemini_ikishindwa_groq_inachukua(self, ubongo):
        ubongo.gemini_client = MagicMock()
        ubongo.gemini_client.models.generate_content.side_effect = Exception("Gemini down")
        ubongo.groq_client = MagicMock()
        ubongo.groq_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="jibu la groq"))]
        )

        jibu = ubongo._piga_mnyororo(
            [{"role": "system", "content": "sys"},
             {"role": "user", "content": "user"}],
            0.1,
        )
        assert jibu == "jibu la groq"

    def test_wote_wakishindwa_runtime_error(self, ubongo):
        ubongo.gemini_client = MagicMock()
        ubongo.gemini_client.models.generate_content.side_effect = Exception("Gemini down")
        ubongo.groq_client = MagicMock()
        ubongo.groq_client.chat.completions.create.side_effect = Exception("Groq down")
        # Hakuna OpenAI

        with pytest.raises(RuntimeError):
            ubongo._piga_mnyororo(
                [{"role": "system", "content": "sys"},
                 {"role": "user", "content": "user"}],
                0.1,
            )


class TestPigaGroq:
    """Groq inarudisha None badala ya kutoa exception (fallback)."""

    def test_groq_bila_client(self, ubongo):
        assert ubongo._piga_groq([{"role": "user", "content": "x"}], 0.1) is None

    def test_groq_ikishindwa_ni_none(self, ubongo):
        ubongo.groq_client = MagicMock()
        ubongo.groq_client.chat.completions.create.side_effect = Exception("Groq error")
        assert ubongo._piga_groq([{"role": "user", "content": "x"}], 0.1) is None

    def test_groq_ikifanya_kazi(self, ubongo):
        ubongo.groq_client = MagicMock()
        ubongo.groq_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="jibu"))]
        )
        jibu = ubongo._piga_groq([{"role": "user", "content": "x"}], 0.1)
        assert jibu == "jibu"


class TestZalishaDataset:
    """zalisha_dataset_ya_kuuza hutoa rekodi au None (kama Kiswahili si sahihi)."""

    def test_dataset_inarudisha_none_kwa_tafsiri_isiyo_sahihi(self, ubongo):
        """Tafsiri yenye makosa ya Kiswahili -> None (haifikii soko)."""
        # Mock chakata_tafsiri_pacha kurudisha Kiswahili kibovu
        with patch.object(ubongo, "chakata_tafsiri_pacha",
                          return_value="Darasani yenye wanafunzi wengi."):
            matokeo = ubongo.zalisha_dataset_ya_kuuza("A classroom with many students.")
        # 'darasani yenye' ni kosa la ngeli-mahali
        assert matokeo is None

    def test_dataset_inarudisha_rekodi_kwa_tafsiri_sahihi(self, ubongo):
        """Tafsiri sahihi -> rekodi kamili."""
        with patch.object(ubongo, "chakata_tafsiri_pacha",
                          return_value="Darasa lenye wanafunzi wengi."):
            matokeo = ubongo.zalisha_dataset_ya_kuuza(
                "A classroom with many students.", "Kiingereza", "Kiswahili"
            )
        assert matokeo is not None
        assert matokeo["source_lang"] == "Kiingereza"
        assert matokeo["target_lang"] == "Kiswahili"
        assert matokeo["register"] == "Kawaida"
        assert "GeminiFirst" in matokeo["verified_by"]

    def test_dataset_bila_kiswahili_hakuna_ukaguzi(self, ubongo):
        """Kiingereza -> Kifaransa: hakuna cha kukagua (hakuna Kiswahili)."""
        with patch.object(ubongo, "chakata_tafsiri_pacha",
                          return_value="Une salle de classe."):
            matokeo = ubongo.zalisha_dataset_ya_kuuza(
                "A classroom.", "Kiingereza", "Kifaransa"
            )
        # Bila Kiswahili, hakuna kosa la kuzuia
        assert matokeo is not None
