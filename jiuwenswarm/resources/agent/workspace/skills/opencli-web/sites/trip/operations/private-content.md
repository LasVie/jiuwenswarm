# Trip: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attraction` | `private_content_read` / `medium` | `opencli trip attraction "<query>" [--limit <limit>] -f json`<br>Search Trip.com attractions and experiences by destination keyword | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `car` | `private_content_read` / `medium` | `opencli trip car "<city>" [--limit <limit>] -f json`<br>List Trip.com car-rental vehicles for a city (category, model, seats, daily price) | `city` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `deals` | `private_content_read` / `medium` | `opencli trip deals [--limit <limit>] -f json`<br>List Trip.com live promotions from the Top Deals hub: campaign title, offer, discount, and link | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `flight` | `private_content_read` / `medium` | `opencli trip flight "<from>" "<to>" --date "<date>" [--limit <limit>] -f json`<br>Search Trip.com one-way flights by IATA route + departure date | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `flight-round` | `private_content_read` / `medium` | `opencli trip flight-round "<from>" "<to>" --depart "<depart>" --return "<return>" [--limit <limit>] -f json`<br>Search Trip.com round-trip flights by IATA route + depart/return dates | `from` (str, required, positional); `to` (str, required, positional); `depart` (str, required); `return` (str, required); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `hotel` | `private_content_read` / `medium` | `opencli trip hotel "<id>" -f json`<br>Show a Trip.com hotel detail by id (rating breakdown, amenities, check-in/out policy) | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `hotel-search` | `private_content_read` / `medium` | `opencli trip hotel-search "<city>" --checkin "<checkin>" --checkout "<checkout>" [--limit <limit>] -f json`<br>List Trip.com hotels for a city id + check-in/out date range | `city` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `tour` | `private_content_read` / `medium` | `opencli trip tour "<query>" [--type "<type>"] [--limit <limit>] -f json`<br>Search Trip.com tour packages by destination keyword (private or group tours) | `query` (str, required, positional); `type` (str, optional, default='private'); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `train` | `private_content_read` / `medium` | `opencli trip train "<from>" "<to>" --country "<country>" [--limit <limit>] -f json`<br>Show a Trip.com train route timetable (departure/arrival times, duration, changes) | `from` (str, required, positional); `to` (str, required, positional); `country` (str, required); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `transfer` | `private_content_read` / `medium` | `opencli trip transfer "<city>" "<airport>" [--limit <limit>] -f json`<br>List Trip.com airport-transfer vehicles for a city + airport (type, seats, from-price) | `city` (str, required, positional); `airport` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `attraction`: sensitive output: private content, account identifiers
- `car`: sensitive output: private content, account identifiers
- `deals`: sensitive output: private content, account identifiers
- `flight`: sensitive output: private content, account identifiers
- `flight-round`: sensitive output: private content, account identifiers
- `hotel`: sensitive output: private content, account identifiers
- `hotel-search`: sensitive output: private content, account identifiers
- `tour`: sensitive output: private content, account identifiers
- `train`: sensitive output: private content, account identifiers
- `transfer`: sensitive output: private content, account identifiers
