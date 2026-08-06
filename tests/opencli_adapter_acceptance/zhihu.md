# 知乎 OpenCLI Adapter 适配测试

- Adapter: `zhihu`
- Display name: 知乎（Zhihu）
- OpenCLI version: `1.8.6`
- Contract command count: 22
- Management TEST: `TEST-FUNC-004`
- Execution status: 按用户要求仅完成静态能力盘点和测试设计，未访问网站、未调用 adapter。

## 适配范围

当前合同覆盖 `www.zhihu.com`、`zhihu.com` 和 `zhuanlan.zhihu.com` 的登录与账号识别、热榜/推荐/搜索、问题与回答、回答评论、用户资料与公开内容、粉丝和关注列表、收藏夹读取、回答/评论发布、关注/赞同/收藏以及专栏文章 Markdown 导出。

没有暴露取消关注、取消赞同、取消收藏、删除回答、删除评论、编辑内容、提问、创建收藏夹、通知或私信命令。这些功能不属于当前 adapter 基础能力，写操作测试完成后不能依赖 OpenCLI 自动清理。

能力清单以本机 OpenCLI 1.8.6 的 `cli-manifest.json` 和 `clis/zhihu/*.js` 为上游事实，并与仓库 `scripts/opencli_skills/sites/zhihu.yaml` 及生成合同交叉核对。冻结 catalog、站点 policy 和生成后的 Skill 均包含相同的 22 条命令。所有命令通过浏览器 Cookie 或浏览器会话执行；做纯 OpenCLI 对比时，Browser Agent 回退必须单独记录，不能计为 OpenCLI 成功。

## 已适配能力

