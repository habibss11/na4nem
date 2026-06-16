import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
sb = None
if SUPABASE_URL and SUPABASE_KEY:
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)


def supabase_upsert_doc(meta: dict, vector: list):
    if not sb:
        raise RuntimeError("Supabase not configured")
    table = sb.table("documents")
    payload = {"text": meta.get("text"), "source": meta.get("source"), "url": meta.get("url"), "embedding": vector}
    table.upsert(payload).execute()


def supabase_search(vector: list, top_k: int = 3):
    if not sb:
        return []
    # assumes a SQL function match_documents(query_embedding, match_count) available
    res = sb.rpc("match_documents", {"query_embedding": vector, "match_count": top_k}).execute()
    return res.data or []
