# OpenCLI 接入的 Agent Core 设计

> 更新：2026-09-23。状态：接口与实施讨论稿，尚未实现。
>
> 本文承接[总体架构](opencli-integration-architecture.md)，应用装配与宿主协议见 [Swarm 设计](opencli-swarm-design.md)。带有“拟新增”的名称用于接口评审；现有入口和源码依据单独标注。

## 1. Core 提供什么能力

执行链路为：**Browser Agent → 匹配已配置站点 adapter → 按需读取操作 Skill → 现有 Bash/PowerShell → adapter**。需要浏览器的 adapter 连接当前任务页面；通用网页操作由同一个 Browser Agent 的 Playwright 工具执行。

本设计接入 OpenCLI 已配置的站点 adapters。应用侧按“站点 + 当前操作”判断覆盖范围和运行条件；无适用 adapter 时使用 Playwright，部分覆盖时按步骤组合。Core 提供装配和执行协作机制，adapter 索引与能力选择规则由 Swarm 接入包负责。

Core 提供三个可以组合使用的能力：

| 能力 | 对应用提供的价值 | 主要位置 |
| --- | --- | --- |
| Skill 按挂载项管理与披露 | 控制能力何时进入上下文，并能准确撤销 | SkillSpec、resolver/binder、SkillUseRail、SkillTool |
| Shell 调用级执行作用域 | 在原命令执行前取得环境和资源，在所有结束路径可靠收尾 | BashTool、PowerShellTool、现有 SysOperation |
| 浏览器任务公开访问 | 两种执行路径共享绑定、操作协调、页面状态和任务证据 | Browser Agent 工厂、Browser runtime、上下文处理器 |

应用侧决定 OpenCLI 的启用、发行物、命令兼容性及站点策略。Electron 宿主实现页面归属和跨执行器操作协调。Core 使用通用接口连接这些能力。

未来桌面或其他 CLI 接入也可以使用 Skill 和 shell 执行作用域；需要浏览器页面时，再组合浏览器任务接口。

## 2. 装配方式与资源归属

### 2.1 装配流程

1. Swarm 按当前设置构造 Browser Agent 的配置和 BuildContext，注入当前会话/成员的可信运行时句柄。
2. Browser Agent 沿用现有工厂装配 runtime、页面工具和上下文处理器，同时登记本节后文定义的浏览器任务访问入口。
3. Swarm 向这个 Browser Agent 加载 OpenCLI PluginSpec。能力包包含简短路由提示、Skill 声明、接入 rail，以及按实际需要提供的现有 shell 工具。
4. 接入 rail 在注册阶段取得浏览器任务入口，并向 shell 登记可撤销的执行作用域工厂。相关资源在首次模型调用前就绪。
5. LoadRecord 记录能力包资源；接入 rail 持有其 shell 登记句柄，卸载时负责撤销和完成在途调用收尾。

已有适用 shell 时复用其配置与权限；需要新增时选用平台对应的 BashTool 或 PowerShellTool。SkillUseRail 的现有 `include_tools` 按装配情况配置，保证工具由明确的提供者负责。

PluginSpec 的加载目标是当前 Agent。Swarm 在 Browser Agent 的创建、缓存复用和恢复入口显式应用能力配置。

### 2.2 配置与运行时数据

| 数据 | 承载方式 | 生命周期 |
| --- | --- | --- |
| Skill 路径、展示策略、rail/tool 的声明参数 | 现有 Spec / Config | 可序列化配置 |
| 当前会话/成员身份及重建依据 | 现有 BuildContext seed 与应用配置 | 随会话恢复重新核对 |
| 宿主协调客户端、执行作用域工厂 | 类型明确的 BuildContext 扩展与运行时装配 | 当前 Agent 实例 |
| shell 登记句柄、Skill 挂载记录 | 插件资源账本及所属 rail | 当前挂载 |
| 页面绑定、租约、进程结果 | 单次调用的局部对象 | 调用开始至完成收尾 |

新增配置沿用 Config / Spec 装配；公开符号由对应子包 `__init__.py` 导出。活连接、endpoint 和在途租约只保存在运行时；跨进程或 checkpoint 恢复时，按 seed 和当前配置重建客户端并重新解析页面。

### 2.3 禁用、卸载和恢复

卸载按以下顺序完成：

1. 将本挂载标为停止接收新调用，并使准备中的调用在启动进程前重新检查状态。
2. 按任务取消策略等待或取消在途执行，完成页面失效、未决结果记录及租约收尾。
3. 撤销 shell 执行作用域登记、提示、Skill 挂载和相关缓存。
4. 释放本包独占的工具与资源；共享资源按使用者归属计数释放。

历史消息与执行结果保留。后续提示和能力列表反映当前配置；缓存 Browser Agent 和恢复会话也执行同一核对。当前会话授权继续通过现有权限机制生效。

## 3. Skill 挂载与渐进披露

### 3.1 面向 Browser Agent 的阅读流程

