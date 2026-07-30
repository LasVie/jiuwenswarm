# Amazon: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `discussion` | `public_read` / `low` | `opencli amazon discussion "<input>" [--limit <limit>] -f json`<br>Amazon review summary and sample customer discussion from product review pages | `input` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `offer` | `public_read` / `low` | `opencli amazon offer "<input>" -f json`<br>Amazon seller, buy box, and fulfillment facts from the product page | `input` (str, required, positional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `product` | `public_read` / `low` | `opencli amazon product "<input>" -f json`<br>Amazon product page facts for candidate validation | `input` (str, required, positional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
