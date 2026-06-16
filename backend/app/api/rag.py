import os, requests
from app.utils.embeddings import embed_text
from app.utils.storage import supabase_search

OPENROUTER_URL = os.getenv("OPENROUTER_CHAT_URL", "https://api.openrouter.ai/v1/chat/completions")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")


async def answer_query(query: str, user_id: str | None = None):
    q_vec = embed_text(query)
    docs = supabase_search(q_vec, top_k=3)
    context = "\n\n".join([f"Источник: {d.get('source')}\n{d.get('text')}" for d in docs])
    system_prompt = (
        "Вы — сертифицированный бухгалтер РФ. Отвечайте кратко, точно и ссылайтесь на нормативные акты. "
        "Всегда добавляйте дисклеймер: это не является юридической консультацией."
    )
    user_prompt = f"Вопрос: {query}\n\nКонтекст:\n{context}\n\nОтвет:"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    body = {
        "model": os.getenv("OPENROUTER_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        "temperature": 0.0,
    }
    if not OPENROUTER_KEY:
        return {"error": "OpenRouter API key not configured"}
    r = requests.post(OPENROUTER_URL, json=body, headers=headers, timeout=30)
    r.raise_for_status()
    ans = r.json()
    text = ans.get("choices", [])[0].get("message", {}).get("content", "")
    return {"answer": text, "sources": docs}
