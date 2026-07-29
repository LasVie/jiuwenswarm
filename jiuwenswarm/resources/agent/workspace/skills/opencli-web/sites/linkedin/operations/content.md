---
opencli_contract:
  version: 2
  site: linkedin
  operation: content
  policy_sha256: 318b046f8d0394572c515dd0fcd92133ed118ddb2219732dc3c17115eac020f9
  commands:
    job-detail:
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
      - help: Exact LinkedIn job URL, e.g. https://www.linkedin.com/jobs/view/123/
        name: job-url
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Linkedin: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `job-detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read one LinkedIn job page with description, apply URL, workplace type, applicants, and company metadata | `job-url` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
