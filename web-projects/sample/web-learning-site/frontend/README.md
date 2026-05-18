# 自动化维护新闻方案（JSON+JS 动态渲染）

本项目支持两种新闻维护方式：

1. 传统静态写法：直接在 index.html 里写死新闻内容。
2. 自动化写法：将新闻内容维护在 news.json 文件中，页面通过 script.js 动态渲染。

## 自动化新闻维护用法

1. 编辑 frontend/news.json，添加或修改新闻条目。例如：
     ```json
     [
         {
             "date": "2026.01.05",
             "title": "新サービス「AIコンサルティング」をリリース",
             "summary": "企業のAI導入を支援する新サービスの提供を開始しました。"
         }
     ]
     ```
2. script.js 会自动读取 news.json 并渲染到 .news-list 区域。
3. index.html 里原有静态新闻内容依然保留，动态内容会追加在后面。

## 动态渲染代码片段

在 script.js 中加入如下代码：
```js
document.addEventListener('DOMContentLoaded', function () {
    fetch('news.json')
        .then(response => response.json())
        .then(newsList => {
            const newsContainer = document.querySelector('.news-list');
            newsList.forEach(item => {
                const article = document.createElement('article');
                article.className = 'news-item';
                article.innerHTML = `
                    <time class="news-date">${item.date}</time>
                    <h3 class="news-title">${item.title}</h3>
                    <p class="news-summary">${item.summary}</p>
                `;
                newsContainer.appendChild(article);
            });
        });
});
```

这样只需维护 news.json 文件即可实现新闻内容的自动化更新。
# 静态站点“お問い合わせ”与“新闻推送”实现方案

## お問い合わせ（表单发信）

### 方案一：第三方表单服务（推荐）

以 Formspree 为例：

1. 注册 Formspree，获取表单 action 地址（如 https://formspree.io/f/xxxxxx）。
2. 修改 HTML 表单：
     ```html
     <form action="https://formspree.io/f/xxxxxx" method="POST">
         <input type="email" name="email" required placeholder="您的邮箱">
         <textarea name="message" required placeholder="留言内容"></textarea>
         <button type="submit">发送</button>
     </form>
     ```
3. 用户提交后，Formspree 自动将内容转发到你设置的邮箱。

### 方案二：Serverless 函数（进阶）

可用 Vercel/Netlify Functions 编写自定义 API，前端 fetch 该 API 实现邮件发送。

---

## 新闻推送

### 方案一：静态内容

直接在 HTML/JS 文件维护新闻列表，手动更新。

```html
<ul id="news-list">
    <li>2026-01-14 新网站上线！</li>
    <li>2026-01-10 发布新版教程</li>
</ul>
```

### 方案二：第三方 CMS 动态内容

用 Contentful、Notion 等 CMS 管理新闻，前端用 fetch 获取并渲染：

```js
fetch('https://cms-api.example.com/news')
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('news-list');
        data.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            list.appendChild(li);
        });
    });
```

### 方案三：自动化构建

用 GitHub Actions/Netlify 自动构建，新闻内容写 Markdown，每次提交自动生成新页面。

---

如需集成具体服务或详细代码，可参考上述示例或联系维护者。
# 会社主页前端项目

简单的公司官网静态页面，纯 HTML/CSS/JavaScript 实现。

## 功能特性

- ✅ 响应式设计（PC/平板/手机）
- ✅ 导航菜单（含移动端汉堡菜单）
- ✅ Hero 区块（首屏大图）
- ✅ 公司简介展示
- ✅ 服务介绍卡片
- ✅ 新闻列表
- ✅ 联系表单（含验证）
- ✅ 页脚信息
- ✅ 平滑滚动
- ✅ 现代化 UI 设计

## 快速启动

### 方法 1：直接打开（最简单）
```bash
# 在浏览器中打开
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### 方法 2：本地服务器（推荐）
```bash
# Python 3
cd /workspaces/study/web-learning-site/frontend
python3 -m http.server 8000

# 或使用 Node.js
npx serve .

# 然后浏览器访问 http://localhost:8000
```

### 方法 3：VS Code Live Server
1. 安装 Live Server 扩展
2. 右键 `index.html` → "Open with Live Server"

## 文件结构

```
frontend/
├── index.html    # 主页面（包含所有内容）
├── styles.css    # 样式表（响应式+现代设计）
├── script.js     # 交互逻辑（菜单+表单+动画）
└── README.md     # 本文档
```

## 页面结构

- **导航栏**：固定顶部，响应式菜单
- **Hero 区**：首屏大标题与 CTA 按钮
- **会社概要**：公司介绍+信息表格
- **服务**：4 张卡片展示服务项目
- **新闻**：3 条示例新闻
- **联系**：表单（姓名/邮箱/留言）
- **页脚**：公司信息+链接

## 表单处理

当前为演示模式：
- 前端验证（必填项、邮箱格式）
- 控制台输出数据
- 2 秒延迟后显示成功消息

**后续接入后台：**
将 `script.js` 第 45-50 行注释取消，改为实际 API 端点：
```javascript
const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
});
```

## 自定义修改

### 修改公司信息
编辑 `index.html`：
- 第 9 行：页面标题
- 第 17 行：导航 Logo
- 第 30-32 行：Hero 文案
- 第 42-58 行：公司表格信息
- 第 155-163 行：页脚联系方式

### 修改颜色主题
编辑 `styles.css` 第 8-17 行的 CSS 变量：
```css
:root {
    --primary-color: #2563eb;  /* 主色 */
    --primary-dark: #1e40af;   /* 主色深色 */
    --text-dark: #1e293b;      /* 文字颜色 */
    ...
}
```

### 添加新闻
复制 `index.html` 第 106-110 行的 `.news-item` 块并修改内容。

## 性能优化建议

1. **图片**：添加实际图片时使用 WebP 格式，并压缩
2. **字体**：当前使用系统字体，速度最快
3. **CSS**：已内联关键 CSS，生产环境可考虑分离
4. **JS**：脚本体积小，可直接内联或异步加载

## Lighthouse 检查

```bash
# 使用 Chrome DevTools
1. 按 F12 打开开发者工具
2. 切换到 "Lighthouse" 标签
3. 选择 "Performance + SEO + Accessibility"
4. 点击 "Generate report"
5. 目标：各项 ≥90 分
```

## 下一步

1. **添加实际内容**：替换文字、添加图片
2. **集成后台**：对接 Strapi/PocketBase 或自建 API
3. **部署**：上传到 Vercel/Netlify（见 ../infra/README.md）
4. **SEO 强化**：添加 sitemap.xml 和 robots.txt
5. **国际化**：支持多语言（中文/日文/英文）

## 浏览器兼容性

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ 移动端浏览器

使用了现代 CSS Grid/Flexbox 和 ES6+ 语法。
