# OpenCLI M4 evaluation

Manifest: `/mnt/d/Job/Huawei/LasVie/jiuwenswarm/scripts/opencli_eval/runs/20261020-163229/manifest.jsonl`. Runs: 38. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| browser | browser | 19 | 19/19 | 40.2 | 3 | 132692 | 0.273 | 0 | 16/19 | 0 | 72 |
| hybrid | hybrid | 19 | 18/19 | 33.1 | 3 | 137606 | 0.257 | 42 | 17/19 | 1 | 35 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | browser | 3 | 3/3 | 36.7 | 3 | 128850 | 0.317 | 0 | 3/3 | 0 | 16 |
| hit | hybrid | 3 | 3/3 | 35.7 | 3 | 141457 | 0.395 | 6 | 3/3 | 0 | 7 |
| list | browser | 2 | 2/2 | 50.9 | 4.5 | 168608 | 0.382 | 0 | 2/2 | 0 | 10 |
| list | hybrid | 2 | 2/2 | 28.2 | 3.0 | 133243 | 0.229 | 4 | 2/2 | 0 | 0 |
| login | browser | 1 | 1/1 | 79.0 | 7 | 219632 | 0.513 | 0 | 1/1 | 0 | 6 |
| login | hybrid | 1 | 0/1 | 24.3 | 2 | 114486 | 0.182 | 2 | 1/1 | 1 | 0 |
| miss | browser | 2 | 2/2 | 36.0 | 3.0 | 124920 | 0.222 | 0 | 2/2 | 0 | 8 |
| miss | hybrid | 2 | 2/2 | 33.5 | 2.5 | 121986 | 0.201 | 0 | 2/2 | 0 | 9 |
| multi_step | browser | 2 | 2/2 | 53.1 | 5.0 | 160952 | 0.321 | 0 | 2/2 | 0 | 8 |
| multi_step | hybrid | 2 | 2/2 | 41.0 | 3.5 | 150580 | 0.292 | 6 | 2/2 | 0 | 3 |
| no_browser | browser | 4 | 4/4 | 51.5 | 4.5 | 161684 | 0.347 | 0 | 4/4 | 0 | 18 |
| no_browser | hybrid | 4 | 4/4 | 44.1 | 4.5 | 174368 | 0.355 | 17 | 4/4 | 0 | 15 |
| partial | browser | 2 | 2/2 | 58.0 | 5.0 | 172041 | 0.367 | 0 | 2/2 | 0 | 6 |
| partial | hybrid | 2 | 2/2 | 58.4 | 5.5 | 191852 | 0.379 | 5 | 2/2 | 0 | 1 |
| routing | browser | 3 | 3/3 | 12.2 | 0 | 76705 | 0.099 | 0 | 0/3 | 0 | 0 |
| routing | hybrid | 3 | 3/3 | 15.7 | 0 | 112893 | 0.108 | 2 | 1/3 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-arxiv-search | browser | 1 | 1/1 | 40.2 | 3 | 140307 | 0.317 | 0 | 1/1 | 0 | 5 |
| hit-arxiv-search | hybrid | 1 | 1/1 | 96.9 | 5 | 183884 | 0.395 | 2 | 1/1 | 0 | 6 |
| hit-bilibili-hot | browser | 1 | 1/1 | 35.4 | 3 | 120224 | 0.365 | 0 | 1/1 | 0 | 6 |
| hit-bilibili-hot | hybrid | 1 | 1/1 | 35.7 | 3 | 141457 | 0.446 | 2 | 1/1 | 0 | 0 |
| hit-github-trending | browser | 1 | 1/1 | 36.7 | 3 | 128850 | 0.250 | 0 | 1/1 | 0 | 5 |
| hit-github-trending | hybrid | 1 | 1/1 | 33.1 | 3 | 127751 | 0.212 | 2 | 1/1 | 0 | 1 |
| hit-hackernews-top | browser | 1 | 1/1 | 34.5 | 3 | 128340 | 0.239 | 0 | 1/1 | 0 | 5 |
| hit-hackernews-top | hybrid | 1 | 1/1 | 32.4 | 3 | 136812 | 0.255 | 2 | 1/1 | 0 | 10 |
| list-bilibili-search | browser | 1 | 1/1 | 65.5 | 6 | 208614 | 0.518 | 0 | 1/1 | 0 | 4 |
| list-bilibili-search | hybrid | 1 | 1/1 | 27.8 | 3 | 138227 | 0.252 | 2 | 1/1 | 0 | 0 |
| list-v2ex-hot | browser | 1 | 1/1 | 36.2 | 3 | 128602 | 0.246 | 0 | 1/1 | 0 | 6 |
| list-v2ex-hot | hybrid | 1 | 1/1 | 28.7 | 3 | 128259 | 0.206 | 2 | 1/1 | 0 | 0 |
| login-zhihu-search | browser | 1 | 1/1 | 79.0 | 7 | 219632 | 0.513 | 0 | 1/1 | 0 | 6 |
| login-zhihu-search | hybrid | 1 | 0/1 | 24.3 | 2 | 114486 | 0.182 | 2 | 1/1 | 1 | 0 |
| miss-example-page | browser | 1 | 1/1 | 28.3 | 3 | 117148 | 0.170 | 0 | 1/1 | 0 | 1 |
| miss-example-page | hybrid | 1 | 1/1 | 20.6 | 2 | 106366 | 0.137 | 0 | 1/1 | 0 | 1 |
| miss-ithome | browser | 1 | 1/1 | 43.7 | 3 | 132692 | 0.273 | 0 | 1/1 | 0 | 7 |
| miss-ithome | hybrid | 1 | 1/1 | 46.5 | 3 | 137606 | 0.265 | 0 | 1/1 | 0 | 8 |
| multistep-bilibili | browser | 1 | 1/1 | 41.7 | 4 | 135475 | 0.228 | 0 | 1/1 | 0 | 3 |
| multistep-bilibili | hybrid | 1 | 1/1 | 41.6 | 4 | 164751 | 0.322 | 2 | 1/1 | 0 | 0 |
| multistep-compare | browser | 1 | 1/1 | 64.6 | 6 | 186429 | 0.414 | 0 | 1/1 | 0 | 5 |
| multistep-compare | hybrid | 1 | 1/1 | 40.4 | 3 | 136410 | 0.263 | 4 | 1/1 | 0 | 3 |
| nobrowser-crates | browser | 1 | 1/1 | 32.3 | 3 | 125340 | 0.221 | 0 | 1/1 | 0 | 6 |
| nobrowser-crates | hybrid | 1 | 1/1 | 26.8 | 3 | 132436 | 0.226 | 2 | 1/1 | 0 | 0 |
| nobrowser-stackoverflow | browser | 1 | 1/1 | 68.4 | 6 | 195028 | 0.455 | 0 | 1/1 | 0 | 6 |
| nobrowser-stackoverflow | hybrid | 1 | 1/1 | 66.2 | 8 | 282794 | 0.682 | 7 | 1/1 | 0 | 5 |
| nobrowser-wikipedia | browser | 1 | 1/1 | 86.5 | 11 | 302791 | 0.703 | 0 | 1/1 | 0 | 1 |
| nobrowser-wikipedia | hybrid | 1 | 1/1 | 55.9 | 6 | 211925 | 0.455 | 6 | 1/1 | 0 | 0 |
| partial-bilibili-detail | browser | 1 | 1/1 | 53.4 | 5 | 176223 | 0.369 | 0 | 1/1 | 0 | 0 |
| partial-bilibili-detail | hybrid | 1 | 1/1 | 48.8 | 5 | 177069 | 0.310 | 2 | 1/1 | 0 | 0 |
| partial-hackernews-comments | browser | 1 | 1/1 | 62.6 | 5 | 167859 | 0.366 | 0 | 1/1 | 0 | 6 |
| partial-hackernews-comments | hybrid | 1 | 1/1 | 68.1 | 6 | 206634 | 0.448 | 3 | 1/1 | 0 | 1 |
| routing-bilibili | browser | 1 | 1/1 | 12.2 | 0 | 76705 | 0.099 | 0 | 0/1 | 0 | 0 |
| routing-bilibili | hybrid | 1 | 1/1 | 30.9 | 3 | 139504 | 0.257 | 2 | 1/1 | 0 | 0 |
| routing-hackernews | browser | 1 | 1/1 | 14.4 | 0 | 112215 | 0.106 | 0 | 0/1 | 0 | 0 |
| routing-hackernews | hybrid | 1 | 1/1 | 15.7 | 0 | 112893 | 0.108 | 0 | 0/1 | 0 | 0 |
| routing-wikipedia | browser | 1 | 1/1 | 8.5 | 0 | 75604 | 0.088 | 0 | 0/1 | 0 | 0 |
| routing-wikipedia | hybrid | 1 | 1/1 | 7.7 | 0 | 75992 | 0.088 | 0 | 0/1 | 0 | 0 |
