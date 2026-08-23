# 同一域名下お名前メール与 Exchange Online 邮箱共存方案

## 1. 结论

可以在同一个域名下，让不同邮箱用户分别使用：

- お名前メール
- Exchange Online

例如：

```text
域名：softbs.jp

info@softbs.jp
→ お名前メール

user@softbs.jp
→ Exchange Online
```

这种方式技术上可以实现，一般称为：

**Split Delivery（分割投递）**

但需要注意：

> **不能通过给两个邮箱分别设置不同 MX 来实现。**

因为 MX 是针对整个域名 `softbs.jp` 设置的，而不是针对单独的邮箱账号设置的。

---

# 2. 为什么不能按照邮箱分别设置 MX？

DNS 管理的是：

```text
softbs.jp
```

因此 MX 可以设置：

```text
softbs.jp
↓
MX
↓
某个邮件服务器
```

但是不能设置成：

```text
info@softbs.jp
→ MX → お名前メール

user@softbs.jp
→ MX → Exchange Online
```

DNS 的 MX 不会根据 `info`、`user` 等邮箱用户名选择不同服务器。

也就是说：

```text
@softbs.jp
```

原则上必须先有一个统一的邮件入口。

---

# 3. 推荐的 Split Delivery 结构

如果确实希望：

```text
info@softbs.jp
→ お名前メール

user@softbs.jp
→ Exchange Online
```

可以考虑让 Exchange Online 成为邮件统一入口。

整体结构：

```text
Internet
   │
   │
   │ 发送到 @softbs.jp
   ↓
softbs.jp
   │
   │ DNS
   ↓
MX
   │
   ↓
Exchange Online
   │
   ├───────────────────────┐
   │                       │
   ↓                       ↓
user@softbs.jp        info@softbs.jp
   │                       │
Exchange中存在             Exchange中不作为普通邮箱处理
   │                       │
   ↓                       ↓
Exchange Mailbox      Mail Routing
                           │
                           ↓
                     お名前メール
                           │
                           ↓
                     info@softbs.jp
```

这样就实现：

| 邮箱地址 | 实际保存邮件的位置 |
|---|---|
| `user@softbs.jp` | Exchange Online |
| `info@softbs.jp` | お名前メール |

---

# 4. Exchange Online 的作用

这种情况下：

```text
softbs.jp
MX
↓
Exchange Online
```

Exchange Online 首先收到所有发给：

```text
xxx@softbs.jp
```

的邮件。

然后 Exchange 判断收件人。

### Exchange 用户

例如：

```text
user@softbs.jp
```

Exchange 中存在这个 Mailbox：

```text
邮件
↓
Exchange
↓
user@softbs.jp
```

直接保存到 Exchange。

---

### お名前メール用户

例如：

```text
info@softbs.jp
```

如果这个用户实际需要保留在お名前メール，则需要让 Exchange 把邮件继续转交给お名前メール侧。

概念上：

```text
info@softbs.jp
↓
Exchange
↓
判断该用户不在 Exchange 保存
↓
Mail Routing / Connector
↓
お名前メール
↓
info@softbs.jp
```

---

# 5. Exchange 的 Internal Relay

Exchange Online 支持将域名设置成：

**Internal Relay**

这种模式适用于：

> 同一个域名的一部分用户位于 Exchange Online，另外一部分用户位于其他邮件系统。

例如：

```text
softbs.jp
↓
Exchange Accepted Domain
↓
Internal Relay
```

然后：

```text
user@softbs.jp
↓
Exchange Mailbox
```

而其他需要送往外部邮件系统的邮箱：

```text
info@softbs.jp
↓
Mail Routing / Connector
↓
お名前メール
```

---

# 6. 不只是修改 MX

如果要让两个邮箱系统长期共存，不是简单设置：

```text
MX → Exchange
```

就结束了。

通常还需要考虑：

```text
DNS
│
├── MX
├── SPF
├── DKIM
└── DMARC

Exchange Online
│
├── Accepted Domain
├── Internal Relay
├── Mailbox
├── Mail Flow
└── Connector

お名前メール
│
├── Mailbox
├── 接收设置
├── SMTP
└── 发件认证
```

因此 Split Delivery 比单独使用一个邮箱服务复杂。

---

# 7. SPF 需要特别注意

如果：

```text
info@softbs.jp
```

从お名前メール发送邮件，而：

```text
user@softbs.jp
```

从 Exchange Online 发送邮件，那么：

```text
@softbs.jp
```

实际上存在两个合法的邮件发送系统。

因此 SPF 必须同时考虑：

```text
Exchange Online
+
お名前メール
```

不能只允许 Exchange。

否则可能出现：

```text
info@softbs.jp
↓
お名前メール发送
↓
对方检查 SPF
↓
SPF 不允许该服务器
↓
垃圾邮件 / 拒收风险
```

---

# 8. DKIM / DMARC 也需要考虑

除了 SPF，还建议正确配置：

### DKIM

负责给发出的邮件增加数字签名。

如果 Exchange 和お名前メール都负责发送：

```text
@softbs.jp
```

邮件，则两个系统的 DKIM 都需要分别考虑。

### DMARC

DMARC 用于告诉其他邮件服务器：

