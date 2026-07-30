# Geogebra: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-circle` | `reversible_remote_write` / `high` | `opencli geogebra add-circle --center "<center>" [--radius "<radius>"] [--point "<point>"] -f json`<br>Create a circle by center+radius or center+point | `center` (str, required); `radius` (str, optional); `point` (str, optional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `add-line` | `reversible_remote_write` / `high` | `opencli geogebra add-line --points "<points>" [--type "<line\|segment\|ray>"] -f json`<br>Create a line through two points or a segment between two points | `points` (str, required); `type` (str, optional, default='line', choices=line,segment,ray) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `add-point` | `reversible_remote_write` / `high` | `opencli geogebra add-point --name "<name>" --coords "<coords>" -f json`<br>Create a point with given label and coordinates | `name` (str, required); `coords` (str, required) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `add-polygon` | `reversible_remote_write` / `high` | `opencli geogebra add-polygon --points "<points>" -f json`<br>Create a polygon from a list of point labels | `points` (str, required) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `hexagon` | `reversible_remote_write` / `high` | `opencli geogebra hexagon [--size "<size>"] -f json`<br>Draw a regular hexagon centered at the origin | `size` (str, optional, default='2') | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `triangle` | `reversible_remote_write` / `high` | `opencli geogebra triangle [--size "<size>"] -f json`<br>Draw an equilateral triangle from a horizontal base segment | `size` (str, optional, default='2') | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
