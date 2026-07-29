---
opencli_contract:
  version: 2
  site: linkedin
  operation: private-content
  policy_sha256: 318b046f8d0394572c515dd0fcd92133ed118ddb2219732dc3c17115eac020f9
  commands:
    inbox:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 40
        help: Maximum conversations to return (1-100)
        name: limit
        required: false
        type: int
      - default: false
        help: Return only conversations with unread messages
        name: unread-only
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    jobs-preferences:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    people-search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: People search keywords, e.g. "site reliability engineer berlin"
        name: keywords
        positional: true
        required: true
        type: string
      - default: 5
        help: Maximum people to return (1-10); each query counts toward LinkedIn's monthly CUL
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    post-analytics:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      - default: 30
        help: Maximum posts to summarize (1-100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    posts:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      - default: 20
        help: Maximum posts to return (1-100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    salesnav-inbox:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 40
        help: Maximum conversations to return (1-500)
        name: limit
        required: false
        type: number
      - default: 30
        help: Maximum Sales Navigator API pages to fetch
        name: max-pages
        required: false
        type: number
      - default: false
        help: Return only unread conversations
        name: unread-only
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    salesnav-search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: People search keywords, e.g. "quality manager food manufacturing"
        name: keywords
        positional: true
        required: true
        type: string
      - default: 25
        help: Maximum leads to return (1-500, fetched 25 per request)
        name: limit
        required: false
        type: number
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    salesnav-thread:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Sales Navigator inbox URL/thread id, Sales Navigator lead URL, recipient urn, or exact participant name
        name: thread-or-recipient
        positional: true
        required: true
        type: string
      - default: 200
        help: Maximum messages to return (1-500)
        name: limit
        required: false
        type: number
      - default: 30
        help: Maximum inbox pages to scan when resolving a recipient
        name: max-pages
        required: false
        type: number
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    sent-invitations:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    services-read:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      - help: LinkedIn /services/page/<id>/ URL. If omitted, it is discovered from the profile.
        name: services-url
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    thread-snapshot:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Exact LinkedIn messaging thread URL to open and snapshot
        name: thread-url
        required: true
        type: str
      - default: 30
        help: Maximum upward scroll attempts to load older messages
        name: max-scrolls
        required: false
        type: number
      - default: false
        help: Return only JSON snapshot string in the snapshot_json field
        name: json
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    timeline:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of posts to return (max 100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Linkedin: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `inbox` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List LinkedIn messaging inbox conversations and unread messages | `limit` (int, optional, default=40); `unread-only` (bool, optional, default=False) |
| `jobs-preferences` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read visible LinkedIn Jobs preferences and alert settings without changing them | none |
| `people-search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search standard LinkedIn (not Sales Navigator) for people by keyword. Each invocation consumes against LinkedIn's monthly Commercial Use Limit on people search; throttle accordingly. | `keywords` (string, required, positional); `limit` (int, optional, default=5) |
| `post-analytics` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Summarize raw visible LinkedIn post counters without custom scoring or classification | `profile-url` (string, optional); `limit` (int, optional, default=30) |
| `posts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Export visible posts from a LinkedIn profile activity page with engagement metrics | `profile-url` (string, optional); `limit` (int, optional, default=20) |
| `salesnav-inbox` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List LinkedIn Sales Navigator message conversations with API pagination | `limit` (number, optional, default=40); `max-pages` (number, optional, default=30); `unread-only` (bool, optional, default=False) |
| `salesnav-search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search LinkedIn Sales Navigator for people leads by keyword | `keywords` (string, required, positional); `limit` (number, optional, default=25) |
| `salesnav-thread` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Return full Sales Navigator message history for a thread id, Sales Navigator inbox URL, lead URL, recipient urn, or exact recipient name | `thread-or-recipient` (string, required, positional); `limit` (number, optional, default=200); `max-pages` (number, optional, default=30) |
| `sent-invitations` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List pending LinkedIn sent invitations for CRM reconciliation | none |
| `services-read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read LinkedIn Services page details including services, overview, availability, pricing, and media titles/descriptions | `profile-url` (string, optional); `services-url` (string, optional) |
| `thread-snapshot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Load a LinkedIn messaging thread, scroll for available history, and return a full context snapshot | `thread-url` (str, required); `max-scrolls` (number, optional, default=30); `json` (bool, optional, default=False) |
| `timeline` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read LinkedIn home timeline posts | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
