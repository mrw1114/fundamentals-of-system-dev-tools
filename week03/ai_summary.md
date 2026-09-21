# 总结opencode安全功能工作原理

> **Workspace:** c:\Users\27111\Documents\github_download\opencode

---

**User**

现在打开的项目是 opencode 的
github 仓库，请查看仓库尝试总结 opencode 中安全相关功能的工作原理。要求：不能修改项目和其他文件。

**Assistant**

我先快速查看一下项目记忆和仓库结构。

项目记忆目录不存在。开始探查仓库结构。

这是研究任务，我先建立任务清单并并行派发探查。

### Relevant Code Snippets
1. c:\Users\27111\Documents\github_download\opencode\packages\schema\src\permission.ts:L24-L64
   — 定义当前权限请求/响应核心数据结构：`Permission.Request`、`Reply`（`once/always/reject`）、`Effect`（`allow/deny/ask`）、`Rule`、`Ruleset`，以及权限事件 `permission.v2.asked/replied`。

2. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L75-L85
   — 权限规则匹配入口：`evaluate()` 使用 `Wildcard.match(action, rule.action)` 和 `Wildcard.match(resource, rule.resource)` 查找最近匹配规则，默认返回 `ask`。

3. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L154-L160
   — 权限决策逻辑：合并 agent 配置规则与持久化规则，按资源逐项评估；存在 `deny` 则拒绝，存在 `ask` 则请求审批，否则允许。

4. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L189-L217
   — `ask`/`assert` 行为：当决策为 `ask` 时创建待处理权限请求并发布 `Event.Asked`；`assert` 在 `allow` 时直接通过，在 `deny` 时抛 `BlockedError`，在 `ask` 时等待审批结果。

5. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L220-L283
   — 权限回复处理：`reply()` 根据 `once/always/reject` 执行不同逻辑；`always` 且带 `save` 时写入持久化规则，并自动通过同 session 的后续匹配请求。

6. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission\saved.ts:L21-L68
   — 持久化权限存储实现：`PermissionSaved.AddInput` 包含 `projectID/action/resources`，`add()` 将 `always` 批准的规则写入 `PermissionTable`，用于跨请求/重启后的权限延续。

7. c:\Users\27111\Documents\github_download\opencode\packages\core\src\v1\config\permission.ts:L16-L49
   — 配置层权限声明：定义 `permission` 配置项支持的 key，如 `read/edit/grep/bash/task/external_directory` 等，并支持全局字符串配置或按工具对象配置。

8. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\agent\subagent-permissions.ts:L4-L27
   — 子代理权限继承/限制逻辑：`deriveSubagentSessionPermission()` 合并父 session 的 `deny` 与 `external_directory` 规则，并根据子代理自身权限决定是否默认禁止 `todowrite/task`。

9. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\acp\permission.ts:L20-L89
   — ACP 前端/代理侧权限交互：定义 `once/always/reject` 选项，调用 `requestPermission()` 发起审批请求，并根据选择回复 `once/always/reject`；`always` 会触发后续持久化。

10. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\cli\cmd\run\permission.shared.ts:L174-L203
   — CLI 权限审批状态机：用户选择 `once` 时直接生成 `PermissionReply`，选择 `always/reject` 时进入对应阶段，体现“请求-回复/批准”的本地交互流程。

11. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\server\routes\instance\httpapi\handlers\permission.ts:L16-L39
   — HTTP API 权限回复路由：`/permission/reply` 接收 `PermissionV1.ReplyBody`，调用 `svc.reply()` 将审批结果写入权限服务，并处理 `NotFoundError`。

12. c:\Users\27111\Documents\github_download\opencode\packages\web\src\content\docs\permissions.mdx:L42-L91
   — 用户文档中的权限配置设计意图：说明 `permission` 配置项、`allow/ask/deny` 语义、全局与工具级配置、对象语法以及“最后匹配规则生效”的匹配顺序。

### Relevant Code Snippets
1. c:\Users\27111\Documents\github_download\opencode\packages\schema\src\credential.ts:L14-L34
   — 定义统一凭据模型：支持 `oauth` 与 `key` 两种类型，OAuth 存储 refresh/access/expires/metadata，key 存储 API key/metadata，是凭据存储格式的核心 schema。

