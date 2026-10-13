# OpenCLI M4 evaluation

Manifest: `scripts/opencli_eval/runs/20261020-105408/manifest.jsonl`. Runs: 2. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| browser | browser | 1 | 1/1 | 35.6 | 4 | 144570 | 0.400 | 0 | 1/1 | 0 | 5 |
| hybrid | hybrid | 1 | 1/1 | 39.4 | 4 | 151118 | 0.400 | 2 | 1/1 | 0 | 0 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | browser | 1 | 1/1 | 35.6 | 4 | 144570 | 0.400 | 0 | 1/1 | 0 | 5 |
| hit | hybrid | 1 | 1/1 | 39.4 | 4 | 151118 | 0.400 | 2 | 1/1 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-bilibili-hot | browser | 1 | 1/1 | 35.6 | 4 | 144570 | 0.400 | 0 | 1/1 | 0 | 5 |
| hit-bilibili-hot | hybrid | 1 | 1/1 | 39.4 | 4 | 151118 | 0.400 | 2 | 1/1 | 0 | 0 |
