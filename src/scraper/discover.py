# scraper/discover.py
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

BASE = "https://wiki.metakgp.org"


async def fetch_allpages(session, cursor=None):
    params = {"title": "Special:AllPages"}
    if cursor:
        params["from"] = cursor

    async with session.get(BASE + "/index.php", params=params) as res:
        html = await res.text()

    soup = BeautifulSoup(html, "html.parser")

    titles = [
        a.text.strip()
        for a in soup.select(".mw-allpages-body a")
        if not a.get("class") or "mw-redirect" not in a.get("class", [])
    ]

    next_link = soup.select_one(".mw-allpages-nav a")
    next_cursor = None

    if next_link:
        qs = parse_qs(urlparse(next_link["href"]).query)
        next_cursor = qs.get("from", [None])[0]

    return titles, next_cursor