| 功能组 | 用户可用功能 | Adapter command | 主要参数 | 输出字段 | 认证与风险 |
|---|---|---|---|---|---|
| 登录 | 打开知乎登录流程并等待认证完成 | `login` | `timeout`，默认 300 秒 | `status`, `logged_in`, `site`, `url_token`, `name`, `uid` | 交互登录；高风险会话变更 |
| 账号 | 查看当前登录账号 | `whoami` | 无 | `logged_in`, `site`, `url_token`, `name`, `uid` | 需登录；中风险账号读取 |
| 内容发现 | 查看知乎热榜 | `hot` | `limit`，默认 20，实际数据源最多取 50 条 | `rank`, `title`, `heat`, `answers` | 登录可选；低风险公开读取 |
| 内容发现 | 查看当前账号首页推荐 | `recommend` | `limit`，默认 20、最大 1000 | `rank`, `type`, `title`, `author`, `votes`, `url` | 需登录；中风险个性化内容读取 |
| 内容发现 | 搜索全部、回答、文章或问题 | `search` | `query` 必填；`limit` 默认 10、最大 1000；`type=all/answer/article/question` | `rank`, `title`, `type`, `author`, `votes`, `url` | 登录可选；低风险公开读取 |
| 问题与回答 | 按问题 ID 读取回答，支持默认或最新排序 | `question` | 数字 `id` 必填；`limit` 默认 5、最大 1000；`sort=default/created` | `rank`, `id`, `author`, `votes`, `url`, `content` | 登录可选；低风险公开读取 |
| 问题与回答 | 按回答 ID、回答 URL 或 typed target 读取完整回答 | `answer-detail` | `id` 必填；`max-content` 默认 0，表示不截断 | `id`, `author`, `votes`, `comments`, `question_id`, `question_title`, `url`, `created_at`, `updated_at`, `content` | 登录可选；低风险公开读取 |
| 问题与回答 | 读取回答的顶层评论及部分回复 | `answer-comments` | `id` 必填；`limit` 默认 20、最大 1000；`replies-limit` 默认 3、最大 100 | `rank`, `comment_rank`, `reply_rank`, `depth`, `id`, `parent_id`, `author`, `reply_to`, `likes`, `created_at`, `url`, `content` | 登录可选；低风险公开读取 |
| 用户 | 查看用户资料和统计 | `user` | 用户 `url_token` 或个人主页 URL | `url_token`, `name`, `headline`, `followers`, `following`, `answers`, `articles`, `voteup`, `url` | 登录可选；低风险公开读取 |
| 用户 | 查看指定用户回答 | `user-answers` | 用户 token/URL；`limit` 默认 20、最大 1000 | `rank`, `question`, `votes`, `comments`, `created`, `url` | 登录可选；低风险公开读取 |
| 用户 | 查看指定用户文章 | `user-articles` | 用户 token/URL；`limit` 默认 20、最大 1000 | `rank`, `title`, `votes`, `comments`, `created`, `url` | 登录可选；低风险公开读取 |
| 用户 | 查看指定用户想法 | `pins` | 用户 token/URL；`limit` 默认 20、最大 1000 | `rank`, `excerpt`, `type`, `likes`, `comments`, `reposts`, `created`, `url` | 登录可选；低风险公开读取 |
| 用户关系 | 查看指定用户粉丝 | `followers` | 用户 token/URL；`limit` 默认 20、最大 1000 | `rank`, `name`, `url_token`, `headline`, `followers`, `url` | 登录可选；低风险公开读取 |
| 用户关系 | 查看指定用户关注的人 | `following` | 用户 token/URL；`limit` 默认 20、最大 1000 | `rank`, `name`, `url_token`, `headline`, `followers`, `url` | 登录可选；低风险公开读取 |
| 收藏夹 | 查看当前账号收藏夹 | `collections` | `limit`，默认 20；内部按最多 20 条分页 | `rank`, `title`, `item_count`, `description`, `collection_id` | 需登录；中风险私有内容读取 |
| 收藏夹 | 查看指定收藏夹内容 | `collection` | 数字收藏夹 `id`；`offset` 默认 0；`limit` 默认 20 | `rank`, `type`, `title`, `author`, `votes`, `excerpt`, `url` | 需登录；中风险私有内容读取 |
| 账号操作 | 关注用户或问题 | `follow` | 用户/问题 URL 或 typed target；必须 `execute=true` | `status`, `outcome`, `message`, `target_type`, `target` | 需登录；高风险远程写入；无取消关注命令 |
| 账号操作 | 赞同回答或文章 | `like` | 回答/文章 URL 或 typed target；必须 `execute=true` | `status`, `outcome`, `message`, `target_type`, `target` | 需登录；高风险远程写入；无取消赞同命令 |
| 账号操作 | 将回答或文章收藏到指定收藏夹 | `favorite` | 回答/文章目标；`collection` 与 `collection-id` 二选一；必须 `execute=true` | `status`, `outcome`, `message`, `target_type`, `target`, `collection_name`, `collection_id` | 需登录；高风险远程写入；无取消收藏命令 |
| 内容发布 | 回答指定问题 | `answer` | 问题 URL/typed target；正文或 UTF-8 文件二选一；必须 `execute=true` | `status`, `outcome`, `message`, `target_type`, `target`, `created_target`, `created_url`, `author_identity` | 需登录；高风险公开写入 |
| 评论发布 | 给回答或专栏文章发送顶层评论 | `comment` | 回答/文章目标；正文或 UTF-8 文件二选一；必须 `execute=true` | `status`, `outcome`, `message`, `target_type`, `target`, `author_identity`, `created_url` | 需登录；高风险消息发送；不支持回复评论 |
| 文件操作 | 将知乎专栏文章导出为 Markdown，可保存图片 | `download` | `url` 必填且仅支持 `zhuanlan.zhihu.com/p/...`；`output` 默认 `./zhihu-articles`；`download-images` 默认 false | `title`, `author`, `publish_time`, `status`, `size` | 本地写入、高风险；Jiuwen 当前合同要求登录 |

## 测试 Prompt

每条 Prompt 都应作为新任务最开始的输入。尖括号内容必须替换为专用测试对象；登录、确认或补充参数属于同一测试的后续交互，不新增 Prompt。公开发布或改变账号状态的操作必须逐项确认；由于 adapter 没有相反命令，不能承诺自动恢复关注、赞同、收藏、回答或评论状态。

### ZHIHU-P01：登录、账号、热榜与推荐

> 帮我做一次知乎登录检查，最多等 5 分钟。如果已经登录就不要切换账号，直接告诉我当前账号；如果还没登录，请打开登录页面等我完成登录。登录后分别列出知乎热榜前 5 条和首页推荐前 5 条，保留标题、作者和链接，再用几句话说说两边内容有什么不同。除了登录，只读取，不要关注、赞同、收藏或发布内容。

覆盖：`login`、`whoami`、`hot`、`recommend`。

### ZHIHU-P02：搜索、问题、回答全文与评论

> 帮我在知乎搜索“AI Agent”，只看问题类型的前 5 条结果并保留链接。选择第一条确实能打开的问题，分别列出默认排序前 5 个回答和最新发布的前 5 个回答。再从默认排序中选赞同数最高的一个，读取完整回答，并整理前 5 条一级评论；每条最多带 2 条回复。最后给我一段简短总结。整个过程只读，不要赞同、收藏、关注或评论。

覆盖：`search`（`question` 类型）、`question`（`default`、`created` 两种排序）、`answer-detail`、`answer-comments`。

