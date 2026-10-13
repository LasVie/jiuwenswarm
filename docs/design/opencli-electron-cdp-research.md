# OpenCLI 与 JiuwenSwarm Electron 的 CDP 接入调查

> 日期：2026-09-23，2026-09-25 按[架构方案 v2](opencli-integration-architecture.md) 更新，同日按第二轮评审更正 daemon 判断；2026-09-29 补充 WP0 实测结论（§8），2026-09-30 补充真实宿主与 Bilibili 只读验证（§9）。范围：源码核对、Electron 43 上的 fixture、单 Agent 执行链路和 Bilibili 只读操作。
>
> 基线：用户确认的 `LasVie/OpenCLI:main`，源码位于与 Swarm 同级的独立仓 `../opencli/`（相对 Swarm 仓根目录）；提交 `8271afc67e8504bda94c147f446ee29775d08274`，包版本 `1.8.8`。实际运行使用原作者的 `@jackwener/opencli@1.8.8` 固定发行物，已由 WP0 和 M1 开发联调验证。

## 1. 结论

1. **CDP 直连精确页面可行（源码层面）。** 设置 `OPENCLI_CDP_ENDPOINT` 后，普通网站命令走 CDPBridge；传入页面级 WebSocket 地址可以跳过目标打分，精确连到指定页面。
2. **扩展路线在内置浏览器上不可行**，旧方案"把 OpenCLI 扩展装进 Browser Agent 的持久化 profile"不再沿用（§3）。
3. **OpenCLI 必须使用独立工作页。** 浏览器型 adapter 普遍会自己导航，连接时还会注入 stealth 脚本，不能与 Playwright 共用页面（§4）。
4. **运行包需要与用户全局的 `~/.opencli` 和 daemon 隔离**：私有 HOME 加上 `OPENCLI_SITE_SESSION=ephemeral`（§5、§6）。命令目录可以直接取自发行包内的 `cli-manifest.json`。
5. **上游错误契约是结构化的**，可以直接映射为工具的结果分类（§5）。

## 2. "自动 CDP"实际包含什么

