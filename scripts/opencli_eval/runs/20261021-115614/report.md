# OpenCLI M4 evaluation

Manifest: `/mnt/d/Job/Huawei/LasVie/jiuwenswarm/scripts/opencli_eval/runs/20261021-115614/manifest.jsonl`. Runs: 80. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| browser | browser | 40 | 38/40 | 70.8 | 5.5 | 153438 | 0.136 | 0 | 34/40 | 0 | 74 |
| hybrid | hybrid | 40 | 38/40 | 39.9 | 3.0 | 92094 | 0.103 | 256 | 37/40 | 2 | 16 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| chain | browser | 2 | 0/2 | 152.5 | 9.0 | 333816 | 0.326 | 0 | 2/2 | 0 | 8 |
| chain | hybrid | 2 | 2/2 | 111.0 | 6.0 | 178188 | 0.165 | 6 | 2/2 | 0 | 3 |
| hit | browser | 6 | 6/6 | 74.8 | 6.5 | 162019 | 0.182 | 0 | 6/6 | 0 | 7 |
| hit | hybrid | 6 | 6/6 | 45.8 | 3.5 | 111666 | 0.147 | 21 | 6/6 | 0 | 3 |
| list | browser | 4 | 4/4 | 85.8 | 5.0 | 179270 | 0.153 | 0 | 4/4 | 0 | 17 |
| list | hybrid | 4 | 4/4 | 32.0 | 3.0 | 90639 | 0.101 | 8 | 4/4 | 0 | 0 |
| login | browser | 2 | 2/2 | 107.8 | 12.5 | 286425 | 0.258 | 0 | 2/2 | 0 | 0 |
| login | hybrid | 2 | 1/2 | 117.5 | 2.0 | 314248 | 0.173 | 4 | 2/2 | 2 | 0 |
| miss | browser | 4 | 4/4 | 92.1 | 6.5 | 165809 | 0.104 | 0 | 4/4 | 0 | 0 |
| miss | hybrid | 4 | 4/4 | 142.2 | 3.5 | 207526 | 0.248 | 0 | 4/4 | 0 | 2 |
| multi_step | browser | 4 | 4/4 | 52.9 | 5.0 | 130988 | 0.106 | 0 | 4/4 | 0 | 12 |
| multi_step | hybrid | 4 | 4/4 | 51.8 | 3.5 | 99456 | 0.092 | 13 | 4/4 | 0 | 2 |
| no_browser | browser | 8 | 8/8 | 90.2 | 10.0 | 197790 | 0.138 | 0 | 8/8 | 0 | 29 |
| no_browser | hybrid | 8 | 8/8 | 38.5 | 5.0 | 116832 | 0.138 | 184 | 8/8 | 0 | 3 |
| partial | browser | 4 | 4/4 | 101.7 | 7.0 | 153438 | 0.144 | 0 | 4/4 | 0 | 1 |
| partial | hybrid | 4 | 3/4 | 42.2 | 4.5 | 109067 | 0.110 | 14 | 4/4 | 0 | 3 |
| routing | browser | 6 | 6/6 | 12.9 | 0.0 | 54011 | 0.057 | 0 | 0/6 | 0 | 0 |
| routing | hybrid | 6 | 6/6 | 27.8 | 1.5 | 80724 | 0.081 | 6 | 3/6 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| chain-bilibili-related | browser | 2 | 0/2 | 152.5 | 9.0 | 333816 | 0.326 | 0 | 2/2 | 0 | 8 |
| chain-bilibili-related | hybrid | 2 | 2/2 | 111.0 | 6.0 | 178188 | 0.165 | 6 | 2/2 | 0 | 3 |
| hit-arxiv-search | browser | 2 | 2/2 | 183.3 | 9.5 | 283854 | 0.276 | 0 | 2/2 | 0 | 6 |
| hit-arxiv-search | hybrid | 2 | 2/2 | 64.9 | 4.5 | 136740 | 0.171 | 14 | 2/2 | 0 | 3 |
| hit-bilibili-hot | browser | 2 | 2/2 | 49.5 | 3.5 | 99758 | 0.132 | 0 | 2/2 | 0 | 1 |
| hit-bilibili-hot | hybrid | 2 | 2/2 | 37.4 | 3.0 | 92990 | 0.111 | 4 | 2/2 | 0 | 0 |
| hit-github-trending | browser | 2 | 2/2 | 74.8 | 6.5 | 181512 | 0.182 | 0 | 2/2 | 0 | 0 |
| hit-github-trending | hybrid | 2 | 2/2 | 38.9 | 4.5 | 117019 | 0.119 | 3 | 2/2 | 0 | 0 |
| hit-hackernews-top | browser | 2 | 2/2 | 43.2 | 4.0 | 102776 | 0.134 | 0 | 2/2 | 0 | 15 |
| hit-hackernews-top | hybrid | 2 | 2/2 | 30.2 | 3.0 | 87872 | 0.101 | 4 | 2/2 | 0 | 0 |
| list-bilibili-search | browser | 2 | 2/2 | 131.8 | 7.5 | 209902 | 0.197 | 0 | 2/2 | 0 | 2 |
| list-bilibili-search | hybrid | 2 | 2/2 | 35.1 | 3.0 | 92094 | 0.104 | 4 | 2/2 | 0 | 0 |
| list-v2ex-hot | browser | 2 | 2/2 | 43.1 | 3.5 | 144794 | 0.132 | 0 | 2/2 | 0 | 15 |
| list-v2ex-hot | hybrid | 2 | 2/2 | 28.9 | 3.0 | 88338 | 0.092 | 4 | 2/2 | 0 | 0 |
| login-zhihu-search | browser | 2 | 2/2 | 107.8 | 12.5 | 286425 | 0.258 | 0 | 2/2 | 0 | 0 |
| login-zhihu-search | hybrid | 2 | 1/2 | 117.5 | 2.0 | 314248 | 0.173 | 4 | 2/2 | 2 | 0 |
| miss-example-page | browser | 2 | 2/2 | 28.8 | 3.5 | 121753 | 0.085 | 0 | 2/2 | 0 | 0 |
| miss-example-page | hybrid | 2 | 2/2 | 17.2 | 2.0 | 70702 | 0.057 | 0 | 2/2 | 0 | 2 |
| miss-ithome | browser | 2 | 2/2 | 206.7 | 8.5 | 190190 | 0.112 | 0 | 2/2 | 0 | 0 |
| miss-ithome | hybrid | 2 | 2/2 | 354.1 | 8.5 | 411354 | 0.459 | 0 | 2/2 | 0 | 0 |
| multistep-bilibili | browser | 2 | 2/2 | 52.4 | 5.0 | 130988 | 0.121 | 0 | 2/2 | 0 | 0 |
| multistep-bilibili | hybrid | 2 | 2/2 | 56.0 | 4.5 | 119756 | 0.107 | 5 | 2/2 | 0 | 2 |
| multistep-compare | browser | 2 | 2/2 | 70.2 | 6.0 | 134272 | 0.100 | 0 | 2/2 | 0 | 12 |
| multistep-compare | hybrid | 2 | 2/2 | 44.6 | 3.0 | 87730 | 0.085 | 8 | 2/2 | 0 | 0 |
| nobrowser-crates | browser | 2 | 2/2 | 64.3 | 5.5 | 114553 | 0.104 | 0 | 2/2 | 0 | 9 |
| nobrowser-crates | hybrid | 2 | 2/2 | 29.2 | 3.0 | 86505 | 0.084 | 4 | 2/2 | 0 | 0 |
| nobrowser-stackoverflow | browser | 2 | 2/2 | 217.9 | 21.0 | 611873 | 0.607 | 0 | 2/2 | 0 | 5 |
| nobrowser-stackoverflow | hybrid | 2 | 2/2 | 298.8 | 38.5 | 1554650 | 1.093 | 162 | 2/2 | 0 | 2 |
| nobrowser-wikipedia | browser | 2 | 2/2 | 131.4 | 14.5 | 297755 | 0.163 | 0 | 2/2 | 0 | 0 |
| nobrowser-wikipedia | hybrid | 2 | 2/2 | 62.2 | 7.5 | 153330 | 0.154 | 14 | 2/2 | 0 | 1 |
| partial-bilibili-detail | browser | 2 | 2/2 | 61.9 | 6.0 | 131790 | 0.106 | 0 | 2/2 | 0 | 1 |
| partial-bilibili-detail | hybrid | 2 | 2/2 | 46.0 | 4.0 | 109067 | 0.118 | 6 | 2/2 | 0 | 2 |
| partial-hackernews-comments | browser | 2 | 2/2 | 134.9 | 12.0 | 388352 | 0.285 | 0 | 2/2 | 0 | 0 |
| partial-hackernews-comments | hybrid | 2 | 1/2 | 41.5 | 5.0 | 109102 | 0.082 | 8 | 2/2 | 0 | 1 |
| routing-bilibili | browser | 2 | 2/2 | 24.1 | 0.0 | 108938 | 0.101 | 0 | 0/2 | 0 | 0 |
| routing-bilibili | hybrid | 2 | 2/2 | 37.6 | 3.0 | 86478 | 0.081 | 4 | 2/2 | 0 | 0 |
| routing-hackernews | browser | 2 | 2/2 | 13.1 | 0.0 | 64908 | 0.074 | 0 | 0/2 | 0 | 0 |
| routing-hackernews | hybrid | 2 | 2/2 | 28.1 | 1.5 | 81298 | 0.099 | 2 | 1/2 | 0 | 0 |
| routing-wikipedia | browser | 2 | 2/2 | 11.3 | 0.0 | 54011 | 0.057 | 0 | 0/2 | 0 | 0 |
| routing-wikipedia | hybrid | 2 | 2/2 | 13.8 | 0.0 | 54203 | 0.074 | 0 | 0/2 | 0 | 0 |