| 层级 | 提供的信息 | 进入上下文的时机 |
| --- | --- | --- |
| 能力元信息 | 站点 adapter 的用途和发现入口 | 能力启用后 |
| 根 Skill | 已配置 adapter 索引及 Playwright 接续约定 | 首次需要定位能力时 |
| 站点索引 | 当前站点 adapters 覆盖的具体操作及前提 | 确认站点后 |
| 操作文件 | 原 CLI 用法、结果语义、兼容性、页面接续建议 | 准备执行该操作时 |

沿用 SkillTool 的相对文件读取能力。已知操作文件可以直接读取，避免为查一个操作反复展开完整目录。OpenCLI Skill 内容限定为当前启用的站点 adapters；通用 browser 命令和 adapter 生成流程不进入本能力的模型说明。相同任务复用已确认的覆盖判断，在配置、版本或相关运行状态变化时更新。

### 3.2 挂载配置

| 字段 | 状态 | 行为 |
| --- | --- | --- |
| `dir` | 已有 | 解析后的准确技能目录 |
| `mode` | 已有，需贯通按挂载项生效 | `all` 提供技能名称/描述；`auto_list` 提供按需发现入口 |
| `enabled_skills` | 已有，需贯通按挂载项生效 | 限定本次挂载可见技能 |
| `directory_view` | 拟新增，默认 `full` | `full` 沿用目录附加输出；`none` 按请求返回文件内容，跳过附加目录扫描和嵌套技能名 |

OpenCLI 使用简短的技能名称/描述，并设置 `directory_view=none`。这里的 `mode=all` 表示技能元信息展示，完整正文仍由读取动作获得。

resolver、binder、rail 和 SkillTool 共同携带同一份挂载配置。挂载记录至少关联 owner、准确目录、可见技能、mode 和 directory_view；叶技能的可见范围以叶目录为准。

### 3.3 共享与撤销

一个 Agent 可以同时挂载多组 Skill。每组配置只作用于自己的目录；提示和列表由当前有效挂载合成。同一物理 Skill 被多个挂载使用时，按访问所属挂载应用策略并保留各自归属。

卸载移除该挂载的提示附件、目录索引和缓存，使后续调用读取当前可见视图。宿主原有 Skill 与其他挂载继续工作。

## 4. Shell 调用级执行作用域

### 4.1 对外接口形态

模型继续调用现有 shell 参数，例如 command、cwd、timeout。作用域是可信运行时扩展，围绕原 shell 的进程执行阶段工作。

拟新增的最小公开访问面如下，命名可在实现评审时校准：

| 入口 | 输入与输出 | 职责 |
| --- | --- | --- |
| `bind_execution_scope(owner_id, factory)` | 向现有 shell 工具登记工厂，返回可撤销句柄 | 支持装配时接入与热卸载，保留原工具配置 |
| `factory(invocation)` | 接收当前调用信息；返回异步作用域或无匹配 | 由应用判断本次命令是否需要接入 |
| 作用域进入 | 返回本次执行的 environment | 准备绑定、租约及其他调用资源 |
| `observe_process_result(result)` | 读取原有底层执行结果 | 收集原始进程信息，并进行应用侧结果处理 |
| 作用域退出 | 接收异常/取消状态，执行最终收尾 | 记录页面变化、释放资源 |

`invocation` 包含实际待执行命令、cwd、shell 类型、tool call ID、可信 Agent/会话关联、执行方式和剩余期限。标识来自运行时调用上下文；页面身份由应用据此解析。

登记归属隔离到 Agent 的 shell 实例。首期每次命令最多由一个接入作用域接管，多个工厂同时命中时明确报告配置冲突。未匹配的调用走原 shell 路径。

### 4.2 执行顺序

~~~mermaid
sequenceDiagram
    participant A as Browser Agent
    participant S as 现有 Shell 工具
    participant I as 接入作用域
    participant H as 浏览器宿主
    participant P as SysOperation / CLI
    A->>S: command、cwd、timeout
    S->>S: 权限与执行检查
    S->>I: 匹配并进入本次作用域
    I->>H: 解析绑定、取得租约、校验代次
    H-->>I: 当前页面绑定与租约
    I-->>S: 调用局部 environment
    S->>P: 原命令 + environment
    P-->>S: 原进程输出/退出状态
    S->>I: observe_process_result
    I->>H: 页面变化与必要状态记录
    S->>I: finally 收尾
    I->>H: 释放本次租约
    S-->>A: 原 Shell ToolOutput
~~~

当前 BaseShellOperation 的普通、流式和后台方法均已有 environment 参数。Core 的工作是在工具层贯通调用局部环境，并使资源生命周期覆盖真实执行过程。

执行作用域位于现有权限和工具检查之后。准备阶段使用同一个调用期限，取得租约后再次检查有效绑定和启用状态，再启动进程。准备失败时在本次工具结果中返回明确原因。

命令经权限检查后保持其执行含义；将来若引入命令改写，实际执行命令须重新经过相同检查。接入环境及受管发行物同样纳入可信配置管理。