2. c:\Users\27111\Documents\github_download\opencode\packages\core\src\credential\sql.ts:L5-L14
   — 数据库表 `credential` 结构：`value` 字段以 JSON 存储凭据内容，说明 OAuth/token/key 数据落盘格式。

3. c:\Users\27111\Documents\github_download\opencode\packages\core\src\credential.ts:L50-L133
   — 凭据服务层实现 CRUD；`create` 会先删除同一 integration 的旧凭据再插入，`update` 更新 label/value，`remove` 删除凭据，是认证凭据存储逻辑主体。

4. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\provider\auth.ts:L163-L220
   — Provider 认证流程：`authorize` 发起 OAuth，`callback` 接收授权码并保存结果；若返回 key 则存为 API 认证，若返回 refresh/access 则存为 OAuth 认证。

5. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\mcp\auth.ts:L37-L81
   — MCP OAuth 本地认证文件存储：凭据写入 `mcp-auth.json`，使用 `fs.writeJson(filepath, next, 0o600)`，权限为仅所有者读写，包含 token/clientInfo/codeVerifier/oauthState。

6. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\mcp\oauth-provider.ts:L96-L124
   — MCP OAuth token 读取与保存：`tokens()` 从本地认证数据读取 access/refresh/expires/scope，`saveTokens()` 回写 token 与过期时间。

7. c:\Users\27111\Documents\github_download\opencode\packages\opencode\src\mcp\oauth-callback.ts:L51-L102
   — OAuth callback 处理授权码与 state 参数，校验 state 防 CSRF，成功后解析 `code` 并返回授权页面，是 OAuth 流程关键节点。

8. c:\Users\27111\Documents\github_download\opencode\packages\llm\src\route\auth-options.ts:L42-L55
   — LLM provider 认证解析：优先使用显式 `auth` override，否则按环境变量/配置解析 `apiKey` 并包装为 bearer token。

### Relevant Code Snippets
1. c:\Users\27111\Documents\github_download\opencode\packages\core\src\tool\bash.ts:L61-L68
   — Bash 工具的安全机制说明与待办：当前是 V2 core shell boundary，明确 `TODO` 引入 tree-sitter bash/PowerShell parser、命令前缀审批、解析器级危险命令检测等。

2. c:\Users\27111\Documents\github_download\opencode\packages\core\src\tool\bash.ts:L78-L94
   — Bash 工具对 shell 命令做最小 token 解析，并扫描命令参数引用的外部目录；这是执行层安全边界的一部分。

3. c:\Users\27111\Documents\github_download\opencode\packages\core\src\tool\bash.ts:L121-L148
   — Bash 工具执行前解析 working directory，若为外部目录则调用 `permission.assert(...)` 做权限审批；随后对 `bash` action 和命令资源再次请求权限。

4. c:\Users\27111\Documents\github_download\opencode\packages\core\src\tool\bash.ts:L153-L170
   — Bash 工具实际启动 shell 进程，使用配置 shell 或默认 shell，并设置 timeout、输出大小限制、stdin ignore、detached 等执行层安全参数。

5. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L75-L85
   — 权限规则匹配核心逻辑：根据 action/resource 与规则做 wildcard 匹配，找不到规则时默认返回 `ask`。

6. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L146-L160
   — 权限判断逻辑：若任何资源匹配到 `deny` 则整体 deny；否则综合 allow/ask 决定，是工具执行层拒绝危险操作的核心路径。

7. c:\Users\27111\Documents\github_download\opencode\packages\core\src\permission.ts:L196-L217
   — `PermissionV2.assert` 执行权限断言；遇到 deny 抛 `BlockedError`，遇到 ask 等待审批，allow 则继续执行。

8. c:\Users\27111\Documents\github_download\opencode\packages\core\src\tool\registry.ts:L131-L134
   — 工具注册/物化阶段的整体禁用判断：如果规则对 tool action 的 resource 为 `*` 且 effect 为 `deny`，则直接移除该工具。

### Relevant Code Snippets
1. c:\Users\27111\Documents\github_download\opencode\packages\server\src\auth.ts:L19-L62
   — 服务端认证配置与凭证生成：从 `OPENCODE_SERVER_PASSWORD` / `OPENCODE_SERVER_USERNAME` 读取鉴权密钥，`authorized()` 校验用户名密码，`header()` 生成 `Authorization: Basic ...` 请求头。

