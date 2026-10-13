# OpenCLI adapters 的 JiuwenSwarm 设计

> 更新：2026-09-23。状态：待评审设计；本轮仅编写文档，未修改功能代码、安装运行包或执行集成测试。
>
> 前置：[总体架构](opencli-integration-architecture.md)、[Agent Core 设计](opencli-agent-core-design.md)、[CDP 调查](opencli-electron-cdp-research.md)。本文中的新增模块、配置及协议字段均为设计提案。

## 1. 产品行为与范围

Browser Agent 负责完整网页任务。它先从当前启用的站点 adapter 索引判断某个具体操作是否有覆盖：适用且可运行时，通过现有 shell 调用 OpenCLI adapter；其余步骤使用 Playwright。两种能力可以在一个任务中反复接续。

首期提供通用的网站 adapter 接入链路：从当前运行包发现已经配置好的网站 adapters，按统一规则生成能力视图和执行环境。逐站专项适配按实际需求渐进补充。Playwright 继续提供打开页面、观察、点击、输入、截图等通用网页能力。OpenCLI 运行包按原作者发行物固定版本使用，未来自维护发行物通过相同运行包边界替换。

Swarm 的工作集中在以下五件事：

1. 根据用户设置和实际浏览器条件，决定给哪个 Browser Agent 装配哪些 adapter。
2. 提供轻量索引和渐进 Skill，使能力发现与操作说明留在 Browser Agent 内。
3. 为正常 shell 调用准备确定的运行包、当前页面连接及执行条件。
4. 让 adapter 与 Playwright 共享 Electron profile 和任务页面，并正确处理并发、状态变化和故障。
5. 在配置、任务进度和诊断中解释能力是否可用、发生了什么及如何接续。

通用 OpenCLI browser 命令、现场探索网站、生成 adapter、桌面应用 adapter 和远端浏览器执行不属于首期功能。Core 的通用扩展边界继续保留。

## 2. 模块与进程职责

### 2.1 运行结构

~~~mermaid
flowchart TB
    UI[浏览器设置与任务进度] --> GW[Gateway：配置请求与状态展示]
    GW --> AS[AgentServer：当前配置与 Agent 装配]
    AS --> Mount[Browser Agent 挂载流程]
    Mount --> BA[Browser Agent]
    Catalog[选定 adapter 索引与 Skill] --> BA
    BA --> Shell[现有 shell 工具]
    BA --> PW[Playwright 工具]
    Shell --> Scope[OpenCLI 调用作用域]
    Scope --> CLI[固定发行物中的 adapter]
    Scope --> Coord[Python 浏览器协调客户端]
    PW --> MCP[目标绑定 MCP wrapper]
    Coord --> Host[Electron：页面解析与操作协调]
    MCP --> Host
    CLI -->|精确页面 CDP| Page[当前任务页面]
    MCP --> Page
    Host --> Page
    Host --> Profile[共享持久化 profile]
~~~

### 2.2 模块责任

| 模块 | 责任 | 拥有的状态 |
| --- | --- | --- |
| OpenCLI 应用扩展 | 配置接入、诊断、包可用性和关闭流程 | 产品启用状态、运行包准备状态 |
| `harness.py` | Browser Agent 的装配、挂载核对、卸载 | 每个 Agent 的挂载版本、LoadRecord、资源归属 |
| `commands.py` 与 Skill | adapter 元数据索引、命令识别、覆盖范围和操作说明 | 有效 adapter 快照、兼容记录、可见 Skill |
| `runtime.py` | 运行包定位、版本/来源核对、调用局部环境 | 已选发行物和入口；按版本共享的准备结果 |
| `rail.py` | 登记 Core shell 执行作用域、每次调用准入及收尾 | 单次调用的绑定、租约、进程状态 |
| `evidence.py`（按需） | 有可靠解析规则时，将 adapter 输出转换为既有浏览器证据 | 按调用提交的证据；普通 adapter 直接沿用 shell 原输出 |
| Electron coordinator 客户端 | 实现 Core 所需的宿主协议 | 逻辑任务身份、当前宿主连接、在途请求 |
| Electron 宿主 | 存储、页面生命周期、操作协调与页面代次 | profile、页面集合、租约、待核实操作记录 |

Gateway 和 AgentServer 即使运行在同机，也分别持有自己的进程状态。Gateway 通过现有 Agent 请求链路读取运行状态；LoadRecord、CLI 进程和页面租约由实际执行所在的 AgentServer/宿主维护，不能依赖 Gateway 内的同一个 Python 对象。

接入包建议放在 `jiuwenswarm/extensions/opencli/`，沿用 ApplicationPluginExtension 和 extension.yaml。应用扩展注册与 Core PluginSpec 挂载分别完成：前者提供产品能力入口，后者挂到实际 Browser Agent。

扩展初始化保持轻量，只登记服务和读取必要配置。上游 Node 包的安装、adapter 索引生成和浏览器连接在启用后的准备阶段进行。扩展 manifest 的 Python dependencies 不承担 Node 运行包安装。

## 3. 配置、就绪状态与产品展示

### 3.1 配置来源

建议沿用浏览器设置的持久化位置：

~~~yaml
browser:
  chrome_path: ""
  opencli:
    enabled: false
    enabled_adapters: null
~~~

