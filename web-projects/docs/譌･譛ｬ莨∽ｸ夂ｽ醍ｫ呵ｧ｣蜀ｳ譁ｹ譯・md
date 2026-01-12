# 日本企业网站完整开发指南 🇯🇵

> **目标**: 最低成本快速开发上线  
> **现有资源**: onamae.com RSプラン WordPress服务器  
> **必备功能**: 新闻发布、联系表单、邮件发送

---

## 📊 方案对比表

| 方案 | 开发时间 | 成本 | 难度 | 推荐度 |
|------|----------|--------|--------|------------|
| **方案1: WordPress单独方案** | 2-3天 | ¥0 | ⭐ | ⭐⭐⭐⭐⭐ |
| **方案2: Bootstrap Studio + WordPress** | 3-5天 | $60 | ⭐⭐ | ⭐⭐⭐⭐ |
| **方案3: VSCode + WordPress联动** | 4-7天 | ¥0 | ⭐⭐⭐ | ⭐⭐⭐ |
| **方案4: Elementor Pro（推荐）** | 1-2天 | $59/年 | ⭐ | ⭐⭐⭐⭐⭐ |

---

## 🏆 方案1: WordPress单独方案【最推荐】

### ✅ 优势
- **完全免费** (使用现有服务器)
- **最快实现** (2-3天完成)
- **日语完美支持** (主题众多)
- **插件实现全部功能**

### 📦 所需内容
1. **主题**: Lightning (免费・日本制作)
2. **表单插件**: Contact Form 7 (免费)
3. **新闻功能**: WordPress标准功能
4. **邮件发送**: WP Mail SMTP (免费)

### 🚀 实施步骤

#### Step 1: WordPress配置 (30分钟)

```bash
# 登录onamae.com RSプラン
# 使用WordPress自动安装功能
# 推荐设置:
# - 网站名称: 公司名
# - 用户名: 不要用admin
# - 密码: 使用强密码
```

#### Step 2: 主题安装 (15分钟)

```
WordPress管理后台 → 外观 → 主题 → 添加新主题
搜索: "Lightning"
安装 → 启用

推荐的日本企业主题:
1. Lightning (免费) - 最适合日本企业
2. Xeory Extension (免费) - SEO已优化
3. Cocoon (免费) - 功能丰富
4. Business Press (免费) - 商务专用
```

#### Step 3: 必装插件安装 (30分钟)

```
插件 → 添加新插件

【必装插件】
1. Contact Form 7 - 联系表单
2. WP Mail SMTP - 邮件发送设置
3. VK All in One Expansion Unit - Lightning扩展功能
4. SiteGuard WP Plugin - 安全防护
5. EWWW Image Optimizer - 图片优化

【可选插件】
6. Yoast SEO - SEO优化
7. UpdraftPlus - 备份
8. WP Super Cache - 缓存
```

#### Step 4: 联系表单设置 (20分钟)

```
Contact Form 7 → 添加新表单

【日本企业标准表单】
<label> 姓名 (必填)
[text* your-name] </label>

<label> 公司名
[text your-company] </label>

<label> 邮箱地址 (必填)
[email* your-email] </label>

<label> 电话号码
[tel your-phone] </label>

<label> 咨询内容 (必填)
[textarea* your-message] </label>

[submit "提交"]

【邮件设置】
收件人: info@yourcompany.co.jp
发件人: wordpress@yourcompany.co.jp
主题: [咨询] 来自[your-name]
```

#### Step 5: 邮件发送设置 (30分钟)

```
WP Mail SMTP → 设置

【onamae.com邮件服务器设置】
发送方式: Other SMTP
SMTP主机: mail.onamae.com
SMTP端口: 465
加密: SSL
认证: ON
SMTP用户名: info@yourcompany.co.jp
SMTP密码: [邮箱密码]

【测试发送】
设置 → 邮件测试 → 发送测试邮件
```

#### Step 6: 新闻功能设置 (30分钟)

```
# 使用WordPress的文章功能作为"新闻"

设置 → 文章设置
添加分类:
- 通知
- 新闻稿
- 活动信息
- 产品信息

固定页面创建:
1. 新闻列表页面
2. 首页显示最新3条新闻

【短代码示例】
在首页插入:
[display-posts posts_per_page="3" include_excerpt="true"]
```

