---
opencli_contract:
  version: 2
  site: geogebra
  operation: write-actions
  policy_sha256: 96b5e0ced92cddb4cb2074e33e62e5c7e81e94d600703a48694341552ae52a5d
  commands:
    add-circle:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Center point label (e.g. A)
        name: center
        required: true
        type: str
      - help: Radius value (number) or a point label on the circle
        name: radius
        required: false
        type: str
      - help: 'Alternative: a point label on the circle (use instead of --radius for Circle(center,point))'
        name: point
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    add-line:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Two point labels separated by comma (e.g. "A,B")
        name: points
        required: true
        type: str
      - choices:
        - line
        - segment
        - ray
        default: line
        help: 'Type: line, segment, or ray (default: line)'
        name: type
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    add-point:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Point label (e.g. A, B, P1)
        name: name
        required: true
        type: str
      - help: Coordinates as x,y (e.g. "1,2")
        name: coords
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    add-polygon:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Comma-separated point labels (e.g. "A,B,C" or "A,B,C,D")
        name: points
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    hexagon:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - default: '2'
        help: 'Radius of the hexagon (default: 2)'
        name: size
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    triangle:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - default: '2'
        help: 'Side length of the triangle (default: 2)'
        name: size
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Geogebra: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `add-circle` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a circle by center+radius or center+point | `center` (str, required); `radius` (str, optional); `point` (str, optional) |
| `add-line` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a line through two points or a segment between two points | `points` (str, required); `type` (str, optional, default='line', choices=line,segment,ray) |
| `add-point` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a point with given label and coordinates | `name` (str, required); `coords` (str, required) |
| `add-polygon` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a polygon from a list of point labels | `points` (str, required) |
| `hexagon` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Draw a regular hexagon centered at the origin | `size` (str, optional, default='2') |
| `triangle` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Draw an equilateral triangle from a horizontal base segment | `size` (str, optional, default='2') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
