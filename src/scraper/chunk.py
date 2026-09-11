from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json


def parse_html_and_chunk(html_content, url, title,
                         chunk_size=500, chunk_overlap=50):

    soup = BeautifulSoup(html_content, "html.parser")

    # Restrict to article content only
    content = soup.select_one("#mw-content-text")
    if not content:
        return []

    # Remove noise
    for tag in content.select("table, sup, .toc, script, style"):
        tag.decompose()

    text = content.get_text(separator="\n", strip=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    chunked_data = []
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "chunk_id": f"{title}#{i}",
            "title": title,
            "url": url,
            "text": chunk
        })

    return chunked_data
