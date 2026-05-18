# 后端实现方案完整指南

> 新闻发布与邮件表单功能的三种实现方案对比与详细步骤

## 📊 方案对比总览

| 项目 | 方案1：第三方服务 | 方案2：PocketBase | 方案3：Node.js 完整后端 |
|------|------------------|------------------|----------------------|
| **开发时间** | 10-30 分钟 | 1-2 小时 | 1-2 周 |
| **技术难度** | ⭐ 极简单 | ⭐⭐ 简单 | ⭐⭐⭐⭐ 复杂 |
| **月成本** | $0-5 | $0-7 | $5-20 |
| **可控性** | 低 | 中 | 高 |
| **学习价值** | 低 | 中高 | 极高 |
| **推荐场景** | 快速演示/MVP | 小型项目/学习 | 生产级应用 |

---

## 🚀 方案 1：第三方服务（最快速、最便宜）

**适合**：快速上线、MVP、演示项目、不想维护后端

### 成本分析
- **邮件**：Formspree 免费 50 次/月；Web3Forms 完全免费；Resend 免费 3000 次/月
- **新闻**：Contentful 免费（25k 记录）；Strapi Cloud 免费层；Sanity.io 免费（3 用户）
- **总成本**：$0/月（免费层足够小型网站）

### 1.1 邮件发送实现

#### 选项 A：Formspree（推荐新手）

**注册与配置**：
1. 访问 https://formspree.io/
2. 注册免费账户
3. 创建新表单，获得表单 ID（如 `abc123xyz`）

**前端代码修改**：
```javascript
// 在 script.js 的表单提交处理中替换
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(contactForm);
    
    try {
        const response = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (response.ok) {
            showMessage('邮件已发送！我们会尽快回复。', 'success');
            contactForm.reset();
        } else {
            throw new Error('发送失败');
        }
    } catch (error) {
        showMessage('发送失败，请稍后重试。', 'error');
    }
});
```

**优点**：
- 零配置，3 分钟上线
- 自动垃圾邮件过滤
- 提供提交记录管理界面

**缺点**：
- 免费版月限额 50 次
- 数据存储在第三方

---

#### 选项 B：Web3Forms（完全免费）

**注册与配置**：
1. 访问 https://web3forms.com/
2. 输入接收邮箱，获得 Access Key
3. 无需注册账户

**前端代码**：
```javascript
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(contactForm);
    formData.append('access_key', 'YOUR_ACCESS_KEY_HERE');
    
    try {
        const response = await fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('邮件已发送！', 'success');
            contactForm.reset();
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        showMessage('发送失败，请稍后重试。', 'error');
    }
});
```

**优点**：
- 完全免费，无限制
- 无需注册账户
- 支持文件上传

**缺点**：
- 无管理界面
- 需要自己处理验证码（推荐集成 hCaptcha）

---

#### 选项 C：Resend API（开发者友好）

**注册与配置**：
1. 访问 https://resend.com/
2. 注册账户，获取 API Key
3. 验证发送域名（测试可用 onboarding@resend.dev）

**需要简单后端**（Cloudflare Worker/Vercel Serverless）：

**前端代码**：
```javascript
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };
    
    try {
        const response = await fetch('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showMessage('邮件已发送！', 'success');
            contactForm.reset();
        } else {
            throw new Error('发送失败');
        }
    } catch (error) {
        showMessage('发送失败，请稍后重试。', 'error');
    }
});
```

**Cloudflare Worker 后端** (`/api/send-email`)：
```javascript
export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }
    
    const { name, email, message } = await request.json();
    
    const emailData = {
      from: 'contact@yourdomain.com',
      to: 'admin@yourdomain.com',
      subject: `新联系：${name}`,
      html: `
        <h2>来自网站的新联系</h2>
        <p><strong>姓名：</strong>${name}</p>
        <p><strong>邮箱：</strong>${email}</p>
        <p><strong>留言：</strong></p>
        <p>${message}</p>
      `
    };
    
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(emailData)
    });
    
    if (response.ok) {
      return new Response(JSON.stringify({ success: true }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } else {
      return new Response(JSON.stringify({ success: false }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};
```

**优点**：
- 免费 3000 封/月
- 开发者友好 API
- 送达率高

**缺点**：
- 需要简单后端（但 Cloudflare Worker 免费）

---

### 1.2 新闻发布实现

#### 选项 A：Contentful（推荐）

