# Facebook: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile` | `public_read` / `low` | `opencli facebook profile "<username>" -f json`<br>Get Facebook user/page profile info | `username` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
