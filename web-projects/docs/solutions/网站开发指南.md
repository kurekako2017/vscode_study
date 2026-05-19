# 现代网站开发完整教程

## 📋 目录

1. [VS Code 网页制作基础教程](#1-vs-code-网页制作基础教程)
2. [VS Code + WordPress 开发方案](#2-vs-code--wordpress-开发方案)
3. [Bootstrap Studio + WordPress 集成](#3-bootstrap-studio--wordpress-集成)
4. [先进快速开发工具与模板](#4-先进快速开发工具与模板)

---

## 1. VS Code 网页制作基础教程

### 1.1 环境准备

#### 必备扩展安装
```bash
# 在 VS Code 中按 Ctrl+Shift+X 打开扩展市场，搜索安装：
```

**核心扩展：**
- **Live Server** (ritwickdey.LiveServer) - 实时预览
- **HTML CSS Support** - HTML/CSS 智能提示
- **Auto Rename Tag** - 自动重命名配对标签
- **Prettier** - 代码格式化
- **Path Intellisense** - 路径智能提示
- **IntelliSense for CSS** - CSS 类名提示

**进阶扩展：**
- **Emmet** (内置) - HTML/CSS 快速编写
- **JavaScript (ES6) code snippets** - JS 代码片段
- **ESLint** - JavaScript 代码检查
- **Sass** - SCSS/Sass 支持
- **Tailwind CSS IntelliSense** - Tailwind 提示

### 1.2 创建第一个网页

#### 项目结构
```
my-website/
├── index.html          # 主页
├── css/
│   └── style.css      # 样式表
├── js/
│   └── script.js      # JavaScript
├── images/            # 图片资源
└── assets/            # 其他资源
```

#### 基础 HTML 模板 (index.html)
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="我的第一个网站">
    <meta name="keywords" content="网站, HTML, CSS, JavaScript">
    <title>我的网站</title>
    
    <!-- CSS 引用 -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">我的网站</div>
            <ul class="nav-menu">
                <li><a href="#home">首页</a></li>
                <li><a href="#about">关于</a></li>
                <li><a href="#services">服务</a></li>
                <li><a href="#contact">联系</a></li>
            </ul>
        </div>
    </nav>

    <!-- 头部横幅 -->
    <header id="home" class="hero">
        <div class="container">
            <h1>欢迎来到我的网站</h1>
            <p>打造专业的网络体验</p>
            <a href="#contact" class="btn">立即联系</a>
        </div>
    </header>

    <!-- 主要内容 -->
    <main>
        <!-- 关于部分 -->
        <section id="about" class="section">
            <div class="container">
                <h2>关于我们</h2>
                <p>这里是关于我们的描述内容...</p>
            </div>
        </section>

        <!-- 服务部分 -->
        <section id="services" class="section">
            <div class="container">
                <h2>我们的服务</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <h3>网页设计</h3>
                        <p>创建美观的网站设计</p>
                    </div>
                    <div class="service-card">
                        <h3>网站开发</h3>
                        <p>专业的前端后端开发</p>
                    </div>
                    <div class="service-card">
                        <h3>SEO优化</h3>
                        <p>提升搜索引擎排名</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 联系部分 -->
        <section id="contact" class="section">
            <div class="container">
                <h2>联系我们</h2>
                <form class="contact-form">
                    <input type="text" placeholder="姓名" required>
                    <input type="email" placeholder="邮箱" required>
                    <textarea placeholder="留言" rows="5" required></textarea>
                    <button type="submit" class="btn">发送消息</button>
                </form>
            </div>
        </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 我的网站. 版权所有.</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="js/script.js"></script>
</body>
</html>
```

#### 样式表 (css/style.css)
```css
/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --text-color: #333;
    --light-bg: #f4f4f4;
    --white: #fff;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
}

body {
    font-family: 'Arial', 'Microsoft YaHei', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 导航栏 */
.navbar {
    background: var(--white);
    box-shadow: var(--shadow);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 20px;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    text-decoration: none;
    color: var(--text-color);
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: var(--primary-color);
}

/* 头部横幅 */
.hero {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--white);
    text-align: center;
    padding: 150px 20px 100px;
    margin-top: 60px;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.5rem;
    margin-bottom: 2rem;
}

/* 按钮 */
.btn {
    display: inline-block;
    background: var(--white);
    color: var(--primary-color);
    padding: 12px 30px;
    border-radius: 5px;
    text-decoration: none;
    transition: transform 0.3s, box-shadow 0.3s;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* 内容区域 */
.section {
    padding: 80px 20px;
}

.section:nth-child(even) {
    background: var(--light-bg);
}

.section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: var(--secondary-color);
}

/* 服务网格 */
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.service-card {
    background: var(--white);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: var(--shadow);
    text-align: center;
    transition: transform 0.3s;
}

.service-card:hover {
    transform: translateY(-10px);
}

.service-card h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

/* 联系表单 */
.contact-form {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-form input,
.contact-form textarea {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-family: inherit;
}

.contact-form input:focus,
.contact-form textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}

/* 页脚 */
.footer {
    background: var(--secondary-color);
    color: var(--white);
    text-align: center;
    padding: 2rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1.2rem;
    }
    
    .services-grid {
        grid-template-columns: 1fr;
    }
}
```

#### JavaScript 交互 (js/script.js)
```javascript
// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// 导航栏滚动效果
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    }
});

