# Web Projects

`web-projects` 是 Web 学习、企业网站方案、前端示例、实战样板和 WordPress 插件相关内容的总目录。

## 先看这里

| 你想做什么 | 推荐入口 |
| --- | --- |
| 学 React / Vue / Angular / Next.js / TypeScript 最小项目 | [examples/README.md](examples/README.md) |
| 看前后端组合项目、企业站样板、Codespaces 模板 | [sample/README.md](sample/README.md) |
| 做日本企业官网、WordPress、报价、SEO、邮箱、域名配置 | [docs/](docs/) |
| 看 WordPress 插件或平台扩展代码 | [plugins/](plugins/) |
| 看部署脚本、onamae / headless 相关辅助脚本 | [deploy/](deploy/) |

## 目录说明

```text
web-projects/
  README.md       # 本文件，作为 web-projects 总入口
  examples/       # 框架最小 hello 示例
  sample/         # 更接近实战的组合项目和项目模板
  docs/           # 网站制作、WordPress、SEO、邮箱、报价、域名等文档
  plugins/        # WordPress 插件或平台扩展代码
  deploy/         # 部署、同步、上传相关脚本
```

一句话区分：

```text
examples 学单点技术，sample 学项目组合，docs 学建站方案，plugins 放扩展代码，deploy 放部署脚本。
```

## Examples 示例

`examples/` 偏“最小可运行项目”，用于学习单个框架或语言的启动方式。

| 项目 | 用途 |
| --- | --- |
| `react_hello` | React + Vite 基础示例，含 React 处理流程图 |
| `vue_hello` | Vue 3 + Vite 基础示例，含 Vue 处理流程图 |
| `angular_hello` | Angular standalone component 基础示例，含 Angular 处理流程图 |
| `next_hello` | Next.js Pages Router 基础示例，含 Next.js 处理流程图 |
| `typescript_hello` | Vanilla TypeScript + Vite 基础示例，含 TypeScript 处理流程图 |
| `headless-nextjs` | Next.js + Headless CMS / WordPress API 进阶示例 |

详细说明见：[examples/README.md](examples/README.md)

## Sample 项目

`sample/` 偏“实战样板”，用于学习前后端联调、企业站项目组织、Dev Container、部署准备等。

| 项目 | 用途 |
| --- | --- |
| `react-node-demo` | 最小 React + Express 前后端联调 demo |
| `react-node-template` | 本地 VS Code React + Node 开发模板 |
| `codespaces-react-node-template` | GitHub Codespaces / Dev Container 模板 |
| `company-website` | Next.js + Supabase 企业官网全栈样板 |
| `web-learning-site` | 企业官网学习路线和静态前端原型 |

详细说明见：[sample/README.md](sample/README.md)

## Docs 文档

`docs/` 是网站制作和业务方案文档集合。

### WordPress / 企业官网

- [WordPress 公司网站制作完全指南.md](docs/wordpress/WordPress%20公司网站制作完全指南.md)
- [WordPress Cocoon主题完全开发指南.md](docs/wordpress/WordPress%20Cocoon主题完全开发指南.md)
- [WordPress快速入门.md](docs/wordpress/WordPress快速入门.md)
- [WordPress Headless 开发完整流程（2026主流方案）.md](docs/wordpress/WordPress%20Headless%20开发完整流程（2026主流方案）.md)

### 日本企业网站方案

- [日本企业网站解决方案.md](docs/solutions/日本企业网站解决方案.md)
- [日本企业网站开发方案指南.md](docs/solutions/日本企业网站开发方案指南.md)
- [日本企业网站完整开发指南 🇯🇵.md](docs/solutions/日本企业网站完整开发指南%20🇯🇵.md)

### 教程

- [VS Code 静态网页快速教程.md](docs/tutorials/VS%20Code%20静态网页快速教程.md)
- [VS Code + Bootstrap + WordPress 后台建站教程.md](docs/tutorials/VS%20Code%20+%20Bootstrap%20+%20WordPress%20后台建站教程.md)
- [30分钟完成带联系表单的企业网站上线 .md](docs/tutorials/30分钟完成带联系表单的企业网站上线%20.md)

### 邮箱 / 域名 / SEO

- [邮件服务快速部署指南.md](docs/email/邮件服务快速部署指南.md)
- [邮件服务器部署与功能实现完整指南.md](docs/email/邮件服务器部署与功能实现完整指南.md)
- [域名和邮箱服务器配置指南.md](docs/domain/域名和邮箱服务器配置指南.md)
- [gk-fuji 域名跳转教程.md](docs/domain/gk-fuji-域名跳转教程.md)
- [SEO优化指南.md](docs/seo/SEO优化指南.md)
- [静态企业网站 SEO 检查与修改实操指南.md](docs/seo/静态企业网站%20SEO%20检查与修改实操指南.md)

### 报价 / 成本

- [网页制作 报价标准（通用版）.md](docs/quotes/网页制作%20报价标准（通用版）.md)
- [电商网站报价方案.md](docs/quotes/电商网站报价方案.md)
- [购物网站制作报价方案（通用版）.md](docs/quotes/购物网站制作报价方案（通用版）.md)
- [企業サイト制作 完全コスト比較 & 実例.md](docs/quotes/企業サイト制作%20完全コスト比較%20&%20実例.md)

## Plugins 是什么

这里的 `plugins/` 指平台扩展或插件代码，目前主要是 WordPress 插件：

- [plugins/ai-codex-agent/README.md](plugins/ai-codex-agent/README.md)

一句话理解：

```text
plugins = 给 WordPress、构建工具或平台增加能力的扩展模块。
```

注意：它和浏览器插件不是同一类东西。这里更接近“安装到 WordPress 或项目里的功能扩展”。

## Deploy 脚本

`deploy/` 存放部署和同步相关脚本：

- `export-and-upload.sh`：导出并上传相关资源。
- `setup-headless-onamae.sh`：Headless / onamae 相关部署初始化。
- `sync-staging-to-prod.sh`：从 staging 同步到 production 的辅助脚本。

使用脚本前建议先打开脚本确认变量、目标服务器和路径，避免误操作。

## 快速选择

| 学习阶段 | 建议 |
| --- | --- |
| 刚学前端 | 从 `examples/typescript_hello`、`examples/react_hello` 或 `examples/vue_hello` 开始 |
| 想理解前后端联调 | 看 `sample/react-node-demo` |
| 想用 VS Code 做全栈模板 | 看 `sample/react-node-template` |
| 想做企业官网 | 看 `sample/company-website` 和 `docs/wordpress/` |
| 想做日本客户网站方案 | 看 `docs/solutions/` 和 `docs/quotes/` |
| 想做 WordPress + AI 扩展 | 看 `plugins/ai-codex-agent` 和 `examples/headless-nextjs` |

## 常用命令

进入任一 Node 项目后通常可以使用：

```bash
npm install
npm run dev
npm run build
```

不同项目端口可能不同：

- Vite：常见 `http://localhost:5173`
- Next.js：常见 `http://localhost:3000`
- Express API：示例中常见 `http://localhost:4000`

具体以各项目 README 和终端输出为准。
