# 项目目录说明

## 📂 完整目录结构

```
web-projects/sample/company-website/
│
├── README.md                    # 项目总览和快速入门
├── TODO.md                      # 任务清单和开发进度
│
├── frontend/                    # Next.js 前端项目
│   ├── app/                     # App Router 页面和路由
│   │   ├── layout.tsx          # 全局布局（Header + Footer）
│   │   ├── page.tsx            # 首页
│   │   ├── globals.css         # 全局样式和 Tailwind
│   │   ├── about/              # 关于我们页面
│   │   ├── services/           # 服务页面
│   │   ├── news/               # 新闻列表和详情
│   │   ├── contact/            # 联系页面
│   │   ├── admin/              # 管理后台
│   │   └── api/                # API 路由
│   │       ├── contact/        # 联系表单 API
│   │       ├── news/           # 新闻 API
│   │       └── upload/         # 文件上传 API
│   │
│   ├── components/             # React 组件库
│   │   ├── Header.tsx          # 导航栏
│   │   ├── Footer.tsx          # 页脚
│   │   ├── Button.tsx          # 按钮组件
│   │   ├── Card.tsx            # 卡片组件
│   │   ├── ContactForm.tsx     # 联系表单
│   │   ├── NewsCard.tsx        # 新闻卡片
│   │   └── admin/              # 后台组件
│   │       ├── NewsEditor.tsx  # 新闻编辑器
│   │       ├── NewsTable.tsx   # 新闻列表
│   │       └── Dashboard.tsx   # 仪表盘
│   │
│   ├── lib/                    # 工具函数和配置
│   │   ├── supabase.ts        # Supabase 客户端
│   │   ├── email.ts           # 邮件发送工具
│   │   ├── utils.ts           # 通用工具函数
│   │   └── validations.ts     # 表单验证
│   │
│   ├── public/                 # 静态资源
│   │   ├── images/            # 图片
│   │   ├── fonts/             # 字体文件
│   │   └── favicon.ico        # 网站图标
│   │
│   ├── package.json           # 依赖管理
│   ├── tsconfig.json          # TypeScript 配置
│   ├── tailwind.config.js     # Tailwind CSS 配置
│   ├── next.config.js         # Next.js 配置
│   ├── .env.example           # 环境变量模板
│   └── .env.local             # 本地环境变量（不提交）
│
├── backend/                    # 后端逻辑（Supabase）
│   ├── supabase/              # Supabase 配置
│   │   ├── schema.sql         # 数据库架构
│   │   ├── seed.sql           # 初始数据
│   │   ├── migrations/        # 数据库迁移文件
│   │   └── README.md          # Supabase 配置指南
│   │
│   └── functions/             # Edge Functions（可选）
│       ├── send-email/        # 发送邮件函数
│       └── process-form/      # 表单处理函数
│
├── infrastructure/            # 基础设施配置
│   ├── terraform/            # IaC 配置（可选）
│   │   ├── main.tf
│   │   └── variables.tf
│   │
│   ├── docker/               # Docker 配置（本地开发）
│   │   ├── docker-compose.yml
│   │   └── Dockerfile
│   │
│   └── cloudflare/           # Cloudflare 配置
│       └── dns-config.txt    # DNS 记录模板
│
├── docs/                      # 文档
│   ├── GETTING_STARTED.md    # 快速入门（新手指南）
│   ├── DEPLOYMENT.md         # 部署指南
│   ├── EMAIL_SETUP.md        # 邮件系统配置
│   ├── API.md                # API 接口文档
│   └── ARCHITECTURE.md       # 架构设计文档
│
├── scripts/                   # 自动化脚本
│   ├── deploy.sh             # 一键部署脚本
│   ├── backup.sh             # 数据库备份脚本
│   ├── test-email.js         # 邮件测试脚本
│   └── setup-dev.sh          # 开发环境设置
│
└── .github/                   # GitHub 配置
    └── workflows/             # CI/CD 工作流
        ├── deploy.yml        # 自动部署
        └── test.yml          # 自动测试
```

## 🎯 主要目录说明

### `/frontend` - 前端项目

Next.js 应用的核心，包含所有前端代码：

- **`/app`**: 页面和路由（使用 App Router）
- **`/components`**: 可复用的 React 组件
- **`/lib`**: 工具函数、API 客户端、配置
- **`/public`**: 静态文件（图片、字体等）

### `/backend` - 后端配置

Supabase 相关配置和 Edge Functions：

- **`/supabase`**: 数据库架构、迁移、初始数据
- **`/functions`**: Serverless 函数（邮件、表单处理）

### `/infrastructure` - 基础设施

部署和运维相关配置：

- **`/terraform`**: 基础设施即代码（可选）
- **`/docker`**: 本地开发环境
- **`/cloudflare`**: DNS 和 CDN 配置

### `/docs` - 文档

完整的项目文档：

- **GETTING_STARTED.md**: 新手入门指南
- **DEPLOYMENT.md**: 生产环境部署
- **EMAIL_SETUP.md**: 邮件系统配置
- **API.md**: API 接口文档

### `/scripts` - 脚本

自动化工具：

- **deploy.sh**: 一键部署到生产环境
- **backup.sh**: 数据库自动备份
- **test-email.js**: 测试邮件发送

## 📄 重要文件说明

| 文件 | 作用 |
|------|------|
| `package.json` | 项目依赖和脚本 |
| `.env.local` | 本地环境变量（敏感信息，不提交） |
| `.env.example` | 环境变量模板（可提交） |
| `next.config.js` | Next.js 配置 |
| `tailwind.config.js` | Tailwind CSS 配置 |
| `tsconfig.json` | TypeScript 配置 |
| `schema.sql` | 数据库表结构 |

## 🚀 使用流程

1. **开始**：阅读 `README.md` 了解项目概览
2. **学习**：跟随 `docs/GETTING_STARTED.md` 学习
3. **开发**：在 `frontend/` 中编写代码
4. **测试**：在 `frontend/` 目录执行 `npm install` 然后运行 `npm run dev`（或使用你偏好的包管理器，但仓库示例使用 `npm`）
5. **部署**：参考 `docs/DEPLOYMENT.md` 上线

## 💡 开发建议

- **组件优先**：先在 `/components` 创建可复用组件
- **类型安全**：充分利用 TypeScript 类型定义
- **文档同步**：代码修改后更新相关文档
- **小步提交**：频繁 commit，清晰的 commit message
