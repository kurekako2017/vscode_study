# 域名和邮箱服务器配置指南

## 📧 完整邮件系统配置

本指南涵盖：
1. 域名购买和 DNS 配置
2. 企业邮箱设置（收件）
3. 邮件发送服务（表单通知）
4. SPF/DKIM/DMARC 认证

---

## 一、域名购买和配置

### 1.1 购买域名

**推荐注册商（按性价比排序）**：

| 注册商 | .com 价格 | 优点 | 缺点 |
|--------|-----------|------|------|
| **Cloudflare Registrar** | ¥60/年 | 成本价，无隐藏费用 | 需要先添加到 Cloudflare |
| **阿里云（万网）** | ¥65/年 | 国内访问快，支持支付宝 | 需要实名认证 |
| **Namecheap** | $9/年 | 隐私保护免费 | 国际支付 |
| **GoDaddy** | $20/年 | 知名度高 | 续费贵 |

### 1.2 迁移到 Cloudflare（强烈推荐）

**为什么用 Cloudflare？**
- ✅ 免费 CDN 加速
- ✅ 免费 SSL 证书
- ✅ 免费 DDoS 防护
- ✅ 免费邮件转发（Email Routing）
- ✅ 快速 DNS 解析

**迁移步骤**：

1. 注册 [Cloudflare](https://dash.cloudflare.com) 账号
2. 点击 "Add a Site"，输入域名
3. 选择 **Free 套餐**
4. Cloudflare 会扫描现有 DNS 记录
5. 复制提供的 Nameserver 地址（例如）：
   ```
   ava.ns.cloudflare.com
   brad.ns.cloudflare.com
   ```
6. 到域名注册商处修改 DNS 服务器：
   - **阿里云**：域名管理 → DNS 修改 → 修改 DNS 服务器
   - **Namecheap**：Domain List → Manage → Nameservers → Custom DNS
   - **GoDaddy**：My Domains → Domain Settings → Nameservers
7. 等待生效（通常 10-30 分钟，最长 24 小时）

### 1.3 基础 DNS 记录配置

在 Cloudflare DNS 设置中添加：

```
# 主域名指向 Vercel
类型: A
名称: @
IPv4 地址: 76.76.21.21
代理状态: 已代理（橙色云朵）

# www 子域名指向 Vercel
类型: CNAME
名称: www
目标: cname.vercel-dns.com
代理状态: 已代理

# 邮件服务器（后面配置）
类型: MX
名称: @
优先级: 10
邮件服务器: mx.zoho.com
代理状态: 仅 DNS
```

---

## 二、企业邮箱方案（接收邮件）

### 方案对比

| 方案 | 成本 | 邮箱数 | 存储 | 适用场景 |
|------|------|--------|------|----------|
| **Cloudflare Email Routing** | 免费 | 无限转发 | 无存储 | 个人/小团队，转发到 Gmail |
| **Zoho Mail Lite** | 免费 | 5个 | 5GB/邮箱 | 小型企业 |
| **Gmail Workspace** | ¥43/月/用户 | 无限 | 30GB | 专业企业 |
| **腾讯企业邮** | 免费 | 50个 | 2GB/邮箱 | 国内企业 |

### 推荐方案 1: Cloudflare Email Routing（最简单）

**适合**：不需要独立邮箱，只需要接收表单通知

**配置步骤**：

1. 在 Cloudflare Dashboard 点击 "Email" → "Email Routing"
2. 点击 "Enable Email Routing"
3. 添加目标地址（你的个人邮箱，如 Gmail）
4. 设置转发规则：
   ```
   info@yourdomain.com → your-gmail@gmail.com
   contact@yourdomain.com → your-gmail@gmail.com
   admin@yourdomain.com → your-gmail@gmail.com
   ```
5. Cloudflare 自动配置 MX 记录
6. 验证完成（发送测试邮件到 info@yourdomain.com）

**在 Gmail 中设置发件人别名**：

1. Gmail 设置 → "账号和导入"
2. "用其他地址发送邮件" → "添加另一个电子邮件地址"
3. 填写：
   - 名称：公司名称
   - 邮箱：info@yourdomain.com
4. 使用 Brevo SMTP 服务器发送（见下文）

### 推荐方案 2: Zoho Mail（独立邮箱）

**适合**：需要专业的企业邮箱系统

**配置步骤**：

1. 注册 [Zoho Mail](https://www.zoho.com/mail/)
2. 选择 "Lite" 套餐（免费）
3. 添加域名并验证所有权（添加 TXT 记录）
4. 在 Cloudflare DNS 添加 Zoho 提供的记录：

```
# MX 记录
类型: MX
名称: @
优先级: 10
内容: mx.zoho.com
代理状态: 仅 DNS

类型: MX
名称: @
优先级: 20
内容: mx2.zoho.com
代理状态: 仅 DNS

# SPF 记录
类型: TXT
名称: @
内容: v=spf1 include:zoho.com ~all

# DKIM 记录（Zoho 提供）
类型: TXT
名称: zoho._domainkey
内容: [Zoho控制台复制]
```

5. 创建邮箱账户：
   - info@yourdomain.com
   - contact@yourdomain.com
   - admin@yourdomain.com

6. 设置邮件客户端或使用 Zoho Webmail

---

## 三、邮件发送服务（表单通知）

### 3.1 Brevo (SendinBlue) 配置

**免费额度**：300 封/天

**注册和配置**：

1. 访问 [Brevo.com](https://www.brevo.com)
2. 注册账号（填写真实信息）
3. 进入 Dashboard

### 3.2 验证发件域名

**关键步骤**：

1. 点击 "Senders & IP" → "Domains"
2. 点击 "Add a Domain"
3. 输入域名：`yourdomain.com`
4. Brevo 提供 3 条 DNS 记录，在 Cloudflare 添加：

```
# SPF 记录（如果已有 Zoho 的，合并）
类型: TXT
名称: @
内容: v=spf1 include:spf.sendinblue.com include:zoho.com ~all

# DKIM 记录
类型: TXT
名称: mail._domainkey
内容: k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA... [Brevo提供]

# DMARC 记录
类型: TXT
名称: _dmarc
内容: v=DMARC1; p=none; rua=mailto:admin@yourdomain.com
```

5. 等待验证通过（几分钟到几小时）

### 3.3 获取 API Key

1. 点击右上角用户名 → "SMTP & API"
2. 点击 "Create a new API Key"
3. 名称：`company-website-production`
4. 权限：勾选 "Send emails"
5. 复制 API Key：`xkeysib-xxxxx`
6. 添加到 Vercel 环境变量

### 3.4 创建邮件模板

在 Brevo 创建以下模板：

#### 模板 1: 联系表单通知

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>新的联系表单提交</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #0369a1;">🔔 新的联系表单提交</h2>
    
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="padding: 10px; background: #f0f9ff; font-weight: bold;">姓名</td>
            <td style="padding: 10px;">{{ params.name }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f0f9ff; font-weight: bold;">邮箱</td>
            <td style="padding: 10px;">{{ params.email }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f0f9ff; font-weight: bold;">电话</td>
            <td style="padding: 10px;">{{ params.phone }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f0f9ff; font-weight: bold;">公司</td>
            <td style="padding: 10px;">{{ params.company }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f0f9ff; font-weight: bold;">主题</td>
            <td style="padding: 10px;">{{ params.subject }}</td>
        </tr>
    </table>
    
    <div style="margin-top: 20px; padding: 15px; background: #f9fafb; border-left: 4px solid #0369a1;">
        <h3 style="margin-top: 0;">留言内容：</h3>
        <p style="white-space: pre-wrap;">{{ params.message }}</p>
    </div>
    
    <p style="color: #6b7280; font-size: 12px; margin-top: 30px;">
        提交时间：{{ params.submitted_at }}<br>
        IP 地址：{{ params.ip_address }}
    </p>
</body>
</html>
```

**模板 ID**: 记录下来（如 `1`），在代码中使用

---

## 四、邮件认证配置（重要！）

### 4.1 SPF 记录（发件人策略框架）

**作用**：防止邮件被标记为垃圾邮件

如果同时使用 Zoho + Brevo：

```
类型: TXT
名称: @
内容: v=spf1 include:spf.sendinblue.com include:zoho.com ~all
```

### 4.2 DKIM 记录（邮件签名）

**Brevo DKIM**：
```
类型: TXT
名称: mail._domainkey
内容: [Brevo 提供的公钥]
```

**Zoho DKIM**：
```
类型: TXT
名称: zoho._domainkey
内容: [Zoho 提供的公钥]
```

### 4.3 DMARC 记录（域名邮件认证报告）

```
类型: TXT
名称: _dmarc
内容: v=DMARC1; p=quarantine; rua=mailto:admin@yourdomain.com; pct=100; adkim=s; aspf=s
```

**参数说明**：
- `p=quarantine`：可疑邮件隔离（建议先用 `p=none` 测试）
- `rua=mailto:...`：接收报告的邮箱
- `pct=100`：应用到 100% 的邮件
- `adkim=s`：严格 DKIM 对齐
- `aspf=s`：严格 SPF 对齐

---

## 五、配置验证

### 5.1 DNS 记录检查

使用工具检查：
- [MXToolbox](https://mxtoolbox.com) - 检查 MX、SPF、DKIM
- [Mail-Tester](https://www.mail-tester.com) - 测试邮件评分

### 5.2 发送测试邮件

```bash
# 使用 Node.js 测试
node scripts/test-email.js
```

`scripts/test-email.js`：
```javascript
const https = require('https');

const data = JSON.stringify({
  sender: { email: 'info@yourdomain.com', name: '公司名称' },
  to: [{ email: 'your-test@gmail.com' }],
  subject: '测试邮件',
  htmlContent: '<p>这是一封测试邮件</p>'
});

const options = {
  hostname: 'api.brevo.com',
  path: '/v3/smtp/email',
  method: 'POST',
  headers: {
    'api-key': 'YOUR_BREVO_API_KEY',
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, (res) => {
  console.log(`状态码: ${res.statusCode}`);
  res.on('data', (d) => process.stdout.write(d));
});

req.on('error', (error) => console.error(error));
req.write(data);
req.end();
```

### 5.3 检查清单

- [ ] 域名 DNS 已迁移到 Cloudflare
- [ ] MX 记录配置正确
- [ ] SPF 记录验证通过
- [ ] DKIM 记录验证通过
- [ ] DMARC 记录已添加
- [ ] Brevo 域名验证通过
- [ ] 可以接收邮件（测试发送到 info@yourdomain.com）
- [ ] 可以发送邮件（使用 Brevo API）
- [ ] 邮件未进入垃圾箱

---

## 六、常见问题

### Q1: 邮件进入垃圾箱怎么办？

**解决方案**：
1. 确保 SPF、DKIM、DMARC 都正确配置
2. 使用 Mail-Tester 测试，评分应 > 8/10
3. 避免使用垃圾邮件关键词（"免费"、"点击这里"等）
4. 确保邮件内容与发件域名相关
5. 逐步增加发送量（不要一开始就大量发送）

### Q2: Cloudflare Email Routing vs Zoho Mail 选哪个？

| 需求 | 推荐方案 |
|------|---------|
| 只需接收表单通知 | Cloudflare Email Routing |
| 需要回复客户邮件 | Zoho Mail |
| 多人协作管理邮件 | Zoho Mail 或 Gmail Workspace |

### Q3: Brevo 免费版 300 封/天够吗？

**估算**：
- 联系表单提交：~5-10 封/天
- 新闻订阅确认：~2-5 封/天
- 总计：~10-20 封/天

对于小型企业完全够用。如果超出，升级到 Lite 套餐（$25/月，40,000 封）。

---

## 📝 配置总结

完成后你将拥有：

✅ **专业域名**（yourdomain.com）  
✅ **企业邮箱**（info@yourdomain.com）  
✅ **邮件发送能力**（Brevo API）  
✅ **反垃圾邮件认证**（SPF/DKIM/DMARC）  
✅ **总成本**：¥60-100/年（仅域名费用）

🎉 现在你的企业网站拥有了完整的通信能力！
