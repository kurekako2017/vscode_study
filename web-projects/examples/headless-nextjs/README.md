# Headless Next.js 示例（最小）

这是一个最小的 Next.js 示例，用于演示如何从前端调用 WordPress 的 REST API（例如 `ai-codex-agent`）或 GraphQL（WPGraphQL）。

## 暂时定位

当前目录暂时保留在 `web-projects/examples/headless-nextjs`，用途是和 `next_hello` 形成对照：

- `next_hello`：Next.js 基础 hello，重点看页面、全局样式和框架启动方式。
- `headless-nextjs`：Next.js 进阶场景，重点看前端如何通过 API / CMS 获取内容。

后续如果这个示例继续扩展到完整的 CMS、GraphQL、认证、缓存、部署等内容，可以再考虑移动到 `web-projects/headless-nextjs/` 或单独的实战目录。

## plugins 是什么

在本示例语境里，`plugins` 一般指给框架、构建工具或 CMS 增加能力的模块。

- 在 Next.js 中，插件可能用于图片处理、Bundle 分析、国际化、PWA、MDX 等。
- 在 WordPress / Headless CMS 中，插件可能提供 REST API 扩展、GraphQL 接口、认证、内容字段管理等能力。
- 在 Vite / Vue / React 示例中，插件通常用于让构建工具识别框架文件、启用开发调试或扩展构建能力。

一句话理解：

```text
plugins = 不改框架核心代码，而是给框架或工具追加能力的扩展模块。
```

## 快速开始

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

## 说明

- `/pages/index.js`：示例页面，展示从 `ai-codex-agent` REST endpoint 获取生成内容的流程。前端演示包含一个简单的表单。
- `/pages/api/generate.js`：示例的 server-side 代理（BFF），将请求转发到 WordPress REST endpoint 并保护服务器端密钥。
