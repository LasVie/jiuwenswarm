# Zhihu: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli zhihu download --url "<url>" [--output "<output>"] [--download-images <true\|false>] -f json`<br>导出知乎文章为 Markdown 格式 | `url` (str, required); `output` (str, optional, default='./zhihu-articles'); `download-images` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
