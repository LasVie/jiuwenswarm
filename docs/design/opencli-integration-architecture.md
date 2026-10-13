# OpenCLI 可插拔接入架构方案（阻塞后重启任务）

> 更新：2026-09-30。状态：M1 开发联调和 M2 本地产品化完成；验证范围与后续项目见实现方案 §8.7、§8.8。
>
> 源码依据与接口定稿前的验证项见 [CDP 调查](opencli-electron-cdp-research.md)；落地步骤见 [实现方案](opencli-implementation-plan.md)。

## 1. 目标与决策

JiuwenSwarm 为 Browser Agent 提供可选的 OpenCLI 站点 adapter 能力：当前步骤有适用的 adapter 时优先调用，其余步骤由同一个 Browser Agent 用 Playwright 完成，一次任务内可以反复切换。用户关闭这项能力时，Agent 上下文和运行时都不留痕迹。

| 编号 | 决策 | 理由 |
| --- | --- | --- |
| D1 | OpenCLI 只是 Browser Agent 内部的能力，主 Agent 不感知 | 主 Agent 的上下文与开关状态无关；兜底由 Browser Agent 内的 Playwright 工具完成，不需要跨 Agent 交接 |
| D2 | 执行入口是两个专用工具 `opencli_describe` 与 `opencli_run`，不给 Browser Agent 加 shell | Browser Agent 持续读取不可信网页，shell 加上无鉴权的本地 CDP 端口，会让提示注入触达产品 UI。两个工具分别承担"发现"与"执行"，Browser runtime 可以区别对待（§7） |
| D3 | 共享 profile，不共享页面：OpenCLI 使用同一 partition 下的独立工作页 | 浏览器型 adapter 普遍会自己导航，连接时还会注入 stealth 脚本，与 Playwright 共用页面会把后者正在操作的页面导航走。登录态由 partition 共享即可，共享范围见 §6.1 |
| D4 | 只在内置 Electron 浏览器下启用；外置浏览器和没有 Electron 的部署完全不启用，包括不需要浏览器的 adapter | 产品边界清晰，启用判断只有一个维度 |
| D5 | 工作页默认显示在侧栏，保留 hidden（无头）模式 | 用户能看到 OpenCLI 的操作过程；以后不需要展示时切换配置即可 |
| D6 | 遇到验证码、登录、人机验证时，本次任务以 `blocked` 结束并交回主 Agent；用户处理完后，主 Agent 在新的一轮里重新发起任务 | 与现有 Playwright 遇到验证码时的行为一致，用户只需理解一套交互；现有 TaskTool 按对话轮次区分浏览器查询，这条路径不需要新增恢复机制（§6.3）；OpenCLI 读操作重跑的成本很低 |
| D7 | 只用 CDP 直连，不使用 OpenCLI 的"扩展 + daemon"路线 | Electron 的扩展 API 不支持 OpenCLI 扩展依赖的 `debugger`、`tabGroups`、`downloads` |
| D8 | 运行包私有化：固定发行物、子进程使用私有 HOME、固定执行配置、命令目录读自发行包的 `cli-manifest.json` | 与用户全局的 `~/.opencli` 和 daemon 隔离，adapter 来源只取决于包版本 |
| D9 | 写命令由用户在侧栏确认条上逐次确认，确认绑定具体命令和参数，在工具调用内同步等待 | 现有权限中断在 Swarm 成员上无法完成 ASK（[config_specs.py:606](../../jiuwenswarm/agents/swarm/config_specs.py#L606)）；本期只支持 Electron，侧栏总是可用，而且确认来自用户点击，不依赖模型转述 |

本期不包含：OpenCLI 通用 `browser` 命令、现场探索或生成 adapter、桌面应用 adapter、外置浏览器、远端成员、后台进程执行、OpenCLI 与 Playwright 操作同一页面，以及被阻塞任务的原地恢复。

开发与验收先全部在本地完成。Swarm 通过 `pyproject.toml` 的 `[tool.uv.sources]` 依赖同级的 `../agent-core`，采用可编辑安装，并在 `uv.lock` 中固定来源。修改 Core 后重启后端即可验证；Core SDK 发布不是接入开发的前置条件。

## 2. 分层与职责

~~~mermaid
flowchart TB
    Main[主 Agent] -->|网页任务| BA[Browser Agent]
    Pkg[Swarm OpenCLI 包] -. 启用时追加工具与路由提示 .-> BA
    BA --> Tool[opencli_describe / opencli_run]
    BA --> PW[Playwright 工具]
    Tool --> RT[私有运行包 node + opencli]
    Tool -->|工作页 / 确认 / 人工处理| Host[Electron 宿主]
    PW --> MCP[target_mcp_wrapper]
    MCP --> P1[Browser Agent 页面]
    RT -->|页面级 CDP| P2[OpenCLI 工作页]
    Host --> P1
    Host --> P2
    P1 --- Part[(persist:jiuwenswarm-browser 共享 cookie 与持久存储)]
    P2 --- Part
~~~

| 层 | 负责 | 不负责 |
| --- | --- | --- |
| Agent Core | 已有的子代理装配与 TaskTool；外部工具参与 Browser runtime 的契约（§7 C1） | 任何 OpenCLI 概念 |
| Swarm OpenCLI 包 `jiuwenswarm/extensions/opencli/` | 启用判断、命令来源接口与 OpenCLI 来源（§8）、两个工具、路由提示、工作页状态、待核实记录、宿主客户端、状态诊断 | Playwright 行为 |
| Electron 宿主 | 在共享 partition 中创建、展示、保留、重置、回收工作页；返回页面级 CDP 地址；侧栏确认条与人工处理说明 | adapter 语义 |
| OpenCLI 运行包 | 参数校验、adapter 逻辑、CDP 操作、结构化输出与错误 | 页面选择（由调用方给定精确页面） |

## 3. 可插拔与上下文

### 3.1 启用判断

单 Agent、Code 模式、Swarm 成员三处共用一个函数。判断放在 Browser Agent 的 RuntimeSettings 最终确定之后，依据它**实际绑定的浏览器**，而不是从配置推测：

| 条件 | 结果 |
| --- | --- |
| `browser.opencli.enabled` 为 false，或 OpenCLI 包不存在 | 不贡献任何内容 |
| Browser Agent 没有绑定 Electron 侧栏：MCP 环境中没有 target resolver 与 session 身份（包括 Swarm 配置了 `chrome_path` 的外置 Chrome） | 不贡献任何内容 |
| 运行包缺失或版本不符 | 不贡献任何内容，设置页显示原因 |
| 以上都满足 | 追加两个工具和路由提示段 |

会话/成员身份直接取自该 Browser Agent 的 Playwright MCP 绑定（`PLAYWRIGHT_MCP_SESSION_ID`、`PLAYWRIGHT_MCP_MEMBER_ID`），保证工作页与 Browser Agent 的页面属于同一会话/成员。

### 3.2 关闭时：零暴露

- 主 Agent：提示、工具描述、技能列表中都不出现 OpenCLI。
- Browser Agent：没有 OpenCLI 工具或路由提示段。
- 运行时：不探测可执行文件，不读 `~/.opencli`，不启动或连接 daemon，不修改进程环境变量。
- 宿主：不创建工作页。

验收：同一任务在"未安装包"和"已安装但关闭"两种状态下，主 Agent 与 Browser Agent 的系统提示和工具列表逐字节一致。

### 3.3 启用时：最小注入

| 内容 | 时机 | 规模 |
| --- | --- | --- |
| `opencli_describe`、`opencli_run` 的 schema | 构建 Browser Agent 时 | 两个工具 |
| 路由提示段：选择规则 + 已启用站点名列表 | 构建 Browser Agent 时 | 约 1k token 以内（当前 179 个站点） |
| 站点命令列表、命令参数说明、该站点的待核实写操作 | `opencli_describe` 按需返回 | 仅当前站点或命令 |

不使用 Skill 机制。站点名列表放在提示里，是为了让 Browser Agent 不多花一轮调用就能判断"这个站点有没有 adapter"。

### 3.4 生效时机

TaskTool 每次调用都会新建临时的 Browser Agent 实例（[interface_deep.py:1887](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py#L1887)），实例由装配阶段生成的 spec 构建。因此：是否贡献在构建 spec 时一次决定；设置变更后刷新 spec，**下一次** Browser Agent 任务生效，进行中的任务按原配置跑完；不做热挂载或热卸载。实施前需确认 Swarm 成员侧没有长期缓存 Browser Agent 实例；如有，设置变更时让缓存失效即可。

## 4. 工具

### 4.1 `opencli_describe`（发现）

参数 `site`（必填）和 `command`（可选）：

- 站点级：返回命令名、一句话说明、读/写类型，以及本会话中该站点结果不明的写操作（§4.3）。
- 命令级：返回参数定义，必要时附上上游 `--help` 文本。

数据来自命令目录（§8）和插件的待核实记录，不启动 CLI 进程、不接触页面。

### 4.2 `opencli_run`（执行）

参数 `site`、`command`、`args`。`args` 是按 manifest 参数名传值的对象，例如 `{"query": "显卡", "limit": 10}`。工具按 manifest 的定义拼出命令行，不经过 shell：具名参数写成 `--name=value`，位置参数按顺序放在 `--` 之后。这样以 `-` 开头的值（例如查询词 `-foo`）不会被当成选项（WP0 实测）。

**模型只能提供 adapter 的业务参数。** 运行控制参数（`-f`、`--site-session`、`--trace`、`--keep-tab`、`--verbose` 等）由工具固定；该命令的 manifest 中没有的参数名一律拒绝。原因是上游"命令行参数优先于环境变量"（[execution.ts:591](../../../opencli/src/execution.ts#L591)），如果放任模型传入 `--site-session persistent`，就会绕过 §8 的执行配置，重新触发 daemon 请求。

一次调用的流程：

1. **准入**：核对 site/command 属于当前启用的目录；按 manifest 校验参数名、必填项、类型与可选值，然后拼出命令行。
2. **写确认**（仅 `access=write`）：请求宿主在侧栏显示确认条，内容是完整的命令和参数；工具调用同步等待用户点击，超时视为未确认。等待时间计入 TaskTool 的浏览器查询预算（简单任务 240 秒、复杂任务 600 秒，[task_tool.py:55-56](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L55-L56)），默认确认超时为 90 秒，并受剩余预算约束。确认只对这一次调用有效。如果同一站点、同一命令存在结果不明的写操作，确认条会醒目提醒，由用户决定是否再次执行。确认结束后、工作页排队结束后各重新检查一次剩余时间；不足以执行时返回未启动，不沿用确认前的时间预算。
3. **工作页**：命令需要浏览器时，占用本会话/成员的工作页（§5），取得页面级 WebSocket 地址。
4. **启动**：用 Electron 自带的 Node 模式（§8.3）直接启动 `<运行包>/entry.mjs <site> <command> <具名参数> -f json --trace off [--site-session ephemeral] [-- <位置参数>]`，不经过 shell。需要浏览器的命令必须带工作页地址，没有地址时拒绝启动：上游在没有 `OPENCLI_CDP_ENDPOINT` 时会改走 daemon 和 Chrome 扩展，也就是用户自己的浏览器。`--site-session ephemeral` 只加给需要浏览器的命令；上游只给 `browser=true` 的命令注册了这个选项（[commanderAdapter.ts:63-68](../../../opencli/src/commanderAdapter.ts#L63-L68)），给不需要浏览器的命令加上它会报"未知参数"。环境变量见 §8.3；工作目录为任务工作区。
5. **超时与取消**：工具自己设定超时（取命令超时与本次调用剩余时间中较小者）。超时或任务取消时，结束整个进程树并等待进程退出，随后工作页进入"待重置"（§5.2）。取消通过 `CommandCancelled` 带回 `RunOutcome.started/killed`：工具先保存已经启动的写操作的待核实记录，再释放租约、重建页面，最后向上层传播取消。重复的停止请求不能打断这些收尾步骤；如果停止发生在页面分配或子进程创建期间，也要等待取得资源的结果并回收。上游 CLI 的内部超时只是竞争等待，并不取消 adapter（[execution.ts:373](../../../opencli/src/execution.ts#L373)），不能依赖它来收尾。
6. **结果**：读取 stdout（JSON 数据）和 stderr（上游 YAML 错误信封），按 §4.3 返回。

步骤 1–3 中的失败都发生在进程启动之前，可以确定命令**未执行**。

### 4.3 结果：读命令看原因，写命令先看是否执行

- `executed`（只对写命令有意义）：`no` 表示进程未启动，包括准入或参数校验失败、确认被拒或超时、工作页不可用；`yes` 表示退出码 0；`unknown` 表示进程已启动，但退出码非 0（包括 66）、超时或被结束。
- `reason`：`ok`、`empty`（66 `EMPTY_RESULT`）、`invalid_args`（2 `ARGUMENT` 或本地校验）、`needs_user`（77 `AUTH_REQUIRED` / `LOGIN_WALL`，含验证码和 WAF 挑战）、`not_confirmed`、`env_unavailable`（69 `BROWSER_CONNECT` / `ADAPTER_LOAD`、78 `CONFIG`、工作页不可用）、`timeout`、`error`。

Browser Agent 的下一步：

| 命令类型 | 情况 | 下一步 |
| --- | --- | --- |
| 读 | `ok` / `empty` | 使用数据；空结果按正常结果解释 |
| 读 | `invalid_args` | 重新 describe 并修正参数，最多重试一次 |
| 读 | `needs_user` | 以 `blocked` 结束，交给用户（§6.3）；由之后的新任务重跑 |
| 读 | 其他 | 这一步改用 Playwright；后续步骤仍可再试 OpenCLI |
| 写 | `executed=no` | `not_confirmed`：停止并如实告知；`needs_user`：以 `blocked` 结束，交给用户，由新任务重新执行（需重新确认）；其他：同读命令的对应规则 |
| 写 | `executed=unknown` + `needs_user` | 以 `blocked` 结束，交给用户；这次写操作记入待核实记录，新任务执行同类操作前会被提示先核实 |
| 写 | `executed=unknown` + 其他原因 | 先核实（读命令或页面观察）。确认未生效后才能再次执行，并且要重新确认；无法核实时向用户报告"结果不确定"，不换 Playwright 重复提交 |
| 写 | `yes` | 继续；需要页面证据时用 Playwright 核对 |

**待核实记录**：`executed=unknown` 的写操作记录在插件的会话级状态中（站点、命令、参数摘要、时间）。它不依赖任何 Agent 的记忆，在同一会话的所有任务之间生效：

- `opencli_describe(site)` 的输出会列出该站点的待核实项，提示先核实；
- 对同一站点、同一命令执行 `opencli_run` 时，确认条会醒目提醒"上次结果不明"；
- 用户在确认条上作出决定后清除该项；会话结束时全部清除。页面重置或重建都不影响记录。

### 4.4 输出与证据

结果是结构化字典：`ok`、`executed`、`reason`、`data`、`error`，以及 `source`（`opencli:<site>/<command>` 和工作页 URL）。

- **与 runtime 结果分类对齐**：runtime 根据 `ok`、`error`、`status` 判断工具成败（[runtime.py:666-680](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L666-L680)）。`reason` 为 `ok` 或 `empty` 时 `ok=true`、不带 `error`；其余情况 `ok=false` 并附 `error`。结果中不使用 `status` 字段，因为 runtime 会把 `partial`、`failed` 等值当作失败。
- **幂等声明**：`opencli_describe` 声明为幂等；`opencli_run` 保持非幂等（`ToolCard.idempotent` 的默认值，[base.py:109](../../../agent-core/openjiuwen/core/foundation/tool/base.py#L109)）。非幂等工具不会被自动重试，也不受外层调用超时约束，所以 `opencli_run` 必须自己控制超时（§4.2 第 5 步）。

- **大结果**：单条结果超过阈值（与回读工具的单次读取量同一量级，约 8k 字符，Core 可配置）时立即落盘，上下文里只放预览和 handle，用现有的 `browser_recall_offload` 分段回读（C1）。回读工具会拒绝超过 8MB 的落盘文件（[offload_recall.py:191](../../../agent-core/openjiuwen/harness/tools/browser_move/offload_recall.py#L191)）。落盘时结果文本作为 JSON 字符串嵌入（`ensure_ascii=False`、`indent=2`），引号和换行都要转义，所以工具按"转义后的 UTF-8 字节数"把结果控制在 7MiB 以内，给外层封装留出余量。超过时按整行截断，并标注 `truncated`、总行数和返回行数，提示收窄查询。
- **证据**：需要满足完成判定时，按 C1 契约提供 `extracted`、`field_provenance`。`extracted` 的字段名来自命令目录中的输出列；列表结果另附 `observed_count`（实际返回的条数）。
- **需要用户处理**：附上 `user_action_required`（阻塞原因、操作说明），runtime 据此以 `blocked` 结束任务（C1）。

## 5. 工作页（Electron 宿主）

### 5.1 身份与分配

- 身份：`panelIdentity(session, member, role='opencli')`。与 Browser Agent 页面属于同一会话/成员，panelId 因 role 不同而不同。
- 存储：与其他页面同在 partition `persist:jiuwenswarm-browser`。
- 数量：每个会话/成员最多一个工作页，第一次需要浏览器的调用时才创建。
- 标签：单 Agent 显示为"OpenCLI"，Swarm 成员显示为"OpenCLI · 成员名"。

### 5.2 状态

状态由 Python 侧的工作页客户端维护，宿主负责保留、重置和回收页面：

| 状态 | 含义 | 规则 |
| --- | --- | --- |
| 空闲 | 无调用占用 | 可被新调用占用；不可见且无租约时宿主可回收 |
| 执行中 | 一次 `opencli_run` 正在进行 | 同一页面的其他调用排队；持有宿主租约 |
| 等待人工 | 调用返回 `needs_user`，页面停在验证码或登录页上；记录一个阻塞 ID | 宿主固定保留、不回收。只有用户在侧栏对这次阻塞点了「已完成，继续」，下一次调用才能使用这个页面；用户还没处理时，调用不执行、不导航，直接返回 `needs_user`。用户点「放弃」或过期（默认 30 分钟）后进入"待重置" |
| 取消收尾 | 超时或取消后，等待进程树退出 | 进程退出后进入"待重置"；写命令记为 `unknown` |
| 待重置 | 页面上可能仍有 adapter 派发的脚本或网络请求在运行，结束 Node 进程并不能停止它们 | 不可复用。宿主销毁并重建该 WebContents（新的 targetId）后回到空闲；重建不影响待核实记录 |

为什么需要用户的明确操作：现有 TaskTool 用主 Agent 当前这一轮的 invocation id 作为浏览器查询 ID（[task_tool.py:267-272](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L267-L272)），所以同一轮里阻塞之后再发起的浏览器任务会被拒绝（[task_tool.py:548](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L548)）。但这只覆盖同一个 invocation。自动继续、团队重新派发都可能开启新的 invocation，"出现了新任务"并不能说明用户已经处理完。

因此解除条件由 Swarm 自己管理：宿主记录侧栏按钮产生的决定（已完成 / 放弃），工作页客户端在下一次调用前查询。这不需要 Core 的暂停与恢复协议。

### 5.3 宿主接口（扩展现有 resolver）

在 [browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs) 的 `createTargetHandler` 上扩展，沿用 loopback、Bearer token、拒绝浏览器 Origin 的安全边界：

| 请求 | 说明 |
| --- | --- |
| `POST /{session}?member=&lease=&pid=` | 新增 `role=opencli`、`visibility=sidebar\|hidden`；返回值新增 `webSocketDebuggerUrl`（`ws://127.0.0.1:<cdpPort>/devtools/page/<targetId>`） |
| `DELETE /{session}?...` | 不变：释放本次调用的租约 |
| `POST /{session}/hold?member=&role=opencli` | 以阻塞 ID 固定保留工作页，并发出 attention（侧栏切到该页、显示处理说明和按钮）；保留期间不回收 |
| `POST /{session}/reset?member=&role=opencli` | 销毁并重建工作页（新的 targetId），用于取消之后和等待过期之后 |
| `POST /{session}/confirm?member=&role=opencli` | 显示写确认条（命令、参数与待核实提醒），等待用户点击或超时，返回用户的决定 |

保留由宿主强制执行：工作页处于保留中且用户尚未决定时，分配请求直接返回 409 `awaiting_user`；用户点「已完成，继续」后，下一次分配自动解除保留并复用该页；点「放弃」或过期后，下一次分配先重建页面。决定只能由侧栏按钮经 IPC 写入，HTTP 接口不能写入。租约沿用现有的 pid 租约，AgentServer 进程退出后由宿主自动清理。确认结果只来自侧栏里的用户点击，模型没有任何途径调用这个接口。

### 5.4 可见性

| 模式 | 行为 |
| --- | --- |
| `sidebar`（默认） | 工作页作为标签出现在该会话的侧栏面板列表中，执行期间显示运行状态；只有写确认和人工处理时才自动切换过去 |
| `hidden` | 工作页不出现在面板列表中；写确认和人工处理时临时放入并切换，结束后宿主恢复隐藏，前端恢复此前选中的成员页；保留用户主动切换的选择 |

前端由常驻的 App 层订阅 attention 与待处理面板状态，重新打开当前会话的浏览器页签、展开侧栏，并把目标 panelId 传给 [DesktopBrowserPane](../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane/index.tsx)。因此侧栏收起、停在其他页签或浏览器页签已关闭时，也能显示写确认和人工处理说明。DesktopBrowserPane 的默认选中排除 `role=opencli`，收到 attention 时再切到工作页；确认与保留状态从宿主面板列表恢复，晚挂载不会漏掉请求。人工处理说明旁提供两个按钮。「已完成，继续」先让宿主把这次阻塞记为 `resolved`，再向当前会话发送一条普通聊天消息，让主 Agent 继续；「放弃」让宿主记为 `abandoned`。人工处理说明只引导用户操作内置浏览器的工作页，以保证使用同一 profile。用户在工作页执行中直接操作页面不会被阻止，只显示"运行中"提示。

### 5.5 并发与回收

- 同一工作页上的调用串行；不同会话/成员的工作页可以并行。
- 页面锁和重建标记按会话/成员共享；每次任务装配创建自己的客户端，保留当时的工作页模式。设置变更不会修改正在执行的工具，下一次任务使用新模式时仍复用同一工作页。
- 工作页计入现有 `MAX_BROWSER_SESSION_VIEWS` 软上限（8 个，[main.cjs:186](../../jiuwenswarm/channels/desktop/electron/main.cjs#L186)），只有"空闲"状态才可能被回收。Swarm 中每个成员最多有两个视图，回收压力会翻倍，所以回收时优先回收空闲的工作页，它们没有需要保留的页面状态。工作页被重置或回收后，从空白页重新开始，不还原上次的 URL（还原会重新触发页面上的脚本；adapter 自己会导航）。
- OpenCLI 从不连接 Browser Agent 的页面，两种执行器之间不需要页面租约、代次或失效通知。

## 6. 与 Playwright 的协作

### 6.1 共享边界

| 随 partition 共享 | 不共享 |
| --- | --- |
| cookie、同源的 localStorage 与 IndexedDB、登录态 | sessionStorage（按页面会话隔离）、页面内存与脚本状态、未提交的表单草稿、部分绑定在页面上的验证状态 |

因此两种执行器之间的接续，只依赖**可重建的 URL、业务 ID 和共享的登录态**。依赖原页面临时状态的操作（例如在当前页已填好一半的表单上继续提交）留在 Playwright 路径。验证码在工作页上由用户处理、页面不被重置，也是为了让之后的命令能用上同一页面里的验证结果。

### 6.2 选择规则（写入路由提示）

- 按"站点 + 当前操作"判断：站点在列表中，就用 describe 找命令；有适用命令就 run，否则用 Playwright。
- describe 列出了待核实项时，先核实再执行同类写操作。
- adapter 只覆盖部分步骤时，按步骤组合两种工具，全程由同一个 Browser Agent 负责。
- 用户明确要求打开页面、截图或在页面上核对时，这一步用 Playwright 完成，例如打开 OpenCLI 结果中的 URL。
- Playwright 接管某一步后，后续步骤仍可回到 OpenCLI。
- `opencli_run` 返回 `needs_user` 时，不尝试用 Playwright 绕过验证，直接结束任务交给用户。
- 默认系统提示以 Playwright 为中心（先观察页面、构造搜索 URL、用 probe 定位）。路由提示段要写明：先判断有没有适用的命令，页面操作相关的指引只在走 Playwright 路径时适用。

### 6.3 人工处理（验证码、登录、人机验证）

1. `opencli_run` 返回 `needs_user`。工作页停在验证码或登录页上，进入"等待人工"；宿主固定保留页面并发出 attention，侧栏显示处理说明。
2. 结果中的 `user_action_required` 让 runtime 以现有的不可重试原因（`captcha`、`login_required`、`user_intervention_required`，见 [runtime.py:208-219](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L208-L219)）把任务结束为 `blocked`。结果中带有已完成的步骤和待核实项。
3. 主 Agent 告知用户需要做什么、在哪里做。这一轮里不会再有新的浏览器任务启动。
4. 用户在侧栏工作页上完成验证（或者在任意页面登录，cookie 共享），然后点击「已完成，继续」。宿主记下这个决定，并发出一条普通聊天消息，开启新的一轮。
5. 主 Agent 根据上一次的阻塞结果，发起一个**描述完整的新浏览器任务**，写清楚已经完成了什么、还要做什么。
6. 新的 Browser Agent 从 describe 开始。工作页客户端确认宿主记录的决定是 `resolved` 后解除保留，验证结果从 partition 的 cookie 或同一页面的 sessionStorage 中生效；待核实项会出现在 describe 输出和确认条上。
7. 如果在用户点按钮之前就有任务被自动发起（自动继续、团队重新派发），或者用户只是用文字说"好了"，调用会直接返回 `needs_user`，页面保持原样。主 Agent 这时应提示用户到侧栏点击按钮。
7. 用户一直没有回来：保留在过期后解除，工作页进入"待重置"。

Swarm 成员被阻塞时，同样由主 Agent（或 leader）按团队现有的阻塞上报流程告知用户，用户处理后重新派发任务；工作页标签带有成员名，用户能找到对应页面。

共享 partition 意味着切换账号会影响所有会话，这是内置浏览器已有的语义，不额外加锁。

### 6.4 写操作

- 执行前逐次确认（§4.2）。
- 结果不明时记入待核实记录；之后任何任务执行同类操作前，都会通过 describe 输出和确认条被提醒。
- 不自动重试写命令，也不换 Playwright 重复提交。

## 7. 对 Browser runtime 的影响与 Core 改动

### 7.1 影响清单

OpenCLI 工具进入 Browser Agent 后，会碰到 runtime 的下列机制。以下各项都已对照源码核实：

| 机制 | 现状 | 不处理的后果 | 处理方式 |
| --- | --- | --- | --- |
| 启动与首次观察 | `before_invoke` 启动 Playwright MCP；首次模型调用时采集页面（[browser_state_context_processor.py:146](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py#L146)），之后每次调用都附带 `<browser_state>` | 纯 OpenCLI 任务也要付启动和采集的成本，每次调用还多带一段无关的页面状态 | C2（可选） |
| 阶段预算与重规划 | 对所有工具生效（[runtime.py:2867](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L2867)） | describe 耗尽"导航"预算；正常的命令查询被判为没有进展 | C1 |
| 页面变化与证据来源 | 非观察类工具都被当作可能改变了页面；字符串结果被套上 Playwright 的 `page_state` | Playwright 页面被误标为已变化；证据来源记错 | C1 |
| 完成判定：证据与字段 | 必须有证据，并且从任务文本推断出的必需字段都被覆盖（[runtime.py:3854-3877](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L3854-L3877)）；只有存在页面观察时，才豁免非严格字段（[runtime.py:5126](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L5126)） | 纯 OpenCLI 任务即使数据齐全，也会因 `missing_required_field` 被判为 `partial` | C1 |
| 完成判定：结果数量 | 从任务文本推断"前 N 条"（[runtime.py:4319](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L4319)），实际条数只从卡片探测的证据中统计（[runtime.py:5289](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L5289)） | "列出前 10 条"是 OpenCLI 最典型的任务，却会因为条数不足被判为未完成 | C1 |
| 工具结果分类 | 按 `ok`、`error`、`status` 判断成败 | 结果字段不一致会被误判为失败 | 结果约定（§4.4） |
| 结果窗口 | 只覆盖五个浏览器工具，保留最新两条完整结果 | 第一次返回的大结果会整个进入上下文 | C1 |
| 自动重试 | 只重试幂等工具；非幂等工具也不受外层调用超时约束 | 如果把 run 标为幂等，超时后写命令可能被重跑 | describe 标为幂等、run 保持非幂等，run 自己控制超时（§4.4） |
| 查询预算 | 简单任务 240 秒、复杂任务 600 秒 | 写确认等待、Node 冷启动、adapter 预导航都要计入预算 | 确认超时受剩余预算约束（§4.2） |
| 系统提示 | 默认提示以 Playwright 为中心；最终状态由 runtime 决定 | 模型可能先观察页面，而不是先查命令 | 路由提示段写明优先级（§6.2） |
| 侧栏视图数量 | 软上限 8 个 | Swarm 中回收压力翻倍 | 优先回收空闲工作页（§5.5） |

不受影响的部分：Playwright 工具本身、target_mcp_wrapper、会话面板绑定、页面状态的刷新判定（它只认浏览器工具名，OpenCLI 调用不会触发刷新）、MCP 工具白名单（只作用于 MCP 工具）、TaskTool。

下面两项 Core 改动都不涉及 OpenCLI 概念。

### 7.2 C1（必需）外部工具参与 Browser runtime 的契约

现状：runtime 对所有工具一视同仁。
- 执行前，`_consume_phase_budget`（[runtime.py:2867](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L2867)）对所有工具扣阶段预算，做策略重复检测和重规划限制；未识别的工具会落进当前阶段，默认是"导航"。豁免名单只写死了几个工具名（L4951）。
- 执行后，`_tool_may_change_browser_state`（L3342）把非观察类工具都当作可能改变了页面；字符串结果连同 Playwright 页面的 `page_state` 一起记为证据（L2997-3003）。
- 结果窗口化只针对写死的五个浏览器工具（[browser_agent.py:374](../../../agent-core/openjiuwen/harness/subagents/browser_agent.py#L374)），而且会保留最新两条完整结果（[tool_result_window_processor.py:108](../../../agent-core/openjiuwen/core/context_engine/processor/offloader/tool_result_window_processor.py#L108)），第一次返回的大结果会整个进入上下文。

契约：外部工具通过 `ToolCard.properties` 声明自己如何参与 runtime。`properties` 是已有的自由字段（[base.py:91](../../../agent-core/openjiuwen/core/foundation/tool/base.py#L91)），不需要改 schema，具体键名在 Core 评审时确定。分两类：

| 方面 | `discovery`（如 `opencli_describe`） | `action`（如 `opencli_run`） |
| --- | --- | --- |
| 阶段预算与重规划 | 豁免，同 `browser_recall_offload` | 计入独立的"外部操作"阶段，有自己的预算；按"工具名 + 完整参数"的规范 JSON 哈希检测重复，忽略映射键顺序，保留嵌套字段与长参数；不复用 Playwright 的语义字段筛选 |
| 进展 | 不算进展，也不算无进展 | 返回数据或新证据即记为进展 |
| 页面状态 | 不影响 | 不影响 Playwright 页面状态，不附加 `page_state` |
| 证据 | 无 | 结果中的 `extracted` + `field_provenance` + `source` 进入既有证据结构 |
| 完成判定 | 无 | `extracted` 的字段名经 runtime 现有的字段别名映射后计入字段覆盖；列表结果的 `observed_count` 计入实际条数；带来源的外部观察与页面观察一样，参与非严格字段的豁免 |
| 大结果 | 可声明 | 可声明。声明后纳入 Browser Agent 的 `ToolResultWindowProcessor`。为它增加一个**按工具的单条阈值**：即使是最新结果，只要超过阈值也立即落盘，上下文里只留预览和 handle。落盘文件沿用这个处理器的前缀和格式，现有的 `browser_recall_offload` 可以直接回读。不采用 `ToolResultBudgetProcessor`：它的 `tool_name_allowlist` 是"永不落盘"的保护名单，而且按每轮总量触发，不适合按单条结果判断 |
| 需要用户处理 | 无 | 结果中的 `user_action_required` 让任务以现有的不可重试原因结束为 `blocked`，不依赖模型自己报告状态 |

不适用于外部工具的页面规则：refs 校验、直接导航引导、价格区间去重、主链接点击改写。

测试覆盖：连续多次 describe 不消耗预算；跨多个站点的 adapter 查询不被判为无进展；纯 OpenCLI 完成的任务通过完成判定，包括含"前 N 条"的列表任务，以及推断出必需字段的任务；外部工具失败时 Playwright 页面状态不被标记为已变化；首次返回的大结果只有预览进入上下文，完整内容可以回读；`user_action_required` 使任务以 `blocked` 结束。

### 7.3 C2（可选，性能）Playwright 懒启动与延后首次观察

`before_invoke` 会先启动 Playwright MCP（[runtime.py:2355-2356](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L2355-L2356)），首次模型调用时还会采集一次页面状态，并在之后每次调用中附带。只用 OpenCLI 的任务也要付这些成本；被阻塞后重启的任务还会再付一次。

改为：第一次调用浏览器工具时才启动 MCP、采集页面；在此之前，`<browser_state>` 只显示"尚未观察页面"。两者需要一起改，只做懒启动没有意义，因为首次采集本身就依赖 MCP。

前提：首轮模型调用之前，浏览器工具的 schema 能不依赖 MCP 进程取得（例如按 MCP 版本缓存）。C2 不阻塞接入，但会影响阶段 E 的评估结论。

## 8. 命令来源与运行包

### 8.1 命令来源边界

工具、工作页、写确认、待核实记录、结果分类和 C1 证据都是产品层，它们只依赖下面两个接口，不依赖 OpenCLI 的任何格式：

| 接口 | 内容 | OpenCLI 来源的实现 |
| --- | --- | --- |
| 命令目录 `CommandSpec` | site、command、说明、读/写、是否需要浏览器、参数定义（名称、类型、必填、可选值、是否位置参数）、输出列、domain | 读取 `cli-manifest.json` 并转换 |
| 执行器 `run(spec, args, page_endpoint, deadline)` | 输入：命令、已校验的参数、工作页的页面级 CDP 地址、截止时间。输出：结果类别（完成 / 空 / 参数错误 / 需要用户 / 环境不可用 / 超时 / 错误）、数据行、原始错误 | 启动 node 进程并固定控制参数，解析 stdout 和 YAML 错误信封，映射退出码 |

- **页面契约**：执行器拿到的是标准的页面级 CDP 地址，Node、Python、Playwright 的 `connect_over_cdp` 都能直接使用，不绑定任何实现。
- **语义归产品层**：`executed`、`reason`、待核实、确认条这些语义，都由产品层根据执行器的输出推导，换一个来源也不用重新实现。
- **取消契约**：来源在取消时负责结束执行，再通过 `CommandCancelled(outcome)` 报出是否已经启动、是否被结束；产品层据此保留未知写入并重建页面。新的来源必须实现这项契约，才能复用同样的取消与写操作保护。
- **一期只有 OpenCLI 一个来源**。预留的规则是：多个来源提供同一个 site/command 时，自有来源优先；目录在装配时合并，模型只看到一份。

**命名（待确认）**：面向模型和用户的名字建议都不带 OpenCLI：
- 工具名 `site_command_describe`、`site_command_run`；
- 配置键 `browser.site_commands`；
- 侧栏标签"站点命令"；
- 包路径 `extensions/site_commands`。

OpenCLI 只作为来源 ID，出现在 `source` 字段和诊断信息里。现在改名几乎没有成本；以后再改，就要迁移用户配置、提示词和评估数据。本文暂时沿用 `opencli_*` 的写法，确认后统一替换。

### 8.2 脱离 OpenCLI 的可行性

依据（上游研究基线 1.8.8）：
- 1366 条命令全部是 JS adapter：1017 个文件用函数实现，114 个用 pipeline，合计约 16 万行。运行时 `src/` 约 2.8 万行，其中大部分是 daemon、浏览器扩展和通用 browser 命令，本方案都用不到。
- adapter 对运行时的依赖面很窄：`registry`（命令声明）1511 处、`errors` 1297 处；页面对象的方法中，`evaluate` 1312 处、`wait` 793 处、`goto` 610 处、`getCookies` 137 处，其余（截图、按键、网络捕获、拦截器、文件上传等）合计不到 200 处。
- 许可证是 Apache 2.0，允许 fork、修改和再分发，需要保留版权与 NOTICE，并标注修改。

三条可选路径，按成本从低到高：

| 路径 | 做法 | 成本 | 适用场景 |
| --- | --- | --- | --- |
| 1. 自维护发行物 | fork 上游，保留 adapter 格式、`registry`、`errors` 和 CDP 页面实现，删掉 daemon、扩展和 BrowserBridge；只保留需要的站点；按需合入上游修复 | 低。旧项目已经在维护 `LasVie/OpenCLI` 分支；CDP 模式下跳过 lease 释放这类补丁也会放在这里 | 首选。manifest 格式不变，产品层完全不用改 |
| 2. 自有来源，逐站接管 | 用同样的格式为重点站点编写自己的 adapter，作为优先来源；长尾站点继续用上游 | 中。主要是跟进网站改版 | 重点站点对质量或合规要求高时 |
| 3. 更换运行时（例如 Python） | 按页面对象的窄接口用 Python 重写运行时，adapter 逐个重写 | 高。约 16 万行 adapter 需要重写 | 只在明确要去掉 Node 依赖时考虑 |

结论：技术上可行，而且产品层不需要改动。真正的长期成本不在运行时，而在 adapter 本身：网站改版、风控变化都要持续跟进。上游社区目前维护着 179 个站点，脱离之后这部分成本要由我们承担。建议现在就把 §8.1 的边界做好，脱离则按需逐站进行，不做一次性替换。

### 8.3 OpenCLI 运行包

- **发行物**：原作者的 `@jackwener/opencli`，版本在阶段 A 选定并固定（研究基线 1.8.8，上游要求 Node ≥ 20.18.1）。安装在产品管理的目录，与用户全局的 npm 安装无关。
- **Node 来源**：使用 Electron 自带的 Node 模式，即 Electron 可执行文件加 `ELECTRON_RUN_AS_NODE=1`，**不依赖系统 PATH 里的 node**。打包版的 Playwright MCP 已经这样运行（[main.cjs:300-316](../../jiuwenswarm/channels/desktop/electron/main.cjs#L300-L316)），而 OpenCLI 只在 Electron 下启用（D4），所以这个运行环境一定存在。Electron 通过发现信息把自己的可执行文件路径交给 AgentServer。OpenCLI 的依赖都是纯 JS，不涉及原生模块的 ABI 问题；Electron 内置的 Node 版本在准备阶段核对。
- **调用**：用上述 Node 直接启动运行包的入口 `entry.mjs`，不依赖 PATH、shim 或 PowerShell 解析。入口在 Electron 下设置 `process.defaultApp = true`，然后导入 `dist/src/main.js`。原因是上游的 commander 检测到 Electron 且 `defaultApp` 未设置时，会认为 argv 中没有脚本路径，把脚本路径当成命令名；直接启动 `main.js` 时所有命令都会失败（WP0 实测）。
- **调用环境**：`OPENCLI_CDP_ENDPOINT`（工作页 ws 地址）、私有 `HOME` / `USERPROFILE` 与缓存目录、`OPENCLI_SITE_SESSION=ephemeral`。需要浏览器的命令，会话模式以工具在命令行上固定传入的 `--site-session ephemeral` 为准，环境变量只是兜底，模型不能覆盖（§4.2）。不需要浏览器的命令不传这个选项，它们本来也不会连接 daemon。
  - 私有 HOME：上游把用户 adapter 与插件目录写死为 `os.homedir()/.opencli`（[discovery.ts:23](../../../opencli/src/discovery.ts#L23)），`OPENCLI_CONFIG_DIR` 管不到这里。
  - `ephemeral`：持久会话里的写命令收尾时，会向 daemon 发送 lease 释放请求（[execution.ts:463](../../../opencli/src/execution.ts#L463)、[daemon-client.ts:72](../../../opencli/src/browser/daemon-client.ts#L72)）；如果用户自己跑着 daemon，就会连到它。ephemeral 模式可以消除这条路径。代价是声明 persistent 的 314 条命令每次都会预导航，并失去站点级租约；后者由工作页串行替代。如果阶段 A 发现某些 adapter 依赖 persistent 语义（例如在同一会话里继续对话），改为在自维护发行物中打补丁：CDP 模式下跳过 lease 释放。
- **命令目录**：在**构建运行包时**，由发行包自带的 `cli-manifest.json`（已列入 package `files`）生成 `catalog.json`，一起打进运行包。生成时只保留网站 adapter，排除 `electron-apps` 登记的桌面应用、`strategy=local` 的命令和外部 CLI 透传条目。运行期只读取这个文件，再与用户配置的 `enabled_sites` 取交集。
- **升级**：替换固定版本并重建目录；不做运行时来源快照。

## 9. 配置与设置页

~~~yaml
browser:
  chrome_path: ""
  opencli:
    enabled: false        # 开发与首批验证期间默认关闭
    worker_page: sidebar  # sidebar | hidden
    enabled_sites: null   # null = 目录中全部网站；列表 = 仅这些站点
~~~

设置页放在现有的浏览器模块，内容包括开关、工作页模式和可用状态。关闭时折叠模式选择；状态区区分关闭、可用、运行包缺失、Electron Node 不可用、当前浏览器模式不支持，以及站点限制后无可用命令。可用状态显示目录版本与站点数，表示基础条件满足，不代表每个网站已通过适配验证。

`diagnose()` 只检查 Electron 文件、运行包和目录哈希，并读取宿主报告的 Node 版本，不解压、不启动进程、不创建工作页或修改环境变量。Electron 将可执行路径和 `process.versions.node` 同时写入启动环境与发现文件。关闭或配置外部浏览器时不读发现信息；实际任务装配时再通过 `prepare_runtime()` 执行 Node 版本检查。

Gateway 与 AgentServer ConfigAdapter 使用相同的字段校验和载荷转换。`path.set` 接收字段补丁，嵌套合并 `opencli`，保留未提交的站点限制。仅修改 OpenCLI 时，通过已有的 `agent_runtime` reload scope 刷新后续 Browser Agent spec，不重启浏览器，不提前重建页面；正在执行的任务保留配置快照。浏览器路径或 headless 实际改变时沿用现有的浏览器重启流程。

首期不使用 ApplicationPluginExtension（它面向 Gateway 路由和前端页面贡献）。OpenCLI 包是一个普通应用包加一个装配函数，以后需要独立安装或卸载时再包装成应用扩展。

## 10. 实施阶段与验收

| 阶段 | 内容 | 完成条件 |
| --- | --- | --- |
| A 连接验证 | 固定发行物与执行配置；在隔离 profile 上用手工创建的工作页跑通 [调查文档 §7](opencli-electron-cdp-research.md#7-接口定稿前的验证项) | 读、写 fixture 命令都能精确访问工作页，在 `--site-session ephemeral` 下全程不连 daemon（反例：`persistent` 会连）；cookie 共享；取消后进程树退出，重建页面后页内活动停止；`HOME` 隔离生效 |
| B 最小闭环 | 宿主 `role=opencli`；两个工具；工作页状态；待核实记录；单 Agent 装配 | fixture 站点 describe/run 成功；未命中时走 Playwright；模型传入运行控制参数时被拒绝；关闭时提示与工具列表零差异 |
| C Core C1 | 外部工具契约 | 连续 describe 不耗预算；纯 OpenCLI 任务通过完成判定（包括"前 N 条"的列表任务和推断出必需字段的任务）；首次大结果只有预览进入上下文；`needs_user` 使任务以 `blocked` 结束 |
| D 产品化 | Code 与 Swarm 装配；侧栏标签、hidden 模式、确认条、人工处理说明；设置页 | 写命令确认绑定参数、超时视为未执行；待核实项在新任务的 describe 输出和确认条上出现；用户没有点「已完成，继续」时，自动重新派发的任务不会解除保留、也不会导航工作页，点击之后新任务能接着用这个页面；系统 PATH 中没有 node 时 OpenCLI 仍然可用；Swarm 两个成员并行调用；外置 Chrome 下不启用 |
| E 产品评估 | 同一批任务对比 Browser-only 与混合路径 | 成功率、耗时、模型轮次、token 有可解释的结果；单独统计被阻塞后重启的次数与重复成本，并注明是否已做 C2 |

## 11. 文件清单

工作区中的 Swarm（`jiuwenswarm/`）、Agent Core（`agent-core/`）和 OpenCLI（`opencli/`）是三个同级独立仓库。以下路径相对 Swarm 仓根目录；跨仓路径使用 `../agent-core/` 或 `../opencli/`；"新增"的文件在实施时创建。

**本地开发依赖**

| 类型 | 文件 | 改动 |
| --- | --- | --- |
| 修改 | [pyproject.toml](../../pyproject.toml)、[uv.lock](../../uv.lock) | Core 使用 `../agent-core` 的可编辑来源，正常依赖同步保持本地联调 |

**Swarm OpenCLI 包**

| 类型 | 文件 | 职责 |
| --- | --- | --- |
| 新增 | `jiuwenswarm/extensions/opencli/__init__.py` | 对外只暴露 `browser_agent_contribution(settings, config)` 与 `diagnose(config)` |
| 新增 | `jiuwenswarm/extensions/opencli/gate.py` | 启用判断（§3.1），从 RuntimeSettings 取出会话/成员身份 |
| 新增 | `jiuwenswarm/extensions/opencli/catalog.py` | 与来源无关的 `CommandSpec`、执行器接口、目录合并规则（§8.1） |
| 新增 | `jiuwenswarm/extensions/opencli/sources/opencli.py` | OpenCLI 来源：只读诊断与实际准备分开；定位私有运行包、校验运行包和目录哈希及版本、构造固定参数与调用环境、启动和结束进程树、映射退出码与错误信封 |
| 新增 | `jiuwenswarm/extensions/opencli/tools.py` | `opencli_describe`、`opencli_run`：按参数名拼命令行并固定运行控制参数、写确认、`executed` × `reason` 分类、C1 声明 |
| 新增 | `jiuwenswarm/extensions/opencli/pending.py` | 会话级待核实记录（持久化到用户数据目录） |
| 新增 | `jiuwenswarm/extensions/opencli/worker_page.py` | 工作页状态机（§5.2）与宿主客户端；共享页面锁及重建标记，任务独立保留配置快照；复用 electron_sideview 的发现信息 |
| 新增 | `jiuwenswarm/extensions/opencli/prompt.py` | 路由提示段（规则 + 站点名列表） |
| 新增 | `tests/unit_tests/extensions/opencli/`（pytest 只收集 `tests/`） | gate、目录转换与合并、OpenCLI 来源、参数拼装与覆盖拒绝、分类表、结果字段与 runtime 分类一致、待核实记录、工作页状态、宿主协议、零暴露对比 |

**装配点**：各加一次调用，把返回的工具和提示段追加到 browser spec。

| 类型 | 文件 |
| --- | --- |
| 修改 | [interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py)（L4755 附近）、[interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py)（L2051 附近）、[code_subagents.py](../../jiuwenswarm/agents/swarm/providers/code_subagents.py)（L225 附近，在 `apply_swarm_browser_settings` 之后） |

**Electron 宿主与前端**

| 类型 | 文件 | 改动 |
| --- | --- | --- |
| 修改 | [browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs) | 身份增加 role；resolver 支持 `role`、`visibility`，返回页面 ws 地址；新增 hold、reset、attention、confirm 路由 |
| 修改 | [main.cjs](../../jiuwenswarm/channels/desktop/electron/main.cjs) | 发布 Electron Node 路径与版本；hidden 页处理结束后由宿主隐藏；hold 期间不回收；reset 重建 WebContents；attention 与确认请求发往前端并回传决定 |
| 修改 | [DesktopBrowserPane](../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane/index.tsx)、[preload.cjs](../../jiuwenswarm/channels/desktop/electron/preload.cjs)、[electron.ts](../../jiuwenswarm/channels/web/frontend/src/types/electron.ts) | 默认选中排除工作页；attention 切换；确认条、人工处理说明与「已完成，继续」按钮（发送普通聊天消息）；运行状态 |
| 新增 | `DesktopBrowserPane/useDesktopBrowserAttention.ts` | 常驻 attention 与面板状态订阅；晚挂载恢复请求，处理结束清除过期 attention |
| 修改 | [browser_panels.test.cjs](../../tests/electron/browser_panels.test.cjs) | role 身份、visibility、ws 地址、hold 不回收、reset 换新 targetId、confirm 超时 |
| 新增 | `tests/electron/opencli_worker_page.cjs`、`opencli_worker_page_driver.py`、`opencli_worker_page_fixture.tsx` | 真实宿主、共享 cookie、任务链路与取消重建；`--settings` 再验证生产设置组件、ConfigAdapter 补丁及 hidden 页的临时显示和恢复 |

**设置**

| 类型 | 文件 | 改动 |
| --- | --- | --- |
| 修改 | [config.yaml](../../jiuwenswarm/resources/config.yaml)、[config.py](../../jiuwenswarm/common/config.py) | `browser.opencli` 配置段与合并写入 |
| 新增 | `jiuwenswarm/common/browser_config.py` | 两条设置 RPC 共用的部分更新校验、配置合并、浏览器重启判断、只读诊断载荷 |
| 修改 | [app_web_handlers.py](../../jiuwenswarm/gateway/channel_manager/web/app_web_handlers.py)、[config_adapter.py](../../jiuwenswarm/server/runtime/gateway_adapter/config_adapter.py) | 读写配置、调用 `diagnose()`、变更后触发 spec 刷新 |
| 新增 | `features/settings/services/browserSettings.ts`、`modules/browser/OpenCLIStatusSetting.tsx` | 嵌套 RPC 与前端字段的转换、仅传已修改字段；使用共享 SettingRow 展示诊断 |
| 修改 | [browser/definition.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition.ts)、`SettingsSourceProvider.tsx`、`settingsSourceContract.ts`、[settingsContract.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/services/settingsContract.ts)、zh/en 语言包 | 声明开关及模式选择、注册字段与保存路径、状态文案 |
| 新增/修改 | `tests/unit_tests/extensions/opencli/test_opencli_settings.py`、Gateway/ConfigAdapter 单测、`frontend/tests/settingsRefactor.test.mjs` | 合并配置、无副作用诊断、任务快照、无需重启、前端补丁与旧载荷兼容 |

**Core（agent-core）**

| 类型 | 文件 | 改动 |
| --- | --- | --- |
| 修改 | [runtime.py](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py) | C1 外部工具分类、阶段、证据、完成判定（字段覆盖、结果数量、观察豁免）、`user_action_required` 结束为 `blocked`；可选 C2 的懒启动 |
| 可选修改 | [browser_state_context_processor.py](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py) | C2：第一次调用浏览器工具之前不采集页面 |
| 修改 | [browser_agent.py](../../../agent-core/openjiuwen/harness/subagents/browser_agent.py)、[tool_result_window_processor.py](../../../agent-core/openjiuwen/core/context_engine/processor/offloader/tool_result_window_processor.py) | 窗口化的工具名单纳入声明参与的外部工具；窗口处理器增加按工具的单条阈值。回读工具不用改 |
| 修改 | `../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_runtime_rail.py` | C1 测试项 |
| 修改 | `../agent-core/openjiuwen/harness/docs/specs/S_05_tools-contract.md`、`S_18_subagents-and-lifecycle.md` | 外部工具契约 |

## 12. 源码依据

| 主题 | 位置 |
| --- | --- |
| adapter 预导航与 stealth 注入 | [execution.ts:315-329](../../../opencli/src/execution.ts#L315-L329)、[cdp.ts:86-87](../../../opencli/src/browser/cdp.ts#L86-L87) |
| 上游超时不取消 adapter | [execution.ts:373](../../../opencli/src/execution.ts#L373) |
| 持久会话写命令的 daemon 请求、site session 解析 | [execution.ts:456-463](../../../opencli/src/execution.ts#L456-L463)、[execution.ts:591](../../../opencli/src/execution.ts#L591) |
| 运行控制参数 | [commanderAdapter.ts:60-67](../../../opencli/src/commanderAdapter.ts#L60-L67) |
| 扩展权限 | [manifest.json:6-15](../../../opencli/extension/manifest.json#L6-L15) |
| 错误契约 | [errors.ts](../../../opencli/src/errors.ts)、[commanderAdapter.ts:170-187](../../../opencli/src/commanderAdapter.ts#L170-L187) |
| 共享 partition 与面板 | [browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs)、[main.cjs:1215-1270](../../jiuwenswarm/channels/desktop/electron/main.cjs#L1215-L1270) |
| Browser Agent 工具集（无 shell）与窗口化名单 | [browser_agent.py:374-379](../../../agent-core/openjiuwen/harness/subagents/browser_agent.py#L374-L379)、[browser_agent.py:413](../../../agent-core/openjiuwen/harness/subagents/browser_agent.py#L413) |
| 阶段预算与豁免 | [runtime.py:2867](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L2867)、[runtime.py:4951](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L4951) |
| 结果窗口保留最新两条、单条阈值落盘 | [tool_result_window_processor.py:108](../../../agent-core/openjiuwen/core/context_engine/processor/offloader/tool_result_window_processor.py#L108)、[tool_result_budget_processor.py](../../../agent-core/openjiuwen/core/context_engine/processor/offloader/tool_result_budget_processor.py) |
| 不可重试的阻塞原因 | [runtime.py:208-219](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L208-L219) |
| 完成判定、观察豁免、结果数量 | [runtime.py:3854-3877](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L3854-L3877)、[runtime.py:5126](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L5126)、[runtime.py:4319](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L4319)、[runtime.py:5289](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L5289) |
| 首次页面采集 | [browser_state_context_processor.py:146](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py#L146) |
| 工具结果分类、幂等默认值、查询预算 | [runtime.py:666-680](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py#L666-L680)、[base.py:109](../../../agent-core/openjiuwen/core/foundation/tool/base.py#L109)、[task_tool.py:55-56](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L55-L56) |
| adapter 对运行时的依赖面、许可证 | [opencli/clis](../../../opencli/clis)、[opencli/LICENSE](../../../opencli/LICENSE) |
| 浏览器查询按对话轮次区分 | [task_tool.py:267-272](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L267-L272)、[task_tool.py:548](../../../agent-core/openjiuwen/harness/tools/subagent/task_tool.py#L548) |
| 子代理权限中断的限制 | [config_specs.py:606](../../jiuwenswarm/agents/swarm/config_specs.py#L606) |
