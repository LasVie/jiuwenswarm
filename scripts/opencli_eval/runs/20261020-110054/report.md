# OpenCLI M4 evaluation

Manifest: `scripts/opencli_eval/runs/20261020-110054/manifest.jsonl`. Runs: 76. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| browser | browser | 38 | 36/38 | 41.1 | 3.0 | 145914 | 0.308 | 0 | 32/38 | 0 | 126 |
| hybrid | hybrid | 38 | 36/38 | 43.4 | 5.0 | 161263 | 0.306 | 64 | 34/38 | 2 | 96 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | browser | 6 | 6/6 | 35.0 | 3.0 | 131686 | 0.268 | 0 | 6/6 | 0 | 25 |
| hit | hybrid | 6 | 6/6 | 35.7 | 4.0 | 150545 | 0.290 | 9 | 6/6 | 0 | 21 |
| list | browser | 4 | 4/4 | 42.4 | 4.0 | 161400 | 0.366 | 0 | 4/4 | 0 | 16 |
| list | hybrid | 4 | 4/4 | 48.0 | 5.0 | 187996 | 0.413 | 6 | 4/4 | 0 | 10 |
| login | browser | 2 | 0/2 | 60.2 | 5.0 | 172273 | 0.373 | 0 | 2/2 | 0 | 2 |
| login | hybrid | 2 | 0/2 | 28.5 | 3.0 | 120990 | 0.166 | 6 | 2/2 | 2 | 0 |
| miss | browser | 4 | 4/4 | 31.1 | 3.0 | 127996 | 0.236 | 0 | 4/4 | 0 | 15 |
| miss | hybrid | 4 | 4/4 | 38.4 | 3.5 | 151224 | 0.265 | 0 | 4/4 | 0 | 15 |
| multi_step | browser | 4 | 4/4 | 49.9 | 4.5 | 189448 | 0.340 | 0 | 4/4 | 0 | 16 |
| multi_step | hybrid | 4 | 4/4 | 45.0 | 5.0 | 171343 | 0.317 | 17 | 4/4 | 0 | 6 |
| no_browser | browser | 8 | 8/8 | 41.5 | 4.5 | 177734 | 0.350 | 0 | 8/8 | 0 | 44 |
| no_browser | hybrid | 8 | 8/8 | 67.8 | 6.0 | 200762 | 0.426 | 9 | 8/8 | 0 | 40 |
| partial | browser | 4 | 4/4 | 54.1 | 5.5 | 174880 | 0.369 | 0 | 4/4 | 0 | 8 |
| partial | hybrid | 4 | 4/4 | 51.9 | 5.5 | 180469 | 0.358 | 9 | 4/4 | 0 | 4 |
| routing | browser | 6 | 6/6 | 12.5 | 0.0 | 76399 | 0.097 | 0 | 0/6 | 0 | 0 |
| routing | hybrid | 6 | 6/6 | 18.2 | 0.0 | 114145 | 0.114 | 8 | 2/6 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-arxiv-search | browser | 2 | 2/2 | 53.6 | 3.0 | 161956 | 0.340 | 0 | 2/2 | 0 | 11 |
| hit-arxiv-search | hybrid | 2 | 2/2 | 69.0 | 4.5 | 192533 | 0.386 | 3 | 2/2 | 0 | 13 |
| hit-bilibili-hot | browser | 2 | 2/2 | 33.4 | 3.0 | 130660 | 0.334 | 0 | 2/2 | 0 | 5 |
| hit-bilibili-hot | hybrid | 2 | 2/2 | 35.4 | 4.5 | 152839 | 0.336 | 6 | 2/2 | 0 | 0 |
| hit-github-trending | browser | 2 | 2/2 | 35.0 | 3.0 | 128566 | 0.247 | 0 | 2/2 | 0 | 9 |
| hit-github-trending | hybrid | 2 | 2/2 | 34.0 | 3.0 | 132706 | 0.243 | 0 | 2/2 | 0 | 8 |
| hit-hackernews-top | browser | 2 | 2/2 | 35.5 | 3.0 | 131718 | 0.266 | 0 | 2/2 | 0 | 20 |
| hit-hackernews-top | hybrid | 2 | 2/2 | 36.6 | 3.0 | 134758 | 0.260 | 0 | 2/2 | 0 | 20 |
| list-bilibili-search | browser | 2 | 2/2 | 50.4 | 5.0 | 199746 | 0.514 | 0 | 2/2 | 0 | 5 |
| list-bilibili-search | hybrid | 2 | 2/2 | 51.3 | 5.5 | 201572 | 0.456 | 3 | 2/2 | 0 | 3 |
| list-v2ex-hot | browser | 2 | 2/2 | 34.2 | 3.0 | 127756 | 0.239 | 0 | 2/2 | 0 | 11 |
| list-v2ex-hot | hybrid | 2 | 2/2 | 45.9 | 5.0 | 176754 | 0.351 | 3 | 2/2 | 0 | 7 |
| login-zhihu-search | browser | 2 | 0/2 | 60.2 | 5.0 | 172273 | 0.373 | 0 | 2/2 | 0 | 2 |
| login-zhihu-search | hybrid | 2 | 0/2 | 28.5 | 3.0 | 120990 | 0.166 | 6 | 2/2 | 2 | 0 |
| miss-example-page | browser | 2 | 2/2 | 22.9 | 2.5 | 109375 | 0.154 | 0 | 2/2 | 0 | 2 |
| miss-example-page | hybrid | 2 | 2/2 | 28.6 | 3.5 | 147904 | 0.188 | 0 | 2/2 | 0 | 3 |
| miss-ithome | browser | 2 | 2/2 | 41.5 | 3.5 | 152884 | 0.351 | 0 | 2/2 | 0 | 13 |
| miss-ithome | hybrid | 2 | 2/2 | 44.0 | 3.5 | 151224 | 0.308 | 0 | 2/2 | 0 | 12 |
| multistep-bilibili | browser | 2 | 2/2 | 45.6 | 4.5 | 158270 | 0.332 | 0 | 2/2 | 0 | 2 |
| multistep-bilibili | hybrid | 2 | 2/2 | 43.4 | 5.0 | 171343 | 0.311 | 5 | 2/2 | 0 | 0 |
| multistep-compare | browser | 2 | 2/2 | 56.1 | 3.5 | 248380 | 0.357 | 0 | 2/2 | 0 | 14 |
| multistep-compare | hybrid | 2 | 2/2 | 57.1 | 5.0 | 173438 | 0.356 | 12 | 2/2 | 0 | 6 |
| nobrowser-crates | browser | 2 | 2/2 | 31.1 | 3.5 | 162498 | 0.300 | 0 | 2/2 | 0 | 10 |
| nobrowser-crates | hybrid | 2 | 2/2 | 72.8 | 6.5 | 217598 | 0.408 | 0 | 2/2 | 0 | 11 |
| nobrowser-stackoverflow | browser | 2 | 2/2 | 55.4 | 6.0 | 205280 | 0.409 | 0 | 2/2 | 0 | 12 |
| nobrowser-stackoverflow | hybrid | 2 | 2/2 | 74.2 | 8.0 | 284453 | 0.600 | 9 | 2/2 | 0 | 6 |
| nobrowser-wikipedia | browser | 2 | 2/2 | 56.8 | 6.5 | 207028 | 0.473 | 0 | 2/2 | 0 | 2 |
| nobrowser-wikipedia | hybrid | 2 | 2/2 | 59.5 | 6.0 | 231872 | 0.496 | 0 | 2/2 | 0 | 3 |
| partial-bilibili-detail | browser | 2 | 2/2 | 49.1 | 5.5 | 171758 | 0.335 | 0 | 2/2 | 0 | 1 |
| partial-bilibili-detail | hybrid | 2 | 2/2 | 45.0 | 5.0 | 176568 | 0.337 | 5 | 2/2 | 0 | 1 |
| partial-hackernews-comments | browser | 2 | 2/2 | 59.7 | 6.0 | 186858 | 0.415 | 0 | 2/2 | 0 | 7 |
| partial-hackernews-comments | hybrid | 2 | 2/2 | 53.0 | 5.5 | 180469 | 0.358 | 4 | 2/2 | 0 | 3 |
| routing-bilibili | browser | 2 | 2/2 | 12.9 | 0.0 | 76399 | 0.097 | 0 | 0/2 | 0 | 0 |
| routing-bilibili | hybrid | 2 | 2/2 | 35.5 | 5.0 | 164158 | 0.271 | 8 | 2/2 | 0 | 0 |
| routing-hackernews | browser | 2 | 2/2 | 15.4 | 0.0 | 113788 | 0.116 | 0 | 0/2 | 0 | 0 |
| routing-hackernews | hybrid | 2 | 2/2 | 18.2 | 0.0 | 114145 | 0.114 | 0 | 0/2 | 0 | 0 |
| routing-wikipedia | browser | 2 | 2/2 | 8.1 | 0.0 | 75598 | 0.088 | 0 | 0/2 | 0 | 0 |
| routing-wikipedia | hybrid | 2 | 2/2 | 8.8 | 0.0 | 75766 | 0.087 | 0 | 0/2 | 0 | 0 |
