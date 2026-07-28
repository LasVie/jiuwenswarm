---
opencli_contract:
  version: 2
  site: lobsters
  operation: content
  policy_sha256: d6b7614221f62ecda60c6e2397512a783ca588b95d09c22acfa05b9a80519cfd
  commands:
    active:
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
        help: Number of stories
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
    domain:
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
      - help: Source domain (e.g. github.com, arxiv.org, blog.cloudflare.com)
        name: domain
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of stories (1-25 — single page)
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
    hot:
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
        help: Number of stories
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
    newest:
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
        help: Number of stories
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
    read:
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
      - help: Lobste.rs short_id (e.g. 6cmh6h)
        name: id
        positional: true
        required: true
        type: str
      - default: 25
        help: Max top-level comments
        name: limit
        required: false
        type: int
      - default: 2
        help: Max reply depth (1=no replies, 2=one level of replies, etc.)
        name: depth
        required: false
        type: int
      - default: 5
        help: Max replies shown per comment at each level
        name: replies
        required: false
        type: int
      - default: 2000
        help: Max characters per comment body (min 100)
        name: max-length
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    tag:
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
      - help: Tag name (e.g. programming, rust, security, ai)
        name: tag
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of stories
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

# Lobsters: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `active` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="active")`<br>Lobste.rs most active discussions | `limit` (int, optional, default=20) |
| `domain` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="domain", arguments={"domain":"<domain>"})`<br>Lobste.rs stories submitted from a specific domain | `domain` (str, required, positional); `limit` (int, optional, default=20) |
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="hot")`<br>Lobste.rs hottest stories | `limit` (int, optional, default=20) |
| `newest` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="newest")`<br>Lobste.rs newest stories | `limit` (int, optional, default=20) |
| `read` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="read", arguments={"id":"<id>"})`<br>Read a Lobste.rs story and its comment tree | `id` (str, required, positional); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000) |
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="lobsters", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>Lobste.rs stories by tag | `tag` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