2. c:\Users\27111\Documents\github_download\opencode\packages\server\src\middleware\authorization.ts:L9-L58
   — 服务端路由中间件实现鉴权：支持从 URL 查询参数 `auth_token` 或 HTTP `Authorization: Basic ...` 解析凭证；未通过时返回 `UnauthorizedError` 并设置 `www-authenticate`。

3. c:\Users\27111\Documents\github_download\opencode\packages\server\src\routes.ts:L39-L68
   — 服务端路由组装：`createRoutes()` 在提供认证配置后创建 HTTP API；`makeRoutes()` 将 `authorizationLayer`、`schemaErrorLayer`、session/location 等中间件注入路由。

4. c:\Users\27111\Documents\github_download\opencode\packages\server\src\cors.ts:L10-L25
   — 服务端 CORS 策略：默认允许 `http://localhost:*`、`http://127.0.0.1:*`、`oc://renderer`、Tauri localhost、`opencode.ai` 域名，以及配置中的 `cors` 白名单。

5. c:\Users\27111\Documents\github_download\opencode\packages\server\src\handlers\pty.ts:L119-L153
   — 与 CORS/Origin 联动安全控制：注释说明自定义 header 会触发 CORS preflight，因此跨源浏览器页面不能绕过服务端 origin 策略获取 PTY ticket；代码中用 `isAllowedRequestOrigin()` 校验 `origin/host`。

6. c:\Users\27111\Documents\github_download\opencode\packages\plugin\src\v2\effect\PLAN.md:L89-L94
   — 插件能力边界说明：transform 可执行任意 Effect，包括读取其他 PluginHost 服务、文件系统 I/O、网络 I/O；这是评估插件是否可执行任意代码/访问网络与文件的关键依据。

7. c:\Users\27111\Documents\github_download\opencode\packages\enterprise\src\routes\api\[...path].ts:L13-L15
   — 企业版 API 路由启用 Hono `cors()` 中间件，说明企业版对外 API 默认走通用 CORS 处理。

8. c:\Users\27111\Documents\github_download\opencode\packages\enterprise\src\routes\api\[...path].ts:L142-L152
   — 企业版管理员接口安全控制：`/support/actions/remove-share` 要求 `Authorization: Bearer <SUPPORT_API_KEY>`，使用 `timingSafeEqual()` 防时序攻击，未通过则返回 401。

让我直接核验几个关键文件，确保结论准确。

opencode 的安全模型核心是**「本机可信代理 + 细粒度权限门控」**——它没有 OS 级沙箱，而是通过「规则评估 → 审批 → 持久化」这套闭环，加上路径边界和凭据保护来控制风险。下图是权限判定的主流程。

## opencode 安全功能工作原理总结

**核心结论**：opencode 没有 OS 级沙箱/容器隔离，它是「**本机可信代理**」模型——工具以宿主用户的完整文件/进程/网络权限运行，安全性由**权限门控 + 路径边界 + 凭据保护 + 本地监听**四层构成。

---

### 一、权限门控（最核心机制）

