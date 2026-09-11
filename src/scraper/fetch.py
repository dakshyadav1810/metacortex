# scraper/fetch.py
import aiohttp

BASE = "https://wiki.metakgp.org"


async def fetch_page(session, title):
    url = f"{BASE}/w/{title.replace(' ', '_')}"
    async with session.get(url) as res:
        return await res.text()
