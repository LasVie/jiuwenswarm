# Notebooklm: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-source` | `reversible_remote_write` / `high` | `opencli notebooklm add-source "<notebook>" [--url "<url>"] [--content "<content>"] [--file "<file>"] [--title "<title>"] [--mime-type "<mime-type>"] [--execute <true\|false>] -f json`<br>Add a URL, text, or local file source to an existing NotebookLM notebook | `notebook` (str, required, positional); `url` (str, optional); `content` (str, optional); `file` (str, optional); `title` (str, optional); `mime-type` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `write-note` | `reversible_remote_write` / `high` | `opencli notebooklm write-note "<notebook>" --title "<title>" --content "<content>" [--execute <true\|false>] -f json`<br>Create a Studio note in an existing NotebookLM notebook with the given title and Markdown content | `notebook` (str, required, positional); `title` (str, required); `content` (str, required); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
