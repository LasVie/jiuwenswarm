---
name: opencli-linkedin
description: Route reviewed Linkedin website operations through the OpenCLI Web structured execution boundary.
---

# Linkedin

Catalog site slug: `linkedin`.
 Known domains: `www.linkedin.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile-analytics`, `profile-experience`, `profile-projects`, `profile-read`, `whoami` | `sites/linkedin/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/linkedin/operations/authentication.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `connect`, `safe-send`, `salesnav-message` | `sites/linkedin/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `inbox`, `job-detail`, `jobs-preferences`, `people-search`, `post-analytics`, `posts`, `salesnav-inbox`, `salesnav-search`, `salesnav-thread`, `search`, `sent-invitations`, `services-read`, `thread-snapshot`, `timeline` | `sites/linkedin/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
