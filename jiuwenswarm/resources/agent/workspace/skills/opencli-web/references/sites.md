# M1 site capability map

Load exactly one matching site skill after `opencli-web`.

| Website | M1 operations | Site skill |
|---|---|---|
| Xiaohongshu / 小红书 (`creator.xiaohongshu.com`) | Create an image/text note draft; publish the confirmed note | `opencli-xiaohongshu` |

Everything else is unsupported by M1, even if the locally installed OpenCLI
catalog contains an adapter. Investigate catalog entries with `opencli list -f
json`, but add and test a dedicated site skill before routing production work to
them.
