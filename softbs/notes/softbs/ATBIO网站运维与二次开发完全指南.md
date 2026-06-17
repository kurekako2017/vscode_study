# ATBIO 网站运维与二次开发完全指南

## 一、当前网站架构分析

### 服务器
- Hostinger VPS（KVM 2）
- Debian 13.5
- 2 Core CPU
- 8GB RAM
- 100GB SSD

### 网站架构

```text
用户浏览器
    ↓
Nginx
    ↓
PHP CMS
    ↓
MySQL
    ↓
Template 模板
```

---

## 二、网站目录说明

```text
/www/www/atmbio.com
├── application
├── core
├── data
├── extend
├── public
├── static
├── template
├── uploads
├── vendor
├── weapp
├── index.php
└── login.php
```

### 重要目录

#### template
网站模板目录

负责：
- 首页布局
- 产品页布局
- 新闻页布局
- About Us布局
- Contact布局
- Header
- Footer

#### uploads

保存：
- 产品图片
- 新闻图片
- Banner图片
- PDF文件

#### static

保存：
- CSS
- JavaScript
- 图片资源

---

## 三、内容修改与模板修改区别

### 后台内容修改

后台 → 内容

可以修改：

- 产品内容
- 新闻内容
- About Us正文
- Contact内容

### 模板修改

template目录

可以修改：

- 页面布局
- 模块位置
- 视频区域
- 导航菜单
- 页脚
- 首页结构

---

## 四、页面工作原理

```text
数据库内容
     ↓
CMS程序
     ↓
Template模板
     ↓
生成最终HTML
     ↓
浏览器显示
```

---

## 五、常见模板文件

```text
template
├── header.htm
├── footer.htm
├── index.htm
├── about.htm
├── product.htm
├── news.htm
├── contact.htm
└── lists_single.htm
```

### header.htm

顶部导航

### footer.htm

页脚

### index.htm

首页

### lists_single.htm

ABOUT US
CONTACT 等单页

---

## 六、如何修改整个页面布局

推荐方式：

### VS Code + Remote SSH

安装插件：

```text
Remote - SSH
```

连接VPS

打开：

```text
/www/www/atmbio.com
```

修改：

```text
template
```

保存后直接生效。

---

## 七、如何定位页面

搜索关键字：

```text
Global Vision
Brand Partnership
youtube
iframe
```

即可找到对应模板。

---

## 八、CSS修改

常见位置：

```text
static/css
```

例如：

```css
.container {}
.header {}
.footer {}
.product-card {}
```

---

## 九、JS修改

位置：

```text
static/js
```

负责：

- 轮播图
- 菜单动画
- 语言切换
- 页面交互

---

## 十、数据库维护

小皮面板 → 数据库

建议：

每周备份一次。

导出：

```sql
mysqldump
```

或者后台导出SQL。

---

## 十一、网站备份

### 文件备份

备份：

```text
/www/www/atmbio.com
```

### 数据库备份

导出：

```text
atbio.sql
```

---

## 十二、服务器维护

查看CPU：

```bash
top
```

查看内存：

```bash
free -h
```

查看磁盘：

```bash
df -h
```

查看端口：

```bash
ss -tulpn
```

---

## 十三、Nginx维护

测试配置：

```bash
nginx -t
```

重启：

```bash
systemctl restart nginx
```

---

## 十四、SSL证书

小皮面板

网站 → SSL

使用：

Let's Encrypt

自动续期。

---

## 十五、推荐开发流程

```text
本地 VS Code
      ↓
Remote SSH
      ↓
修改 template
      ↓
保存
      ↓
浏览器 Ctrl+F5
      ↓
查看效果
```

---

## 十六、未来扩展

- ChatGPT客服
- DeepSeek客服
- 多语言（日文/英文）
- CRM询盘系统
- Google Analytics
- SEO优化
- AI产品搜索

---

## 十七、上线前检查清单

- 备份数据库
- 备份template目录
- 检查Nginx配置
- 清理缓存
- 浏览器测试
- 手机端测试
- SSL正常
- 联系表单正常
