# OpenCLI M4 evaluation

Manifest: `scripts/opencli_eval/runs/20261020-102708/manifest.jsonl`. Runs: 1. C2 (deferred MCP start) not enabled.

Success = the final reply passes the task's structural check (enough links on the expected domain), without timeout or driver error. Total tokens = main agent + Browser Agent.

## By arm

| arm | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid | hybrid | 1 | 1/1 | 24.8 | 0 | 113679 | 0.200 | 0 | 0/1 | 0 | 0 |

## By task group

| group | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| no_browser | hybrid | 1 | 1/1 | 24.8 | 0 | 113679 | 0.200 | 0 | 0/1 | 0 | 0 |

## By task

| task | arm | runs | success | median wall s | median browser model calls | median total tokens | median cost | OpenCLI calls | delegated first | needs_user | unbacked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hit-hackernews-top | hybrid | 1 | 1/1 | 24.8 | 0 | 113679 | 0.200 | 0 | 0/1 | 0 | 0 |
