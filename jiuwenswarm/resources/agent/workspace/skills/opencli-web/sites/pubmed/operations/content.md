---
opencli_contract:
  version: 2
  site: pubmed
  operation: content
  policy_sha256: 870bd148e1f5649c695d65a65eaa5978085f62a97cbad6ca74a974df3899b21c
  commands:
    article:
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
      - help: PubMed ID, e.g. 37780221
        name: pmid
        positional: true
        required: true
        type: str
      - default: false
        help: Do not truncate the abstract in table output
        name: full-abstract
        required: false
        type: boolean
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
      - help: Author name, e.g. "Smith J"
        name: name
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - help: Filter by author affiliation
        name: affiliation
        required: false
        type: str
      - choices:
        - any
        - first
        - last
        default: any
        help: 'Author position: any, first, or last'
        name: position
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
      - choices:
        - date
        - relevance
        default: date
        help: Sort by date or relevance
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
      - help: PubMed ID, e.g. 37780221
        name: pmid
        positional: true
        required: true
        type: str
      - choices:
        - citedby
        - references
        default: citedby
        help: citedby or references
        name: direction
        required: false
        type: str
      - default: 20
        help: Max results (1-100)
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
    clinical-trial:
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
      - help: Clinical topic query, e.g. "breast cancer"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - help: Filter publication year from
        name: year-from
        required: false
        type: int
      - help: Filter publication year to
        name: year-to
        required: false
        type: int
      - default: false
        help: Only include free full text articles
        name: free-full-text
        required: false
        type: boolean
      - choices:
        - date
        - relevance
        default: date
        help: Sort by date or relevance
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
    journal:
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
      - help: Journal name, e.g. "Nature" or "The Lancet"
        name: journal
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - help: Filter publication year from
        name: year-from
        required: false
        type: int
      - help: Filter publication year to
        name: year-to
        required: false
        type: int
      - choices:
        - relevance
        - date
        default: relevance
        help: Sort by relevance or date
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
    mesh:
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
      - help: MeSH term, e.g. "Neoplasms" or "Machine Learning"
        name: term
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - default: false
        help: Only include articles where this is a major MeSH topic
        name: major
        required: false
        type: boolean
      - choices:
        - relevance
        - date
        default: relevance
        help: Sort by relevance or date
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
    related:
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
      - help: PubMed ID, e.g. 37780221
        name: pmid
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - default: false
        help: Show similarity scores when available
        name: score
        required: false
        type: boolean
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    review:
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
      - help: Review topic query, e.g. "immunotherapy"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results (1-100)
        name: limit
        required: false
        type: int
      - help: Filter publication year from
        name: year-from
        required: false
        type: int
      - help: Filter publication year to
        name: year-to
        required: false
        type: int
      - default: false
        help: Only include articles with abstracts
        name: has-abstract
        required: false
        type: boolean
      - choices:
        - date
        - relevance
        default: date
        help: Sort by date or relevance
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

# Pubmed: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `article` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="article", arguments={"pmid":"<pmid>"})`<br>Get detailed information for a PubMed article by PMID | `pmid` (str, required, positional); `full-abstract` (boolean, optional, default=False) |
| `author` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="author", arguments={"name":"<name>"})`<br>Search PubMed articles by author name and optional affiliation | `name` (str, required, positional); `limit` (int, optional, default=20); `affiliation` (str, optional); `position` (str, optional, default='any', choices=any,first,last); `year-from` (int, optional); `year-to` (int, optional); `sort` (str, optional, default='date', choices=date,relevance) |
| `citations` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="citations", arguments={"pmid":"<pmid>"})`<br>Get PubMed citation relationships for an article | `pmid` (str, required, positional); `direction` (str, optional, default='citedby', choices=citedby,references); `limit` (int, optional, default=20) |
| `clinical-trial` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="clinical-trial", arguments={"query":"<query>"})`<br>Search PubMed clinical trials with a trial-study preset | `query` (str, required, positional); `limit` (int, optional, default=20); `year-from` (int, optional); `year-to` (int, optional); `free-full-text` (boolean, optional, default=False); `sort` (str, optional, default='date', choices=date,relevance) |
| `journal` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="journal", arguments={"journal":"<journal>"})`<br>Search PubMed articles by journal name | `journal` (str, required, positional); `limit` (int, optional, default=20); `year-from` (int, optional); `year-to` (int, optional); `sort` (str, optional, default='relevance', choices=relevance,date) |
| `mesh` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="mesh", arguments={"term":"<term>"})`<br>Search PubMed articles by MeSH term | `term` (str, required, positional); `limit` (int, optional, default=20); `major` (boolean, optional, default=False); `sort` (str, optional, default='relevance', choices=relevance,date) |
| `related` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="related", arguments={"pmid":"<pmid>"})`<br>Find articles related to a PubMed article | `pmid` (str, required, positional); `limit` (int, optional, default=20); `score` (boolean, optional, default=False) |
| `review` | `enabled` | `public_read` / `low` | `opencli_execute(site="pubmed", operation="content", command="review", arguments={"query":"<query>"})`<br>Search PubMed review articles with a review preset | `query` (str, required, positional); `limit` (int, optional, default=20); `year-from` (int, optional); `year-to` (int, optional); `has-abstract` (boolean, optional, default=False); `sort` (str, optional, default='date', choices=date,relevance) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