**注册与配置**：
1. 访问 https://www.contentful.com/
2. 注册免费账户（Community 版）
3. 创建 Space（空间）
4. 创建内容模型 "News"：
   - 标题（Title）：Short text
   - Slug：Short text
   - 摘要（Summary）：Long text
   - 正文（Body）：Rich text
   - 封面图（Cover）：Media
   - 发布时间（Published At）：Date and time

**获取 API 凭证**：
- Space ID：在设置中找到
- Content Delivery API - access token：在 API keys 中生成

**前端代码**（新闻列表页）：
```javascript
// 在页面加载时获取新闻
async function loadNews() {
    const SPACE_ID = 'your_space_id';
    const ACCESS_TOKEN = 'your_access_token';
    
    try {
        const response = await fetch(
            `https://cdn.contentful.com/spaces/${SPACE_ID}/entries?access_token=${ACCESS_TOKEN}&content_type=news&order=-fields.publishedAt&limit=10`
        );
        
        const data = await response.json();
        const newsList = document.querySelector('.news-list');
        newsList.innerHTML = '';
        
        data.items.forEach(item => {
            const article = document.createElement('article');
            article.className = 'news-item';
            article.innerHTML = `
                <time class="news-date">${new Date(item.fields.publishedAt).toLocaleDateString('ja-JP')}</time>
                <h3 class="news-title">${item.fields.title}</h3>
                <p class="news-summary">${item.fields.summary}</p>
            `;
            newsList.appendChild(article);
        });
    } catch (error) {
        console.error('新闻加载失败:', error);
    }
}

// 页面加载时执行
document.addEventListener('DOMContentLoaded', loadNews);
```

**发布新闻**：
1. 登录 Contentful 控制台
2. 在 Content 标签中点击 "Add entry"
3. 选择 "News" 类型
4. 填写内容并点击 "Publish"
5. 前端自动显示（刷新页面）

**优点**：
- 免费 25,000 条记录
- 强大的管理界面
- 支持版本控制和多语言

**缺点**：
- API 有学习曲线
- 需要前端对接

---

#### 选项 B：Strapi Cloud（一体化 CMS）

**注册与配置**：
1. 访问 https://strapi.io/cloud
2. 注册免费账户
3. 创建项目（Free 版）
4. 在 Content-Type Builder 中创建 "News" 集合：
   - title: Text
   - slug: Text (Unique)
   - summary: Text
   - content: Rich Text
   - cover: Media
   - publishedAt: DateTime

**API 设置**：
1. 在 Settings → Roles → Public 中
2. 允许 News 的 find 和 findOne 权限
3. 保存

**获取 API URL**：
- 在项目仪表板复制 API URL（如 `https://your-project.strapiapp.com`）

**前端代码**：
```javascript
async function loadNews() {
    const API_URL = 'https://your-project.strapiapp.com/api';
    
    try {
        const response = await fetch(`${API_URL}/news?sort=publishedAt:desc&pagination[limit]=10`);
        const result = await response.json();
        
        const newsList = document.querySelector('.news-list');
        newsList.innerHTML = '';
        
        result.data.forEach(item => {
            const { title, summary, publishedAt } = item.attributes;
            const article = document.createElement('article');
            article.className = 'news-item';
            article.innerHTML = `
                <time class="news-date">${new Date(publishedAt).toLocaleDateString('ja-JP')}</time>
                <h3 class="news-title">${title}</h3>
                <p class="news-summary">${summary}</p>
            `;
            newsList.appendChild(article);
        });
    } catch (error) {
        console.error('新闻加载失败:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadNews);
```

**发布新闻**：
1. 登录 Strapi 控制台
2. 在左侧菜单选择 "News"
3. 点击 "Create new entry"
4. 填写内容并点击 "Save" → "Publish"

**优点**：
- 一体化解决方案
- 优秀的管理界面
- 自动生成 REST 和 GraphQL API

**缺点**：
- 免费版性能有限
- 项目休眠策略（需定期访问）

---

### 1.3 快速部署步骤

**前端部署**（Cloudflare Pages/Vercel/Netlify）：

```bash
# 1. 安装 Cloudflare Wrangler（如果用 Cloudflare）
npm install -g wrangler

# 2. 登录
wrangler login

# 3. 创建 Pages 项目
wrangler pages project create company-website

# 4. 部署
cd /workspaces/study/web-learning-site/frontend
wrangler pages publish . --project-name=company-website

# 或使用 Git 集成（推荐）
# 1. 推送代码到 GitHub
# 2. 在 Cloudflare/Vercel/Netlify 连接 GitHub 仓库
# 3. 自动部署
```

