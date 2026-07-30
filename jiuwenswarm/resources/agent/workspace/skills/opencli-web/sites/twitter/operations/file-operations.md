# Twitter: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli twitter download ["<username>"] [--tweet-url "<tweet-url>"] [--limit <limit>] [--output "<output>"] -f json`<br>Download Twitter/X media (images and videos). Provide either <username> to fetch every media item from their profile via the GraphQL UserMedia endpoint with cursor pagination, or --tweet-url to download a single tweet. | `username` (str, optional, positional); `tweet-url` (str, optional); `limit` (int, optional, default=10); `output` (str, optional, default='./twitter-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
