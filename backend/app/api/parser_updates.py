import requests
from bs4 import BeautifulSoup
from app.utils.embeddings import embed_text
from app.utils.storage import supabase_upsert_doc

SOURCES = [
    {"url": "https://www.nalog.ru/", "name": "nalog.ru"},
    {"url": "https://publication.pravo.gov.ru/", "name": "pravo.gov.ru"},
]


def fetch_text(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    return "\n\n".join(paragraphs)


async def trigger_update():
    for s in SOURCES:
        try:
            text = fetch_text(s["url"])
        except Exception:
            continue
        # chunking
        chunk_size = 2000
        for i in range(0, len(text), chunk_size):
            c = text[i : i + chunk_size]
            vec = embed_text(c)
            supabase_upsert_doc({"text": c, "source": s["name"], "url": s["url"]}, vec)
    return {"status": "ok"}