### 4.3 OpenCLI 接入包如何使用它

接入包识别可确认的直接站点 adapter 命令，并核对当前配置、操作覆盖和兼容性。需要浏览器时，通过 BrowserTaskAccess 取得页面绑定并提供本次子进程的 `OPENCLI_CDP_ENDPOINT`；已确认无需浏览器的 adapter 只准备其执行环境。固定实际发行物来源适用于两种情况。

本地 adapter 元数据发现按需执行，通常无需页面资源。对明确识别的 OpenCLI 通用 browser 命令，接入层说明本能力的适用范围并指向 Playwright；具体识别规则属于应用包，Core 的 shell 作用域保持通用。

命令识别基于所选 shell 的语法和实际可执行入口。Skill 推荐直接命令形式。无法可靠解析的浏览器调用返回可操作的说明，引导拆成受支持形式；受管浏览器绑定以明确识别为前提。

Core 负责调用生命周期，OpenCLI 专有判断留在应用。环境按调用传给现有 SysOperation，进程全局环境保持独立。准确 endpoint 提供运行路由保证；可运行任意脚本的 shell 本身仍遵循其原有权限边界。

### 4.4 普通、流式、取消及异常

| 路径 | 规定行为 |
| --- | --- |
| 准备失败 | 清理已取得的局部资源，返回准备错误；进程尚未启动 |
| 正常结束 | 读取既有结果，完成状态通知和证据处理，释放租约 |
| CLI 非零退出 | 保留原错误输出；按实际或可能的页面变化发出失效通知 |
| 流式执行 | 作用域覆盖整个流；消费结束、主动关闭及异常都进入收尾 |
| 超时或取消 | 通过现有进程取消机制终止/收尾，记录可能未决的页面或业务影响 |
| 观察结果或清理失败 | 保留原执行结果及独立诊断，标记待核实状态；本次进程保持已执行事实 |
| Agent 卸载/关闭 | 禁止新调用取得该挂载的资源，按相同规则处理在途调用 |

所有调用状态保存在各自作用域中。收尾有独立、有限的清理期限，并处理任务取消期间的资源释放；不能只依赖 AFTER_TOOL_CALL 回调完成清理。

首期受管 OpenCLI 使用前台或流式执行，独立页面通过多个正常工具调用并发。后台进程需要租约随真实进程完成而释放，留作后续能力；首期识别到后台或脱离执行形式时，在启动前说明支持的调用方式。

### 4.5 权限、输出与重试

真实 shell 命令继续经过现有权限链、路径约束和执行模式。读取 Skill 提供使用知识，命令执行仍依据当前会话授权。

保留当前 shell ToolOutput、内容截断、错误展示及持久化方式。可信作用域在输出渲染前可读取底层结果中的 stdout/stderr、退出信息；模型看到的内容仍由原 shell 渲染。

shell 保持非幂等默认声明，通用重试 rail 按现有约束工作。命令结束后的诊断或清理错误不能触发整条命令自动重跑；Browser Agent 依据业务状态和已有证据决定后续动作。

## 5. 浏览器任务公开访问

### 5.1 入口与装配

拟新增 `BrowserTaskAccess`，作为 Browser runtime 面向可信应用集成的公开访问面。拟提供 `get_browser_task_access(agent)`，返回当前 Browser Agent 的访问对象；尚未配置浏览器 runtime 时返回明确的不可用状态。

Browser Agent 工厂在创建 runtime 时登记这个对象，并让页面工具、接入包和状态处理器使用同一份任务状态。配置构造与直接工厂构造两条路径均需覆盖。

宿主协作客户端通过现有 RuntimeSettings 承载拟新增的可选运行时字段 `coordinator`，默认值为空。该客户端由应用的 BuildContext 装配，负责绑定解析和操作租约；BrowserTaskAccess 负责把它与 runtime 的页面状态、证据机制连接起来。序列化路径只保存重建依据，恢复时重新注入客户端。

### 5.2 公开语义

| 拟新增入口 | 输入/输出 | 必须保证的行为 |
| --- | --- | --- |
| `resolve_binding()` | 返回当前任务的逻辑页面身份、代次及可信连接信息 | 由宿主按当前任务归属解析 |
| `operation_scope(binding, call_id, mode)` | 异步作用域；mode 为共享读或独占 | 取得宿主租约并校验绑定仍有效；覆盖完整复合操作 |
| `invalidate_page(binding, source_call_id, reason)` | 标记当前观察可能过期 | 更新页面状态版本，使相关观察及 refs 接受后续有效性检查 |
| `record_external_evidence(binding, call_id, evidence)` | 接收符合现有证据结构的数据 | 校验归属与格式，保留来源，进入既有 working context / 完成判定 |

上述名称表达最小接口形态。绑定字段复用现有 browser_instance/key 和宿主 resolver 的身份体系；具体 TargetID、endpoint 和租约只向可信执行端提供。

