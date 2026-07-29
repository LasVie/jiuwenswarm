---
opencli_contract:
  version: 2
  site: '12306'
  operation: content
  policy_sha256: a9c2153ec6af33e164eaa13b3178d3ca73ad689492934924eebed94b624550da
  commands:
    price:
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
      - help: Internal train_no from `12306 trains` (e.g. 24000000G10L)
        name: train-no
        positional: true
        required: true
        type: str
      - help: Origin station (Chinese name, telecode, or pinyin) - must be a stop of this train
        name: from
        required: true
        type: str
      - help: Destination station - must be a stop of this train
        name: to
        required: true
        type: str
      - help: Departure date in YYYY-MM-DD
        name: date
        required: true
        type: str
      - default: OM9PA1A3A4FWZ
        help: 'Seat-type letters to query (default covers the common classes). Examples: OM9 (二等/一等/商务), A1A3A4 (硬座/硬卧/软卧).'
        name: seat-types
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    stations:
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
      - help: Chinese substring (上海), telecode (AOH), or pinyin (shanghai)
        name: keyword
        positional: true
        required: true
        type: str
      - default: 20
        help: Maximum results (1-50)
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
    train:
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
      - help: Internal train_no from `12306 trains` (e.g. 24000000G10L), not the public code (G1)
        name: train-no
        positional: true
        required: true
        type: str
      - help: 'Origin station for the segment: Chinese name, telecode, or pinyin'
        name: from
        required: true
        type: str
      - help: Destination station for the segment
        name: to
        required: true
        type: str
      - help: Departure date in YYYY-MM-DD
        name: date
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    trains:
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
      - help: 'Origin station: Chinese name (北京), telecode (BJP), or pinyin (beijing)'
        name: from
        positional: true
        required: true
        type: str
      - help: 'Destination station: same forms as <from>'
        name: to
        positional: true
        required: true
        type: str
      - help: Departure date in YYYY-MM-DD
        name: date
        required: true
        type: str
      - default: 50
        help: Maximum rows (1-100)
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

# 12306: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `price` | `enabled` | `public_read` / `low` | `opencli_execute(site="12306", operation="content", command="price", arguments={"train-no":"<train-no>","from":"<from>","to":"<to>","date":"<date>"})`<br>Look up 12306 ticket prices by seat class for one train on a given date and segment (anonymous, no login required) | `train-no` (str, required, positional); `from` (str, required); `to` (str, required); `date` (str, required); `seat-types` (str, optional, default='OM9PA1A3A4FWZ') |
| `stations` | `enabled` | `public_read` / `low` | `opencli_execute(site="12306", operation="content", command="stations", arguments={"keyword":"<keyword>"})`<br>Search 12306 (China Railway) stations by Chinese name, telecode, or pinyin keyword | `keyword` (str, required, positional); `limit` (int, optional, default=20) |
| `train` | `enabled` | `public_read` / `low` | `opencli_execute(site="12306", operation="content", command="train", arguments={"train-no":"<train-no>","from":"<from>","to":"<to>","date":"<date>"})`<br>List every station a 12306 train calls at, with arrival / departure / stopover time (anonymous, no login required) | `train-no` (str, required, positional); `from` (str, required); `to` (str, required); `date` (str, required) |
| `trains` | `enabled` | `public_read` / `low` | `opencli_execute(site="12306", operation="content", command="trains", arguments={"from":"<from>","to":"<to>","date":"<date>"})`<br>List trains between two 12306 stations on a given date (anonymous, no login required) | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=50) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
