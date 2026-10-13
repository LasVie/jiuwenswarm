# OpenCLI 可插拔接入架构方案

> 更新：2026-09-23。状态：架构讨论稿；本文定义目标方案，尚未实现或完成运行验证。
>
> 阅读顺序：本文说明完整链路与职责；[Agent Core 设计](opencli-agent-core-design.md)说明公共接口；[Swarm 设计](opencli-swarm-design.md)细化产品装配、动态 adapter 目录、宿主协议和文件计划；[Electron/CDP 调查](opencli-electron-cdp-research.md)记录源码依据与验证条件。

## 1. 目标与使用方式

JiuwenSwarm 为 Browser Agent 提供一项可选的 OpenCLI 站点 adapter 能力。Browser Agent 先检查已配置 adapters 是否覆盖当前任务步骤，按需读取对应 Skill，通过现有 Bash/PowerShell 执行 adapter 命令。通用网页操作统一使用已有 Playwright 工具。

需要浏览器的 adapter 与 Playwright 连接 Swarm 内置浏览器中的同一个任务页面，复用登录态、页面位置和任务证据。每一步都可以重新选择合适的能力，因此一次任务可以经历 OpenCLI → Playwright → OpenCLI。

首期产品约定如下：

| 项目 | 设计约定 |
| --- | --- |
| 任务范围 | 已配置的 OpenCLI 网站 adapters 及其与 Browser Agent 的协作 |
| 能力选择 | 当前步骤有适用、可运行的 adapter 时优先调用；其余步骤使用 Playwright |
| 执行入口 | Browser Agent 的现有 shell 工具，命令参数由 OpenCLI 校验 |
| 浏览器 | Swarm 内置 Electron 浏览器；配置外部浏览器时使用现有 Browser Agent 路径 |
| 存储与页面 | 同一用户共享持久化 profile；会话、成员及独立交互分支使用各自页面 |
| 上下文 | 能力发现、具体操作说明及执行细节主要留在 Browser Agent 内 |
| 运行包 | 当前使用原作者的固定版本发行物；接入包记录版本和兼容范围，可更换发行来源 |
| 开发环境 | 新仓内的本地 Agent Core 依赖；运行时确认主进程和 agent server 实际导入同一份 Core |

“OpenCLI 优先”在操作粒度上生效。例如，适配器可以直接查询数据时使用命令；用户要求查看页面或截图时，实际完成相应页面步骤。适配器不适用、当前传输不支持或需要补充交互时，Browser Agent 继续使用页面工具。

### 1.1 能力边界

| 能力 | 本方案中的角色 |
| --- | --- |
| 已配置的站点 adapter 命令 | 提供面向具体站点和业务操作的能力，例如搜索、读取详情或已支持的写操作 |
| Playwright 页面工具 | 负责打开页面、观察、查找元素、点击、输入、截图等通用操作，以及 adapter 未覆盖的步骤 |
| adapter 索引与操作 Skill | 帮助 Browser Agent 判断当前步骤能否使用 adapter，并按需获得原 CLI 用法 |
| 运行包定位和诊断 | 为上述 adapter 的执行提供必要环境，属于接入运行时职责 |

首期面向 Agent 的 OpenCLI 能力限定为已配置 adapters 的发现与调用。OpenCLI 的通用 `browser` 命令、现场探索网站和生成新 adapter 的工作流不属于本期能力范围。安装原作者运行包不意味着将其全部命令或 Skill 暴露给 Agent。

这里区分的是 Agent 使用的能力入口。adapter 内部仍可能通过 CDP 导航、执行脚本或操作 DOM，这些动作属于 adapter 的执行过程，仍需遵守共享页面和操作租约。

### 1.2 选择规则

Browser Agent 按“站点 + 当前具体操作”匹配当前启用的 adapter 索引，再确认输入、认证条件和运行兼容性。站点存在 adapter，只代表它提供了一组特定操作。

- 匹配且可运行：读取操作说明，通过 shell 执行 adapter 命令。
- 无对应操作或当前不可运行：直接使用 Playwright 完成该步骤。
- adapter 只覆盖任务的一部分：按步骤组合两种能力，由同一个 Browser Agent 持续负责。
- 写操作结果不明：先核实结果，再选择下一步，避免自动换后端重复提交。

发现优先使用简短索引和按需 Skill；同一任务中复用已确认结果。运行包、adapter 配置或相关认证/宿主状态变化时才更新对应判断，无需在每次点击前重复枚举全部命令。

