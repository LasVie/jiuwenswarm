---
opencli_contract:
  version: 2
  site: pubmed
  operation: discovery
  policy_sha256: 870bd148e1f5649c695d65a65eaa5978085f62a97cbad6ca74a974df3899b21c
  commands:
    search:
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
      - help: Search query, e.g. "machine learning cancer"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - help: Filter by author name
        name: author
        required: false
        type: str
      - help: Filter by journal name
        name: journal
        required: false
        type: str
      - help: Filter publication year from
        name: year-from
        required: false
        type: int
      - help: Filter publication year to
        name: year-to
        required: false
        type: int
      - help: Filter by publication type, e.g. Review or Clinical Trial
        name: article-type
        required: false
        type: str
      - default: false
        help: Only include articles with abstracts
        name: has-abstract
        required: false
        type: boolean
      - default: false
        help: Only include free full text articles
        name: free-full-text
        required: false
        type: boolean
      - default: false
        help: Only include human studies
        name: humans-only
        required: false
        type: boolean
      - default: false
        help: Only include English articles
        name: english-only
        required: false
        type: boolean
      - choices:
        - relevance
        - date
        - author
        - journal
        default: relevance
        help: Sort by relevance, date, author, or journal
        name: sort
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Pubmed: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search PubMed articles with advanced filters | `query` (str, required, positional); `limit` (int, optional, default=20); `author` (str, optional); `journal` (str, optional); `year-from` (int, optional); `year-to` (int, optional); `article-type` (str, optional); `has-abstract` (boolean, optional, default=False); `free-full-text` (boolean, optional, default=False); `humans-only` (boolean, optional, default=False); `english-only` (boolean, optional, default=False); `sort` (str, optional, default='relevance', choices=relevance,date,author,journal) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
