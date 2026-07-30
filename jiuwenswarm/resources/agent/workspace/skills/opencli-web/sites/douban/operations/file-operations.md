# Douban: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli douban download "<id>" [--type "<type>"] [--limit <limit>] [--photo-id "<photo-id>"] [--output "<output>"] -f json`<br>下载电影海报/剧照图片 | `id` (str, required, positional); `type` (str, optional, default='Rb'); `limit` (int, optional, default=120); `photo-id` (str, optional); `output` (str, optional, default='./douban-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
