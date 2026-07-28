---
name: opencli-bluesky
description: Route reviewed Bluesky website operations through the OpenCLI Web structured execution boundary.
---

# Bluesky

Catalog site slug: `bluesky`.
 Known domains: `public.api.bsky.app`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile` | `sites/bluesky/operations/account.md` |
| `content` | Read site content and metadata. | `feeds`, `followers`, `following`, `starter-packs`, `thread`, `user` | `sites/bluesky/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search`, `trending` | `sites/bluesky/operations/discovery.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
