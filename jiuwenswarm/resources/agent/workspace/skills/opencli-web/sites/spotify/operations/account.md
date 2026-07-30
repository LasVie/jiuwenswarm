# Spotify: account

Read account-scoped playback state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli spotify status -f json`<br>Show current playback status | none | auth=required; transport=mixed; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: Token refresh may rewrite the local Spotify token file.; file inputs: ~/.opencli/spotify.env, ~/.opencli/spotify-tokens.json; file outputs: ~/.opencli/spotify-tokens.json; sensitive output: private playback state, account identifiers, OAuth access and refresh tokens
