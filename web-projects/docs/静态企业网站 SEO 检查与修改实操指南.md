# 静态企业网站 SEO 检查与修改实操指南

## 一、SEO 现状检查清单

### 1. **基础技术 SEO 检查**

```bash
# 检查项目
□ robots.txt 文件是否存在且配置正确
□ sitemap.xml 是否存在
□ HTTPS 是否启用
□ 页面加载速度（建议 < 3秒）
□ 移动端适配情况
□ 404 页面是否友好
```

### 2. **页面级别检查**

每个页面需检查：

**HTML 头部元素：**
- `<title>` 标签（50-60字符）
- `<meta name="description">` （150-160字符）
- `<meta name="keywords">`（可选，但建议保留）
- `<meta name="viewport">` 移动端适配
- Open Graph 标签（社交媒体分享）
- Canonical 标签（避免重复内容）

**内容结构：**
- H1 标签（每页仅一个）
- H2-H6 层级结构清晰
- 图片 alt 属性
- 内部链接结构
- 外部链接的 rel 属性

### 3. **内容质量检查**
- 关键词密度（2-3%为宜）
- 内容原创性
- 内容长度（建议 300+ 字）
- 关键词布局（标题、首段、小标题、结尾）

## 二、实操修改步骤

### **步骤 1：准备工作**

```bash
# 1. 备份原网站
cp -r /path/to/website /path/to/website_backup_$(date +%Y%m%d)

# 2. 建立 SEO 检查表格
# 用 Excel 或 Google Sheets 记录每个页面的优化状态
```

### **步骤 2：创建/优化核心文件**

**robots.txt 示例：**
```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: https://yourdomain.com/sitemap.xml
```

**sitemap.xml 生成：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <lastmod>2026-01-09</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/about.html</loc>
    <lastmod>2026-01-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- 添加所有页面 -->
</urlset>
```

### **步骤 3：优化 HTML 页面头部**

**标准模板：**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 核心 SEO 标签 -->
    <title>主关键词 - 副关键词 | 品牌名</title>
    <meta name="description" content="简洁描述页面内容，包含核心关键词，吸引用户点击">
    <meta name="keywords" content="关键词1, 关键词2, 关键词3">
    
    <!-- 规范链接 -->
    <link rel="canonical" href="https://yourdomain.com/current-page.html">
    
    <!-- Open Graph 社交媒体优化 -->
    <meta property="og:title" content="页面标题">
    <meta property="og:description" content="页面描述">
    <meta property="og:image" content="https://yourdomain.com/images/og-image.jpg">
    <meta property="og:url" content="https://yourdomain.com/current-page.html">
    <meta property="og:type" content="website">
    
    <!-- 网站图标 -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    
    <!-- 结构化数据（JSON-LD） -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "公司名称",
      "url": "https://yourdomain.com",
      "logo": "https://yourdomain.com/logo.png",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+86-xxx-xxxx",
        "contactType": "customer service"
      }
    }
    </script>
</head>
```

### **步骤 4：优化页面内容结构**

**修改前：**
```html
<div class="header">公司介绍</div>
<p>我们是一家...</p>
```

**修改后：**
```html
<h1>公司名称 - 行业领先的解决方案提供商</h1>
<p>我们是一家专注于<strong>核心业务关键词</strong>的企业，为客户提供...</p>

<h2>我们的服务</h2>
<ul>
    <li><a href="/service1.html">服务项目一</a>：详细描述</li>
    <li><a href="/service2.html">服务项目二</a>：详细描述</li>
</ul>

<h2>为什么选择我们</h2>
<p>包含关键词的自然段落...</p>
```

### **步骤 5：图片优化**

```html
<!-- 修改前 -->
<img src="image1.jpg">

<!-- 修改后 -->
<img src="image1.jpg" 
     alt="关键词描述的图片内容" 
     title="图片标题"
     width="800" 
     height="600"
     loading="lazy">
```

**图片文件命名：**
```bash
# 不好的命名
IMG_001.jpg
photo.png

# 好的命名（包含关键词）
gongsi-chanpin-zhanshi-2026.jpg
qiye-fuwu-anli-beijing.png
```

### **步骤 6：内部链接优化**

```html
<!-- 使用描述性锚文本 -->
<a href="/about.html">了解更多关于我们的企业文化</a>

<!-- 避免 -->
<a href="/about.html">点击这里</a>
<a href="/about.html">更多</a>

<!-- 相关页面互联 -->
<div class="related-links">
    <h3>相关内容</h3>
    <ul>
        <li><a href="/service1.html">相关服务一</a></li>
        <li><a href="/case-study.html">成功案例展示</a></li>
    </ul>
</div>
```

## 三、性能优化

### 1. **压缩和合并资源**

```html
<!-- CSS 合并压缩 -->
<link rel="stylesheet" href="css/main.min.css">

<!-- JavaScript 延迟加载 -->
<script src="js/main.min.js" defer></script>
```

### 2. **启用缓存（.htaccess 配置）**

```apache
# 浏览器缓存
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Gzip 压缩
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript
</IfModule>
```

## 四、验证与提交

### 1. **使用工具检查**
- Google Search Console（必须）
- Bing Webmaster Tools
- 百度站长平台（中文网站）
- Google PageSpeed Insights（性能检查）
- SEMrush 或 Ahrefs（专业工具）

### 2. **提交网站地图**

```bash
# Google Search Console
1. 登录 search.google.com/search-console
2. 添加资源（网站）
3. 验证所有权
4. 提交 sitemap.xml

# 手动触发爬取（可选）
通过 "网址检查" 工具请求编入索引
```

## 五、监控与维护

### **定期检查清单（每月）**

```markdown
□ Google Search Console 检查错误
□ 检查网站排名变化
□ 分析流量来源
□ 更新过期内容
□ 检查死链接
□ 添加新内容/博客文章
□ 检查竞争对手 SEO 策略
```

## 六、常见问题处理

### **问题 1：页面未被收录**
```bash
解决方案：
1. 检查 robots.txt 是否误屏蔽
2. 提交 sitemap
3. 通过 Search Console 请求索引
4. 增加外部链接引流
```

### **问题 2：排名下降**
```bash
检查项：
1. 内容是否被竞争对手超越
2. 页面加载速度是否变慢
3. 移动端体验是否良好
4. 是否有技术错误
```

## 七、进阶优化建议

1. **添加博客或资讯栏目** - 定期更新内容
2. **建立本地 SEO**（如果适用）- Google My Business
3. **获取高质量