import os, requests

OPENROUTER_EMBED_URL = os.getenv("OPENROUTER_EMBED_URL", "https://api.openrouter.ai/v1/embeddings")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")


def embed_text(text: str):
    if OPENROUTER_KEY:
        resp = requests.post(
            OPENROUTER_EMBED_URL,
            json={"model": os.getenv("OPENROUTER_EMBED_MODEL", "text-embedding-3-small"), "input": text},
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["data"][0]["embedding"]
    # fallback to sentence-transformers local model
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("intfloat/multilingual-e5-small")
        emb = model.encode([text])[0]
        return emb.tolist()
    except Exception:
        raise RuntimeError("No embedding provider available")
