# 公司网站项目 - 低成本高质量企业主页解决方案

## 📋 项目概述

这是一个现代化的企业网站全栈项目，专注于低成本、高效率地构建精美的公司主页。

### 🎯 核心功能

- ✅ 响应式企业主页（首页、关于我们、服务、案例、联系）
- ✅ 新闻/博客系统（前台展示 + 后台管理）
- ✅ 表单提交（联系表单、订阅表单）
- ✅ 后台管理系统（新闻发布、表单查看、数据管理）
- ✅ SEO 优化（meta 标签、sitemap、robots.txt）
- ✅ 邮件发送（表单通知、新闻订阅）

### 💰 成本优化策略

| 服务 | 推荐方案 | 月成本 |
|------|---------|--------|
| 域名 | Cloudflare + 任意注册商 | ¥60-100/年 |
| 前端托管 | Vercel/Netlify 免费版 | ¥0 |
| 后端 + 数据库 | Supabase 免费版 | ¥0 |
| 邮件发送 | Brevo 免费版（300封/天） | ¥0 |
| 企业邮箱 | Cloudflare Email Routing + Gmail | ¥0 |
| CDN + SSL | Cloudflare 免费版 | ¥0 |
| **总计** | **首年** | **¥60-100/年** |

## 🛠️ 技术栈

### 前端
- **框架**: Next.js 14 (App Router)
- **样式**: Tailwind CSS + shadcn/ui
- **动画**: Framer Motion
- **表单**: React Hook Form + Zod
- **状态管理**: React Context / Zustand

### 后端
- **数据库 + 认证**: Supabase (PostgreSQL + Auth)
- **API**: Next.js API Routes / Supabase Edge Functions
- **文件存储**: Supabase Storage

### 部署
- **前端**: Vercel / Netlify
- **域名 DNS**: Cloudflare
- **邮件**: Brevo (SendinBlue) / Postmark
- **CI/CD**: GitHub Actions

## 📁 项目结构

```
company-website/
├── frontend/                 # Next.js 前端项目
│   ├── app/                 # App Router 页面
│   ├── components/          # React 组件
│   ├── lib/                 # 工具函数
│   └── public/              # 静态资源
├── backend/                 # 后端逻辑（可选独立服务）
│   ├── supabase/           # Supabase 配置和迁移
│   └── functions/          # Edge Functions
├── infrastructure/          # 基础设施配置
│   ├── terraform/          # IaC（可选）
│   └── docker/             # Docker 配置（本地开发）
├── docs/                   # 文档
│   ├── SETUP_GUIDE.md      # 安装指南
│   ├── DEPLOYMENT.md       # 部署指南
│   └── API.md              # API 文档
└── scripts/                # 自动化脚本
    ├── deploy.sh           # 部署脚本
    └── backup.sh           # 备份脚本
```

## 🚀 快速开始

### 前置要求

- Node.js 18+ 
- pnpm / npm / yarn
- Git
- Supabase 账号（免费）
- Vercel 账号（免费）

### 本地开发

```bash
# 1. 克隆项目
cd web-projects/sample/company-website

# 2. 安装前端依赖
cd frontend
pnpm install

# 3. 配置环境变量
cp .env.example .env.local
# 编辑 .env.local，填入 Supabase 配置

# 4. 运行开发服务器
pnpm dev
# 访问 http://localhost:3000
```

### 生产部署

查看 [DEPLOYMENT.md](docs/DEPLOYMENT.md) 获取完整部署指南。

## 📚 学习路径

### 阶段 1: 基础设置（1-2天）
1. [x] 创建项目结构
2. [ ] 配置 Next.js + Tailwind CSS
3. [ ] 设置 Supabase 项目
4. [ ] 配置域名和 Cloudflare

### 阶段 2: 前端页面（3-5天）
1. [ ] 首页（Hero、服务、案例、最新动态）
2. [ ] 关于我们 / 服务页面
3. [ ] 新闻列表 / 详情页
4. [ ] 联系页面（表单）

### 阶段 3: 后端功能（2-3天）
1. [ ] 新闻数据模型和 API
2. [ ] 表单提交处理
3. [ ] 邮件发送集成
4. [ ] 管理员认证

### 阶段 4: 管理后台（3-4天）
1. [ ] 管理员登录
2. [ ] 新闻 CRUD 功能
3. [ ] 表单提交查看
4. [ ] 基础数据统计

### 阶段 5: 部署上线（1-2天）
1. [ ] Vercel 部署配置
2. [ ] 域名和 SSL 配置
3. [ ] 邮件服务配置
4. [ ] 性能优化和测试

## 🔗 相关资源

- [Next.js 文档](https://nextjs.org/docs)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)
- [Supabase 文档](https://supabase.com/docs)
- [Vercel 部署指南](https://vercel.com/docs)
- [Cloudflare DNS 配置](https://developers.cloudflare.com/dns/)

## 📝 待办事项

查看 [TODO.md](TODO.md) 了解当前进度和待完成任务。

## 📄 许可证

MIT License - 自由使用和学习
