# Youdao: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `note` | `public_read` / `low` | `opencli youdao note "<url>" -f json`<br>Read a public shared Youdao Note | `url` (str, required, positional) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
