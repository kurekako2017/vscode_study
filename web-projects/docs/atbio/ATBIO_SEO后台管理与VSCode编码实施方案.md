# ATBIO SEO 实施方案：后台管理 vs VS Code 编码修改

## 1. 结论先说

ATBIO 网站的 SEO 不应该只靠后台，也不应该全部靠写代码。

最佳方案是：

```text
后台管理负责：内容型 SEO
VS Code 编码负责：技术型 SEO
第三方工具负责：监控、收录、速度、安全
```

也就是：

```text
后台 SEO：Title / Description / Keywords / Sitemap / Robots
模板代码 SEO：Canonical / hreflang / OpenGraph / Schema / H标签 / Alt标签
第三方工具：Google Search Console / GA4 / Cloudflare / Clarity
```

---

## 2. 当前网站真实情况

根据目前网站模板结构：

```text
template/default/pc
├── header.htm
├── footer.htm
├── index.htm
├── lists_single.htm
├── lists_product.htm
├── view_product.htm
```

说明 ATBIO 网站是：

```text
PHP CMS + 模板系统 + 后台管理 + MySQL数据库
```

后台主要管理内容，模板文件主要控制页面结构。

---

## 3. 后台管理适合做什么 SEO

后台适合修改这些内容：

### 3.1 首页 SEO

位置：

```text
后台 → 设置 → SEO管理 / TDK管理
```

负责：

```text
首页 Title
首页 Keywords
首页 Description
```

模板中对应：

```html
<title>{zan:global name='web_title' /}</title>
<meta name="keywords" content="{zan:global name='web_keywords' /}" />
<meta name="description" content="{zan:global name='web_description' /}" />
```

---

### 3.2 栏目页 SEO

例如：

```text
Product
Composite Resins
Brand
News
About Us
Contact
```

后台可以设置：

```text
SEO标题
SEO关键词
SEO描述
```

模板中对应：

```html
<title>{$zan.field.seo_title}</title>
<meta name="keywords" content="{$zan.field.seo_keywords}" />
<meta name="description" content="{$zan.field.seo_description}" />
```

---

### 3.3 产品页 SEO

后台适合修改：

```text
产品名称
产品描述
产品关键词
产品图片
产品详情
FAQ
说明书
Brochure
```

模板中产品详情页已经使用：

```html
<h1>{$zan.field.title}</h1>
<img src="{$zan.field.litpic}" alt="{$zan.field.seo_title}">
```

所以产品页后台内容填写得越完整，SEO效果越好。

---

### 3.4 Sitemap

后台可以开启：

```text
Sitemap
```

当前后台已经显示：

```text
https://www.atmbio.com/sitemap.xml
https://www.atmbio.com/siteurls.txt
https://www.atmbio.com/sitemap.html
```

建议保持开启。

---

### 3.5 Robots

后台可以维护：

```text
robots.txt
```

建议允许搜索引擎抓取前台页面，禁止后台目录。

示例：

```txt
User-agent: *
Disallow: /login.php
Disallow: /application/
Disallow: /core/
Disallow: /data/
Allow: /
Sitemap: https://www.atmbio.com/sitemap.xml
```

---

## 4. VS Code 编码适合做什么 SEO

后台无法完成的 SEO，需要改模板代码。

推荐使用：

```text
VS Code + Remote SSH
```

直接打开：

```text
/www/www/atmbio.com/template/default/pc
```

---

## 5. 必须用 VS Code 修改的 SEO 项目

### 5.1 Canonical

作用：

防止重复页面被 Google 误判。

建议在：

```text
index.htm
lists_single.htm
lists_product.htm
view_product.htm
```

的 `<head>` 中加入。

示例：

```html
<link rel="canonical" href="https://www.atmbio.com/current-page-url/" />
```

如果 CMS 有当前 URL 标签，应使用动态变量。

---

### 5.2 hreflang

以后追加日语、中文时必须加。

作用：

告诉 Google 不同语言版本之间的对应关系。

示例：

```html
<link rel="alternate" hreflang="en" href="https://www.atmbio.com/" />
<link rel="alternate" hreflang="ja" href="https://www.atmbio.com/ja/" />
<link rel="alternate" hreflang="zh" href="https://www.atmbio.com/zh/" />
<link rel="alternate" hreflang="x-default" href="https://www.atmbio.com/" />
```

建议位置：