#### Step 7: 页面创建 (2-3小时)

```
【日本企业标准页面结构】
1. 首页 (HOME)
2. 公司简介 (Company)
3. 业务内容 (Business)
4. 产品·服务 (Products/Services)
5. 新闻 (News)
6. 招聘信息 (Recruit)
7. 联系我们 (Contact)
8. 隐私政策 (Privacy)

每个页面创建:
固定页面 → 添加新页面
使用Lightning的页面编辑器创建
```

### 💰 成本明细

```
初期费用: ¥0
月费: ¥0 (使用现有服务器)
年费: ¥0

※onamae.com RSプラン费用包含在现有合同中
```

### 📱 响应式适配

```
Lightning主题自动适配
确认方法:
- 手机显示: F12 → 设备工具栏
- 平板显示: 调整尺寸确认
```

---

## 🎨 方案2: Bootstrap Studio + WordPress

### 📋 概要
- **Bootstrap Studio**: 静态HTML设计创建
- **WordPress**: 内容管理·表单·新闻功能

### 角色分工

```
【Bootstrap Studio】60%
- 首页设计
- 企业信息页面
- 产品介绍页面
- 响应式布局
- 自定义动画

【WordPress】40%
- 新闻文章管理
- 联系表单
- 邮件发送功能
- 管理后台更新
```

### 🚀 实施步骤

#### Phase 1: Bootstrap Studio设计 (2天)

```bash
# 1. Bootstrap Studio安装
# 价格: $60 (买断)
# 下载: https://bootstrapstudio.io/

# 2. 选择日本企业模板
File → New from Template
推荐模板:
- Corporate Template
- Business Template
- Professional Template
```

#### Phase 2: 页面创建

```html
<!-- 首页结构示例 -->
1. 头部导航
   - 公司Logo
   - 菜单 (公司简介/业务内容/新闻/招聘/联系)
   - 语言切换 (日语/English)

2. 主视觉
   - 幻灯片 (3-5张)
   - 宣传口号
   - CTA按钮

3. 业务介绍区域
   - 3列布局
   - 图标 + 文字

4. 最新新闻 (WordPress联动部分)
   - 显示3条
   - "查看更多"链接

5. 公司简介
   - 简要信息
   - 地图

6. 页脚
   - 公司信息
   - SNS链接
   - 隐私政策
```

#### Phase 3: WordPress主题化 (1天)

```bash
# 1. Bootstrap Studio → 导出
File → Export → Custom Code

# 2. 文件结构转换
static-site/
├── index.html
├── css/
├── js/
└── images/

↓ 转换 ↓

wordpress-theme/
├── style.css
├── index.php
├── header.php
├── footer.php
├── functions.php
├── page-templates/
├── css/
├── js/
└── images/
```

#### Phase 4: WordPress集成

```php
// functions.php - 基本设置
<?php
function custom_theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    
    register_nav_menus(array(
        'primary' => '主菜单',
        'footer' => '页脚菜单'
    ));
}
add_action('after_setup_theme', 'custom_theme_setup');

// 样式加载
function custom_scripts() {
    wp_enqueue_style('bootstrap', get_template_directory_uri() . '/css/bootstrap.min.css');
    wp_enqueue_style('main-style', get_stylesheet_uri());
    wp_enqueue_script('bootstrap-js', get_template_directory_uri() . '/js/bootstrap.bundle.min.js', array('jquery'), null, true);
}
add_action('wp_enqueue_scripts', 'custom_scripts');
?>
```

```php
// index.php - 新闻列表显示
<?php get_header(); ?>

<div class="container mt-5">
    <h1>新闻</h1>
    
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article class="mb-4">
            <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p class="text-muted"><?php the_date(); ?></p>
            <?php the_excerpt(); ?>
        </article>
    <?php endwhile; endif; ?>
</div>

<?php get_footer(); ?>
```

### 💰 成本明细

```
Bootstrap Studio: $60 (买断)
WordPress: ¥0
插件: ¥0
总初期费用: $60 (约¥9,000)
月费: ¥0
```

---

## 💻 方案3: VSCode + WordPress联动

### 📋 概要
VSCode本地开发 → 同步到WordPress服务器

### 角色分工

