# Spotify: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli spotify search "<query>" [--limit <limit>] -f json`<br>Search for tracks | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=required; transport=mixed; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `search`: Token refresh may rewrite the local Spotify token file.; file inputs: ~/.opencli/spotify.env, ~/.opencli/spotify-tokens.json; file outputs: ~/.opencli/spotify-tokens.json; sensitive output: OAuth access and refresh tokens
