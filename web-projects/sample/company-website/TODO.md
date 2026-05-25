# 待办事项

## ✅ 已完成（截至 2026-05-16）

- [x] 创建项目结构
- [x] 配置 Next.js + Tailwind CSS
- [x] 设计数据库架构（`backend/supabase/schema.sql`）
- [x] 创建首页示例（`frontend/app/page.tsx`）
- [x] 更新 `STRUCTURE.md`（将 dev 命令改为 `npm install && npm run dev`）
- [x] 在 `scripts/` 添加占位脚本：`deploy.sh`, `backup.sh`
- [x] 在 `infrastructure/` 添加占位说明（`docker/`, `terraform/`, `cloudflare/`）
- [x] 在 `frontend/app/contact/page.tsx` 标记为 Client Component（添加 `"use client"`）以修复 hooks 错误
- [x] 添加 `frontend/public/README.md` 占位说明

## 🚧 进行中

- ### 前端开发
- [ ] 创建所有页面组件
  - [ ] 关于我们页面
  - [ ] 服务页面
  - [ ] 案例展示页面
  - [ ] 新闻列表页面（注意：`/news` 页面当前在 dev 时因调用 `/api/news` 报 `ERR_INVALID_URL`，需修复 fetch URL）
  - [ ] 新闻详情页面
  - [x] 联系页面（已修复为 Client Component）
- [ ] 创建可复用组件
  - [ ] Header 导航栏
  - [ ] Footer 页脚
  - [ ] Button 按钮
  - [ ] Card 卡片
  - [ ] ContactForm 联系表单
  - [ ] NewsCard 新闻卡片
- [ ] 实现响应式设计
- [ ] 添加加载动画

### 后端开发
- [ ] 实现新闻 CRUD API
- [ ] 实现联系表单提交 API
- [ ] 集成 Brevo 邮件发送
- [ ] 实现文件上传（新闻封面）
- [ ] 添加 API 错误处理
- [ ] 实现 API 限流

### 管理后台
- [ ] 创建登录页面
- [ ] 实现认证逻辑
- [ ] 新闻管理界面
  - [ ] 新闻列表
  - [ ] 创建新闻
  - [ ] 编辑新闻
  - [ ] 删除新闻
  - [ ] 发布/下架
- [ ] 表单管理界面
  - [ ] 查看所有提交
  - [ ] 标记已读/未读
  - [ ] 回复表单
  - [ ] 导出数据
- [ ] 仪表盘（统计）
  - [ ] 访问量统计
  - [ ] 新闻阅读量
  - [ ] 表单提交趋势

### 部署和运维
- [ ] 配置 Supabase 项目
- [ ] 部署到 Vercel
- [ ] 配置自定义域名
- [ ] 配置 Brevo 邮件服务
- [ ] 设置 CI/CD（GitHub Actions）
- [ ] 配置监控和日志
- [ ] 备份策略（占位脚本已添加为 `scripts/backup.sh`，需替换为真实备份实现）

## 📌 待办（优先级低）

### 功能增强
- [ ] 添加搜索功能
- [ ] 实现新闻分类和标签筛选
- [ ] 添加评论系统
- [ ] 实现新闻订阅
- [ ] 添加社交媒体分享
- [ ] SEO 优化（sitemap、robots.txt）
- [ ] 实现多语言支持（中英文）

### 性能优化
- [ ] 图片懒加载
- [ ] 代码分割优化
- [ ] 实现 ISR（增量静态再生成）
- [ ] 添加 Service Worker（PWA）
- [ ] 优化首屏加载时间
- [ ] 配置 CDN 缓存策略

### 安全和质量
- [ ] 添加单元测试
- [ ] 添加 E2E 测试
- [ ] 实现 CSRF 保护
- [ ] 添加 Rate Limiting
- [ ] 配置 Content Security Policy
- [ ] 代码审计和安全扫描

## 🔧 技术债务

- [ ] 统一错误处理机制
- [ ] 完善 TypeScript 类型定义
- [ ] 优化数据库查询（添加索引）
- [ ] 重构重复代码
- [ ] 添加 ESLint 和 Prettier 配置
- [ ] 编写 API 文档

## 📝 文档待完善

- [ ] API 接口文档（补充 `/api/*` 规范）
- [ ] 组件使用文档
- [ ] 数据库设计文档（补充 ER 图与说明）
- [ ] 部署流程示例（脚本与步骤）
- [ ] 常见问题 FAQ
- [ ] 贡献指南

---

**更新时间**: 2026年5月16日
