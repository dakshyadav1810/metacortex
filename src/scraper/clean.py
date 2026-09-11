# scraper/clean.py
from bs4 import BeautifulSoup


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#mw-content-text")
    if not content:
        return None

    for tag in content.select("table, sup, .toc"):
        tag.decompose()

    text = "\n".join(
        p.get_text(" ", strip=True)
        for p in content.find_all(["p", "li"])
        if len(p.get_text(strip=True)) > 40
    )

    return text.strip()
