# Boss: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli boss detail "<security-id>" -f json`<br>BOSS直聘查看职位详情 | `security-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