```text
header.htm 或每个页面模板的 head 区域
```

注意：如果不同页面要对应不同语言 URL，最好用动态变量生成，而不是全部写首页。

---

### 5.3 OpenGraph

作用：

让页面分享到 Facebook、LinkedIn、WhatsApp 时显示正确标题、描述、图片。

示例：

```html
<meta property="og:type" content="website" />
<meta property="og:title" content="{$zan.field.seo_title}" />
<meta property="og:description" content="{$zan.field.seo_description}" />
<meta property="og:image" content="https://www.atmbio.com/static/img/share.jpg" />
<meta property="og:url" content="https://www.atmbio.com/current-page-url/" />
```

首页可以用：

```html
<meta property="og:title" content="{zan:global name='web_title' /}" />
<meta property="og:description" content="{zan:global name='web_description' /}" />
```

---

### 5.4 Twitter Card

示例：

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{$zan.field.seo_title}" />
<meta name="twitter:description" content="{$zan.field.seo_description}" />
<meta name="twitter:image" content="https://www.atmbio.com/static/img/share.jpg" />
```

---

### 5.5 Schema 结构化数据

这是后台一般做不了的。

#### Organization Schema

适合放在全站。

位置：

```text
header.htm 或 footer.htm
```

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ATBIO",
  "url": "https://www.atmbio.com/",
  "logo": "https://www.atmbio.com/static/img/logo.png",
  "sameAs": [
    "LinkedIn URL",
    "Facebook URL",
    "YouTube URL"
  ]
}
</script>
```

---

#### Product Schema

适合放在：

```text
view_product.htm
```

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{$zan.field.title}",
  "description": "{$zan.field.seo_description}",
  "image": "https://www.atmbio.com{$zan.field.litpic}",
  "brand": {
    "@type": "Brand",
    "name": "ATBIO"
  }
}
</script>
```

---

#### FAQ Schema

你的产品详情页已经有 FAQ：

```text
{zan:faq group_id='1'}
```

所以可以进一步加 FAQ Schema。

适合放在：

```text
view_product.htm
```

作用：

让 Google 更好理解产品问答内容。

---

### 5.6 图片 Alt 优化

后台能改一部分，但模板也要保证所有图片都有 alt。

已经比较好的地方：

```html
<img src="{$field.litpic}" alt="{$field.title}" loading="lazy">
```

需要继续检查：

```html
<img src="/static/img/xxx.webp" alt="">
```

静态图片需要手动补充有意义的 alt。

---

### 5.7 H 标签结构

建议：

每个页面只有一个 H1。

产品详情页当前已经比较好：

```html
<h1>{$zan.field.title}</h1>
```

但是首页、About、产品列表页要继续检查：

```text
首页：建议 H1 表达品牌核心关键词
About：页面标题可以用 H1
产品列表：分类标题可以用 H1
模块标题用 H2
卡片标题用 H3
```

---

## 6. 第三方工具适合做什么

### 6.1 Google Search Console

必须接入。

作用：

```text
提交 sitemap
查看收录
查看关键词
查看抓取错误
查看页面体验
```

---

### 6.2 Google Analytics 4

建议接入。

作用：

```text
分析访问量
分析国家地区
分析流量来源
分析询盘转化
```

---

### 6.3 Google Tag Manager

推荐接入。

作用：

统一管理：

```text
GA4
Google Ads
Meta Pixel
事件追踪
按钮点击
表单提交
```

---

### 6.4 Microsoft Clarity

当前 header.htm 已经接入 Clarity。

作用：

```text
热力图
用户录屏
点击分析
滚动分析
```

可以继续保留。

---

### 6.5 Cloudflare

推荐接入。

作用：

```text
CDN加速
HTTPS
缓存
防攻击
辅助DNS管理
```

对海外访问和 SEO 都有帮助。

> 如果当前域名和 DNS 解析已经在阿里云控制台管理，那么域名记录、Nameserver 和续费仍应以阿里云为准，Cloudflare 只是可选的额外接入层，不是当前主入口。

---

## 7. 多语言网页方案

### 7.1 当前网站已经有多语言基础

header.htm 中已有语言切换逻辑：

```html
{zan:language type='list'}
<a href="{$field.pageurl}">
  <option value="{$field.title}">{$field.title}</option>
