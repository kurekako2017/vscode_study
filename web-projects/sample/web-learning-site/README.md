# 企业官网全栈开发实战项目

> 系统化学习现代 Web 开发：从前端到后端、从开发到部署、从性能优化到安全加固的完整工程实践

## 🎯 项目目标

构建一个**生产级企业官网系统**，涵盖：
- 高性能响应式前端（Lighthouse 90+ 分）
- RESTful API 后端与内容管理系统
- 数据库设计、迁移与备份
- 邮件服务集成（SMTP/API）
- CI/CD 自动化部署
- 监控、日志与告警体系
- 安全加固（HTTPS/CSP/CORS/限流/CSRF）
- 域名、DNS、SSL 证书管理
- SEO 优化与网站分析

## 📁 项目架构

```
web-learning-site/
├── frontend/               # 前端应用（静态或 SSR）
│   ├── public/            # 静态资源（图片/字体/favicon）
│   ├── src/               # 源代码
│   │   ├── components/    # 可复用组件
│   │   ├── pages/         # 页面
│   │   ├── styles/        # 样式（全局/主题）
│   │   ├── utils/         # 工具函数
│   │   └── api/           # API 调用封装
│   ├── tests/             # 单元与集成测试
│   └── package.json       # 依赖与脚本
│
├── backend/               # 后端 API 与管理系统
│   ├── src/
│   │   ├── controllers/   # 路由控制器
│   │   ├── models/        # 数据模型（ORM/ODM）
│   │   ├── services/      # 业务逻辑
│   │   ├── middleware/    # 中间件（鉴权/日志/限流）
│   │   ├── config/        # 配置管理
│   │   └── utils/         # 工具库
│   ├── migrations/        # 数据库迁移脚本
│   ├── tests/             # API 测试
│   ├── .env.example       # 环境变量模板
│   └── package.json
│
├── infra/                 # 基础设施即代码
│   ├── docker/            # Docker 配置
│   ├── terraform/         # Terraform IaC（可选）
│   ├── deployment/        # 部署脚本与配置
│   └── monitoring/        # 监控配置（Prometheus/Grafana）
│
├── docs/                  # 项目文档
│   ├── architecture.md    # 架构设计文档
│   ├── api-spec.md        # API 接口规范
│   ├── deployment.md      # 部署指南
│   ├── runbook.md         # 运维手册
│   └── security.md        # 安全策略
│
└── scripts/               # 自动化脚本
    ├── setup.sh           # 环境初始化
    ├── backup.sh          # 数据备份
    └── health-check.sh    # 健康检查
```

## 🎨 技术选型对比

### 前端方案

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **Next.js** | SSR/SSG 灵活、SEO 友好、React 生态、Vercel 部署 | 学习曲线、打包体积 | 需要 SEO、动态内容 |
| **Astro** | 超快速度、零 JS 默认、多框架兼容 | 生态较小、动态能力弱 | 内容为主的站点 |
| **纯静态** | 简单直接、兼容性最好 | 无框架、维护性差 | 快速原型、学习基础 |

### 后端方案

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **Strapi** | 开箱即用 CMS、管理界面、权限系统 | 笨重、自定义受限 | 快速上线、标准 CMS 需求 |
| **PocketBase** | 单二进制、内置认证、实时订阅 | Go 生态、功能有限 | 小型项目、快速迭代 |
| **Express + Prisma** | 灵活可控、生态丰富、类型安全 | 需要自建一切 | 深度定制、学习完整后端 |
| **Nest.js** | 企业级架构、TypeScript、模块化 | 复杂度高 | 大型项目、团队协作 |

### 数据库选择

| 数据库 | 优势 | 劣势 | 推荐服务 |
|--------|------|------|----------|
| **PostgreSQL** | 功能强大、开源、扩展丰富 | 需要托管 | Supabase/Neon/Render |
| **SQLite** | 零配置、单文件、快速 | 并发受限 | 开发/演示 |
| **MySQL** | 普及度高、兼容性好 | 特性不如 PG | PlanetScale |

## 🚀 分阶段实施计划

### Phase 1: 基础前端（1-2 周）
- [x] 静态 HTML/CSS/JS 原型
- [ ] 组件化改造（选定框架）
- [ ] 响应式布局完善（移动端）
- [ ] 可访问性优化（ARIA/键盘导航）
- [ ] Lighthouse 测试达标（90+）

### Phase 2: 后端基础（2-3 周）
- [ ] 技术选型与项目初始化
- [ ] 数据库设计（ER 图、迁移脚本）
- [ ] RESTful API 开发
  - [ ] 新闻 CRUD（GET/POST/PUT/DELETE）
  - [ ] 联系表单提交与存储
  - [ ] 认证与授权（JWT/Session）
- [ ] API 文档（OpenAPI/Swagger）
- [ ] 单元测试与集成测试

### Phase 3: 前后端集成（1-2 周）
- [ ] API 客户端封装
- [ ] 新闻列表与详情页动态化
- [ ] 联系表单异步提交
- [ ] 错误处理与加载状态
- [ ] 环境变量管理（dev/staging/prod）

### Phase 4: 邮件与通知（1 周）
- [ ] SMTP 配置或 API 服务集成
- [ ] 邮件模板设计
- [ ] 联系表单邮件通知
- [ ] 异常邮件告警（可选）
- [ ] SPF/DKIM/DMARC 配置

