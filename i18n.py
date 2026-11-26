"""
i18n.py - Kibadilisha lugha cha mfumo (interface language switcher)
Lingual Africa Sanifu

Matumizi katika app.py:
    from i18n import language_selector, t
    language_selector()          # weka MARA MOJA, juu ya sidebar
    st.title(t("enter_text"))
"""
import streamlit as st

DEFAULT_LANG = "sw"

# Lugha 12 za mfumo (jina kwa lugha yake yenyewe)
LANGUAGES = {
    "sw": "Kiswahili",
    "en": "English",
    "fr": "Français",
    "ar": "العربية",
    "zh": "中文",
    "pt": "Português",
    "zu": "isiZulu",
    "tn": "Setswana",
    "rw": "Kinyarwanda",
    "lg": "Luganda",
    "ln": "Lingála",
    "ny": "Chichewa",
}

RTL_LANGS = {"ar"}  # lugha zinazoandikwa kulia kwenda kushoto

# ---------------------------------------------------------------------------
# MAANDISHI YA MFUMO. Ongeza ufunguo mpya (key) kwa lugha ZOTE 12.
# Ukikosa tafsiri, mfumo hutumia English kisha Kiswahili.
# ---------------------------------------------------------------------------
_STR = {
    "sw": {
        "ui_language": "Lugha ya mfumo",
        "choose_service": "Chagua huduma",
        "svc_mhariri": "Mhariri",
        "svc_mtafsiri": "Mtafsiri",
        "svc_kamusi": "Kamusi",
        "svc_sauti": "Sauti (Kuamrisha)",
        "enter_text": "Andika au bandika maandishi yako",
        "source_language": "Lugha ya chanzo",
        "target_language": "Lugha lengwa",
        "btn_edit": "Hariri",
        "btn_translate": "Tafsiri",
        "btn_clear": "Futa",
        "result": "Matokeo",
        "quality_score": "Alama ya ubora",
        "processing": "Inachakata...",
        "empty_warning": "Tafadhali weka maandishi kwanza.",
        "search_word": "Tafuta neno",
        "pay_now": "Lipa sasa",
    },
    "en": {
        "ui_language": "Interface language",
        "choose_service": "Choose a service",
        "svc_mhariri": "Editor",
        "svc_mtafsiri": "Translator",
        "svc_kamusi": "Dictionary",
        "svc_sauti": "Voice (Dictation)",
        "enter_text": "Type or paste your text",
        "source_language": "Source language",
        "target_language": "Target language",
        "btn_edit": "Edit",
        "btn_translate": "Translate",
        "btn_clear": "Clear",
        "result": "Result",
        "quality_score": "Quality score",
        "processing": "Processing...",
        "empty_warning": "Please enter some text first.",
        "search_word": "Search a word",
        "pay_now": "Pay now",
    },
    "fr": {
        "ui_language": "Langue de l'interface",
        "choose_service": "Choisir un service",
        "svc_mhariri": "Éditeur",
        "svc_mtafsiri": "Traducteur",
        "svc_kamusi": "Dictionnaire",
        "svc_sauti": "Voix (dictée)",
        "enter_text": "Saisissez ou collez votre texte",
        "source_language": "Langue source",
        "target_language": "Langue cible",
        "btn_edit": "Corriger",
        "btn_translate": "Traduire",
        "btn_clear": "Effacer",
        "result": "Résultat",
        "quality_score": "Score de qualité",
        "processing": "Traitement en cours...",
        "empty_warning": "Veuillez d'abord saisir du texte.",
        "search_word": "Rechercher un mot",
        "pay_now": "Payer maintenant",
    },
    "ar": {
        "ui_language": "لغة الواجهة",
        "choose_service": "اختر الخدمة",
        "svc_mhariri": "المحرر",
        "svc_mtafsiri": "المترجم",
        "svc_kamusi": "القاموس",
        "svc_sauti": "الصوت (الإملاء)",
        "enter_text": "اكتب نصك أو الصقه",
        "source_language": "لغة المصدر",
        "target_language": "اللغة الهدف",
        "btn_edit": "تحرير",
        "btn_translate": "ترجمة",
        "btn_clear": "مسح",
        "result": "النتيجة",
        "quality_score": "درجة الجودة",
        "processing": "جارٍ المعالجة...",
        "empty_warning": "يرجى إدخال نص أولاً.",
        "search_word": "ابحث عن كلمة",
        "pay_now": "ادفع الآن",
    },
    "zh": {
        "ui_language": "界面语言",
        "choose_service": "选择服务",
        "svc_mhariri": "编辑器",
        "svc_mtafsiri": "翻译器",
        "svc_kamusi": "词典",
        "svc_sauti": "语音（听写）",
        "enter_text": "输入或粘贴您的文本",
        "source_language": "源语言",
        "target_language": "目标语言",
        "btn_edit": "编辑",
        "btn_translate": "翻译",
        "btn_clear": "清除",
        "result": "结果",
        "quality_score": "质量评分",
        "processing": "处理中...",
        "empty_warning": "请先输入文本。",
        "search_word": "搜索单词",
        "pay_now": "立即支付",
    },
    "pt": {
        "ui_language": "Idioma da interface",
        "choose_service": "Escolha o serviço",
        "svc_mhariri": "Editor",
        "svc_mtafsiri": "Tradutor",
        "svc_kamusi": "Dicionário",
        "svc_sauti": "Voz (ditado)",
        "enter_text": "Digite ou cole o seu texto",
        "source_language": "Idioma de origem",
        "target_language": "Idioma de destino",
        "btn_edit": "Editar",
        "btn_translate": "Traduzir",
        "btn_clear": "Limpar",
        "result": "Resultado",
        "quality_score": "Pontuação de qualidade",
        "processing": "A processar...",
        "empty_warning": "Por favor, insira um texto primeiro.",
        "search_word": "Pesquisar palavra",
        "pay_now": "Pagar agora",
    },
    "zu": {
        "ui_language": "Ulimi lohlelo",
        "choose_service": "Khetha isevisi",
        "svc_mhariri": "Umhleli",
        "svc_mtafsiri": "Umhumushi",
        "svc_kamusi": "Isichazamazwi",
        "svc_sauti": "Izwi (Ukubhala ngezwi)",
        "enter_text": "Bhala noma unamathisele umbhalo wakho",
        "source_language": "Ulimi oluyisisekelo",
        "target_language": "Ulimi oluqondiwe",
        "btn_edit": "Hlela",
        "btn_translate": "Humusha",
        "btn_clear": "Sula",
        "result": "Umphumela",
        "quality_score": "Isikolo sekhwalithi",
        "processing": "Iyacubungula...",
        "empty_warning": "Sicela ufake umbhalo kuqala.",
        "search_word": "Sesha igama",
        "pay_now": "Khokha manje",
    },
    "tn": {
        "ui_language": "Puo ya porogramo",
        "choose_service": "Tlhopha tirelo",
        "svc_mhariri": "Edita",
        "svc_mtafsiri": "Mofetoledi",
        "svc_kamusi": "Pukuntsu",
        "svc_sauti": "Lentswe (Go kwala ka lentswe)",
        "enter_text": "Kwala kgotsa kopolola mokwalo wa gago",
        "source_language": "Puo ya mothale",
        "target_language": "Puo e e batlwang",
        "btn_edit": "Baakanya",
        "btn_translate": "Fetolela",
        "btn_clear": "Phimola",
        "result": "Diphelelo",
        "quality_score": "Maduo a boleng",
        "processing": "Go a dira...",
        "empty_warning": "Tsweetswee tsenya mokwalo pele.",
        "search_word": "Batla lefoko",
        "pay_now": "Duela jaanong",
    },
    "rw": {
        "ui_language": "Ururimi rw'imikoreshereze",
        "choose_service": "Hitamo serivisi",
        "svc_mhariri": "Ikosora",
        "svc_mtafsiri": "Umusemuzi",
        "svc_kamusi": "Inkoranyamagambo",
        "svc_sauti": "Ijwi (Kwandika uvuga)",
        "enter_text": "Andika cyangwa ushyiremo inyandiko yawe",
        "source_language": "Ururimi rw'inkomoko",
        "target_language": "Ururimi rugenewe",
        "btn_edit": "Kosora",
        "btn_translate": "Semura",
        "btn_clear": "Siba",
        "result": "Igisubizo",
        "quality_score": "Amanota y'ubwiza",
        "processing": "Biri gukorwa...",
        "empty_warning": "Nyamuneka banza ushyiremo inyandiko.",
        "search_word": "Shakisha ijambo",
        "pay_now": "Ishyura ubu",
    },
    "lg": {
        "ui_language": "Olulimi lw'enkola",
        "choose_service": "Londa empeereza",
        "svc_mhariri": "Omulongoosa",
        "svc_mtafsiri": "Omuvvuunuzi",
        "svc_kamusi": "Edikisinaale",
        "svc_sauti": "Eddoboozi",
        "enter_text": "Wandiika oba teeka ekiwandiiko kyo wano",
        "source_language": "Olulimi olusookerwako",
        "target_language": "Olulimi olugenderwa",
        "btn_edit": "Longoosa",
        "btn_translate": "Vvuunula",
        "btn_clear": "Sangula",
        "result": "Ekivuddemu",
        "quality_score": "Obubonero bw'omutindo",
        "processing": "Kikolebwa...",
        "empty_warning": "Nsaba osooke kuwandiika ekiwandiiko.",
        "search_word": "Noonya ekigambo",
        "pay_now": "Wa kati",
    },
    "ln": {
        "ui_language": "Lokota ya sistɛmɛ",
        "choose_service": "Poná servisi",
        "svc_mhariri": "Mobongisi",
        "svc_mtafsiri": "Mobongoli",
        "svc_kamusi": "Diksionɛrɛ",
        "svc_sauti": "Mongongo (Kokoma na mongongo)",
        "enter_text": "Koma to tya makomi na yo",
        "source_language": "Lokota ya ebandeli",
        "target_language": "Lokota ya kokóma",
        "btn_edit": "Bongisa",
        "btn_translate": "Bongola",
        "btn_clear": "Pàngusa",
        "result": "Eyano",
        "quality_score": "Nota ya kalite",
        "processing": "Ezali kosala...",
        "empty_warning": "Tɔbela, koma makomi liboso.",
        "search_word": "Luka liloba",
        "pay_now": "Futa sikoyo",
    },
    "ny": {
        "ui_language": "Chilankhulo cha pulogalamu",
        "choose_service": "Sankhani ntchito",
        "svc_mhariri": "Mkonzi",
        "svc_mtafsiri": "Womasulira",
        "svc_kamusi": "Dikishonale",
        "svc_sauti": "Mawu (Kulemba polankhula)",
        "enter_text": "Lembani kapena ikani zolemba zanu",
        "source_language": "Chilankhulo choyambira",
        "target_language": "Chilankhulo chofunidwa",
        "btn_edit": "Konza",
        "btn_translate": "Masulira",
        "btn_clear": "Fufuta",
        "result": "Zotsatira",
        "quality_score": "Mulingo wa khalidwe",
        "processing": "Ikukonza...",
        "empty_warning": "Chonde lowetsani zolemba choyamba.",
        "search_word": "Fufuzani liwu",
        "pay_now": "Lipirani tsopano",
    },
}


