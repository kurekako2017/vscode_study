# 网站SEO优化完整指南

## 📋 目录

1. [SEO基础知识](#1-seo基础知识)
2. [已上线网站SEO工具](#2-已上线网站seo工具)
3. [本地环境SEO工具](#3-本地环境seo工具)
4. [关键词研究与优化](#4-关键词研究与优化)
5. [技术SEO实现](#5-技术seo实现)
6. [内容优化策略](#6-内容优化策略)
7. [WordPress SEO优化](#7-wordpress-seo优化)

---

## 1. SEO基础知识

### 1.1 什么是SEO

**SEO (Search Engine Optimization)** - 搜索引擎优化

**三大核心支柱：**
- 🔧 **技术SEO** - 网站结构、速度、索引
- 📝 **内容SEO** - 关键词、质量、相关性
- 🔗 **外链SEO** - 权威性、反向链接

### 1.2 SEO检查清单

#### 基础优化（必做）
- ✅ 标题标签优化 (Title Tag)
- ✅ 元描述优化 (Meta Description)
- ✅ H1-H6 标题层级
- ✅ 图片 Alt 属性
- ✅ URL 结构优化
- ✅ 移动端适配
- ✅ 页面加载速度
- ✅ HTTPS 安全连接
- ✅ XML 网站地图
- ✅ Robots.txt 文件

#### 进阶优化
- ✅ 结构化数据 (Schema.org)
- ✅ Open Graph 标签
- ✅ Twitter Cards
- ✅ 规范链接 (Canonical)
- ✅ 面包屑导航
- ✅ 内部链接策略
- ✅ 404 错误处理
- ✅ 301 重定向管理

---

## 2. 已上线网站SEO工具

### 2.1 综合分析工具

#### **Google Search Console** (必备，免费)
🌐 https://search.google.com/search-console

**功能：**
- 索引状态监控
- 搜索查询分析
- 网站性能报告
- 移动可用性
- Core Web Vitals
- 安全问题提醒

**使用方法：**
1. 访问 Google Search Console
2. 添加网站资源
3. 验证所有权（DNS/HTML文件/Google Analytics）
4. 提交 sitemap.xml

#### **Google Analytics 4** (必备，免费)
🌐 https://analytics.google.com

**功能：**
- 流量来源分析
- 用户行为追踪
- 转化率监控
- 实时访客数据

**安装代码：**
```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

#### **PageSpeed Insights** (免费)
🌐 https://pagespeed.web.dev/

**功能：**
- 性能评分（0-100分）
- Core Web Vitals 测试
- 移动端/桌面端分析
- 优化建议

**重要指标：**
- **LCP** (Largest Contentful Paint) - 最大内容绘制 < 2.5s
- **FID** (First Input Delay) - 首次输入延迟 < 100ms
- **CLS** (Cumulative Layout Shift) - 累积布局偏移 < 0.1

#### **GTmetrix** (免费 + 付费)
🌐 https://gtmetrix.com/

**功能：**
- 详细性能报告
- 瀑布流分析
- 历史数据对比
- 监控提醒

#### **SEMrush** (付费，专业)
🌐 https://www.semrush.com/

**功能：**
- 关键词排名追踪
- 竞争对手分析
- 反向链接监控
- 内容差距分析
- 技术SEO审计

**价格：** $119.95/月起

#### **Ahrefs** (付费，专业)
🌐 https://ahrefs.com/

**功能：**
- 网站探索器
- 关键词研究
- 内容探索
- 排名追踪
- 网站审计

**价格：** $99/月起

#### **Moz Pro** (付费)
🌐 https://moz.com/

**功能：**
- Domain Authority (DA) 评分
- 关键词研究
- 网站爬取
- 排名追踪

**价格：** $99/月起

### 2.2 免费在线SEO工具

#### **Ubersuggest** (Neil Patel)
🌐 https://neilpatel.com/ubersuggest/

**功能：**
- 关键词建议
- SEO审计
- 竞争对手分析
- 反向链接数据

**限制：** 免费版每天3次查询

#### **Screaming Frog SEO Spider** (免费 + 付费)
🌐 https://www.screamingfrogseoseo.com/seo-spider/

**功能：**
- 网站爬取（免费版500个URL）
- 技术SEO问题发现
- 元数据分析
- 断链检测

#### **Seobility** (免费 + 付费)
🌐 https://www.seobility.net/

**功能：**
- 免费网站审计
- 关键词监控
- 反向链接检查
- 排名追踪

#### **AnswerThePublic** (免费 + 付费)
🌐 https://answerthepublic.com/

**功能：**
- 用户搜索问题挖掘
- 长尾关键词发现
- 内容灵感生成

#### **Google Keyword Planner** (免费)
🌐 https://ads.google.com/home/tools/keyword-planner/

**功能：**
- 关键词搜索量
- 竞争程度分析
- 相关关键词建议
- 出价建议

---

## 3. 本地环境SEO工具

### 3.1 VS Code 扩展

#### **SEO Utils** (推荐)
- ID: `hridoy.seo-utils`
- 功能：实时SEO检查、meta标签建议

#### **HTML CSS Support**
- ID: `ecmel.vscode-html-css`
- 功能：HTML标签提示、属性补全

#### **HTMLHint**
- ID: `mkaufman.HTMLHint`
- 功能：HTML代码质量检查

#### **Lighthouse**
- ID: `GoogleChrome.lighthouse`
- 功能：本地性能审计

**安装方法：**
```bash
# 打开 VS Code
# 按 Ctrl+Shift+X
# 搜索扩展名安装
```

### 3.2 Node.js SEO工具

#### **lighthouse-cli** (Google官方)
```bash
# 安装
npm install -g lighthouse

# 运行审计
lighthouse http://localhost:3000 --view

# 生成报告
lighthouse http://localhost:3000 --output html --output-path ./report.html

# 只检查SEO
lighthouse http://localhost:3000 --only-categories=seo --view

# CI/CD集成
lighthouse http://localhost:3000 --output json --output-path ./lighthouse.json
```

**配置文件 (lighthouse-config.js)：**
```javascript
module.exports = {
  extends: 'lighthouse:default',
  settings: {
    onlyCategories: ['seo', 'performance', 'accessibility'],
    locale: 'zh-CN'
  }
};
```

#### **seo-checker** (npm包)
```bash
npm install -g seo-checker

# 检查网站
seo-checker http://localhost:3000
```

#### **broken-link-checker**
```bash
npm install -g broken-link-checker

# 检查断链
blc http://localhost:3000 -ro
```

### 3.3 本地SEO审计脚本

#### 创建 `seo-audit.js`
```javascript
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs');

async function runAudit(url) {
    // 启动 Chrome
    const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
    
    const options = {
        logLevel: 'info',
        output: 'html',
        onlyCategories: ['seo', 'performance', 'accessibility'],
        port: chrome.port,
        locale: 'zh-CN'
    };

    // 运行审计
    const runnerResult = await lighthouse(url, options);

    // 生成报告
    const reportHtml = runnerResult.report;
    fs.writeFileSync('lighthouse-report.html', reportHtml);

    // 输出评分
    console.log('📊 SEO审计结果:');
    console.log('SEO评分:', runnerResult.lhr.categories.seo.score * 100);
    console.log('性能评分:', runnerResult.lhr.categories.performance.score * 100);
    console.log('可访问性:', runnerResult.lhr.categories.accessibility.score * 100);

    // 输出SEO问题
    const seoAudits = runnerResult.lhr.categories.seo.auditRefs;
    console.log('\n❌ SEO问题:');
    seoAudits.forEach(audit => {
        const auditResult = runnerResult.lhr.audits[audit.id];
        if (auditResult.score !== 1) {
            console.log(`- ${auditResult.title}: ${auditResult.description}`);
        }
    });

    await chrome.kill();
}

// 使用
runAudit('http://localhost:3000');
```

**运行：**
```bash
node seo-audit.js
```

### 3.4 自动化SEO检查工具

#### 创建 `check-seo.js`
```javascript
const puppeteer = require('puppeteer');
const cheerio = require('cheerio');

async function checkLocalSEO(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);
    
    const content = await page.content();
    const $ = cheerio.load(content);
    
    const report = {
        url: url,
        issues: [],
        warnings: [],
        suggestions: []
    };

    // 检查标题
    const title = $('title').text();
    if (!title) {
        report.issues.push('❌ 缺少 <title> 标签');
    } else if (title.length < 30) {
        report.warnings.push('⚠️ 标题太短（建议30-60字符）');
    } else if (title.length > 60) {
        report.warnings.push('⚠️ 标题太长（建议30-60字符）');
    } else {
        report.suggestions.push(`✅ 标题: ${title}`);
    }

    // 检查Meta描述
    const description = $('meta[name="description"]').attr('content');
    if (!description) {
        report.issues.push('❌ 缺少 meta description');
    } else if (description.length < 120) {
        report.warnings.push('⚠️ 描述太短（建议120-160字符）');
    } else if (description.length > 160) {
        report.warnings.push('⚠️ 描述太长（建议120-160字符）');
    } else {
        report.suggestions.push(`✅ 描述: ${description}`);
    }

    // 检查H1标签
    const h1Count = $('h1').length;
    if (h1Count === 0) {
        report.issues.push('❌ 缺少 H1 标签');
    } else if (h1Count > 1) {
        report.warnings.push(`⚠️ 有 ${h1Count} 个 H1 标签（建议只有1个）`);
    } else {
        report.suggestions.push(`✅ H1: ${$('h1').text()}`);
    }

    // 检查图片Alt属性
    const images = $('img');
    const imagesWithoutAlt = images.filter((i, img) => !$(img).attr('alt')).length;
    if (imagesWithoutAlt > 0) {
        report.warnings.push(`⚠️ 有 ${imagesWithoutAlt} 张图片缺少 alt 属性`);
    }

    // 检查内部链接
    const links = $('a[href]');
    const brokenLinks = [];
    links.each((i, link) => {
        const href = $(link).attr('href');
        if (href && href.startsWith('#') && !$(href).length) {
            brokenLinks.push(href);
        }
    });
    if (brokenLinks.length > 0) {
        report.warnings.push(`⚠️ 发现 ${brokenLinks.length} 个断链`);
    }

    // 检查移动端视口
    const viewport = $('meta[name="viewport"]').attr('content');
    if (!viewport) {
        report.issues.push('❌ 缺少移动端 viewport meta 标签');
    }

    // 检查Open Graph
    const ogTitle = $('meta[property="og:title"]').attr('content');
    if (!ogTitle) {
        report.warnings.push('⚠️ 缺少 Open Graph 标签（社交媒体分享）');
    }

    // 检查结构化数据
    const jsonLd = $('script[type="application/ld+json"]');
    if (jsonLd.length === 0) {
        report.suggestions.push('💡 建议添加结构化数据 (Schema.org)');
    }

    // 检查语言标签
    const lang = $('html').attr('lang');
    if (!lang) {
        report.warnings.push('⚠️ HTML标签缺少 lang 属性');
    }

    await browser.close();

    // 输出报告
    console.log('\n📊 SEO审计报告');
    console.log('='.repeat(50));
    console.log(`🌐 URL: ${url}\n`);

    if (report.issues.length > 0) {
        console.log('🔴 严重问题:');
        report.issues.forEach(issue => console.log(issue));
        console.log('');
    }

    if (report.warnings.length > 0) {
        console.log('🟡 警告:');
        report.warnings.forEach(warning => console.log(warning));
        console.log('');
    }

    if (report.suggestions.length > 0) {
        console.log('🟢 通过检查:');
        report.suggestions.forEach(suggestion => console.log(suggestion));
        console.log('');
    }

    // 计算SEO分数
    const totalChecks = report.issues.length + report.warnings.length + report.suggestions.length;
    const score = Math.round((report.suggestions.length / totalChecks) * 100);
    console.log(`\n📈 SEO评分: ${score}/100`);
    
    return report;
}

// 使用
checkLocalSEO('http://localhost:3000');
```

**安装依赖：**
```bash
npm install puppeteer cheerio
```

**运行：**
```bash
node check-seo.js
```

---

## 4. 关键词研究与优化

### 4.1 关键词研究工具

#### **免费工具**

1. **Google Keyword Planner**
   - 获取搜索量数据
   - 发现相关关键词
   - 竞争程度分析

2. **Google Trends**
   🌐 https://trends.google.com
   - 关键词趋势
   - 地域分布
   - 相关主题

3. **AnswerThePublic**
   - 用户问题挖掘
   - 长尾关键词

4. **Keyword Surfer** (Chrome扩展)
   - 搜索结果页显示搜索量
   - 相关关键词建议

#### **付费工具**

1. **Ahrefs Keywords Explorer**
   - 搜索量
   - 关键词难度
   - 点击率预估
   - SERP概览

2. **SEMrush Keyword Magic Tool**
   - 数十亿关键词数据库
   - 问题型关键词
   - 关键词分组

### 4.2 关键词分析策略

#### 关键词类型

```
┌─────────────────────────────────────┐
│      关键词金字塔                      │
├─────────────────────────────────────┤
│  Head Keywords (头部关键词)          │
│  • 搜索量: 高 (>10,000/月)           │
│  • 竞争度: 高                        │
│  • 转化率: 低                        │
│  • 示例: "网站制作"                   │
├─────────────────────────────────────┤
│  Body Keywords (躯干关键词)          │
│  • 搜索量: 中 (1,000-10,000/月)      │
│  • 竞争度: 中                        │
│  • 转化率: 中                        │
│  • 示例: "东京网站制作公司"           │
├─────────────────────────────────────┤
│  Long-tail Keywords (长尾关键词)     │
│  • 搜索量: 低 (<1,000/月)            │
│  • 竞争度: 低                        │
│  • 转化率: 高                        │
│  • 示例: "东京低成本企业网站制作服务"  │
└─────────────────────────────────────┘
```

#### 关键词研究流程

```javascript
// 关键词分析脚本
const keywords = {
    primary: "网站制作",  // 主关键词
    secondary: [          // 次要关键词
        "网页设计",
        "网站开发",
        "企业建站"
    ],
    longtail: [          // 长尾关键词
        "东京网站制作价格",
        "响应式网站开发",
        "WordPress企业网站制作",
        "电商网站制作服务"
    ],
    related: [           // 相关关键词
        "网站优化",
        "SEO服务",
        "网站维护",
        "域名注册"
    ]
};

// 关键词密度计算
function calculateKeywordDensity(text, keyword) {
    const words = text.toLowerCase().split(/\s+/);
    const keywordCount = words.filter(word => word === keyword.toLowerCase()).length;
    const density = (keywordCount / words.length) * 100;
    
    console.log(`关键词: ${keyword}`);
    console.log(`出现次数: ${keywordCount}`);
    console.log(`密度: ${density.toFixed(2)}%`);
    console.log(`建议: ${density < 1 ? '增加' : density > 3 ? '减少' : '合适'}`);
    
    return density;
}

// 使用示例
const pageContent = "网站制作是我们的专长...";
calculateKeywordDensity(pageContent, "网站制作");
```

### 4.3 关键词布局建议

#### 页面优化位置

| 位置 | 重要性 | 建议 |
|------|--------|------|
| **Title标签** | ⭐⭐⭐⭐⭐ | 关键词放在前面，50-60字符 |
| **H1标签** | ⭐⭐⭐⭐⭐ | 包含主关键词，每页一个 |
| **Meta描述** | ⭐⭐⭐⭐ | 自然融入关键词，120-160字符 |
| **URL** | ⭐⭐⭐⭐ | 简短、包含关键词、使用连字符 |
| **前100个字** | ⭐⭐⭐⭐ | 在开头段落包含主关键词 |
| **H2-H6标签** | ⭐⭐⭐ | 使用相关关键词和变体 |
| **图片Alt** | ⭐⭐⭐ | 描述性文字，包含关键词 |
| **内部链接** | ⭐⭐⭐ | 锚文本使用相关关键词 |
| **正文内容** | ⭐⭐⭐ | 自然分布，密度1-2% |

#### 关键词密度建议

```
理想密度: 1-2%
可接受: 0.5-3%
过度优化: >3%
不足: <0.5%
```

---

## 5. 技术SEO实现

### 5.1 HTML基础优化

#### 完整SEO优化模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <!-- 基础Meta标签 -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- SEO核心标签 -->
    <title>东京网站制作 - 专业企业网站开发服务 | 公司名称</title>
    <meta name="description" content="提供专业的东京网站制作服务，包括企业网站、电商平台、响应式设计。10年经验，价格透明，售后完善。免费咨询：400-123-4567">
    <meta name="keywords" content="东京网站制作,网页设计,企业建站,响应式网站,网站开发">
    
    <!-- 作者和版权 -->
    <meta name="author" content="公司名称">
    <meta name="copyright" content="© 2026 公司名称">
    <meta name="robots" content="index, follow">
    
    <!-- 规范链接 -->
    <link rel="canonical" href="https://www.example.com/web-design">
    
    <!-- 多语言支持 -->
    <link rel="alternate" hreflang="zh-CN" href="https://www.example.com/zh/">
    <link rel="alternate" hreflang="ja" href="https://www.example.com/ja/">
    <link rel="alternate" hreflang="en" href="https://www.example.com/en/">
    
    <!-- Open Graph (Facebook) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="东京网站制作 - 专业企业网站开发服务">
    <meta property="og:description" content="提供专业的东京网站制作服务，10年经验，价格透明">
    <meta property="og:image" content="https://www.example.com/images/og-image.jpg">
    <meta property="og:url" content="https://www.example.com/web-design">
    <meta property="og:site_name" content="公司名称">
    <meta property="og:locale" content="zh_CN">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="东京网站制作 - 专业企业网站开发服务">
    <meta name="twitter:description" content="提供专业的东京网站制作服务，10年经验，价格透明">
    <meta name="twitter:image" content="https://www.example.com/images/twitter-image.jpg">
    <meta name="twitter:site" content="@yourcompany">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    
    <!-- DNS预解析 -->
    <link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    
    <!-- 结构化数据 (Schema.org) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "公司名称",
      "url": "https://www.example.com",
      "logo": "https://www.example.com/logo.png",
      "description": "专业网站制作公司",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "东京都渋谷区...",
        "addressLocality": "渋谷区",
        "addressRegion": "东京都",
        "postalCode": "150-0000",
        "addressCountry": "JP"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+81-3-1234-5678",
        "contactType": "customer service",
        "areaServed": "JP",
        "availableLanguage": ["Japanese", "Chinese"]
      },
      "sameAs": [
        "https://www.facebook.com/yourcompany",
        "https://twitter.com/yourcompany",
        "https://www.linkedin.com/company/yourcompany"
      ]
    }
    </script>
    
    <!-- 面包屑结构化数据 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "首页",
        "item": "https://www.example.com"
      },{
        "@type": "ListItem",
        "position": 2,
        "name": "服务",
        "item": "https://www.example.com/services"
      },{
        "@type": "ListItem",
        "position": 3,
        "name": "网站制作",
        "item": "https://www.example.com/services/web-design"
      }]
    }
    </script>
    
    <!-- 文章结构化数据 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "东京网站制作完整指南",
      "image": "https://www.example.com/images/article-image.jpg",
      "author": {
        "@type": "Person",
        "name": "作者名称"
      },
      "publisher": {
        "@type": "Organization",
        "name": "公司名称",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.example.com/logo.png"
        }
      },
      "datePublished": "2026-01-06",
      "dateModified": "2026-01-06"
    }
    </script>
    
    <!-- CSS -->
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <!-- 跳转到主内容（辅助功能） -->
    <a href="#main-content" class="skip-link">跳转到主内容</a>
    
    <!-- 头部 -->
    <header>
        <nav aria-label="主导航">
            <!-- 导航内容 -->
        </nav>
    </header>
    
    <!-- 面包屑导航 -->
    <nav aria-label="面包屑">
        <ol class="breadcrumb">
            <li><a href="/">首页</a></li>
            <li><a href="/services">服务</a></li>
            <li aria-current="page">网站制作</li>
        </ol>
    </nav>
    
    <!-- 主内容 -->
    <main id="main-content">
        <article>
            <h1>东京专业网站制作服务</h1>
            
            <!-- 文章内容，使用语义化标签 -->
            <section>
                <h2>为什么选择我们的网站制作服务</h2>
                <p>我们提供专业的<strong>东京网站制作</strong>服务...</p>
                
                <!-- 图片优化 -->
                <figure>
                    <img 
                        src="/images/web-design-services.jpg" 
                        alt="东京网站制作服务展示 - 响应式设计示例"
                        width="800" 
                        height="600"
                        loading="lazy"
                    >
                    <figcaption>专业的响应式网站设计</figcaption>
                </figure>
            </section>
            
            <section>
                <h2>我们的网站制作流程</h2>
                <!-- 内容 -->
            </section>
        </article>
    </main>
    
    <!-- 页脚 -->
    <footer>
        <p>&copy; 2026 公司名称. 版权所有.</p>
    </footer>
    
    <!-- JavaScript (延迟加载) -->
    <script src="/js/script.js" defer></script>
</body>
</html>
```

### 5.2 网站地图 (Sitemap)

#### sitemap.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
    
    <!-- 首页 -->
    <url>
        <loc>https://www.example.com/</loc>
        <lastmod>2026-01-06</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
        
        <!-- 多语言版本 -->
        <xhtml:link rel="alternate" hreflang="zh-CN" href="https://www.example.com/zh/"/>
        <xhtml:link rel="alternate" hreflang="ja" href="https://www.example.com/ja/"/>
    </url>
    
    <!-- 服务页面 -->
    <url>
        <loc>https://www.example.com/services/web-design</loc>
        <lastmod>2026-01-05</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- 博客文章 -->
    <url>
        <loc>https://www.example.com/blog/seo-guide</loc>
        <lastmod>2026-01-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>
```

#### 生成Sitemap的Node.js脚本
```javascript
const fs = require('fs');
const { SitemapStream, streamToPromise } = require('sitemap');
const { Readable } = require('stream');

async function generateSitemap() {
    const links = [
        { url: '/', changefreq: 'daily', priority: 1.0 },
        { url: '/about', changefreq: 'monthly', priority: 0.8 },
        { url: '/services/web-design', changefreq: 'weekly', priority: 0.9 },
        { url: '/services/seo', changefreq: 'weekly', priority: 0.9 },
        { url: '/blog', changefreq: 'daily', priority: 0.7 },
        { url: '/contact', changefreq: 'monthly', priority: 0.8 }
    ];

    const stream = new SitemapStream({ hostname: 'https://www.example.com' });
    const sitemap = await streamToPromise(Readable.from(links).pipe(stream));
    
    fs.writeFileSync('./public/sitemap.xml', sitemap.toString());
    console.log('✅ Sitemap生成成功');
}

generateSitemap();
```

### 5.3 Robots.txt

```txt
# Robots.txt for www.example.com

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/
Disallow: /*.json$
Disallow: /*?*sort=
Disallow: /*?*filter=

# 特殊爬虫
User-agent: Googlebot
Allow: /

User-agent: Baiduspider
Allow: /
Crawl-delay: 5

# 站点地图
Sitemap: https://www.example.com/sitemap.xml
Sitemap: https://www.example.com/sitemap-news.xml
Sitemap: https://www.example.com/sitemap-images.xml
```

### 5.4 .htaccess优化（Apache）

```apache
# 开启压缩
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# 浏览器缓存
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# 强制HTTPS
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

# 移除尾部斜杠
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)/$ /$1 [L,R=301]

# 添加尾部斜杠（二选一）
# RewriteCond %{REQUEST_FILENAME} !-f
# RewriteRule ^(.*[^/])$ /$1/ [L,R=301]
```

---

## 6. 内容优化策略

### 6.1 内容优化检查清单

#### 标题优化
```
✅ 包含主关键词
✅ 长度50-60字符
✅ 吸引点击
✅ 独特性
✅ 品牌名称（可选）

示例：
❌ "服务"
✅ "东京网站制作服务 - 专业企业建站 | 公司名"
```

#### 内容结构
```
H1 (1个)
├── H2 (主要章节)
│   ├── H3 (子章节)
│   │   └── H4
│   └── H3
├── H2
│   └── H3
└── H2
```

### 6.2 内容优化工具

#### **Yoast SEO Real-time Content Analysis**
```javascript
// 内容分析算法示例
function analyzeContent(content, keyword) {
    const analysis = {
        wordCount: content.split(/\s+/).length,
        keywordDensity: calculateKeywordDensity(content, keyword),
        readabilityScore: calculateReadability(content),
        headings: extractHeadings(content),
        suggestions: []
    };
    
    // 字数检查
    if (analysis.wordCount < 300) {
        analysis.suggestions.push('❌ 内容太短，建议至少300字');
    } else if (analysis.wordCount > 2000) {
        analysis.suggestions.push('⚠️ 内容较长，考虑分页或分成多篇');
    }
    
    // 关键词密度
    if (analysis.keywordDensity < 0.5) {
        analysis.suggestions.push('⚠️ 关键词密度过低，增加关键词使用');
    } else if (analysis.keywordDensity > 3) {
        analysis.suggestions.push('❌ 关键词密度过高，避免过度优化');
    }
    
    // H1检查
    const h1Count = (content.match(/<h1>/gi) || []).length;
    if (h1Count === 0) {
        analysis.suggestions.push('❌ 缺少H1标签');
    } else if (h1Count > 1) {
        analysis.suggestions.push('⚠️ 有多个H1标签，建议只有一个');
    }
    
    return analysis;
}
```

### 6.3 图片优化

#### 图片SEO检查清单
```html
<!-- ❌ 不好的图片标签 -->
<img src="img1.jpg">

<!-- ✅ 优化后的图片标签 -->
<img 
    src="/images/tokyo-web-design-services-2026.jpg"
    alt="东京网站制作服务展示 - 响应式网页设计案例"
    title="专业网站制作案例"
    width="800"
    height="600"
    loading="lazy"
>

<!-- ✅ 使用WebP格式 + 回退 -->
<picture>
    <source srcset="/images/hero.webp" type="image/webp">
    <source srcset="/images/hero.jpg" type="image/jpeg">
    <img 
        src="/images/hero.jpg" 
        alt="网站制作服务"
        width="1200"
        height="800"
        loading="lazy"
    >
</picture>
```

#### 图片压缩工具
```bash
# ImageMagick 批量压缩
mogrify -resize 1920x1920\> -quality 85 -format jpg *.jpg

# Node.js 自动化
npm install sharp

# compress-images.js
const sharp = require('sharp');
const fs = require('fs');

async function compressImages() {
    const files = fs.readdirSync('./images');
    
    for (const file of files) {
        if (file.match(/\.(jpg|jpeg|png)$/i)) {
            await sharp(`./images/${file}`)
                .resize(1920, 1920, { fit: 'inside', withoutEnlargement: true })
                .jpeg({ quality: 85 })
                .toFile(`./images/optimized/${file}`);
            
            console.log(`✅ 压缩完成: ${file}`);
        }
    }
}

compressImages();
```

---

## 7. WordPress SEO优化

### 7.1 必装SEO插件

#### **Yoast SEO** (推荐，免费)
🌐 https://yoast.com/

**功能：**
- 实时内容分析
- XML网站地图
- 面包屑导航
- 社交媒体优化
- 重定向管理

**基础设置：**
1. 安装激活 Yoast SEO
2. SEO → 常规 → 配置向导
3. SEO → 搜索外观 → 设置标题和描述模板
4. SEO → 社交 → 配置 Open Graph

#### **Rank Math** (替代方案，免费)
🌐 https://rankmath.com/

**优势：**
- 更现代的界面
- Google Search Console 集成
- 404监控
- 重定向管理
- 内置Schema生成器

#### **All in One SEO** (免费 + 付费)
**功能：**
- TruSEO分数
- 本地SEO
- WooCommerce支持

### 7.2 WordPress SEO设置

#### 基础设置（设置 → 常规）
```php
// 网站标题
"公司名称 - 东京专业网站制作服务"

// 副标题
"提供企业网站、电商平台、SEO优化等全方位服务"

// 时区
"Asia/Tokyo"
```

#### 固定链接设置（设置 → 固定链接）
```
✅ 推荐: /%postname%/
或
✅ /%category%/%postname%/

❌ 避免: ?p=123
```

#### functions.php优化
```php
<?php
// 移除WordPress版本号
remove_action('wp_head', 'wp_generator');

// 移除不必要的链接
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');

// 添加Open Graph支持
function add_og_tags() {
    if (is_single()) {
        global $post;
        ?>
        <meta property="og:type" content="article">
        <meta property="og:title" content="<?php echo get_the_title(); ?>">
        <meta property="og:description" content="<?php echo wp_trim_words(get_the_excerpt(), 30); ?>">
        <meta property="og:url" content="<?php echo get_permalink(); ?>">
        <?php if (has_post_thumbnail()) : ?>
        <meta property="og:image" content="<?php echo get_the_post_thumbnail_url(null, 'large'); ?>">
        <?php endif; ?>
        <?php
    }
}
add_action('wp_head', 'add_og_tags');

// 延迟加载图片
add_filter('the_content', function($content) {
    return str_replace('<img ', '<img loading="lazy" ', $content);
});

// 添加结构化数据
function add_schema_markup() {
    if (is_single()) {
        global $post;
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => get_the_title(),
            'datePublished' => get_the_date('c'),
            'dateModified' => get_the_modified_date('c'),
            'author' => array(
                '@type' => 'Person',
                'name' => get_the_author()
            )
        );
        echo '<script type="application/ld+json">' . json_encode($schema) . '</script>';
    }
}
add_action('wp_head', 'add_schema_markup');

// 优化数据库查询
define('WP_POST_REVISIONS', 3); // 限制修订版本
define('AUTOSAVE_INTERVAL', 300); // 自动保存间隔5分钟
?>
```

### 7.3 WordPress性能优化

#### 缓存插件（必装）
- **WP Super Cache** (免费)
- **W3 Total Cache** (免费)
- **WP Rocket** (付费，$49/年)

#### CDN服务
- **Cloudflare** (免费)
- **StackPath**
- **KeyCDN**

#### 图片优化插件
- **Smush** (免费 + 付费)
- **ShortPixel** (免费额度 + 付费)
- **Imagify** (付费)

---

## 📊 SEO成效追踪

### 关键指标 (KPIs)

| 指标 | 说明 | 目标 |
|------|------|------|
| **自然流量** | 搜索引擎来的访问 | 月增长10-20% |
| **关键词排名** | 目标关键词位置 | 前3页 → 前10 → 前3 |
| **点击率 (CTR)** | 展现转点击 | >3% |
| **跳出率** | 单页访问离开率 | <50% |
| **页面停留时间** | 用户停留时长 | >2分钟 |
| **转化率** | 访问转行动 | >2% |

### 追踪工具设置

#### Google Analytics 4 目标设置
```javascript
// 追踪表单提交
gtag('event', 'form_submit', {
    'event_category': 'Contact',
    'event_label': 'Contact Form'
});

// 追踪按钮点击
document.querySelector('.cta-button').addEventListener('click', function() {
    gtag('event', 'click', {
        'event_category': 'CTA',
        'event_label': 'Get Quote Button'
    });
});
```

---

## 💡 SEO最佳实践总结

### 每天
- ✅ 检查Google Search Console错误
- ✅ 回复用户评论
- ✅ 发布/更新内容

### 每周
- ✅ 分析流量和排名变化
- ✅ 检查断链
- ✅ 优化一个旧页面

### 每月
- ✅ 完整SEO审计
- ✅ 竞争对手分析
- ✅ 生成SEO报告
- ✅ 更新sitemap

### 每季度
- ✅ 关键词策略调整
- ✅ 内容战略评估
- ✅ 技术SEO升级

---

## 📚 推荐学习资源

### 官方文档
- [Google搜索中心](https://developers.google.com/search)
- [Google SEO入门指南](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Bing网站管理员指南](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)

### 博客和社区
- **Moz Blog** - https://moz.com/blog
- **Search Engine Journal** - https://www.searchenginejournal.com
- **Search Engine Land** - https://searchengineland.com
- **Backlinko** - https://backlinko.com/blog

### 工具文档
- [Yoast SEO文档](https://yoast.com/help/)
- [Screaming Frog教程](https://www.screamingfrog.co.uk/seo-spider/user-guide/)

---

**文档创建时间**: 2026年1月6日  
**适用场景**: 企业网站、博客、电商平台、内容网站  
**更新频率**: 每季度更新

---

*SEO是长期工程，需要持续优化和监控。建议配合专业SEO顾问服务获得更好效果。*
