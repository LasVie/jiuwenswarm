# Notebooklm: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `generate-audio` | `quota_consumption` / `high` | `opencli notebooklm generate-audio "<notebook>" [--execute <true\|false>] -f json`<br>Trigger an Audio Overview (Deep Dive podcast) generation for a NotebookLM notebook, using all of its sources | `notebook` (str, required, positional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `generate-slides` | `quota_consumption` / `high` | `opencli notebooklm generate-slides "<notebook>" [--length "<length>"] [--language "<language>"] [--execute <true\|false>] -f json`<br>Trigger a Slide Deck (AI presentation) generation for a NotebookLM notebook, using all of its sources | `notebook` (str, required, positional); `length` (str, optional); `language` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
