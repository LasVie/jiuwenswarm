# Dongchedi: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `koubei` | `public_read` / `low` | `opencli dongchedi koubei "<series_id>" [--limit <limit>] -f json`<br>懂车帝车系口碑/车主评价（评分 / 购车款型 / 点赞 / 评论 / 正文摘要） | `series_id` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `models` | `public_read` / `low` | `opencli dongchedi models "<series_id>" [--status "<status>"] -f json`<br>懂车帝车系款型列表（car_id / 名称 / 年款 / 指导价 / 经销商价 / 车主成交价） | `series_id` (str, required, positional); `status` (str, optional, default='online') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `score` | `public_read` / `low` | `opencli dongchedi score "<series_id>" -f json`<br>懂车帝车系评分（懂车分 8 维度 + 同级车均值对比） | `series_id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `series` | `public_read` / `low` | `opencli dongchedi series "<series_id>" -f json`<br>懂车帝车系概览（品牌 / 指导价 / 二手价 / 懂车分 / 销量排名 / 在售款型数） | `series_id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `specs` | `public_read` / `low` | `opencli dongchedi specs "<series_id>" -f json`<br>懂车帝车系配置概览（尺寸 / 动力 / 发动机 / 变速箱 / 四驱 / 悬挂 / 气囊） | `series_id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