**自定义域名**：
1. 在 Cloudflare/Vercel 添加自定义域名
2. 更新域名的 CNAME 记录指向提供的地址
3. 自动配置 SSL 证书

---

## 🐘 方案 2：PocketBase（轻量级完整后端）

**适合**：想学习后端但不想太复杂、小型项目、需要自主控制

### 成本分析
- **开发**：免费开源
- **托管**：Fly.io 免费 3 个应用；Railway $5/月；Render 免费层
- **数据库**：内置 SQLite，无需额外费用
- **总成本**：$0-5/月

### 2.1 本地开发设置

**下载 PocketBase**：
```bash
cd /workspaces/study/web-learning-site/backend

# Linux (x64)
wget https://github.com/pocketbase/pocketbase/releases/download/v0.22.0/pocketbase_0.22.0_linux_amd64.zip
unzip pocketbase_0.22.0_linux_amd64.zip
chmod +x pocketbase

# 启动
./pocketbase serve --http=0.0.0.0:8090
```

**首次访问**：
1. 浏览器打开 `http://localhost:8090/_/`
2. 创建管理员账户

### 2.2 数据建模

**创建 News 集合**：
1. 在管理界面点击 "New collection"
2. 类型选择 "Base"
3. 名称：`news`
4. 添加字段：
   - `title`（Text，必填）
   - `slug`（Text，必填，唯一）
   - `summary`（Text）
   - `content`（Editor，富文本）
   - `cover`（File，图片类型）
   - `published`（Bool，默认 false）
5. 在 API Rules 中设置：
   - List/View rule: `published = true`（公开已发布的）
   - Create/Update/Delete: `@request.auth.id != ""`（仅管理员）

**创建 Contacts 集合**：
1. 新建集合 `contacts`
2. 添加字段：
   - `name`（Text，必填）
   - `email`（Email，必填）
   - `company`（Text）
   - `phone`（Text）
   - `message`（Text，必填）
3. API Rules：
   - Create rule: `""` （任何人可创建，即提交表单）
   - List/View: `@request.auth.id != ""`（仅管理员查看）

### 2.3 前端集成

**安装 PocketBase JS SDK**：
```bash
cd /workspaces/study/web-learning-site/frontend
npm init -y
npm install pocketbase
```

**或使用 CDN**（无需构建工具）：
```html
<script type="module">
import PocketBase from 'https://cdn.jsdelivr.net/npm/pocketbase@0.21.0/+esm';

const pb = new PocketBase('http://localhost:8090');

// 新闻加载
async function loadNews() {
    try {
        const records = await pb.collection('news').getList(1, 10, {
            filter: 'published = true',
            sort: '-created'
        });
        
        const newsList = document.querySelector('.news-list');
        newsList.innerHTML = '';
        
        records.items.forEach(item => {
            const article = document.createElement('article');
            article.className = 'news-item';
            article.innerHTML = `
                <time class="news-date">${new Date(item.created).toLocaleDateString('ja-JP')}</time>
                <h3 class="news-title">${item.title}</h3>
                <p class="news-summary">${item.summary}</p>
            `;
            newsList.appendChild(article);
        });
    } catch (error) {
        console.error('加载失败:', error);
    }
}

// 联系表单提交
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        company: document.getElementById('company').value,
        phone: document.getElementById('phone').value,
        message: document.getElementById('message').value
    };
    
    try {
        await pb.collection('contacts').create(formData);
        showMessage('提交成功！我们会尽快回复。', 'success');
        contactForm.reset();
    } catch (error) {
        console.error('提交失败:', error);
        showMessage('提交失败，请稍后重试。', 'error');
    }
});

// 页面加载
document.addEventListener('DOMContentLoaded', loadNews);
</script>
```

### 2.4 邮件通知配置

**方式 A：使用 PocketBase 内置 SMTP**：
1. 在管理界面 Settings → Mail settings
2. 配置 SMTP：
   - SMTP server: `smtp.gmail.com`
   - Port: `587`
   - Username: 你的 Gmail
   - Password: 应用专用密码（非账号密码）
   - TLS: 启用