| 字段 | 语义 |
| --- | --- |
| `enabled` | 用户是否启用 adapter 能力；开发与首批验证阶段默认 false |
| `enabled_adapters` | 原 adapter 的规范站点/命令名称列表；null 使用已发现且满足通用运行条件的网站 adapter 集合，空列表表示没有选中操作 |
| 固定发行物、入口与版本 | 来自接入包的兼容配置和部署记录；高级开发路径覆盖单独校验，普通设置页无需暴露命令拼接细节 |

配置中的规范名称只是上游命令身份，用于筛选和核对；模型执行实际 CLI 命令。首期 UI 提供总开关和已发现的网站/操作及可用状态清单，细粒度筛选可先由配置完成。

设置写入采用字段合并，保留 chrome_path、headless 和其他已有值。OpenCLI 开关变化触发能力核对；只有浏览器本身的配置变更才沿用当前浏览器重启流程。

### 3.2 统一启用判断

单 Agent、Code 和 Swarm 成员使用同一判断函数。先检查用户配置，再检查执行模式和宿主条件：

| 条件 | 结果 |
| --- | --- |
| 用户关闭或接入包未安装 | Browser Agent 使用原有能力；不注入 adapter 提示、工具贡献、Skill 或自动探测 |
| 配置了外部浏览器 | 保留用户开关值，有效状态显示“当前浏览器模式暂不支持”；本期所有 adapter 能力暂停 |
| 未选择/无法发现内置 Electron 宿主 | 暂不可用；不把任意 localhost CDP 或默认浏览器视为该宿主 |
| 当前执行环境无法使用宿主本机 CLI | 暂不可用；已有沙箱和权限模式保持有效 |
| 运行包缺失或版本/来源不兼容 | 显示准备或诊断信息，网页任务继续使用 Playwright |
| 选定 adapter 集合为空 | 显示没有可用操作，不挂载无内容的 adapter Skill |
| 运行条件满足 | 给 Browser Agent 挂载当前有效 adapter 集合 |

首期只支持与 Electron 同机的本地 CLI 执行。远端成员或不能连接该宿主的沙箱成员返回明确的能力缺口；本期不因接入 OpenCLI 将执行从沙箱搬到宿主机。

即使某个站点 adapter 不依赖浏览器，也遵循本期统一的产品启用条件；进入执行后再按其实际依赖决定是否取得页面资源。这样各模式中的能力范围一致。

### 3.3 状态与用户反馈

持久化的“已启用”与运行时的“可使用”分别展示。运行状态使用：关闭、待准备、可使用、部分操作不可用、宿主不可用、当前模式不支持、正在停用。

设置页建议继续使用现有浏览器模块：开关、有效状态、已发现的网站/操作数量、可用状态及简短原因。准备或检查动作在用户进入设置或启用后执行，普通任务遇到缺少运行包时给出明确状态并继续网页路径。升级固定发行物由显式管理动作完成。

Browser Agent 的工具时间线保留 shell 调用，可附加“使用某站点 adapter”“等待页面”“改用页面操作”“结果待核实”等简短标签。主 Agent 接收任务结论、关键证据与阻塞原因，adapter 帮助和完整终端输出主要保留在 Browser Agent 内。

## 4. Browser Agent 装配与可插拔生命周期

### 4.1 统一装配入口

拟在 `harness.py` 提供应用内部 helper：

| 入口 | 用途 |
| --- | --- |
| `configure_browser_integration(browser_spec, context)` | 根据当前配置为 Browser Agent 配置准备宿主 coordinator、轻量挂载 rail 和所需运行时上下文 |
| `reconcile_opencli_mount(agent, context)` | 在实际 Browser Agent 上比较配置/能力版本，调用现有 load_plugin_spec 或 unload_extension，返回当前挂载状态 |

这两个 helper 服务应用装配；用户和模型继续使用原 Browser Agent 与原工具。

| 装配入口 | 注入身份与职责 |
| --- | --- |
| `interface_deep.py` | 单 Agent 会话身份与当前配置；装配 Browser Agent 时调用 helper |
| `interface_code.py` / CodeBuildContext | Code 会话身份、原 SysOperation/权限和浏览器配置；调用相同 helper |
| `swarm/providers/code_subagents.py` / SwarmBuildContext | session_id、唯一 member 身份及已有任务分支关联；成员恢复后重建当前上下文 |

主 Agent 上的普通聊天 plugin_names 不能自动传播成 Browser Agent 的 adapter 能力；OpenCLI 使用上述明确的子代理装配路径。

### 4.2 从配置到实际挂载

现有装配多返回 SubAgentConfig，Browser Agent 实例稍后才创建。因此建议使用一个应用侧的轻量挂载 rail：

1. 当前配置启用接入时，在装配配置中附加挂载 rail；它自身不提供模型工具、Skill 正文或站点目录。
2. 在实际 Browser Agent 的 BEFORE_INVOKE 阶段，通过 ctx.agent 取得外层 Agent，核对当前配置并调用 reconcile。
3. reconcile 构造 PluginSpec，挂载提示、Skill、必要的现有 shell 和 OpenCLI 执行接入 rail；保存 LoadRecord。
4. 接入 rail 的初始化登记 shell 执行作用域，完成准备后才允许第一次模型调用。
5. 原生 BrowserRuntimeRail 按既有生命周期运行；新挂载需要的初始化显式完成，不假定刚注册的 BEFORE_INVOKE 回调会在本次事件分发中自动执行。

