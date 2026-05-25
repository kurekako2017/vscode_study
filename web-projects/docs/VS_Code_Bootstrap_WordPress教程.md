# VS Code + Bootstrap + WordPress 后台建站教程

## 1. 环境准备

- 安装 VS Code。
- 安装 PHP（建议 7.4+）、MySQL/MariaDB、本地服务器（推荐 XAMPP/WAMP/MAMP）。
- 下载 WordPress 官方包：https://cn.wordpress.org/download/
- 推荐插件：Live Server、Prettier、Path Intellisense、Auto Close Tag。

## 2. 本地搭建 WordPress

1. 解压 WordPress 到本地服务器的 `htdocs`（XAMPP）或 `www` 目录。
2. 启动 Apache 和 MySQL 服务。
3. 访问 http://localhost/wordpress 按提示安装，设置数据库。

## 3. 创建自定义主题（集成 Bootstrap）

1. 在 `wp-content/themes/` 下新建文件夹 `my-bootstrap-theme`。
2. 新建 `style.css`，写入主题头部：
   ```css
   /*
   Theme Name: My Bootstrap Theme
   Author: 你的名字
   Version: 1.0
   */
   ```
3. 新建 `index.php`、`functions.php`、`header.php`、`footer.php`。
4. 在 `functions.php` 注册 Bootstrap：
   ```php
   function mytheme_enqueue_scripts() {
     wp_enqueue_style('bootstrap', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
     wp_enqueue_style('style', get_stylesheet_uri());
     wp_enqueue_script('bootstrap', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js', array('jquery'), null, true);
   }
   add_action('wp_enqueue_scripts', 'mytheme_enqueue_scripts');
   ```
5. 在 `header.php`、`footer.php` 引入 WordPress 头部和底部函数：
   ```php
   <!-- header.php -->
   <!DOCTYPE html>
   <html <?php language_attributes(); ?>>
   <head>
     <meta charset="<?php bloginfo('charset'); ?>">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <?php wp_head(); ?>
   </head>
   <body <?php body_class(); ?>>
   <header class="container py-3">
     <h1><?php bloginfo('name'); ?></h1>
   </header>
   <!-- ... -->
   ```
   ```php
   <!-- footer.php -->
     <footer class="container py-3">
       <p>&copy; <?php echo date('Y'); ?> My Bootstrap Theme</p>
     </footer>
     <?php wp_footer(); ?>
   </body>
   </html>
   ```
6. 在 `index.php` 结构如下：
   ```php
   <?php get_header(); ?>
   <main class="container py-4">
     <?php
     if (have_posts()) :
       while (have_posts()) : the_post();
         echo '<article class="mb-4">';
         the_title('<h2>', '</h2>');
         the_content();
         echo '</article>';
       endwhile;
     else:
       echo '<p>暂无内容</p>';
     endif;
     ?>
   </main>
   <?php get_footer(); ?>
   ```
7. 在 WordPress 后台“外观→主题”启用你的主题。

## 4. 前端开发与调试

- 用 VS Code 打开 `my-bootstrap-theme` 文件夹，编辑 PHP/HTML/CSS/JS。
- 推荐用 Live Server 预览纯静态页面（不带 PHP），或用 XAMPP 访问 http://localhost/wordpress/ 预览动态页面。
- 可用 Bootstrap 组件丰富页面结构。

## 5. WordPress 后台内容管理

- 在后台“文章”、“页面”中添加内容，前端自动渲染。
- 可用自定义菜单、小工具、特色图片等功能。
- 推荐插件：Classic Editor、Elementor、Yoast SEO、WPForms。

## 6. 部署上线

- 将本地 WordPress 站点文件和数据库导出，上传到服务器。
- 修改 `wp-config.php` 数据库配置。
- 推荐使用宝塔、cPanel、宝云等面板简化部署。

## 7. 进阶建议

- 主题开发可拆分模板（如 `single.php`、`page.php`、`archive.php`）。
- 支持自定义文章类型、字段、短代码。
- 可用 SASS/SCSS、Gulp/Webpack 优化前端开发。

---
如需详细代码示例或自动生成主题骨架，请告知你的具体需求。