### ZHIHU-P03：用户主页、内容与关注关系

> 帮我看看这个知乎用户：https://www.zhihu.com/people/vczh。先整理他的主页资料，再分别列出最近 5 个回答、5 篇文章和 5 条想法；最后各列出前 5 位粉丝和前 5 位关注的人。某一类确实没有内容就如实说明，不要猜，也不要改用普通浏览器补结果。只查看，不要关注、赞同、收藏或评论。

覆盖：`user`、`user-answers`、`user-articles`、`pins`、`followers`、`following`。

### ZHIHU-P04：我的收藏夹与收藏内容

> 帮我整理一下自己的知乎收藏夹。先列出前 10 个收藏夹，包含名称、内容数量和收藏夹 ID；再选择内容数量最多的一个，从第一条开始列出前 10 项，告诉我每项是回答、文章还是想法，并保留标题、作者和链接。整个过程只读，不要新增、移动或删除收藏内容。

覆盖：`collections`、`collection`。

### ZHIHU-P05：搜索并导出一篇专栏文章

> 帮我在知乎搜索“大模型智能体”，只列出前 5 篇文章。选择第一篇可以公开访问的知乎专栏文章，准备连同图片一起保存为 Markdown，目录用工作区下的 `downloads/zhihu-test`。先告诉我文章标题、作者、原始链接和最终保存目录，等我明确确认后只下载一次；遇到登录、权限、路径或内容访问问题就停止，不要自动换文章、重试或改用普通浏览器下载。

覆盖：`search`（`article` 类型）、`download`（自定义目录与图片下载）。

### ZHIHU-P06：关注用户与问题

> 用我准备的两个测试目标做知乎关注检查：用户是 `<测试用户主页 URL>`，问题是 `<测试问题 URL>`。先分别核对用户名称和问题标题，并说明 OpenCLI 没有自动取消关注的能力。然后分别问我是否关注这个用户、是否关注这个问题；只有得到对应的单独确认后才各执行一次。关注用户后再从我的关注列表核对一次，问题关注以命令返回结果为准。任何一步失败或结果不明确都立即停止，不要重复关注。

覆盖：`follow`（用户、问题两种目标）、`following`（用户关注结果核对）。

### ZHIHU-P07：回答与文章的赞同、收藏

> 用这些专用测试数据检查知乎的赞同和收藏：回答是 `<测试回答 URL>`，专栏文章是 `<测试专栏文章 URL>`，收藏夹名称是 `<测试收藏夹名称>`，同一个收藏夹的 ID 是 `<测试收藏夹 ID>`。先展示两个目标和收藏夹，说明 OpenCLI 没有自动取消赞同或取消收藏的能力。之后按顺序准备四项操作：赞同回答、赞同文章、按收藏夹名称收藏回答、按收藏夹 ID 收藏文章。四项都必须分别等我确认后各执行一次；收藏完成后只读检查该收藏夹是否出现对应内容。失败或状态不明确时立即停止，不要重试。

覆盖：`like`（回答、文章两种目标）、`favorite`（回答/文章及收藏夹名称/ID 两种定位）、`collection`（收藏结果核对）。

### ZHIHU-P08：发布回答与两类顶层评论

> 我准备了可以公开测试的知乎内容：问题是 `<测试问题 URL>`，专栏文章是 `<测试专栏文章 URL>`。先准备在问题下发布这段回答：“我更看重两个方面：先明确实际问题，再用小规模实验验证效果。工具本身不是目的，能稳定解决问题才有价值。”发布前展示问题和最终全文，并单独等我确认。回答成功后，准备在刚创建的回答下评论：“补充一点：落地时也要关注数据来源和隐私边界。”另外准备在测试专栏文章下评论：“这篇文章把思路梳理得很清楚，尤其是从实际场景出发的部分。”两条评论也要分别展示目标和全文、分别等我确认后只发布一次。任何一步失败或结果不明确都立即停止，不要重试；不要声称能用 OpenCLI 自动删除这些测试内容。

覆盖：`answer`、`comment`（回答、文章两种目标）及 `execute` 写入保护。

## 命令覆盖矩阵

