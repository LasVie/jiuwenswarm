# OpenCLI M4 evaluation

Manifest: `scripts/opencli_eval/runs/20261020-160735/manifest.jsonl`. Runs: 4. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid | hybrid | 4 | 4/4 | 45.2 | 5.5 | 187833 | 0.447 | 2 | 4/4 | 0 | 13 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | hybrid | 1 | 1/1 | 36.6 | 3 | 135317 | 0.252 | 0 | 1/1 | 0 | 4 |
| no_browser | hybrid | 2 | 2/2 | 45.2 | 5.5 | 187833 | 0.447 | 2 | 2/2 | 0 | 6 |
| partial | hybrid | 1 | 1/1 | 80.6 | 9 | 260853 | 0.543 | 0 | 1/1 | 0 | 3 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-github-trending | hybrid | 1 | 1/1 | 36.6 | 3 | 135317 | 0.252 | 0 | 1/1 | 0 | 4 |
| hit-hackernews-top | hybrid | 1 | 1/1 | 38.5 | 3 | 135511 | 0.421 | 2 | 1/1 | 0 | 0 |
| nobrowser-crates | hybrid | 1 | 1/1 | 52.0 | 8 | 240155 | 0.472 | 0 | 1/1 | 0 | 6 |
| partial-hackernews-comments | hybrid | 1 | 1/1 | 80.6 | 9 | 260853 | 0.543 | 0 | 1/1 | 0 | 3 |
