# 部署指南 - 低成本全栈部署方案

## 🎯 部署架构

```
用户浏览器
    ↓
Cloudflare (DNS + CDN + SSL)
    ↓
Vercel (Next.js 前端)
    ↓
Supabase (数据库 + Auth + Storage)
    ↓
Brevo (邮件服务)
```

## 📋 部署清单

### 第一步：域名配置 (Cloudflare)

#### 1.1 购买域名

**推荐注册商**：
- 阿里云（万网）
- Cloudflare Registrar（最便宜）
- GoDaddy
- Namecheap

**成本**：¥60-100/年（.com 域名）

#### 1.2 添加到 Cloudflare

1. 注册 [Cloudflare](https://dash.cloudflare.com) 账号
2. 点击 "Add a Site"，输入域名
3. 选择 **Free 套餐**
4. 复制 Cloudflare 提供的 DNS 服务器地址（如 `ava.ns.cloudflare.com`）
5. 在域名注册商处修改 DNS 服务器为 Cloudflare 的地址
6. 等待 DNS 生效（24-48小时，通常几分钟）

#### 1.3 配置 SSL

Cloudflare 免费提供：
- SSL/TLS 加密模式：选择 **Full (strict)**
- 自动 HTTPS 重写：**开启**
- Always Use HTTPS：**开启**

### 第二步：前端部署 (Vercel)

#### 2.1 连接 GitHub

1. 将代码推送到 GitHub 仓库
```bash
cd web-projects/company-website
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/company-website.git
git push -u origin main
```

2. 访问 [Vercel Dashboard](https://vercel.com)
3. 点击 "Import Project"
4. 选择你的 GitHub 仓库

#### 2.2 配置构建设置

- **Framework Preset**: Next.js
- **Root Directory**: `frontend`
- **Build Command**: `pnpm build` (或 `npm run build`)
- **Output Directory**: `.next`

#### 2.3 添加环境变量

在 Vercel 项目设置中添加：
```
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
BREVO_API_KEY=xkeysib-...
CONTACT_EMAIL=info@yourdomain.com
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

#### 2.4 部署

点击 "Deploy" - Vercel 会自动构建和部署
部署完成后获得：
- **预览 URL**: `https://company-website-xxx.vercel.app`
- 每次推送代码自动重新部署

#### 2.5 绑定自定义域名

1. 在 Vercel 项目设置中点击 "Domains"
2. 添加你的域名（如 `www.yourdomain.com`）
3. Vercel 会提供 DNS 记录配置指引
4. 回到 Cloudflare DNS 设置，添加记录：
   ```
   类型: CNAME
   名称: www (或 @)
   目标: cname.vercel-dns.com
   代理状态: 已代理（橙色云朵）
   ```
5. 等待 DNS 生效（几分钟）

### 第三步：数据库配置 (Supabase)

参考 [backend/supabase/README.md](../backend/supabase/README.md)

关键步骤：
1. ✅ 创建 Supabase 项目
2. ✅ 执行 schema.sql 迁移
3. ✅ 配置 RLS 策略
4. ✅ 创建 Storage bucket
5. ✅ 添加第一个管理员用户

### 第四步：邮件服务 (Brevo)

#### 4.1 注册 Brevo（免费版）

1. 访问 [Brevo](https://www.brevo.com)（前身为 SendinBlue）
2. 注册账号（免费版：300封邮件/天）
3. 进入 Dashboard

#### 4.2 验证发件域名

1. 点击 "Senders & IP"
2. 点击 "Domains" → "Add a Domain"
3. 输入你的域名（如 `yourdomain.com`）
4. Brevo 会提供 DNS 记录（SPF、DKIM、DMARC）
5. 在 Cloudflare DNS 中添加这些记录：

```
类型: TXT
名称: @
内容: v=spf1 include:spf.sendinblue.com ~all

类型: TXT
名称: mail._domainkey
内容: [Brevo提供的DKIM值]

类型: TXT
名称: _dmarc
内容: v=DMARC1; p=none; rua=mailto:your@email.com
```

6. 等待验证通过（几分钟到几小时）

#### 4.3 获取 API Key

1. 点击右上角用户名 → "SMTP & API"
2. 创建新的 API Key
3. 复制并保存（只显示一次）
4. 添加到 Vercel 环境变量：
   ```
   BREVO_API_KEY=xkeysib-xxxxx
   ```

#### 4.4 创建邮件模板

在 Brevo 中创建：
- **联系表单通知模板**
- **新用户欢迎模板**
- **订阅确认模板**

### 第五步：企业邮箱配置（可选）

#### 方案 1: Cloudflare Email Routing（免费）

1. 在 Cloudflare Dashboard 点击 "Email"
2. 启用 Email Routing
3. 添加转发规则：
   ```
   info@yourdomain.com → your-gmail@gmail.com
   contact@yourdomain.com → your-gmail@gmail.com
   ```
4. 在 Gmail 中设置发件人别名（使用 Brevo SMTP）

#### 方案 2: Zoho Mail Lite（免费，5个邮箱）

1. 注册 [Zoho Mail](https://www.zoho.com/mail/)
2. 添加域名
3. 在 Cloudflare DNS 添加 MX 记录：
   ```
   类型: MX
   名称: @
   优先级: 10
   内容: mx.zoho.com
   ```

## 🚀 一键部署脚本

创建 `scripts/deploy.sh`：

```bash
#!/bin/bash

echo "🚀 开始部署..."

# 1. 构建前端
echo "📦 构建前端..."
cd frontend
pnpm build

# 2. 部署到 Vercel
echo "🌐 部署到 Vercel..."
vercel --prod

# 3. 清除 Cloudflare 缓存
echo "🗑️ 清除 CDN 缓存..."
curl -X POST "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer YOUR_CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

echo "✅ 部署完成！"
```

## 📊 成本总结

| 服务 | 免费额度 | 超出后成本 |
|------|---------|------------|
| **Cloudflare** | 无限流量 + CDN + SSL | 免费 |
| **Vercel** | 100GB 带宽/月 | $20/月起 |
| **Supabase** | 500MB 数据库 + 1GB 存储 | $25/月起 |
| **Brevo** | 300 封邮件/天 | $25/月起 |
| **域名** | - | ¥60-100/年 |
| **企业邮箱** | Cloudflare 转发 | 免费 |
| **总计（首年）** | - | **¥60-100/年** |

💡 **对于小企业/初创公司**，这套方案可以完全使用免费额度运行 6-12 个月。

## 🔧 持续维护

### 自动化部署

使用 GitHub Actions（`.github/workflows/deploy.yml`）：

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: cd frontend && pnpm install && pnpm build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

### 监控和备份

1. **Uptime Monitoring**: [UptimeRobot](https://uptimerobot.com)（免费）
2. **数据库备份**: Supabase 自动每日备份（保留 7 天）
3. **日志监控**: Vercel Analytics（免费版）

## 🔗 检查清单

部署完成后检查：

- [ ] 网站可通过自定义域名访问（HTTPS）
- [ ] 前端页面正常加载和渲染
- [ ] 新闻列表数据正常显示
- [ ] 联系表单提交成功
- [ ] 收到表单通知邮件
- [ ] 管理后台可以登录
- [ ] 图片上传和显示正常
- [ ] 移动端响应式正常
- [ ] SEO meta 标签正确
- [ ] Google Search Console 已提交

## 📞 技术支持

遇到问题参考：
- [Vercel 文档](https://vercel.com/docs)
- [Cloudflare 文档](https://developers.cloudflare.com)
- [Supabase 社区](https://github.com/supabase/supabase/discussions)