### Phase 5: 管理后台（2-3 周）
- [ ] 管理界面框架（React Admin/自建）
- [ ] 登录页与会话管理
- [ ] 新闻管理界面（列表/编辑/发布）
- [ ] Markdown 编辑器集成
- [ ] 图片上传与管理（S3/本地）
- [ ] 联系记录查看与导出（CSV）
- [ ] 权限与角色管理（可选）

### Phase 6: 部署与 DevOps（1-2 周）
- [ ] Docker 容器化
- [ ] CI/CD 流水线（GitHub Actions）
- [ ] 前端部署（Vercel/Netlify/Cloudflare Pages）
- [ ] 后端部署（Render/Fly/Railway）
- [ ] 数据库迁移自动化
- [ ] 环境变量与密钥管理
- [ ] 域名与 DNS 配置
- [ ] SSL 证书（Let's Encrypt/Cloudflare）

### Phase 7: 监控与运维（1 周）
- [ ] 健康检查端点
- [ ] 日志聚合（Winston/Pino → Logtail）
- [ ] 错误追踪（Sentry）
- [ ] 性能监控（New Relic/Datadog）
- [ ] 存活监测（Uptime Kuma/Better Stack）
- [ ] 数据库备份自动化

### Phase 8: 安全加固（1 周）
- [ ] HTTPS 强制与 HSTS
- [ ] CSP 头配置
- [ ] CORS 策略
- [ ] 限流与防刷（rate-limit-redis）
- [ ] CSRF 防护
- [ ] 输入验证与清理
- [ ] SQL 注入与 XSS 防护
- [ ] 依赖安全扫描（npm audit/Snyk）

### Phase 9: 性能优化（1 周）
- [ ] 图片优化（WebP/AVIF、懒加载）
- [ ] 代码分割与按需加载
- [ ] CDN 配置与缓存策略
- [ ] 数据库查询优化（索引/N+1）
- [ ] 静态资源压缩（Gzip/Brotli）
- [ ] 预加载与预连接
- [ ] Service Worker（PWA 可选）

### Phase 10: SEO 与分析（1 周）
- [ ] 元标签完善（title/description/OG）
- [ ] 结构化数据（schema.org）
- [ ] sitemap.xml 与 robots.txt
- [ ] 网站分析（Google Analytics/Plausible）
- [ ] 搜索引擎提交（Google/Bing）
- [ ] 页面速度优化
- [ ] Core Web Vitals 达标

## 📊 质量标准

### 性能指标
- Lighthouse Performance: ≥ 90
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
- Time to Interactive (TTI): < 3.8s

### 可访问性
- WCAG 2.1 AA 级别
- Lighthouse Accessibility: ≥ 90
- 键盘导航完整支持
- 屏幕阅读器兼容

### SEO
- Lighthouse SEO: ≥ 90
- 移动友好测试通过
- 结构化数据验证通过
- Core Web Vitals 良好

### 安全性
- HTTPS 强制
- 安全头评分 A+（securityheaders.com）
- 无高危依赖漏洞
- OWASP Top 10 防护

## 🛠️ 开发环境设置

### 前置要求
- Node.js 18+ / Python 3.10+ / Go 1.21+（根据后端选择）
- Git
- Docker & Docker Compose（可选）
- PostgreSQL 客户端（psql）或 MySQL 客户端

### 快速启动

```bash
# 1. 克隆项目
git clone <repo-url>
cd web-learning-site

# 2. 前端设置
cd frontend
npm install
npm run dev  # 默认 http://localhost:3000

# 3. 后端设置（另一终端）
cd backend
cp .env.example .env  # 编辑环境变量
npm install
npm run migrate       # 数据库迁移
npm run dev          # 默认 http://localhost:5000

# 4. 测试
npm test             # 运行测试套件
```

### Docker 启动（推荐）

```bash
docker-compose up -d
# 前端: http://localhost:3000
# 后端: http://localhost:5000
# 数据库: localhost:5432
```

## 📚 学习资源

- **前端**：MDN Web Docs、React 官方文档、Next.js Learn
- **后端**：Node.js 最佳实践、Express 官方指南、Prisma 文档
- **数据库**：PostgreSQL 教程、Use The Index Luke（索引优化）
- **DevOps**：The Twelve-Factor App、Docker 官方文档
- **安全**：OWASP Cheat Sheet、Web Security Academy

## 🔗 相关文档

- [详细学习路线](../docs/specs/company-website-learning-plan.md)
- [前端实现说明](frontend/README.md)
- [API 接口文档](docs/api-spec.md)
- [部署指南](docs/deployment.md)
- [运维手册](docs/runbook.md)

## 💡 下一步行动

1. **确定技术栈**：根据学习目标与项目规模选择合适的前后端方案
2. **搭建开发环境**：安装依赖、配置 IDE、设置 Git hooks
3. **设计数据模型**：绘制 ER 图，编写迁移脚本
4. **API 优先开发**：先定义接口规范，再实现前后端
5. **持续集成**：从第一天起就配置 CI/CD 和自动化测试

## 📈 项目里程碑

- [ ] MVP 完成（基础前台 + 静态内容）
- [ ] 后台管理可用（新闻发布流程跑通）
- [ ] 生产环境部署（域名、HTTPS、监控）
- [ ] 性能与安全达标（Lighthouse 90+、安全头 A+）
- [ ] 文档完善（API 文档、部署文档、运维手册）
