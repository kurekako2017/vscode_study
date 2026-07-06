# Root Cause

当前失败点是 `GEMINI_API_KEY` 本身无效，不是网络、TLS 或 DNS 问题。

已验证事实：

- `GEMINI_API_KEY` 存在，长度 `39`
- 前 6 位：`AIzaSy`
- 后 4 位：`nTOc`
- `GOOGLE_API_KEY` 未设置
- 直接调用 Gemini API 的 `models` 接口返回 `HTTP 400`
- 返回体包含 `reason: API_KEY_INVALID`

Roo 侧已确认事实：

- 当前 Roo 会话使用的 profile 名称是 `default`
- Roo 的 provider 配置不是明文存放在工作区目录里，而是通过 VS Code `context.secrets` 持久化
- Roo 代码中对应的 secret 存储键是 `roo_cline_config_api_config`
- Roo 的可见任务历史只记录 `apiConfigName=default`，没有把 `geminiApiKey` 明文写入任务文件

当前无法进一步证明的部分：

- 本机文件系统里没有找到可直接读取的 VS Code secret storage 文件
- 没有找到可直接导出 Roo `default` profile 中 `geminiApiKey` 明文的持久化文件
- 因此，当前无法从本地磁盘证据直接证明 Roo 实际发送的那把 key 的完整值

最小可证结论：

1. 当前 shell 里的 `GEMINI_API_KEY` 无效
2. Roo 的 `default` profile 已确认存在，但实际 `geminiApiKey` 值当前无法从本机文件系统直接取出
3. 现阶段唯一可执行修复仍然是重新生成 Google AI Studio Gemini API Key，并更新 Roo 的 Gemini 配置

# Evidence

- 环境变量检查：`GEMINI_API_KEY` 存在，`GOOGLE_API_KEY` 未设置
- Gemini API 直连测试：`https://generativelanguage.googleapis.com/v1beta/models?key=<GEMINI_API_KEY>` 返回 `HTTP 400`
- 返回错误：`API_KEY_INVALID`
- Roo 任务历史记录：当前会话 `apiConfigName=default`
- Roo 扩展实现：provider profile 通过 `context.secrets` 存储，secret key 为 `roo_cline_config_api_config`
- Roo 全局存储目录内容：只看到 `cache/`、`settings/`、`tasks/`，没有明文 `geminiApiKey` 文件
- VS Code Server 侧未找到可读的 `state.vscdb` / secret storage 文件

参考路径：

- `/home/victorkure/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/_index.json`
- `/home/victorkure/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/tasks/019f34b7-5879-7143-b7a3-73c3729fd211/history_item.json`
- `/home/victorkure/.vscode-server/extensions/rooveterinaryinc.roo-cline-3.54.0/dist/extension.js`
- `/home/victorkure/.vscode-server/data/logs/20260706T000938/exthost1/remoteexthost.log`
- `/home/victorkure/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/`

# Roo 实际使用 Key 验证

这一步目前只能验证到“存储位置”，不能验证到“明文 key 值”。

已验证：

- Roo 当前 session 使用 `default` profile
- Roo 的 profile 数据由 `context.secrets` 持久化
- Roo 的 secret key 名称是 `roo_cline_config_api_config`
- Roo 自己的 `globalStorage/rooveterinaryinc.roo-cline` 目录里没有可读明文 key

未能验证：

- `default` profile 内实际 `geminiApiKey` 的明文值
- Roo 实际发送到 Gemini API 的完整 key

因此，不能把“shell 里的 `GEMINI_API_KEY` 无效”自动等同于“Roo 必然用了同一把 key”，只能说：

1. shell key 已经被证明无效
2. Roo 的实际 key 当前不可从本机文件系统直接提取
3. 如果 Roo 仍然报 `API_KEY_INVALID`，就需要把 Roo 里保存的 Gemini key 更新成新的 Google AI Studio key

# Fix

唯一需要执行的动作：

1. 重新生成 Google AI Studio Gemini API Key
2. 更新 Roo `default` profile 中的 `geminiApiKey`
3. 如果 shell 也要直连测试，再同步更新 `GEMINI_API_KEY`
4. 重新测试 `curl`、Roo、VSCode

不要修改项目代码。
不要修改业务逻辑。
不要把 key 写进报告或日志。

# Verification

已完成的验证：

- `GEMINI_API_KEY`：存在
- `GOOGLE_API_KEY`：未设置
- Gemini `models` 接口：返回 `HTTP 400`
- 错误原因：`API_KEY_INVALID`
- Roo 当前会话：`default` profile
- Roo 配置存储方式：`context.secrets`

待新 key 到位后的验证：

1. 再跑一次同样的 `curl`，应返回 `200`
2. 在 Roo 里用 `default` profile 发一个最小请求，不应再出现 `API_KEY_INVALID`
3. VS Code / Roo 日志里不应再出现 Gemini 认证失败