**方式 B：使用 Webhook + Resend API**：
1. 在 `contacts` 集合的 Settings → API hooks
2. 添加 After create hook：
```javascript
// 在 PocketBase 的 pb_hooks 目录创建 contacts.pb.js
onRecordAfterCreateRequest((e) => {
    const record = e.record;
    
    // 发送到 Resend API
    $http.send({
        url: "https://api.resend.com/emails",
        method: "POST",
        headers: {
            "Authorization": "Bearer YOUR_RESEND_API_KEY",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            from: "contact@yourdomain.com",
            to: "admin@yourdomain.com",
            subject: `新联系：${record.name}`,
            html: `
                <h2>来自网站的新联系</h2>
                <p><strong>姓名：</strong>${record.name}</p>
                <p><strong>邮箱：</strong>${record.email}</p>
                <p><strong>留言：</strong>${record.message}</p>
            `
        })
    });
}, "contacts");
```

### 2.5 生产环境部署

**Fly.io 部署**（免费 3 个应用）：

```bash
# 1. 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 2. 登录
flyctl auth login

# 3. 在 backend 目录创建 fly.toml
cd /workspaces/study/web-learning-site/backend
cat > fly.toml << 'EOF'
app = "your-company-site-backend"
primary_region = "nrt"  # Tokyo

[build]
  image = "ghcr.io/pocketbase/pocketbase:latest"

[env]
  PB_DATA_DIR = "/pb_data"

[[mounts]]
  source = "pb_data"
  destination = "/pb_data"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  
[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/api/health"
EOF

# 4. 创建应用
flyctl apps create your-company-site-backend

# 5. 创建持久化卷
flyctl volumes create pb_data --size 1 --region nrt

# 6. 部署
flyctl deploy

# 7. 获取 URL
flyctl info
```

**前端环境变量更新**：
```javascript
// 将 PocketBase URL 改为生产地址
const pb = new PocketBase('https://your-company-site-backend.fly.dev');
```

---

## ⚙️ 方案 3：Node.js + Express 完整后端

**适合**：深入学习、生产级应用、完全自主控制

### 成本分析
- **开发**：免费（开源工具）
- **托管**：Render 免费层；Railway $5/月；Fly.io $0-10/月
- **数据库**：Supabase 免费 500MB；Neon 免费 10GB
- **邮件**：Resend 免费 3000 封/月
- **总成本**：$0-15/月

### 3.1 项目初始化

```bash
cd /workspaces/study/web-learning-site/backend
npm init -y

# 安装依赖
npm install express cors dotenv
npm install @prisma/client resend
npm install -D prisma nodemon typescript @types/node @types/express ts-node

# 初始化 TypeScript
npx tsc --init

# 初始化 Prisma
npx prisma init
```

### 3.2 数据库设计（Prisma Schema）

**编辑 `prisma/schema.prisma`**：
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model News {
  id          String   @id @default(cuid())
  title       String
  slug        String   @unique
  summary     String?
  content     String
  coverUrl    String?
  published   Boolean  @default(false)
  publishedAt DateTime?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([published, publishedAt])
}

model Contact {
  id        String   @id @default(cuid())
  name      String
  email     String
  company   String?
  phone     String?
  message   String
  status    String   @default("new") // new, read, replied
  createdAt DateTime @default(now())

  @@index([status, createdAt])
}

model Admin {
  id           String   @id @default(cuid())
  email        String   @unique
  passwordHash String
  name         String
  createdAt    DateTime @default(now())
}
```

**环境变量 `.env`**：
```env
DATABASE_URL="postgresql://user:password@host:5432/dbname"
RESEND_API_KEY="re_xxx"
ADMIN_EMAIL="your@email.com"
JWT_SECRET="your-secret-key-change-this"
PORT=5000
```

**运行迁移**：
```bash
npx prisma migrate dev --name init
npx prisma generate
```

### 3.3 后端核心代码

**`src/index.ts`**：
```typescript
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import newsRouter from './routes/news';
import contactRouter from './routes/contact';
import adminRouter from './routes/admin';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// 路由
app.use('/api/news', newsRouter);
app.use('/api/contacts', contactRouter);
app.use('/api/admin', adminRouter);

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

**`src/routes/news.ts`**（新闻 API）：
```typescript
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

// 获取已发布新闻列表
router.get('/', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    
    const news = await prisma.news.findMany({
      where: { published: true },
      orderBy: { publishedAt: 'desc' },
      take: Number(limit),
      skip: (Number(page) - 1) * Number(limit),
      select: {
        id: true,
        title: true,
        slug: true,
        summary: true,
        coverUrl: true,
        publishedAt: true
      }
    });
    
    res.json({ data: news });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch news' });
  }
});

// 获取单条新闻
router.get('/:slug', async (req, res) => {
  try {
    const news = await prisma.news.findFirst({
      where: {
        slug: req.params.slug,
        published: true
      }
    });
    
    if (!news) {
      return res.status(404).json({ error: 'News not found' });
    }
    
    res.json({ data: news });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch news' });
  }
});

export default router;
```

