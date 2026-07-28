---
opencli_contract:
  version: 2
  site: weread
  operation: discovery
  policy_sha256: fe850910e20949248d867b786fb8ba6f525ea8a61d6b349ac040bef7c4f02ebb
  commands:
    book-search:
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
      - help: Book title keyword, numeric bookId, or reader URL
        name: book
        positional: true
        required: true
        type: str
      - help: Keyword to search inside the selected book
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: Which book search result to use when book is a title keyword
        name: book-rank
        required: false
        type: int
      - default: 20
        help: Max in-book matches to return (1-100)
        name: limit
        required: false
        type: int
      - default: 150
        help: Snippet length around each match (1-500)
        name: fragment-size
        required: false
        type: int
      - default: false
        help: Output structured rows instead of markdown text
        name: raw
        required: false
        type: boolean
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: 10
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

# Weread: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `book-search` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread", operation="discovery", command="book-search", arguments={"book":"<book>","query":"<query>"})`<br>Search within a WeRead book after resolving it by title | `book` (str, required, positional); `query` (str, required, positional); `book-rank` (int, optional, default=1); `limit` (int, optional, default=20); `fragment-size` (int, optional, default=150); `raw` (boolean, optional, default=False) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search books on WeRead | `query` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
