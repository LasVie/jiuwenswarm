---
opencli_contract:
  version: 2
  site: bluesky
  operation: content
  policy_sha256: d3ed06f93ef09c634420e340ee8d5835e2d5f5308a0719468af5195dc46d3e5a
  commands:
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
      args:
      - default: 20
        help: Number of feeds
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
    followers:
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
      - help: Bluesky handle
        name: handle
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of followers
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
    following:
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
      - help: Bluesky handle
        name: handle
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of accounts
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
    starter-packs:
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
      - help: Bluesky handle
        name: handle
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of starter packs
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
    thread:
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
      - help: Post AT URI (at://did:.../app.bsky.feed.post/...) or bsky.app URL
        name: uri
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of replies
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
      - help: Bluesky handle (e.g. bsky.app)
        name: handle
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of posts
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

# Bluesky: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feeds` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="feeds")`<br>Popular Bluesky feed generators | `limit` (int, optional, default=20) |
| `followers` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="followers", arguments={"handle":"<handle>"})`<br>List followers of a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=20) |
| `following` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="following", arguments={"handle":"<handle>"})`<br>List accounts a Bluesky user is following | `handle` (str, required, positional); `limit` (int, optional, default=20) |
| `starter-packs` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="starter-packs", arguments={"handle":"<handle>"})`<br>Get starter packs created by a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=10) |
| `thread` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="thread", arguments={"uri":"<uri>"})`<br>Get a Bluesky post thread with replies | `uri` (str, required, positional); `limit` (int, optional, default=20) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="bluesky", operation="content", command="user", arguments={"handle":"<handle>"})`<br>Get recent posts from a Bluesky user | `handle` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