// 表单提交处理
document.querySelector('.contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // 获取表单数据
    const formData = new FormData(this);
    
    // 显示成功消息
    alert('消息已发送！我们会尽快与您联系。');
    
    // 重置表单
    this.reset();
});

// 服务卡片动画
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.service-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s, transform 0.6s';
    observer.observe(card);
});
```

### 1.3 使用 Live Server 实时预览

1. 安装 Live Server 扩展
2. 右键点击 `index.html`
3. 选择 "Open with Live Server"
4. 浏览器自动打开 `http://127.0.0.1:5500`
5. 修改代码后自动刷新

### 1.4 Emmet 快速编写

**HTML 快捷键：**
```
! + Tab                    → 生成 HTML5 模板
nav>ul>li*5>a             → 创建导航菜单
div.container>h1+p        → 创建容器结构
section#hero.hero-section → ID和类名
```

**CSS 快捷键：**
```
m10     → margin: 10px;
p20     → padding: 20px;
w100p   → width: 100%;
df      → display: flex;
```

---

## 2. VS Code + WordPress 开发方案

### 2.1 本地 WordPress 环境搭建

#### 方法一：使用 LocalWP (推荐)
```bash
# 1. 下载 LocalWP: https://localwp.com/
# 2. 安装并创建新站点
# 3. 站点路径: C:\Users\YourName\Local Sites\my-site\app\public
```

#### 方法二：使用 Docker
```yaml
# docker-compose.yml
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./wordpress:/var/www/html
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db

volumes:
  db_data:
```

**启动命令：**
```powershell
# 在项目目录下运行
docker-compose up -d

# 访问:
# WordPress: http://localhost:8080
# phpMyAdmin: http://localhost:8081
```

### 2.2 VS Code WordPress 扩展

**必装扩展：**
- **WordPress Snippets** - WP 代码片段
- **PHP Intelephense** - PHP 智能提示
- **PHP Debug** - PHP 调试
- **WordPress Hooks IntelliSense** - WP 钩子提示
- **WordPress Toolbox** - WP 工具集

### 2.3 自定义主题开发

#### 主题目录结构
```
wp-content/themes/mytheme/
├── style.css              # 主题样式表（必需）
├── index.php             # 主模板（必需）
├── functions.php         # 主题函数
├── header.php           # 页眉
├── footer.php           # 页脚
├── sidebar.php          # 侧边栏
├── single.php           # 单篇文章
├── page.php             # 单页面
├── archive.php          # 归档页
├── 404.php              # 404页面
├── screenshot.png       # 主题截图
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── template-parts/      # 模板片段
```

