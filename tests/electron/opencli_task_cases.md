# OpenCLI task cases and M4 evaluation (WP11)

The task set lives in [`scripts/opencli_eval/tasks.json`](../../scripts/opencli_eval/tasks.json) so the
evaluation driver can run it unattended. Each task runs in a fresh Single Agent chat, once per arm:

- **browser**: OpenCLI off; the Browser Agent only has Playwright page tools.
- **hybrid**: OpenCLI on (site commands plus page tools).

Write commands are excluded: they would act on real accounts.

## Groups

| Group | Tasks | What it shows |
| --- | --- | --- |
| `hit` | Bilibili hot, arXiv search, GitHub trending | a command covers the whole task |
| `list` | Bilibili search, V2EX hot | "top N" lists backed by row evidence |
| `no_browser` | Hacker News, Wikipedia, crates.io, Stack Overflow | commands that need no browser page |
| `partial` | Bilibili video detail, Hacker News comments | command result handed to page tools |
| `miss` | IT之家, example.org | sites without an adapter fall back to page tools |
| `login` | Zhihu search | `needs_user` when not signed in |
| `multi_step` | three-step Bilibili, HN vs GitHub comparison | task budget and longer flows |
| `routing` | Hacker News, Bilibili, Wikipedia in natural wording | how often the main agent skips the browser |

All groups except `routing` are sent with a prefix that hands the task to the Browser Agent without
prescribing how ("Hand this task to the browser agent and let it decide how to get the data: " /
"请把这个任务交给浏览器子代理，由它决定如何获取数据："): the main agent has its own web tools
(`fetch_webpage`, `curl`) and otherwise often answers public-API tasks without the Browser Agent, which
would hide the difference between the arms. The first two M4 runs used "Use the browser to complete this
task: ", which pushed the main agent to write page-by-page delegations.

Live lists change, so each task's check is structural: the final reply must contain at least
`min_links` distinct links on `link_domain`. Read the replies in the session histories for anything
the check cannot judge.

## Running

1. Start the desktop app (built-in browser, no external Chrome path) and sign in to the sites you
   want covered, e.g. Bilibili and Zhihu.
2. Run the driver. It toggles `opencli.enabled` per arm through the same `path.set` call as the
   Settings page and restores the original value at the end:

   ```bash
   uv run python scripts/opencli_eval/run_eval.py --runs 2
   # one task, one arm, as a smoke test
   uv run python scripts/opencli_eval/run_eval.py --tasks hit-hackernews-top --arms hybrid --runs 1
   ```

3. Build the report from the printed manifest path:

   ```bash
   uv run python scripts/opencli_eval/report.py scripts/opencli_eval/runs/<timestamp>/manifest.jsonl
   ```

   `report.md` summarizes by arm, group and task; `runs.csv` holds one row per run.

## Metrics

| Metric | Source |
| --- | --- |
| success | final reply passes the structural check, no timeout or driver error |
| wall time | driver: from `chat.send` until processing stops and events go quiet |
| main-agent tokens and cost | `chat.usage_summary` in the session history |
| Browser Agent model calls, tool calls, tokens and cost | `browser_result.model_usage` (Core) |
| OpenCLI vs page tool calls | `model_usage.tool_calls_by_name` |
| delegated first | the first tool call is `task_tool` to `browser_agent` |
| `needs_user` blocks, `unbacked_items` | `browser_result` |

A run that raises an agent question (`chat.ask_user_question`) cannot be answered unattended; the
driver stops waiting and records it as `asked_user`. C2 (deferring the Playwright MCP start, WP10) is
not enabled.