Core 的默认 runtime 可以继续按当前配置工作。使用外部宿主协调时，Core 将解析和租约请求委托给注入客户端，Electron 的页面分配、HTTP/RPC 协议和存储管理由 Swarm 实现。

### 5.3 身份与失效

| 信息 | 意义 | 变化时机 |
| --- | --- | --- |
| browser/page 逻辑身份 | 当前交互分支应操作哪个页面 | 任务重新分配页面 |
| profile / 存储身份 | 哪些页面共享登录与同源存储 | 宿主选择不同存储空间 |
| host_epoch | 当前宿主实例 | Electron 重启 |
| page_epoch | 当前页面实例 | 页面重建 |
| state_revision | 页面观察是否仍可用于后续决策 | 已知或可能影响页面的操作 |
| 现有 refs 版本 | 元素引用属于哪次有效观察 | runtime 刷新与引用失效 |

解析和加锁期间页面可能变化，operation_scope 必须校验代次，取得租约后返回有效绑定；调用使用作用域内的最终绑定执行。已保存的连接信息不能跳过该检查。

页面保活租约与操作租约分别管理。关闭接入连接或释放操作租约只结束本次调用的资源占用，页面回收由宿主决策。

### 5.4 两类执行器的协调

同一页面中，确认无导航、脚本状态及网络配置变更的读取可以共享租约；交互、导航及未知行为使用独占租约。不同页面的独立调用可以并发。登录、退出及共享存储变化由宿主协调相关 profile/origin，并通知受影响 runtime。

adapter 的操作类别由接入包的已验证兼容信息决定。adapter 内部可能导航、点击或执行脚本，因此仍需页面操作协调。命令名称或业务上的“查询”不能单独证明页面操作可并发；已确认完全不依赖浏览器的命令不申请页面租约。