#### style.css (必需的主题头部)
```css
/*
Theme Name: My Custom Theme
Theme URI: https://example.com
Author: Your Name
Author URI: https://example.com
Description: 一个自定义的WordPress主题
Version: 1.0.0
License: GNU General Public License v2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html
Text Domain: mytheme
Tags: blog, responsive, custom
*/

/* 主题样式从这里开始 */
```

#### functions.php (主题核心功能)
```php
<?php
/**
 * My Theme Functions
 */

// 主题设置
function mytheme_setup() {
    // 添加主题支持
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption'
    ));
    
    // 注册导航菜单
    register_nav_menus(array(
        'primary' => __('主导航', 'mytheme'),
        'footer' => __('页脚导航', 'mytheme')
    ));
    
    // 设置内容宽度
    if (!isset($content_width)) {
        $content_width = 1200;
    }
}
add_action('after_setup_theme', 'mytheme_setup');

// 注册侧边栏
function mytheme_widgets_init() {
    register_sidebar(array(
        'name'          => __('主侧边栏', 'mytheme'),
        'id'            => 'sidebar-1',
        'description'   => __('添加小工具到主侧边栏', 'mytheme'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
}
add_action('widgets_init', 'mytheme_widgets_init');

// 加载样式和脚本
function mytheme_scripts() {
    // 主样式表
    wp_enqueue_style('mytheme-style', get_stylesheet_uri(), array(), '1.0.0');
    
    // 自定义CSS
    wp_enqueue_style('mytheme-custom', get_template_directory_uri() . '/assets/css/custom.css', array(), '1.0.0');
    
    // JavaScript
    wp_enqueue_script('mytheme-script', get_template_directory_uri() . '/assets/js/script.js', array('jquery'), '1.0.0', true);
    
    // 评论回复
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'mytheme_scripts');

// 自定义摘要长度
function mytheme_excerpt_length($length) {
    return 40;
}
add_filter('excerpt_length', 'mytheme_excerpt_length');

// 自定义摘要结尾
function mytheme_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'mytheme_excerpt_more');

// 添加自定义字段支持
function mytheme_custom_fields() {
    add_meta_box(
        'mytheme_custom_fields',
        '自定义字段',
        'mytheme_custom_fields_callback',
        'post',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'mytheme_custom_fields');

// 自定义REST API端点
add_action('rest_api_init', function() {
    register_rest_route('mytheme/v1', '/posts', array(
        'methods' => 'GET',
        'callback' => 'mytheme_get_posts',
    ));
});

function mytheme_get_posts() {
    $args = array(
        'post_type' => 'post',
        'posts_per_page' => 10
    );
    $posts = get_posts($args);
    return rest_ensure_response($posts);
}
?>
```

#### index.php (主模板)
```php
<?php get_header(); ?>

<main id="main" class="site-main">
    <div class="container">
        <div class="row">
            <div class="col-lg-8">
                <?php
                if (have_posts()) :
                    while (have_posts()) : the_post();
                        ?>
                        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                            <header class="entry-header">
                                <?php
                                if (is_singular()) :
                                    the_title('<h1 class="entry-title">', '</h1>');
                                else :
                                    the_title('<h2 class="entry-title"><a href="' . esc_url(get_permalink()) . '">', '</a></h2>');
                                endif;
                                ?>
                                
                                <div class="entry-meta">
                                    <span class="posted-on">
                                        <?php echo get_the_date(); ?>
                                    </span>
                                    <span class="byline">
                                        作者: <?php the_author(); ?>
                                    </span>
                                </div>
                            </header>

                            <?php if (has_post_thumbnail()) : ?>
                                <div class="post-thumbnail">
                                    <?php the_post_thumbnail('large'); ?>
                                </div>
                            <?php endif; ?>

                            <div class="entry-content">
                                <?php
                                if (is_singular()) :
                                    the_content();
                                else :
                                    the_excerpt();
                                    echo '<a href="' . esc_url(get_permalink()) . '" class="read-more">阅读更多</a>';
                                endif;
                                ?>
                            </div>

                            <footer class="entry-footer">
                                <?php
                                $categories = get_the_category();
                                if ($categories) {
                                    echo '<span class="cat-links">分类: ';
                                    foreach ($categories as $category) {
                                        echo '<a href="' . esc_url(get_category_link($category->term_id)) . '">' . esc_html($category->name) . '</a> ';
                                    }
                                    echo '</span>';
                                }
                                
                                $tags = get_the_tags();
                                if ($tags) {
                                    echo '<span class="tags-links">标签: ';
                                    foreach ($tags as $tag) {
                                        echo '<a href="' . esc_url(get_tag_link($tag->term_id)) . '">' . esc_html($tag->name) . '</a> ';
                                    }
                                    echo '</span>';
                                }
                                ?>
                            </footer>
                        </article>
                        <?php
                    endwhile;

                    // 分页导航
                    the_posts_pagination(array(
                        'prev_text' => __('&laquo; 上一页', 'mytheme'),
                        'next_text' => __('下一页 &raquo;', 'mytheme'),
                    ));
                else :
                    ?>
                    <p>没有找到内容。</p>
                    <?php
                endif;
                ?>
            </div>

            <div class="col-lg-4">
                <?php get_sidebar(); ?>
            </div>
        </div>
    </div>
</main>

<?php get_footer(); ?>
```

