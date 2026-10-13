# OpenCLI 与 JiuwenSwarm Electron 的 CDP 接入调查

> 日期：2026-09-23。范围：源码核对；没有执行 Electron 连接或站点操作。
>
> 基线：用户确认的 `LasVie/OpenCLI:main`，已拉取到新仓 `opencli/`；提交 `8271afc67e8504bda94c147f446ee29775d08274`，包版本 `1.8.8`。本轮未更新旧的全局 npm 安装。
>
> 目标链路：Browser Agent 通过现有 shell 调用已配置的 OpenCLI 站点 adapter；需要浏览器时连接 Swarm 分配的任务页面，通用网页操作使用 Playwright。上述 checkout 为源码研究基线，对应发行物尚未安装或验证。本文仅核对 adapter 所需的浏览器/CDP 能力。

## 1. 结论

源码已有普通网站适配器直接连接 CDP 的基础，可作为内置 Electron 的首选接入路径。它没有自动识别 JiuwenSwarm 会话/成员页面的能力，也不能只设置一个浏览器级 HTTP 地址就认为绑定准确。

建议路径：Browser Agent 提交原 CLI shell 命令 → 经过原 shell 权限链 → 接入层向 Swarm 解析当前页面 → 取得准确 TargetID 与页面 WebSocket → 通过现有 shell 底层的调用级 environment 设置 `OPENCLI_CDP_ENDPOINT` → 执行命令 → 收尾并通知页面状态，保留宿主页面。调用级环境与收尾由 [Core 执行作用域](opencli-agent-core-design.md#4-shell-调用级执行作用域)提供。

这是一条由源码支持的可行候选链路，尚不是端到端兼容性结论。先以固定版本验证，后续不要依赖浮动 main 保证行为不变。

本期能力边界可与当前源码结构对应：站点 adapter 命令经 [commanderAdapter.ts](../../../../../opencli/src/commanderAdapter.ts) 进入 [execution.ts](../../../../../opencli/src/execution.ts)，通用 browser 命令在 CLI 中另有入口。adapter 可能需要预导航或页面交互，也存在无需浏览器的命令分支。因此，绑定与租约按实际 adapter 依赖启用，通用链路先用 fixture 验证；站点专项兼容后续补充，设计不依赖逐站准入白名单。应用方案见 [Swarm 设计](opencli-swarm-design.md)。

## 2. “自动 CDP”实际包含什么

| 能力 | 实际实现 | 对本项目的含义 |
| --- | --- | --- |
| 自动选择传输 | `src/runtime.ts:getBrowserFactory` 看到 `OPENCLI_CDP_ENDPOINT` 就选择 CDPBridge；否则已登记 Electron 应用走 CDP，其余走扩展 Bridge | 普通网站命令可以显式指定 CDP，不必伪装为桌面应用 |
| 桌面应用端口发现 | `src/launcher.ts:resolveElectronEndpoint` 根据应用注册项的端口探测；未就绪时在支持的平台走启动逻辑 | 不是浏览器的通用发现服务；Windows 自动启动未实现，且本产品不应让 OpenCLI 重启 Electron |
| HTTP endpoint 目标选择 | `src/browser/cdp.ts` 请求 `/json`，给目标打分后选最高分 | 无法保证是当前任务页面 |
| `OPENCLI_CDP_TARGET` | 对 URL/标题模式匹配加分，而非严格过滤 | 不能作为任务边界；匹配不存在时仍可能选到别的目标 |
| 精确 WebSocket | endpoint 非 HTTP 时直接用其建立 WebSocket 连接 | 可以由 Swarm 提供准确的 page WebSocket，跳过启发式选择 |
| 连接释放 | `CDPBridge.close()` 关闭自身连接并清理 pending/event listener | 源码层面没有在该方法中调用 Browser.close；仍需验证真实适配器不会另外关闭页面 |

还有一个具体风险：目标打分会偏向 localhost/127.0.0.1 和某些应用页面，而 JiuwenSwarm 的可信产品 UI 也可能通过本地 HTTP 加载。因此“自动挑一个看起来合适的页面”不仅可能挑错成员，还可能挑到产品 UI。必须精确绑定。

来源：[本地 runtime](../../../../../opencli/src/runtime.ts)、[launcher](../../../../../opencli/src/launcher.ts)、[CDPBridge](../../../../../opencli/src/browser/cdp.ts)。对应远端：[runtime](https://github.com/LasVie/OpenCLI/blob/8271afc67e8504bda94c147f446ee29775d08274/src/runtime.ts)、[CDPBridge](https://github.com/LasVie/OpenCLI/blob/8271afc67e8504bda94c147f446ee29775d08274/src/browser/cdp.ts)。

## 3. 传输能力与操作兼容范围

- `CDPPage.tabs()` 返回空列表，`selectTab()` 未实现。宿主分配工作页可支持不同命令并发，但不等同于适配器内部的任意多标签页逻辑可用。
- 通用 `opencli browser` 的相关 CLI 入口仍直接构造 BrowserBridge。这组能力不属于本期 adapter 接入范围；通用网页操作由 Playwright 提供。
- `opencli doctor` 的相关健康检查仍围绕 daemon 和扩展；CDP 模式不能把它单独作为健康判据，也不应因扩展离线自动判定 Electron 不可用。
- BrowserBridge 的 profile/contextId 和 session lease 不自动变成 Electron 页面身份或操作锁。CDPBridge 接收 session 参数不意味着会按 session 创建新页面。
- 站点适配器可能使用 cookies、页面内 fetch、网络捕获、文件接口或自身的 daemon 辅助路径，需按真实操作依赖建立兼容清单。
- 不能将完整浏览器 WebSocket 或猜测地址冒充页面 WebSocket；页面关闭、宿主重启后需重新解析 TargetID，并核实所属 session/成员/profile。

来源：[CLI](../../../../../opencli/src/cli.ts)、[doctor](../../../../../opencli/src/doctor.ts)、[execution](../../../../../opencli/src/execution.ts)、[CDPBridge](../../../../../opencli/src/browser/cdp.ts)。

## 4. 并发能力的保留方式

上游 `extension/src/background.test.ts` 包含同 session 不同页面、不同 session 的并发执行用例；daemon 有 persistent site session 的写入租约。它们证明存在相应实现与测试设计，本次没有运行这些测试，不能当作 Electron 模式的验证结果。

Swarm 接入应保留三层并发：

1. 不同独立页面可并发调用不同 CLI 子进程，各自取得准确 endpoint 和局部环境；不修改全局 `OPENCLI_CDP_ENDPOINT`。
2. 同页经验证的纯读取可用共享租约；凡是导航、全局状态或网络捕获配置会变更，就不能仅按业务 `access=read` 放行。
3. 适配器内部已实现的独立请求并发可以保留，外层租约覆盖整条命令的资源占用；不把它的内部请求强制改成串行。

需要临时页时，由宿主分配同 partition 的任务工作页。记录 branch/page/shell call 对应关系，保留原 CLI 输出；失败需接续时保留该页。首期通过多个前台/流式 shell 调用并发，不把返回后台 PID 当作命令完成。页面间共享 cookies 和同源 storage，账号切换与业务冲突仍需协调。

Core 已有工具并行调用入口；本期不必先改写总调度器。页面锁属于动态资源约束，需要在两个执行器都能遵守的宿主边界执行。

来源：[扩展并发用例](../../../../../opencli/extension/src/background.test.ts)、[daemon](../../../../../opencli/src/daemon.ts)、[Core AbilityManager](../../../../../agent-core/openjiuwen/core/single_agent/ability_manager.py)。

## 5. 与现有 Electron 的衔接点

现有 `browser_panels.cjs` 已按 session/member 解析页面，并用 lease 防止活跃页面被回收。`target_mcp_wrapper.cjs` 已按准确 TargetID 找到 Playwright page。优先扩展这条契约：

- 保持持久化 partition 与受信任产品 UI 分离。
- 增加任务工作页身份及有上限的分配策略，用于真正独立的并发分支。
- 区分页面保活 lease 与 shared-read/exclusive 操作 lease。
- 向可信执行器返回经过校验的绑定，模型只持有不透明逻辑句柄。
- 两种执行器完成操作后汇报页面和认证状态变化，使对方的旧观察失效。
- 不允许过期绑定退回默认 profile、任意页面或重启宿主。

准确 endpoint 是运行路由保证，不是任意第三方脚本的安全沙箱；本轮范围仍是受信任适配器。

来源：[browser_panels.cjs](../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs)、[target_mcp_wrapper.cjs](../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs)、[electron_sideview.py](../../jiuwenswarm/agents/harness/common/electron_sideview.py)。

## 6. 接口冻结前的最小验证

以下是接口定稿前需要完成的验证，本轮仅制定方案：

| 项目 | 应观察的结果 |
| --- | --- |
| 精确绑定 | 多个成员页与可信产品 UI 同时存在时，只访问分配的页面；目标丢失时明确失败 |
| 页面与存储 | 同 partition 两页可共享预置测试存储，但导航独立；无需真实账号 |
| 适配器执行入口 | 使用预先配置的 fixture adapter 走实际 CLI 执行管线，验证浏览器绑定；通用 browser 命令不作为该项验证入口 |
| 双向接续 | OpenCLI 修改 fixture 页后 Playwright 获取新状态，反方向同样成立 |
| 并发 | 两条独立页面命令实际重叠执行；同页冲突动作串行，已验证同页读取可并发 |
| 释放与重连 | 释放/取消不关闭宿主；重建页面后重新绑定，不复用旧 TargetID |

先在隔离 Electron profile 与本地 fixture adapter 中完成这些检查，后续按真实网站 adapter 的依赖补充认证、文件操作或不确定写入回归；无需为接入站点 adapters 验证 OpenCLI 全部通用网页命令。设计文档可以先推进；涉及上游兼容承诺的接口在这些检查后定稿。

关联：[总体架构](opencli-integration-architecture.md)、[Agent Core 设计](opencli-agent-core-design.md)。
