Viraka kamili viko kwenye [MAREKEBISHO_APP_TAFSIRI.md](MAREKEBISHO_APP_TAFSIRI.md). Hapa ni kiini chake:

## 1. Kisanduku cha matokeo (kinachokosekana)

Kwenye tawi la `mtafsiri`, badilisha `onyesha_jibu(...)` na hii:

```python
        _h = hash(_t_mwisho["tafsiri"])
        if str_platform.session_state.get("tafsiri_hash") != _h:
            str_platform.session_state["tafsiri_hash"] = _h
            str_platform.session_state["tafsiri_namba"] = (
                str_platform.session_state.get("tafsiri_namba", 0) + 1
            )

        str_platform.markdown("#### \U0001F4C4 Matini Iliyotafsiriwa")
        matini_iliyotafsiriwa = str_platform.text_area(
            "Matini iliyotafsiriwa:",
            value=_t_mwisho["tafsiri"],
            height=220,
            key="tafsiri_matokeo_" + str(str_platform.session_state["tafsiri_namba"]),
            label_visibility="collapsed",
        )
        _c1, _c2 = str_platform.columns(2)
        with _c1:
            str_platform.download_button(
                "\u2B07\uFE0F Pakua matini (.txt)", matini_iliyotafsiriwa,
                file_name="tafsiri.txt", mime="text/plain",
                key="tafsiri_pakua_btn", use_container_width=True)
        with _c2:
            if str_platform.button(
                "\u21A9\uFE0F Rudisha kwenye kisanduku cha kuingiza",
                key="tafsiri_rudisha_btn", use_container_width=True):
                str_platform.session_state["tafsiri_rudisha_inasubiri"] = (
                    matini_iliyotafsiriwa[:MAX_CHARS])
                str_platform.rerun()
```

Na **juu kabisa** ya tawi la `mtafsiri` (kabla ya `col1, col2 = ...`):

```python
    if "tafsiri_rudisha_inasubiri" in str_platform.session_state:
        str_platform.session_state["trans_v14_clean_box"] = (
            str_platform.session_state.pop("tafsiri_rudisha_inasubiri"))
```

## 2. Mahali pa kuweka matini uliyo nayo tayari

Hii ndiyo sehemu inayokosekana kabisa — umeandika/umetafsiri mahali pengine, unataka kuikagua:

```python
    with str_platform.expander("\U0001F50D Nina matini tayari — ikague"):
        if "kagua_matini_inasubiri" in str_platform.session_state:
            str_platform.session_state["kagua_matini_box"] = (
                str_platform.session_state.pop("kagua_matini_inasubiri"))

        matini_ya_kukagua = str_platform.text_area(
            "Bandika matini yako hapa:", height=150,
            key="kagua_matini_box", max_chars=MAX_CHARS)

        if str_platform.button("Kagua matini hii", key="kagua_matini_btn"):
            if not matini_ya_kukagua.strip():
                str_platform.warning("Bandika matini kwanza.")
            else:
                with str_platform.spinner("Inakagua..."):
                    try:
                        _pk = sarufi_bridge.kagua_pamoja(
                            matini_ya_kukagua, piga_ai=_piga_ai,
                            piga_ai_kina=(_piga_ai_kina if _UTHIBITISHO_WA_PRO else None),
                            lugha=lugha_lengwa)
                    except Exception as e:
                        _pk = None
                        onyesha_hitilafu("kukagua matini", e)
                if _pk and _pk["issues"]:
                    str_platform.warning(f"Makosa {len(_pk['issues'])} yamepatikana.")
                    for _x in _pk["issues"]:
                        str_platform.checkbox(
                            f'{_ep_md(_x["original"])} \u2192 {_ep_md(_x["suggestion"])}',
                            value=True, key=f"km_{_x['id']}")
                    if str_platform.button("Tumia marekebisho", key="km_tumia"):
                        _chaguliwa = {_x["id"] for _x in _pk["issues"]
                                      if str_platform.session_state.get(f"km_{_x['id']}", True)}
                        str_platform.session_state["kagua_matini_inasubiri"] = (
                            mhariri.tumia_marekebisho(
                                matini_ya_kukagua, _pk["issues"], _chaguliwa)[:MAX_CHARS])
                        str_platform.rerun()
                elif _pk:
                    str_platform.success("Hakuna makosa yaliyopatikana. \u2705")
```

## Muhimu: kwa nini `session_state["..._inasubiri"]`

Streamlit hukataza kuandika kwenye key ya widget **iliyokwisha tengenezwa** kwenye run huo huo (`st.session_state.trans_v14_clean_box cannot be modified after the widget is instantiated`). Ndiyo maana matini huwekwa kwenye key ya "inasubiri", kisha kiitikio cha juu kinaihamisha **kabla** widget haijatengenezwa kwenye run inayofuata. Hii ni muhimu — bila hiyo utapata `StreamlitAPIException`.

## Kuhusu ukaguzi mara mbili

Ni wa makusudi, na unaweza kuuzima:

| Ukaguzi | Uko wapi | Kuzima |
|---|---|---|
| Kabla ya tafsiri | tiki "Kagua makosa... kabla ya kutafsiri" | ondoa tiki |
| Baada ya tafsiri | `SYSTEM_UKAGUZI` ndani ya API | `HATUA_MBILI=0` kwenye Render |

## Ujumbe wa commit

```
feat(tafsiri): kisanduku cha matokeo na ukaguzi wa matini iliyopo

- Badilisha onyesha_jibu (HTML ya kusoma pekee) na st.text_area inayoharirika
  yenye kitufe cha kupakua
- Ongeza "Rudisha kwenye kisanduku cha kuingiza" ili matokeo yaweze
  kutafsiriwa au kukaguliwa tena
- Ongeza expander "Nina matini tayari — ikague" kwa kuweka matini
  iliyotafsiriwa/iliyohaririwa mahali pengine
- Tumia key ya "inasubiri" kuepuka StreamlitAPIException ya widget
  iliyokwisha tengenezwa
```

Kama unataka, nipe `mhariri_pro_ui.py` na nitarekebisha tawi la mhariri vivyo hivyo — hilo ndilo linalobaki bila kisanduku cha matokeo.