#### header.php
```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    <header id="masthead" class="site-header">
        <div class="container">
            <div class="site-branding">
                <?php
                if (has_custom_logo()) :
                    the_custom_logo();
                else :
                    ?>
                    <h1 class="site-title">
                        <a href="<?php echo esc_url(home_url('/')); ?>">
                            <?php bloginfo('name'); ?>
                        </a>
                    </h1>
                    <p class="site-description"><?php bloginfo('description'); ?></p>
                    <?php
                endif;
                ?>
            </div>

            <nav id="site-navigation" class="main-navigation">
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'primary',
                    'menu_id'        => 'primary-menu',
                    'container'      => false,
                ));
                ?>
            </nav>
        </div>
    </header>
```

#### footer.php
```php
    <footer id="colophon" class="site-footer">
        <div class="container">
            <div class="footer-widgets">
                <div class="row">
                    <?php if (is_active_sidebar('footer-1')) : ?>
                        <div class="col-md-4">
                            <?php dynamic_sidebar('footer-1'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <?php if (is_active_sidebar('footer-2')) : ?>
                        <div class="col-md-4">
                            <?php dynamic_sidebar('footer-2'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <?php if (is_active_sidebar('footer-3')) : ?>
                        <div class="col-md-4">
                            <?php dynamic_sidebar('footer-3'); ?>
                        </div>
                    <?php endif; ?>
                </div>
            </div>

            <div class="site-info">
                <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. 
                   <?php _e('版权所有', 'mytheme'); ?>
                </p>
            </div>
        </div>
    </footer>
</div><!-- #page -->

<?php wp_footer(); ?>
</body>
</html>
```

### 2.4 插件开发基础

#### 创建插件目录
```
wp-content/plugins/my-plugin/
├── my-plugin.php         # 主文件
├── includes/             # 核心功能
├── admin/               # 后台管理
├── public/              # 前台展示
└── assets/              # 资源文件
```

