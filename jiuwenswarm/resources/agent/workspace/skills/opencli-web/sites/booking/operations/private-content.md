---
opencli_contract:
  version: 2
  site: booking
  operation: private-content
  policy_sha256: ae58fe19cc95a2824f37d000c6a87caf5784a7c9ce0ea235c2d769c611d68ba5
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Destination keyword (city, district, or hotel name)
        name: destination
        positional: true
        required: true
        type: str
      - help: Check-in date YYYY-MM-DD
        name: checkin
        required: true
        type: str
      - help: Check-out date YYYY-MM-DD
        name: checkout
        required: true
        type: str
      - default: 2
        help: Number of adults (1-30)
        name: adults
        required: false
        type: int
      - default: 1
        help: Number of rooms (1-30)
        name: rooms
        required: false
        type: int
      - default: 0
        help: Number of children (0-10)
        name: children
        required: false
        type: int
      - help: Force result currency (e.g. USD, JPY, CNY)
        name: currency
        required: false
        type: str
      - help: Force result language (e.g. en-us, zh-cn, ja)
        name: lang
        required: false
        type: str
      - default: 25
        help: Max rows to return (1-100; Booking pages 25 per request)
        name: limit
        required: false
        type: int
      - default: 0
        help: Result offset for pagination (multiple of 25)
        name: offset
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

# Booking: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Booking.com hotels by destination and dates (server-rendered card scrape). | `destination` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `adults` (int, optional, default=2); `rooms` (int, optional, default=1); `children` (int, optional, default=0); `currency` (str, optional); `lang` (str, optional); `limit` (int, optional, default=25); `offset` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
