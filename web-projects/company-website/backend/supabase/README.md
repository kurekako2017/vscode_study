# Supabase 配置指南

## 📋 设置步骤

### 1. 创建 Supabase 项目

1. 访问 [Supabase Dashboard](https://app.supabase.com)
2. 点击 "New Project"
3. 填写项目信息：
   - **Name**: company-website
   - **Database Password**: 生成强密码并保存
   - **Region**: 选择 Singapore (最接近中国)
4. 等待项目创建完成（约 2 分钟）

### 2. 获取项目凭证

在项目设置中找到：
- **Project URL**: `https://xxxxx.supabase.co`
- **Anon/Public Key**: `eyJhbGciOiJIUzI1NiIs...`

将这些信息填入 `frontend/.env.local`：
```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
```

### 3. 执行数据库迁移

#### 方法 1：使用 Supabase Dashboard（推荐）

1. 进入项目 Dashboard
2. 点击左侧 "SQL Editor"
3. 点击 "New Query"
4. 复制 `backend/supabase/schema.sql` 的内容
5. 粘贴并点击 "Run" 执行

#### 方法 2：使用 Supabase CLI

```bash
# 安装 Supabase CLI
npm install -g supabase

# 登录
supabase login

# 链接项目
supabase link --project-ref your-project-ref

# 执行迁移
supabase db push
```

### 4. 配置认证

1. 在 Dashboard 左侧点击 "Authentication"
2. 点击 "Providers"
3. 启用 "Email" 认证
4. （可选）配置邮件模板

### 5. 配置存储

1. 点击左侧 "Storage"
2. 创建 bucket "news-images"
3. 设置为 Public（用于新闻封面图）
4. 配置策略：
   - SELECT: 所有人可读
   - INSERT/UPDATE/DELETE: 仅管理员

### 6. 设置第一个管理员

在 SQL Editor 执行：

```sql
-- 创建管理员用户（在 Auth 中注册后）
INSERT INTO admin_profiles (id, display_name, role)
VALUES (
  'user-uuid-from-auth-users', 
  '管理员',
  'admin'
);
```

## 🔒 安全配置

### RLS 策略检查

确保以下策略已启用：
- ✅ 公开用户只能查看已发布的新闻
- ✅ 管理员可以管理所有内容
- ✅ 任何人可以提交联系表单
- ✅ 只有管理员可以查看表单提交

### API 密钥管理

⚠️ **重要**：
- `ANON_KEY` 可以公开（前端使用）
- `SERVICE_ROLE_KEY` 必须保密（仅后端使用）

## 📊 数据表说明

| 表名 | 用途 | 重要字段 |
|------|------|----------|
| `news` | 新闻文章 | title, slug, content, is_published |
| `contact_submissions` | 联系表单 | name, email, message, status |
| `newsletter_subscribers` | 邮件订阅 | email, is_active |
| `admin_profiles` | 管理员信息 | role, display_name |
| `activity_logs` | 操作日志 | action, resource_type |

## 🔧 本地开发

使用 Supabase 本地开发环境：

```bash
# 启动本地 Supabase
supabase start

# 查看本地凭证
supabase status

# 停止本地环境
supabase stop
```

## 📝 常用 SQL 查询

```sql
-- 查看所有已发布新闻
SELECT * FROM news WHERE is_published = true ORDER BY published_at DESC;

-- 查看未处理的表单提交
SELECT * FROM contact_submissions WHERE status = 'new' ORDER BY created_at DESC;

-- 查看活跃订阅者
SELECT * FROM newsletter_subscribers WHERE is_active = true;

-- 查看管理员列表
SELECT * FROM admin_profiles;
```

## 🔗 相关资源

- [Supabase 文档](https://supabase.com/docs)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Storage 配置](https://supabase.com/docs/guides/storage)