</a>
{/zan:language}
```

说明 CMS 已经支持多语言列表。

---

### 7.2 推荐 URL 方案

最推荐：

```text
英文：https://www.atmbio.com/
日文：https://www.atmbio.com/ja/
中文：https://www.atmbio.com/zh/
```

不要优先使用：

```text
jp.atmbio.com
atmbio.jp
```

因为目录模式更容易集中 SEO 权重。

---

### 7.3 新增日语站步骤

#### 第一步：后台开启多语言

进入：

```text
后台 → 网站设置 / 多语言 / 语言管理
```

新增：

```text
日语 JA
```

---

#### 第二步：复制栏目

复制英文栏目结构：

```text
Product
Education
News
About Us
Contact
```

到日语站。

---

#### 第三步：翻译页面内容

优先顺序：

```text
首页
Product
产品详情
About Us
Contact
FAQ
News
Education
```

---

#### 第四步：翻译 SEO

每个页面都要翻译：

```text
SEO标题
SEO描述
SEO关键词
```

不要只翻正文，不翻 SEO。

---

#### 第五步：增加 hreflang

在模板中增加语言对应关系。

---

#### 第六步：生成日语 sitemap

例如：

```text
https://www.atmbio.com/ja/sitemap.xml
```

或者 CMS 自动生成多语言 sitemap。

---

#### 第七步：提交 Google Search Console

分别提交：

```text
https://www.atmbio.com/sitemap.xml
https://www.atmbio.com/ja/sitemap.xml
```

---

## 8. 后台 vs 编码 vs 第三方工具分工表

| SEO项目 | 后台管理 | VS Code编码 | 第三方工具 |
|---|---|---|---|
| Title | ✅ | ❌ | ❌ |
| Description | ✅ | ❌ | ❌ |
| Keywords | ✅ | ❌ | ❌ |
| Sitemap | ✅ | ⚠️ | ✅提交 |
| Robots | ✅ | ⚠️ | ✅检测 |
| Canonical | ❌ | ✅ | ✅检测 |
| hreflang | ❌ | ✅ | ✅检测 |
| OpenGraph | ❌ | ✅ | ✅检测 |
| Twitter Card | ❌ | ✅ | ✅检测 |
| Schema | ❌ | ✅ | ✅检测 |
| H标签 | ⚠️ | ✅ | ✅检测 |
| 图片Alt | ⚠️ | ✅ | ✅检测 |
| 页面速度 | ❌ | ✅ | ✅检测 |
| CDN | ❌ | ⚠️ | ✅ |
| 收录情况 | ❌ | ❌ | ✅ |
| 关键词排名 | ❌ | ❌ | ✅ |

---

## 9. 推荐实施路线

### 第一阶段：安全备份

先备份：

```text
/www/www/atmbio.com
数据库 SQL
template/default/pc
```

---

### 第二阶段：后台 SEO 完善

后台逐个填写：

```text
首页 SEO
产品分类 SEO
产品详情 SEO
About Us SEO
Contact SEO
News SEO
Education SEO
```

---

### 第三阶段：模板 SEO 改造

用 VS Code 修改：

```text
index.htm
lists_single.htm
lists_product.htm
view_product.htm
header.htm
footer.htm
```

增加：

```text
Canonical
OpenGraph
Twitter Card
Schema
hreflang
```

---

### 第四阶段：第三方工具接入

接入：

```text
Google Search Console
Google Analytics 4
Google Tag Manager
Cloudflare
```

---

### 第五阶段：追加日语网页

新增：

```text
/ja/
```

并完整翻译：

```text
页面内容
产品内容
FAQ
SEO标题
SEO描述
图片Alt
```

---

## 10. 本地开发与数据库说明

### 这套站点最适合怎么开发

ATBIO 网站不是纯内容站，它更像是：

```text
CMS后台 + 模板系统 + MySQL数据库 + 服务器文件
```

所以开发方式应该分层：

| 修改类型 | 推荐位置 | 说明 |
| --- | --- | --- |
| 内容更新 | CMS 后台 | 产品、新闻、页面文案、SEO、询盘 |
| 结构调整 | 本地 VS Code | 模板、样式、交互、页面结构 |
| 运行配置 | 小皮面板 / VPS | Nginx、PHP、SSL、数据库、部署 |

### 本地 VS Code 是不是主要开发方式

是，尤其适合模板开发和整站定制。

本地开发的典型方式不是“只写几个 HTML”，而是把整站目录拉到本地后，在 VS Code 里维护：

```text
template
static
application（必要时）
uploads（资源引用）
```

这样做的优点是：

| 优点 | 说明 |
| --- | --- |
| 可批量搜索修改 | 适合大范围重构和统一风格 |
| 便于版本管理 | 可以配合 Git 做回滚 |
| 不会直接影响线上 | 先在本地验证，再同步 |
| 便于团队协作 | 多人开发时更容易统一规范 |

### `atmbio.com` 目录是不是可以直接拿来整站开发

可以，但前提是把整站开发所需的资源补齐。

你从小皮面板下载下来的 `atmbio.com` 目录，通常包含：

```text
PHP 程序
template 模板
static 静态资源
部分 uploads 资源
```

但这还不算完整的开发环境，因为还缺：

| 还需要什么 | 原因 |
| --- | --- |
| 数据库 SQL | 页面内容、栏目、产品、SEO 都在库里 |
| 本地 MySQL | 需要运行和验证数据读写 |
| 本地 PHP 环境 | 需要让 CMS 跑起来 |
| 配置文件 | 需要把本地库和线上库区分开 |
| 完整 uploads | 图片、PDF、Banner 等资源需要同步 |

所以结论是：

| 问题 | 答案 |
| --- | --- |
| 本地能不能重新定制整站 | 能 |
| 本地主要是不是开发模板 | 是，日常最常见 |
| 本地能不能做功能重构 | 能，但要同步数据库和程序逻辑 |
| 本地只拿一个目录够不够 | 不够，最好配数据库和资源文件 |

### 数据库是不是这个网站正在用的

从你截图看，小皮面板的数据库页显示了一个名为 `atmbio` 的 MySQL 库，并且用户名也是 `atmbio`。结合当前站点目录和已有 SQL 备份，可以判断这就是 ATBIO 站点正在使用的主库，属于当前服务器上的本地 MySQL 数据库。

这意味着：

| 结论 | 说明 |
| --- | --- |
| 这是站点正在使用的数据库 | 页面内容、产品、栏目都依赖它 |
| 它不是单独的第三方云数据库 | 更像是 VPS 上的本地 MySQL |
| CMS 后台改内容实际上就是改它的数据 | 后台保存后会写入这个库 |

### 本地开发时数据库怎么处理

推荐两种方式：

| 方式 | 建议等级 | 适合场景 |
| --- | --- | --- |
| 导出线上数据库，导入本地 MySQL | 推荐 | 日常开发、模板调整、结构重构 |
| 直接连接线上数据库 | 不推荐长期使用 | 临时排查、紧急核对、只读检查 |

推荐流程：

```text
小皮面板导出 atmbio 数据库
  ↓
