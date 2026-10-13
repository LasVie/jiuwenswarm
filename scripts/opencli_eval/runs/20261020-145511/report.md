# OpenCLI M4 evaluation

Manifest: `/mnt/d/Job/Huawei/LasVie/jiuwenswarm/scripts/opencli_eval/runs/20261020-145511/manifest.jsonl`. Runs: 38. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| browser | browser | 19 | 18/19 | 44.1 | 3 | 153053 | 0.287 | 0 | 16/19 | 0 | 61 |
| hybrid | hybrid | 19 | 18/19 | 41.5 | 3 | 138055 | 0.296 | 23 | 17/19 | 1 | 47 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | browser | 3 | 3/3 | 44.1 | 3 | 160328 | 0.362 | 0 | 3/3 | 0 | 10 |
| hit | hybrid | 3 | 3/3 | 37.1 | 3 | 138055 | 0.383 | 3 | 3/3 | 0 | 10 |
| list | browser | 2 | 2/2 | 42.8 | 4.0 | 161482 | 0.363 | 0 | 2/2 | 0 | 5 |
| list | hybrid | 2 | 2/2 | 38.0 | 4.0 | 168614 | 0.349 | 3 | 2/2 | 0 | 3 |
| login | browser | 1 | 0/1 | 69.6 | 6 | 188362 | 0.392 | 0 | 1/1 | 0 | 1 |
| login | hybrid | 1 | 0/1 | 29.1 | 2 | 113823 | 0.181 | 2 | 1/1 | 1 | 0 |
| miss | browser | 2 | 2/2 | 29.1 | 2.5 | 116156 | 0.197 | 0 | 2/2 | 0 | 8 |
| miss | hybrid | 2 | 2/2 | 43.0 | 4.0 | 153736 | 0.278 | 0 | 2/2 | 0 | 7 |
| multi_step | browser | 2 | 2/2 | 46.9 | 3.0 | 197257 | 0.306 | 0 | 2/2 | 0 | 8 |
| multi_step | hybrid | 2 | 2/2 | 42.1 | 3.5 | 144025 | 0.265 | 6 | 2/2 | 0 | 3 |
| no_browser | browser | 4 | 4/4 | 45.0 | 4.5 | 157074 | 0.323 | 0 | 4/4 | 0 | 24 |
| no_browser | hybrid | 4 | 4/4 | 48.8 | 4.5 | 178246 | 0.352 | 5 | 4/4 | 0 | 20 |
| partial | browser | 2 | 2/2 | 77.0 | 7.0 | 207874 | 0.449 | 0 | 2/2 | 0 | 5 |
| partial | hybrid | 2 | 2/2 | 60.0 | 6.5 | 211306 | 0.405 | 2 | 2/2 | 0 | 4 |
| routing | browser | 3 | 3/3 | 12.1 | 0 | 76641 | 0.097 | 0 | 0/3 | 0 | 0 |
| routing | hybrid | 3 | 3/3 | 15.8 | 0 | 112799 | 0.109 | 2 | 1/3 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-arxiv-search | browser | 1 | 1/1 | 44.8 | 3 | 183850 | 0.362 | 0 | 1/1 | 0 | 6 |
| hit-arxiv-search | hybrid | 1 | 1/1 | 50.2 | 4 | 204489 | 0.383 | 1 | 1/1 | 0 | 5 |
| hit-bilibili-hot | browser | 1 | 1/1 | 44.1 | 4 | 160328 | 0.519 | 0 | 1/1 | 0 | 0 |
| hit-bilibili-hot | hybrid | 1 | 1/1 | 36.7 | 3 | 138055 | 0.433 | 2 | 1/1 | 0 | 1 |
| hit-github-trending | browser | 1 | 1/1 | 39.5 | 3 | 129044 | 0.249 | 0 | 1/1 | 0 | 4 |
| hit-github-trending | hybrid | 1 | 1/1 | 37.1 | 3 | 134262 | 0.250 | 0 | 1/1 | 0 | 4 |
| hit-hackernews-top | browser | 1 | 1/1 | 31.4 | 3 | 129953 | 0.253 | 0 | 1/1 | 0 | 10 |
| hit-hackernews-top | hybrid | 1 | 1/1 | 35.4 | 3 | 136332 | 0.258 | 0 | 1/1 | 0 | 10 |
| list-bilibili-search | browser | 1 | 1/1 | 46.8 | 5 | 195176 | 0.487 | 0 | 1/1 | 0 | 0 |
| list-bilibili-search | hybrid | 1 | 1/1 | 47.8 | 5 | 204053 | 0.462 | 1 | 1/1 | 0 | 3 |
| list-v2ex-hot | browser | 1 | 1/1 | 38.7 | 3 | 127788 | 0.239 | 0 | 1/1 | 0 | 5 |
| list-v2ex-hot | hybrid | 1 | 1/1 | 28.1 | 3 | 133176 | 0.237 | 2 | 1/1 | 0 | 0 |
| login-zhihu-search | browser | 1 | 0/1 | 69.6 | 6 | 188362 | 0.392 | 0 | 1/1 | 0 | 1 |
| login-zhihu-search | hybrid | 1 | 0/1 | 29.1 | 2 | 113823 | 0.181 | 2 | 1/1 | 1 | 0 |
| miss-example-page | browser | 1 | 1/1 | 19.1 | 2 | 101831 | 0.135 | 0 | 1/1 | 0 | 1 |
| miss-example-page | hybrid | 1 | 1/1 | 18.9 | 2 | 103756 | 0.126 | 0 | 1/1 | 0 | 1 |
| miss-ithome | browser | 1 | 1/1 | 39.1 | 3 | 130480 | 0.260 | 0 | 1/1 | 0 | 7 |
| miss-ithome | hybrid | 1 | 1/1 | 67.1 | 6 | 203715 | 0.430 | 0 | 1/1 | 0 | 6 |
| multistep-bilibili | browser | 1 | 1/1 | 44.7 | 4 | 153053 | 0.325 | 0 | 1/1 | 0 | 2 |
| multistep-bilibili | hybrid | 1 | 1/1 | 41.5 | 4 | 158617 | 0.296 | 2 | 1/1 | 0 | 0 |
| multistep-compare | browser | 1 | 1/1 | 49.0 | 2 | 241461 | 0.287 | 0 | 1/1 | 0 | 6 |
| multistep-compare | hybrid | 1 | 1/1 | 42.8 | 3 | 129433 | 0.233 | 4 | 1/1 | 0 | 3 |
| nobrowser-crates | browser | 1 | 1/1 | 27.8 | 3 | 122883 | 0.206 | 0 | 1/1 | 0 | 6 |
| nobrowser-crates | hybrid | 1 | 1/1 | 43.3 | 4 | 160754 | 0.317 | 0 | 1/1 | 0 | 5 |
| nobrowser-stackoverflow | browser | 1 | 1/1 | 58.6 | 6 | 184195 | 0.394 | 0 | 1/1 | 0 | 5 |
| nobrowser-stackoverflow | hybrid | 1 | 1/1 | 58.6 | 5 | 237978 | 0.485 | 1 | 1/1 | 0 | 5 |
| nobrowser-wikipedia | browser | 1 | 1/1 | 67.0 | 6 | 198970 | 0.468 | 0 | 1/1 | 0 | 3 |
| nobrowser-wikipedia | hybrid | 1 | 1/1 | 54.4 | 6 | 195738 | 0.387 | 4 | 1/1 | 0 | 0 |
| partial-bilibili-detail | browser | 1 | 1/1 | 99.2 | 9 | 247653 | 0.533 | 0 | 1/1 | 0 | 1 |
| partial-bilibili-detail | hybrid | 1 | 1/1 | 71.3 | 8 | 252739 | 0.488 | 2 | 1/1 | 0 | 1 |
| partial-hackernews-comments | browser | 1 | 1/1 | 54.8 | 5 | 168094 | 0.364 | 0 | 1/1 | 0 | 4 |
| partial-hackernews-comments | hybrid | 1 | 1/1 | 48.6 | 5 | 169872 | 0.322 | 0 | 1/1 | 0 | 3 |
| routing-bilibili | browser | 1 | 1/1 | 12.1 | 0 | 76641 | 0.097 | 0 | 0/1 | 0 | 0 |
| routing-bilibili | hybrid | 1 | 1/1 | 28.5 | 3 | 135645 | 0.239 | 2 | 1/1 | 0 | 0 |
| routing-hackernews | browser | 1 | 1/1 | 14.3 | 0 | 112494 | 0.108 | 0 | 0/1 | 0 | 0 |
| routing-hackernews | hybrid | 1 | 1/1 | 15.8 | 0 | 112799 | 0.109 | 0 | 0/1 | 0 | 0 |
| routing-wikipedia | browser | 1 | 1/1 | 8.3 | 0 | 75143 | 0.086 | 0 | 0/1 | 0 | 0 |
| routing-wikipedia | hybrid | 1 | 1/1 | 9.5 | 0 | 76010 | 0.088 | 0 | 0/1 | 0 | 0 |