Playwright 工具、runtime 内部观察/恢复和 MCP wrapper 都参与同一租约协议。复合操作内部透传调用关联，复用已持有的租约，避免重新申请同一互斥资源。跨进程传播与宿主校验方式见 [Swarm 设计第 7 节](opencli-swarm-design.md#74-mcp-调用关联与复合操作)。

任务超时、租约过期或 CLI 退出后，浏览器发出的业务请求仍可能在执行。协调方对这类调用记录待核实状态，后续冲突操作先确认当前状态再继续。

### 5.5 跨进程调用关联

可信 runtime 需要将 operation/call 关联、父租约与页面代次送达实际 MCP wrapper。拟使用 MCP 请求的应用命名空间 `_meta`，不加入模型可填写的工具参数。Core 提供通用调用元数据的透传能力，Swarm 负责租约内容和宿主核验。

当前 McpTool 和 stdio/Playwright 客户端主要发送工具名称及 arguments，尚没有上述通路。实现需贯穿浏览器 runtime、工具适配与实际客户端发送；复合操作的内部调用继承父关联，并保留自己的子调用身份。缺省不携带元数据时保持既有行为；要求协调但无法透传的链路须明确返回能力缺口，不能悄悄丢弃关联。

具体公开签名在接口评审时确定，采用调用局部数据，避免进程级“当前租约”变量。首期验证本地 stdio 链路，并检查 MCP 客户端接口及其他实现的签名兼容性；远端协调不在本期范围。

## 6. 页面状态、原始输出和任务证据

### 6.1 页面状态处理

当前 BrowserStateContextProcessor 的部分刷新依据是 browser_* 工具名称。拟将外部页面失效通知接入同一状态更新流程，使它也能处理 shell 所触发的变化。

1. 接入包根据已验证操作语义和真实执行情况发出失效通知；发生异常且可能改页时保守失效。
2. runtime 依据 page、调用 ID 和状态版本去重，标记当前观察与引用的有效性。
3. 下一次模型推理前，按任务需要获取新页面状态。
4. 同批工具调用中的后续元素动作，在真正执行前核对页面代次及 refs 状态，避免使用刚刚失效的引用。

失效通知须在释放冲突操作租约前落定。并发共享读观察若遇到版本变化，其结果需要按版本检查后采用。普通 shell 命令未声明页面影响时，沿用原处理。

### 6.2 输出处理与证据接入

BrowserRuntimeRail 对 shell 调用保留原 ToolOutput 和展示内容；浏览器状态与证据通过公开入口单独接入。实现时明确区分浏览器原生工具结果与外部 shell 结果，避免将普通终端输出套入页面工具的归一化逻辑。

证据有两种来源：

| 来源 | 处理方式 |
| --- | --- |
| 已支持操作的可靠 CLI 数据 | 应用接入包按规则解释，提交当前 runtime 接受的证据结构，并记录命令/页面/调用来源 |
| Browser Agent 的页面观察 | 沿用 Playwright 和现有 Browser runtime 的证据路径 |

未经适配的 CLI 输出可以帮助 Agent 决策；需要满足 runtime 完成条件时，必须获得被其接受的证据。退出码 0 只证明进程层面的成功返回。任务完成由现有证据规则和用户要求共同约束。

通用链路必须验证原 CLI 输出可供 Agent 使用，并验证 CLI 证据或页面观察能够满足 runtime 的完成判定；站点专用转换器按需添加。若所需证据仍不足，继续收集页面证据并明确结果状态。用户指定的截图、页面核对等步骤按原任务要求执行。

## 7. 当前实现与目标改动

下表来自源码阅读，运行行为仍需实施阶段验证。

| 模块 | 当前实现 | 本设计要完成的工作 |
| --- | --- | --- |
| PluginSpec / LoadRecord | 已有工具、rail、提示及 Skill 装卸机制 | 纳入挂载归属和接入 rail 持有的可撤销登记生命周期 |
| SkillSpec / binder | 已有 dir、mode、enabled_skills；挂载配置传递尚不完整 | 按挂载项贯通配置，加入 directory_view |
| SkillTool | 已有相对文件读取，每次会附加目录信息 | 根据挂载策略决定是否扫描与附加 |
| BashTool / PowerShellTool | 调用 SysOperation，工具层尚未贯通调用环境 | 登记执行作用域，传递 environment，覆盖普通/流式/取消 |
| BaseShellOperation | execute_cmd、execute_cmd_stream、execute_cmd_background 已有 environment | 复用现有进程接口 |
| Browser Agent 工厂 | 构造 runtime、rail、工具和上下文处理器 | 登记公开访问面，贯通可选 coordinator |
| BrowserRuntimeRail | 浏览器结果归一化、状态与证据处理 | 保持 shell 原结果，通过公开入口衔接页面和证据 |
| BrowserStateContextProcessor | 部分刷新依赖浏览器工具名称 | 消费显式失效信号，执行前校验过期 refs |
| ToolCallResilienceRail / ToolCard | 已有幂等性与重试约束 | 保持 shell 非幂等语义，验证接入异常不造成重复执行 |

当前 BrowserRuntimeRail 会提前准备 Playwright/MCP。首期沿用该生命周期，并在混合任务验证中记录这部分启动成本。

### 7.1 功能文件清单

以下路径以新仓内的 `agent-core/` 为根。“修改”表示文件已存在；“新增”表示建议落点，实施时才创建。工作项编号对应第 8.1 节，说明中的接口均属于本设计的拟实现内容。

**Skill 挂载与披露（C1、C5）**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [openjiuwen/harness/schema/extension_spec.py](../../../../../agent-core/openjiuwen/harness/schema/extension_spec.py) | 为 SkillSpec 增加 `directory_view` 及默认值、取值校验；保持配置可序列化。 |
| 修改 | [openjiuwen/harness/resources/extension_resolver.py](../../../../../agent-core/openjiuwen/harness/resources/extension_resolver.py) | 将展示策略传入 ResolvedSkill；保留 mode、enabled_skills 和准确目录，作为 binder 的完整输入。 |
| 修改 | [openjiuwen/harness/extension_binder.py](../../../../../agent-core/openjiuwen/harness/extension_binder.py) | 按挂载 owner 应用 Skill 配置，记录叶目录与资源归属；卸载准确撤销提示、缓存和本挂载贡献，并处理共享工具的使用者关系。 |
| 修改 | [openjiuwen/harness/rails/skills/skill_use_rail.py](../../../../../agent-core/openjiuwen/harness/rails/skills/skill_use_rail.py) | 管理按挂载项区分的可见视图、元信息提示和发现缓存；向读取/列表工具提供当前挂载配置，按归属复用工具。 |
| 修改 | [openjiuwen/harness/tools/skills/skill_tool.py](../../../../../agent-core/openjiuwen/harness/tools/skills/skill_tool.py) | 读取目标文件时应用所属挂载策略；`none` 跳过附加目录树与嵌套技能名，`full` 保持当前展示。 |

**Shell 执行作用域（C2、C5）**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 新增 | `openjiuwen/harness/tools/shell/execution_scope.py` | 放置调用信息、作用域协议和可撤销登记的共用实现；处理 owner、命中冲突、结果观察及有界收尾。内容保持与 OpenCLI、浏览器无关。 |
| 修改 | [openjiuwen/harness/tools/shell/bash/_tool.py](../../../../../agent-core/openjiuwen/harness/tools/shell/bash/_tool.py) | 提供 `bind_execution_scope`，在既有检查后进入作用域，将 environment 传给 SysOperation；普通、流式、异常和取消路径共用生命周期逻辑。 |
| 修改 | [openjiuwen/harness/tools/shell/powershell/_tool.py](../../../../../agent-core/openjiuwen/harness/tools/shell/powershell/_tool.py) | 接入相同作用域机制，保留 PowerShell 的命令、权限和输出语义；启动前检查受管调用支持的执行方式。 |
| 修改 | [openjiuwen/harness/tools/shell/__init__.py](../../../../../agent-core/openjiuwen/harness/tools/shell/__init__.py) | 导出应用登记作用域所需的公共类型，供接入 rail 正常导入。 |

**浏览器访问、页面状态和证据（C3、C4）**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 新增 | `openjiuwen/harness/tools/browser_move/playwright_runtime/task_access.py` | 定义 BrowserTaskAccess 和宿主 coordinator 的最小协议，承载绑定解析、操作作用域、页面失效与证据提交的公开语义。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/config.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/config.py) | 为 RuntimeSettings 增加可选运行时 coordinator；默认空值兼容现有装配，活句柄通过重建流程恢复。 |
| 修改 | [openjiuwen/harness/subagents/browser_agent.py](../../../../../agent-core/openjiuwen/harness/subagents/browser_agent.py) | 两种构造入口贯通 coordinator，在创建 runtime 时登记任务访问对象，提供 `get_browser_task_access`，随 Agent 生命周期清理登记。 |
| 修改 | [openjiuwen/harness/subagents/__init__.py](../../../../../agent-core/openjiuwen/harness/subagents/__init__.py) | 导出浏览器任务访问 helper，使应用使用正式入口。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/__init__.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/__init__.py) | 按包的导出方式公开任务访问协议，保持导入依赖受控。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py) | 实现公开入口到 runtime 的衔接；将页面动作、内部观察和恢复纳入操作作用域；在 BrowserRuntimeRail 中保留 shell 原结果，将外部证据接入现有任务完成判断。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/page_state.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/page_state.py) | 维护外部失效对页面观察和 refs 的影响；明确页面代次、状态版本与引用版本的关系，支持执行前有效性检查。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py) | 消费显式页面失效信号，按当前状态决定刷新；覆盖 shell 改页后的下一轮观察。 |
| 修改 | [openjiuwen/harness/tools/browser_move/playwright_runtime/browser_working_context.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_working_context.py) | 将已校验外部证据写入既有 working context，保留来源调用与页面关联，并沿用现有保留/压缩语义。 |