## 2. 整体结构

~~~mermaid
flowchart TB
    User[用户任务] --> Main[主 Agent]
    Main --> BA[Browser Agent：网页任务负责人]
    Plugin[Swarm 可选 OpenCLI 接入包] --> Skill[渐进式 Skill]
    Skill --> BA
    BA --> Match{当前步骤有适用且可运行的 adapter？}
    Match -->|有| Shell[现有 Bash / PowerShell 工具]
    Match -->|无或需要通用页面操作| PW[Playwright 页面工具]
    Plugin -. 注册调用级绑定与收尾 .-> Shell
    Shell --> CLI[固定版本 OpenCLI 的站点 adapter]
    CLI -->|需要浏览器时| CDP[当前任务页的精确 CDP 连接]
    PW --> MCP[按 TargetID 绑定的 MCP 路径]
    CDP --> Page[任务页面]
    MCP --> Page
    Host[Swarm Electron 浏览器宿主] --> Page
    Host --> Profile[用户持久化 profile]
    Host -. 页面归属与操作协调 .-> Plugin
    Host -. 同一操作协调 .-> MCP
~~~

Browser Agent 负责选择与判断；Core 提供可复用机制；Swarm 接入包将 OpenCLI 与产品浏览器连接起来；Electron 宿主最终拥有页面和存储。

### 2.1 各层职责

| 层次 | 负责的内容 | 主要交付物 |
| --- | --- | --- |
| Agent Core | Skill 挂载与披露；shell 调用级环境和生命周期；浏览器任务公开访问、状态失效和既有证据接入 | 通用接口、默认兼容行为、生命周期测试 |
| Swarm 应用层 | 用户设置、运行条件检查、Browser Agent 装配、会话/成员身份、状态展示、本地 Core 依赖 | 启用策略、装配流程、产品配置 |
| Swarm 可选接入包 | 已配置 adapter 的索引与 Skill、发行物定位、adapter 命令识别、兼容说明、按需 CDP 绑定和结果衔接 | 可装卸的 adapter 能力包及固定版本兼容记录 |
| Electron 浏览器宿主 | 持久化 profile、页面分配和回收、精确 TargetID 解析、页面操作租约、重连 | 两条执行路径共同遵守的宿主契约 |
| OpenCLI 运行包 | CLI 参数校验、站点适配器逻辑、CDP 调用和原始输出 | 选定发行物及其依赖 |

接入包首期可以与 Swarm 同仓发布，其逻辑边界独立。Core 的接口使用 shell 调用、页面绑定和资源生命周期等通用概念；站点名称、OpenCLI 环境变量、Electron 地址发现及产品启用策略由应用侧实现。

## 3. 一次任务的完整链路

### 3.1 装配与发现

1. Swarm 根据当前配置判断可用能力。OpenCLI 已启用且使用内置浏览器时，将接入包挂到实际执行任务的 Browser Agent。
2. 通过现有 PluginSpec / BuildContext / LoadRecord 装配提示、Skill 和运行时接入资源。已有适用 shell 则复用；需要时装配平台对应的现有 shell 工具。
3. Browser Agent 初始只看到简短的 adapter 能力说明。它从已配置 adapter 索引匹配站点和具体操作，匹配后读取相关操作文件；未匹配时沿用 Playwright 执行当前步骤。
4. 运行包准备与浏览器连接在首次需要相应能力时完成。安装状态、用户启用状态和运行就绪状态分别记录。

主 Agent 继续将网页任务委派给 Browser Agent。详细 adapter 目录和操作帮助按任务需要进入子代理上下文，子代理向上返回任务结果、关键证据及需要用户处理的事项。

### 3.2 执行一条 adapter 命令

1. Browser Agent 向 shell 提交真实命令、工作目录和超时等现有参数。
2. 命令经过现有 shell 权限和执行检查。
3. 接入包识别受支持的直接 adapter 命令，核对它属于当前已配置、已启用的操作集合，并确认发行物、认证前提和兼容性。
4. 通过 Core 的浏览器任务访问接口，请 Swarm 宿主解析当前逻辑页面，校验会话/成员归属和页面代次，并取得相应操作租约。
5. 将准确的页面 WebSocket 写入本次子进程的 `OPENCLI_CDP_ENDPOINT`，由原 shell 执行路径启动 CLI。
6. 保留 CLI 输出和现有 shell 展示方式。接入包记录必要进程信息、使相关页面观察过期；有可靠转换规则时提交可验证证据，其余使用原输出和必要页面核实。
7. 完成收尾后释放本次资源；Browser Agent 根据输出和必要页面证据决定下一步。

