---
opencli_contract:
  version: 2
  site: bluesky
  operation: account
  policy_sha256: d3ed06f93ef09c634420e340ee8d5835e2d5f5308a0719468af5195dc46d3e5a
  commands:
    profile:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Bluesky handle (e.g. bsky.app, jay.bsky.team)
        name: handle
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Bluesky: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="account", command="profile", arguments={"handle":"<handle>"})`<br>Get Bluesky user profile info | `handle` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
