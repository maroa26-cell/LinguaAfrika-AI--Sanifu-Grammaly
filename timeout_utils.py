"""
timeout_utils.py — Kikomo cha muda kwa miito ya AI inayozuia (blocking) na async.

Kwa nini faili hii ipo:
- SDK za AI (google-genai, groq, openai) zinaweza kukwama kwa muda mrefu
  (DNS, TCP alive bila data, SDK timeout ya 600s kwa default).
- Bila kikomo cha muda, thread ya mtumiaji (Streamlit) au worker wa seva
  (api_server) inangoja bila mwisho.
- Faili hii inatoa kikomo kimoja, kinachoweza kutumika kila mahali.

Matumizi ya blocking (mfano sanifu_editor, cerebral_cortex):

    from timeout_utils import na_muda, TimeoutAI

    piga_ai_na_muda = na_muda(timeout=25.0)(piga_ai)
    try:
        jibu = piga_ai_na_muda(mfumo, maandishi)
    except TimeoutAI:
        # mtoa huduma amechelewa; jaribu anayefuata
        ...

Matumizi ya async (mfano FastAPI):

    from timeout_utils import na_muda_async, TimeoutAI

    try:
        jibu = await na_muda_async(piga_ai, mfumo, maandishi, timeout=25.0)
    except TimeoutAI:
        return JSONResponse(status_code=504, content={"kosa": "AI_IMECHELEWA"})

Kumbuka: kwa blocking, thread iliyoachwa na timeout INAENDELEA nyuma hadi
SDK yake itakapomaliza. Executor ina max_workers=8; ikiwa unahitaji zaidi,
badilisha MAX_WORKERS chini.
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import logging
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


# Executor mmoja wa module-level: threads zilizoachwa na timeout zinaendelea
# nyuma hadi SDK yake itakapomaliza. Hazizuii mwitaji (caller).
MAX_WORKERS = 8
_EXECUTOR = concurrent.futures.ThreadPoolExecutor(
    max_workers=MAX_WORKERS, thread_name_prefix="ai-timeout"
)


class TimeoutAI(RuntimeError):
    """AI haikujibu ndani ya muda uliotolewa.

    Ni tofauti na RuntimeError ya jumla ili mwitaji (caller) aweze kuamua
    kujaribu mtoa huduma anayefuata au kurudisha kosa la 504.
    """


def na_muda(timeout: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator: hufunga kitendakazi cha blocking kwa kikomo cha muda (sekunde).

    Mfano:
        piga_ai_25s = na_muda(25.0)(piga_ai)
        # au
        @na_muda(25.0)
        def piga_ai(...): ...

    Hutoa TimeoutAI ikiwa kitendakazi hakikukamilika ndani ya `timeout`.
    Hitilafu nyingine yoyote (Exception) inapitishwa juu kama ilivyo.
    """
    if timeout <= 0:
        raise ValueError("timeout lazima iwe > 0")

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fut = _EXECUTOR.submit(fn, *args, **kwargs)
            try:
                return fut.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                logger.warning(
                    "%s haikujibu ndani ya sekunde %.1f",
                    getattr(fn, "__name__", "kitendakazi"), timeout,
                )
                raise TimeoutAI(
                    f"{getattr(fn, '__name__', 'kitendakazi')} haikujibu ndani ya sekunde {timeout:.1f}"
                ) from None
        return wrapper
    return decorator


async def na_muda_async(fn: Callable[..., Any], *args: Any, timeout: float,
                        **kwargs: Any) -> Any:
    """Async wrapper: hukimbiza kitendakazi cha blocking kwenye thread na kikomo cha muda.

    Inatumia asyncio.to_thread + asyncio.wait_for, kwa hiyo haizui event loop
    ya FastAPI/uvicorn. Hutoa TimeoutAI ikiwa `timeout` imepita.

    Mfano:
        try:
            jibu = await na_muda_async(piga_ai, mfumo, maandishi, timeout=25.0)
        except TimeoutAI:
            return JSONResponse(status_code=504, content={"kosa": "AI_IMECHELEWA"})
    """
    if timeout <= 0:
        raise ValueError("timeout lazima iwe > 0")
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(fn, *args, **kwargs), timeout=timeout
        )
    except asyncio.TimeoutError:
        logger.warning(
            "%s haikujibu ndani ya sekunde %.1f (async)",
            getattr(fn, "__name__", "kitendakazi"), timeout,
        )
        raise TimeoutAI(
            f"{getattr(fn, '__name__', 'kitendakazi')} haikujibu ndani ya sekunde {timeout:.1f}"
        ) from None


def shutdown_executor(wait: bool = False) -> None:
    """Funga executor (kwa tests au wakati wa kuzima app).

    Kwa kawaida huitwa mara moja kwenye mwisho wa maisha ya app (atexit au
    handler ya SIGTERM). Haifai kuitwa katikati ya maombi yanayoendelea.
    """
    _EXECUTOR.shutdown(wait=wait)


# ============================================================
# Majaribio ya haraka
# ============================================================
if __name__ == "__main__":
    import time

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    # 1. Kazi fupi inapita
    @na_muda(2.0)
    def kazi_fupi():
        time.sleep(0.1)
        return "ok"

    assert kazi_fupi() == "ok"
    print("✓ kazi_fupi imepita")

    # 2. Kazi ndefu inatoa TimeoutAI
    @na_muda(0.3)
    def kazi_ndefu():
        time.sleep(2.0)
        return "haipaswi kufika hapa"

    try:
        kazi_ndefu()
        print("✗ kazi_ndefu haikutoa TimeoutAI")
    except TimeoutAI as e:
        print(f"✓ kazi_ndefu imetoa TimeoutAI: {e}")

    # 3. Hitilafu nyingine inapitishwa
    @na_muda(2.0)
    def kazi_yenye_kosa():
        raise ValueError("kosa la kweli")

    try:
        kazi_yenye_kosa()
    except ValueError as e:
        print(f"✓ kosa la kweli limepitishwa: {e}")

    # 4. Async
    async def kazi_async():
        time.sleep(0.1)
        return "async-ok"

    async def jaribio_async():
        jibu = await na_muda_async(kazi_async, timeout=2.0)
        print(f"✓ na_muda_async imepita: {jibu}")

        try:
            await na_muda_async(kazi_ndefu.__wrapped__, timeout=0.2)
        except TimeoutAI as e:
            print(f"✓ na_muda_async imetoa TimeoutAI: {e}")

    asyncio.run(jaribio_async())
    shutdown_executor(wait=True)
    print("✓ Majaribio yote yamepita")
