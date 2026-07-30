# Xiaohongshu: drafts

Read or change local or remote draft state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `draft-clear` | `destructive_or_admin` / `critical` | `opencli xiaohongshu draft-clear [--type "<type>"] [--execute <true\|false>] -f json`<br>清空小红书本地草稿 | `type` (str, optional, default='image'); `execute` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `draft-delete` | `destructive_or_admin` / `critical` | `opencli xiaohongshu draft-delete "<id>" [--type "<type>"] [--execute <true\|false>] -f json`<br>删除一条小红书本地草稿 | `id` (str, required, positional); `type` (str, optional, default='image'); `execute` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `draft-open` | `private_content_read` / `medium` | `opencli xiaohongshu draft-open "<id>" [--type "<type>"] -f json`<br>读取一条小红书本地草稿详情 | `id` (str, required, positional); `type` (str, optional, default='image') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `drafts` | `private_content_read` / `medium` | `opencli xiaohongshu drafts [--type "<type>"] -f json`<br>小红书本地草稿箱列表 | `type` (str, optional, default='image') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `draft-open`: sensitive output: private content, account identifiers
- `drafts`: sensitive output: private content, account identifiers
