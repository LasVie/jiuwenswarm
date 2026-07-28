---
opencli_contract:
  version: 2
  site: producthunt
  operation: content
  policy_sha256: 7914bffd5537a3ada92b095f92c47f649f0e8bc2229832a8016784a014bff7e7
  commands:
    posts:
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
      - default: 20
        help: Number of results (max 50)
        name: limit
        required: false
        type: int
      - default: ''
        help: 'Category filter: ai-agents, ai-coding-agents, ai-code-editors, ai-chatbots, ai-workflow-automation, vibe-coding, developer-tools, productivity, design-creative, marketing-sales, no-code-platforms, llms, finance, social-community, engineering-development'
        name: category
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    today:
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
      - default: 20
        help: Max results
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Producthunt: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `posts` | `enabled` | `public_read` / `low` | `opencli_execute(site="producthunt", operation="content", command="posts")`<br>Latest Product Hunt launches (optional category filter) | `limit` (int, optional, default=20); `category` (string, optional, default='') |
| `today` | `enabled` | `public_read` / `low` | `opencli_execute(site="producthunt", operation="content", command="today")`<br>Today's Product Hunt launches (most recent day in feed) | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
