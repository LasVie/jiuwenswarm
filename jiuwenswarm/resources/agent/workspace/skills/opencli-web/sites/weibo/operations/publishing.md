---
opencli_contract:
  version: 2
  site: weibo
  operation: publishing
  policy_sha256: ad9fe9aad5f989b83f399caba4b2e7a2cb38fc789078e5f2ab7ddcbd9f56e44b
  commands:
    publish:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Weibo text content (max 2000 chars)
        name: text
        positional: true
        required: true
        type: string
      - help: Image paths, comma-separated, max 9 (jpg/png/gif/webp)
        name: images
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Weibo: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `publish` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Publish a new Weibo post immediately | `text` (string, required, positional); `images` (string, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
