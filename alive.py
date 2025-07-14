# alive.py
import aiohttp
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

async def is_url_alive(url: str, retries: int = 3, delay: float = 2) -> bool:
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        logging.info(f"[keep-alive] URL {url} responded 200")
                        return True
        except Exception as e:
            logging.warning(f"[keep-alive] Try {attempt+1} failed: {e}")
        await asyncio.sleep(delay)
    return False

async def keep_alive_forever(url: str = "https://api.telegram.org", interval: float = 600):
    while True:
        await is_url_alive(url)
        await asyncio.sleep(interval)