**MCP 调用元数据：C3 的配套改动**

| 类型 | 文件 | 改动说明 |
| --- | --- | --- |
| 修改 | [openjiuwen/core/foundation/tool/mcp/base.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/base.py) | 从可信调用上下文取得可选元数据，送往实际客户端；模型 arguments 保持原工具语义。 |
| 修改 | [openjiuwen/core/foundation/tool/mcp/client/mcp_client.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/client/mcp_client.py) | 定义默认兼容的可选请求元数据入口，检查现有客户端实现的签名兼容。 |
| 修改 | [openjiuwen/core/foundation/tool/mcp/client/stdio_client.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/client/stdio_client.py)、[playwright_client.py](../../../../../agent-core/openjiuwen/core/foundation/tool/mcp/client/playwright_client.py) | 将元数据真正写入 MCP 请求，验证 SDK 支持与取消链路；具体方法签名以联调结果为准。 |

### 7.2 需要按接口落地情况联动的文件

这些文件已有对应机制，是否修改取决于主改动能否通过现有入口完成；实施评审按下列触发条件确认范围。

| 文件 | 触发条件与改动说明 |
| --- | --- |
| [openjiuwen/harness/tools/skills/list_skill.py](../../../../../agent-core/openjiuwen/harness/tools/skills/list_skill.py) | 若现有 get_skills 回调不足以表达挂载身份或同名 Skill，则补列表与选择逻辑；可见集合由 SkillUseRail 提供。 |
| [openjiuwen/harness/resources/extension_loader.py](../../../../../agent-core/openjiuwen/harness/resources/extension_loader.py) | 若包文件归一化不能透传 directory_view，则补字段传递，使文件加载与直接 PluginSpec 加载一致。 |
| [openjiuwen/harness/schema/config.py](../../../../../agent-core/openjiuwen/harness/schema/config.py)、[openjiuwen/harness/schema/deep_agent_spec.py](../../../../../agent-core/openjiuwen/harness/schema/deep_agent_spec.py) | 检查 RuntimeSettings 活句柄经过 SubAgentConfig / Spec 的路径；需要时补序列化排除与恢复装配，保持 seed 仅含可重建信息。 |
| [openjiuwen/harness/deep_agent.py](../../../../../agent-core/openjiuwen/harness/deep_agent.py) | 若现有插件卸载/Agent 关闭不能等待接入 rail 的在途收尾，则补异步卸载次序和失败传播。 |
| [openjiuwen/harness/tools/browser_move/playwright_runtime/runtime_tools.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime_tools.py)、[openjiuwen/harness/tools/browser_move/controllers/action.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/controllers/action.py) | 复合工具或内部动作需要透传同一调用/租约时调整入口，确保一个 batch 的完整操作区间。 |
| [openjiuwen/harness/tools/browser_move/playwright_runtime/browser_tools.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_tools.py) | 将浏览器 operation 关联传入 MCP 客户端，覆盖公开工具和 runtime 内部调用；与第 7.1 节的客户端透传共同验收。 |
| [openjiuwen/harness/tools/browser_move/playwright_runtime/browser_working_context_processor.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_working_context_processor.py) | 若现有投影不能读取新增来源关联，则补外部证据的上下文投影，保持 shell 原消息内容。 |

