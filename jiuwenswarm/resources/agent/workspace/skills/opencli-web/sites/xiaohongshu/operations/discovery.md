# Xiaohongshu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli xiaohongshu ask "<query>" [--timeout <timeout>] [--source-limit <source-limit>] -f json`<br>Ask 小红书点点 and return the answer with citation sources. | `query` (str, required, positional); `timeout` (int, optional, default=90); `source-limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `feed` | `private_content_read` / `medium` | `opencli xiaohongshu feed [--limit <limit>] -f json`<br>小红书首页推荐 Feed (reads hydrated Pinia store) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli xiaohongshu search "<query>" [--limit <limit>] -f json`<br>搜索小红书笔记 | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `ask`: Treat a citation URL as usable only when it contains a non-empty xsec_token. Before presenting citations or passing one to note, comments, or download, resolve every unsigned source with search using its title and author, require the returned note ID to match, and copy the signed search result URL unchanged. Never expose a bare /explore/<note-id> URL as a clickable link; if resolution fails, report that source as unavailable without a link
- `feed`: Preserve every returned note URL unchanged, including its non-empty xsec_token and complete query string; never shorten it to a bare /explore/<note-id> URL; sensitive output: private content, account identifiers
- `search`: Preserve every returned note URL unchanged, including its non-empty xsec_token and complete query string; never shorten it to a bare /explore/<note-id> URL; sensitive output: private content, account identifiers