当前 BEFORE_INVOKE 位于 DeepAgent 外层，load_plugin_spec 是已有公开入口。挂载顺序、热加载初始化和回滚仍是实施阶段必须验证的边界。

对实际 Agent 实例串行核对，使用“接入包版本 + 配置版本 + adapter 快照”形成挂载版本。配置相同则复用；有变化时安全切换到新快照。每个 child instance 持有自己的 LoadRecord，进程共享的只读索引和运行包记录独立缓存。

### 4.3 禁用和恢复

关闭能力时，AgentServer 先推进配置版本，停止接受新的受管 adapter 调用。准备中的命令在启动前再次核对版本；已经执行的命令按正常完成或用户取消路径收尾。状态变化不能让普通写操作自动重跑。

完成在途收尾后，卸载提示、Skill、接入 rail、登记句柄及本包独占的 shell。宿主原有 shell 和其他能力的资源按各自归属保留。控制用挂载 rail 可以在缓存实例中保留为空闲配置观察者，它不提供模型能力，也不启动探测；实例重建后只按当前配置装配。

新配置通过现有配置更新链路通知活跃实例，并在下一次 invoke 和每次受管调用启动前复核。跨进程使用配置版本与 seed 重建；恢复状态只包含逻辑身份和重建依据，不能恢复旧 endpoint、lease 或 LoadRecord 对象。

从关闭切换到启用时，已有缓存实例可能没有挂载 rail。配置刷新流程需在安全边界重新装配该实例或重建子代理配置，并保留任务历史与逻辑页面身份；不能依赖一个尚未安装的观察者完成首次启用。

历史对话保留；后续主动注入的提示、Skill 列表及工具贡献反映当前配置。未启用时的验证指标应包括上下文差异和运行包探测次数。

## 5. Adapter 索引、Skill 和运行包

### 5.1 有效 adapter 集合

有效集合由以下条件共同确定：

**实际安装且来源明确的网站 adapter ∩ 用户选择 ∩ 通用运行条件，排除已知不支持的操作。**

单个网站尚未做专项回归，不单独构成禁用理由。运行包和基础 CDP 链路经过验证后，普通 adapter 可使用通用路径；其站点验证状态如实标注。兼容补充记录用于已知限制、修正及经过验证的优化。

索引沿用上游站点/命令名称、别名、domain、description、args 和输出说明。Swarm 只补本次接入需要的运行事实：

| 信息 | 用途 |
| --- | --- |
| 实际运行包与 adapter 来源/内容版本 | 保证发现的操作和实际执行的操作一致 |
| 当前传输条件及站点验证状态 | 分别记录能否进入通用执行、是否经过站点专项回归以及已知限制 |
| 是否需要浏览器、页面影响 | 决定绑定、租约和观察失效 |
| 是否已验证同页并发读取 | 默认页面独占；有证据时才放宽 |
| 可选的认证前提、结果核实方法、证据转换版本 | 上游说明优先；专项记录可逐步补充，缺少时使用通用输出与页面核实 |
| Skill 相对路径 | 让 Browser Agent 读取实际操作说明 |

网站范围优先依据上游元数据和命令分类生成，缺少分类时可以用少量声明式范围补充；仅一个 domain 字段不足以区分全部命令。桌面 adapter、外部 CLI 和通用 browser 能力不进入该索引。分类不明的条目先列为待分类，普通网站无需在 Swarm 编写专用执行实现。

通用默认值是：浏览器依赖不明确时准备当前页面；页面影响不明确时独占该页并在结束后使观察失效；没有可靠幂等声明时不自动重试；没有专用输出转换时保留原结果。依赖不支持的 CDP 接口、多页行为或其他运行条件时，记录具体限制并由 Playwright 接续。

上游 `opencli list -f json` 能输出结构化命令元数据，可作为索引核对入口；操作参数和帮助由上游提供。该命令的完整启动可能执行用户插件初始化，因此索引刷新属于可信运行包准备过程，不能当作对任意插件目录的无副作用文件读取。

### 5.2 渐进式披露

| 时机 | Browser Agent 获得的内容 |
| --- | --- |
| 能力挂载 | 一段选择规则、adapter Skill 的短描述 |
| 首次需要匹配站点 | 当前有效集合的简短网站索引 |
| 定位站点 | 该站点支持的操作摘要 |
| 准备执行 | 对应操作文件中的原 CLI 用法、前置条件、结果语义和接续建议 |

Skill 选择 `directory_view=none`。根索引仅包含当前有效站点，操作文件按需读取；完整上游 Skill 库不会整体加入上下文。

接入包保存通用 Skill 模板，网站和操作说明优先根据当前运行包的元数据、help 与已有说明生成；专项补充覆盖相应条目，无需为每个网站手写文档。按启用集合生成只读挂载视图，建议缓存于用户数据目录 `runtime_state/opencli/skills/<catalog_revision>/`。视图内的索引、站点文件和操作文件均按有效集合裁剪，禁止因读取根文件而展示禁用操作。切换快照后，旧视图在最后一个挂载释放时清理。

