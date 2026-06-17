# ATBIO 网站运维开发手册（高级版）

## 文档目标

本手册用于维护和二次开发 ATBIO 网站。

适用对象：

- 网站管理员
- 开发人员
- VPS维护人员
- 后续接手人员

---

# 第一篇：整体架构

## 系统架构图

Internet
↓
域名
↓
Hostinger VPS
↓
Nginx
↓
PHP CMS
↓
MySQL
↓
Template模板
↓
浏览器

---

## 网站组成

- 域名
- VPS服务器
- 小皮面板
- PHP环境
- MySQL数据库
- CMS后台
- Template模板
- SSL证书

---

# 第二篇：Hostinger VPS

## VPS作用

用于运行：

- 网站
- 数据库
- Nginx
- SSL证书
- 后续AI服务

---

## 当前配置

- 2 Core CPU
- 8GB RAM
- 100GB SSD
- Debian 13

---

## Hostinger控制台功能

### 重启服务器

用于：

- 修改配置后生效
- 故障恢复

### 重装系统

重置整台服务器

### 快照

服务器备份

### SSH

远程连接服务器

---

## 常用Linux命令

查看CPU

```bash
top
```

查看内存

```bash
free -h
```

查看硬盘

```bash
df -h
```

查看端口

```bash
ss -tulpn
```

---

# 第三篇：小皮面板

## 小皮面板作用

可视化管理服务器

---

## 网站管理

功能：

- 创建网站
- 删除网站
- 修改域名
- 配置SSL
- 修改PHP版本

---

## 数据库管理

功能：

- 创建数据库
- 修改密码
- 导入SQL
- 导出SQL

---

## 文件管理

功能：

- 上传文件
- 下载文件
- 编辑文件
- 解压压缩包

---

## SSL证书

支持：

- Let's Encrypt
- 自动续期

---

## 定时任务

可实现：

- 自动备份
- 自动清理日志
- 自动同步

---

# 第四篇：CMS后台

## 后台菜单

### 网站

网站基础设置

### 分类

栏目管理

### 内容

文章与页面内容

### 设置

SEO与系统设置

### 询盘

客户留言管理

### 功能

扩展插件

---

## 产品管理

功能：

- 新增产品
- 编辑产品
- 上传图片
- SEO设置

---

## 新闻管理

功能：

- 发布新闻
- 修改新闻
- 新闻分类

---

## About Us

企业介绍

品牌介绍

视频内容

---

## Contact

联系方式

地图

询盘表单

---

# 第五篇：Template模板开发

## Template作用

控制：

- 页面布局
- 页面结构
- 模块位置

不负责：

- 内容数据

---

## Template目录

典型结构

```text
template
├─header.htm
├─footer.htm
├─index.htm
├─lists_single.htm
├─product.htm
├─news.htm
```

---

## Header

控制：

- Logo
- 菜单
- 语言切换

---

## Footer

控制：

- 地址
- 电话
- 邮箱
- 版权

---

## 首页

控制：

- Banner
- 产品展示
- 新闻展示

---

## ABOUT US

控制：

- 视频
- 品牌介绍
- 页面布局

---

# 第六篇：CSS与JS

## CSS

位置

```text
static/css
```

负责

- 颜色
- 字体
- 布局
- 响应式

---

## JavaScript

位置

```text
static/js
```

负责

- 动画
- 轮播图
- 弹窗
- 表单验证

---

# 第七篇：VS Code开发

## 推荐方式

VS Code + Remote SSH

---

## 推荐插件

- Remote SSH
- GitLens
- Prettier
- Path Intellisense

---

## Git管理

建议：

所有模板修改进入Git管理

---

# 第八篇：数据库维护

## 数据库作用

保存：

- 产品
- 新闻
- 询盘
- 页面内容

---

## 备份策略

每日：数据库

每周：网站全量

每月：服务器快照

---

## 恢复策略

恢复SQL

恢复网站目录

恢复快照

---

# 第九篇：Nginx

## 配置位置

```text
/etc/nginx
```

---

## 常用命令

测试

```bash
nginx -t
```

重启

```bash
systemctl restart nginx
```

---

## 伪静态

用于SEO优化

---

# 第十篇：网站安全

## SSH安全

建议：

- 修改默认端口
- 使用密钥登录
- 禁止root远程

---

## 防火墙

推荐：

- UFW
- Fail2Ban

---

## 数据库安全

定期修改密码

定期备份

---

# 第十一篇：故障排查

## 网站打不开

检查：

- VPS
- Nginx
- 域名

---

## 数据库错误

检查：

- MySQL
- 配置文件

---

## SSL失效

重新申请证书

---

## 页面修改不生效

清缓存

Ctrl+F5

---

# 第十二篇：未来扩展

## AI客服

- ChatGPT
- DeepSeek
- Gemini

---

## 多语言

- 中文
- 英文
- 日文

---

## CRM

询盘管理

客户管理

---

## Google Analytics

流量统计

---

## SEO优化

- Sitemap
- Robots
- Title
- Description

---

# 附录

## 常用Linux命令

top
free -h
df -h
ps aux
ss -tulpn

## 常用Nginx命令

nginx -t
systemctl restart nginx

## 上线检查清单

□ 数据库备份

□ Template备份

□ SSL正常

□ 手机端测试

□ PC端测试

□ 表单测试

□ SEO检查