#### 插件主文件示例
```php
<?php
/**
 * Plugin Name: My Custom Plugin
 * Plugin URI: https://example.com
 * Description: 一个自定义WordPress插件
 * Version: 1.0.0
 * Author: Your Name
 * Author URI: https://example.com
 * License: GPL v2 or later
 * Text Domain: my-plugin
 */

// 防止直接访问
if (!defined('ABSPATH')) {
    exit;
}

// 定义常量
define('MY_PLUGIN_VERSION', '1.0.0');
define('MY_PLUGIN_PATH', plugin_dir_path(__FILE__));
define('MY_PLUGIN_URL', plugin_dir_url(__FILE__));

// 激活钩子
register_activation_hook(__FILE__, 'my_plugin_activate');
function my_plugin_activate() {
    // 创建数据库表
    global $wpdb;
    $table_name = $wpdb->prefix . 'my_plugin_data';
    
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        name varchar(100) NOT NULL,
        email varchar(100) NOT NULL,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY  (id)
    ) $charset_collate;";
    
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}

// 停用钩子
register_deactivation_hook(__FILE__, 'my_plugin_deactivate');
function my_plugin_deactivate() {
    // 清理工作
}

// 添加短代码
add_shortcode('my_custom_content', 'my_plugin_shortcode');
function my_plugin_shortcode($atts) {
    $atts = shortcode_atts(array(
        'title' => '默认标题',
        'content' => '默认内容'
    ), $atts);
    
    return '<div class="my-plugin-content">
                <h3>' . esc_html($atts['title']) . '</h3>
                <p>' . esc_html($atts['content']) . '</p>
            </div>';
}

// 添加管理菜单
add_action('admin_menu', 'my_plugin_menu');
function my_plugin_menu() {
    add_menu_page(
        'My Plugin Settings',
        'My Plugin',
        'manage_options',
        'my-plugin',
        'my_plugin_settings_page',
        'dashicons-admin-generic',
        20
    );
}

function my_plugin_settings_page() {
    ?>
    <div class="wrap">
        <h1>My Plugin Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('my_plugin_settings');
            do_settings_sections('my-plugin');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
?>
```

---

## 3. Bootstrap Studio + WordPress 集成

### 3.1 Bootstrap Studio 介绍

**Bootstrap Studio** 是一个可视化网页设计工具，专门用于创建响应式网站。

**下载地址：** https://bootstrapstudio.io/

### 3.2 工作流程

```
1. Bootstrap Studio 设计 
   ↓
2. 导出 HTML/CSS/JS
   ↓
3. 转换为 WordPress 主题
   ↓
4. 集成到 WordPress
```

### 3.3 Bootstrap Studio 基础操作

#### 创建项目
1. 打开 Bootstrap Studio
2. File → New
3. 选择模板或从空白开始
4. 拖拽组件到画布

#### 常用组件
- **Container/Row/Column** - 网格布局
- **Navbar** - 导航栏
- **Card** - 卡片
- **Form** - 表单
- **Button** - 按钮
- **Modal** - 模态框

### 3.4 导出并转换为 WordPress 主题

#### 步骤 1：导出 Bootstrap Studio 项目
```
File → Export → 选择导出路径
生成文件：
- index.html
- assets/
  ├── css/
  ├── js/
  └── img/
```

#### 步骤 2：创建 WordPress 主题结构
```bash
mkdir wp-content/themes/bsstudio-theme
cd wp-content/themes/bsstudio-theme
```

#### 步骤 3：转换 HTML 为 PHP 模板

**style.css**
```css
/*
Theme Name: Bootstrap Studio Theme
Theme URI: https://example.com
Description: 使用Bootstrap Studio创建的WordPress主题
Version: 1.0.0
Author: Your Name
*/

/* 导入Bootstrap Studio的CSS */
@import url('assets/css/bootstrap.min.css');
@import url('assets/css/styles.css');
```

**functions.php**
```php
<?php
function bsstudio_theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo');
}
add_action('after_setup_theme', 'bsstudio_theme_setup');

function bsstudio_scripts() {
    // Bootstrap CSS
    wp_enqueue_style('bootstrap', get_template_directory_uri() . '/assets/css/bootstrap.min.css');
    
    // 自定义样式
    wp_enqueue_style('bsstudio-style', get_template_directory_uri() . '/assets/css/styles.css');
    wp_enqueue_style('main-style', get_stylesheet_uri());
    
    // Bootstrap JS
    wp_enqueue_script('bootstrap-bundle', get_template_directory_uri() . '/assets/js/bootstrap.bundle.min.js', array('jquery'), null, true);
    
    // 自定义 JS
    wp_enqueue_script('bsstudio-script', get_template_directory_uri() . '/assets/js/script.js', array('jquery'), null, true);
}
add_action('wp_enqueue_scripts', 'bsstudio_scripts');
?>
```

