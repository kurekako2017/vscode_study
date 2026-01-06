# Web Projects - 网站开发项目

## 📚 文档导航

### 🎓 教程文档

1. **[WEB_DEVELOPMENT_GUIDE.md](docs/WEB_DEVELOPMENT_GUIDE.md)** - 网站开发完整教程
   - VS Code 网页制作基础
   - WordPress 开发方案
   - Bootstrap Studio 集成
   - 现代开发工具和模板

2. **[EMAIL_NEWS_IMPLEMENTATION_GUIDE.md](docs/EMAIL_NEWS_IMPLEMENTATION_GUIDE.md)** - 邮件和新闻功能实现
   - 邮件服务器部署
   - 邮件发送功能
   - 新闻提交管理
   - 生产环境部署

3. **[EMAIL_DEPLOYMENT_QUICK_START.md](docs/EMAIL_DEPLOYMENT_QUICK_START.md)** - 5分钟快速上手
   - 快速部署邮件服务
   - 简化版实现
   - 常见问题解决

4. **[SEO_OPTIMIZATION_GUIDE.md](docs/SEO_OPTIMIZATION_GUIDE.md)** - SEO 优化指南
   - 已上线网站SEO工具
   - 本地环境SEO检查
   - 关键词研究优化
   - WordPress SEO优化

### 💼 业务文档

5. **[WEB_QUOTATION_STANDARD.md](docs/WEB_QUOTATION_STANDARD.md)** - 网页制作报价标准
   - 页面制作费用
   - 服务器维护费用
   - 企业邮箱年费
   - 完整案例计算

6. **[ECOMMERCE_QUOTATION_TEMPLATE.md](docs/ECOMMERCE_QUOTATION_TEMPLATE.md)** - 电商网站报价方案
   - 购物网站功能模块
   - 电商平台报价
   - 支付集成费用

7. **[EMAIL_SETUP.md](docs/EMAIL_SETUP.md)** - 邮箱服务器配置
   - 域名和邮箱配置
   - SMTP设置
   - 企业邮箱方案

---

## 🚀 快速开始

### 方案一：纯静态网站（最简单）

```bash
# 使用 Vite
npm create vite@latest my-site
cd my-site
npm install
npm run dev
```

### 方案二：邮件功能网站

```bash
# 创建项目
mkdir my-website
cd my-website
npm init -y

# 安装依赖
npm install express nodemailer dotenv body-parser cors

# 创建文件
# 参考 EMAIL_DEPLOYMENT_QUICK_START.md

# 启动
node server.js
```

### 方案三：WordPress 网站

```bash
# 1. 下载 LocalWP: https://localwp.com
# 2. 创建新站点
# 3. 安装主题（Astra/OceanWP）
# 4. 安装 Elementor
# 5. 开始设计
```

### 方案四：Next.js 现代应用

```bash
npx create-next-app@latest my-site
cd my-site
npm run dev
```

---

## 📂 项目结构

```
web-projects/
├── README.md                              # 本文件
├── WEB_DEVELOPMENT_GUIDE.md              # 开发教程
├── EMAIL_NEWS_IMPLEMENTATION_GUIDE.md    # 邮件新闻实现
├── EMAIL_DEPLOYMENT_QUICK_START.md       # 快速部署
└── company-website/                       # 公司网站项目
    ├── docs/
    │   ├── WEB_QUOTATION_STANDARD.md     # 报价标准
    │   └── EMAIL_SETUP.md                # 邮件配置
    └── [项目文件...]
```

---

## 💡 技术栈选择

### 静态网站
- **HTML + CSS + JavaScript** - 最基础
- **Bootstrap** - 快速响应式
- **Tailwind CSS** - 现代工具优先

### 动态网站
- **Node.js + Express** - 轻量级后端
- **WordPress** - CMS 管理
- **Next.js** - React 全栈

### 邮件服务
- **Nodemailer** - Node.js 邮件
- **Gmail SMTP** - 免费方案
- **阿里云/腾讯云** - 企业方案

### 数据库
- **MySQL** - 关系型数据库
- **MongoDB** - NoSQL 文档
- **PostgreSQL** - 高级特性

---

## 🛠️ 常用命令

### 开发命令
```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 启动生产服务
npm start
```

### Git 命令
```bash
# 初始化
git init

# 提交更改
git add .
git commit -m "feat: add new feature"
git push
```

### Docker 命令
```bash
# 构建镜像
docker build -t my-website .

# 运行容器
docker run -p 3000:3000 my-website

# 使用 docker-compose
docker-compose up -d
```

---

## 📖 学习路径

### 初学者（0-3个月）
1. ✅ HTML + CSS 基础
2. ✅ JavaScript 基础
3. ✅ Bootstrap 框架
4. ✅ Git 版本控制
5. ✅ VS Code 使用

### 进阶（3-6个月）
1. ✅ Node.js + Express
2. ✅ MySQL 数据库
3. ✅ WordPress 主题开发
4. ✅ React 或 Vue 基础
5. ✅ API 开发

### 高级（6-12个月）
1. ✅ Next.js / Nuxt.js
2. ✅ TypeScript
3. ✅ Docker 部署
4. ✅ CI/CD 流程
5. ✅ 性能优化

---

## 💰 成本估算

### 小型企业网站
- **开发费用**：¥100,000-200,000
- **年维护费**：¥30,000-50,000
- **服务器**：¥2,000-5,000/年
- **域名**：¥60-100/年

### 中型电商平台
- **开发费用**：¥500,000-1,000,000
- **年维护费**：¥100,000-200,000
- **服务器**：¥10,000-30,000/年

### 内部管理系统
- **开发费用**：¥300,000-800,000
- **年维护费**：¥50,000-150,000
- **服务器**：¥5,000-15,000/年

详细报价见：[WEB_QUOTATION_STANDARD.md](company-website/docs/WEB_QUOTATION_STANDARD.md)

---

## 🔗 有用的资源

### 官方文档
- [MDN Web Docs](https://developer.mozilla.org/)
- [Node.js Docs](https://nodejs.org/docs/)
- [WordPress Developer](https://developer.wordpress.org/)
- [React Docs](https://react.dev/)

### 学习平台
- [freeCodeCamp](https://www.freecodecamp.org/)
- [MDN](https://developer.mozilla.org/)
- [W3Schools](https://www.w3schools.com/)

### 工具和资源
- [GitHub](https://github.com/)
- [VS Code](https://code.visualstudio.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 📞 获取帮助

如有问题，请查看：
1. 文档中的"常见问题"章节
2. GitHub Issues
3. Stack Overflow
4. 项目内的具体文档

---

## 📝 更新日志

- **2026-01-06**: 创建项目文档结构
  - 添加完整开发教程
  - 添加邮件功能实现指南
  - 添加快速部署文档
  - 添加报价标准文档

---

**最后更新**：2026年1月6日
**文档版本**：v1.0