| 能力 | 实际实现 | 对本项目的含义 |
| --- | --- | --- |
| 传输选择 | [runtime.ts:14-17](../../../opencli/src/runtime.ts#L14-L17)：有 `OPENCLI_CDP_ENDPOINT` 就用 CDPBridge；已登记的 Electron 应用走 CDP；其余走扩展 BrowserBridge | 普通网站命令可以显式指定 CDP，不必伪装成桌面应用 |
| HTTP endpoint 选目标 | [cdp.ts:64-71](../../../opencli/src/browser/cdp.ts#L64-L71) 请求 `/json` 后按分数挑一个目标；分数偏向 localhost 和部分应用页面 | 可能挑到别的成员页，甚至产品可信 UI，**不能使用** |
| `OPENCLI_CDP_TARGET` | 只对 URL/标题匹配加分，不做严格过滤 | 不能作为页面边界 |
| 页面级 WebSocket | endpoint 不以 http 开头时直接连接该地址 | 由宿主给出 `ws://127.0.0.1:<port>/devtools/page/<targetId>`，精确绑定 |
| 连接时的动作 | [cdp.ts:86-87](../../../opencli/src/browser/cdp.ts#L86-L87)：`Page.enable`，并通过 `Page.addScriptToEvaluateOnNewDocument` 注入 stealth 脚本 | 会改变目标页的脚本环境，进一步说明不能与 Playwright 共用页面 |
| 连接释放 | [runtime.ts:63-85](../../../opencli/src/runtime.ts#L63-L85) 在 finally 中调用 `CDPBridge.close()`，只关闭自身的 ws | 源码层面不会关闭页面，需实测确认 |
| 桌面应用端口发现 | `launcher.ts:resolveElectronEndpoint` 按应用注册项探测端口 | 不是通用发现服务；本产品不允许 OpenCLI 启动或重启 Electron |

## 3. 扩展路线为何不用

- OpenCLI 扩展是 MV3，申请了 `debugger`、`tabs`、`cookies`、`tabGroups`、`downloads` 等权限（[manifest.json:6-15](../../../opencli/extension/manifest.json#L6-L15)）。Electron 支持的扩展 API 只是 Chrome 的一个子集，不包含 `chrome.debugger`、`tabGroups`、`downloads`，扩展的核心能力在内置浏览器里无法工作。
- 旧实现（`OpenJiuwen_OpenCLI_Adapter` 中的 `opencli_browser_bridge.py`）依赖本地 daemon（端口 19825），通过扫描 profile 的 LevelDB 找 contextId，再用正则往命令里注入 `--profile`。链路长、依赖多，并且需要 shell 命令改写。
- 结论：只用 CDP 直连。以后外置 Chrome 模式如果要支持 OpenCLI，也走"managed Chrome 打开调试端口 + CDP"，不回到扩展。

## 4. adapter 对页面的影响

依据发行包内的 `cli-manifest.json`（1366 条命令，179 个站点）统计：

| 类别 | 命令数 | 说明 |
| --- | --- | --- |
| 不需要浏览器（`public` / `local`） | 324 | 本期同样不开放给外置浏览器模式（架构决策 D4） |
| 需要浏览器 · `cookie` | 778 | 以页面作为带登录态的请求环境 |
| 需要浏览器 · `ui` | 195 | 直接操作页面 UI |
| 需要浏览器 · `public` / `intercept` | 69 | 读取公开页面或拦截网络请求 |

导航行为：

- 388 条命令声明了预导航 URL，执行前先 `page.goto(...)`（[execution.ts:315-329](../../../opencli/src/execution.ts#L315-L329)）；`cookie` 策略且有 domain 的命令默认预导航到 `https://<domain>`（[registry.ts:191-200](../../../opencli/src/registry.ts#L191-L200)）。
- 428 条 `navigateBefore=false` 的命令中，至少 259 条所在文件里有 `goto`/`navigate` 调用，即在函数内自行导航（未逐条核实）。
- `ui`/`intercept` 策略且没有 domain 的命令，`navigateBefore=true`：表示需要浏览器，但不做预导航。

结论：OpenCLI 与 Playwright 共用页面，就会把 Playwright 正在操作的页面导航走。共享登录态只需要同一个 partition，因此 OpenCLI 使用独立工作页。

同一 partition 共享的是 cookie、同源的 localStorage 与 IndexedDB。sessionStorage 按页面会话隔离；页面内存、未提交的表单和部分绑定在页面上的验证状态也不会随 URL 转移。所以两种执行器之间的接续只依赖可重建的 URL、业务 ID 和共享登录态，依赖原页面临时状态的操作留给 Playwright。

## 5. 运行包、目录与错误契约

**隔离**：用户 adapter 与插件目录写死为 `os.homedir()/.opencli`（[discovery.ts:23](../../../opencli/src/discovery.ts#L23)、[main.ts:31](../../../opencli/src/main.ts#L31)、[plugin.ts:32-42](../../../opencli/src/plugin.ts#L32-L42)）。`OPENCLI_CONFIG_DIR` 只影响配置文件，不影响这些目录。不隔离的话，用户全局安装的同名 adapter 或插件会覆盖内置版本。方案：让子进程的 `HOME`/`USERPROFILE` 指向产品私有目录（Node 的 `os.homedir()` 读取这两个变量）。

**目录**：package `files` 包含 `cli-manifest.json`，每条记录都有 `site`、`name`、`description`、`access`、`domain`、`strategy`、`browser`、`args`、`navigateBefore`、`siteSession`。可以直接用作命令目录，不需要运行 `opencli list`（它会执行插件初始化）。

**错误契约**：失败时，上游把 YAML 格式的错误信封 `{ok:false, error:{code, message, help, exitCode}}` 写到 stderr（[commanderAdapter.ts:170-187](../../../opencli/src/commanderAdapter.ts#L170-L187)）。退出码定义见 [errors.ts:26-36](../../../opencli/src/errors.ts#L26-L36)：

| 退出码 | 典型 code | 含义 |
| --- | --- | --- |
| 2 | `ARGUMENT` | 参数错误 |
| 66 | `EMPTY_RESULT` | 无数据 |
| 69 | `BROWSER_CONNECT`、`ADAPTER_LOAD` | 浏览器或 adapter 不可用 |
| 75 | `TIMEOUT`、`SESSION_BUSY` | 超时或会话忙 |
| 77 | `AUTH_REQUIRED`、`LOGIN_WALL` | 需要登录；验证码与 WAF 挑战也归入这一类（例如 [ctrip/train.js:56-58](../../../opencli/clis/ctrip/train.js#L56-L58)） |
| 78 | `CONFIG` | 配置错误 |

## 6. 传输能力的已知限制

- `CDPPage.tabs()` 返回空列表，`selectTab()` 未实现（[cdp.ts:448-452](../../../opencli/src/browser/cdp.ts#L448-L452)）。依赖多标签页的 adapter 在 CDP 模式下不可用，应归类为 `env_unavailable`，这一步改用 Playwright。
- 通用 `opencli browser` 命令直接构造 BrowserBridge，不在本期范围内。
- `opencli doctor` 的检查围绕 daemon 和扩展，不能作为 CDP 模式的健康判据。
- **CDP 模式仍可能连接 daemon（更正 09-25 初版的判断）。** 持久会话（`siteSession=persistent`）中的写命令会建立站点租约上下文（[execution.ts:282-285](../../../opencli/src/execution.ts#L282-L285)），收尾时调用 `releaseSiteSessionLease`（[execution.ts:456-463](../../../opencli/src/execution.ts#L456-L463)）。该函数会向 `127.0.0.1:19825` 发送 HTTP 请求（[daemon-client.ts:72](../../../opencli/src/browser/daemon-client.ts#L72)）。它不会启动 daemon，但如果用户自己在跑 daemon，就会连到它。`OPENCLI_DAEMON_PORT` 上游已不支持改端口（[constants.ts:6-26](../../../opencli/src/constants.ts#L6-L26)）。执行路径上只有这一处调用 daemon，`clis/` 下的 adapter 都不直接调用 daemon。
- **执行配置**：会话模式为 ephemeral 时，`leaseRun` 为空，不再发送释放请求。上游的解析顺序是：命令行 `--site-session`，其次环境变量 `OPENCLI_SITE_SESSION`，再次命令声明（[execution.ts:591-596](../../../opencli/src/execution.ts#L591-L596)）。所以必须由调用方在命令行上固定传入 `--site-session ephemeral`，并拒绝模型传入的运行控制参数；环境变量只能兜底。注意上游只给 `browser=true` 的命令注册了 `--site-session`（[commanderAdapter.ts:63-68](../../../opencli/src/commanderAdapter.ts#L63-L68)），不需要浏览器的命令不能带这个选项。受影响的是 314 条声明了 persistent 的命令（其中 144 条写命令，覆盖 bilibili、zhihu、xiaohongshu 以及各类对话站点等）：每次调用都会预导航（原本已在该域名下就会跳过），并失去站点级租约。后者由工作页串行替代。如果某些 adapter 依赖 persistent 语义，比如在同一会话里继续对话，就改为在自维护发行物中打补丁：CDP 模式下跳过 lease 释放。
- **上游超时不取消 adapter**：CLI 内部超时只是竞争等待（[execution.ts:373](../../../opencli/src/execution.ts#L373)），adapter 仍在后台运行。调用方要自己设定超时，并结束整个进程树。
- 页面级 CDP 地址只是运行路由，不是安全边界：本地 CDP 端口没有鉴权。所以 Browser Agent 不应该拿到 shell（架构决策 D2）。

## 7. 接口定稿前的验证项

在隔离的 Electron profile 上，用手工创建的同 partition 工作页和本地 fixture adapter 完成：

| 项目 | 应观察的结果 |
| --- | --- |
| 精确绑定 | 多个成员页和产品 UI 同时存在时，OpenCLI 只访问指定工作页；目标消失时明确报错 |
| 连接时的动作 | 页面级 ws 上 `Page.enable`、stealth 注入、`Network.getCookies`、页面内带凭据的 fetch 都能工作 |
| 共享登录态 | 在 Browser Agent 页面写入的 cookie，工作页上的 `cookie` 策略命令能读到；两页导航互不影响 |
| 释放与取消 | 断开 ws 后，工作页和宿主都存活；超时或取消后，结束整个进程树（含 adapter 启动的子进程），确认进程退出后，工作页进入"待重置"，不能直接复用 |
| 不连接 daemon | 命令行传入 `--site-session ephemeral` 时，**读、写两类** fixture 命令（写命令用声明了 persistent 的 fixture）执行期间都没有连接 19825 端口，也没有启动 daemon 进程；再在用户 daemon 运行的情况下重复一遍。反例：环境变量设为 ephemeral、命令行传入 `--site-session persistent` 时会连接 daemon（命令行优先，[execution.ts:591-596](../../../opencli/src/execution.ts#L591-L596)），说明运行控制参数必须由工具固定，不能交给模型 |
| 页内活动的停止 | 在 fixture 页面上让 adapter 派发一个长时间运行的脚本和请求，然后结束 CLI 进程：确认页面上的活动仍在继续；宿主重建 WebContents 后活动停止 |
| persistent 语义 | 抽查声明了 persistent 的真实站点命令（含对话类），在 ephemeral 下行为是否正确；有依赖时改用补丁方案 |
| 隐藏页面 | hidden 模式下 `ui` 策略命令能正常工作（`backgroundThrottling:false` 已设置，仍需确认可见性相关行为） |
| 未自行导航的命令 | `navigateBefore=true` 且函数内不导航的命令，在空白工作页上的表现；如果依赖页面已停在站点域名下，就在工具层先导航到 domain |
| 目录隔离 | 私有 `HOME` 下不加载用户全局 `~/.opencli` 中的 adapter 与插件；下载类命令的输出位置符合预期 |
| 错误映射 | fixture 分别触发 `AUTH_REQUIRED`、`EMPTY_RESULT`、`ARGUMENT`、超时，工具的 `executed` × `reason` 与架构方案 §4.3 一致；写命令进程启动后的任何失败都记为 `executed=unknown` |
| Electron Node 模式 | 开发版和打包版都用 `ELECTRON_RUN_AS_NODE=1 <electron 可执行文件>` 运行 OpenCLI；记录内置 Node 版本（要求不低于 20.18.1）；在系统 PATH 中没有 node 的环境下同样可用 |
| 不需要浏览器的命令 | `browser=false` 的 fixture 不带 `--site-session` 时正常执行；带上时报未知参数（反例） |
| 验证状态保留 | 在工作页上触发验证码，由人工完成后在同一页面重跑命令，确认验证结果能被复用（cookie 或同一页面的 sessionStorage） |

这些检查通过后，再按真实站点逐步补充认证、文件操作和写操作不确定场景的回归。Bilibili 可以作为第一个真实站点候选。

## 8. 实测结论（WP0，2026-09-29）

用 `tests/electron/opencli_smoke.cjs` 在 Electron 43.5.1（内置 Node 24.19.0）上逐项验证了 §7。逐项结果见[实现方案 §8.6](opencli-implementation-plan.md#86-wp0-连接验证)。需要真实站点的三项（persistent 语义、未自行导航的命令、验证状态保留）留给 WP11。

对本文结论的补充：

1. **§1 第 1 条得到证实**：页面级 ws 精确绑定工作页，Browser Agent 页不受影响；HttpOnly cookie 在两页之间共享。
2. **Electron Node 模式需要一个入口脚本**：commander 在 Electron 下会误判 argv 布局，所以运行包带一个 `entry.mjs`，先设置 `process.defaultApp` 再导入 `main.js`。
3. **§6 关于 daemon 的判断得到证实，并补充一条**：ephemeral 下不连接 daemon，persistent 写命令会连接。此外，需要浏览器的命令如果**没有** `OPENCLI_CDP_ENDPOINT`，会整体改走 daemon 和 Chrome 扩展，即用户自己的浏览器。执行器因此禁止在没有工作页地址时启动这类命令。
4. **§4 关于页内活动的判断得到证实**：结束 CLI 后，adapter 在页面里启动的活动仍在继续，必须重建 WebContents。
5. **参数写法**：可选具名参数注册为 `--name [value]`。拼装时用 `--name=value`，位置参数放在 `--` 之后，才能安全传递以 `-` 开头的值。

## 9. 真实宿主与站点补充（2026-09-30）

用真实 `main.cjs` 的工作页/IPC 函数、preload、React 确认与保留界面、Python 工具和固定 CLI 完成联调；范围与复现方式见[实现方案 §8.7](opencli-implementation-plan.md#87-m1-开发联调2026-09-30)。

- 写确认能在浏览器面板未挂载时被接收；「已完成」保留原 target 和 fixture 验证 cookie，「放弃」重建页面；真实写操作被取消后，未知结果落盘，进程与页面活动都停止。重建时恢复仍被选中面板的可见性，用户已切走的页面仍保持隐藏；再次验证码的原生页面截图已核对。
- Bilibili `hot`、`ranking`、`search` 第一轮和最终轮均返回 3 条；中间一轮 `hot/search` 各 3 条，`ranking` 为 empty，原因未定位。Agent 页未导航。ranking/search 的函数不自行导航，测试通过上游的预导航在工作页上执行。
- 单 Agent 使用固定模型响应，真实的 Swarm 装配和 Core runtime 对列表任务输出 completed，对验证码输出 blocked；同一次任务也能 adapter → 真实 Playwright → adapter，并以 completed 结束。真实模型决策与完整应用的恢复交互仍需后续验证。
- 外部操作重复签名必须保留完整参数；复用 Playwright 的签名会漏掉 site/command/嵌套 args。修复后，同一 Agent 的三个分页参数都到达了真实 CLI 和网站，未被误判为重复调用。
- reset/confirm 与 acquire 一样携带工作页标签和 visibility；否则重建后的 OpenCLI 页签会变成「主浏览器」，hidden 也可能被覆盖。
- WP0 探针无法独占 19825 时必须提前退出；端口占用回归已确认此时不会启动 CLI，也不会向现有 daemon 发命令。

打包版、真实站点验证码恢复、依赖 persistent 的对话命令，以及 hidden 页面的 ui 策略仍未验证。