**header.php** (从 index.html 提取头部)
```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

<!-- 从 Bootstrap Studio 导出的导航栏 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a class="navbar-brand" href="<?php echo home_url('/'); ?>">
            <?php bloginfo('name'); ?>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'menu_class' => 'navbar-nav ms-auto',
                'container' => false,
                'fallback_cb' => false,
                'depth' => 2,
            ));
            ?>
        </div>
    </div>
</nav>
```

**index.php** (转换主内容区域)
```php
<?php get_header(); ?>

<main class="container my-5">
    <div class="row">
        <div class="col-lg-8">
            <?php
            if (have_posts()) :
                while (have_posts()) : the_post();
                    ?>
                    <!-- Bootstrap Card 样式 -->
                    <article class="card mb-4">
                        <?php if (has_post_thumbnail()) : ?>
                            <img src="<?php the_post_thumbnail_url('large'); ?>" class="card-img-top" alt="<?php the_title(); ?>">
                        <?php endif; ?>
                        
                        <div class="card-body">
                            <h2 class="card-title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h2>
                            <p class="card-text text-muted">
                                <small><?php echo get_the_date(); ?> | <?php the_author(); ?></small>
                            </p>
                            <div class="card-text">
                                <?php the_excerpt(); ?>
                            </div>
                            <a href="<?php the_permalink(); ?>" class="btn btn-primary">阅读更多</a>
                        </div>
                    </article>
                    <?php
                endwhile;
                
                // Bootstrap 分页
                the_posts_pagination(array(
                    'prev_text' => '&laquo; 上一页',
                    'next_text' => '下一页 &raquo;',
                    'class' => 'pagination justify-content-center'
                ));
            endif;
            ?>
        </div>
        
        <div class="col-lg-4">
            <?php get_sidebar(); ?>
        </div>
    </div>
</main>

<?php get_footer(); ?>
```

**footer.php**
```php
<footer class="bg-dark text-white py-4">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?></p>
            </div>
            <div class="col-md-6 text-end">
                <p>由 Bootstrap Studio + WordPress 强力驱动</p>
            </div>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
```

### 3.5 Bootstrap Studio 高级技巧

#### 使用自定义代码
```html
<!-- 在 Bootstrap Studio 中添加自定义 HTML -->
<div class="container">
    <!-- WordPress Loop 占位符 -->
    <!--WP_LOOP_START-->
    <div class="post-item">
        <h2><!--WP_TITLE--></h2>
        <div><!--WP_CONTENT--></div>
    </div>
    <!--WP_LOOP_END-->
</div>
```

#### 转换脚本
创建 `convert.php` 自动转换标记：
```php
<?php
$html = file_get_contents('index.html');

// 替换占位符
$html = str_replace('<!--WP_LOOP_START-->', '<?php while(have_posts()): the_post(); ?>', $html);
$html = str_replace('<!--WP_LOOP_END-->', '<?php endwhile; ?>', $html);
$html = str_replace('<!--WP_TITLE-->', '<?php the_title(); ?>', $html);
$html = str_replace('<!--WP_CONTENT-->', '<?php the_content(); ?>', $html);

file_put_contents('index.php', $html);
?>
```

---

## 4. 先进快速开发工具与模板

### 4.1 现代前端框架

#### **Astro** (推荐 - 超快静态站点)
```bash
npm create astro@latest

# 特点：
# - 零JS默认加载
# - 支持多框架（React, Vue, Svelte）
# - 内置优化
# - 适合博客、文档、营销网站
```

#### **Next.js** (React 全栈框架)
```bash
npx create-next-app@latest my-site

# 特点：
# - 服务端渲染(SSR)
# - 静态生成(SSG)
# - API路由
# - 图片优化
```

#### **Nuxt.js** (Vue 全栈框架)
```bash
npx nuxi@latest init my-site

# 特点：
# - Vue 3 + Vite
# - 自动路由
# - SEO 友好
```

### 4.2 无代码/低代码平台

#### **Webflow**
- 🌐 https://webflow.com
- 可视化设计 + CMS
- 导出纯净代码
- 托管服务

#### **Framer**
- 🌐 https://framer.com
- 交互设计工具
- React 组件
- 实时协作

