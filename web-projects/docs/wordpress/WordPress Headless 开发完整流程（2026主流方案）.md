(本文件已追加：来自上传图片的结构化转写内容。请核对下列条目，如需逐字原文或调整格式请告知。)

---

# WordPress Headless 开发完整流程（2026 主流方案）

## 1. 概览

- 目的：将 WordPress 作为内容后台（CMS），前端使用现代框架进行 Headless 开发，提高灵活性与性能。
- 适用场景：企业官网、内容型站点、营销页面、微前端场景。

## 2. 为什么选择 Headless WordPress

- 解耦：前后端分离，前端可使用 Next.js、Nuxt、Remix 等框架。
- 性能：前端可实现更好的缓存与静态化策略（ISR/SSG/SSR）。
- 体验：前端能实现更流畅的交互与现代化 UI。

## 3. 2026 年主流组件与版本（示例）

- WordPress: 最新长期支持版本或托管服务提供的稳定版
- PHP: 推荐 8.1+ 或 8.2
- 前端：Next.js（React）为首选，支持 App Router / Server Components
- 数据与 API：REST API 或 WPGraphQL

## 4. 两种常见 Headless 模式

1. 前后端完全分离（纯 Headless）
	 - WordPress 仅做内容管理与 API 提供
	 - 前端独立部署（Vercel / Netlify / 静态 CDN）

2. 部分混合（Hybrid/Decoupled）
	 - 仍保留部分 WordPress 前端渲染路径
	 - 用于兼容主题或插件场景

## 5. 常用插件与工具

- WPGraphQL（可选）
- WP REST API（内置）
- JWT Auth 或 OAuth 插件（用于认证）
- Headless CMS 辅助插件（如自定义 REST endpoints）

## 6. 前端架构建议（以 Next.js 为例）

- 使用 `app/` 路由与 Server Components 做 SSR/SSG
- 静态导出或 ISR：根据流量与更新频率选择
- 数据抓取：在 server-side 使用 `fetch` 或 GraphQL 客户端

示例：用 `fetch('/api/news')` 报错时需要使用完整服务端可识别的 URL 或在客户端请求。

## 7. 身份认证与表单提交

- 联系表单：建议使用后端 API（Edge Function / Serverless）处理并调用邮件服务（如 Brevo）
- 对接 WordPress：可通过自定义 REST endpoint 将数据写入 WP 或直接写入 Supabase 等后端

### 6.1 详细实现步骤（前端架构）

- 目录示例：

```
frontend/
├─ app/
│  ├─ layout.tsx
│  ├─ page.tsx
	├─ news/
	│  ├─ page.tsx       // Server Component 列表页
	│  └─ [slug]/page.tsx // Server Component 详情页
	└─ contact/
		 └─ page.tsx       // 标记为 Client Component 如需 useState
├─ components/
└─ lib/
	 └─ wpClient.ts       // 封装 WP REST / GraphQL 请求
```

- 推荐在服务端（Server Component / server action）使用环境变量存放后端 URL：

```js
// lib/wpClient.ts
export function wpFetch(path) {
	const base = process.env.WP_API_URL || 'https://cms.example.com';
	return fetch(new URL(path, base).toString(), { next: { revalidate: 60 } });
}
```

### 6.2 数据获取模式

- Server Component（推荐用于 SEO）：在 `page.tsx` 中直接调用 `wpFetch('/wp-json/wp/v2/posts')`，返回 HTML 渲染。
- Client Component（交互）：用 `fetch` 或 `swr` 在客户端拉取动态数据或表单提交。

示例：Server Component 获取新闻列表

```jsx
// app/news/page.tsx (Server Component)
import { wpFetch } from '@/lib/wpClient';
export default async function NewsPage() {
	const res = await wpFetch('/wp-json/wp/v2/posts');
	const posts = await res.json();
	return (
		<div>
			{posts.map(p => <article key={p.id}><h2>{p.title.rendered}</h2></article>)}
		</div>
	)
}
```

---

## 7. 身份认证与表单提交

- 联系表单：建议使用后端 API（Edge Function / Serverless）处理并调用邮件服务（如 Brevo）
- 对接 WordPress：可通过自定义 REST endpoint 将数据写入 WP 或直接写入 Supabase 等后端

### 7.1 联系表单 - 推荐实现流程

1. 前端：Contact 表单为 Client Component，提交到 Next.js API Route（或 Edge Function）。
2. 服务端：验证字段、执行防机器人验证（reCAPTCHA 或 hCaptcha）、写入数据库或转发到 WordPress 自定义 endpoint。
3. 发送通知：使用 Brevo / SendGrid 在服务端发送邮件通知。

示例：Next.js API Route（简化）