| Command | Prompt |
|---|---|
| `login` | ZHIHU-P01 |
| `whoami` | ZHIHU-P01 |
| `hot` | ZHIHU-P01 |
| `recommend` | ZHIHU-P01 |
| `search` | ZHIHU-P02, ZHIHU-P05 |
| `question` | ZHIHU-P02 |
| `answer-detail` | ZHIHU-P02 |
| `answer-comments` | ZHIHU-P02 |
| `user` | ZHIHU-P03 |
| `user-answers` | ZHIHU-P03 |
| `user-articles` | ZHIHU-P03 |
| `pins` | ZHIHU-P03 |
| `followers` | ZHIHU-P03 |
| `following` | ZHIHU-P03, ZHIHU-P06 |
| `collections` | ZHIHU-P04 |
| `collection` | ZHIHU-P04, ZHIHU-P07 |
| `download` | ZHIHU-P05 |
| `follow` | ZHIHU-P06 |
| `like` | ZHIHU-P07 |
| `favorite` | ZHIHU-P07 |
| `answer` | ZHIHU-P08 |
| `comment` | ZHIHU-P08 |

覆盖结论：22/22 条 manifest 命令均关联至少一个真实用户风格的测试输入；`follow`、`like`、`favorite` 和 `comment` 的主要目标分支也已纳入设计。

## 静态发现的问题与建议

### 1. `download` 的 OpenCLI access metadata 没有表达本地写入

- 现象：`download.js` 注册为 `access: 'read'`，但会创建 Markdown 和可选图片文件。Jiuwen policy 已额外标为 `local_write / high`。
- 影响：只依赖 OpenCLI manifest 的调用方可能漏掉文件写入确认；纯 OpenCLI 与 Jiuwen 路径的风险行为可能不同。
- 建议：上游增加明确的本地写入语义；当前保留 Jiuwen 高风险覆盖，并用 ZHIHU-P05 验证路径展示、单次确认和失败停止。

### 2. 远程写操作没有对应回滚命令

- 现象：`follow`、`like`、`favorite`、`answer` 和 `comment` 被视为可撤销或可清理的远程动作，但 adapter 没有 `unfollow`、`unlike`、`unfavorite`、删除回答或删除评论命令。
- 影响：自动化测试不能完成状态往返；重复执行可能累积真实账号副作用。
- 建议：测试使用专用目标并逐项确认，运行后由用户在网站端人工清理；上游补充反向命令和执行后只读校验能力。

### 3. `question` 描述与输出不完全一致

- 现象：命令描述为“问题详情和回答”，但输出只有回答行，没有问题标题、描述、关注数等问题详情字段。
- 影响：模型可能根据页面或搜索结果补造问题详情，或把搜索字段误认为该命令输出。
- 建议：上游补充问题元数据，或把描述改为“问题回答列表”；ZHIHU-P02 只按实际回答字段验收。

### 4. `hot` 缺少可继续操作的 URL

- 现象：热榜仅返回排名、标题、热度和回答数，没有问题 ID 或 URL，且实现固定最多拉取 50 条。
- 影响：无法可靠地从热榜结果继续调用 `question`；请求超过 50 条也不会获得更多结果。
- 建议：输出问题 ID 和规范 URL，并明确 `limit` 上限。

### 5. `download` 的认证要求可能过严

- 现象：Jiuwen policy 将公开专栏导出标记为 `auth: required`，但 OpenCLI 实现没有显式调用登录校验，只导航并提取公开文章页面。
- 影响：公开文章下载可能被不必要的登录前置阻塞。
- 建议：用 ZHIHU-P05 动态验证匿名/登录态行为；若公开文章可稳定读取，将 policy 调整为 `auth: optional`，同时保留本地写入高风险确认。

### 6. 按名称收藏只搜索前 50 个收藏夹

- 现象：`favorite --collection` 只读取 `people/self/collections?limit=50`，不继续分页；重名时直接报歧义。
- 影响：收藏夹超过 50 个时，名称定位可能找不到真实存在的目标。
- 建议：优先使用稳定的 `collection-id`；上游补充分页。ZHIHU-P07 同时覆盖名称和 ID 两种路径。

## 用户执行时的核对项

1. 每次新任务使用对应 ZHIHU-Pxx 原文作为最开始的 Prompt，只替换尖括号测试数据。
2. 保存 trace 后核对实际命令、参数、工具调用次数、运行时间、token、是否发生 Browser Agent 回退，以及最终返回字段。
3. 登录态、收藏夹和个性化推荐内容不得原样写入报告；只保存脱敏账号标识、数量、状态和必要错误摘要。
4. `download`、`follow`、`like`、`favorite`、`answer` 和 `comment` 必须展示非敏感目标与参数，并取得对应的单独确认后执行一次。
5. 写操作失败或结果不明确时不得自动重试，也不得改走 Browser Agent；adapter 没有反向命令时不得承诺自动清理。
6. 本文件不预先记录通过、失败或性能结论；动态证据统一进入管理文档的 RUN 记录。
