# OpenCLI M4 evaluation

Manifest: `/mnt/d/Job/Huawei/LasVie/jiuwenswarm/scripts/opencli_eval/runs/20261020-162609/manifest.jsonl`. Runs: 4. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid | hybrid | 4 | 4/4 | 32.0 | 3.0 | 134292 | 0.327 | 9 | 4/4 | 0 | 3 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | hybrid | 1 | 1/1 | 32.2 | 3 | 133491 | 0.239 | 2 | 1/1 | 0 | 1 |
| no_browser | hybrid | 2 | 2/2 | 29.5 | 3.0 | 133494 | 0.319 | 4 | 2/2 | 0 | 1 |
| partial | hybrid | 1 | 1/1 | 54.4 | 6 | 202249 | 0.414 | 3 | 1/1 | 0 | 1 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-github-trending | hybrid | 1 | 1/1 | 32.2 | 3 | 133491 | 0.239 | 2 | 1/1 | 0 | 1 |
| hit-hackernews-top | hybrid | 1 | 1/1 | 31.8 | 3 | 135093 | 0.417 | 2 | 1/1 | 0 | 0 |
| nobrowser-crates | hybrid | 1 | 1/1 | 27.2 | 3 | 131894 | 0.220 | 2 | 1/1 | 0 | 1 |
| partial-hackernews-comments | hybrid | 1 | 1/1 | 54.4 | 6 | 202249 | 0.414 | 3 | 1/1 | 0 | 1 |
