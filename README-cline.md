# Настройка roo-cline (OpenRouter / Groq)

Инструкции по подключению провайдера для расширения `rooveterinaryinc.roo-cline`.

1) Настройки в рабочем пространстве

- Файл: [.vscode/settings.json](.vscode/settings.json#L1-L10)
- По умолчанию настроено на OpenRouter:

```
"roo-cline.vsCodeLmModelSelector": { "vendor": "openrouter", "family": "gpt-4o-mini" }
```

2) Добавление API-ключа

- OpenRouter: экспортируйте в окружение или сохраните в безопасном месте (секреты VS Code):

```bash
export OPENROUTER_API_KEY="your_openrouter_key"
```

- Groq (если используете Groq):

```bash
export GROQ_API_KEY="your_groq_key"
```

3) Переключение провайдера

Откройте `.vscode/settings.json` и замените `vendor` на `groq` и укажите желаемую `family`, например:

```
"roo-cline.vsCodeLmModelSelector": { "vendor": "groq", "family": "groq-1" }
```

4) Перезапустите VS Code (или повторно загрузите окно), чтобы расширение подхватило изменения.

Если хотите, могу добавить поддержку сохранения ключа в рабочем пространстве (не рекомендуется в публичных репозиториях). Напишите, какой провайдер и модель предпочитаете.
