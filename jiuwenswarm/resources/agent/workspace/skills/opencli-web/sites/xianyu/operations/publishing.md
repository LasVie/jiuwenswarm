# Xianyu: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli xianyu publish "<title>" "<description>" <price> "<condition>" "<category>" [--original_price <original_price>] [--location "<location>"] [--images "<images>"] -f json`<br>发布闲鱼宝贝（需先在浏览器中登录闲鱼） | `title` (str, required, positional); `description` (str, required, positional); `price` (float, required, positional); `condition` (str, required, positional); `category` (str, required, positional); `original_price` (float, optional); `location` (str, optional); `images` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: file inputs: workspace-relative input when declared by adapter