上述页面绑定步骤用于需要浏览器的 adapter。已确认完全不依赖浏览器的站点 adapter 只准备自身执行环境；本地元数据发现本身不申请页面资源。是否使用浏览器依据实际 adapter 依赖核对，业务上的“查询”本身不足以判断。

绑定和租约在可信运行时流转，模型按 Skill 编写命令即可。每个调用具有独立环境，两个并发调用可以连接不同页面。接入层对明确识别的 OpenCLI 通用 browser 调用返回能力范围说明，引导使用现有 Playwright 工具。

首期的受管调用采用可确认的直接命令形式，优先一条 shell 调用执行一条 CLI 命令。复杂别名或嵌套脚本需要浏览器绑定时，应明确拆成受支持的形式。普通 shell 命令继续沿用自己的执行流程。

### 3.3 与页面工具接续

Browser Agent 选择 Playwright 时，使用同一任务页面和同一宿主协调机制。OpenCLI 可能改变页面后，Core 使旧页面观察及元素引用失效；下一次观察获取新状态，真正执行元素动作前还要校验引用有效性。

Playwright 完成登录、筛选或其他操作后，Browser Agent 可以再次选择适用的 OpenCLI 命令。每次重新解析当前绑定，因此页面重建或宿主重启后能够获得新连接。

例如：读取某站点 Skill → OpenCLI 发现认证失效 → 在内置页面完成登录 → OpenCLI 查询 → Playwright 打开结果并截图 → OpenCLI 执行后续适用查询。

## 4. 浏览器身份、存储与所有权

### 4.1 共享关系

| 对象 | 共享范围 | 所有者 |
| --- | --- | --- |
| 持久化 profile / Electron partition | 同一用户的会话与成员 | Electron 宿主 |
| cookies、同源 localStorage | 同一 profile 内按浏览器规则共享 | 浏览器 |
| 页面与导航状态 | 单个会话/成员/交互分支 | Electron 宿主 |
| sessionStorage、页面脚本状态 | 遵循各页面自身语义 | 浏览器页面 |
| 当前页面绑定 | 同一交互分支内的 OpenCLI 与 Playwright | 宿主解析，Core 暴露任务访问入口 |
| CLI 进程与连接 | 单次调用 | shell 执行路径与接入包 |

当前内置浏览器使用 `persist:jiuwenswarm-browser` partition。接入设计沿用共享存储、独立页面的模式。同一用户的账号切换会影响使用同一站点存储的其他页面；产品需要把它作为共享状态变化处理。

共享 profile 由运行中的 Electron 持有。两类执行器连接这个宿主已经创建的页面，页面生命周期由宿主统一管理。

### 4.2 页面绑定

绑定应包含逻辑浏览器/页面标识、会话和成员归属、存储身份、宿主代次、页面代次，以及仅供可信执行端使用的准确连接信息。

- 宿主代次随 Electron 重启变化；页面代次随页面重建变化。
- 页面状态版本用于表示当前观察是否过期，与页面代次、现有元素引用版本分别维护。
- 旧 checkpoint 保存逻辑身份；恢复后根据当前配置重新取得运行时绑定。
- 页面消失或归属校验失败时，返回明确状态，由任务重新解析或申请页面。

独立并发分支可以由宿主分配同 partition 的工作页，并保留 branch/page/call 关系。每个分支的两种执行器仍使用同一页面。具体分配上限及页面展示方式在 Swarm 设计中确定。

### 4.3 CDP 接入选择

首选候选路径是向 OpenCLI 提供准确的页面 WebSocket。当前研究版本的普通站点运行链路可以通过 `OPENCLI_CDP_ENDPOINT` 选择 CDPBridge，页面 WebSocket 可跳过 HTTP endpoint 的启发式目标选择。

此能力仍需端到端验证。先验证通用发现、执行和页面接续；adapter 涉及多页、上传下载或网络捕获时，再按真实依赖验证对应接口。通用网页能力的任务测试继续使用 Playwright。详细依据和限制见 [CDP 调查](opencli-electron-cdp-research.md)。

## 5. 可插拔与渐进式上下文

### 5.1 能力生命周期

