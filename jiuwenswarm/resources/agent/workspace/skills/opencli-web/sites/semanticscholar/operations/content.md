---
opencli_contract:
  version: 2
  site: semanticscholar
  operation: content
  policy_sha256: 80cdefddefe3c688c608e3f21efc4648d5112d91919554bf26227e9a9924071d
  commands:
    citations:
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
      - help: paperId (40-char hex), DOI, arXiv id, or prefixed id
        name: id
        positional: true
        required: true
        type: str
      - default: 20
        help: Max citing papers (1-1000, single Semantic Scholar page)
        name: limit
        required: false
        type: int
      - default: 0
        help: Page offset (0-based)
        name: offset
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
      - help: paperId (40-char hex), DOI, arXiv id, or prefixed id (e.g. "ARXIV:1706.03762", "PMID:12345")
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
    recommendations:
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
      - help: paperId (40-char hex), DOI, arXiv id, or prefixed id
        name: id
        positional: true
        required: true
        type: str
      - default: 10
        help: Max recommendations (1-500)
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

# Semanticscholar: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `citations` | `enabled` | `public_read` / `low` | `opencli_execute(site="semanticscholar", operation="content", command="citations", arguments={"id":"<id>"})`<br>List papers that cite a Semantic Scholar paper (paginated) | `id` (str, required, positional); `limit` (int, optional, default=20); `offset` (int, optional, default=0) |
| `paper` | `enabled` | `public_read` / `low` | `opencli_execute(site="semanticscholar", operation="content", command="paper", arguments={"id":"<id>"})`<br>Semantic Scholar paper detail (citation graph + AI tldr) by paperId, DOI, or arXiv id | `id` (str, required, positional) |
| `recommendations` | `enabled` | `public_read` / `low` | `opencli_execute(site="semanticscholar", operation="content", command="recommendations", arguments={"id":"<id>"})`<br>Semantic Scholar AI-curated related papers for a paperId, DOI, or arXiv id | `id` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