```
【VSCode】开发环境
- HTML模板创建
- CSS/JavaScript自定义
- Git版本管理
- FTP/SFTP文件同步

【WordPress】生产环境
- 内容管理
- 插件功能
- 数据库管理
```

### 🚀 实施步骤

#### Step 1: VSCode环境构建 (30分钟)

```bash
# 1. 确认VSCode已安装
code --version

# 2. 安装必要扩展
- PHP Intelephense
- WordPress Snippets
- SFTP/FTP Sync
- Live Server
- Prettier - Code formatter
```

#### Step 2: 本地开发环境

```bash
# 项目结构
mkdir japan-corporate-site
cd japan-corporate-site

japan-corporate-site/
├── wp-content/
│   └── themes/
│       └── corporate-theme/
│           ├── style.css
│           ├── index.php
│           ├── header.php
│           ├── footer.php
│           ├── functions.php
│           ├── page-templates/
│           │   ├── front-page.php
│           │   ├── page-about.php
│           │   └── page-contact.php
│           ├── css/
│           │   └── custom.css
│           ├── js/
│           │   └── custom.js
│           └── images/
└── .vscode/
    └── sftp.json
```

#### Step 3: SFTP设置

```json
// .vscode/sftp.json
{
    "name": "onamae.com WordPress",
    "host": "your-server.onamae.com",
    "protocol": "sftp",
    "port": 22,
    "username": "your-username",
    "password": "your-password",
    "remotePath": "/home/your-username/public_html/wp-content/themes/corporate-theme",
    "uploadOnSave": true,
    "ignore": [
        ".vscode",
        ".git",
        "node_modules"
    ]
}
```

#### Step 4: 主题开发

```css
/* style.css - WordPress主题头部 */
/*
Theme Name: Japan Corporate Theme
Theme URI: https://yourcompany.co.jp
Description: 日本企业专用主题
Author: Your Name
Version: 1.0
License: GNU General Public License v2 or later
Text Domain: japan-corporate
*/

/* 自定义样式 */
:root {
    --primary-color: #003366;
    --secondary-color: #0066cc;
    --text-color: #333333;
}

body {
    font-family: 'Noto Sans JP', sans-serif;
    color: var(--text-color);
}

.hero-section {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 100px 0;
}
```

```php
// front-page.php - 首页模板
<?php
/*
Template Name: Front Page
*/
get_header();
?>

<section class="hero-section">
    <div class="container">
        <h1>将您的业务<br>推向下一阶段</h1>
        <p class="lead">以创新解决方案支持企业成长</p>
        <a href="#contact" class="btn btn-light btn-lg">立即咨询</a>
    </div>
</section>

<section class="news-section py-5">
    <div class="container">
        <h2 class="text-center mb-4">最新新闻</h2>
        <div class="row">
            <?php
            $news_query = new WP_Query(array(
                'post_type' => 'post',
                'posts_per_page' => 3
            ));
            
            if ($news_query->have_posts()) :
                while ($news_query->have_posts()) : $news_query->the_post();
            ?>
                <div class="col-md-4">
                    <div class="card">
                        <?php if (has_post_thumbnail()) : ?>
                            <?php the_post_thumbnail('medium', array('class' => 'card-img-top')); ?>
                        <?php endif; ?>
                        <div class="card-body">
                            <p class="text-muted"><?php the_date(); ?></p>
                            <h5 class="card-title"><?php the_title(); ?></h5>
                            <p class="card-text"><?php the_excerpt(); ?></p>
                            <a href="<?php the_permalink(); ?>" class="btn btn-primary">查看详情</a>
                        </div>
                    </div>
                </div>
            <?php
                endwhile;
                wp_reset_postdata();
            endif;
            ?>
        </div>
    </div>
</section>

<?php get_footer(); ?>
```

#### Step 5: 同步与部署

```bash
# VSCode命令面板 (Ctrl+Shift+P)
SFTP: Sync Local -> Remote

# 或者右键
右键 → Upload Folder
```

### 💰 成本明细

```
VSCode: ¥0 (免费)
插件: ¥0 (免费)
开发时间: 4-7天
月费: ¥0
```

---

## ⚡ 方案4: Elementor Pro【超高速开发】

### ✅ 为什么最快？

```
1. 拖拽式操作即可完成
2. 丰富的日语模板
3. 内置表单功能
4. 响应式自动适配
5. 无需编程知识
```