#### **Wix Studio**
- 🌐 https://wix.com/studio
- 拖拽式编辑器
- 完整后台
- 应用市场

#### **WordPress Page Builders**
- **Elementor** (最流行)
- **Beaver Builder**
- **Divi Builder**
- **Oxygen Builder** (性能最佳)

### 4.3 静态站点生成器 (SSG)

| 工具 | 语言 | 特点 | 适用场景 |
|------|------|------|----------|
| **Hugo** | Go | 超快构建速度 | 博客、文档 |
| **Jekyll** | Ruby | GitHub Pages原生支持 | 个人博客 |
| **Gatsby** | React | GraphQL数据层 | 企业网站 |
| **Eleventy** | JavaScript | 灵活模板引擎 | 任意场景 |
| **VitePress** | Vue | Vue官方文档工具 | 技术文档 |

#### Hugo 快速开始
```bash
# 安装 Hugo
choco install hugo-extended  # Windows

# 创建站点
hugo new site my-site
cd my-site

# 添加主题
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> config.toml

# 创建文章
hugo new posts/my-first-post.md

# 启动服务
hugo server -D

# 构建
hugo
```

### 4.4 现代 CSS 框架

#### **Tailwind CSS** (最流行)
```bash
npm install -D tailwindcss
npx tailwindcss init

# 配置
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}

# HTML 示例
<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="p-6 max-w-sm bg-white rounded-xl shadow-lg">
        <h1 class="text-2xl font-bold text-gray-900">Hello Tailwind!</h1>
    </div>
</div>
```

#### **Bootstrap 5**
```html
<!-- CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

#### **其他优秀框架**
- **Bulma** - 纯CSS，无JS依赖
- **Foundation** - 企业级响应式框架
- **UIKit** - 轻量级现代框架
- **Materialize** - Material Design

### 4.5 UI 组件库

#### React 生态
```bash
# Ant Design
npm install antd

# Material-UI
npm install @mui/material @emotion/react @emotion/styled

# Chakra UI
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion

# shadcn/ui (推荐)
npx shadcn-ui@latest init
```

#### Vue 生态
```bash
# Element Plus
npm install element-plus

# Vuetify
npm install vuetify

# Naive UI
npm install naive-ui
```

### 4.6 网站模板资源

#### 免费模板网站

**HTML/CSS 模板：**
- 🌐 **HTML5 UP** - https://html5up.net
- 🌐 **Free CSS** - https://www.free-css.com
- 🌐 **Templated** - https://templated.co
- 🌐 **Colorlib** - https://colorlib.com/wp/templates

**WordPress 主题：**
- 🌐 **WordPress.org** - https://wordpress.org/themes
- 🌐 **ThemeForest** - https://themeforest.net (付费)
- 🌐 **Astra** - https://wpastra.com (免费+付费)
- 🌐 **OceanWP** - https://oceanwp.org

**Bootstrap 模板：**
- 🌐 **Start Bootstrap** - https://startbootstrap.com
- 🌐 **BootstrapMade** - https://bootstrapmade.com
- 🌐 **Creative Tim** - https://www.creative-tim.com

**Tailwind 模板：**
- 🌐 **Tailwind UI** - https://tailwindui.com (官方，付费)
- 🌐 **Tailwind Toolbox** - https://www.tailwindtoolbox.com
- 🌐 **Tailwind Components** - https://tailwindcomponents.com

### 4.7 完整解决方案

#### **Vercel** (推荐 - 最佳部署平台)
```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel

# 特点：
# - 自动 HTTPS
# - 全球 CDN
# - 预览部署
# - 零配置
# - 免费套餐
```

#### **Netlify**
```bash
# 安装 Netlify CLI
npm install -g netlify-cli

# 部署
netlify deploy

