# OpenCLI M4 evaluation

Manifest: `scripts/opencli_eval/runs/20261021-111252/manifest.jsonl`. Runs: 4. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid | hybrid | 4 | 4/4 | 30.1 | 3.0 | 134876 | 0.263 | 10 | 4/4 | 0 | 3 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit | hybrid | 1 | 1/1 | 31.9 | 3 | 132230 | 0.401 | 2 | 1/1 | 0 | 0 |
| list | hybrid | 2 | 2/2 | 25.3 | 3.0 | 132274 | 0.224 | 4 | 2/2 | 0 | 0 |
| multi_step | hybrid | 1 | 1/1 | 39.3 | 3 | 137523 | 0.272 | 4 | 1/1 | 0 | 3 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-bilibili-hot | hybrid | 1 | 1/1 | 31.9 | 3 | 132230 | 0.401 | 2 | 1/1 | 0 | 0 |
| list-bilibili-search | hybrid | 1 | 1/1 | 28.3 | 3 | 137968 | 0.255 | 2 | 1/1 | 0 | 0 |
| list-v2ex-hot | hybrid | 1 | 1/1 | 22.3 | 3 | 126580 | 0.194 | 2 | 1/1 | 0 | 0 |
| multistep-compare | hybrid | 1 | 1/1 | 39.3 | 3 | 137523 | 0.272 | 4 | 1/1 | 0 | 3 |
