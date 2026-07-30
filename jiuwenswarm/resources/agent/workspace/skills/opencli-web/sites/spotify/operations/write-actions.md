# Spotify: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `next` | `reversible_remote_write` / `high` | `opencli spotify next -f json`<br>Skip to next track | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `pause` | `reversible_remote_write` / `high` | `opencli spotify pause -f json`<br>Pause playback | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `play` | `reversible_remote_write` / `high` | `opencli spotify play ["<query>"] -f json`<br>Resume playback or search and play a track/artist | `query` (str, optional, positional, default='') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `prev` | `reversible_remote_write` / `high` | `opencli spotify prev -f json`<br>Skip to previous track | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `queue` | `reversible_remote_write` / `high` | `opencli spotify queue "<query>" -f json`<br>Add a track to the playback queue | `query` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `repeat` | `reversible_remote_write` / `high` | `opencli spotify repeat ["<off\|track\|context>"] -f json`<br>Set repeat mode (off / track / context) | `mode` (str, optional, positional, default='context', choices=off,track,context) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `shuffle` | `reversible_remote_write` / `high` | `opencli spotify shuffle ["<on\|off>"] -f json`<br>Toggle shuffle on/off | `state` (str, optional, positional, default='on', choices=on,off) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `volume` | `reversible_remote_write` / `high` | `opencli spotify volume <level> -f json`<br>Set playback volume (0-100) | `level` (int, required, positional, default=50) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
