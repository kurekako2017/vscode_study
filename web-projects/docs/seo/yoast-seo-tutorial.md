# Yoast SEO 插件使用与配置指南

> 本文为中文教程，面向 WordPress 站点管理员与内容编辑，介绍如何安装、配置、验证 Yoast SEO，以解决 meta 描述缺失、生成站点地图、管理社交摘要等常见 SEO 问题。

---

## 目录

- 安装与启用
- 初次配置向导
- 核心设置说明
- 为文章/页面设置 SEO
- 高级设置与验证
- 测试与排查
- 与缓存/优化插件的兼容性
- 常见问题与解决方案
- 快速检查清单

---

## 安装与启用

1. 登录 WordPress 后台，导航到“插件 → 安装插件”，在搜索框输入“Yoast SEO”。
2. 找到 `Yoast SEO — SEO for everyone`，点击“现在安装”，完成后点击“启用”。
3. 若无后台安装权限，可在官网下载 ZIP，后台“插件 → 安装插件 → 上传插件”上传并启用。
4. 多站点（Network）环境：建议由网络管理员在网络级别启用插件，然后在每个子站点上单独配置。

---

## 初次配置向导（Configuration Wizard）

首次启用后，Yoast 会在仪表盘显示向导入口，建议运行：

- 网站类型（个人/公司）
- 是否为多作者站点（决定作者页索引策略）
- 内容可见性建议（文章/页面等是否允许搜索引擎索引）
- 站点地图启用与默认行为

向导完成后，会生成基础的 meta 输出与站点地图。

---

## 核心设置说明

### 仪表盘（Dashboard）
- 提示插件状态与问题（例如：索引、社交配置提醒）。

### 常规 → 功能（Features）
- 建议开启：SEO 分析、可读性分析、XML 站点地图、面包屑、结构化数据等。

### 搜索外观（Search Appearance）

- **一般（General）**：设置站点名称、分隔符等。
- **内容类型（Content Types）**：为文章、页面等定义标题模板与 meta 描述模板（可使用变量如 `%%title%%`、`%%sep%%`、`%%sitename%%`）。
- **分类法（Taxonomies）**：控制分类、标签页面是否允许索引（很多站点建议将标签页设置为 `noindex`）。
- **档案（Archives）**：作者页、日期归档等（单作者站点可以将作者页设为 `noindex`）。

### XML 站点地图（XML Sitemaps）

- Yoast 会自动生成站点地图，通常入口为 `/sitemap_index.xml`。将该地址提交至 Google Search Console。可在插件设置中排除特定类型或分类。

### 社交（Social）

- 配置站点的社交账号（Facebook、Twitter 等），并设置默认的 Open Graph 与 Twitter Card 行为。确保文章中设置了合适的预览图（og:image）。

---

## 为每篇文章/页面设置 SEO

在编辑器页面，Yoast 面板提供以下字段：

- **SEO 标题（SEO title）**：建议 50–60 字符，包含目标关键词。
- **元描述（Meta description）**：建议 120–160 字符，写吸引点击的摘要。
- **焦点关键词（Focus keyphrase）**：填入目标关键字，Yoast 会给出优化建议。
- **可读性与 SEO 分析**：按面板的提示优化段落长度、句子结构、内链等。

实时预览会显示搜索结果中标题与描述的展示效果。

---

## 高级设置与验证

### 面包屑（Breadcrumbs）

- 若你希望站点显示面包屑导航，可在 Yoast 中启用并将主题模板里插入 Yoast 的面包屑函数，或使用主题中自带的面包屑支持。具体实现请参考主题开发文档。

### Schema（结构化数据）

- Yoast 会输出 JSON-LD 格式的 Schema（例如 Article、Organization、Website 等），可在页面源码中查找 `application/ld+json` 块来验证。

### 站长工具验证（Google/Bing）

- 在 Yoast → 常规 → 工具/功能 找到 Webmaster Tools 验证字段，将 Google/Bing 等验证 meta 粘贴至相应框，保存后在 Search Console/站长工具完成验证。

---

## 测试与排查

1. 在前端页面右键“查看页面源代码”，确认是否有 `<meta name="description">`、`<link rel="canonical">`、`<script type="application/ld+json">` 等 Yoast 输出的标签。
2. 使用 Chrome DevTools 的 Lighthouse 报告检查 SEO 项目（meta 描述、可抓取链接、移动可用性等）。
3. 在 Google Search Console 中提交站点地图并查看覆盖率、抓取错误。
4. 若 Lighthouse 或 Search Console 仍然报告 `javascript:void(0)` 链接或无 meta 描述：
   - 清除所有缓存（页面缓存、CDN 缓存）。
   - 确认最终生成的 HTML（而非编辑器源码）是否存在问题。
   - 若链接由 JS 动态生成，定位对应脚本或插件并修复（将 `javascript:void(0)` 替换为 `#` 或实际 URL`）。

---

## 与缓存/压缩/优化插件的兼容性

- 在配置与调试阶段请临时关闭 HTML 最小化或合并，以避免压缩过程移除或篡改头部 meta 标签。
- 任何对 `wp_head()` 输出进行修改的插件或主题，都可能影响 Yoast 的标签输出。

---

## 常见问题与解决方案

- **Meta 描述缺失**：检查 Yoast 是否启用，对应内容类型是否被设置为 `noindex`，并确认主题未移除 `wp_head()`。也可检查是否有其他 SEO 插件冲突。
- **站点地图未更新**：清空站点缓存，禁用相关缓存功能后强制刷新 Yoast 站点地图，或短时禁用缓存插件排查。
- **社交预览图片不显示**：检查文章是否设置 `featured image` 或 Yoast 的社交图片字段；使用 Facebook Sharing Debugger 强制抓取最新数据。

---

## 快速检查清单（部署后验证）

1. 页面源码包含 `<meta name="description">`。
2. 文章页面包含合适的 `og:image` 和 Twitter Card。
3. 站点地图 `/sitemap_index.xml` 可访问并已提交到 Search Console。
4. 在 Lighthouse 中“内容最佳做法”不再报 meta 描述缺失和无效链接警告。

---

## 参考链接

- Yoast 官方文档: https://yoast.com/help/
- Google Search Console 帮助: https://support.google.com/webmasters
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/

---

如果你需要我把该文档放到仓库的特定子目录或生成一个精简版的“速查卡”，告诉我路径和格式偏好即可。