---
opencli_contract:
  version: 2
  site: arxiv
  operation: content
  policy_sha256: 998590eea391c1c50c41701f6bd820cb23ed8f22b8da1b6022beddb16e7240ee
  commands:
    author:
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
      - help: Author name (e.g. "Yoshua Bengio" or "Y Bengio")
        name: author
        positional: true
        required: true
        type: str
      - default: 20
        help: Max papers to return (max 50)
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
    paper:
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
      - help: arXiv paper ID (e.g. 1706.03762)
        name: id
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
    recent:
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
      - help: arXiv category (e.g. cs.CL, cs.LG, math.PR, q-bio.NC)
        name: category
        positional: true
        required: true
        type: str
      - default: 10
        help: Max results (max 50)
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

# Arxiv: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `author` | `enabled` | `public_read` / `low` | `opencli_execute(site="arxiv", operation="content", command="author", arguments={"author":"<author>"})`<br>List arXiv papers by a given author (newest first) | `author` (str, required, positional); `limit` (int, optional, default=20) |
| `paper` | `enabled` | `public_read` / `low` | `opencli_execute(site="arxiv", operation="content", command="paper", arguments={"id":"<id>"})`<br>Get arXiv paper details by ID | `id` (str, required, positional) |
| `recent` | `enabled` | `public_read` / `low` | `opencli_execute(site="arxiv", operation="content", command="recent", arguments={"category":"<category>"})`<br>List recent arXiv submissions in a category | `category` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