### 🚀 实施步骤 (1-2天完成)

#### Step 1: Elementor Pro购买 (10分钟)

```
价格: $59/年 (约¥9,000)
官网: https://elementor.com/pricing/
方案: Essential ($59/年・1站点)
```

#### Step 2: 安装 (15分钟)

```
WordPress管理后台
插件 → 添加新插件 → 搜索"Elementor"
1. Elementor (免费版) - 安装
2. Elementor Pro - 输入许可证密钥
```

#### Step 3: 模板选择 (30分钟)

```
Elementor → 模板 → 模板库

日本企业向模板:
1. Corporate Business
2. Professional Services
3. Consulting Firm
4. Technology Company

选择 → 导入 → 开始自定义
```

#### Step 4: 页面创建 (3-4小时)

```
【超高速创建步骤】
1. 插入模板
2. 点击文字修改为公司信息
3. 拖拽图片替换
4. 更改配色方案 (品牌颜色)
5. 点击发布按钮

完成!
```

#### Step 5: 表单设置 (30分钟)

```
Elementor Pro表单组件:
1. 拖拽表单组件
2. 添加字段:
   - 姓名
   - 公司名
   - 邮箱地址
   - 电话号码
   - 咨询内容
3. Actions设置:
   - Email: info@yourcompany.co.jp
   - Email2: 自动回复邮件
4. SMTP设置: WP Mail SMTP联动
```

### 💰 成本明细

```
Elementor Pro: $59/年
初期费用: ¥9,000
月费: ¥0
年费: ¥9,000/年
```

---

## 📧 免费邮件·新闻功能实现

### 方法1: Contact Form 7 + WP Mail SMTP (完全免费)

```
【联系表单】
插件: Contact Form 7
设置时间: 20分钟
功能: 表单提交、自动回复

【邮件发送】
插件: WP Mail SMTP
设置时间: 30分钟
支持: onamae.com邮件服务器

【新闻发布】
功能: WordPress标准文章功能
RSS发布: 自动生成
分类: 通知/新闻稿/活动
```

### 方法2: Mailchimp联动 (有免费额度)

```
免费方案: 每月2,000封
插件: MC4WP (免费)

设置步骤:
1. 创建Mailchimp账户
2. 获取API密钥
3. 安装MC4WP
4. 创建表单
5. 邮件发送设置

【优势】
- 专业的邮件设计
- 打开率·点击率分析
- 自动发送设置
```

### 方法3: Sendinblue (免费: 300封/天)

```
插件: Sendinblue (免费)

功能:
✅ 事务邮件 (无限制)
✅ 营销邮件 (300封/天)
✅ SMS发送
✅ 聊天功能

设置:
1. Sendinblue注册
2. 插件安装
3. API密钥联动
4. 发件人设置
```

---

## 🚀 部署设置

### onamae.com RSプラン设置

```bash
【FTP/SFTP信息】
主机: ftp.your-domain.com
端口: 21 (FTP) / 22 (SFTP)
用户名: [合同时的用户名]
密码: [设置的密码]
根目录: /public_html/

【WordPress URL设置】
设置 → 常规设置
WordPress地址: https://yourcompany.co.jp
站点地址: https://yourcompany.co.jp

【SSL证书】
onamae.com管理后台 → SSL设置
启用Let's Encrypt (免费)

【.htaccess设置】
# HTTPS强制重定向
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
```

### 备份设置

```
插件: UpdraftPlus (免费)

自动备份设置:
- 计划: 每天
- 保存位置: Google Drive / Dropbox (免费)
- 保留期间: 30天份

手动备份:
管理后台 → UpdraftPlus → 立即备份
```

---

## 📊 方案选择流程图

```
有编程经验吗？
├─ 有 → 想要技术挑战？
│   ├─ 是 → 【方案3】VSCode + WordPress
│   └─ 否 → 【方案1】WordPress单独
│
└─ 无 → 有预算吗？($60)
    ├─ 有 → 重视设计？
    │   ├─ 是 → 【方案4】Elementor Pro (最快)
    │   └─ 否 → 【方案2】Bootstrap Studio
    │
    └─ 无 → 【方案1】WordPress单独 (完全免费)
```

---

## 🎯 推荐方案: 分阶段实施

### Phase 1: 先做能动的 (1-2天)

