---
opencli_contract:
  version: 2
  site: linkedin-learning
  operation: content
  policy_sha256: 613a7e30082d1f650dbc5df6c9960d87c964b19f140a6ff75924f641310b9671
  commands:
    course:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Course slug (e.g. agentic-ai-build-your-first-agentic-ai-system) or full /learning/<slug> URL
        name: slug
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Linkedin Learning: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `course` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get LinkedIn Learning course detail by slug or course URL | `slug` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
