# Uiverse: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `code` | `public_read` / `low` | `opencli uiverse code "<input>" --target "<html\|css\|react\|vue>" -f json`<br>Export Uiverse component code (HTML, CSS, React, or Vue) | `input` (str, required, positional); `target` (str, required, choices=html,css,react,vue) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