```js
// pages/api/contact.js 或 /app/api/contact/route.js
import fetch from 'node-fetch';

export async function POST(req) {
	const body = await req.json();
	// 校验
	if (!body.email || !body.message) return new Response('Bad Request', { status: 400 });

	// 可选：调用 WordPress 自定义 endpoint
	await fetch(process.env.WP_API_URL + '/wp-json/custom/v1/contact', {
		method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
	});

	// 发送邮件通知（示例：Brevo）
	await fetch('https://api.brevo.com/v3/smtp/email', {
		method: 'POST', headers: { 'Content-Type': 'application/json', 'api-key': process.env.BREVO_KEY },
		body: JSON.stringify({ to: [{ email: 'admin@example.com' }], subject: 'New contact', htmlContent: `<p>${body.message}</p>` })
	});

	return new Response(JSON.stringify({ ok: true }), { status: 200 });
}
```

### 7.2 用户认证（JWT / OAuth）

- 若前端需要登录对接 WP：推荐使用 JWT 插件（例如 `jwt-auth`）或使用 OAuth2 中介服务。
- 流程（JWT 简化）：
	1. 用户在前端提交账号密码到后端 API
	2. 后端向 WordPress 发起验证并获取 token
	3. 后端返回 token 给前端，前端把 token 存入 HttpOnly cookie 或 memory（注意 XSS/CSRF 风险）

示例：在服务端封装 `login` 调用并设置 cookie 的伪代码略。

---

## 8. 部署与托管建议

- 前端：Vercel / Netlify / Cloudflare Pages（支持 Next.js）
- 后端（WordPress）：传统主机、Managed WordPress、或 Docker 部署在云主机
- 静态资源与 CDN：使用 CDN 提速与缓存

### 8.1 前端部署（Vercel）快速步骤

1. 在 Vercel 上创建项目并连接 GitHub 仓库。
2. 设置环境变量：`WP_API_URL`、`BREVO_KEY`、其他私钥。
3. 部署分支（main）自动构建。

示例：GitHub Actions（构建 Next.js 并部署到 Vercel via CLI）

```yaml
name: Deploy Frontend
on: push
jobs:
	build:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Setup Node
				uses: actions/setup-node@v4
				with: node-version: 20
			- run: npm ci
			- run: npm run build
			- run: npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

### 8.2 WordPress 部署（Docker Compose）示例

```yaml
version: '3.8'
services:
	db:
		image: mysql:8
		environment:
			MYSQL_DATABASE: wordpress
			MYSQL_USER: wordpress
			MYSQL_PASSWORD: example
			MYSQL_ROOT_PASSWORD: example
	wordpress:
		image: wordpress:php8.1-apache
		ports:
			- '8080:80'
		environment:
			WORDPRESS_DB_HOST: db:3306
			WORDPRESS_DB_USER: wordpress
			WORDPRESS_DB_PASSWORD: example
			WORDPRESS_DB_NAME: wordpress
```

### 8.3 静态导出与同步（如需上传到传统主机）

- 使用 `next export` 生成静态文件，或用 `rsync`/FTP 上传到主机。

```bash
npm run build && npm run export
# rsync -avz out/ user@host:/var/www/html
```

---

完成展开并增加示例代码与部署模板。
## 9. SEO 与社交分享

- 在服务端（SSR/SSG）生成 meta、sitemap、Open Graph
- 对于动态内容，使用预渲染或 server-side rendering 保证爬虫抓取

## 10. 缓存策略

- 前端：ISR、CDN 缓存、Cache-Control
- 后端：缓存 API 响应、使用 Redis 等加速层

## 11. 安全性

- 对 API 进行鉴权与速率限制（Rate Limiting）
- 保护敏感环境变量（不要在前端暴露 API keys）
- 使用 HTTPS 与 CORS 控制

## 12. 常见问题与修复（图片中摘录）

- `/news` 页面在本地开发时可能出现 `Failed to parse URL from /api/news` 的错误：说明在 server-side 环境中使用了相对路径，需改为完整后端 URL 或在客户端调用。
- 在 App Router 中使用 `useState`/`useEffect` 的页面必须标记为 Client Component（在文件顶部添加 `"use client"`）。

## 13. 示例代码段（图片中示例）

```jsx
// 次示例展示了一个 client component 的写法
"use client"
import { useState } from 'react'

export default function Contact() {
	const [name, setName] = useState('')
	return (
		<form>
			<input value={name} onChange={e => setName(e.target.value)} />
		</form>
	)
}
```

## 14. 参考与下一步建议

- 校对并补充图片中可能的细节（如插件列表、配置示例、命令行示例）
- 我可以：
	- 将图片中每一段逐字原样转写到文档（如需）
	- 或按章节继续丰富（添加具体插件名称、代码片段、部署脚本）

---

*注：以上为从你上传图片整理的结构化 Markdown 摘要，已尽量保留图片原意并做小幅格式化便于阅读。若需要我将每一处文字按原样逐字保存到文档中，请回复“逐字”。*

