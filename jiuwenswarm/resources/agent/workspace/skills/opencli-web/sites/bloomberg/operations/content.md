---
opencli_contract:
  version: 2
  site: bloomberg
  operation: content
  policy_sha256: fc11a4e4f3dba4820f8bc9aa003f0fa2e715721959938e3cfb3f97b8b6cab036
  commands:
    businessweek:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 1
        help: Number of stories to return (max 20)
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
    crypto:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    economics:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    feeds:
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
      args: []
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    green:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    industries:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    main:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    markets:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    opinions:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    politics:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    pursuits:
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
      - default: 1
        help: Number of feed items to return (max 20)
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
    tech:
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
      - default: 1
        help: Number of feed items to return (max 20)
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

# Bloomberg: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `businessweek` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="businessweek")`<br>Bloomberg Businessweek top stories | `limit` (int, optional, default=1) |
| `crypto` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="crypto")`<br>Bloomberg Crypto top stories (RSS) | `limit` (int, optional, default=1) |
| `economics` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="economics")`<br>Bloomberg Economics top stories (RSS) | `limit` (int, optional, default=1) |
| `feeds` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="feeds")`<br>List the Bloomberg RSS feed aliases used by the adapter | none |
| `green` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="green")`<br>Bloomberg Green (climate & energy) top stories (RSS) | `limit` (int, optional, default=1) |
| `industries` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="industries")`<br>Bloomberg Industries top stories (RSS) | `limit` (int, optional, default=1) |
| `main` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="main")`<br>Bloomberg homepage top stories (RSS) | `limit` (int, optional, default=1) |
| `markets` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="markets")`<br>Bloomberg Markets top stories (RSS) | `limit` (int, optional, default=1) |
| `opinions` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="opinions")`<br>Bloomberg Opinion top stories (RSS) | `limit` (int, optional, default=1) |
| `politics` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="politics")`<br>Bloomberg Politics top stories (RSS) | `limit` (int, optional, default=1) |
| `pursuits` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="pursuits")`<br>Bloomberg Pursuits (lifestyle) top stories (RSS) | `limit` (int, optional, default=1) |
| `tech` | `enabled` | `public_read` / `low` | `opencli_execute(site="bloomberg", operation="content", command="tech")`<br>Bloomberg Tech top stories (RSS) | `limit` (int, optional, default=1) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