未命中结果在任务内缓存；adapter 快照变化重新匹配，登录或宿主恢复只刷新受影响的运行条件。能力选择由 Browser Agent 依据任务语义完成，运行时确认该命令属于当前有效集合并满足执行条件。

### 5.3 发行物和实际来源

当前建议基线是原作者 `@jackwener/opencli` 的固定发行物；本地研究源码版本为 1.8.8，具体发行物与 Node 入口需在连接验证阶段核对。开发使用本地 Core editable 依赖，同时检查 AgentServer 子进程的实际导入路径。

runtime.py 记录 Node 可执行路径、包根目录、CLI 入口、包版本及所选 adapter 的实际来源快照。模型优先使用普通 `opencli <site> <command> ...` 命令形式，由调用局部 PATH 指向已选发行物；作用域须核对实际解析入口，处理 PowerShell alias/function 优先级和 shell 启动配置。无法保证解析结果时，Skill 提供正确引用的绝对原 CLI 入口形式，实际命令经过原权限检查。

路径包含空格、中文和跨磁盘是正式验收项。避免通过共享工具对象或进程全局环境保存当前页面、当前包路径。运行期间固定当前发行物，准备新版本后在安全的调用边界切换。

**包版本与 adapter 来源必须一起核对。** 当前上游会依次发现内置 adapters、用户 adapters 和用户插件，同名条目可被后加载来源覆盖。索引必须反映真实生效的来源；覆盖变化使旧帮助、并发优化和兼容记录失效，重新生成视图后按通用条件判断。来源无法确认，或插件导致运行入口/页面绑定契约无法成立时，才将相应操作或环境标为不可用。保留用户现有目录，不通过清空覆盖文件解决绑定问题。

为得到可核对的有效来源，需要检查源码清单、用户覆盖目录和实际命令发现结果；准备前后的快照须一致。普通任务期间不修改 adapter 文件；检测到来源变化时使兼容与 Skill 缓存过期。未来自维护发行物仍使用相同来源记录与验证流程。

## 6. Shell 调用与结果接续

### 6.1 一次调用

1. Browser Agent 选择操作并读取 Skill，向已有 Bash/PowerShell 提交原 CLI 命令。
2. 原权限检查完成后，执行作用域核对当前配置版本、运行包入口和 adapter 身份；复杂组合无法明确识别时提示拆成直接命令。
3. 根据上游元数据、通用默认值及可选兼容补充确定执行条件。明确无浏览器依赖的操作只准备 CLI 环境；其余操作向 coordinator 解析当前任务页面并申请租约。
4. 取得租约后再次校验宿主/页面代次，向本次子进程注入精确页面的 `OPENCLI_CDP_ENDPOINT`，记录操作已开始，再由 shell 启动 CLI。
5. 收集原进程结果并按页面影响更新状态；存在可靠转换规则时再提交可验证事实。普通 adapter 无需专用证据转换器即可执行。
6. 在结束冲突操作区间前完成状态记录，finally 释放本次资源。Browser Agent 读取原输出决定下一步。

首期支持正常前台/流式调用。复杂别名、嵌套脚本、后台脱离进程及命令内并行形式不获得受管页面绑定。OpenCLI 通用 browser 命令给出范围说明并指向 Playwright。普通 shell 命令继续使用自己的权限与执行路径。

### 6.2 失败和接续

| 结果 | Browser Agent 与运行时的下一步 |
| --- | --- |
| 没有适用 adapter | 直接使用 Playwright；无需试跑不存在的命令 |
| 登录失效 | 暂停该操作，通过页面完成认证；相关认证与观察状态更新后再评估 adapter |
| 已知传输不支持 | 使用 Playwright 完成当前步骤，按操作/来源/传输缓存不可用原因 |
| 明确空结果 | 作为正常查询结果解释，按任务需要调整条件 |
| 参数错误或来源已变化 | 在未执行前解释具体问题，重新读取帮助或刷新索引 |
| 进程退出但业务结果不足 | 阅读输出，必要时通过页面核实；退出码不直接产生“任务完成”证据 |
| 写操作超时、断连、取消 | 标记结果待核实；先观察业务状态，才能决定继续或重试 |

一个站点或操作失败不会使整个任务永久退出 adapter 路径。接续仍由同一个 Browser Agent 完成。用户指定页面查看或截图时，按其要求实际执行。

需要用户手动登录时，先让当前自动操作安全结束并释放页面独占占用，再让用户操作；恢复后更新认证状态并重新观察。共享 profile 意味着账号切换可能影响其他会话，这一点在页面操作提示与恢复判断中体现。

## 7. Electron 页面与协调协议

### 7.1 页面身份

沿用 `persist:jiuwenswarm-browser` 持久化 partition。业务网页与产品可信 UI 保持分离；绑定只能解析到该任务的网页 WebContents。

页面逻辑键为 `session_id + member_id + branch_id`。默认 branch 使用当前会话/成员主页面；确实独立的任务分支由现有子任务运行身份派生 branch_id，并在调用前注入可信上下文。同一分支的 CLI 和 MCP 始终解析同一逻辑页。

首期首先交付已有会话/成员独立页面的并发。单个 Browser Agent 的普通多步任务持续使用同一页面。额外工作页只在有明确分支身份时分配，限制活跃数量；不能看到两条 shell 命令就自行判断它们可以换页并发。adapter 自身的任意多标签页逻辑单独按兼容性验证。

