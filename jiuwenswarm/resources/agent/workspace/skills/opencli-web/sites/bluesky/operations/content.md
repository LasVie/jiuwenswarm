# Bluesky: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feeds` | `public_read` / `low` | `opencli bluesky feeds [--limit <limit>] -f json`<br>Popular Bluesky feed generators | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `followers` | `public_read` / `low` | `opencli bluesky followers "<handle>" [--limit <limit>] -f json`<br>List followers of a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `following` | `public_read` / `low` | `opencli bluesky following "<handle>" [--limit <limit>] -f json`<br>List accounts a Bluesky user is following | `handle` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `starter-packs` | `public_read` / `low` | `opencli bluesky starter-packs "<handle>" [--limit <limit>] -f json`<br>Get starter packs created by a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `thread` | `public_read` / `low` | `opencli bluesky thread "<uri>" [--limit <limit>] -f json`<br>Get a Bluesky post thread with replies | `uri` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli bluesky user "<handle>" [--limit <limit>] -f json`<br>Get recent posts from a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
