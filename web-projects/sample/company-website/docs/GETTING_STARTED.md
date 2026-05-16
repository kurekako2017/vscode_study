# 快速入门指南

欢迎使用公司网站项目！这个指南将帮助你快速上手并运行项目。

## 🎯 学习目标

完成本项目后，你将掌握：

1. ✅ **前端开发**：Next.js 14 + Tailwind CSS
2. ✅ **后端开发**：Supabase (PostgreSQL + Auth)
3. ✅ **全栈整合**：API 设计、数据流、状态管理
4. ✅ **部署运维**：Vercel + Cloudflare + 域名配置
5. ✅ **邮件系统**：Brevo 邮件发送 + 企业邮箱

## 📋 前置要求

### 必需软件

- **Node.js** 18+ ([下载](https://nodejs.org/))
- **pnpm** (推荐) 或 npm
  ```bash
  npm install -g pnpm
  ```
- **Git** ([下载](https://git-scm.com/))
- **VS Code** ([下载](https://code.visualstudio.com/))

### VS Code 扩展（推荐）

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets

### 云服务账号（免费）

- [Supabase](https://supabase.com) - 数据库和认证
- [Vercel](https://vercel.com) - 前端托管
- [Cloudflare](https://cloudflare.com) - DNS 和 CDN
- [Brevo](https://brevo.com) - 邮件发送

## 🚀 5 分钟快速启动

### 步骤 1: 克隆项目

```bash
cd web-projects/sample/company-website
```

### 步骤 2: 安装依赖

```bash
cd frontend
pnpm install
# 或使用 npm
# npm install
```

### 步骤 3: 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env.local
```

编辑 `.env.local`，暂时使用测试值：

```bash
# 暂时使用占位符（后面配置 Supabase 后替换）
NEXT_PUBLIC_SUPABASE_URL=https://placeholder.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=placeholder-key
BREVO_API_KEY=placeholder-key
CONTACT_EMAIL=info@example.com
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME=公司名称
```

### 步骤 4: 启动开发服务器

```bash
pnpm dev
```

访问 [http://localhost:3000](http://localhost:3000) 🎉

现在你应该能看到首页了！

## 📚 完整学习路径

### 第 1 天：前端基础

**目标**：理解 Next.js 和 Tailwind CSS

1. **阅读代码结构**
   - 浏览 `frontend/app/` 目录
   - 查看 `page.tsx`（首页）和 `layout.tsx`（布局）
   - 了解 `globals.css`（全局样式）

2. **修改首页内容**
   - 编辑 [app/page.tsx](../frontend/app/page.tsx)
   - 修改标题、描述、颜色
   - 保存后自动刷新（热重载）

3. **学习 Tailwind CSS**
   - 尝试修改 `className`
   - 参考 [Tailwind 文档](https://tailwindcss.com/docs)
   - 实践：改变按钮颜色、调整间距

4. **创建新页面**
   ```bash
   # 创建关于我们页面
   mkdir frontend/app/about
   touch frontend/app/about/page.tsx
   ```
   
   编写内容：
   ```tsx
   export default function AboutPage() {
     return (
       <div className="container py-20">
         <h1 className="text-4xl font-bold mb-6">关于我们</h1>
         <p className="text-lg text-gray-600">
           这里是公司介绍...
         </p>
       </div>
     )
   }
   ```

### 第 2 天：Supabase 数据库

**目标**：连接数据库，获取新闻数据

1. **创建 Supabase 项目**
   - 跟随 [backend/supabase/README.md](../backend/supabase/README.md)
   - 执行 `schema.sql` 创建数据表
   - 获取 URL 和 API Key

2. **更新环境变量**
   ```bash
   NEXT_PUBLIC_SUPABASE_URL=https://你的项目.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=你的密钥
   ```

3. **测试数据库连接**
   创建 `frontend/app/test-db/page.tsx`：
   ```tsx
   import { supabase } from '@/lib/supabase'

   export default async function TestDBPage() {
     const { data, error } = await supabase
       .from('news')
       .select('*')
       .limit(5)

     if (error) {
       return <div>错误: {error.message}</div>
     }

     return (
       <div className="container py-20">
         <h1 className="text-3xl font-bold mb-6">数据库测试</h1>
         <pre>{JSON.stringify(data, null, 2)}</pre>
       </div>
     )
   }
   ```

4. **显示新闻列表**
   - 创建 `frontend/app/news/page.tsx`
   - 从数据库获取新闻
   - 渲染列表

### 第 3 天：表单和邮件

**目标**：实现联系表单提交

1. **创建表单组件**
   ```tsx
   // frontend/components/ContactForm.tsx
   'use client'
   
   import { useState } from 'react'
   import { useForm } from 'react-hook-form'

   export default function ContactForm() {
     const { register, handleSubmit } = useForm()
     const [status, setStatus] = useState('')

     const onSubmit = async (data: any) => {
       setStatus('发送中...')
       const res = await fetch('/api/contact', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(data),
       })
       
       if (res.ok) {
         setStatus('提交成功！')
       } else {
         setStatus('提交失败，请重试')
       }
     }

     return (
       <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
         <input 
           {...register('name', { required: true })}
           placeholder="姓名"
           className="w-full px-4 py-2 border rounded"
         />
         <input 
           {...register('email', { required: true })}
           type="email"
           placeholder="邮箱"
           className="w-full px-4 py-2 border rounded"
         />
         <textarea 
           {...register('message', { required: true })}
           placeholder="留言"
           rows={5}
           className="w-full px-4 py-2 border rounded"
         />
         <button type="submit" className="btn-primary">
           提交
         </button>
         {status && <p>{status}</p>}
       </form>
     )
   }
   ```

2. **创建 API 路由**
   ```typescript
   // frontend/app/api/contact/route.ts
   import { supabase } from '@/lib/supabase'
   import { NextResponse } from 'next/server'

   export async function POST(request: Request) {
     const body = await request.json()
     
     // 保存到数据库
     const { error } = await supabase
       .from('contact_submissions')
       .insert([body])

     if (error) {
       return NextResponse.json(
         { error: error.message }, 
         { status: 500 }
       )
     }

     // TODO: 发送邮件通知

     return NextResponse.json({ success: true })
   }
   ```

3. **配置 Brevo 邮件**
   - 跟随 [docs/EMAIL_SETUP.md](EMAIL_SETUP.md)
   - 获取 API Key
   - 验证域名（生产环境）

### 第 4 天：管理后台

**目标**：创建简单的后台管理

1. **设置认证**
   - 使用 Supabase Auth
   - 创建登录页面
   - 保护后台路由

2. **新闻管理界面**
   - 列表页（查看所有新闻）
   - 创建页（发布新闻）
   - 编辑页（修改新闻）

3. **表单提交查看**
   - 显示所有提交
   - 标记为已读
   - 删除/归档

### 第 5 天：部署上线

**目标**：将项目部署到生产环境

1. **推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/company-website.git
   git push -u origin main
   ```

2. **部署到 Vercel**
   - 跟随 [docs/DEPLOYMENT.md](DEPLOYMENT.md)
   - 连接 GitHub 仓库
   - 配置环境变量
   - 一键部署

3. **配置域名**
   - 购买域名
   - 迁移到 Cloudflare
   - 绑定到 Vercel
   - 配置 SSL

4. **设置邮件服务**
   - 验证 SPF/DKIM/DMARC
   - 测试邮件发送
   - 配置企业邮箱

## 🔧 常用命令

```bash
# 开发
pnpm dev              # 启动开发服务器
pnpm build            # 构建生产版本
pnpm start            # 运行生产服务器
pnpm lint             # 代码检查

# 数据库
supabase start        # 启动本地 Supabase
supabase db push      # 推送数据库迁移
supabase db reset     # 重置数据库

# 部署
vercel               # 部署到 Vercel（预览）
vercel --prod        # 部署到生产环境
```

## 📖 推荐学习资源

### 官方文档
- [Next.js 文档](https://nextjs.org/docs)
- [React 文档](https://react.dev)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)
- [Supabase 文档](https://supabase.com/docs)

### 视频教程
- [Next.js 13+ 完整教程（中文）](https://www.bilibili.com/video/BV1...)
- [Tailwind CSS 从零开始](https://www.bilibili.com/video/BV1...)

### 实用工具
- [Tailwind Play](https://play.tailwindcss.com) - 在线测试 Tailwind
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples) - 官方示例

## 💡 学习技巧

1. **动手实践**：不要只看代码，要修改和运行
2. **小步迭代**：每完成一个小功能就测试
3. **阅读错误**：仔细阅读错误信息，大部分问题都有提示
4. **查文档**：遇到问题先查官方文档
5. **记录笔记**：记录遇到的问题和解决方案

## 🆘 遇到问题？

1. **检查控制台**：F12 打开开发者工具
2. **查看日志**：终端输出的错误信息
3. **环境变量**：确保 `.env.local` 配置正确
4. **清除缓存**：
   ```bash
   rm -rf .next
   pnpm dev
   ```

## 🎉 下一步

完成基础学习后，你可以：

1. **扩展功能**：
   - 添加搜索功能
   - 实现评论系统
   - 集成分析工具（Google Analytics）
   
2. **性能优化**：
   - 图片优化（Next.js Image）
   - 代码分割
   - 缓存策略

3. **进阶功能**：
   - 多语言支持（i18n）
   - PWA（Progressive Web App）
   - 服务端渲染（SSR）优化

祝学习愉快！🚀
