---
opencli_contract:
  version: 2
  site: booking
  operation: discovery
  policy_sha256: f98ede62d80d01b8a28551b538a0475f0e73b690a74f14e8425c4bf6db920d94
  commands:
    search:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Booking: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="booking", operation="discovery", command="search", arguments={"destination":"<destination>","checkin":"<checkin>","checkout":"<checkout>"})`<br>Search Booking.com hotels by destination and dates (server-rendered card scrape). | `destination` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `adults` (int, optional, default=2); `rooms` (int, optional, default=1); `children` (int, optional, default=0); `currency` (str, optional); `lang` (str, optional); `limit` (int, optional, default=25); `offset` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