| 状态 | 产品行为 |
| --- | --- |
| 已安装、未启用 | 保存包信息，Browser Agent 按其原有能力运行 |
| 已启用、待使用 | 挂载短说明和 Skill 入口；按需准备运行包与连接 |
| 可运行 | 提供满足通用运行条件的网站操作，独立标注站点验证状态，由任务按需执行 |
| 暂不可用 | 记录具体原因，Browser Agent 使用适用的页面工具；相关状态变化后可重新评估 |
| 禁用中 | 拒绝新受管调用，处理在途命令并收尾，撤销本包资源 |
| 已禁用 | 后续装配、缓存子代理复用和会话恢复均按当前配置工作 |

每项提示、Skill、执行挂钩及按需提供的 shell 都记录资源归属。卸载释放本包贡献；共享资源在最后一个使用者退出时释放，宿主原有资源按原生命周期保留。

禁用后的上下文目标是：后续系统提示、工具能力、Skill 列表及自动探测均反映当前配置。已经发生的对话和执行结果作为历史保留；精简目标针对后续主动注入的内容。

### 5.2 Skill 组织

采用“adapter 能力元信息 → 已配置站点/操作索引 → 操作说明”的披露顺序，也允许直接读取已经确定的操作文件。索引由实际生效的 adapter 和启用配置确定，排除已知不兼容项；Skill 内容限定为这些 adapters 的用法。普通网站无需逐站实现或先进入验证白名单，未知页面行为采用保守执行条件。

操作说明包括实际 CLI 命令、参数示例、已知前提、结果语义及接续建议。说明优先由上游元数据、help 和已有文档生成，专项兼容和验证记录按需补充；没有可靠语义说明时保留原输出并核实，避免凭退出码判断业务完成。

Core 为 Skill 挂载提供 `directory_view=full|none`，默认沿用完整展示。OpenCLI 挂载选择 `none`，按文档内的明确链接发现内容。目录、可见技能列表和缓存都以挂载项为单位管理。

## 6. 并发、页面状态与任务结果

### 6.1 操作协调

| 操作场景 | 协调规则 |
| --- | --- |
| 不同页面上的独立命令 | 可以并发，每次调用使用自己的页面绑定和环境 |
| 同页已验证的纯读取 | 可以共享读租约；要求全过程无导航、页面状态或网络配置变更 |
| 同页导航、交互及行为未知的命令 | 页面独占租约覆盖完整操作 |
| 登录、退出、账号切换及共享存储变更 | 协调相关 profile/origin，并使受影响页面的观察与认证状态过期 |
| 不同页面修改同一业务对象 | 按业务操作语义协调与核实，页面隔离本身不足以解决业务冲突 |

OpenCLI 适配器内部已有的请求并发保持有效，外层租约覆盖整条 CLI 命令。页面保活租约负责避免回收，操作租约负责执行冲突，两者职责分别定义。