**`src/routes/contact.ts`**（联系表单）：
```typescript
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import { Resend } from 'resend';

const router = Router();
const prisma = new PrismaClient();
const resend = new Resend(process.env.RESEND_API_KEY);

router.post('/', async (req, res) => {
  try {
    const { name, email, company, phone, message } = req.body;
    
    // 验证
    if (!name || !email || !message) {
      return res.status(400).json({ error: '缺少必填字段' });
    }
    
    // 存储到数据库
    const contact = await prisma.contact.create({
      data: { name, email, company, phone, message }
    });
    
    // 发送邮件通知
    await resend.emails.send({
      from: 'contact@yourdomain.com',
      to: process.env.ADMIN_EMAIL!,
      subject: `新联系：${name}`,
      html: `
        <h2>来自网站的新联系</h2>
        <p><strong>姓名：</strong>${name}</p>
        <p><strong>邮箱：</strong>${email}</p>
        <p><strong>公司：</strong>${company || '未提供'}</p>
        <p><strong>电话：</strong>${phone || '未提供'}</p>
        <p><strong>留言：</strong></p>
        <p>${message}</p>
      `
    });
    
    res.json({ success: true, id: contact.id });
  } catch (error) {
    console.error('Contact submission error:', error);
    res.status(500).json({ error: '提交失败' });
  }
});

export default router;
```

### 3.4 管理后台（简化版）

**`src/routes/admin.ts`**：
```typescript
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import jwt from 'jsonwebtoken';

const router = Router();
const prisma = new PrismaClient();

// 认证中间件
const auth = (req: any, res: any, next: any) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// 创建新闻
router.post('/news', auth, async (req, res) => {
  try {
    const news = await prisma.news.create({
      data: req.body
    });
    res.json({ data: news });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create news' });
  }
});

// 更新新闻
router.put('/news/:id', auth, async (req, res) => {
  try {
    const news = await prisma.news.update({
      where: { id: req.params.id },
      data: req.body
    });
    res.json({ data: news });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update news' });
  }
});

// 删除新闻
router.delete('/news/:id', auth, async (req, res) => {
  try {
    await prisma.news.delete({
      where: { id: req.params.id }
    });
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete news' });
  }
});

// 查看联系记录
router.get('/contacts', auth, async (req, res) => {
  try {
    const contacts = await prisma.contact.findMany({
      orderBy: { createdAt: 'desc' }
    });
    res.json({ data: contacts });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch contacts' });
  }
});

export default router;
```

### 3.5 部署到 Render

**创建 `render.yaml`**：
```yaml
services:
  - type: web
    name: company-website-backend
    env: node
    plan: free
    buildCommand: npm install && npx prisma generate && npx prisma migrate deploy && npm run build
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: RESEND_API_KEY
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: ADMIN_EMAIL
        sync: false
```

**部署步骤**：
1. 推送代码到 GitHub
2. 在 Render.com 创建账户
3. 连接 GitHub 仓库
4. 选择 `backend` 目录
5. 添加环境变量
6. 点击部署

---

## 📋 总结与建议

### 最快上线路径（推荐新手）
1. **邮件**：Web3Forms（5 分钟）
2. **新闻**：Contentful（15 分钟）
3. **部署**：Cloudflare Pages（5 分钟）
4. **总时间**：25 分钟，成本 $0/月

### 学习价值最高路径
1. **后端**：PocketBase（2 小时）
2. **前端集成**：PocketBase JS SDK（1 小时）
3. **部署**：Fly.io（30 分钟）
4. **总时间**：3.5 小时，成本 $0-5/月

### 生产级完整路径
1. **后端**：Node.js + Express + Prisma（1 周）
2. **管理后台**：React Admin（3 天）
3. **部署与 CI/CD**：Render + GitHub Actions（1 天）
4. **总时间**：10-14 天，成本 $5-15/月

### 下一步行动
选定方案后：
1. 按照对应章节的步骤执行
2. 测试功能完整性
3. 配置生产环境
4. 设置监控与备份
5. 编写运维文档

需要我帮你实现具体哪个方案的代码？
