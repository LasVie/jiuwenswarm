---
name: opencli-spotify
description: Route reviewed Spotify website operations through the OpenCLI Web structured execution boundary.
---

# Spotify

Catalog site slug: `spotify`.
 Known domains: `accounts.spotify.com`, `api.spotify.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account-scoped playback state. | `status` | `sites/spotify/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `auth` | `sites/spotify/operations/authentication.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/spotify/operations/discovery.md` |
| `write-actions` | Change remote service state. | `next`, `pause`, `play`, `prev`, `queue`, `repeat`, `shuffle`, `volume` | `sites/spotify/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
