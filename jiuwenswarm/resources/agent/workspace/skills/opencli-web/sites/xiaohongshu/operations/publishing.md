# Xiaohongshu: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli xiaohongshu publish "<content>" --title "<title>" [--images "<images>"] [--card-text "<card-text>"] [--card-style "<card-style>"] [--topics "<topics>"] [--draft <true\|false>] -f json`<br>小红书发布图文笔记 (creator center UI automation) | `content` (str, required, positional); `title` (str, required); `images` (str, optional); `card-text` (str, optional); `card-style` (str, optional); `topics` (str, optional); `draft` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: On Windows, shell_type=auto is allowed. For multiline or quote-rich user values, encode them as UTF-8 Base64 and decode them into PowerShell variables with `$value=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('<base64>'))` before invoking opencli; never inline raw multiline user text. In --card-text, use the literal characters \n for an in-card line break and ||| between cards. Pass --topics as comma-separated names without #. Style availability is dynamic: omit --card-style unless the user explicitly names an exact style, and omission uses 基础. Never infer a style from the static help catalog. If OpenCLI returns `requested style "..." is not available` with `options`, the failure is before submission; retry at most once using only an exact value from those returned options. If no suitable option is clear, ask the user or retry without --card-style; file inputs: /images/*
