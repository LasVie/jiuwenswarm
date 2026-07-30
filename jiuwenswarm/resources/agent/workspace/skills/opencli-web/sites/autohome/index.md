# Autohome

- Site slug: `autohome`
- Domains: `www.autohome.com.cn`, `k.autohome.com.cn`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `brand`, `score` | `sites/autohome/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `brand` | `public_read` / `low` | `opencli autohome brand "<brand>" [--limit <limit>] -f json`<br>汽车之家按品牌列出全部车系 + 厂商指导价（免登录） | `brand` (str, required, positional); `limit` (int, optional, default=60) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `score` | `public_read` / `low` | `opencli autohome score "<series_id>" -f json`<br>汽车之家车系口碑评分（总分 + 各维度 + 故障率PPH + 竞品对比，免登录） | `series_id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
