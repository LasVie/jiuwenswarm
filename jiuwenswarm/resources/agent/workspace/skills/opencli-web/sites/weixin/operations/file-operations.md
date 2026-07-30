# Weixin: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli weixin download --url "<url>" [--output "<output>"] [--download-images <true\|false>] -f json`<br>下载微信公众号文章为 Markdown 格式 | `url` (str, required); `output` (str, optional, default='./weixin-articles'); `download-images` (boolean, optional, default=True) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
