# OpenClaw 在 Win11 + WSL 的安装配置教程

> 适用场景：你已经在 Win11 上装了 WSL，准备把 OpenClaw 跑起来，并通过 Web 控制台或 Telegram 这类通道实际使用。

---

## 1. 整体架构先看懂

这套环境里有两层：

- Windows：负责浏览器访问 `http://127.0.0.1:18789`
- WSL：实际运行 `openclaw gateway`

最关键的结论是：

- 真正生效的 OpenClaw 配置通常在 WSL 里
- 浏览器只是控制台
- `Gateway token` 和模型 API Key 不是一回事

---

## 2. 推荐安装方式

在 WSL 里安装 OpenClaw：

```bash
npm install -g openclaw
openclaw --version
```

如果要用浏览器控制台，建议本地模式运行：

```bash
openclaw gateway --port 18789
```

浏览器访问：

```text
http://127.0.0.1:18789
```

---

## 3. 配置文件在哪里

WSL 里最重要的配置文件通常是：

```text
~/.openclaw/openclaw.json
```

常用的几类配置都在这里：

- 模型
- 通道
- gateway token
- workspace

---

## 4. 先区分 3 种常见凭据

### 4.1 模型 API Key

例如：

- `GEMINI_API_KEY`
- `OPENAI_API_KEY`

这是给模型平台用的。

### 4.2 Gateway token

例如：

```text
gateway.auth.token
```

这是 OpenClaw 控制台连本地 gateway 时用的。

### 4.3 渠道 token

例如：

- Telegram bot token
- 企业微信 token

这是聊天通道自己用的，不等于 gateway token，也不等于模型 API Key。

---

## 5. 现有配置界面里每个 section 是干什么的

如果你执行：

```bash
openclaw configure
```

看到的是已有配置界面，一般会有这些 section：

- `Workspace`
- `Model`
- `Web tools`
- `Gateway`
- `Channels`
- `Skills`

最常用的是：

- `Model`：改模型供应商、模型名、API Key
- `Gateway`：改本地网关模式、地址、token
- `Channels`：接 Telegram、WhatsApp 等通道

---

## 6. Gemini 免费方案怎么配

如果你优先使用 Gemini 免费方案，建议先在 WSL 里设置环境变量：

```bash
export GEMINI_API_KEY="你的_Gemini_API_Key"
echo 'export GEMINI_API_KEY="你的_Gemini_API_Key"' >> ~/.bashrc
source ~/.bashrc
```

然后在 `Model` 里配置：

- Provider: `gemini` 或 `google`
- Model: `gemini-2.5-flash`
- API Key: 你的 Gemini Key

如果支持环境变量，也可以直接走环境变量而不是明文写入。

---

## 7. Gateway 怎么配

推荐本地模式：

- `gateway.mode = local`
- WebSocket URL: `ws://127.0.0.1:18789`
- Auth: `token`

如果控制台报认证错误，优先检查：

- `gateway.auth.token`
- `gateway.remote.token`

这两个值最好保持一致。

---

## 8. Telegram 怎么接

Telegram 不走扫码登录，而是直接配置 bot token。

先去 `@BotFather` 创建机器人，拿到类似这样的 token：

```text
1234567890:AA...
```

然后在配置里写：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "1234567890:AA...",
      "dmPolicy": "open",
      "allowFrom": ["*"],
      "groupPolicy": "disabled",
      "streaming": "partial"
    }
  }
}
```

说明：

- `botToken` 字段名要写对
- 不是 `token`
- `dmPolicy = "open"` + `allowFrom = ["*"]` 更适合刚开始联通测试

改完后重启 gateway。

---

## 9. 浏览器里连不上时怎么查

如果看到这些错误：

- `unauthorized`
- `gateway token mismatch`
- `gateway token missing`
- `Version n/a`

优先排查：

1. WSL 里的 gateway 是否在跑
2. 浏览器控制台是否带了正确 token
3. `gateway.auth.token` 和 `gateway.remote.token` 是否一致
4. 浏览器是否缓存了旧 token

---

## 10. 当前最稳的最小可用方案

如果你只是想先跑通一套可用环境，建议用下面组合：

- OpenClaw 跑在 WSL
- 模型先用 Gemini 免费方案
- 通道先用 Telegram
- 浏览器通过 `127.0.0.1:18789` 控制台管理

这是目前最稳、最容易成功的方案。

---

## 11. 推荐的后续阅读顺序

后面建议按这个顺序继续看：

1. [OpenClaw 实用使用教程](./OpenClaw_实用使用教程.md)
2. [OpenClaw 本地模型与自动切换教程](./OpenClaw_本地模型与自动切换教程.md)
