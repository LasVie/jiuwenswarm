---
opencli_contract:
  version: 2
  site: weread-official
  operation: discovery
  policy_sha256: d16f3266d955da66267fd7e1dbaf9cdfc6ea30567dde1ce258059361ff600b3d
  commands:
    discover:
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
      - help: Anchor bookId for similar-book mode; omit for personalized recommendations
        name: bookId
        positional: true
        required: false
        type: str
      - default: 12
        help: Page size (default 12)
        name: count
        required: false
        type: int
      - default: 0
        help: 'Pagination cursor (recommend: previous searchIdx; similar: previous idx)'
        name: max-idx
        required: false
        type: int
      - help: Carry-forward sessionId for /book/similar paging
        name: session-id
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    list-apis:
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
        name: keyword
        positional: true
        required: true
        type: str
      - choices:
        - all
        - ebook
        - webnovel
        - audio
        - author
        - fulltext
        - booklist
        - mp
        - article
        default: ebook
        help: Search type (all/ebook/webnovel/audio/author/fulltext/booklist/mp/article)
        name: scope
        required: false
        type: str
      - help: Page size (gateway default 15 when omitted)
        name: count
        required: false
        type: int
      - default: 0
        help: Pagination offset, use searchIdx of last item from previous page
        name: max-idx
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

# Weread Official: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `discover` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="discovery", command="discover")`<br>Personalized or similar-book recommendations from WeRead | `bookId` (str, optional, positional); `count` (int, optional, default=12); `max-idx` (int, optional, default=0); `session-id` (str, optional) |
| `list-apis` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="discovery", command="list-apis")`<br>List every api_name supported by the WeRead agent gateway | none |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>Search WeRead store via the official agent gateway | `keyword` (str, required, positional); `scope` (str, optional, default='ebook', choices=all,ebook,webnovel,audio,author,fulltext,booklist,mp,article); `count` (int, optional); `max-idx` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