拟返回的绑定信息如下，连接和租约字段仅供可信运行时使用：

| 字段 | 含义 |
| --- | --- |
| session_id / member_id / branch_id | 任务归属，由运行时传入并经宿主校验 |
| page_id / profile_id | 宿主管理的逻辑页面与共享存储身份 |
| host_epoch / page_epoch | 宿主重启、页面重建的代次 |
| state_revision / auth_revision | 页面观察与共享认证状态的版本 |
| target_id / page_ws_endpoint | 与实际 WebContents 对应的精确页面连接 |
| protocol_version / capabilities | 宿主协议版本和已支持的协调能力 |

页面 WebSocket 由宿主依据已登记 WebContents 的 TargetID 从本地调试目标中精确核对；目标消失时明确失败。浏览器级 endpoint 只在宿主/受信任 MCP 内部使用。

### 7.2 宿主接口

建议在现有 loopback target resolver 上增加版本化操作接口。以下名称描述拟定语义，最终 URL 在实现评审时固定：

| 操作 | 输入与结果 |
| --- | --- |
| resolve page | 校验任务归属，取得或恢复页面，返回绑定和保活句柄 |
| acquire operation | 按 page/epoch、call_id、占用方式和剩余期限申请租约，返回最终有效绑定与租约凭据 |
| renew operation | 更新活跃调用的租约；仅在拥有者与代次有效时接受 |
| start operation | 登记已进入真实执行阶段；相同调用的重复开始必须识别 |
| finish operation | 记录进程/传输完成事实、页面影响及是否待核实，更新版本并结束占用 |
| release page | 释放调用方的保活引用，由宿主按既有回收规则管理页面 |
| read revisions | 查询页面/认证版本与待核实状态，恢复或下一次执行前进行核对 |

沿用 loopback、Bearer token、拒绝浏览器 Origin 请求的现有边界。请求具有 call_id，租约申请和收尾可以幂等重试；这个幂等性仅针对宿主控制请求，不能据此重跑 CLI 或网页写操作。

保活租约与操作租约分别管理：前者阻止宿主回收页面，后者覆盖一次完整动作。取得操作租约时隐含保活引用，释放操作引用不等于关闭页面。

### 7.3 并发策略

| 场景 | 初期策略 |
| --- | --- |
| 不同页面、独立操作 | 并发执行 |
| 同页操作 | 默认独占，覆盖整个 adapter 调用或 Playwright 复合动作 |
| 同页已验证纯读取 | 共享读租约，兼容记录必须证明无导航、页面全局状态或网络拦截配置变化 |
| adapter 内部请求并发 | 保留适配器自身逻辑，外层租约覆盖整个调用 |
| 已知登录、退出或账号切换 | 使用共享认证协调，更新 auth_revision，使相关观察与账号判断过期 |

为简化首期实现，建议每个页面操作同时持有 profile 认证共享占用，已知认证变更取得该 profile 的认证独占占用。普通操作之间仍可跨页并行；只有认证变更短暂协调整个共享 profile。按 origin 细分可在确有并发收益后细化。

认证占用与页面占用由宿主一次性申请，使用一致次序和有界等待，避免分别拿锁后互相等待。页面行为未知时默认独占，结束后刷新观察；经过验证的行为声明才可放宽同页并发。已知会修改认证状态的动作使用认证独占占用；未声明的 Cookie/存储变化还需通过宿主可观测事件推动状态失效，不能宣称认证锁涵盖了所有网页后台变化。

页面租约协调自动执行器。用户直接操作和网页后台脚本不会自动遵守它；宿主可观测的导航/页面变化推进版本，恢复时重新观察。需要严格接管顺序时采用“暂停自动操作—用户操作—恢复”的交互，不能把租约宣称为浏览器页面完全静止的保证。

### 7.4 MCP 调用关联与复合操作

Python runtime 在操作作用域中持有调用/租约关联。adapter 路径由 shell 作用域持有租约；Playwright 路径需要将相同关联传到 target_mcp_wrapper。

