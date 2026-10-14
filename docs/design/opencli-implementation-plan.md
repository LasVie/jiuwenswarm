# OpenCLI 接入实现方案

> 更新：2026-10-14。状态：M1 开发联调和 M2 本地产品化已完成（§8.7、§8.8），迁移后的开发环境恢复及回归已通过（§8.9）。真实桌面应用、真实模型与 Bilibili 只读链路已验证，完整应用验收为部分通过，仍有任务分派与结果证据问题（§8.10）；M3 Code/Swarm 装配尚未开始，M4 完整评估尚未完成。当前进度的提交前复验见 §8.11；问题 A 的分派修复见 §8.12，复验通过（小样本）；问题 B、C 的修复及新发现 D、E 见 §8.13；B、C 的完整应用复验通过见 §8.14（B 混合路径未复验，C 的上下文重绑定待确认）。
>
> 依据：[架构方案](opencli-integration-architecture.md)（下称"设计"）、[CDP 调查](opencli-electron-cdp-research.md)。文中的行号基于 2026-09-28 的 swarm 与 agent-core 代码。
>
> 命名：本文沿用 `opencli_*`。如果采纳设计 §8.1 的中性命名，做一次统一替换即可，结构不变。

## 1. 工作包总览

| 编号 | 工作包 | 所在仓 | 依赖 | 对应设计阶段 | 规模 |
| --- | --- | --- | --- | --- | --- |
| WP0 | 连接验证（spike） | swarm（只有脚本和夹具，不进产品） | §3 契约冻结 | A | M |
| WP1 | 运行包打包与 Electron Node 定位 | swarm | WP0 | A、B | M |
| WP2 | 命令目录与 OpenCLI 来源 | swarm | WP1 | B | M |
| WP3 | Electron 工作页与宿主接口 | swarm（Electron） | WP0 | B | L |
| WP4 | 工作页客户端 | swarm | WP3 | B | M |
| WP5 | 两个工具与待核实记录 | swarm | WP2、WP4；§3 契约 | B | L |
| WP6 | 路由提示、启用判断与装配 | swarm | WP5 | B → D | M |
| WP7 | Core C1 | agent-core | §3 契约 | C | L |
| WP8a | 最小界面：确认条、人工处理横幅与按钮、attention 切换 | swarm（前端 + Electron） | WP3 | B | M |
| WP8b | 其余界面：hidden 模式、运行状态、样式与文案完善 | swarm（前端） | WP8a | D | S |
| WP9 | 设置与诊断 | swarm | WP6 | D | S |
| WP10 | Core C2（可选） | agent-core | WP7 | — | M |
| WP11 | 端到端验证与评估 | 全部 | 以上 | E | M |

规模是粗估：S 约 1–2 人日，M 约 3–5 人日，L 约 6–10 人日。WP0 完成后再修正。

```
§3 契约冻结 → WP0 ─┬→ WP1 → WP2 ─────────┐
                   └→ WP3 → WP4 ──────────┼→ WP5 → WP6 ─→ M1 验收 → WP9、WP8b、Code/Swarm 装配 → WP11
                         WP3 → WP8a ──────┤
               §3 契约冻结 → WP7（本地 Core）┘
```

**顺序**：先按本文 §3 冻结 WP5 与 WP7 之间的契约（工具声明、结果字段、剩余时间入口、窗口阈值），再做 WP0。WP5 和 WP7 依据同一份契约并行开发。

**合入与验收是两回事**：

- **合入**：代码可以分批合入，默认关闭，不影响现有功能。
- **可用闭环（M1）的验收**：必须同时具备 WP1–WP7 和 WP8a。
  - 缺少 WP7，describe/run 仍会受原有阶段预算和页面规则的约束，`needs_user` 也不会确定地结束任务，工具还拿不到剩余时间。
  - 缺少 WP8a，写确认没有界面接收，最后只能超时。
- **本地开发依赖**：全部开发与验收先在本地完成。Swarm 的 `pyproject.toml` 通过 `[tool.uv.sources]` 将 `openjiuwen` 指向同级的 `../agent-core`，使用可编辑安装；`uv.lock` 同步记录这个来源。正常 `uv sync` / `uv run` 使用本地 Core，无需跳过依赖同步。Core SDK 发布不作为任何开发里程碑的前置条件，交付方式以后再定。

## 2. 代码布局

**swarm 仓（新增）**

```
third_party/opencli/package.json, package-lock.json   固定 @jackwener/opencli 版本
scripts/update_opencli_runtime.py                     生成运行包 zip、清单与命令目录
scripts/verify_opencli_bundle.py                      校验运行包（在 Electron Node 模式下运行）
jiuwenswarm/resources/runtime/opencli/                opencli-<版本>.zip、manifest.json
jiuwenswarm/common/browser_config.py                  两条设置 RPC 共用的字段校验、合并、重启判断与诊断载荷
jiuwenswarm/common/bundled_node_runtime.py            从 playwright_mcp_runtime.py 抽出的通用解压与缓存逻辑
jiuwenswarm/extensions/opencli/
  __init__.py          browser_agent_contribution()、diagnose()
  gate.py              启用判断；从 RuntimeSettings 取出会话、成员与 Electron Node
  catalog.py           CommandSpec、ArgSpec、Catalog、CommandSource 协议
  sources/opencli.py   OpenCLI 来源：运行包、目录、参数拼装、执行、错误映射
  worker_page.py       工作页状态机与宿主客户端
  pending.py           会话级待核实记录
  tools.py             opencli_describe、opencli_run
  prompt.py            路由提示段（中文与英文）
tests/unit_tests/extensions/opencli/                  上述模块的单元测试（pytest 只收集 tests/）
tests/electron/opencli_smoke.cjs                      WP0 的连接验证脚本（Electron 主进程）
tests/electron/opencli_smoke_driver.py                WP0 中经真实 Python 工具栈执行的部分
tests/electron/opencli_worker_page.cjs                WP11 的端到端验证
```

**swarm 仓（修改）**：

- 开发依赖：`pyproject.toml`、`uv.lock`，将 Core 来源固定为 `../agent-core` 的可编辑安装；
- Electron：`browser_panels.cjs`、`main.cjs`、`preload.cjs`；
- 前端：`DesktopBrowserPane`、`types/electron.ts`、浏览器设置模块与语言包；
- 装配点：`interface_deep.py`、`interface_code.py`、`code_subagents.py`；
- 配置：`config.yaml`、`config.py`，以及 Gateway 的浏览器设置处理；
- 其他：`playwright_mcp_runtime.py`（改为调用通用解压函数）、`electron_sideview.py`（读取 Electron Node）、打包脚本。

**agent-core 仓（修改）**：`runtime.py`（C1）、`tool_result_window_processor.py`、`browser_agent.py`、规约 S_05 与 S_18；做可选的 C2 时还要改 `browser_state_context_processor.py`。

## 3. 接口与数据结构（冻结的契约）

### 3.1 命令目录

```python
@dataclass(frozen=True)
class ArgSpec:
    name: str
    type: str                      # 上游的 str / int / bool 等
    required: bool
    positional: bool
    choices: tuple[str, ...] = ()
    default: Any = None
    help: str = ""

@dataclass(frozen=True)
class CommandSpec:
    source: str                    # "opencli"
    site: str
    command: str
    description: str
    access: Literal["read", "write"]
    needs_browser: bool            # 等于 manifest 的 browser 字段，决定是否占用工作页、是否传 --site-session
    args: tuple[ArgSpec, ...]
    columns: tuple[str, ...]       # 输出列，用于证据字段映射
    domain: str = ""
```

- 目录在**构建期**生成，成为运行包里的 `catalog.json`（WP1）。运行期只读取这个文件，再按 `enabled_sites` 过滤。
- `Catalog` 提供 `sites()`、`site_summary(site)`、`get(site, command)`、`merge(*catalogs)`。`merge` 为以后接入自有来源预留，规则是自有来源优先。

### 3.2 命令来源（执行器）

```python
class CommandSource(Protocol):
    id: str
    def catalog(self) -> Catalog: ...
    async def run(self, spec: CommandSpec, values: list[tuple[ArgSpec, str]], *,
                  page_endpoint: str | None, timeout_s: float, cwd: Path) -> RunOutcome: ...

@dataclass
class RunOutcome:
    started: bool                  # 进程是否已启动
    category: Literal["ok", "empty", "invalid_args", "needs_user",
                      "env_unavailable", "timeout", "error"]
    rows: list[dict] | dict | None
    exit_code: int | None = None
    killed: bool = False           # 超时或取消后由我们结束了进程树
    output_too_large: bool = False # stdout 超过读取上限
    error_code: str = ""           # 上游 error.code，如 AUTH_REQUIRED
    error_message: str = ""
    error_help: str = ""

class CommandCancelled(asyncio.CancelledError):
    outcome: RunOutcome            # 来源结束执行后，带回 started/killed，随后继续传播取消
```

取消不会返回普通工具结果。来源先结束执行，以 `CommandCancelled` 带回事实；工具把已启动的写命令保存为待核实，再由工作页客户端完成租约释放和页面重建。页面分配、子进程创建与收尾期间的取消也必须保有资源所有权，不能因为调用栈提前退出而漏掉清理。

OpenCLI 的退出码映射：

| 退出码 | category |
| --- | --- |
| 0 | ok |
| 66 | empty |
| 2 | invalid_args |
| 77 | needs_user |
| 69、78 | env_unavailable |
| 75 | timeout |
| 命令超时后主动结束进程 | timeout，并且 `killed=true` |
| 任务被取消 | 抛出 `CommandCancelled`，不生成普通返回；其中 outcome 为 error / CANCELLED，记录 started/killed |
| stdout 超过 16MiB | error，并且 `output_too_large=true` |
| 其他 | error |

### 3.3 `opencli_run` 的返回结果

```json
{
  "ok": true,
  "executed": "yes | no | unknown",
  "reason": "ok | empty | invalid_args | needs_user | not_confirmed | env_unavailable | timeout | error",
  "data": [],
  "truncated": false, "total_rows": 10, "returned_rows": 10,
  "observed_count": 10,
  "extracted": {},
  "field_provenance": {},
  "source": {"provider": "opencli", "command": "bilibili/search", "page_url": "https://..."},
  "user_action_required": {"reason": "captcha | login_required | user_intervention_required", "instructions": "..."},
  "pending_writes": [],
  "error": "..."
}
```

字段规则：

