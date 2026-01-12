# 🚀 image.png

> **目标**: 30分钟完成带联系表单的企业网站上线  
> **前提**: onamae.com RSプラン已完成WordPress自动安装

---

## ⚡ 30分钟时间安排

```
00:00 - 05:00  主题安装
05:00 - 10:00  插件批量安装  
10:00 - 15:00  联系表单配置
15:00 - 20:00  邮件发送设置
20:00 - 25:00  基本页面创建
25:00 - 30:00  测试与发布
```

---

## 📦 Step 1: 主题安装 (5分钟)

```
登录WordPress管理后台
↓
外观 → 主题 → 添加新主题
↓
搜索: "Lightning"
↓
安装 → 启用
```

### ✅ 确认要点
- 查看网站确认已应用Lightning主题

---

## 🔌 Step 2: 插件批量安装 (5分钟)

```
插件 → 添加新插件 → 搜索以下插件并安装启用

必装4个:
1. Contact Form 7         ← 联系表单
2. WP Mail SMTP           ← 邮件发送设置
3. VK All in One Expansion Unit  ← Lightning扩展功能
4. SiteGuard WP Plugin    ← 安全防护

推荐2个:
5. EWWW Image Optimizer   ← 图片自动压缩
6. UpdraftPlus            ← 自动备份
```

### ✅ 检查清单
- [ ] 6个插件全部启用完成
- [ ] 没有出现错误信息

---

## 📝 Step 3: 联系表单创建 (5分钟)

### 3-1: 创建表单

```
Contact Form 7 → 添加新表单
标题: 联系表单
```

### 3-2: 复制粘贴表单代码

```html
<label> 姓名 (必填)
    [text* your-name autocomplete:name placeholder "山田太郎"] </label>

<label> 公司名称
    [text your-company autocomplete:organization placeholder "株式会社Sample"] </label>

<label> 邮箱地址 (必填)
    [email* your-email autocomplete:email placeholder "example@company.co.jp"] </label>

<label> 电话号码
    [tel your-phone autocomplete:tel placeholder "03-1234-5678"] </label>

<label> 咨询内容 (必填)
    [textarea* your-message placeholder "请输入您的咨询内容"] </label>

<label>
    [acceptance acceptance-privacy] 同意<a href="/privacy-policy" target="_blank">隐私政策</a>
</label>

[submit "提交"]
```

### 3-3: 邮件设置

```
点击"邮件"标签

收件人: info@yourcompany.co.jp  ← 改为您的公司邮箱
发件人: wordpress@yourcompany.co.jp
主题: [联系咨询] 来自[your-name]

邮件正文:
发件人: [your-name]
公司名: [your-company]
邮箱: [your-email]
电话: [your-phone]

咨询内容:
[your-message]
```

### 3-4: 自动回复邮件设置 (可选)

```
勾选「使用邮件(2)」

收件人: [your-email]
发件人: info@yourcompany.co.jp
主题: 已收到您的咨询

邮件正文:
[your-name] 先生/女士

感谢您的咨询。
我们已收到以下内容。

-----------------------------------------
【咨询内容】
[your-message]
-----------------------------------------

负责人将在2个工作日内与您联系。

株式会社〇〇
负责人:〇〇
Email: info@yourcompany.co.jp
```

### 3-5: 保存并复制短代码

```
保存 → 复制短代码
示例: [contact-form-7 id="123" title="联系表单"]
```

---

## 📧 Step 4: 邮件发送设置 (5分钟)

```
WP Mail SMTP → 设置
```

### 4-1: 基本设置

```
发件邮箱: info@yourcompany.co.jp
发件人名称: 株式会社〇〇

发送方式: Other SMTP
```

### 4-2: SMTP配置 (onamae.com)

```
SMTP主机: mail.onamae.com
加密方式: SSL
SMTP端口: 465
自动TLS: OFF（关闭）

认证: ON（开启）
SMTP用户名: info@yourcompany.co.jp
SMTP密码: [输入邮箱密码]
```

### 4-3: 测试发送

```
保存设置
↓
WP Mail SMTP → Email Test
↓
收件人: 填写自己的邮箱
↓
发送测试邮件
↓
✅ 确认收到邮件
```

**故障时的替代配置:**
```
SMTP端口: 587
加密方式: TLS
自动TLS: ON（开启）
```

---

## 📄 Step 5: 基本页面创建 (5分钟)

### 5-1: 联系我们页面

```
固定页面 → 添加新页面

标题: 联系我们
永久链接: contact

内容:
欢迎随时与我们联系。
负责人将在2个工作日内回复您。

[粘贴刚才复制的Contact Form 7短代码]

发布
```

### 5-2: 公司简介页面

```
固定页面 → 添加新页面

标题: 公司简介
永久链接: about

内容:
<h2>公司简介</h2>
公司名: 株式会社〇〇
成立: 20XX年X月
代表: 代表取締役 〇〇
地址: 東京都〇〇区〇〇
业务内容: 〇〇

发布
```

### 5-3: 首页设置