**数据结构**（[permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/schema/src/permission.ts#L25-L64)）：一条规则是 `{ action, resource, effect }`，`effect` 只有 `allow / deny / ask` 三值。一个请求 `Permission.Request` 携带 `sessionID`、`action`、`resources[]`、`save[]`（"always" 时可持久化的模式）、`metadata`、`source`（哪个工具调用发起）。

**规则匹配**（[permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/permission.ts#L76-L86)）用通配符匹配，**最后命中的规则获胜**（`findLast`），无命中默认 `ask`——即「默认保守」。通配符实现见 [wildcard.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/util/wildcard.ts#L3-L14)（`*`/`?`，Windows 下大小写不敏感）。

**判定优先级**（[permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/permission.ts#L147-L162)）：先看 agent 自身规则，**任一 resource 命中 `deny` 立即整体拒绝**（deny 优先，不可被 allow 覆盖）；否则合并「agent 规则 + 已保存规则」评估，结果按 `deny > ask > allow` 收敛。

**执行入口** `assert()`（[permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/permission.ts#L197-L218)）：
- `allow` → 直接放行
- `deny` → 抛 `BlockedError`，工具不执行
- `ask` → 创建 pending 项并 `publish(Event.Asked)`，然后 `Deferred.await` **阻塞住工具调用**，直到用户回复

**审批回复** `reply()`（[permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/permission.ts#L220-L286)）：
- `reject` → 失败并**级联拒绝同 Session 的所有 pending 请求**；带 message 时抛 `CorrectedError`（把用户反馈回传给模型）
- `always` → 把 `request.save` 里的模式**写入数据库持久化**，并自动放行同 Session 中所有已被新规则覆盖的 pending 请求
- `once` → 只放行本次

**持久化**落在 SQLite 的 `PermissionTable`（[saved.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/permission/saved.ts#L54-L69)），按 `project_id` 隔离，读取时统一转成 `effect: "allow"` 规则。

**配置 → 规则的转换**在 [permission/index.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/permission/index.ts#L178-L198)：支持 `"permission": "allow"` 简写（展开为 `{"*": "allow"}`）和按工具的对象语法；pattern 支持 `~` / `$HOME` 展开。

**默认值**（[agent.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/agent/agent.ts#L119-L136)）：整体默认 `*: allow`，但 `doom_loop` 和 `external_directory` 默认 `ask`；`question`/`plan_enter`/`plan_exit` 默认 `deny`；`read` 对 `*.env` / `*.env.*` 默认 `ask`（`*.env.example` 放行），这是**唯一一处针对敏感文件的默认限制**。

**工具级全局禁用**（[registry.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/tool/registry.ts#L132-L135)）：如果某工具规则是 `resource: "*" && effect: "deny"`，该工具会**从模型可见的工具列表中直接移除**，模型根本看不到它。

**子代理继承**（[subagent-permissions.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/agent/subagent-permissions.ts#L14-L27)）：只继承父 Session 的 `deny` 规则和 `external_directory` 规则（父代理的限制不外溢到子代理的能力判定），并默认禁止子代理再用 `todowrite` / `task`（防递归派生）。

**双实现并存**：`core/src/permission.ts` 是 V2（按 Location 分片），`opencode/src/permission/index.ts` 是 V1 遗留实现，语义一致但状态存在 `InstanceState` 内存中。

**传播链路**：权限请求通过 `Event.Asked`/`Event.Replied` 事件发布，经 Server 的 HTTP/SSE 推给 TUI、App 前端和 ACP 客户端，HTTP 回复入口在 [handlers/permission.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/server/routes/instance/httpapi/handlers/permission.ts#L16-L39)。

---

### 二、工具层边界

**路径边界**是这层最实的设计（[location-mutation.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/location-mutation.ts#L90-L150)）：
- 相对路径必须留在 Location 内，否则抛 `relative_escape`
- 对已解析的真实路径（`realPath`）再做一次包含检查，**防符号链接逃逸**，否则抛 `location_escape`
- 绝对路径/Absolute 越界时标记为 external，必须单独走 `external_directory` 权限审批（`resource` 形如 `/path/to/dir/*`）

所有涉及路径的工具（`read`/`write`/`edit`/`apply-patch`/`glob`/`grep`/`bash`）都会先 `permission.assert` 再执行，见 [bash.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/tool/bash.ts#L128-L149)、[read.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/tool/read.ts#L63-L72) 等。

**bash 工具**（[bash.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/core/src/tool/bash.ts#L62-L95)）：
- 它**不具备命令解析能力**。文件顶部有一串明确 TODO：tree-sitter bash/PowerShell 解析、命令前缀审批（BashArity）、解析器级危险命令检测——都还没做
- 目前只有基于正则切 token 的**「命令参数外部目录扫描」**，且代码里明确写着 `this scan is advisory only`（仅提醒，不拦截）
- 安全兜底靠的是：命令字符串整体作为 resource 走 bash 权限规则（所以 `"rm *": "deny"` 这类配置才生效）+ 缺省 `ask`
- 资源保护：`stdin: "ignore"`、默认 2 分钟超时（上限 10 分钟）、**输出捕获上限 1 MiB**、POSIX 下 `detached` 便于进程组清理

**doom loop 检测**（[processor.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/session/processor.ts#L356-L379)）：检测最近 N 条 part 是否是**同一个工具 + 完全相同的 JSON 输入**，命中则触发 `doom_loop` 权限询问，防模型死循环刷工具。

---

### 三、凭据与认证

- **凭据模型**（[credential.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/schema/src/credential.ts#L15-L34)）：统一为 `oauth`（refresh/access/expires/metadata）与 `key`（api key）两种，落在 SQLite `credential` 表的 `value` JSON 字段
- **凭据文件**：[auth/index.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/auth/index.ts#L10-L88) 写 `auth.json` 时显式指定 **`0o600`**（仅所有者读写）；MCP 的 [mcp-auth.json](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/mcp/auth.ts#L75-L81) 同样 `0o600` 并用 flock 保护并发写。为**明文存储**，无加密/keychain
- **OAuth 流程**：回调服务器绑定 **`127.0.0.1`**，MCP 回调会**校验 `state` 参数防 CSRF**（[oauth-callback.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/mcp/oauth-callback.ts#L51-L102)），同时保存 `codeVerifier`（PKCE）
- **注入**：provider 层优先使用显式 auth override，否则从环境变量/配置解析 apiKey 并包装为 bearer（[auth-options.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/llm/src/route/auth-options.ts#L42-L55)）

---

### 四、服务端与插件

**服务端**：
- 默认绑定 **`127.0.0.1`**（[network.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/cli/network.ts#L12-L16)），默认不可远程访问
- 鉴权是 **HTTP Basic**，密码来自 `OPENCODE_SERVER_PASSWORD`（用户名默认 `opencode`）。未设置密码时**中间件直接透传、完全不鉴权**——安全性完全依赖「只监听 loopback」这个前提（[authorization.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/server/src/middleware/authorization.ts#L38-L57)）
- 凭证可来自 `Authorization: Basic` 头或 URL 查询参数 `auth_token`
- **CORS 白名单**（[cors.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/server/src/cors.ts#L11-L26)）：`http://localhost:*`、`http://127.0.0.1:*`、`oc://renderer`、Tauri 源、`*.opencode.ai`，外加配置 `cors` 白名单；无 Origin 时放行。`isAllowedRequestOrigin()` 额外允许同 host
- **PTY 连接的两段式防护**（[pty.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/server/src/handlers/pty.ts#L116-L157)）：因为 WebSocket 升级请求无法携带自定义头，改用 **ticket** 机制；发行 ticket 的接口要求自定义 header（**强制触发 CORS preflight**，从而让跨源浏览器页面无法绕过 origin 策略）+ `isAllowedRequestOrigin` 校验，消费时再校验 origin

**插件**：**无沙箱、无权限限制**。加载即 `await import(entry)`（[loader.ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/opencode/src/plugin/loader.ts#L139)），插件可执行任意代码、访问文件系统与网络。**信任模型 = 用户显式安装即完全信任**，这是当前架构最大的信任边界缺口。

**enterprise**：有 `SUPPORT_API_KEY` 保护的管理接口，用 `timingSafeEqual` + 长度预检**防时序攻击**，未通过返回 401（[[...path].ts](file:///c:/Users/27111/Documents/github_download/opencode/packages/enterprise/src/routes/api/%5B...path%5D.ts#L142-L155)）；其 `/api` 路由默认挂了通用 `cors()`。

---

### 风险提示（客观观察）

1. **bash 无命令解析**：危险命令拦截完全依赖用户配置的 pattern 规则，默认 `ask` 是唯一防线；仓库 `TODO` 明确承认这块是技术债
2. **插件零隔离**：第三方插件等同任意代码执行
3. **凭据明文落盘**：仅靠 `0o600` 文件权限，无加密
4. **服务端默认无鉴权**：一旦 `--hostname 0.0.0.0` 暴露且未设 `OPENCODE_SERVER_PASSWORD`，即为无认证开放
5. **`--auto` 自动批准**：只跳过 `ask`，显式 `deny` 仍生效（[permissions.mdx](file:///c:/Users/27111/Documents/github_download/opencode/packages/web/src/content/docs/permissions.mdx#L22-L38)）

全程只读调研，未修改任何项目文件。

---

