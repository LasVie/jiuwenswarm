# 1688: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli 1688 download "<input>" [--output "<output>"] -f json`<br>批量下载 1688 商品页可提取的图片和视频素材 | `input` (str, required, positional); `output` (str, optional, default='./1688-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