Playwright 工具、内部观察、恢复操作及 MCP wrapper 都须遵守同一协调机制。复合操作传递同一次调用/租约关联，保证整体执行并避免嵌套重复加锁；当前 Core 的 MCP 客户端尚需补可信请求元数据透传。首期 CLI 采用前台或流式执行，跨页并发由多个正常工具调用实现。具体协议见 [Swarm 设计第 7 节](opencli-swarm-design.md#7-electron-页面与协调协议)。

### 6.2 状态和证据

CLI 输出沿用 shell 的结果、截断及文件引用能力。Browser Agent 阅读这些输出；接入包只将有可靠解释规则的事实接入浏览器已有证据结构，并记录来源、页面与调用关系。

进程成功退出、网站业务完成、证据满足任务要求分别判断。空查询可以是正常结果；用户要求的截图或页面核对是任务的一部分。页面可能变化时，收尾阶段在释放冲突操作租约前发出失效通知。

### 6.3 故障后的下一步

| 情况 | 下一步 |
| --- | --- |
| 命令/传输不支持当前操作 | 使用合适的 Playwright 步骤；后续适用操作仍可使用 OpenCLI |
| 认证失效 | 完成登录并刷新相关状态，然后重新评估操作 |
| CLI 参数或运行包错误 | 修正可确定的问题，再按权限和操作语义执行 |
| 查询成功但结果为空 | 按查询语义解释，必要时调整查询条件 |
| 已启动的写操作超时、断连或被取消 | 标记结果待核实，先检查业务状态再决定是否继续 |
| 页面或宿主重建 | 获取新绑定，重新观察当前页面后接续 |

shell 保持非幂等默认声明。租约到期或进程退出不能证明页面中发出的请求已经终止；未决写入需要保留核实状态，避免两条执行路径重复提交。

## 7. 运行包与部署边界

接入包记录发行来源、版本、安装入口、实际生效的 adapter 来源及已知限制。Skill、命令识别和兼容说明跟随这个基线更新。子进程使用受管安装位置和调用局部环境，诊断能够核对实际执行的版本。

上游存在内置、用户 adapter 和用户插件的覆盖关系，运行包版本本身不足以确定操作来源。来源变化时重建索引并使旧优化记录失效，普通 adapter 再按通用条件判断；具体流程见 [Swarm 运行包设计](opencli-swarm-design.md#53-发行物和实际来源)。

源码研究基线为新仓 `opencli/` 中的 `LasVie/OpenCLI:main` 固定提交，版本 1.8.8；原作者对应发行物尚未安装和验证。实现时先选定可获取的具体发行物，再执行兼容验证，版本号相同本身不足以证明入口和行为一致。

首期浏览器宿主与 CLI 执行位于本机。未来远端成员应通过浏览器所在设备的执行服务使用能力，连接地址的有效性和页面归属都在宿主设备上解析。

Core 的 shell 执行作用域独立于浏览器；未来桌面或其他 CLI 能力可以提供自己的环境与生命周期逻辑，按需组合浏览器接口。

## 8. 实施阶段与验收

本轮产出设计，以下为评审通过后的实施顺序。具体 Core 工作项见 [Core 设计第 8 节](opencli-agent-core-design.md#8-实施工作项与验收)。

| 阶段 | 主要工作 | 进入下一阶段的条件 |
| --- | --- | --- |
| A：连接验证与开发基线 | 配置本地 Core；固定原作者运行包；隔离 profile、本地 fixture 上验证实际 CLI → 精确 Electron 页面 | 多页面不串页；两种执行器能双向接续；释放连接后宿主仍存活 |
| B：Core 公共能力 | 完成 Skill 挂载、shell 执行作用域、浏览器公开访问和页面失效/证据入口 | 普通/流式/取消与卸载测试通过；默认行为兼容 |
| C：Swarm 集成 | 统一启用判断、Browser Agent 装配、宿主操作协调、运行包定位和诊断 | 跨页并发、同页互斥、禁用/恢复、外部浏览器路径符合约定 |
| D：通用 adapter 链路 | 动态索引、生成式 Skill 视图、通用输出、按需兼容补充与 fixture 任务 | 新网站无需修改 Swarm 执行代码，命中/未命中、部分覆盖、双向接续和未决写入处理正确 |
| E：产品评估 | 对相同任务比较 Browser-only 与混合路径 | 成功率、完成质量、耗时、模型轮次和上下文成本具有可解释结果 |

连接验证与接口评审可以并行推进；涉及上游能力的接口承诺在验证后定稿。首批测试应覆盖准确页面、共享存储、跨页并发、同页冲突、状态失效、进程取消和宿主重建。

### 8.1 产品选择与建议

| 选择 | 当前建议 | 影响范围 |
| --- | --- | --- |
| 默认启用方式 | 开发和首批验证期间显式启用 | 安装与设置界面、能力装配 |
| 站点策略 | 通用链路先行，逐站适配后续补充；Bilibili 作为用户已有验证的回归候选 | 动态 Skill、通用验收和后续兼容修正 |
| 工作页策略 | 限量分配，按独立交互分支关联页面 | Electron 宿主、并发上限、页面展示 |

配置与页面策略的具体提案见 [Swarm 设计](opencli-swarm-design.md)。Core 公共接口按能力可选、调用局部和资源归属明确的原则推进。

### 8.2 文件清单的阅读方式

以下路径相对新仓根目录。“修改”对应已经存在的文件，“新增”是计划中的文件，实施时才创建。下表为概览，Swarm 的具体模块职责、宿主协议及完整文件计划见 [Swarm 设计第 9 节](opencli-swarm-design.md#9-文件清单)。

Core 的功能、测试与规约文件逐项列在 [Core 设计第 7 节](opencli-agent-core-design.md#71-功能文件清单)，并与 C1—C5 工作项对应。下面列出 Swarm 与接入包的文件责任。

### 8.3 Swarm 与接入包文件

**可选 OpenCLI 接入包：阶段 C、D**

建议将接入包放在 `jiuwenswarm/extensions/opencli/`，通过现有应用扩展机制承载产品生命周期，向实际 Browser Agent 提供 Core PluginSpec。应用扩展与 Agent 能力挂载分别按各自生命周期管理。

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 新增 | `jiuwenswarm/extensions/opencli/__init__.py`、`extension.yaml`、`extension.py`（同目录） | 定义包身份、入口及产品生命周期；接入启用/禁用和诊断服务，发布本包的装配入口。 |
| 新增 | `jiuwenswarm/extensions/opencli/settings.py` | 统一读取启用状态、运行包配置和内置浏览器条件；返回可运行或不可用的明确原因，供各 Agent 模式共用。 |
| 新增 | `jiuwenswarm/extensions/opencli/harness.py` | 构造 Browser Agent 使用的 PluginSpec 与运行时上下文，组合提示、Skill、接入 rail 和按需复用/提供的 shell；管理挂载记录。 |
| 新增 | `jiuwenswarm/extensions/opencli/rail.py` | 在 Agent 上登记 shell 执行作用域工厂；完成每次受管调用的准入、页面绑定、局部 environment、结果观察和收尾，处理卸载中的在途命令。 |
| 新增 | `jiuwenswarm/extensions/opencli/runtime.py` | 定位和核对受管 CLI 发行物、可执行入口与版本，生成调用局部运行环境，提供就绪诊断。实际进程由 Core 的现有 shell 启动。 |
| 新增 | `jiuwenswarm/extensions/opencli/commands.py` | 读取当前已配置 adapter 元数据，提供站点/操作索引并识别直接 adapter 命令；结合兼容记录判断浏览器依赖、准入与租约，对通用 browser 调用给出 Playwright 路由说明。 |
| 新增 | `jiuwenswarm/extensions/opencli/compatibility.yaml` | 固定发行物、通用约束及可选分类/兼容补充，记录已知限制和经验证的优化；普通 adapter 不依赖逐站准入白名单。 |
| 按需新增 | `jiuwenswarm/extensions/opencli/evidence.py` | 有可靠输出契约时补证据转换；普通 adapter 沿用 shell 原输出与必要页面核实。 |
| 新增 | `jiuwenswarm/extensions/opencli/skills/opencli/SKILL.md` | 简短 adapter 能力说明、已配置站点/操作索引和选择约定；未命中时指向 Playwright，作为按需读取入口。 |
| 运行时生成 | `runtime_state/opencli/skills/<catalog_revision>/sites/<site>/index.md`、站点内 `operations/<operation>.md`（用户数据目录） | 根据上游元数据和帮助生成当前有效操作视图；站点专项内容按需补充。 |

上述文件按职责拆分，内容较少的模块可在实现评审时合并；运行时与 Skill 的可见性边界保持一致。

**浏览器宿主与 Python 接入：阶段 A、C**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [jiuwenswarm/channels/desktop/electron/browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs) | 扩展现有页面 resolver，明确逻辑页面、profile、host/page 代次和精确 TargetID；接入工作页分配、操作租约和共享状态通知。 |
| 新增 | `jiuwenswarm/channels/desktop/electron/browser_operation_leases.cjs` | 实现宿主侧 shared-read/exclusive 协调、调用归属、复合操作关联及未决状态管理；与页面保活机制配合。 |
| 修改 | [jiuwenswarm/channels/desktop/electron/main.cjs](../../jiuwenswarm/channels/desktop/electron/main.cjs) | 在宿主启动、页面创建/销毁及关闭时装配和清理协调服务，提供解析与租约访问入口。 |
| 修改 | [jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs](../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs) | 将准确 TargetID 绑定与操作租约结合；校验并透传调用关联，让 Playwright 与 CLI 遵守同一页面协调。 |
| 修改 | [jiuwenswarm/agents/harness/common/electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py) | 沿用发现、会话/成员绑定和保活逻辑，补完整页面身份、代次与新宿主接口信息。 |
| 新增 | `jiuwenswarm/agents/harness/common/electron_browser_coordinator.py` | 实现 Core coordinator 协议的 Python 客户端；解析页面、申请/释放租约、处理重连及失效通知，供两条执行路径共用。 |

**Agent 装配、配置与开发依赖：阶段 A、C**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [jiuwenswarm/server/runtime/agent_adapter/interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py) | 在单 Agent 的 Browser Agent 创建、缓存复用与配置更新流程中应用统一启用判断，注入 coordinator 并装卸接入包。 |
| 修改 | [jiuwenswarm/server/runtime/agent_adapter/interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py) | 在 Code 模式 Browser Agent 配置中应用相同装配逻辑，使 OpenCLI 能力归属于执行网页任务的子代理。 |
| 修改 | [jiuwenswarm/agents/harness/code/spec.py](../../jiuwenswarm/agents/harness/code/spec.py) | 通过 CodeBuildContext 传递所需可信句柄和当前配置，供子代理装配使用，保持活句柄的运行时属性。 |
| 修改 | [jiuwenswarm/agents/swarm/providers/code_subagents.py](../../jiuwenswarm/agents/swarm/providers/code_subagents.py) | 在 Swarm Browser Agent provider 中按 session/member 构造任务上下文，调用统一接入包装配入口。 |
| 修改 | [jiuwenswarm/agents/swarm/browser_runtime.py](../../jiuwenswarm/agents/swarm/browser_runtime.py) | 统一内置/外部浏览器选择与接入条件，将宿主 coordinator 贯通到 RuntimeSettings。 |
| 修改 | [jiuwenswarm/agents/swarm/context.py](../../jiuwenswarm/agents/swarm/context.py)、[jiuwenswarm/agents/swarm/registry.py](../../jiuwenswarm/agents/swarm/registry.py) | 补运行时句柄、逻辑身份及 seed 重建衔接；恢复时重新读取启用状态和宿主绑定。 |
| 修改 | [jiuwenswarm/resources/config.yaml](../../jiuwenswarm/resources/config.yaml) | 增加 OpenCLI 配置示例、开发期显式启用的默认约定及运行包配置说明。 |
| 修改 | [pyproject.toml](../../pyproject.toml)、[uv.lock](../../uv.lock) | 配置本地 Core 的开发依赖并同步解析结果；检查接入包声明、Skill 和兼容文件能随产品打包。锁文件由依赖工具生成。 |
| 新增 | `docs/development/opencli-local-setup.md` | 记录本地 Core 导入检查、固定 CLI 发行物、内置浏览器启动和诊断步骤，覆盖主进程与 agent server。 |

**设置与状态展示：阶段 C，随 Swarm 交互设计确认**

当前建议在现有浏览器设置中提供 OpenCLI 开关和可用状态。以下是采用该入口时的文件范围：

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition.ts) | 定义 OpenCLI 设置项和当前运行条件的展示入口。 |
| 修改 | [jiuwenswarm/channels/web/frontend/src/features/settings/services/settingsContract.ts](../../jiuwenswarm/channels/web/frontend/src/features/settings/services/settingsContract.ts)、[SettingsSourceProvider.tsx](../../jiuwenswarm/channels/web/frontend/src/features/settings/services/SettingsSourceProvider.tsx) | 贯通字段、加载/保存和状态返回；配置外部浏览器时说明当前可用范围。 |
| 修改 | [jiuwenswarm/server/runtime/gateway_adapter/config_adapter.py](../../jiuwenswarm/server/runtime/gateway_adapter/config_adapter.py)、[jiuwenswarm/gateway/channel_manager/web/app_web_handlers.py](../../jiuwenswarm/gateway/channel_manager/web/app_web_handlers.py) | 让设置读写与能力就绪状态进入现有配置链路；具体 OpenCLI 规则调用接入包 settings，变更后触发 Agent 能力重新核对。 |
| 修改 | [jiuwenswarm/common/config.py](../../jiuwenswarm/common/config.py) | 贯通配置持久化和更新，保证读取、保存及重新装配使用一致值。 |
| 修改 | [jiuwenswarm/channels/web/frontend/src/i18n/locales/zh.json](../../jiuwenswarm/channels/web/frontend/src/i18n/locales/zh.json)、[en.json](../../jiuwenswarm/channels/web/frontend/src/i18n/locales/en.json) | 补设置、未启用、待准备、运行包错误和外部浏览器条件等用户文案。 |

### 8.4 Swarm 与端到端验证文件

| 类型 | 文件 | 覆盖说明 |
| --- | --- | --- |
| 新增 | `jiuwenswarm/extensions/opencli/tests/test_harness.py` | PluginSpec 装配、启用/禁用、资源归属、共享 shell 和恢复后的当前配置。 |
| 新增 | `jiuwenswarm/extensions/opencli/tests/test_commands.py`、`test_runtime.py`（同目录） | adapter 索引与直接命令识别、通用 browser 范围检查、兼容判断、固定发行物、路径含空格和调用局部环境；覆盖执行路径问题。 |
| 新增 | `jiuwenswarm/extensions/opencli/tests/test_rail.py`；有证据转换时补同目录 `test_evidence.py` | 精确页面绑定、取消收尾、输出保留、证据接入和未决写入处理。 |
| 修改 | [tests/electron/browser_panels.test.cjs](../../tests/electron/browser_panels.test.cjs) | 页面归属、代次、共享 partition、工作页及回收与操作租约的配合。 |
| 新增 | `tests/electron/browser_operation_leases.test.cjs` | 跨页并发、同页读共享/冲突互斥、复合操作关联、过期和未决状态。 |
| 修改 | [tests/unit/harness_common/test_electron_sideview.py](../../tests/unit/harness_common/test_electron_sideview.py)、[tests/unit/test_electron_browser_target.py](../../tests/unit/test_electron_browser_target.py) | resolver 与 wrapper 的精确目标、重连和错误归属行为。 |
| 新增 | `tests/unit/harness_common/test_electron_browser_coordinator.py` | Python 客户端的租约协议、取消、失效通知与宿主重建。 |
| 修改 | [tests/agents/swarm/test_electron_browser_fallback.py](../../tests/agents/swarm/test_electron_browser_fallback.py)、[tests/unit/deep_agent/test_browser_subagent_integration.py](../../tests/unit/deep_agent/test_browser_subagent_integration.py) | 各模式挂载、adapter 命中/未命中和部分覆盖的装配与路由条件、外部浏览器条件及缓存更新；实际 Agent 选择另以任务级验证核对。 |
| 新增 | `tests/electron/opencli_integration.cjs` | 使用隔离 profile 和本地 fixture，验证真实 CLI 管线、两个页面共享存储、双向接续、并发与释放后宿主存活；复用 [browser_fixture.cjs](../../tests/electron/browser_fixture.cjs) 的测试宿主基础，按需要扩展 fixture。 |
| 修改 | [jiuwenswarm/channels/web/frontend/tests/settingsRefactor.test.mjs](../../jiuwenswarm/channels/web/frontend/tests/settingsRefactor.test.mjs) | 若采用现有浏览器设置入口，覆盖字段读写和条件展示。 |
| 修改 | [jiuwenswarm/channels/desktop/electron/README.md](../../jiuwenswarm/channels/desktop/electron/README.md) | 实现后同步页面解析、操作租约、连接归属和本地验证说明。 |

运行包源码 `opencli/` 用于基线核对和验证依据。首期集成针对选定的原作者发行物；若验证暴露上游兼容问题，再依据问题记录决定发行版本或后续自维护包的处理范围。

## 9. 源码依据

以下为设计核对过的当前实现；目标行为与现有实现的差异在 Core 设计中逐项标明。

| 主题 | 主要文件 |
| --- | --- |
| Core 扩展装配 | [extension_spec.py](../../../../../agent-core/openjiuwen/harness/schema/extension_spec.py)、[extension_binder.py](../../../../../agent-core/openjiuwen/harness/extension_binder.py) |
| Shell 执行 | [BashTool](../../../../../agent-core/openjiuwen/harness/tools/shell/bash/_tool.py)、[PowerShellTool](../../../../../agent-core/openjiuwen/harness/tools/shell/powershell/_tool.py)、[BaseShellOperation](../../../../../agent-core/openjiuwen/core/sys_operation/shell.py) |
| Browser Agent 与状态 | [browser_agent.py](../../../../../agent-core/openjiuwen/harness/subagents/browser_agent.py)、[runtime.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py)、[状态处理器](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py) |
| Skill 披露 | [skill_tool.py](../../../../../agent-core/openjiuwen/harness/tools/skills/skill_tool.py)、[skill_use_rail.py](../../../../../agent-core/openjiuwen/harness/rails/skills/skill_use_rail.py) |
| 应用装配 | [interface_deep.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_deep.py)、[interface_code.py](../../jiuwenswarm/server/runtime/agent_adapter/interface_code.py)、[browser_runtime.py](../../jiuwenswarm/agents/swarm/browser_runtime.py) |
| 内置浏览器 | [electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py)、[browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs)、[target_mcp_wrapper.cjs](../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs) |
| OpenCLI 传输 | [runtime.ts](../../../../../opencli/src/runtime.ts)、[cdp.ts](../../../../../opencli/src/browser/cdp.ts)、[绑定调查](opencli-electron-cdp-research.md) |