- `executed` 只在写命令上出现；`error` 只在 `ok=false` 时出现。
- 不使用 `status` 字段，避免被 runtime 的结果分类误判为失败。
- 工作页的 ws 地址不出现在结果里。
- **大小上限**：把整个结果序列化成模型可见的文本后，按落盘时的方式（作为 JSON 字符串、`ensure_ascii=False`）转义，再计算 UTF-8 字节数，上限 7MiB。超过时按整行截断 `data`，并填写 `truncated`、`total_rows`、`returned_rows`。这样可以保证落盘文件（再加上 `indent=2` 和外层封装）低于回读工具的 8MB 上限（[offload_recall.py:191](../../../agent-core/openjiuwen/harness/tools/browser_move/offload_recall.py#L191)），任何 handle 都能读回来。

### 3.4 工具声明

| 位置 | 键 / 属性 | 值 | 用于 |
| --- | --- | --- | --- |
| `ToolCard.properties`（键名在 Core 评审时定稿） | `browser_runtime.role` | `discovery` / `action` | describe / run |
| 同上 | `browser_runtime.windowed` | `true` | run |
| 同上 | `browser_runtime.inline_limit_chars` | `8000` | run |
| `ToolCard` | `idempotent` | describe 为 `True`；run 保持默认 `False` | — |
| 工具类属性 | `accepts_tool_callback_context = True` | AbilityManager 只向声明了它的工具注入 `_tool_callback_context`（[ability_manager.py:1452](../../../agent-core/openjiuwen/core/single_agent/ability_manager.py#L1452)） | run |

**剩余时间入口**：由 WP7 提供公开函数 `browser_remaining_time(callback_context) -> float | None`。工具把 `kwargs["_tool_callback_context"]` 传给它，不直接读 `extra` 里的内部键。

### 3.5 待核实记录

```json
{"id": "uuid", "site": "bilibili", "command": "follow", "args_digest": "sha256...",
 "args_preview": "uid=123", "reason": "timeout", "created_at": "2026-09-28T10:00:00Z"}
```

- 按（会话、成员）分组，持久化到 `<用户数据目录>/runtime_state/opencli/pending/<session_id>.json`。
- 清除的时机：用户在确认条上对同一命令作出决定，或者记录过期（默认 7 天，待定）。

### 3.6 工作页状态

| 当前状态 | 事件 | 下一状态 | 宿主动作 |
| --- | --- | --- | --- |
| IDLE | run 开始 | RUNNING | 申请租约 |
| RUNNING | 正常结束 | IDLE | 释放租约 |
| RUNNING | 返回 needs_user | AWAITING_USER | 释放租约；以新的阻塞 ID 执行 hold；attention |
| RUNNING | 超时或取消 | CANCELLING | 结束进程树 |
| CANCELLING | 进程退出 | NEEDS_RESET | 释放租约 |
| AWAITING_USER | run，宿主查询结果为 `resolved` | RUNNING | 解除 hold，申请租约 |
| AWAITING_USER | run，宿主查询结果为 `pending` | AWAITING_USER | 无，run 直接返回 `executed=no` + `needs_user`，不导航页面 |
| AWAITING_USER | run，宿主查询结果为 `abandoned` 或 `expired` | NEEDS_RESET → RUNNING | 解除 hold，reset，申请租约 |
| NEEDS_RESET | run | RUNNING | reset，申请租约 |

**只有用户在侧栏按钮上的决定，才能把 AWAITING_USER 推进到可用状态。** 新的 invocation、自动继续、团队重新派发都不算。

### 3.7 宿主 HTTP 接口

沿用现有的 loopback 地址、Bearer token 和"拒绝浏览器 Origin"规则。请求体和响应都是 JSON，请求体上限 64KB。

| 请求 | 响应 |
| --- | --- |
| `POST /{session}?member=&label=&lease=&pid=&role=opencli&visibility=sidebar` | `{panelId, sessionId, memberId, label, targetId, webSocketDebuggerUrl}` |
| `DELETE /{session}?member=&lease=&pid=&role=opencli` | `{released: true}` |
| `POST /{session}/hold?member=&role=opencli`，请求体 `{block_id, reason, instructions, ttl_s}` | `{held, until}`；同时发出 attention |
| `POST /{session}/reset?member=&role=opencli` | `{targetId, webSocketDebuggerUrl}` |
| `POST /{session}/confirm?member=&role=opencli`，请求体 `{command, args, warnings, timeout_s}` | `{decision: "approve" / "reject" / "timeout"}`（长轮询） |

hold 的决定（resolved / abandoned）只能由渲染进程通过 IPC 写入（§3.8），HTTP 接口不能写入。保留由宿主在分配时强制执行：用户未决定时分配返回 409 `{error: "awaiting_user", reason, instructions}`；`resolved` 时自动解除并复用该页；`abandoned` 或过期时先重建页面再分配。因此 Python 侧不需要查询保留状态，AgentServer 重启也不会丢失保留。

### 3.8 Electron IPC

| 方向 | 通道 | 数据 |
| --- | --- | --- |
| 主进程 → 渲染进程 | `browser:attention` | `{sessionId, panelId, blockId, kind, reason, instructions}` |
| 主进程 → 渲染进程 | `browser:confirm-request` | `{requestId, sessionId, panelId, command, args, warnings, expiresAt}` |
| 渲染进程 → 主进程 | `browser:confirm-response`（invoke） | `(requestId, decision)` |
| 渲染进程 → 主进程 | `browser:hold-decision`（invoke） | `(sessionId, panelId, blockId, decision)`，decision 为 `resolved` 或 `abandoned` |

preload 的 `browser` 对象新增 `onAttention`、`onConfirmRequest`、`respondConfirm`、`decideHold`；面板状态新增 `role` 字段。

### 3.9 配置与诊断

```yaml
browser:
  opencli:
    enabled: false
    worker_page: sidebar      # sidebar | hidden
    enabled_sites: null
```

`diagnose(config, electron_node, node_version=...)` 按状态返回 `{state, version, node_version, site_count, detail}` 的适用字段。`state` 为 `off`、`available`、`runtime_missing`、`electron_node_unavailable`、`unsupported_browser_mode` 或 `no_sites_enabled`。最后一种表示运行包有效，但站点限制后没有可用命令。

设置诊断只检查文件、运行包和目录哈希，并读取宿主报告的 Node 版本；不解压、不启动进程、不创建工作页，也不改环境变量。开关关闭或配置外部浏览器时不读取 Electron 发现信息。实际任务装配仍通过 `prepare_runtime()` 验证 Node 的执行能力。

## 4. 各工作包

### WP0 连接验证

目标：在写产品代码之前，确认设计依赖的外部前提。

1. 按 WP1 的 `third_party/opencli/package.json` 把 1.8.8 安装到临时目录。
2. 编写 fixture adapter，放在私有 HOME 下的 `.opencli/clis/fixture/`。上游会从 homedir 加载用户 adapter，正好借私有 HOME 注入测试 adapter；产品运行时的私有 HOME 下没有这个目录。需要的命令：
   - `fixture/read`：cookie 策略，预导航到本地 fixture 服务；
   - `fixture/list`：返回 N 行，N 可调，用来做大结果测试；
   - `fixture/public`：`browser=false`，不需要浏览器；
   - `fixture/write`：persistent、`access=write`；
   - `fixture/captcha`：抛出 `AuthRequiredError`；
   - `fixture/slow`：在页面里持续派发 fetch。
3. 复用 [browser_fixture.cjs](../../tests/electron/browser_fixture.cjs) 启动带 CDP 的 Electron，在同一个 partition 里建两个 WebContentsView，分别模拟 Browser Agent 页和工作页。
4. 用 `tests/electron/opencli_smoke.cjs` 逐项验证[调查文档 §7](opencli-electron-cdp-research.md#7-接口定稿前的验证项)，另外还要确认：
   - **Electron Node 模式**：开发版和打包版都用 `ELECTRON_RUN_AS_NODE=1 <electron 可执行文件>` 运行 OpenCLI，并记录 `process.versions.node`，要求不低于 20.18.1。整个过程要在**系统 PATH 中没有 node** 的环境下做一遍。
   - **`--site-session` 的反例**：`fixture/public` 加上 `--site-session` 会报未知参数；不加则正常。
   - **其他记录项**：Electron 43 下页面级 ws 地址的格式、Node 冷启动耗时、运行包体积。
5. 把结论写回调查文档 §7。

**完成标准**：每一项都通过；不通过的项有明确的补丁方案，并据此决定是否需要自维护发行物。

### WP1 运行包打包与 Electron Node 定位

照搬现有 Playwright MCP 运行包的做法（[update_playwright_mcp_runtime.py](../../scripts/update_playwright_mcp_runtime.py)、[playwright_mcp_runtime.py](../../jiuwenswarm/common/playwright_mcp_runtime.py)）。

- `third_party/opencli/package.json` 只有一个依赖 `"@jackwener/opencli": "1.8.8"`（精确版本），并提交 lock 文件。
- `scripts/update_opencli_runtime.py` 按顺序做四件事：
  1. 在临时目录执行 `npm ci --omit=dev`；
  2. 在私有 HOME 下执行入口 `entry.mjs --version`，核对版本。入口是 `third_party/opencli/entry.mjs`，打进 zip 根目录，清单的 `cli_relative_path` 指向它（原因见 §8.6）；
  3. 生成 `catalog.json`：读取 `cli-manifest.json`，去掉 [electron-apps.ts](../../../opencli/src/electron-apps.ts) 登记的桌面应用站点、`strategy=local` 的命令、外部 CLI 透传条目，再转换成 §3.1 的结构；
  4. 打包成 `jiuwenswarm/resources/runtime/opencli/opencli-<版本>.zip`，并写 `manifest.json`，字段有 version、archive_sha256、cli_path、catalog_path、node_min="20.18.1"。
- 新建 `jiuwenswarm/common/bundled_node_runtime.py`：把 `materialize_bundled_runtime`（安全解压、哈希校验、缓存标记）抽成带参数的通用函数，Playwright MCP 改为调用它，行为不变。
- **Electron Node 定位**（不使用只查 PATH 的 `resolve_node_executable`）：
  - [main.cjs](../../jiuwenswarm/channels/desktop/electron/main.cjs)：把 `process.execPath` 以 `JIUWENSWARM_ELECTRON_NODE`、`process.versions.node` 以 `JIUWENSWARM_ELECTRON_NODE_VERSION` 写入 AgentServer 启动环境和发现文件（与 `cdp_endpoint`、`target_resolver` 放在一起）。开发版也使用自己的 Electron。
  - [electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py)：读取这个值，发现文件过期时一并失效。
  - `OpenCLISource.prepare()` 执行 `ELECTRON_RUN_AS_NODE=1 <exe> -p process.versions.node` 核对版本，不满足就在诊断里显示 `electron_node_unavailable`。
- 确认打包脚本（[build-electron-exe.ps1](../../scripts/build-electron-exe.ps1) 及对应的 `.sh`）和 `MANIFEST.in` 包含了 `resources/runtime/opencli/`。

**测试**：解压与哈希校验、缓存复用、Electron Node 的定位与版本判定（包括 PATH 里没有 node 的情况）、catalog 过滤规则、Playwright MCP 回归。

### WP2 命令目录与 OpenCLI 来源

`catalog.py`：定义 §3.1 与 §3.2 的数据结构，提供 `Catalog.load(path)`、`filter(enabled_sites)` 和 `merge`。

`sources/opencli.py` 中的 `OpenCLISource`：

- **`prepare_runtime()`**：任务装配时解压运行包、执行并核对 Electron Node、加载目录。结果按进程缓存，失败时抛出带原因的异常。
- **`inspect_runtime()`**：设置诊断使用的只读检查，核对文件和宿主版本，不调用 `prepare_runtime()`。
- **`build_argv(spec, args)`**：
  - 具名参数写成 `--name=value`，布尔值写成 `--flag=true` / `--flag=false`（WP0 已确认）；
  - 所有命令都追加 `-f json --trace off`；
  - **只有 `spec.needs_browser` 为真时**才追加 `--site-session ephemeral`，因为上游只给 `browser=true` 的命令注册了这个选项（[commanderAdapter.ts:63-68](../../../opencli/src/commanderAdapter.ts#L63-L68)）；
  - 位置参数按 ArgSpec 的顺序放在最后的 `--` 之后。以 `-` 开头的位置参数不这样放会报"未知选项"；可选具名参数（`--name [value]`）也不会把以 `-` 开头的下一个参数当作值；
  - `normalize_args` 拒绝"跳过前面的可选位置参数、只给后面的"：位置参数按顺序匹配，值会错位（目录中有 `xianyu/messages`、`xianyu/reply` 两条）。
- **`run(...)` 的前置检查**：需要浏览器的命令没有工作页地址时直接返回 `env_unavailable`，不启动进程。
- **`build_env(page_endpoint)`**：
  - 从最小白名单起步（PATH、SystemRoot、TEMP/TMP、LANG 等），不继承完整的 `os.environ`；
  - 设置 `ELECTRON_RUN_AS_NODE=1`；
  - 设置 `HOME` / `USERPROFILE` 为 `<用户数据目录>/runtime_state/opencli/home`，并设置 `OPENCLI_CACHE_DIR`、`OPENCLI_CONFIG_DIR`、`OPENCLI_SITE_SESSION=ephemeral`；
  - 需要浏览器时设置 `OPENCLI_CDP_ENDPOINT`；
  - 不设置 `OPENCLI_PROFILE`、`OPENCLI_CDP_TARGET`、`OPENCLI_DAEMON_PORT`。
- **`run(...)`**：
  - 可执行文件是 Electron，第一个参数是 `cli_path`；用 `asyncio.create_subprocess_exec` 启动。Windows 下使用 `CREATE_NEW_PROCESS_GROUP`，结束时执行 `taskkill /T /F /PID`；POSIX 下使用 `start_new_session=True` 和 `os.killpg`。
  - stdout 读取上限 16MiB，超过就结束进程，返回 `output_too_large`；stderr 上限 1MiB。
  - 超时后结束整个进程树，最多等 5 秒让它退出。
  - stdout 按 JSON 解析，stderr 用 `yaml.safe_load` 解析，最后产出 `RunOutcome`。

**测试**：
- 参数拼装：`--name=value`、`--` 之后的位置参数、固定参数不可覆盖、跳过可选位置参数被拒绝；`fixture/public` 不带 `--site-session`；需要浏览器的命令没有地址时不启动。
- 环境白名单。
- 退出码映射。
- 超时后结束进程树（用 `fixture/slow`）。
- stdout 超过上限时的处理。

### WP3 Electron 工作页与宿主接口

[browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs)：

- `panelIdentity(sessionId, memberId, label, role = '')`：role 非空时，panelId 由 `[sid, member, role]` 的哈希生成；role 为空时保持原算法，兼容已有面板和 lastUrl 记录。
- `createTargetHandler` 新增注入项 `pageEndpoint`、`holdView`、`holdState`、`resetView`、`requestAttention`、`requestConfirm`：
  - 解析 `role` 和 `visibility` 参数；
  - 按路径后缀和 HTTP 方法分发 hold（POST、GET）、reset、attention、confirm；
  - POST 的响应增加 `webSocketDebuggerUrl`。
- `evictionCandidates`：排除处于 hold 的条目；空闲的 `role=opencli` 条目排在最前，优先回收。

[main.cjs](../../jiuwenswarm/channels/desktop/electron/main.cjs)：

- 视图条目新增 `role`、`hidden`、`hold: {blockId, state, until}`、`attention` 字段。
- `allBrowserPanels()` 不下发 hidden 且没有 attention 的条目。
- `initializeBrowserView`（L1275）：`role=opencli` 的页面既不还原也不记录 lastUrl，从 `about:blank` 开始。
- 新增 `resetBrowserView(identity)`：关闭 WebContents、移除条目，再调用 `ensureBrowserView`（L1215）重建，返回新的 targetId。
- 新增 `requestConfirm`：生成 requestId，发送 `browser:confirm-request`，在 `ipcMain.handle('browser:confirm-response')` 中完成；超时返回 `timeout`；窗口关闭时所有等待中的请求都按 `timeout` 结束。
- 新增 `ipcMain.handle('browser:hold-decision')`：只有 blockId 与当前 hold 一致时才写入 `resolved` 或 `abandoned`，旧阻塞的迟到点击会被忽略。
- 新增 `requestAttention`：标记 attention，调用 `emitBrowserPanels()`（L1091），并发送 `browser:attention`。
- hold 到期由定时检查把状态置为 `expired`，只解除回收保护，不关闭页面。
- `startBrowserTargetResolver`（L1486）传入上述新函数，以及 `pageEndpoint = targetId => ws://127.0.0.1:<cdpPort>/devtools/page/<targetId>`。
- 把 `process.execPath` 写入 AgentServer 环境和发现文件（见 WP1）。

[preload.cjs](../../jiuwenswarm/channels/desktop/electron/preload.cjs)：新增 `onAttention`、`onConfirmRequest`、`respondConfirm`、`decideHold`。

**测试**：
- [browser_panels.test.cjs](../../tests/electron/browser_panels.test.cjs) 新增用例：role 身份、visibility、ws 地址、hold 期间不回收、hold 状态查询、过期的 blockId 被忽略、reset 后 targetId 变化、confirm 超时与批准。
- [test_desktop_electron_contract.py](../../tests/unit_tests/test_desktop_electron_contract.py) 同步新增的 IPC 通道。

### WP4 工作页客户端（`worker_page.py`）

- **绑定信息**：从 Browser Agent 的 RuntimeSettings 读取 resolver 地址、token、会话和成员，来源是 `settings.mcp_cfg.params["env"]` 中的 `PLAYWRIGHT_MCP_TARGET_RESOLVER`、`PLAYWRIGHT_MCP_SESSION_ID`、`PLAYWRIGHT_MCP_MEMBER_ID`。token 目前经由 `PLAYWRIGHT_MCP_ENV_JSON` 传递（[electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py) `_apply_discovered_env`），实现时核对它在 params env 里的实际位置。
- **进程内注册表**：以（会话、成员）为键，值是 `PageSlot{state, lock, block_id, target_id}`。
- **`async with slot.use(timeout)`**：先拿锁，再按 §3.6 处理当前状态：
  - AWAITING_USER：先用 `GET /hold` 查询；`pending` 时抛出 `AwaitingUser`，由工具转成 `executed=no` + `needs_user`；
  - NEEDS_RESET：先 reset；
  - 然后申请工作页、交出 ws 地址，退出时释放租约。
- **其他方法**：`mark_awaiting_user(reason, instructions)`（生成 block_id、执行 hold、发出 attention）、`mark_needs_reset()`、`confirm(command, args, warnings, timeout_s)`。
- **已知假设**：桌面端只有一个 AgentServer 进程，进程内的锁就够用；以后如果出现多个进程共用一个宿主，改成由宿主加锁。

**测试**：用本地 HTTP 桩模拟宿主，覆盖全部状态转换、并发排队、`pending` 时不申请工作页、过期与放弃后 reset。

### WP5 工具（`tools.py`、`pending.py`）

`OpenCLIDescribeTool`：

- **工具卡**：名称 `opencli_describe`；输入 `{site: string, command?: string}`；`idempotent=True`；`properties` 声明 `role=discovery`。
- **站点级输出**：命令名、说明、读/写、是否需要浏览器，以及该站点的待核实项。
- **命令级输出**：参数定义和输出列。

`OpenCLIRunTool`：

- **工具卡**：输入 `{site, command, args: object}`；`idempotent=False`；`parallel_safe=False`；`properties` 声明 `role=action`、`windowed`、`inline_limit_chars`。类属性 `accepts_tool_callback_context = True`。
- **调用流程**（对应设计 §4.2）：
  1. 从构造时注入的绑定取得会话和成员；从 `kwargs["session"]` 取得 Browser Agent 的子会话；从 `kwargs["_tool_callback_context"]` 调用 `browser_remaining_time()` 取得剩余时间。
  2. 准入与参数校验：按 ArgSpec 检查类型、必填和可选值，未知参数名一律拒绝。
  3. 写命令：用 `pending.find(site, command)` 生成提醒，再调用 `slot.confirm(...)`，超时为 min(120 秒, 剩余时间 − 30 秒)。拒绝或超时即返回 `executed=no`。
  4. 需要浏览器的命令：通过 `async with slot.use()` 拿到 ws 地址；遇到 `AwaitingUser` 时返回 `executed=no` + `needs_user`，并重复一遍处理说明。
  5. 调用 `source.run(...)`，命令超时为 min(120 秒, 剩余时间 − 10 秒)。
  6. 按 §3.3 组装结果：
     - 写命令只要进程已启动，除退出码 0 以外一律为 `executed=unknown`，并写入 pending；
     - `needs_user` 时调用 `slot.mark_awaiting_user`，并附上 `user_action_required`；
     - 如果我们主动结束了进程，调用 `slot.mark_needs_reset`。
  7. 组装证据：`extracted` 取第一行、按列名给出字段；`observed_count` 为实际行数；`field_provenance` 指向命令和页面 URL。
  8. 按 §3.3 的大小上限截断。
- **`render_for_llm`**：输出紧凑 JSON，只包含分类、数据和提醒；ws 地址与内部标识不进入模型可见的文本。

**测试**：
- 设计 §4.3 分类表每一行一个用例；写命令进程启动后的任何失败都是 `unknown`；未知参数被拒绝；模型可见文本里没有 ws 地址；待核实项在新任务的 describe 和确认条上都会出现。
- **大小边界**：转义后在 7MiB 上下的结果；引号密集的 JSON 行；大量中文；确认截断后落盘文件小于 8MB，并且 `browser_recall_offload` 能读回。这一项与 WP7 联合验证。
- **经过真实调用链**：工具注册进 Browser Agent，由模型的工具调用触发，确认 AbilityManager 注入了 `_tool_callback_context`、剩余时间可以读到。不能只直接调用工具来测。

### WP6 路由提示、启用判断与装配

- **`gate.py`**：`resolve_binding(settings) -> Binding | None`，只有 MCP env 里同时有 resolver 和 session、并且拿得到 Electron Node 时才返回绑定。Swarm 配置了外置 Chrome 时，这些 env 已被剥离（[browser_runtime.py](../../jiuwenswarm/agents/swarm/browser_runtime.py)），自然返回 None。
- **`browser_agent_contribution(settings, config) -> Contribution | None`**：依次检查 `browser.opencli.enabled`、绑定、运行包（`prepare()` 失败即返回 None），全部满足时返回 `Contribution(tools=[describe, run], prompt_text)`。
- **装配**：三处调用同一个 helper `apply_opencli_contribution(spec, config)`，它做两件事：`spec.tools += contribution.tools`，以及把 `prompt_text` 追加到 `spec.system_prompt` 末尾。spec 的 `system_prompt` 和 `tools` 在实例化时会传给 `create_browser_agent`，所以不需要额外的 rail。三处位置都在 settings 最终确定之后、`subagents.append` 之前：
  - [interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py)：L4755 构建之后，`apply_session_sideview_target` 之后（M1 只接这一处）；
  - [interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py)：L2051 构建之后，同样的位置（M3）；
  - [code_subagents.py](../../jiuwenswarm/agents/swarm/providers/code_subagents.py)：`apply_swarm_browser_settings` 之后（M3）。
- **`prompt.py`**：中文、英文两版，内容是设计 §6.2 的规则加上按目录生成的站点名列表。提示中要写明：`needs_user` 时需要用户到侧栏点「已完成，继续」。用单测把长度限制在约 1k token 以内。
- **配置变更**：复用现有"配置更新后重建 Agent"的入口（实现时定位具体函数），开关变化后，下一次构建的 spec 生效。

**测试**：零暴露对比（"未安装"和"已关闭"两种状态下，spec 的 `system_prompt` 与 `tools` 完全一致）；装配入口；外置 Chrome 下不贡献。

### WP7 Core C1（agent-core）

[runtime.py](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py) 中的 `BrowserRuntimeRail`：

1. **读取工具角色**：新增 `_external_tool_role(ctx, tool_name)`。`ctx.agent.ability_manager.get(tool_name)` 返回的已经是 Card，没找到时返回 None（[ability_manager.py:930](../../../agent-core/openjiuwen/core/single_agent/ability_manager.py#L930)），所以直接读取 `card.properties`。取不到 Card 或没有声明时返回 None，原有逻辑完全不变。
2. **执行前**（`_prepare_tool_call` → `_consume_phase_budget`，L2867 / L4706）：
   - discovery 与 `_is_replan_exempt_tool`（L4951）同样处理，不计预算；
   - action 归入 `_BROWSER_PHASE_DEFINITIONS` 中新增的 `external` 阶段，单独设预算，按"工具 + 参数"签名检测重复。
3. **执行后**（`after_tool_call`，L2956）：
   - 外部工具的 `state_changed=False`；
   - 不走"字符串结果套上 `page_state`"的分支（L2997-3003）；
   - 只从 dict 结果中的 `extracted` 记录证据，来源取结果里的 `source`。
4. **完成判定**：
   - 用 `observed_count` 更新 `observed_result_count`（L5289 附近）；
   - 外部证据登记为 `external_observation`，`_task_observations`（L5119）同时认它，这样 `_advisory_missing_fields`（L5126）对纯外部证据也生效。
5. **需要用户处理**：结果带 `user_action_required` 时，把任务状态置为 `blocked`。blockers 用结果给出的原因，并且必须属于 `_BROWSER_NON_RETRYABLE_BLOCKER_TOKENS`（L208）；`terminal_reason` 设为 `external_user_action_required`。
6. **剩余时间**：提供公开函数 `browser_remaining_time(callback_context)`，从任务截止时间和本次调用截止时间中取较早者；读取不到时返回 None。

[tool_result_window_processor.py](../../../agent-core/openjiuwen/core/context_engine/processor/offloader/tool_result_window_processor.py)：配置新增 `inline_limit_by_tool: dict[str, int]`。窗口内的结果只要超过该工具的阈值，也立即落盘；落盘格式和前缀不变，`browser_recall_offload` 不用改。

[browser_agent.py](../../../agent-core/openjiuwen/harness/subagents/browser_agent.py)（L374 附近）：窗口化名单 = 原有的五个工具 + 声明了 `windowed` 的外部工具；各工具声明的 `inline_limit_chars` 汇总成 `inline_limit_by_tool`。

规约：在 S_05、S_18 中补充外部工具契约。规约和测试一律使用一个假的外部工具来写，agent-core 里不出现 "opencli"。

**测试**：
- 设计 §7.2 列出的各类用例，都要**经过真实的 AbilityManager 调用链**（工具注册进 DeepAgent，由模型的工具调用触发）。
- 覆盖 `get()` 返回 None 的情况，以及 `_tool_callback_context` 只注入给声明了 `accepts_tool_callback_context` 的工具。
- Playwright 路径回归：现有 browser_move 测试全部通过，没有声明 properties 的工具行为不变。

### WP8a 最小界面（M1 的一部分）

- **[App.tsx](../../jiuwenswarm/channels/web/frontend/src/App.tsx)**：通过常驻 `useDesktopBrowserAttention` 接收当前会话的 attention，并恢复已有的 `pendingConfirm/hold`；需要用户处理时重新打开浏览器页签、展开侧栏，将目标面板传给 DesktopBrowserPane。
- **[DesktopBrowserPane](../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane/index.tsx)**：
  - 面板数据增加 role；默认选中时排除 `role=opencli`。
  - 根据传入的 attention 选中对应面板；根据面板的 `hold` 显示原因、操作说明，以及「已完成，继续」和「放弃」两个按钮。
    - 「已完成，继续」：先调用 `decideHold(..., 'resolved')`，再调用前端现有的发送消息函数，发送一条固定的本地化文案；
    - 「放弃」：调用 `decideHold(..., 'abandoned')`。
  - 根据面板的 `pendingConfirm` 显示确认条，包括命令、参数、待核实提醒、倒计时和确认/拒绝按钮，点击后调用 `respondConfirm`。
- **其他文件**：`types/electron.ts` 补类型，zh/en 语言包补文案。
- **测试**：前端单测覆盖默认选中逻辑、横幅按钮的调用顺序、确认条交互。

### WP8b 其余界面

- hidden 模式：attention 和确认时临时显示面板，结束后宿主恢复隐藏，前端恢复之前选中的成员页面；用户主动切换页面时保留其选择。
- "运行中"状态：复用 `browser:state-changed` 的 loading 和 busy 租约状态，覆盖不导航的 adapter。
- 每个任务保留自己的工作页模式快照；同一会话/成员的任务共享页面锁和重建标记，后续任务读取新模式。
- 样式与文案的完善；按仓内约定做界面检查。

### WP9 设置与诊断

- `config.yaml` 增加 `browser.opencli` 段（§3.9）。
- `update_browser_in_config`（[config.py:826](../../jiuwenswarm/common/config.py#L826)）支持嵌套 `opencli` 字段的合并写入。
- Gateway 和 AgentServer ConfigAdapter 复用 `common/browser_config.py`：`path.get` 返回完整浏览器设置和诊断，`path.set` 接收字段补丁，嵌套合并 `opencli`，保留未提交的 `enabled_sites`。
- 仅修改 OpenCLI 时，写入后通过现有 `agent_runtime` scope 刷新配置，不调用 `_restart_agent_browser_runtime`；只有浏览器路径或 headless 实际改变才重启浏览器。已有任务保留装配快照，后续任务读取新配置。
- 前端：[definition.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition.ts) 声明开关与依赖的模式选择，`OpenCLIStatusSetting.tsx` 用共享 `SettingRow` 显示状态；`browserSettings.ts` 转换 RPC 的嵌套载荷与前端字段补丁，同步修改 source contract 和中英文案。

**测试**：配置合并、诊断的各个状态、前端 settingsRefactor 测试。

### WP10 Core C2（可选）

- `before_invoke`（runtime.py L2355）不再立即调用 `ensure_runtime_ready`，改到第一次调用浏览器工具时再启动。
- [browser_state_context_processor.py:146](../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py#L146)：第一次调用浏览器工具之前不采集页面，状态消息写"尚未观察页面"。
- 前提：工具 schema 可以离线提供，例如按 Playwright MCP 版本缓存 `tools/list` 的结果。

**测试**：纯 OpenCLI 任务全程不启动 MCP；第一次调用浏览器工具时能正确启动并采集。

### WP11 端到端验证与评估

- `tests/electron/opencli_worker_page.cjs`：用真实 CLI 加 fixture，验证 cookie 共享、两个页面互不导航、取消后页面被重建。
- `tests/electron/opencli_task_cases.md` 列出任务级用例：
  - 命中、未命中、部分覆盖、"前 N 条"列表；
  - 不需要浏览器的命令；
  - 验证码 → 用户点「已完成，继续」→ 新任务接着做；
  - 验证码 → 无人处理时自动重新派发，工作页仍保持保留、不被导航；
  - 写确认、写结果不明、大结果回读。
- 评估：同一批任务分别跑纯 Browser 路径和混合路径，统计成功率、耗时、模型轮次、token 和"被阻塞后重启"的次数，并注明是否启用了 C2。

## 5. 里程碑

| 里程碑 | 包含 | 退出条件 |
| --- | --- | --- |
| M0 | §3 契约冻结；WP0 | 调查文档 §7 与 WP0 的附加检查项都有结论 |
| M1（可用闭环） | WP1–WP7（使用本地 Core）、WP8a；只接单 Agent | 开启后，fixture 和一个真实站点的 describe/run 可用；写命令能在界面上确认；`needs_user` 使任务以 `blocked` 结束，并且只有点击按钮后才解除保留；纯 OpenCLI 的列表任务被判为完成；系统 PATH 中没有 node 时也可用；零暴露测试和 Playwright 回归都通过 |
| M2（本地产品化） | WP8b、WP9；继续使用本地 Core | 设置页可切换开关和工作页模式、显示诊断状态；变更在下一次 Browser Agent 任务生效；hidden 模式、人工处理和关闭时零暴露的回归通过 |
| M3 | Code 与 Swarm 装配；继续使用本地 Core | 满足设计 §10 阶段 D 的条件，包括两个成员并行调用 |
| M4 | WP11（可选 WP10） | 产出评估报告 |

## 6. 风险与应对

| 风险 | 触发时机 | 应对 |
| --- | --- | --- |
| 页面级 CDP 在 Electron 43 上连接失败，或行为与源码推断不同 | WP0 | 改为在自维护发行物中让 CDPBridge 接受 targetId，由它自己连接；不回退到按分数挑选目标 |
| Electron 内置的 Node 版本低于 20.18.1，或在 Node 模式下运行 OpenCLI 出现不兼容 | WP0 | 先确认版本和具体的不兼容点；实在不行就随运行包带一个固定版本的 Node。不依赖系统 PATH |
| ephemeral 模式破坏了依赖 persistent 语义的 adapter | WP0、WP11 | 在自维护发行物中打补丁：CDP 模式下跳过 lease 释放，恢复 persistent |
| 运行包体积过大 | WP1 | 在 WP0 里实测；必要时在构建期裁掉不需要的站点目录（目录与 adapter 保持一致） |
| C1 引入 Playwright 路径的回归 | WP7 | 新逻辑只作用于声明了 properties 的工具；把现有 browser_move 测试全量作为门禁 |
| 用户只用文字说"好了"、没有点按钮，任务反复被阻塞 | M1 | 提示段和处理说明里明确要求点按钮；阶段 E 统计这种情况的频率，必要时再考虑其他解除方式 |
| 上游 adapter 随网站改版失效 | 长期 | 真实站点回归（从 Bilibili 开始）；按设计 §8.2 逐站接管 |

## 7. 待决事项

1. 中性命名（设计 §8.1）：建议在 M1 之前定下来，避免之后迁移配置和提示。
2. 首版写确认、命令超时已按 §8.2 实现，后续依据使用与评估结果调整。
3. 首版待核实记录保留 24 小时（§8.2），后续验证提醒是否过早失效。
4. Bilibili 已用于 M1 的只读联调（§8.7）；真实登录与验证码恢复仍需补验。

## 8. 第一版实现记录（2026-09-29）

### 8.1 已实现

| 工作包 | 状态 | 主要落点 |
| --- | --- | --- |
| WP1 运行包 | 已完成 | `third_party/opencli/`、`scripts/update_opencli_runtime.py`、`jiuwenswarm/resources/runtime/opencli/`（zip 6.5MB；`catalog.json` 1209 条命令、169 个站点）；PyInstaller spec 与 `MANIFEST.in` |
| WP2 目录与来源 | 已完成 | `extensions/opencli/catalog.py`、`sources/opencli.py` |
| WP3 Electron 宿主 | 已完成；2026-09-30 经真实宿主函数与 UI 联调（§8.7） | `browser_panels.cjs`、`main.cjs`、`preload.cjs` |
| WP4 工作页客户端 | 已完成 | `extensions/opencli/worker_page.py` |
| WP5 工具与待核实记录 | 已完成 | `extensions/opencli/tools.py`、`pending.py` |
| WP6 启用判断与装配 | 已完成单 Agent；Code 与 Swarm 未接 | `extensions/opencli/__init__.py`、`gate.py`、`prompt.py`；`interface_deep.py`；`config.yaml` 增加 `browser.opencli`（默认关闭） |
| WP7 Core C1 | 已完成（agent-core 分支 `feat/browser-external-tools`） | `runtime.py`、`tool_result_window_processor.py`、`browser_agent.py`、`playwright_runtime/__init__.py` |
| WP8a 最小界面 | 已完成 | `DesktopBrowserPane/OpenCLIPrompt.tsx`、`DesktopBrowserPane/index.tsx`、`App.tsx`（`jiuwen:send-chat-message` 事件）、`types/electron.ts`、中英文案 |
| WP0 连接验证 | 开发版完成（见 §8.6）；打包版和真实站点项留给 WP11 | `tests/electron/opencli_smoke.cjs`、`opencli_smoke_driver.py`；运行包入口改为 `third_party/opencli/entry.mjs` |
| WP11 | 已开始 M1 所需的 fixture、任务链路和 Bilibili 只读验证；完整评估未完成 | `opencli_worker_page.cjs`、`opencli_worker_page_driver.py`、`opencli_worker_page_fixture.tsx` |
| WP8b hidden 与运行状态 | 已完成 M2 开发联调（§8.8） | `DesktopBrowserPane`、`useDesktopBrowserAttention.ts`、`main.cjs`、`worker_page.py` |
| WP9 设置与诊断 | 已完成 M2 开发联调（§8.8） | `common/browser_config.py`、两条设置 RPC、浏览器设置模块、`inspect_runtime()` |
| WP10，以及 Code 与 Swarm 装配 | 未开始；WP10 可选，Code/Swarm 为下一步 M3 | — |

### 8.2 默认值

| 项目 | 默认值 | 理由 |
| --- | --- | --- |
| 命令超时 | 120 秒，并受剩余时间约束（剩余 − 10 秒，最少 15 秒） | 上游浏览器命令自身超时为 60 秒、连接超时 45 秒；留出余量，让上游的结构化超时错误先出现 |
| 写确认超时 | 90 秒，并受剩余时间约束（剩余 − 30 秒，最少 15 秒） | 简单任务预算只有 240 秒，确认之后还要留时间执行命令 |
| 等待人工的保留时间 | 30 分钟 | 登录或验证码可能需要用户离开一会儿；过期后页面重建 |
| 待核实记录保留期限 | 24 小时 | 与上游网络缓存 TTL 一致；覆盖一个工作日内的重试，避免长期提醒已经无关的操作 |
| 外部操作预算 | 每个任务 16 次，同一命令加同一参数最多 2 次 | 查询命令不计预算；执行类命令单独计数，不占用导航阶段 |
| 单条结果内联上限 | 8000 字符（超过即落盘，用回读工具读取） | 与回读工具单次读取量同一量级 |
| 结果大小上限 | 转义后 7MiB | 保证落盘文件低于回读工具的 8MB 上限 |

### 8.3 与计划的差异

- **保留由宿主在分配时强制执行**，不再单独查询保留状态；attention 随保留一起发出，没有单独的 attention 接口。好处是 AgentServer 重启后保留仍然有效。
- **确认条和人工处理横幅由面板状态驱动**：`pendingConfirm`、`hold` 随 `browser:panels-changed` 下发，渲染进程晚于请求挂载也不会漏掉；`browser:attention` 只负责切换标签。
- **运行包解压**：复用 `playwright_mcp_runtime.materialize_bundled_runtime`，只增加 `runtime_name` 和 `load_manifest` 两个参数（默认值保持原行为），没有另建通用模块。
- **命令目录**：`catalog.json` 作为明文文件与 zip 放在一起，由清单记录哈希，方便评审时查看命令清单。
- **参数校验放在与来源无关的 `CommandSpec.normalize_args`**：执行器只接收校验后的有序参数。
- **测试位置**：swarm 侧测试在 `tests/unit_tests/extensions/opencli/`；Electron 侧测试并入 `tests/electron/browser_panels.test.cjs`；agent-core 侧新增 `test_browser_external_tools.py`，并在 `test_tool_result_window_processor.py` 中补了用例。

### 8.4 验证情况

- swarm：新增 46 个单元测试；装配、Electron 回退、sideview、运行包、打包脚本、桌面契约等相关测试共 153 个通过、1 个跳过；Electron 页面测试 10 个通过。
- agent-core：新增 12 个测试（其中经过真实 AbilityManager 调用链的 1 个）；浏览器相关测试 557 个全部通过。
- **真实运行包冒烟**：用固定版本运行包执行 `hackernews top`、`npm package` 以及一个不存在的包，解压、目录、参数拼装、JSON 解析、错误信封（66 `EMPTY_RESULT`）都正常。
- 前端：改动文件的类型检查与 eslint 均通过。

- **WP0 冒烟**（§8.6）：44 项全部通过，覆盖 Electron 工作页上的整条链路和 Electron Node 模式。

**尚未验证**：
- 截至 2026-09-29，`main.cjs` 中真实的工作页创建、确认条与横幅在真实界面中的交互、「已完成，继续」尚未验证；2026-09-30 已补充 §8.7 的联调。完整 App 启动与真实模型决策的评估仍属于后续验证；
- 打包版：运行包加载，以及打包后的 exe 在 Node 模式下运行 OpenCLI；
- 真实站点（persistent 语义、未自行导航的命令、验证状态保留），留给 WP11。

### 8.5 发现的既有环境问题（与本次改动无关）

- swarm 的 `.venv` 中安装的 openjiuwen 版本过旧，导入 `openjiuwen.agent_teams.external.external_cli_agent_spec_from_template` 会失败。2026-09-30 已将依赖配置和 lockfile 固定为本地 Core 可编辑安装；开发启动方式见 §8.7。
- swarm 的 `.venv` 在目录调整后，入口脚本路径失效（`uv run pytest` 报 trampoline 错误）；2026-09-30 已把 Electron 启动前的契约检查改为 `python -m pytest`。
- agent-core 的 `probes.py` 第 870 行存在非法转义 `\s`，在 swarm 的 pytest 配置（warning 视为错误）下会变成 SyntaxError。
- agent-core 中 `test_compression_recall.py` 等 24 个上下文压缩测试在本机 Windows 上失败（文件名非法字符、创建符号链接的权限），恢复原始代码后依然失败。
- 前端 `node_modules` 缺少 `fflate`，`trajectoryArchive.ts` 报 4 个类型错误；2026-09-30 已按现有 lockfile 重新安装，构建通过。
- `tests/unit_tests/test_build_config.py::test_cli_sync_status_uses_stderr_without_log_prefix` 在 Windows 上失败：输出里的路径分隔符是 `\`，而测试断言写死了 `/`。
- 从 VS Code 集成终端启动的进程会继承 `ELECTRON_RUN_AS_NODE=1`，直接运行 `electron.exe <main>` 时 Electron 会以 Node 模式启动。冒烟脚本已自动去掉该变量后重新启动。

### 8.6 WP0 连接验证

**验证工具**：`npm run test:opencli:smoke`（在 Electron 包目录执行）。

- 脚本启动一个最小的 Electron 主进程：隐藏窗口，同一 partition 下建两个页面（Browser Agent 页、OpenCLI 工作页），另起本地 fixture 网站和 19825 端口探针，并在私有 HOME 中放置 fixture adapter。
- A 部分直接以 Electron Node 模式运行打包好的 OpenCLI，检查上游行为。
- B 部分运行 `opencli_smoke_driver.py`，经真实的 `prepare_runtime`、`OpenCLISource`、`OpenCLIRunTool`、`PageSlot` 以及真实的 `createTargetHandler` 路由执行。

**结果（2026-09-29，Electron 43.5.1 / Chromium 150 / 内置 Node 24.19.0）**：A 部分 29 项、B 部分 15 项全部通过，连续多次运行结果稳定。

| 调查文档 §7 的项目 | 结论 |
| --- | --- |
| Electron Node 模式 | 内置 Node 24.19.0，满足 ≥ 20.18.1。PATH 中没有 node 时同样可用。`--version` 约 0.1 秒，不需要浏览器的命令约 0.25 秒。**必须经 `entry.mjs` 启动**（见下文发现 1） |
| 精确绑定 | 页面级 ws 地址格式为 `ws://127.0.0.1:<port>/devtools/page/<targetId>`，只有工作页被导航，Browser Agent 页的 URL 不变。目标已不存在时约 0.2 秒失败，退出码 1（`UNKNOWN`，`connect ECONNREFUSED`） |
| 连接时的动作 | 页内带凭据的 fetch、`Network.getCookies`（能读到 HttpOnly cookie）、预导航都正常 |
| 共享登录态 | Browser Agent 页登录后写入的 HttpOnly cookie，工作页上的命令能用；工作页重建后登录态仍在 |
| 不连接 daemon | 带 `--site-session ephemeral` 的读、写命令，CLI 对 19825 的请求数为 0。反例成立：`--site-session persistent` 的写命令会发出 `POST /command`。另外，**没有 `OPENCLI_CDP_ENDPOINT` 时，需要浏览器的命令会改走 daemon 和扩展**（约 210 次请求后以 69 退出），见下文发现 3 |
| 释放与取消 | 结束 CLI 进程树后，工作页和宿主都存活，同一页面还能继续执行命令 |
| 页内活动的停止 | 结束进程后，adapter 在页面里启动的定时请求仍在继续（1.5 秒内 15 次）；重建 WebContents 后停止。"被结束过的页面必须重置"这条设计成立 |
| 不需要浏览器的命令 | 不带 `--site-session` 正常；带上时报 `unknown option '--site-session'`，退出码 1 |
| 错误映射 | `AUTH_REQUIRED` 77，stderr 为 YAML 信封；`EMPTY_RESULT` 66；参数错误 2；adapter 返回空数组时退出码 0，输出 `[]`，工具归为 `empty`；未知命令或选项（commander 报错）退出码 1，归为 `error` |
| 目录隔离 | fixture adapter 从私有 HOME 加载，说明 `os.homedir()` 已被重定向，用户全局 `~/.opencli` 不参与 |
| 工具层流程（B 部分） | 读、不需要浏览器、写确认通过/拒绝/超时、结果不明的写入被记录并在下次确认时提醒、验证码 → 保留 → 下一次调用收到 409 → 用户"已完成"后页面不变 /"放弃"后页面重建、超时后结束进程并重建页面，全部符合 §3 的契约 |
| 隐藏页面 | 工作页 `setVisible(false)` 并放在隐藏窗口中，fetch、导航、定时器都正常。`ui` 策略的真实点击留给 WP11 |
| persistent 语义、未自行导航的命令、验证状态保留 | 需要真实站点，留给 WP11 |

**发现 1：Electron Node 模式下 OpenCLI 的 argv 解析错误（已修复）**。直接启动 `dist/src/main.js` 时，除 `--version` 外所有命令都报 `unknown command '<main.js 路径>'`。
- 原因：OpenCLI 调用 `program.parse()` 时不传 argv，commander 检测到 `process.versions.electron`；只要 `process.defaultApp` 未设置，它就按"打包的 Electron 应用"处理，认为 argv 中没有脚本路径，于是把脚本路径当成了命令名。上游 bundle 中只有 commander 依赖这个判断。
- 修复：运行包新增入口 `third_party/opencli/entry.mjs`。它在 Electron 下设置 `process.defaultApp = true`，然后导入 `dist/src/main.js`；在普通 Node 下什么也不做。`update_opencli_runtime.py` 把它打进 zip 根目录，清单的 `cli_relative_path` 改为 `entry.mjs`；运行包已重新生成，目录没有变化。

**发现 2：以 `-` 开头的参数值（已修复）**。上游把可选具名参数注册为 `--name [value]`：以 `-` 开头的位置参数会报"未知选项"，可选值也不会吃掉以 `-` 开头的下一个参数。`build_argv` 改为 `--name=value` 加 `-- <位置参数>`。实测以 `-` 开头的值，以及含空格、含 `=` 的值、布尔 `true`/`false`，都能原样到达 adapter；B 部分经真实工具再验证了一遍。同时，`normalize_args` 拒绝只给后面的可选位置参数（否则值会错位）。

**发现 3：没有工作页地址时会用到用户自己的浏览器（已加防护）**。本机 Chrome 装有 OpenCLI 扩展 1.0.24，并在轮询 `localhost:19825/ping`。如果需要浏览器的命令在没有 `OPENCLI_CDP_ENDPOINT` 的情况下启动，上游会通过 daemon 和这个扩展操作用户的 Chrome。工具层本来就不会这样调用；现在 `OpenCLISource.run` 也拒绝启动这种进程，作为最后一道防线。

**测试注意**：探针会收到扩展的 `/ping`（带 Chrome 的 User-Agent，没有 Origin）。CLI 自身不请求 `/ping`，冒烟脚本按这一点区分两者，只统计 CLI 发出的请求。

### 8.7 M1 开发联调（2026-09-30）

**当前结论**：M1 的开发联调退出项已验证。用本地 Core 跑通真实 Electron 工作页、真实 OpenCLI 命令、写确认 UI、保留与取消，以及单 Agent 的权威结束结果。单 Agent 用固定模型响应验证执行链路，不代表真实模型的路由准确率已评估。默认仍关闭，未提交或发版。

**本次修复**：

- 来源取消时携带启动事实；已经启动的写操作保存为待核实。工作页租约释放、页面重建和进程清理不受第二次取消打断。取消发生在页面分配或子进程创建期间时，也会取得资源的结果后完成回收。
- 写确认结束、页面排队结束后重新计算剩余预算，预算不足时不启动命令。
- Core 外部操作的重复签名改为「工具名 + 完整参数」的规范 JSON 哈希。原先复用了 Playwright 的语义字段筛选，丢掉 site/command/嵌套 args，使不同命令在第三次调用时被误判为重复；新增用例验证不同命令、长参数、键顺序、相同调用两次限制与总量 16 次限制。
- attention 由常驻 App 层订阅；能重新打开显式关闭的浏览器页签，并展开原本卸载浏览器面板的侧栏。人工处理说明只指向同 profile 的内置工作页。
- 重建工作页时，宿主恢复仍被选中面板的可见性；如果用户已切走，则保留后台隐藏。回归先复现了「放弃后新 target 存在但页面隐藏」，修复后也验证了取消重建和再次验证码的原生页面显示。
- 所有宿主请求统一携带工作页标签和 visibility，避免 reset/首次 confirm 把 OpenCLI 页签变成「主浏览器」或把 hidden 覆盖为 sidebar；sidebar/hidden 两种配置的重建参数均有回归。
- WP0 无法独占 19825 探针端口时立即中止，不能跳过隔离验证后继续执行反例命令。新增端口占用回归测试；原先仅记录的参数和空数组项改为明确断言。
- Swarm 的 `pyproject.toml` 与 `uv.lock` 已将 `openjiuwen` 固定为 `../agent-core` 的可编辑安装，基础依赖及 harmony、claude、codex、distribute 等 extras 共用这个来源。前端按现有 lockfile 执行 `npm ci`，解决缺失的 fflate 与依赖重复，构建通过。Electron 的 `check:contract` 使用 `python -m pytest`，避免搬迁目录后旧入口脚本的绝对路径失效。

**验证工具与范围**：

`opencli_worker_page.cjs` 复用 `browser_fixture.cjs`：编译并运行真实 `main.cjs` 中的浏览器管理函数、宿主路由和 IPC，使用真实 preload、DesktopBrowserPane、OpenCLIPrompt，以及常驻 attention hook；不启动完整 AgentServer/Gateway/App。profile、工作区、HOME、fixture adapter 都在独立临时目录，默认屏蔽外网。传入 `--real-site` 后只放行 Bilibili 相关域名，驱动器也只接受目录中声明为 read 的 Bilibili 命令。

| M1 退出项 | 实测 |
| --- | --- |
| fixture describe/run | describe 不创建工作页；read 返回 2 条数据；工作页使用 Browser Agent 页写入的 HttpOnly cookie，Agent 页 URL 不变 |
| 写确认 | 浏览器面板未挂载、页签显式关闭时能打开确认条；同一次批准执行一次，拒绝与超时不启动命令；未知写入在后续确认上显示提醒 |
| needs_user → blocked | 真实 Browser Agent 经 describe/run 两次模型调用后强制以 blocked 结束、retryable=false，不再调用模型；宿主保留不随任务结束解除，自动调用不能导航保留页 |
| 按钮恢复 | 「已完成，继续」保留原 target 和 fixture 验证 cookie，并发出固定的普通聊天消息事件；「放弃」后下次使用重建 target，选中页仍显示 |
| 纯 adapter 列表任务 | 真实 Swarm contribution + Core factory/AbilityManager/rails + MCP；固定模型依次 describe、run、自然语言回答，最终权威结果 completed，不需要模型调用页面工具 |
| 混合路径 | 同一个 Browser Agent 在一次任务中 describe → adapter read → 真实 Playwright navigate → adapter read → 回答，5 次模型调用后 completed；两个页面导航独立，已切走的工作页在重建后仍隐藏 |
| 外部操作预算 | 同一 Agent 连续执行 3 次 read（page=1/2/3），本地网站收到三个参数，权威结果 completed，账本记录 3 次操作与 3 个签名；不会把第三次不同参数调用误当作重试 |
| 取消 | 真实写命令提交后取消：进程停止、待核实落盘、租约释放、target 重建、页内定时请求停止；下一条读命令仍使用共享登录态 |
| 真实站点 | Bilibili hot、ranking、search 的 describe 均返回只读命令合同；第一轮和最终轮各返回 3 条数据，中间一轮 hot/search 各 3 条、ranking 为 empty；各轮 Agent 页都未导航 |
| 系统无 node | WP0 用 Electron Node 24.19.0，在 PATH 无 node 时启动并执行，仍通过 |
| 关闭时零暴露 | 禁止运行包探测的单测中，关闭或外置浏览器时，prompt/tools 不变 |
| Playwright 回归 | 原有真实 Electron + MCP/SDK 集成通过；Core 浏览器测试 544 项与结果窗口测试 15 项通过 |

**最新检查结果**：

- Swarm：OpenCLI 单测 54 项；连同运行包、装配、安全约束、桌面契约等选定回归，共 123 项通过。
- Core：544 + 15 = 559 项通过。
- Electron：WP0 44 项通过；真实宿主/UI/任务链路 15 项通过，加上真实站点验证共 16 项；探针端口占用回归 1 项通过；面板单测 10 项通过；语法检查及既有 Electron/Playwright 集成通过。
- 前端：`npm run build` 通过；改动文件没有新增 eslint 问题，App 的 4 条 warnings 与 HEAD 相同；常规宽度与 540px 窄窗口的确认、提醒和保留横幅截图已检查。原生 WebContentsView 不在 renderer 截图内，另存页面截图并核对工作页已显示。

**重跑**（在 `jiuwenswarm/channels/desktop/electron/`）：

```text
npm run test:opencli:worker                   # 本地 fixture + 单 Agent，15 项
npm run test:opencli:worker -- --real-site    # 再做 Bilibili 只读验证，16 项
npm run test:opencli:smoke                    # WP0，44 项
npm run test:opencli:probe                    # 单独验证探针端口占用；不要与 smoke 并行
```

脚本需要已经解压的固定版本 Playwright MCP runtime，默认从用户 runtime 缓存定位，也可用 `SWARM_TEST_MODULES` 指向其 node_modules。运行结束输出独立临时目录，保留 `results.json`、任务权威结果、Bilibili 原始返回和截图供复查。

**截图夹具修正**：测试中 `page.screenshot` 在原生视图切换后两次超时，交互与宿主断言仍可执行。截图现统一通过 Electron 的 `webContents.capturePage` 保存，分别捕获 renderer 与原生工作页，并继续断言工作页可见；没有跳过页面验证或修改产品运行行为。

**本地 Core 开发启动**：三个仓保持同级独立，Swarm 从 `../agent-core` 读取 Core 源码。依赖配置已写入 `pyproject.toml` 与 `uv.lock`，无需临时手动安装或设置 `UV_NO_SYNC`。已实测正常 `uv run --locked` 在同步依赖后仍从本地 Core 导入；锁文件中的其他包版本没有变化。Core 源码修改在新启动的 Python 进程中生效，已运行的后端需要重启。PowerShell：

```powershell
# 在 Swarm 仓根目录
Remove-Item Env:UV_NO_SYNC -ErrorAction SilentlyContinue  # 清除之前联调的临时设置
uv sync --locked
uv run --locked python -c "import openjiuwen; print(openjiuwen.__file__)"
npm --prefix jiuwenswarm/channels/desktop/electron run dev
```

**仍待验证**：完整应用启动后的主 Agent 重新派发和真实模型路由；打包版 exe/资源加载；真实站点的登录/验证码恢复、persistent 对话语义、hidden 下 ui 策略及下载；Code/Swarm 多成员装配；同批任务的成功率、时间、轮次和 token 评估。Bilibili ranking 两轮不一致的原因尚未定位，不能把本次链路通过当作所有 adapter 已稳定适配。

**按计划的后续里程碑**：M2 的完成记录见 §8.8；下一步进入 M3 的 Code/Swarm 装配，再完成 M4 评估。整个过程使用本地 Core，不以 SDK 发布或切换远端版本为前提。

### 8.8 M2 设置、诊断与后台工作页（2026-09-30）

WP8b、WP9 已完成本地实现与开发联调。本次只改 Swarm，继续使用 `../agent-core` 可编辑依赖，没有发布 SDK 或提交代码。

**产品行为**：

- 浏览器设置增加 OpenCLI 网站 adapters 开关、工作页显示模式和诊断。默认关闭，关闭时折叠模式选择，后续 Browser Agent 不增加 OpenCLI 工具或提示。
- `path.set` 只提交实际编辑的字段，嵌套合并 `opencli`，保留 `enabled_sites` 等未提交的配置。只改 OpenCLI 时不重启浏览器、不重建工作页，通过既有 `agent_runtime` reload scope 刷新后续任务的配置。
- 诊断区分关闭、可用、运行包缺失、Electron Node 不可用、外部浏览器不支持、站点限制后无命令。诊断检查文件和哈希，读取宿主的 Node 版本，不启动 Node、解压运行包或修改环境。
- 运行状态同时使用页面 loading 和执行租约 busy，覆盖不导航的 adapter。
- 后台工作页平时不显示；写确认或验证码时临时显示。确认、拒绝、超时、已完成或放弃后由宿主隐藏，前端恢复之前选中的成员页面。用户自己切换页面时保留其选择。
- 工作页的锁与重建标记共享，客户端配置按任务保存。修正了缓存第一份客户端后，后续任务一直沿用旧工作页模式的问题；旧任务继续保留自己的快照。

**新增或修改的主要文件**：

| 文件 | 说明 |
| --- | --- |
| `common/browser_config.py`（新增） | 两条设置 RPC 的共用校验、字段合并、重启判断和诊断载荷；只读访问 Electron 启动/发现信息 |
| `common/config.py`、`gateway/channel_manager/web/app_web_handlers.py`、`server/runtime/gateway_adapter/config_adapter.py` | 配置落盘与部分更新；区分 OpenCLI 配置刷新和浏览器重启 |
| `extensions/opencli/__init__.py`、`sources/opencli.py` | `inspect_runtime()` 与实际准备分开；校验目录哈希、站点限制后的可用性 |
| `extensions/opencli/worker_page.py` | 共享页面状态与任务客户端分开，避免模式配置被首次调用固定 |
| `channels/desktop/electron/main.cjs` | 传递 Node 版本；结束人工处理后隐藏后台工作页，并拒绝过期的显示回调 |
| `features/settings/services/browserSettings.ts`、`modules/browser/OpenCLIStatusSetting.tsx`（新增） | 前端载荷转换、字段补丁、共享 SettingRow 诊断行 |
| `modules/browser/definition.ts`、`SettingsSourceProvider.tsx`、两个 settings contract、中英文案 | 声明开关与依赖选择；保存与回滚字段；状态显示 |
| `DesktopBrowserPane/index.tsx`、`useDesktopBrowserAttention.ts`、相关 CSS/类型 | 后台页临时显示、恢复原页面、清理已结束的 attention、运行状态 |
| `tests/unit_tests/extensions/opencli/test_opencli_settings.py`（新增）及 Gateway/ConfigAdapter 单测 | 嵌套合并、诊断无副作用、旧配置兼容、配置快照和无需重启 |
| `tests/electron/opencli_worker_page.*`、Electron `package.json` | 生产设置组件通过真实 ConfigAdapter 保存；真实宿主后台页交互；新增 `test:opencli:settings` |

前端路径相对 `jiuwenswarm/channels/web/frontend/src/`，其他产品路径相对 `jiuwenswarm/`；测试路径相对 Swarm 仓根目录。

**验证**：

- Python：OpenCLI、ConfigAdapter、浏览器设置 Gateway、桌面契约和配置更新相关选择项共 **112 项通过**。包含关闭时不读取发现信息/运行包、外部浏览器不探测 Node、诊断无进程/解压/环境副作用、目录篡改拒绝，以及模式快照共享页面锁。
- Electron：`npm run test:opencli:settings` **24 项通过并重跑通过**，包括原有 15 项宿主/UI/Agent 链路与 9 项 M2 检查。开关和模式经过生产设置组件、真实 ConfigAdapter 和临时 YAML；写确认、验证码、超时和放弃经过真实宿主及 CLI。
- 前端：`npm run build` 通过；本次修改的 9 个 TS/TSX 文件 eslint 为 **0 errors、0 warnings**；`git diff --check` 通过。
- `npm run test:settings-panel` 为 **55 项通过、8 项失败**。用 HEAD `52abe68d` 的前端源码和测试在独立临时目录重跑，为 **52 项通过、9 项失败**；当前 8 项失败全部属于原有失败，没有新增失败。新增的两个浏览器载荷/补丁测试通过，OpenCLI 文案相关旧断言已同步。
- 已与 General 模块比较共享布局，检查宽屏、540px 窄屏、模式展开/收起和后台页的确认/人工处理。夹具的控制按钮在设置页改为顶部布局，避免夹具侧栏挤占验证区域；截图等待 React 布局与滚动完成。renderer 与原生工作页分别捕获。

原有前端失败涉及模块顺序、旧字段列表、免费模型目录刷新、连接状态、媒体字段、Tag 的旧正则和模型行顺序，本次没有改动这些产品功能。可复查的报告为 `C:\Users\soong\AppData\Local\Temp\swarm-settings-baseline-7ReliL\baseline.xml`；最新 UI/宿主记录与截图为 `C:\Users\soong\AppData\Local\Temp\swarm-opencli-worker-xMem1C\`。

**重跑**：在 Electron 包目录执行 `npm run test:opencli:settings`，在前端目录执行 `npm run build` 与 `npm run test:settings-panel`。Python 选择项使用正常 `uv run --locked`，未跳过本地 Core 的依赖同步。

**验证边界与下一步**：M2 验证了设置保存后重新装配的贡献变化，Gateway 的 scoped reload 与不重启行为有单测；完整 App/Gateway 启动后的任务缓存刷新、真实模型和打包版尚未验证。真实网站的验证码恢复及特殊 adapter 行为仍在 M4。下一步 M3 接入 `interface_code.py` 和 `code_subagents.py`，验证成员身份绑定后装配、关闭时零暴露、同一成员串行与不同成员并发。Core C2 仍为可选项。

### 8.9 迁移后的开发环境恢复（2026-10-02）

**结论**：代码与开发环境迁移已完成恢复验收。M1、M2 的选定回归在新机器上通过，Swarm 继续依赖同级本地 Core；M3 尚未开始。本次没有修改产品代码、依赖配置或锁文件，没有提交代码或发布 SDK。用户数据和浏览器登录态按本次迁移范围可重新建立。

**目录与保留项**：

- 当前仓库父目录为 `C:\Users\wangy\Documents\openJiuwen_OpenCLI\openJiuwen_OpenCLI\`，`jiuwenswarm`、`agent-core`、`opencli` 各自独立；父目录本身不是 Git 仓。旧实验仓保持为独立参考目录。
- Swarm 分支 `feat/openJiuwen_opencli`、HEAD `52abe68d`；Core 分支 `feat/browser-external-tools`、HEAD `6786cbe9`。迁移前的未提交修改保留，三个仓的 Git 连通性检查通过。
- 原 `.venv` 引用了不存在的 `C:\Users\soong\anaconda3`，本地 Core 的可编辑安装也指向旧用户路径。原环境已移到 `C:\Users\wangy\Documents\openJiuwen_OpenCLI\.migration-backups\20261002\jiuwenswarm.venv\`，没有删除。
- 新 `.venv` 使用 Python 3.13.9，通过 `uv sync --locked --python 3.13.9` 从原锁文件重建。`pyproject.toml` 和 `uv.lock` 的 SHA-256 与恢复前一致；264 个已安装包的 `uv pip check` 通过。
- 正常 `uv run --locked` 已验证导入当前 Swarm 及 `../agent-core`；Core 的 `direct_url.json` 指向新用户的同级仓，并且保持 `editable=true`。

**工具与运行缓存**：

| 工具 | 当前版本 | 恢复方式 |
| --- | --- | --- |
| Python | 3.13.9 | uv 管理的用户目录安装；用户 PATH 指向可运行的实际安装目录 |
| uv | 0.10.6 | 用户级命令；项目环境中的 uv 依赖仍按原锁文件为 0.12.5 |
| Node / npm | 24.19.0 / 11.17.0 | 用户目录安装，Node 归档与官方校验和一致 |
| Git | 2.53.0.windows.3 | 从本机已验证的完整 Git 运行包复制到用户工具目录，已验证仓库操作和独立 exec-path |
| Electron / 内置 Node | 43.5.1 / 24.19.0 | 保留仓内安装，实测可启动 Electron 和 Node 模式 |

uv 生成的全局 Python 代理在本机报 `entity not found`，而实际 Python 可运行。失效代理已备份到 `.migration-backups\20261002\python-proxies\`，通过用户 PATH 使用实际解释器；新项目虚拟环境的解释器也已验证可运行。原用户 PATH 的已有条目保留。现有终端和应用需要重启以读取更新后的 PATH。

通过生产函数 `materialize_bundled_runtime()` 和 `prepare_runtime()` 重建新用户缓存，校验并实际准备 Playwright MCP 0.0.78 和 OpenCLI 1.8.8。缓存位于 `C:\Users\wangy\.jiuwenswarm\runtime\`，OpenCLI 入口仍为 `entry.mjs`，使用 Electron 内置 Node。没有更换运行包或命令目录。

**本机复验**：

| 检查 | 结果 |
| --- | --- |
| Swarm：OpenCLI、ConfigAdapter、Gateway、桌面契约、配置更新的 M2 选择项 | 112 项通过，391 项未选中 |
| Core：浏览器工具及结果窗口 | 559 项通过 |
| Electron 启动前 `check:contract` | 30 项通过，与 Swarm 选择项部分重叠，不累加计数 |
| WP0 `test:opencli:smoke` | 44 项通过（上游行为 29 项、真实 Python 工具链 15 项） |
| M1/M2 `test:opencli:settings` | 24 项真实宿主/UI/Agent 检查通过 |
| 浏览器面板 / 探针端口占用 | 10 项 / 1 项通过 |
| 原有 `test:browser:integration` | 通过：真实 Electron + MCP、本地 SDK、会话及成员并发、共享登录态、面板切换、淘汰和 profile 内登录态持久化 |
| Electron 语法检查 / 前端 TypeScript / 前端构建 | 通过 |
| 前端 `test:settings-panel` | 55 项通过、8 项失败；失败名称与 §8.8 已记录的原有失败一致 |
| 两仓 `git diff --check` | 通过 |

Python 选择项沿用开发回归的 asyncio 配置，并忽略 Core 现有无效转义触发的 `SyntaxWarning`；没有改动相关源码。原有浏览器集成脚本需要显式传入 `SWARM_TEST_MODULES`，首次因未设置该参数中止，指向已重建的固定 MCP 缓存后通过；这项测试参数没有写入产品配置或全局环境。

**证据与重跑**：报告保存在三个仓之外的 `C:\Users\wangy\Documents\openJiuwen_OpenCLI\.migration-backups\20261002\verification\`，包括 `toolchain.json`、`runtime-restored.json`、两组 pytest XML/日志、Electron 和前端测试日志。真实工作页的 `results.json`、任务结果及截图已复制到其中的 `electron-worker\`。已检查窄窗口设置、写确认的 renderer 截图及对应原生工作页截图。§8.7、§8.8 的旧机器临时目录仍作为历史记录，本次记录替代其当前可复查位置。

新开 PowerShell 后，在 Swarm 仓根目录可按本地 Core 配置启动开发环境：

```powershell
uv sync --locked
uv run --locked python -c "import openjiuwen; print(openjiuwen.__file__)"
npm.cmd --prefix jiuwenswarm/channels/desktop/electron run dev
```

原有浏览器集成测试的重跑命令（在 Electron 包目录）：

```powershell
$env:SWARM_TEST_MODULES = 'C:\Users\wangy\.jiuwenswarm\runtime\playwright-mcp\0.0.78\f0cffc29bd13\node_modules'
npm.cmd run test:browser:integration
```

**验证边界**：本次使用隔离的本地 fixture、临时 profile 和固定模型响应；没有迁移旧账号登录态，也没有重跑真实站点或真实模型评估。完整应用、Code/Swarm 的 OpenCLI 成员装配和打包版仍按 M3、M4 推进；原有 Playwright 成员并发回归通过不代表 OpenCLI 的 M3 并发验收已经完成。

### 8.10 完整桌面应用与真实模型只读验收（2026-10-02）

**结论**：开发版 Single Agent 的基础链路可用。真实主 Agent 能委派 Browser Agent，Browser Agent 能在内置浏览器的独立工作页调用 Bilibili adapter，并在同一个子任务中执行 adapter → Playwright → adapter。设置的关闭 → 开启 → 关闭经过生产界面和 Gateway，已有父会话的后续 Browser Agent 能刷新工具装配。完整应用验收仍为**部分通过**：本轮发现一次主 Agent 错误判断子 Agent 能力，以及最终列表与结构化证据不一致；没有修改产品代码来掩盖这些问题，也不据此将 M3 或 M4 标为完成。

**环境与范围**：

- 使用生产 `main.cjs` 启动的开发桌面应用，经过真实 Web、Gateway、AgentServer 和设置/聊天界面；不是最小 Electron smoke 进程。
- 用户在应用内配置的 `OpenAIAccount / gpt-6-luna` 实际参与主 Agent 与 Browser Agent 调用。Swarm 继续使用同级 `../agent-core` 的可编辑依赖。
- Electron 43.5.1、内置 Node 24.19.0、OpenCLI 1.8.8。设置界面和 `path.get` 均确认运行包可用，目录包含 169 个网站。
- 本轮只执行公开网页的只读任务；没有登录、解决验证码、点赞、收藏、评论或其他网站写操作。

**实际结果**：

| 检查 | 结果与证据 |
| --- | --- |
| 真实模型连接 | 主 Agent 在实际聊天界面返回指定的“验收连接正常。” |
| OpenCLI 关闭时的浏览器基线 | Browser Agent 通过 Playwright 导航 `https://example.com` 并读取标题和首段；模型调用携带 17 个工具 |
| 在设置界面开启 OpenCLI | 开关保存成功，`path.get` 为 `enabled=true`，诊断为 `available`；Electron PID 和 CDP/宿主路由端口不变 |
| 自然语言 Bilibili 热门查询 | 未指定工具的任务实际先调用两次 `opencli_describe`、再调用 `opencli_run(bilibili/hot, limit=3)`，随后导航热门页并调用 `browser_probe_cards`；执行链路通过，内容与证据一致性未通过，见问题 B |
| 已有会话的关闭 → 开启刷新 | 在关闭时创建的父会话继续派发，新 Browser Agent 携带 19 个工具并成功调用 adapter；无需新建父会话或重启桌面应用 |
| 同一 Browser Agent 内的三步协作 | 子会话尾号 `dc3886bd` 实际按顺序调用 `opencli_run(hot, limit=1)` → `mcp_playwright-official_browser_navigate(热门页)` → `opencli_run(hot, limit=2)`；均成功，返回页面标题“哔哩哔哩热门”及两次 adapter 结果 |
| 已有会话的开启 → 关闭刷新 | 恢复关闭后，原父会话派发的新 Browser Agent 仅携带 17 个工具，通过 Playwright 导航 `https://example.org` 并返回“Example Domain”；本次没有 OpenCLI 工具调用 |

三步协作中两次 CLI 调用分别约 3.83s、3.97s，中间实际 Playwright 导航约 0.75s；Browser Agent 总耗时 32.87s，界面显示包含主 Agent 分派/汇总的总耗时 51.49s。这些是单次运行记录，不是加速率或稳定性评估。

第一次三步尝试的中间目标为 `example.com`，页面已在前面的基线任务中打开，后续 Browser Agent 复用了页面状态，日志只有两次 describe 和两次 run。该次结果不作为“实际发生 adapter → Playwright → adapter”的证据；因此重新使用 Bilibili 热门页，明确要求实际导航，并核对了上述调用顺序。

关闭后的 17 个工具证明后续 Browser Agent 不再装配两个 OpenCLI 工具；已有对话历史和已创建工作页仍可保留。本轮没有重新验证“未安装包”与“已安装但关闭”的上下文逐字节比较，也不声称关闭能删除历史里已经出现的信息。

**验收发现，尚未修复**：

| 编号 | 现象 | 判断与建议 |
| --- | --- | --- |
| A：主 Agent 分派 | 明确要求“把三步交给同一个 Browser Agent，使用 Bilibili adapter”时，主 Agent 在自己的工具中调用 `tool_search`，随后回答“目前可用工具中没有 Bilibili adapter”，没有派发 Browser Agent。说明 adapter 属于子 Agent 局部能力并明确要求 `task_tool` 后，原会话的新子任务即可执行 | 这是一次真实模型分派失败，不是运行包不可用，也不是已证明的配置缓存问题。建议补充通用的子 Agent 分派规则：父 Agent 的工具搜索不能证明子 Agent 没有相应能力，网页任务应让 Browser Agent 自己发现能力。保持 D1，不能用给主 Agent 增加 OpenCLI 专属提示的方式解决；修复后需重测不含人工纠正的原始请求 |
| B：列表与证据不一致 | 自然查询要求热门前 3 条的标题、UP 主和链接。`browser_result` 判为 `completed`，结构化 evidence 却仍只包含 adapter 第一条 `BV1PHay6UEaS` 的 title/url；summary 和最终答复采用了后续页面探针观察到的另一组链接 `BV1vRYP6oE14`、`BV11kao6XEvN`、`BV1VRaz6DEiW`。结构化请求槽位只有 title/url，未覆盖 UP 主；最终 observed count 为 5 | 现有 WP5 明确只将第一行映射到 `extracted`，实现符合这条约定，但第一行字段与总条数不足以证明最终三个列表项及其 UP 主。后续页面观察改变了答复采用的列表，结构化证据没有同步。建议先明确列表逐项身份、所需字段及跨来源证据的对齐规则；不能把 `completed` 当作最终列表全部已核实。现有日志不足以认定是 adapter 返回错误或模型凭空编造 |
| C：本地 Core API 兼容警告 | Swarm 的 `interface_deep.py` 在调用 `rebind_context_model` 时传入 `model`、`model_config`、`model_client_config`，当前本地 Core 的方法只接受 config、session_id、context_id，因此日志出现 `unexpected keyword argument 'model'` | 异常被捕获，provider 模型切换和本轮文本/浏览器任务继续工作，没有阻断 OpenCLI。它仍是待处理的本地 Core 兼容问题；不能将本轮成功等同于上下文模型重绑定也已通过 |

建议先处理 A 的通用分派规则和 B 的结果证据语义，再将相同装配方式推广到 M3 的 Code/Swarm 成员，并同时处理 C。B 涉及契约语义，具体修改应在 Core 与 Swarm 的职责边界确认后实施；本记录不改变已接受的 D1 或 C1 契约。

**保留的验证边界**：真实账号登录态在两个页面之间共享、真实验证码处理后的恢复、完整应用的写确认/待核实记录、真实网站的 hidden/attention 行为、persistent 站点语义、下载、打包版、Code/Swarm 多成员及并发、任务成功率/时间/轮次/token 对比仍未在本轮覆盖。先前 fixture 回归提供对应机制的证据，不能替代这些真实场景。本次匿名 Bilibili hot 命令成功也不代表其他 adapter 已稳定适配。

**证据与现场状态**：

- 证据位于三个仓之外的 `C:\Users\wangy\Documents\openJiuwen_OpenCLI\.migration-backups\20261002\full-app-acceptance\`。`acceptance-summary.json` 保存验收状态、工具序列、工具数、耗时、结构化结果及发现；`acceptance-results.json` 保存两个验收会话的摘要和脱敏 Browser Agent 日志事件；`browser-before.json`、`browser-enabled.json`、`browser-after.json` 保存真实 Gateway 的设置响应。
- 对话 `web_1a0fb8746ea_101116584d75` 覆盖连接、关闭基线、分派失败、三步协作和恢复关闭；`web_1a0fb8a0afc_7a03c68232eb` 为自然 Bilibili 热门查询。共完成 5 个 Browser Agent 子任务；主 Agent 分派失败未启动子任务，因此不计入该数字。
- 实际应用保持运行；OpenCLI 已恢复为验收前的关闭状态，用户的模型配置保留。Electron PID 34884、CDP 端口 58716、宿主路由端口 58720 在本轮未变化，`resources/config.yaml` 与启动前备份逐字节一致。
- 本轮未修改产品源码、依赖或锁文件，未提交代码、未发布 SDK。新增的证据收集脚本存放在上述仓外目录；Playwright MCP 自动生成的 13 个本轮 console/page 文件已移到其中的 `playwright-artifacts\`，保留内容，没有留在仓根目录。

### 8.11 当前进度的提交前复验（2026-10-13）

用户要求将当前本地进度保存到 Git，目的仓限定为 LasVie 名下的对应仓库。保存范围包含现有 Core C1 实现及测试、Swarm M1/M2 实现及测试、OpenCLI 1.8.8 运行包与命令目录、架构/调查/执行计划和历史设计归档。Swarm 的本地 Core 可编辑依赖保持不变。

| 仓库 | 目的仓 | 当前分支 |
| --- | --- | --- |
| Swarm | `LasVie/jiuwenswarm` | `feat/openJiuwen_opencli` |
| Core | `LasVie/agent-core` | `feat/browser-external-tools` |
| OpenCLI | `LasVie/OpenCLI` | `main`（与远端一致，无新增变更） |

**本次复验**：

- Swarm：OpenCLI、Gateway/ConfigAdapter 的浏览器选择项和桌面契约共 **112 项通过、205 项未选中**。
- Core：`tests/unit_tests/harness/tools/browser_move/` 和工具结果窗口处理器共 **559 项通过**。
- 前端：生产构建通过，保留构建产物体积的现有警告。
- Core 静态检查尚未通过：当前环境没有 `make` 和 `codespell`；直接运行 Makefile 对应的 Ruff/Pylint 检查仍有导入排序、格式和代码诊断。诊断保存在 `core-lint.log`，本次进度提交不附带整文件格式化或无关重构。
- 源码及新增文件未发现本次凭据格式检查所匹配的真实密钥；运行包约 6.5 MB。`.env`、浏览器 profile、依赖安装目录和仓外迁移备份不作为源码提交。
- Swarm 根目录的 Playwright MCP `console-*.log` / `page-*.yml` 加入忽略规则，自动生成的调试文件继续保留在本地。

复验日志和 XML 位于 `C:\Users\wangy\Documents\openJiuwen_OpenCLI\.migration-backups\20261013\git-publish\`。

这些提交保存的是当前进度。§8.10 的 A/B/C 发现尚未修复，完整应用验收仍为部分通过；M3 尚未开始，M4 尚未完成。

### 8.12 问题 A：主 Agent 分派修复（2026-10-14）

**结论**：针对 §8.10 的问题 A，在 Swarm 与 Core 两侧各做一处修改，使主 Agent 能得知 Browser Agent 具备站点命令，并且不再仅凭自己的 `tool_search` 未命中就判定能力不存在。单元测试已通过；真实模型复验尚未进行，问题 A 暂不标记为已解决。

**根因**：

- 主 Agent 依据子代理列表（`SubagentRail._build_available_agents_description`）判断能否委派。Browser Agent 卡片描述只写 Playwright，`apply_opencli_contribution` 只改 `spec.tools` 与 `spec.system_prompt`，没有改卡片，主 Agent 看不到站点名。
- Core 渐进式工具规则写有"最新目录覆盖……task_tool 或子代理描述中的工具名称"，且 `tool_search` 未命中时要求直接说明没有合适工具。

**修改**：

| 仓 | 文件 | 改动 |
| --- | --- | --- |
| Swarm | `jiuwenswarm/extensions/opencli/prompt.py` | 新增 `build_card_note()`（中英文），说明 Browser Agent 具备 OpenCLI 站点命令及启用的站点名（最多 30 个，其余以总数表示），提示涉及这些站点（包括提到 adapter 或站点命令）的任务应主动委派 |
| Swarm | `jiuwenswarm/extensions/opencli/__init__.py` | `Contribution` 增加 `card_note`；启用时用 `model_copy` 追加到 `spec.agent_card.description`，不修改可能共享的原卡片；关闭或不可用时不变 |
| Core | `openjiuwen/harness/prompts/sections/progressive_tool_rail.py` | 覆盖规则收窄为只针对被标记删除的工具；`tool_search` 未命中时先检查 `task_tool` 中的子代理，网页任务交给浏览器子代理（Core 提交及 `F_07`、`S_06` 不变量 8） |

**验证**：Swarm `tests/unit_tests/extensions/opencli/` 共 76 项通过，零暴露对比扩展到卡片描述，并新增卡片复制与长度测试；Core 渐进式工具、tool_search、prompts 与子代理 rail 相关共 144 项通过。

**待办**：在开发版桌面应用中用真实模型复验 §8.10 的分派对话及若干自然措辞变体，同时加入不应委派的任务，确认规则没有导致过度派发。问题 B、C 仍未处理；M3 尚未开始。

### 8.13 问题 A 复验，问题 B、C 修复（2026-10-14）

**结论**：问题 A 的真实模型复验通过（小样本）；问题 B、C 已在代码层修复并通过单元测试，尚未在完整应用中复验。复验中另发现两个新问题（见下表 D、E）。

**问题 A 复验**（开发版桌面应用，Single Agent，修复后重新启动）：

| 提示 | 主 Agent | Browser Agent | 结果 |
| --- | --- | --- | --- |
| §8.10 原失败对话（三步，"使用 Bilibili adapter"） | 首轮即调用 `task_tool → browser_agent` | 第 1、2 步完成（`opencli_run bilibili hot` → 页面）；第 3 步未执行 | A 通过；见 D |
| "Show me today's top 5 trending videos on Bilibili." | 直接委派，并说明 Bilibili 属于浏览器子代理支持的站点 | 一次 `opencli_run bilibili/hot`，5 行 | 通过 |
| "用知乎 adapter 搜一下 '大模型 Agent'" | 委派 | 需要登录，返回 `needs_user` 及侧栏处理说明 | 通过（登录流程符合设计） |
| CDP 解释、17×23、读取 README | 直接回答或使用文件工具，未委派 | — | 通过（规则未导致过度派发） |

**问题 B 修复**（列表与证据不一致）：

- 根因（Core）：字段别名缺少 uploader/UP主；证据每字段只保存一个值（外部结果只读 `extracted` 第一行，卡片探针只取第一张）；结果数量对所有来源取 `max()`，可由其他来源满足；summary 从未与证据比对。
- Core：外部 action 结果新增可选 `records`（行列表），卡片探针同样按行记录；任一来源报告过行时，"前 N 条"只由同一来源 N 行带齐所需字段满足；终态返回 `records`、`records_source`、`backed_result_count`；summary 中不在证据里的链接列入 `unbacked_items`，状态不变；task_tool 描述要求父 Agent 以 `records` 为准。见 Core `F_08`、`S_05` 不变量 15。
- Swarm：`opencli_run` 将每行（最多 20 行）作为 `records` 返回。

**问题 C 修复**（`rebind_context_model` 参数不兼容）：Core 分支 `feat/browser-external-tools` 落后 develop 62 个提交，develop 已在 `be7dadd2` 中支持 `model`、`model_config`、`model_client_config`。已将 `origin/develop` 合并进该分支；冲突处理：`runtime.py` 保留 develop 的槽位记录并只对 card_probe 记录行，`S_05`/`S_18` 保留 develop 的新不变量，本分支的不变量顺延编号。使用 Swarm 的实际参数调用已不再报错。

**提交**：

| 仓 | 提交 |
| --- | --- |
| Core | `4f7e936c` / `71896391` / `92799ab8`（B：代码 / 测试 / 文档）；`8fe3a978`（合并 develop，C） |
| Swarm | `01e1acfa`（B：`opencli_run` 输出 `records`） |

**验证**：合并后 Core 浏览器运行时、context engine、prompts、子代理 rail、tool_search 与渐进式工具相关共 1408 项通过、18 项跳过；Swarm OpenCLI、Gateway 适配与 Web 处理相关共 290 项通过。

**新发现**：

| 编号 | 现象 | 判断 |
| --- | --- | --- |
| D：多步任务提前结束 | §8.10 三步对话中第 2 步后子会话结束且标记为不可重试，第 3 步需由新的 Browser Agent 执行，不满足"同一 Browser Agent" | 推测为简单任务 240 秒期限（任务描述不含 compare/筛选等复杂词时使用），尚未核对该次耗时 |
| E：偶发缺少 OpenCLI 工具 | 14:35 的会话中（修复前），连续两次委派，第二次 Browser Agent 报告工具列表中没有 `opencli_describe` / `opencli_run`，日志无 `[opencli]` 警告 | 工具装配偶发问题，原因未定位 |

**待办**：在完整应用中复验 B（"返回B站热门前 3 条视频的标题、UP主和链接"，核对答复链接与 `records` 一致、无 `unbacked_items`）与 C（切换模型后日志不再出现 `unexpected keyword argument 'model'`）；调查 D、E；随后开始 M3。

### 8.14 问题 B、C 的完整应用复验（2026-10-14）

**结论**：B、C 在开发版桌面应用中复验通过。B 的混合路径（OpenCLI 加页面浏览）未在真实应用中复验；C 的报错已消失，但模型切换时 `rebound_contexts=0`，上下文是否随新模型重绑定尚待确认。

**环境**：修复与合并后重新启动开发版桌面应用（Single Agent，内置浏览器，OpenCLI 开启），真实模型 `anthropic/claude-opus-5.5`。结果取自会话历史中的 `browser_result` 与 `full.log`。

**问题 B 复验**：

| 项 | "返回B站热门前 3 条视频的标题、UP主和链接" | "Give me the top 5 Bilibili hot videos with uploader names" |
| --- | --- | --- |
| 会话 | `web_1a139827d72_8995cffbe51a` | `web_1a139832c3a_261d7febee13` |
| 状态 | `completed` | `completed` |
| 请求 / 有证据支撑的行数 | 3 / 3 | 5 / 5 |
| 证据来源 | `external:bilibili/hot` | `external:bilibili/hot` |
| 请求字段 | `title`、`author`、`url`（UP主 已识别） | `author`（uploader 已识别） |
| `unbacked_items` | 无 | 无 |
| 最终答复与 `records` | 3 条标题、UP 主、链接及顺序全部一致 | 5 条全部一致 |

与 §8.10 相比，答复不再使用其他来源的链接，并包含 UP 主。

**问题 C 复验**：

- 最后一条 `rebind_context_model() got an unexpected keyword argument 'model'` 出现在重启前的 15:21，重启后没有再出现。
- 会话 `web_1a13983e263_d7afbe7935e6` 中切换到 `deepseek/deepseek-v4-pro` 后，日志记录 `synchronized context model=deepseek/deepseek-v4-pro … rebound_contexts=0`，同步成功，切换后对话正常。
- 包括切换在内的所有同步记录均为 `rebound_contexts=0`：调用不再报错，但没有找到可重绑定的已缓存上下文。无法据此确认切换后该会话的 token 计数与上下文窗口已跟随新模型；需检查 develop 中 context engine 的上下文缓存键。

**待办**：在真实应用中复验 B 的混合路径（例如"B站热门前 3 条视频是什么？然后打开热门页面截图"）；调查 `rebound_contexts=0`；调查 §8.13 的 D、E；随后开始 M3。

**补充：问题 E 已确认非缺陷**。14:35:06 与 14:36:14 各有一次 `agent.reload_config`，对应用户在设置页关闭再开启 OpenCLI；缺少工具的 Browser Agent 在 14:35:16 创建，位于关闭期间。关闭时不装配工具、不记录警告属于设计行为（零暴露）。E 关闭，仅在今后出现未伴随设置变更的同类情况时重新调查。
