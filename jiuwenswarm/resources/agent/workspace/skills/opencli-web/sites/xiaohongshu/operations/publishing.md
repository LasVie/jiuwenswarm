# Xiaohongshu: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli xiaohongshu publish "<content>" --title "<title>" [--images "<images>"] [--card-text "<card-text>"] [--card-style "<card-style>"] [--topics "<topics>"] [--draft <true\|false>] -f json`<br>小红书发布图文笔记 (creator center UI automation) | `content` (str, required, positional); `title` (str, required); `images` (str, optional); `card-text` (str, optional); `card-style` (str, optional); `topics` (str, optional); `draft` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: file inputs: /images/*
