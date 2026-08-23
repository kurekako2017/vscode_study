# 域名、DNS 与企业邮箱（Exchange / お名前メール）配置说明

## 1. 基本概念

拥有一个域名，例如：

```text
softbs.jp
```

并不代表自动拥有：

```text
info@softbs.jp
```

要使用企业邮箱，还必须有一个**邮件服务器 / 邮箱服务（Mail Hosting）**。

整体关系：

```text
域名：softbs.jp
        │
        ↓
DNS / ネームサーバー
        │
        ├── A / CNAME → 网站服务器
        │
        └── MX        → 邮件服务器
                            │
                            ├── Exchange Online
                            ├── お名前メール
                            ├── Google Workspace
                            └── 其他邮件服务器
```

---

## 2. DNS 在哪里设置？

如果域名通过お名前.com管理，并且当前 DNS 也是お名前.com负责，则进入：

```text
お名前.com Navi
   ↓
ネームサーバー / DNS
   ↓
DNS設定
   ↓
DNSレコード設定
```

这里就是设置：

- A
- AAAA
- CNAME
- MX
- TXT

等 DNS Record 的地方。

**不是「レンタルサーバー」中的 Server DNS 邮箱设置。**

---

## 3. MX 是什么？

MX = Mail Exchanger。

它负责告诉互联网：

> 发往 `@softbs.jp` 的邮件应该交给哪一个邮件服务器。

例如：

```text
客户发送邮件
     ↓
info@softbs.jp
     ↓
查询 softbs.jp DNS
     ↓
找到 MX
     ↓
Exchange Online
     ↓
info@softbs.jp 邮箱
```

所以：

**决定收件服务器的核心 DNS Record 就是 MX。**

---

## 4. Exchange 与域名的关系

如果使用 Exchange Online，可以理解成：

```text
softbs.jp
   ↓
DNS
   ↓
MX
   ↓
Exchange Online
   ↓
info@softbs.jp
```

Exchange 是实际负责：

- 收邮件
- 发邮件
- 保存邮件
- 管理邮箱
- 管理日历
- 邮件安全

等功能的邮件服务。

---

## 5. Exchange 和 Microsoft 365 的关系

Exchange Online 本身就是 Microsoft 的企业邮箱服务。

Microsoft 365 是更大的产品和管理体系，可以包含：

```text
Microsoft 365
│
├── Exchange Online
├── Outlook
├── Word
├── Excel
├── Teams
└── OneDrive
```

也可以单独购买 Exchange Online Plan，而不一定购买完整的 Office 套餐。

因此：

```text
Exchange Online = 企业邮箱服务

Outlook = 邮件客户端

Microsoft 365 = Microsoft 企业服务/套餐/管理体系
```

---

## 6. Outlook 不等于 Exchange

这一点非常重要。

Outlook 可以连接很多不同的邮件服务器。

例如：

```text
Exchange Online
      ↕
   Outlook
```

也可以：

```text
お名前メール
      ↕
  IMAP / SMTP
      ↕
   Outlook
```

因此，如果只是希望：

> 使用 Outlook 软件收发 `info@softbs.jp`

并不一定需要 Exchange。

可以直接：

```text
お名前メール
      ↓
info@softbs.jp
      ↕
   IMAP / SMTP
      ↕
    Outlook
```

---

## 7. 使用 Exchange 创建企业邮箱的标准流程

假设希望创建：

```text
info@softbs.jp
```

推荐流程：

### STEP 1：拥有域名

例如：

```text
softbs.jp
```

域名可以购买于：

- お名前.com
- Xserver
- Cloudflare Registrar
- 其他域名服务商

---

### STEP 2：在 Exchange / Microsoft 管理后台添加域名

添加：

```text
softbs.jp
```

Microsoft 会要求证明这个域名属于你。

通常会提供一条 TXT DNS Record。

---

### STEP 3：在域名 DNS 添加验证记录

进入：

```text
お名前.com
↓
ネームサーバー / DNS
↓
DNS設定
↓
DNSレコード設定
```

按照 Microsoft 提供的内容添加 TXT Record。

Microsoft 验证成功以后：

```text
softbs.jp
        ↓
Microsoft 确认域名所有权
```

---

### STEP 4：创建 Exchange 邮箱

在 Exchange / Microsoft 后台创建：

```text
info@softbs.jp
```

以后也可以继续创建：

```text
sales@softbs.jp
admin@softbs.jp
support@softbs.jp
```

---

## 8. 设置 Exchange 的 DNS Record

Microsoft 会提供需要添加的 DNS Record。

不要自己猜 VALUE，应以 Microsoft 管理后台显示的实际值为准。

通常包括：

| TYPE | 作用 |
|---|---|
| MX | 指定 Exchange 为收件服务器 |
| TXT / SPF | 指定允许发送 `@softbs.jp` 邮件的服务器 |
| CNAME | Outlook 自动发现等 |
| DKIM | 邮件数字签名 |
| DMARC | 防止域名被伪造发送邮件 |