> 如果收到声称来自 `@softbs.jp` 的邮件，但是 SPF/DKIM 验证失败，应该如何处理。

因此两个邮箱系统共存时：

```text
SPF
DKIM
DMARC
```

需要统一设计。

---

# 9. 两个 MX 不等于同时投递

不要简单设置：

```text
MX 10 → Exchange
MX 20 → お名前メール
```

然后认为：

```text
Exchange用户 → Exchange
お名前用户 → お名前
```

这是错误理解。

MX Priority 主要表示：

```text
优先服务器
↓
失败
↓
备用服务器
```

并不是：

```text
根据邮箱用户名
↓
自动选择服务器
```

因此不能依靠两个 MX 实现 Split Delivery。

---

# 10. 方案一：全部使用 Exchange Online

结构最简单：

```text
softbs.jp
↓
MX
↓
Exchange Online
│
├── info@softbs.jp
├── user@softbs.jp
└── sales@softbs.jp
```

### 优点

- 邮件架构简单
- DNS 简单
- SPF/DKIM/DMARC 容易管理
- Outlook 使用体验好
- Exchange 日历、通讯录等功能统一
- 后期维护简单

### 缺点

每一个需要独立 Exchange Mailbox 的用户通常需要相应许可证。

如果邮箱数量增加，费用也会增加。

---

# 11. 方案二：全部使用お名前メール

如果只是普通企业邮箱，没有强烈的 Exchange 功能需求：

```text
softbs.jp
↓
MX
↓
お名前メール
│
├── info@softbs.jp
├── user@softbs.jp
└── sales@softbs.jp
```

然后使用：

```text
IMAP / SMTP
↓
Outlook
```

也可以正常通过 Outlook 收发邮件。

### 优点

- 成本通常较低
- 配置简单
- 适合少人数公司
- 不需要复杂的 Split Delivery

### 缺点

Exchange 特有的企业协作、日历、通讯录和 Microsoft 生态整合能力较弱。

---

# 12. 方案三：お名前メール + Exchange Online 共存

例如：

```text
softbs.jp
│
├── info@softbs.jp
│      ↓
│   お名前メール
│
└── user@softbs.jp
       ↓
    Exchange Online
```

邮件入口：

```text
Internet
↓
softbs.jp
↓
MX
↓
Exchange Online
↓
收件人判断
│
├── Exchange用户
│      ↓
│   Exchange Mailbox
│
└── お名前メール用户
       ↓
    Mail Routing
       ↓
    お名前メール
```

### 优点

可以只让真正需要 Exchange 功能的用户购买 Exchange 服务。

例如：

```text
社长 / 主要员工
→ Exchange

info / 普通业务邮箱
→ お名前メール
```

有可能降低许可证费用。

### 缺点

系统复杂度明显提高，需要维护：

- MX
- SPF
- DKIM
- DMARC
- Exchange Accepted Domain
- Internal Relay
- Connector
- Mail Routing
- お名前メール侧配置

因此如果只有 2～3 个邮箱，为节省少量许可证费用而使用这种架构，需要衡量维护成本。

---

# 13. 三种方案比较

| 方案 | 成本 | 配置难度 | 维护难度 | 推荐程度 |
|---|---:|---:|---:|---|
| 全部 Exchange | 较高 | 低 | 低 | ★★★★★ |
| 全部お名前メール | 低 | 低 | 低 | ★★★★☆ |
| Exchange + お名前共存 | 中 | 高 | 高 | ★★★☆☆ |

---

# 14. 如果只是两个邮箱

例如现在只有：

```text
info@softbs.jp
user@softbs.jp
```

如果没有特殊原因，最简单的是统一：

### Exchange 方案

```text
softbs.jp
↓
Exchange Online
│
├── info@softbs.jp
└── user@softbs.jp
```

或者：

### お名前メール方案

```text
softbs.jp
↓
お名前メール
│
├── info@softbs.jp
└── user@softbs.jp
```

如果确实存在：

> 一个用户必须使用 Exchange，但另一个邮箱希望继续使用便宜的お名前メール

这种情况下才比较值得考虑 Split Delivery。

---

# 15. 最终总结

同一个域名：

```text
softbs.jp
```

下面完全可以实现：

```text
info@softbs.jp
→ お名前メール

user@softbs.jp
→ Exchange Online
```

但不是通过：

```text
邮箱 A → MX A
邮箱 B → MX B
```

实现。

而是：

```text
softbs.jp
↓
统一 MX
↓
主邮件系统
↓
根据收件人进行 Mail Routing
↓
分别投递
```

如果以 Exchange Online 为主入口，典型架构为：

```text
softbs.jp
↓
MX
↓
Exchange Online
↓
Accepted Domain / Internal Relay
│
├── Exchange用户
│      ↓
│   Exchange Mailbox
│
└── お名前メール用户
       ↓
    Connector / Mail Routing
       ↓
    お名前メール
```

因此：

> **可以共存，但属于邮件路由设计问题，不是简单的 DNS MX 设置问题。**

如果邮箱数量很少，优先统一使用一个邮件系统；只有存在许可证成本、迁移过渡或特殊业务需求时，再考虑 Exchange Online + お名前メール的 Split Delivery。