建议使用 MCP 请求 `params._meta` 的应用命名空间承载 call_id、lease 凭据和页面代次，由可信调用上下文注入。它与工具的模型参数分开，wrapper 在调用实际工具前核验并消费。MCP 为附加元数据提供了该字段；具体本地 SDK 的发送与接收需验证。[MCP 元数据约定](https://modelcontextprotocol.io/specification/2025-11-25/basic#meta)

现有 Core stdio/Playwright 客户端主要透传工具名称和 arguments，因此“把租约写入 _meta”仍是一项待补的 Core 联调能力，不能只改 Swarm wrapper。该缺口见第 10 节。

root 操作取得一次租约；内部观察、Probe、恢复及 batch 的子步骤继承它。每个 MCP 子调用保留自己的消息 ID 和子调用关联，宿主核对其 parent operation。wrapper 有可信父租约时复用，缺少父租约的独立调用按当前页面申请自己的租约。两者不能同时为同一动作重复申请互斥占用。

callback、MCP transport、子进程和宿主之间的取消/异常收尾需要联调。该路径尚未通过验证前，不能宣称两类执行器的同页并发安全。

### 7.5 结果不确定、宿主重启与页面恢复

进程被取消或 lease 到期后，已发出的网页请求可能仍在执行。宿主与任务运行时分别保存自己的事实：是否已派发、是否返回、页面版本和是否需要核实；业务完成仍由任务证据判断。

建议在宿主用户数据目录保存最小的在途/未决操作日志：调用身份、页面、代次、操作类别和时间。对可能产生副作用的操作在派发前登记，已完成后收尾；不保存登录令牌或整段命令参数。宿主重启发现未收尾记录时，将其转为待核实，由任务恢复处理。

记录待核实状态不会无限持有旧 mutex。宿主允许指定的观察/核实步骤进入，但在确认前阻止同一未决范围的自动重复写入。新页面不能证明旧业务请求失败，不能通过换页消除未决状态。

恢复流程为：重新发现宿主 → 检查配置与 adapter 来源 → 解析新的页面绑定 → 检查未决记录 → 获取新观察 → 继续任务。旧 TargetID、lease 和 refs 均需重新核对。

## 8. 状态同步、证据与运行记录

普通 adapter 的原始输出直接返回 Browser Agent，不要求逐站解析器。接入包有可靠转换规则时，再把事实提交给 Core 的既有证据结构；否则通过已有页面观察补充 runtime 所需证据。页面失效通知携带 page、call_id 和变化原因，与 shell 输出分别处理。

单次调用完成时，先记录页面/认证版本与必要证据，再允许冲突操作接续。不同 Agent 对共享认证状态的同步，首期可以在每次取得操作租约时比较 auth_revision；页面版本在下一次观察和真正执行元素动作前再次检查。

原始 stdout/stderr、截断和文件引用沿用 shell。诊断记录额外关联运行包版本、adapter 来源、规范命令名、会话/成员、页面、租约等待时间、进程时长和接续原因。endpoint、租约凭据和完整敏感参数不进入普通 UI 或模型提示。

需要区分三种失败：能力未覆盖、环境不可用、已执行但结果不确定。前两类通常可以直接继续适合的 Playwright 步骤，第三类先核实。评估统计也按这个分类，避免把正常“无 adapter”当作产品错误。

## 9. 文件清单

以下路径相对新仓根目录。“新增”为拟新增；本轮只编写和同步设计文档。总体方案中的清单作为概览，具体职责以本节为准。

### 9.1 接入包

| 类型 | 文件 | 职责与本轮细化 |
| --- | --- | --- |
| 新增 | `jiuwenswarm/extensions/opencli/__init__.py`、同目录 `extension.yaml`、`extension.py` | 应用扩展声明、轻量服务注册、配置/诊断入口和产品关闭流程 |
| 新增 | `jiuwenswarm/extensions/opencli/settings.py` | 统一启用条件、配置解析、当前配置版本及状态原因 |
| 新增 | `jiuwenswarm/extensions/opencli/harness.py` | 两个装配 helper、轻量挂载 rail、PluginSpec、LoadRecord、挂载版本及生成的 Skill 视图 |
| 新增 | `jiuwenswarm/extensions/opencli/commands.py` | 有效 adapter 索引、规范名称/别名、直接命令识别、来源快照和兼容查询 |
| 新增 | `jiuwenswarm/extensions/opencli/compatibility.yaml` | 固定发行物、通用运行约束及可选的分类/兼容补充；记录已知限制与验证过的优化，不作为逐站准入白名单 |
| 新增 | `jiuwenswarm/extensions/opencli/runtime.py` | 实际 Node/CLI 入口核对、运行包准备及局部环境；关注 Windows 路径和用户覆盖来源 |
| 新增 | `jiuwenswarm/extensions/opencli/rail.py` | Core shell 作用域工厂、调用准入、绑定、租约、结果观察与可靠收尾 |
| 按需新增 | `jiuwenswarm/extensions/opencli/evidence.py` | 存在可靠输出契约时实现证据转换；普通 adapter 使用原输出及既有页面证据 |
| 新增 | `jiuwenswarm/extensions/opencli/skills/opencli/SKILL.md` | adapter 选择规则与短索引的模板 |
| 运行时生成 | `runtime_state/opencli/skills/<catalog_revision>/sites/<site>/index.md`、站点内 `operations/<operation>.md`（用户数据目录） | 按发现结果与上游帮助生成、按启用范围裁剪；站点专项说明以后按需补充 |

### 9.2 Agent 装配与宿主

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py)、[interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py) | 调用统一装配 helper；配置变更、缓存实例、原权限/SysOperation 和当前会话身份贯通 |
| 修改 | [Code spec.py](../../jiuwenswarm/agents/harness/code/spec.py)、[Swarm context.py](../../jiuwenswarm/agents/swarm/context.py)、[registry.py](../../jiuwenswarm/agents/swarm/registry.py) | 传递可信句柄与可重建身份；接收进程按当前配置重新装配 |
| 修改 | [code_subagents.py](../../jiuwenswarm/agents/swarm/providers/code_subagents.py)、[browser_runtime.py](../../jiuwenswarm/agents/swarm/browser_runtime.py) | Swarm Browser Agent 采用相同 adapter 门控、宿主 coordinator 和成员身份 |
| 修改 | [electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py) | 从现有发现信息取得宿主身份和新协议能力；页面 endpoint 留在局部调用 |
| 新增 | `jiuwenswarm/agents/harness/common/electron_browser_coordinator.py` | Core coordinator 协议的 Python 实现、页面解析、租约、版本及重连 |
| 修改 | [browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs) | 逻辑页面与分支身份、代次、精确页面 endpoint、新协议路由；保活与操作占用衔接 |
| 新增 | `jiuwenswarm/channels/desktop/electron/browser_operation_leases.cjs` | 页面/认证协调、调用归属、重复控制请求及在途/未决日志 |
| 修改 | [main.cjs](../../jiuwenswarm/channels/desktop/electron/main.cjs) | 装配协调服务；发布协议能力、宿主代次；接入页面创建/导航/销毁事件 |
| 修改 | [target_mcp_wrapper.cjs](../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs) | 消费可信请求元信息，核验/复用父租约，按消息 ID 跟踪完成和取消，维护精确页面连接 |