# ---------------------------------------------------------------------------
# Msingi wa utendaji
# ---------------------------------------------------------------------------
def _init_lang() -> None:
    """Weka lugha ya kuanzia: kutoka kwenye URL (?lang=fr) au Kiswahili."""
    if "ui_lang" not in st.session_state:
        try:
            q = st.query_params.get("lang")
        except Exception:
            q = None
        st.session_state["ui_lang"] = q if q in LANGUAGES else DEFAULT_LANG


def current_lang() -> str:
    _init_lang()
    return st.session_state["ui_lang"]


def t(key: str, **kwargs) -> str:
    """Rudisha maandishi ya `key` kwa lugha iliyochaguliwa."""
    lang = current_lang()
    text = (
        _STR.get(lang, {}).get(key)
        or _STR["en"].get(key)
        or _STR["sw"].get(key)
        or key
    )
    return text.format(**kwargs) if kwargs else text


def _on_change() -> None:
    # Hifadhi lugha kwenye URL ili isipotee ukirefresh ukurasa
    try:
        st.query_params["lang"] = st.session_state["ui_lang"]
    except Exception:
        pass


def _apply_direction(lang: str) -> None:
    """Arabic: geuza mpangilio kuwa kulia-kwenda-kushoto (CSS ndogo tu)."""
    if lang in RTL_LANGS:
        st.markdown(
            "<style>"
            ".stApp{direction:rtl;}"
            "section[data-testid='stSidebar']{direction:rtl;}"
            "</style>",
            unsafe_allow_html=True,
        )


def language_selector() -> str:
    """Kitufe cha kuchagua lugha kwenye sidebar. Rudisha code ya lugha (mf. 'sw')."""
    _init_lang()
    st.sidebar.selectbox(
        "🌐 Language · Lugha · 语言 · لغة",  # lebo ya lugha nyingi ili kila mtu aione
        options=list(LANGUAGES.keys()),
        format_func=lambda code: LANGUAGES[code],
        key="ui_lang",
        on_change=_on_change,
    )
    lang = st.session_state["ui_lang"]
    _apply_direction(lang)
    return lang