### 7.3 测试文件清单

下表是后续开发的验证落点，本轮只登记计划。新增测试按现有测试目录组织，重点验证行为与边界。

| 类型 | 文件 | 覆盖说明 |
| --- | --- | --- |
| 修改 | [tests/unit_tests/harness/tools/test_skill_tool.py](../../../../../agent-core/tests/unit_tests/harness/tools/test_skill_tool.py)、[tests/unit_tests/harness/test_skill_rail.py](../../../../../agent-core/tests/unit_tests/harness/test_skill_rail.py) | full/none、按需读取、列表与提示范围、叶技能隔离及原行为回归。 |
| 修改 | [tests/unit_tests/harness/resources/test_loader.py](../../../../../agent-core/tests/unit_tests/harness/resources/test_loader.py) | directory_view 从包配置到 Spec 的传递及默认值兼容。 |
| 新增 | `tests/unit_tests/harness/resources/test_skill_mounts.py` | 多挂载策略、同目录多 owner、准确卸载与可见视图恢复。 |
| 新增 | `tests/unit_tests/harness/resources/test_plugin_resource_ownership.py` | 共用 shell、登记归属、在途卸载以及挂载失败后的回滚。 |
| 新增 | `tests/unit_tests/harness/tools/test_shell_execution_scope.py` | 登记/撤销、多个命中冲突、并发环境隔离、准备失败、流关闭/取消、清理异常与实际执行次数。 |
| 修改 | [tests/unit_tests/harness/tools/test_shell_tools.py](../../../../../agent-core/tests/unit_tests/harness/tools/test_shell_tools.py)、[tests/unit_tests/harness/tools/test_powershell/test_powershell_tool.py](../../../../../agent-core/tests/unit_tests/harness/tools/test_powershell/test_powershell_tool.py) | 两种真实工具实现接入作用域后仍遵守权限和输出约定。 |
| 新增 | `tests/unit_tests/harness/tools/browser_move/test_browser_task_access.py` | 使用假宿主验证绑定代次、租约范围、任务归属、公开入口及失效/证据提交。 |
| 修改 | [tests/unit_tests/harness/tools/browser_move/test_create_browser_agent.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_create_browser_agent.py) | 两种构造路径、默认 coordinator、任务访问对象和重建装配。 |
| 修改 | [tests/unit_tests/harness/tools/browser_move/test_browser_runtime_rail.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_runtime_rail.py)、[tests/unit_tests/harness/tools/browser_move/test_browser_result_contracts.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_result_contracts.py) | shell 原结果保留、外部证据进入完成判定、非零退出与未决状态。 |
| 修改 | [tests/unit_tests/harness/tools/browser_move/test_browser_page_state.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_page_state.py)、[tests/unit_tests/harness/tools/browser_move/test_browser_state_context_processor.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_state_context_processor.py) | 外部改页、旧 refs 拒绝、同批次执行检查、按需刷新及通知去重。 |
| 修改 | [tests/unit_tests/harness/tools/browser_move/test_browser_working_context.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_working_context.py)、[tests/unit_tests/harness/tools/browser_move/test_browser_batch_interact.py](../../../../../agent-core/tests/unit_tests/harness/tools/browser_move/test_browser_batch_interact.py) | 外部证据保留与复合操作的完整租约范围。 |

MCP 调用关联另新增 `tests/unit_tests/core/foundation/tool/mcp/client/test_request_metadata.py`，覆盖缺省兼容、并发调用隔离、实际请求字段及取消；浏览器复合动作继承由上述 runtime/batch 测试覆盖。Swarm 端到端测试必须确认 wrapper 实际收到关联，不能只验证 Python 对象中存在字段。

### 7.4 实现时同步的规约文件

| 类型 | 文件 | 同步说明 |
| --- | --- | --- |
| 修改 | [openjiuwen/harness/docs/specs/S_01_public-api-and-construction.md](../../../../../agent-core/openjiuwen/harness/docs/specs/S_01_public-api-and-construction.md) | 公开入口、runtime 句柄装配和序列化边界。 |
| 修改 | [openjiuwen/harness/docs/specs/S_05_tools-contract.md](../../../../../agent-core/openjiuwen/harness/docs/specs/S_05_tools-contract.md) | shell 执行作用域、权限次序、原结果和收尾约定。 |
| 修改 | [openjiuwen/harness/docs/specs/S_13_resources-packages.md](../../../../../agent-core/openjiuwen/harness/docs/specs/S_13_resources-packages.md) | SkillSpec 字段、挂载归属、共享资源和卸载规则。 |
| 修改 | [openjiuwen/harness/docs/specs/S_18_subagents-and-lifecycle.md](../../../../../agent-core/openjiuwen/harness/docs/specs/S_18_subagents-and-lifecycle.md) | BrowserTaskAccess、coordinator、页面失效/证据及恢复生命周期。 |
| 新增 | `openjiuwen/harness/docs/features/F_<编号>_shell-browser-integration.md` | 记录实现决策、验证结果和兼容边界；编号在实施归档时按仓内顺序分配。 |