其中最重要的是：

```text
MX
```

Exchange Online 的 MX 通常类似：

```text
xxxx.mail.protection.outlook.com
```

但具体值必须使用 Microsoft 为 `softbs.jp` 提供的值。

---

## 9. DNS 不是创建具体邮箱的地方

DNS 不负责创建：

```text
info@softbs.jp
```

DNS 负责的是：

```text
@softbs.jp
的邮件应该送到哪里？
```

例如：

```text
softbs.jp
     ↓
DNS
     ↓
MX
     ↓
Exchange Online
```

然后 Exchange 内部再负责：

```text
Exchange Online
│
├── info@softbs.jp
├── sales@softbs.jp
├── admin@softbs.jp
└── support@softbs.jp
```

因此，Exchange 已经正确配置域名以后，再增加：

```text
sales@softbs.jp
```

通常不需要重新修改 DNS。

只需要在 Exchange 后台创建邮箱即可。

---

## 10. 网站服务器和邮箱服务器可以完全分开

例如：

```text
softbs.jp
│
├── 网站
│     ↓
│    A / CNAME
│     ↓
│    Web Server
│
└── 邮件
      ↓
     MX
      ↓
     Exchange Online
```

因此完全可以：

```text
域名       → お名前.com
DNS        → お名前.com
网站       → Xserver / VPS / AWS
企业邮箱   → Exchange Online
```

彼此并不冲突。

---

## 11. 如果不用 Exchange

也可以使用其他邮件服务，例如：

### 方案 A：お名前メール

```text
softbs.jp
   ↓
DNS MX
   ↓
お名前メール
   ↓
info@softbs.jp
```

### 方案 B：Google Workspace

```text
softbs.jp
   ↓
DNS MX
   ↓
Google Workspace
   ↓
info@softbs.jp
```

### 方案 C：Exchange Online

```text
softbs.jp
   ↓
DNS MX
   ↓
Exchange Online
   ↓
info@softbs.jp
```

原理完全相同。

---

## 12. 同一个邮箱能否同时在お名前メール和 Exchange 创建？

技术上可以分别创建：

```text
お名前メール
└── info@softbs.jp

Exchange Online
└── info@softbs.jp
```

但是：

**创建了两个同名邮箱，不代表两边会自动同时收到邮件。**

最终邮件首先送到哪里，由：

```text
softbs.jp 的 MX
```

决定。

例如 MX 指向 Exchange：

```text
info@softbs.jp
       ↓
DNS
       ↓
MX
       ↓
Exchange
```

那么 Exchange 是主要收件服务器。

如果 MX 指向お名前メール：

```text
info@softbs.jp
       ↓
DNS
       ↓
MX
       ↓
お名前メール
```

那么お名前メール是主要收件服务器。

如果确实需要两边同时保存邮件，需要额外设计：

- 邮件转发
- Mail Routing
- Dual Delivery

等机制。

**不要简单地通过配置两个 MX 来实现双重收件。**

---

## 13. 最简单的理解方式

整个企业邮箱配置可以记成下面四层：

```text
【第 1 层：域名】

softbs.jp

        ↓

【第 2 层：DNS】

A   → 网站去哪里
MX  → 邮件去哪里

        ↓

【第 3 层：邮件服务器】

Exchange Online
或
お名前メール
或
Google Workspace

        ↓

【第 4 层：具体邮箱】

info@softbs.jp
sales@softbs.jp
admin@softbs.jp
```

---

## 14. Exchange 配置的最终流程

如果决定使用 Exchange，整个流程可以浓缩成：

```text
① 购买/拥有域名
   softbs.jp

        ↓

② Exchange / Microsoft 后台
   添加 softbs.jp

        ↓

③ Microsoft 提供域名验证 DNS Record

        ↓

④ お名前.com
   DNSレコード設定
   添加验证记录

        ↓

⑤ 域名验证成功

        ↓

⑥ Exchange 创建邮箱
   info@softbs.jp

        ↓

⑦ Microsoft 提供邮件 DNS 设置

        ↓

⑧ お名前.com DNS 添加
   MX
   SPF
   DKIM
   DMARC
   CNAME 等

        ↓

⑨ MX 指向 Exchange

        ↓

⑩ info@softbs.jp
   正式通过 Exchange 收发邮件
```

## 15. 一句话总结

> **域名决定邮箱地址叫什么，DNS 的 MX 决定邮件送到哪个邮件服务器，Exchange / お名前メール等邮件服务负责真正创建、收发和保存 `info@softbs.jp`。**

如果使用 Exchange：

> **在 Exchange 中添加并验证 `softbs.jp` → 创建 `info@softbs.jp` → 根据 Microsoft 提供的参数，在域名 DNS 中配置 MX/SPF/DKIM/DMARC → 完成企业邮箱配置。**