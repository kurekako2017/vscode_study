Headless Next.js 示例（最小）

这是一个最小的 Next.js 示例，用于演示如何从前端调用 WordPress 的 REST API（例如 `ai-codex-agent`）或 GraphQL（WPGraphQL）。

快速开始

1. 进入目录并安装依赖：

```bash
cd web-projects/examples/headless-nextjs
npm install
```

2. 创建 `.env.local` 并设置：

```
WP_API_URL=https://your-wordpress-site.com
WP_API_TOKEN= # 如果需要认证（可选）
```

3. 启动开发服务器：

```bash
npm run dev
```

说明

- `/pages/index.js`：示例页面，展示从 `ai-codex-agent` REST endpoint 获取生成内容的流程。前端演示包含一个简单的表单。
- `/pages/api/generate.js`：示例的 server-side 代理（BFF），将请求转发到 WordPress REST endpoint 并保护服务器端密钥。