以上规约随实际实现同步；当前讨论稿仍以本文为准。

## 8. 实施工作项与验收

### 8.1 Core 工作项

| 编号 | 交付内容 | 验收重点 |
| --- | --- | --- |
| C1：Skill 挂载 | Spec → resolver → binder → rail/tool 的配置与归属贯通 | 目录策略、叶技能可见性、共享挂载、卸载及恢复 |
| C2：Shell 作用域 | 两种 shell 的公开登记、调用局部 environment、统一收尾 | 权限顺序、环境隔离、真实进程生命周期、原结果保留 |
| C3：浏览器访问 | BrowserTaskAccess、工厂登记、coordinator 与 MCP 调用元数据传递 | 两种构造路径、准确归属、重建与代次校验，wrapper 实际收到父/子关联 |
| C4：状态与证据 | 外部失效通知、refs 执行前检查、既有证据接入 | 双向接续、同批调用、完成判定、异常后页面状态 |
| C5：装配闭环 | PluginSpec 资源归属、缓存子代理与恢复处理 | 在途卸载、共用 shell、当前配置生效、默认行为兼容 |

C1 和 C2 可分别实现；C3 与 Swarm 宿主契约共同评审；C4 基于 C2/C3 验证完整链路，C5 验证能力生命周期。Core 主要修改 harness，底层进程能力通过现有 SysOperation 复用；MCP 请求元数据透传需要联动 foundation/tool/mcp。

### 8.2 必须覆盖的验证

| 场景 | 预期证据 |
| --- | --- |
| 未装配接入能力 | 原 Browser Agent、shell 和 Skill 行为保持兼容 |
| 两条命令并发 | 每条命令获得自身环境与页面，进程全局环境不变 |
| 权限拒绝或准备失败 | CLI 未启动，已取得的局部资源已清理 |
| 普通/流式/取消 | 收尾执行一次，输出保留，租约按真实生命周期结束 |
| 清理或证据处理失败 | 原命令只执行一次，保留原结果与待处理状态 |
| 页面重建 | 旧绑定失效，重新解析后连接正确页面 |
| shell → Playwright → shell | 页面状态连续，旧 refs 被拒绝，证据能用于任务完成 |
| 同页冲突和跨页并发 | 冲突操作隔离，独立页面存在实际执行重叠 |
| Skill 与能力卸载 | 后续上下文遵循当前配置，共享资源继续有效 |
| 未决写入 | 先核实业务状态，两个执行路径不会自动重复提交 |

以上为待实施测试，本轮未编写或执行。修改正式 Core 契约时同步相关 S_01、S_05、S_13、S_18 等规约和特性说明，保持规约与实际实现一致。

### 8.3 Swarm 配套交付

[Swarm 设计](opencli-swarm-design.md)已给出统一启用判断、轻量挂载 rail、动态 adapter 索引与渐进 Skill、运行包/实际来源管理、页面映射、宿主协调协议和诊断展示。普通网站 adapter 走通用路径，站点专项记录按需补充。协议仍为待评审提案，MCP 调用关联和真实 CDP 路径须通过端到端验证后定稿。

Core 与 Swarm 的关键联调边界是：**在原 shell 调用内取得当前页面的执行条件，并在结束时正确更新同一个 Browser runtime 的状态。**

## 9. 代码阅读入口

- 装配：[extension_spec.py](../../../../../agent-core/openjiuwen/harness/schema/extension_spec.py)、[extension_binder.py](../../../../../agent-core/openjiuwen/harness/extension_binder.py)、[BuildContext](../../../../../agent-core/openjiuwen/harness/schema/build_context.py)。
- Shell：[BashTool](../../../../../agent-core/openjiuwen/harness/tools/shell/bash/_tool.py)、[PowerShellTool](../../../../../agent-core/openjiuwen/harness/tools/shell/powershell/_tool.py)、[BaseShellOperation](../../../../../agent-core/openjiuwen/core/sys_operation/shell.py)。
- Skill：[SkillUseRail](../../../../../agent-core/openjiuwen/harness/rails/skills/skill_use_rail.py)、[SkillTool](../../../../../agent-core/openjiuwen/harness/tools/skills/skill_tool.py)。
- 浏览器：[browser_agent.py](../../../../../agent-core/openjiuwen/harness/subagents/browser_agent.py)、[RuntimeSettings](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/config.py)、[runtime.py](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/runtime.py)、[状态处理器](../../../../../agent-core/openjiuwen/harness/tools/browser_move/playwright_runtime/browser_state_context_processor.py)。
- 权限与重试：[tool_security_rail.py](../../../../../agent-core/openjiuwen/harness/rails/security/tool_security_rail.py)、[tool_call_resilience_rail.py](../../../../../agent-core/openjiuwen/harness/rails/tool_call_resilience_rail.py)。