```
设置 → 阅读设置

主页显示: 静态页面
主页: [选择首页]
文章页: [选择新闻列表页]

保存更改
```

---

## 🎨 Step 6: 菜单设置 (5分钟)

```
外观 → 菜单 → 创建新菜单

菜单名称: 主导航菜单

添加页面:
- 首页
- 公司简介
- 业务内容
- 新闻
- 联系我们

菜单位置: Header Navigation
保存菜单
```

---

## ✅ Step 7: 最终确认 (5分钟)

### 检查清单

```
□ 查看网站 → 设计确认
□ 手机端显示确认 (F12 → 设备工具栏)
□ 联系页面显示确认
□ 填写表单 → 测试提交
□ 确认收到邮件 (管理员)
□ 确认收到自动回复邮件 (发送者)
□ 所有页面链接确认
□ 检查是否有404错误
```

---

## 🔒 安全设置 (+5分钟)

### SiteGuard设置

```
SiteGuard → 登录页面更改

登录页面更改: ON（开启）
更改后的登录页面名: [随机字符串]

※ 请收藏新的登录URL!
示例: https://yourcompany.co.jp/login_12345
```

### SSL强制重定向

```
onamae.com管理后台 → SSL设置
启用Let's Encrypt免费SSL证书

WordPress管理后台:
设置 → 常规
WordPress地址: https://yourcompany.co.jp
站点地址: https://yourcompany.co.jp
保存更改
```

---

## 📱 手机端适配确认

```
Chrome开发者工具:
F12 → 设备工具栏 (Ctrl+Shift+M)

检查设备:
- iPhone 12/13
- iPad
- Galaxy S20

检查要点:
✅ 菜单变成汉堡菜单
✅ 文字易读
✅ 表单易于输入
✅ 按钮易于点击
```

---

## 🎯 完成!

### 网站已上线!

```
✅ 联系表单正常工作
✅ 邮件发送成功
✅ 手机端适配完成
✅ 安全设置完成

总成本: ¥0
所需时间: 30分钟
```

---

## 📈 下一步 (可选)

### 1周内要做的事

```
□ 设置Google Analytics
□ 注册Google Search Console
□ 发布3篇新闻文章
□ 充实公司信息页面
□ 创建隐私政策页面
□ 生成站点地图 (XML Sitemaps)
```

### SEO基本设置

```
插件: Yoast SEO (免费)

设置:
- 网站标题设置
- 元描述
- SNS连接 (Twitter/Facebook)
- XML站点地图生成
```

### 自动备份设置

```
UpdraftPlus → 设置

文件备份计划: 每周
数据库备份计划: 每天
保留备份数: 4个

备份位置: Google Drive (免费)
```

---

## 🆘 故障排除

### 邮件收不到

```
【检查1】垃圾邮件文件夹
→ 检查垃圾邮件设置

【检查2】SMTP设置
→ WP Mail SMTP → Email Test 重新测试
→ 尝试端口 587 / TLS

【检查3】onamae.com邮件服务器
→ 在onamae.com管理后台确认邮件设置
→ 确认邮箱账户是否有效

【最后手段】
Contact Form 7 → 集成
→ 连接Sendinblue (免费: 300封/天)
```

### 表单不显示

```
【检查1】短代码
→ 确认是否正确复制
→ 检查 [ ] 符号是否是全角

【检查2】Contact Form 7已启用
→ 插件 → 已安装插件中确认

【检查3】清除缓存
→ 清除浏览器缓存
→ Ctrl+Shift+Delete
```

### 页面加载慢

```
【对策1】图片优化
→ 确认EWWW Image Optimizer已启用
→ 媒体 → 批量优化

【对- 2】删除不用的插件
→ 停用并删除未使用的插件

【对策3】缓存插件
→ 安装WP Super Cache
→ 设置 → 缓存 ON
```

---

## 💡 省时技巧

### 复制模板页面

```
固定页面列表 → 鼠标悬停在页面上
复制 (需要Duplicate Post插件)

或者:
页面编辑 → 复制所有内容
新建页面 → 粘贴
```

### 常用块重复使用

```
在编辑器中选择块
↓
选项 (⋮) → 添加到可重复使用块
↓
命名并保存

使用时:
添加块 → 可重复使用 → 选择
```

### 批量安装插件

```
插件 → 添加新插件
搜索 → 勾选复选框
批量操作 → 安装
启用所有选中的插件
```

---

## 📊 30分钟后的状态

```
【完成内容】
✅ 专业的企业网站
✅ 联系表单功能
✅ 邮件发送・自动回复
✅ 手机端适配
✅ 安全设置
✅ SSL对应 (HTTPS)

【费用】
💰 ¥0 (完全免费)

【接下来要做的】
📝 充实内容
📈 SEO对策
📊 访问分析
```

---

## 🎉 恭喜您!

您的企业网站已经上线了! 🚀

下一步:
1. 充实网站内容
2. 定期发布新闻文章
3. 强化SEO对策
4. 完善联系咨询流程

**如有问题，随时提供支持!** 💪