### 9.3 设置与开发配套

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [resources/config.yaml](../../jiuwenswarm/resources/config.yaml)、[common/config.py](../../jiuwenswarm/common/config.py) | browser.opencli 配置示例、合并更新、配置版本与重载 |
| 修改 | [config_adapter.py](../../jiuwenswarm/server/runtime/gateway_adapter/config_adapter.py)、[app_web_handlers.py](../../jiuwenswarm/gateway/channel_manager/web/app_web_handlers.py) | 贯通配置/状态；将能力装卸与浏览器整体重启区分 |
| 修改 | [browser/definition.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition.ts)、[settingsContract.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/services/settingsContract.ts)、[SettingsSourceProvider.tsx](../../jiuwenswarm/channels/web/frontend/src/features/settings/services/SettingsSourceProvider.tsx) | 声明式开关、状态、只读支持范围；遵循现有设置组件与字段来源契约 |
| 修改 | [zh.json](../../jiuwenswarm/channels/web/frontend/src/i18n/locales/zh.json)、[en.json](../../jiuwenswarm/channels/web/frontend/src/i18n/locales/en.json) | 补双语设置、状态和接续原因文案 |
| 修改 | [pyproject.toml](../../pyproject.toml)、[uv.lock](../../uv.lock) | 本地 Core 开发依赖，打包 Skill/兼容数据；锁文件由依赖工具生成 |
| 新增 | `docs/development/opencli-local-setup.md` | 主进程/AgentServer 导入检查、运行包路径、adapter 来源核对及隔离 fixture 验证步骤 |
| 修改 | [Electron README](../../jiuwenswarm/channels/desktop/electron/README.md) | 实现后同步页面身份、协调协议、接管与诊断流程 |

### 9.4 验证文件

| 类型 | 文件 | 验证重点 |
| --- | --- | --- |
| 新增 | `jiuwenswarm/extensions/opencli/tests/test_settings.py`、`test_harness.py` | 三种模式一致、默认关闭、BEFORE_INVOKE 首次挂载、热装卸、缓存及恢复 |
| 新增 | 同测试目录 `test_commands.py`、`test_runtime.py` | 索引裁剪、未命中、同名覆盖/来源变化、真实入口、空格/中文路径、版本固定 |
| 新增 | 同测试目录 `test_rail.py`；有证据转换时补 `test_evidence.py` | 局部环境、页面归属、准备失败、取消、原结果及完成证据 |
| 修改 | [browser_panels.test.cjs](../../tests/electron/browser_panels.test.cjs)；新增 `tests/electron/browser_operation_leases.test.cjs` | 保活、代次、跨页并发、同页冲突、共享读、认证协调与未决恢复 |
| 修改 | [test_electron_sideview.py](../../tests/unit/harness_common/test_electron_sideview.py)、[test_electron_browser_target.py](../../tests/unit/test_electron_browser_target.py)；新增 `tests/unit/harness_common/test_electron_browser_coordinator.py` | 发现、精确绑定、协议版本、断连和取消 |
| 修改 | [test_electron_browser_fallback.py](../../tests/agents/swarm/test_electron_browser_fallback.py)、[test_browser_subagent_integration.py](../../tests/unit/deep_agent/test_browser_subagent_integration.py) | 各模式实际装配、外部浏览器、沙箱/远端条件及当前配置 |
| 新增 | `tests/electron/opencli_integration.cjs` | fixture adapter 经真实 shell/CLI 操作准确页面、共享存储、双向接续和宿主存活；复用已有 fixture |
| 修改 | [settingsRefactor.test.mjs](../../jiuwenswarm/channels/web/frontend/tests/settingsRefactor.test.mjs) | 设置字段、状态和条件展示；实现 UI 时按仓内约定做浏览器视觉检查 |
| 新增 | `tests/electron/opencli_task_cases.md` | 任务级验证输入、期望能力选择和证据：命中、未命中、部分覆盖、认证接续和未决写入 |

## 10. 与 Core 的对接条件

