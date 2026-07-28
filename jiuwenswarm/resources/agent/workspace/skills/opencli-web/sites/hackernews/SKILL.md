---
name: opencli-hackernews
description: Route reviewed Hackernews website operations through the OpenCLI Web structured execution boundary.
---

# Hackernews

Catalog site slug: `hackernews`.
 Known domains: `news.ycombinator.com`, `hacker-news.firebaseio.com`, `hn.algolia.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `content` | Read site content and metadata. | `ask`, `best`, `jobs`, `new`, `read`, `show`, `top`, `user` | `sites/hackernews/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/hackernews/operations/discovery.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