```
【方案1】WordPress单独开始
↓
基本功能实现:
- Lightning主题
- Contact Form 7
- WP Mail SMTP
- 基本页面创建

成本: ¥0
时间: 2天
```

### Phase 2: 设计改善 (根据需要)

```
选项1: 追加Elementor Pro
成本: $59/年
效果: 专业设计

选项2: Bootstrap Studio
成本: $60 (买断)
效果: 完全自定义设计
```

### Phase 3: 功能扩展 (运营开始后)

```
- 多语言对应 (WPML: $39/年)
- 预约系统 (Amelia: 有免费版)
- EC网站功能 (WooCommerce: 免费)
- 会员系统 (Ultimate Member: 免费)
```

---

## 📋 实施检查清单

### 启动前 (1周内)

- [ ] WordPress安装
- [ ] 主题选择·安装
- [ ] 必装插件安装
- [ ] 联系表单创建
- [ ] 邮件发送测试成功
- [ ] 基本页面创建 (7页)
- [ ] 响应式确认
- [ ] SSL证书设置
- [ ] Google Analytics设置
- [ ] Google Search Console注册

### 启动时

- [ ] 全页面动作确认
- [ ] 表单提交测试
- [ ] 邮件接收确认
- [ ] 手机显示确认
- [ ] 加载速度检查
- [ ] SEO基本设置完成
- [ ] 隐私政策刊载
- [ ] 站点地图生成

### 启动后 (1个月)

- [ ] 备份自动化
- [ ] 访问分析确认
- [ ] 新闻文章3篇发布
- [ ] SNS联动设置
- [ ] 客户咨询响应测试

---

## 💡 成功要点

### 1. 首先不追求完美

```
✅ 以60%的完成度发布
✅ 收集反馈
✅ 阶段性改善

❌ 等到100%完美才发布
```

### 2. 最大限度活用现有资源

```
✅ 活用onamae.com服务器
✅ 使用WordPress标准功能
✅ 优先免费插件
✅ 从免费主题开始

💰 初期成本: ¥0
```

### 3. 考虑未来的扩展性

```
✅ 插件可追加功能
✅ 主题变更简单
✅ 多语言对应准备
✅ EC功能可追加

🚀 对应业务成长
```

---

## 📚 参考资源

### WordPress官方

- [WordPress.org](https://ja.wordpress.org/)
- [主题目录](https://ja.wordpress.org/themes/)
- [插件目录](https://ja.wordpress.org/plugins/)

### 学习资源

- [WordPress Codex 日语版](https://wpdocs.osdn.jp/)
- [dotinstall WordPress入门](https://dotinstall.com/lessons/basic_wordpress)
- [Udemy WordPress讲座](https://www.udemy.com/topic/wordpress/)

### 社区

- [WordBench](https://wordbench.org/) - 日本WordPress社区
- [WordPress论坛](https://ja.wordpress.org/support/forums/)

---

## 🆘 故障排除

### 常见问题及解决方法

```
【问题1】邮件发送失败
→ WP Mail SMTP设置确认
→ 尝试SMTP端口 465/587
→ SSL/TLS设置确认

【问题2】图片无法上传
→ php.ini upload_max_filesize 确认
→ 媒体设置确认
→ 服务器磁盘容量确认

【问题3】页面加载慢
→ 图片优化 (EWWW Image Optimizer)
→ 缓存插件导入
→ 删除不必要插件

【问题4】表单垃圾邮件
→ 追加reCAPTCHA
→ Akismet设置
→ SiteGuard WP Plugin启用
```

---

## 🎉 总结: 最快·最便宜路线图

### Week 1: 启动

```
Day 1-2: WordPress单独配置
- 主题安装 (Lightning)
- 插件设置
- 基本页面创建

Day 3-4: 内容创建
- 公司信息输入
- 图片准备·上传
- 新闻文章创建

Day 5: 测试
- 表单测试
- 邮件发送测试
- 响应式确认

Day 6-7: 发布准备
- SSL设置
- 最终确认
- 🚀 启动!
```

### 总成本

```
必要成本: ¥0
可选 (Elementor Pro): ¥9,000/年
推荐初期投资: ¥0〜¥9,000

月费: ¥0
(onamae.com服务器费用为现有)
```

---

**如有问题或需要支持，请随时告知具体的实施阶段！** 🚀
