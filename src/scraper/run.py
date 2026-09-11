# scraper/run.py
import asyncio
import json
import aiohttp

from src.scraper.discover import fetch_allpages
from src.scraper.fetch import fetch_page
from src.scraper.clean import clean_html


OUTPUT = "data/raw/pages.jsonl"


async def run():
    async with aiohttp.ClientSession(
        headers={"User-Agent": "GraphMind/1.0"}
    ) as session:

        cursor = None
        seen = set()

        with open(OUTPUT, "w") as f:
            while True:
                titles, cursor = await fetch_allpages(session, cursor)

                if not titles:
                    break

                for title in titles:
                    if title in seen:
                        continue
                    seen.add(title)

                    html = await fetch_page(session, title)
                    text = clean_html(html)

                    if not text:
                        continue

                    record = {
                        "title": title,
                        "url": f"https://wiki.metakgp.org/w/{title.replace(' ', '_')}",
                        "text": text,
                    }

                    f.write(json.dumps(record) + "\n")
                    print("scraped:", title)

                if not cursor:
                    break


if __name__ == "__main__":
    asyncio.run(run())
