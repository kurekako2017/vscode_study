# 静态企业网站 SEO 检查与修改实操指南

> 适用前提：**已知网站网址 + 拥有网站源代码（静态 HTML）**

---

## 一、整体思路（一句话）

**SEO = 页面结构 + HTML 标签 + 内容 + 技术细节 + 外部验证**

我们分 **5 个步骤**来做，每一步都包含「怎么检查」和「怎么修改」。

---

## 二、Step 1：SEO 体检（不改代码）

### 1. 浏览器快速检查
打开页面 → 右键 **查看网页源代码**，重点查看：

```html
<title></title>
<meta name="description" content="">
<meta name="keywords" content="">
<h1></h1>
```

检查要点：
- 是否存在 `title`
- title 是否每页唯一
- 是否存在 `description`
- 是否只有一个 `h1`

---

### 2. 在线工具扫描（推荐）
- Google PageSpeed Insights
- Google Search Console
- Ahrefs / SEMrush（如有）

关注问题：
- Missing meta tags
- Duplicate title
- Mobile friendly
- SEO Issues

---

## 三、Step 2：核心 HTML SEO 写法

### 1. `<title>`（最重要）

❌ 错误：
```html
<title>首页</title>
```

✅ 正确：
```html
<title>工业自动化设备制造商 | XX公司官网</title>
```

原则：
- 50–60 字符
- 关键词 + 品牌
- 每页唯一

---

### 2. `<meta description>`

❌ 错误：
```html
<meta name="description" content="">
```

✅ 正确：
```html
<meta name="description" content="XX公司专注工业自动化设备研发与制造，提供PLC控制系统和智能生产线解决方案。">
```

原则：
- 120–160 字
- 像广告文案
- 每页唯一

---

### 3. Heading 标签（H1 / H2）

❌ 错误：
```html
<h1>欢迎来到我们的网站</h1>
<h1>产品介绍</h1>
```

✅ 正确：
```html
<h1>工业自动化设备解决方案</h1>
<h2>PLC 控制系统</h2>
<h2>智能生产线</h2>
```

原则：
- 每页一个 h1
- h1 放核心关键词
- h2/h3 拆分内容结构

---

## 四、Step 3：内容层 SEO

### 1. 一个页面一个主题
示例：
- `/products/plc.html` → PLC 控制系统
- `/products/robot.html` → 工业机器人

---

### 2. 关键词自然出现
推荐分布：
- h1：1 次
- 前 100 字：1 次
- 正文：2–4 次
- 图片 alt：1 次

避免关键词堆砌。

---

### 3. 图片 SEO

❌ 错误：
```html
<img src="img1.jpg">
```

✅ 正确：
```html
<img src="plc-control-system.jpg" alt="PLC工业自动化控制系统">
```

---

## 五、Step 4：技术型 SEO

### 1. URL 结构

❌
```
/page1.html?id=3
```

✅
```
/products/plc-control-system.html
```

---

### 2. 移动端与性能
- 响应式布局
- 图片压缩（WebP）
- CSS/JS 合并
- CDN（如 Cloudflare）

---

### 3. sitemap.xml

```xml
<url>
  <loc>https://example.com/products/plc.html</loc>
  <lastmod>2026-01-01</lastmod>
</url>
```

提交到 Google Search Console。

---

### 4. robots.txt

```txt
User-agent: *
Allow: /
Sitemap: https://example.com/sitemap.xml
```

---

## 六、Step 5：搜索引擎验证

### 1. Google Search Console
- 提交 sitemap
- 查看收录情况
- 分析关键词曝光

---

### 2. 收录检查
Google 搜索：
```
site:example.com
```

---

### 3. 持续优化
SEO 是 **长期、稳定增长** 的过程，通常 1–4 周开始看到变化。

---

## 七、静态企业站 SEO 最小检查清单

- [ ] 每页唯一 title  
- [ ] 每页 description  
- [ ] 仅一个 h1  
- [ ] 图片有 alt  
- [ ] 页面主题明确  
- [ ] URL 可读  
- [ ] sitemap.xml  
- [ ] 移动端友好  
- [ ] 页面加载速度快  

---

**文档用途建议：**
- 企业官网 SEO 自查
- 技术/运营交接文档
- 新项目 SEO 标准模板
