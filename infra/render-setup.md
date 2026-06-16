# Развёртывание на Render.com — быстрое руководство

1) Подключение репозитория
- Войдите в https://render.com
- Создайте новый Web Service → Connect a repository → выберите ваш репозиторий на GitHub.
- В `Root` укажите `/` (репозиторий корневой), Branch — `main`.

2) Build & Start
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3) Переменные окружения (Environment > Environment Variables)
Добавьте следующие ключи (значения должны быть заполнены вами):
- `OPENROUTER_API_KEY` — ключ OpenRouter (зарегистрируйтесь на openrouter.ai)
- `OPENROUTER_MODEL` — (рекомендуется `gpt-4o-mini`)
- `OPENROUTER_EMBED_MODEL` — (рекомендуется `text-embedding-3-small`)
- `OPENROUTER_CHAT_URL` — (обычно `https://api.openrouter.ai/v1/chat/completions`)
- `OPENROUTER_EMBED_URL` — (обычно `https://api.openrouter.ai/v1/embeddings`)
- `SUPABASE_URL` — URL проекта Supabase
- `SUPABASE_KEY` — service_role или anon key (рекомендуется service role для апдейтов)
- `ADMIN_SECRET` — произвольная секретная строка для триггера обновлений
- `RENDER_ADMIN_URL` — полный URL до endpoint'а обновления знаний (например `https://<your>.onrender.com/api/admin/update-knowledge`)
- `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` — опционально для уведомлений

Важно: не коммитьте секреты в репозиторий. Используйте UI Render или GitHub Secrets.

4) GitHub Actions и автоматический апдейт
- Для автоматического еженедельного обновления знаний добавьте секреты в GitHub: `ADMIN_SECRET` и `RENDER_ADMIN_URL`.
- В репо уже есть workflow `.github/workflows/update_knowledge.yml`, он использует эти секреты и вызывает ваш endpoint.

5) Cron / периодичность
- Рекомендация по частоте: `weekly` (еженедельно) для источников НК РФ и официальных публикаций.

6) Модель и бюджет
- Рекомендуемые модели:
  - `OPENROUTER_MODEL=gpt-4o-mini` — основной баланс качества/цены
  - `OPENROUTER_MODEL=gpt-4o` — для критичных случаев (ресурсоёмко)
  - `OPENROUTER_EMBED_MODEL=text-embedding-3-small` — эмбеддинги
- Для экономии: кэшируйте ответы и используйте локальные расчёты в модуле `tax_calc`.