导入本地 MySQL
  ↓
VS Code 打开整站副本
  ↓
修改模板和静态资源
  ↓
本地验证页面和数据库逻辑
  ↓
同步到线上
```

### 为什么不建议长期直连生产库

| 风险 | 说明 |
| --- | --- |
| 误删数据 | 本地调试时可能不小心写入或删除生产数据 |
| 并发冲突 | 多人同时操作时容易互相覆盖 |
| 环境不一致 | 本地和线上 PHP / MySQL 版本可能不同 |
| 备份困难 | 直接连生产库不利于回滚 |

### 配置文件的理解

项目里能看到 `database.php_read` 这类占位配置，说明真实数据库参数通常是在部署后写入或替换的。

这类项目的推荐做法是：

| 建议 | 说明 |
| --- | --- |
| 线上参数单独管理 | 不把生产密码硬写在公开仓库里 |
| 本地单独配置数据库 | 本地开发使用本地库 |
| 同步前先备份 | 避免配置覆盖错误 |
| 模板和数据库分开管理 | 便于回滚和迁移 |

## 11. 最终建议

ATBIO 当前最佳方案：

```text
后台：负责内容和TDK
VS Code：负责模板级SEO
第三方工具：负责监控、收录、性能和数据分析
```

不要只依赖后台。

后台只能完成基础 SEO，大约占 20% 到 30%。

真正能提升 Google 排名的，是：

```text
模板结构
结构化数据
多语言 hreflang
内容质量
页面速度
Google Search Console 数据反馈
```

所以长期维护时，应该把 SEO 当成一个组合工程，而不是只点后台几个按钮。
