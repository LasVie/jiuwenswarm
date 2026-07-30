# 12306: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `price` | `public_read` / `low` | `opencli 12306 price "<train-no>" --from "<from>" --to "<to>" --date "<date>" [--seat-types "<seat-types>"] -f json`<br>Look up 12306 ticket prices by seat class for one train on a given date and segment (anonymous, no login required) | `train-no` (str, required, positional); `from` (str, required); `to` (str, required); `date` (str, required); `seat-types` (str, optional, default='OM9PA1A3A4FWZ') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `stations` | `public_read` / `low` | `opencli 12306 stations "<keyword>" [--limit <limit>] -f json`<br>Search 12306 (China Railway) stations by Chinese name, telecode, or pinyin keyword | `keyword` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `train` | `public_read` / `low` | `opencli 12306 train "<train-no>" --from "<from>" --to "<to>" --date "<date>" -f json`<br>List every station a 12306 train calls at, with arrival / departure / stopover time (anonymous, no login required) | `train-no` (str, required, positional); `from` (str, required); `to` (str, required); `date` (str, required) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trains` | `public_read` / `low` | `opencli 12306 trains "<from>" "<to>" --date "<date>" [--limit <limit>] -f json`<br>List trains between two 12306 stations on a given date (anonymous, no login required) | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=50) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
