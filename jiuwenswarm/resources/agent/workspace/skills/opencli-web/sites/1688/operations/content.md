# 1688: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `assets` | `public_read` / `low` | `opencli 1688 assets "<input>" -f json`<br>列出 1688 商品页可提取的图片/视频素材 | `input` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `item` | `public_read` / `low` | `opencli 1688 item "<input>" -f json`<br>1688 商品详情（公开商品字段、价格阶梯、卖家基础信息） | `input` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `store` | `public_read` / `low` | `opencli 1688 store "<input>" -f json`<br>1688 店铺/供应商公开信息（联系方式、主营、入驻年限、公开服务信号） | `input` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `assets`: Source-audited against OpenCLI 1.8.6 1688/assets.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `item`: Source-audited against OpenCLI 1.8.6 1688/item.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `store`: Source-audited against OpenCLI 1.8.6 1688/store.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