| 条件 | Core 责任 | Swarm 责任 |
| --- | --- | --- |
| 按挂载项披露 | Skill 配置、可见视图、准确卸载 | 生成有效 adapter Skill 视图与短提示 |
| shell 执行作用域 | 正常/流式生命周期、调用局部 environment、原结果、取消和收尾 | 命令识别、固定入口、页面资源、adapter 结果处理 |
| BrowserTaskAccess | 公开绑定/协调/失效/证据入口 | Electron coordinator 实现和身份注入 |
| 外部页面变化 | refs 有效性检查、观察刷新、完成证据 | 在租约结束前提交变化与可验证事实 |
| MCP 调用关联 | 可信调用元数据从 runtime 到具体客户端发送路径，默认无元数据时保持兼容 | wrapper 校验租约、宿主确认归属及复合动作关联 |
| 挂载生命周期 | load/unload 的资源归属、接入 rail 初始化/收尾 | BEFORE_INVOKE 核对与 LoadRecord 管理 |

MCP 关联的初步代码落点是 Core 的浏览器调用路径及 `core/foundation/tool/mcp/base.py`、`client/mcp_client.py`、`client/stdio_client.py`、`client/playwright_client.py`。需要同时验证正常 MCP 工具调用和 Browser runtime 内部调用；具体签名在 Core 接口评审时确定，不能仅靠进程全局变量传递“当前 lease”。

首期围绕本地目标绑定的 stdio 链路验证。协议字段有规范依据并不代表当前 SDK 已完成透传；底层库、当前客户端和 wrapper 的端到端测试是接口定稿条件。

## 11. 实施顺序与评审重点

| 阶段 | 交付内容 | 完成条件 |
| --- | --- | --- |
| S1：固定运行基线 | 本地 Core、上游发行物、实际 adapter 来源、隔离 fixture adapter | 实际 CLI 入口可用，来源可核对，准确连接 Electron 工作页 |
| S2：最小装配闭环 | 配置判断、挂载 helper、有效索引、渐进 Skill、shell 接入 | 一个 adapter 可从 Browser Agent 使用；无匹配操作直接走 Playwright；禁用无新增上下文 |
| S3：两条路径协调 | 宿主 lease、MCP 关联、状态版本、认证共享与取消 | 跨页实际并发，同页冲突隔离，batch 不重复加锁，断连不误关宿主 |
| S4：结果与恢复 | 通用原输出/页面证据、在途/未决记录、宿主重启和能力热更新 | shell → Playwright → shell 连续；写入不明先核实；恢复不使用旧连接 |
| S5：产品与通用验收 | 设置页、诊断、动态目录及任务级用例 | 新发现的普通网站 adapter 无需改 Swarm 执行代码即可使用，能力选择与结果处理可验证 |

S1 可以在 Core 实现前完成独立连接验证；S2 与 Core C1/C2/C3 配合，S3/S4 依赖 Core 状态及调用关联。开发可以分阶段，但正式启用混合网页任务前须完成共享页面协调和不确定结果验证。

本轮建议先评审三项边界：

- **挂载方式**：应用扩展与 Browser Agent PluginSpec 分别管理，由统一 helper 和轻量挂载 rail 衔接。
- **通用接入**：目录与 Skill 由真实生效的 adapters 生成，普通网站走统一执行路径；站点专项兼容和优化记录可以后续补充。
- **并发粒度**：先保证现有会话/成员跨页并发，同页默认独占；认证变更协调共享 profile，纯读放宽以验证为依据。

用户已验证过 Bilibili adapter，可作为后续回归候选。本轮先设计通用版本，使用预配置 fixture adapter 验证发现、执行、状态与接续；不以选定真实网站名单或逐站实现为前置条件。后续按需要增加真实站点回归、兼容修正与性能优化。工作页数量等容量参数在实际负载验证后设置，不作为当前接口的固定常量。

## 12. 依据与待验证事实

| 源码依据 | 本次确认的现状 |
| --- | --- |
| [ApplicationPluginExtension](../../jiuwenswarm/extensions/sdk/application_plugin.py)、[loader.py](../../jiuwenswarm/extensions/loader.py)、[manager.py](../../jiuwenswarm/extensions/manager.py) | 应用扩展的注册/设置服务与 Agent 能力挂载是不同链路；加载器会处理声明依赖 |
| [interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py)、[interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py)、[code_subagents.py](../../jiuwenswarm/agents/swarm/providers/code_subagents.py) | 三处 Browser Agent 配置装配需要统一门控与注入 |
| [Core DeepAgent](../../../../../agent-core/openjiuwen/harness/deep_agent.py) | BEFORE_INVOKE 位于外层，已有 load_plugin_spec 与卸载入口 |
| [browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs)、[target_mcp_wrapper.cjs](../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs) | 已有共享 partition、准确 TargetID 和保活 lease；操作协调与请求关联待补 |
| [OpenCLI main.ts](../../../../../opencli/src/main.ts)、[discovery.ts](../../../../../opencli/src/discovery.ts)、[CLI list](../../../../../opencli/src/cli.ts) | 存在内置/用户/plugin 覆盖顺序和结构化命令发现；索引刷新需考虑实际来源 |
| [OpenCLI execution.ts](../../../../../opencli/src/execution.ts)、[capabilityRouting.ts](../../../../../opencli/src/capabilityRouting.ts) | adapter 的浏览器依赖、预导航和执行路径需要按操作核对 |
| [Core stdio_client.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/client/stdio_client.py)、[playwright_client.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/client/playwright_client.py) | 当前发送路径主要传递工具名称和 arguments，可信租约关联仍需实现 |

本文提出的装配流程、CDP 联通、MCP 元数据传播、并发和真实站点兼容性均未在本轮运行验证。
