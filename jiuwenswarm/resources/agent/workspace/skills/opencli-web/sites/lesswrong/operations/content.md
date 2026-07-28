---
opencli_contract:
  version: 2
  site: lesswrong
  operation: content
  policy_sha256: e4038a061ced01aa02a9e4d980a78f9e7eaa68cde6ab7d30c108f8c2028f618b
  commands:
    comments:
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
      - help: Post URL or LessWrong post ID
        name: url-or-id
        positional: true
        required: true
        type: string
      - default: 5
        help: Number of comments
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
    curated:
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
      - default: 10
        help: Number of results
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
    frontpage:
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
      - default: 10
        help: Number of results
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
    new:
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
      - default: 10
        help: Number of results
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
      - help: Post URL or LessWrong post ID
        name: url-or-id
        positional: true
        required: true
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    sequences:
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
      - default: 10
        help: Number of results
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
    shortform:
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
      - default: 10
        help: Number of results
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
      - help: Tag slug or name
        name: tag
        positional: true
        required: true
        type: string
      - default: 10
        help: Number of results
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
    tags:
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
        help: Number of results
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
    top:
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
      - default: 10
        help: Number of results
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
    top-month:
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
      - default: 10
        help: Number of results
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
    top-week:
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
      - default: 10
        help: Number of results
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
    top-year:
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
      - default: 10
        help: Number of results
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
    user:
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
      - help: LessWrong username or slug
        name: username
        positional: true
        required: true
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-posts:
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
      - help: LessWrong username or slug
        name: username
        positional: true
        required: true
        type: string
      - default: 10
        help: Number of results
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

# Lesswrong: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="comments", arguments={"url-or-id":"<url-or-id>"})`<br>Top comments on a post | `url-or-id` (string, required, positional); `limit` (int, optional, default=5) |
| `curated` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="curated")`<br>Curated editor's picks | `limit` (int, optional, default=10) |
| `frontpage` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="frontpage")`<br>Algorithmic frontpage | `limit` (int, optional, default=10) |
| `new` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="new")`<br>Latest posts | `limit` (int, optional, default=10) |
| `read` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="read", arguments={"url-or-id":"<url-or-id>"})`<br>Read full post by URL or ID | `url-or-id` (string, required, positional) |
| `sequences` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="sequences")`<br>List post collections | `limit` (int, optional, default=10) |
| `shortform` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="shortform")`<br>Quick takes / shortform posts | `limit` (int, optional, default=10) |
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>Posts by tag | `tag` (string, required, positional); `limit` (int, optional, default=10) |
| `tags` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="tags")`<br>List popular tags | `limit` (int, optional, default=20) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="top")`<br>Top all-time | `limit` (int, optional, default=10) |
| `top-month` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="top-month")`<br>Top this month | `limit` (int, optional, default=10) |
| `top-week` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="top-week")`<br>Top this week | `limit` (int, optional, default=10) |
| `top-year` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="top-year")`<br>Top this year | `limit` (int, optional, default=10) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="user", arguments={"username":"<username>"})`<br>User profile | `username` (string, required, positional) |
| `user-posts` | `enabled` | `public_read` / `low` | `opencli_execute(site="lesswrong", operation="content", command="user-posts", arguments={"username":"<username>"})`<br>List a user's posts | `username` (string, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