# 特点：
# - 表单处理
# - 无服务器函数
# - 分支预览
# - 免费 SSL
```

#### **Cloudflare Pages**
- 连接 GitHub 仓库
- 自动构建部署
- 全球 CDN
- 免费无限带宽

### 4.8 内容管理系统 (CMS)

#### **Headless CMS** (现代方案)

| CMS | 类型 | 特点 |
|-----|------|------|
| **Strapi** | 开源 | Node.js, 自托管 |
| **Sanity** | 云服务 | 实时协作, GraphQL |
| **Contentful** | 云服务 | 企业级, API驱动 |
| **Ghost** | 开源 | 专注博客 |
| **Directus** | 开源 | 数据库驱动 |

#### Strapi 快速开始
```bash
npx create-strapi-app@latest my-project --quickstart

# 访问 http://localhost:1337/admin
# 创建内容类型
# 使用 REST/GraphQL API
```

### 4.9 AI 辅助开发工具

#### **GitHub Copilot**
- VS Code 扩展
- AI 代码补全
- 自然语言转代码

#### **v0.dev** (Vercel AI)
- 🌐 https://v0.dev
- AI 生成 UI 组件
- 基于 shadcn/ui

#### **Framer AI**
- AI 生成网站布局
- 自动生成内容

#### **10Web AI Builder**
- WordPress AI 建站
- 自动设计优化

### 4.10 性能优化工具

#### **图片优化**
- **TinyPNG** - https://tinypng.com
- **Squoosh** - https://squoosh.app
- **ImageOptim** - 批量压缩

#### **CDN 服务**
- **Cloudflare** - 免费 CDN + 防护
- **jsDelivr** - 免费 npm CDN
- **unpkg** - npm 包 CDN

#### **测试工具**
- **Lighthouse** - Chrome DevTools
- **PageSpeed Insights** - Google
- **GTmetrix** - 详细性能报告

---

## 📚 学习路线建议

### 初学者路线（0-3个月）
1. ✅ HTML + CSS 基础
2. ✅ JavaScript 基础
3. ✅ Bootstrap 框架
4. ✅ VS Code 熟练使用
5. ✅ Git 版本控制

### 进阶路线（3-6个月）
1. ✅ WordPress 主题开发
2. ✅ React / Vue 基础
3. ✅ Tailwind CSS
4. ✅ REST API 使用
5. ✅ 响应式设计原理

### 高级路线（6-12个月）
1. ✅ Next.js / Nuxt.js
2. ✅ Headless CMS
3. ✅ TypeScript
4. ✅ GraphQL
5. ✅ 性能优化

---

## 🚀 快速开始项目模板

### 方案一：纯静态网站
```bash
# 使用 Vite + Tailwind
npm create vite@latest my-site -- --template vanilla
cd my-site
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm run dev
```

### 方案二：WordPress 快速站点
```bash
# 使用 LocalWP
# 1. 下载 LocalWP: https://localwp.com
# 2. 创建新站点
# 3. 安装 Elementor 或 Astra 主题
# 4. 开始设计
```

### 方案三：现代 React 应用
```bash
npx create-next-app@latest my-site
cd my-site
npm install @shadcn/ui
npm run dev
```

### 方案四：一键博客
```bash
# Hugo + 主题
hugo new site my-blog
cd my-blog
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
echo "theme = 'PaperMod'" >> config.toml
hugo server
```

---

## 💡 实用技巧

### VS Code 设置优化
```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "emmet.includeLanguages": {
        "javascript": "javascriptreact",
        "php": "html"
    },
    "files.associations": {
        "*.php": "php"
    },
    "liveServer.settings.port": 5500
}
```

### Git 工作流
```bash
# 初始化项目
git init
git add .
git commit -m "Initial commit"

# 连接远程仓库
git remote add origin https://github.com/username/repo.git
git push -u origin main

# 日常开发
git add .
git commit -m "feat: add new feature"
git push
```

---

## 📞 获取帮助

- **VS Code 文档**: https://code.visualstudio.com/docs
- **WordPress 开发文档**: https://developer.wordpress.org
- **Bootstrap 文档**: https://getbootstrap.com/docs
- **MDN Web 文档**: https://developer.mozilla.org
- **Stack Overflow**: https://stackoverflow.com

---

**最后更新**: 2026年1月6日
