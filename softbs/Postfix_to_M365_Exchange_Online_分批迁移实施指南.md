# Postfix → Microsoft 365 Exchange Online 分批迁移实施指南

## 1. 目的

在**不影响现有 Postfix
用户正常收发邮件**的前提下，将同一企业域名下的一部分邮箱用户分批迁移到
Microsoft 365 Exchange Online。

目标状态示例：

``` text
同一域名：example.com

Exchange Online
├── user1@example.com   ← 已迁移
└── user2@example.com   ← 已迁移

Postfix
├── info@example.com    ← 暂时保留
├── sales@example.com   ← 暂时保留
└── user3@example.com   ← 暂时保留
```

核心原则：

-   不需要一次迁移所有用户。
-   如果最终把 MX 切到 Exchange Online，而 Postfix
    仍保留部分用户，则必须建立 **Exchange Online → Postfix**
    的邮件路由。
-   推荐采用 **Exchange Online 作为统一入口 + Internal Relay + Connector
    → Postfix**。
-   不要用两个不同优先级 MX 来区分 Exchange 用户和 Postfix 用户。
-   用户迁移后，Postfix
    上该用户原有的转发、Alias、自动回复等配置需要逐项确认，并在 M365
    中重新建立相应功能。

------------------------------------------------------------------------

## 2. 迁移前现状流程图

假设当前所有用户都在 Postfix：

``` text
                    Internet
                       │
                       │ 发邮件到 xxx@example.com
                       ↓
                 DNS 查询 MX
                       │
                       ↓
             MX → mail.example.com
                       │
                       ↓
        A Record → Postfix Server IP
                       │
                       ↓
                    Postfix
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
 info@example.com  sales@...    user1@...
          │            │            │
          ↓            ↓            ↓
      原邮箱保存     原邮箱保存     原邮箱保存
```

当前关系：

``` text
example.com
   ↓
DNS MX
   ↓
mail.example.com
   ↓
Postfix Server
   ↓
全部 @example.com 用户
```

------------------------------------------------------------------------

## 3. 迁移后的目标流程图

例如先把 `user1`、`user2` 迁移到 M365，而 `info`、`sales`、`user3`
暂时继续使用 Postfix。

``` text
                         Internet
                            │
                            │ xxx@example.com
                            ↓
                      DNS 查询 MX
                            │
                            ↓
                   Exchange Online
                            │
               example.com = Internal Relay
                            │
              ┌─────────────┴──────────────┐
              │                            │
       Exchange 中存在用户            未迁移到 Exchange
              │                            │
      ┌───────┴───────┐                    │
      ↓               ↓                    ↓
 user1@example.com user2@example.com    Connector
      │               │                    │
      ↓               ↓                    ↓
 Exchange Mailbox Exchange Mailbox   mail.example.com
                                           │
                                           ↓
                                        Postfix
                                           │
                             ┌─────────────┼─────────────┐
                             ↓             ↓             ↓
                       info@example.com sales@...    user3@...
```

也就是说：

``` text
【迁移前】

softbs.jp
   ↓
当前 DNS 投递方式
   │
   ├── 有 MX → MX → Postfix
   │
   └── 无 MX → A/AAAA → Postfix
   ↓
全部用户


【分批迁移期间】

Internet
   ↓
MX
   ↓
Exchange Online
   │
   ├── 已迁移用户 → Exchange Mailbox
   │
   └── 未迁移用户 → Connector → Postfix


【全部迁移完成后】

Internet
   ↓
MX
   ↓
Exchange Online
   ↓
全部用户
```

------------------------------------------------------------------------

# 4. MX 切换到 M365 后，Postfix 的 A Record 是否失效？

**不会失效。**

MX 和 A/AAAA 是不同类型的 DNS Record。把 `softbs.jp` 的 MX 指向
Microsoft 365 Exchange Online 后，不会自动删除、覆盖或使 Postfix 使用的
A/AAAA Record 失效。

例如分批迁移期间可以同时存在：

``` text
softbs.jp
│
├── MX
│    ↓
│   xxxx.mail.protection.outlook.com
│    ↓
│   Exchange Online
│
└── mail.softbs.jp
     ↓ A Record
    Postfix Server IP
```

对于外部发送到 `xxx@softbs.jp` 的邮件，只要 `softbs.jp` 已经存在有效
MX，正常邮件投递首先按照 MX 进入 Exchange Online：

``` text
softbs.jp
   ↓
MX
   ↓
Exchange Online
```

`mail.softbs.jp` 的 A Record 仍然存在，但它不再作为 `@softbs.jp`
外部邮件的第一入口。

## 4.1 为什么 Postfix 的 A Record 还要保留？

因为未迁移用户仍然需要：

``` text
Exchange Online
   ↓
Connector
   ↓
mail.softbs.jp
   ↓
A Record
   ↓
Postfix Server IP
   ↓
Postfix
```

因此共存期间：

``` text
mail.softbs.jp
A → Postfix Server IP
```

通常必须继续保留。

如果 Connector 使用 `mail.softbs.jp` 作为目标，而删除该 A Record：

``` text
Exchange Online
   ↓
Connector
   ↓
mail.softbs.jp
   ↓
DNS 无法解析
   ↓
无法连接 Postfix
   ↓
未迁移用户可能无法收件
```

## 4.2 MX、A Record、Connector、Postfix 的职责

  项目                              作用
  --------------------------------- ----------------------------------------------
  `softbs.jp MX → M365`             决定发给 `@softbs.jp` 的外部邮件第一站
  `mail.softbs.jp A → Postfix IP`   把 Postfix 主机名解析到服务器 IP
  Exchange Connector                把未迁移用户的邮件从 Exchange 路由到 Postfix
  Postfix                           接收 Connector 转来的邮件并投递给原有用户
  `softbs.jp A → Web Server IP`     通常用于网站，与邮件 MX 独立

因此不要因为 MX 切到 M365 就删除 Postfix 的 A Record。

------------------------------------------------------------------------

# 5. 三个阶段的完整邮件流程对比

## 5.1 迁移前：当前存在 MX 的情况

``` text
softbs.jp
   ↓
MX
   ↓
mail.softbs.jp
   ↓
A Record
   ↓
Postfix Server
   ↓
全部 Postfix 用户
```

## 5.2 迁移前：当前没有 MX 的可能情况

``` text
softbs.jp
   ↓
查询 MX
   ↓
没有 MX
   ↓
softbs.jp A/AAAA
   ↓
Postfix Server
   ↓
全部 Postfix 用户
```

正式实施前必须通过 DNS 查询确认实际属于哪一种，不能预先假定。

## 5.3 分批迁移期间

``` text
                         softbs.jp
                            │
                            ↓
                           MX
                            │
                            ↓
                     Exchange Online
                            │
                   Internal Relay
                            │
              ┌─────────────┴─────────────┐
              │                           │
          已迁移用户                  未迁移用户
              │                           │
              ↓                           ↓
       Exchange Mailbox               Connector
                                          │
                                          ↓
                                  mail.softbs.jp
                                          │
                                     A Record
                                          ↓
                                  Postfix Server
                                          │
                                          ↓
                                  Postfix Mailbox
```

## 5.4 全部迁移完成后

``` text
softbs.jp
   ↓
MX
   ↓
Exchange Online
   ↓
全部用户
```

所有 Postfix 用户迁移完成并确认没有网站、NAS、业务系统等继续依赖 Postfix
后，才进入 Connector/Postfix 的最终清理阶段。

------------------------------------------------------------------------

# 6. 实施步骤------严格按照工作先后顺序

## STEP 1：调查现有 DNS

**此阶段只调查，不修改 DNS。**

确认当前 MX：

``` bash
dig MX example.com
```

Windows 也可以：

``` cmd
nslookup -type=mx example.com
```

如果结果类似：

``` text
example.com. MX 10 mail.example.com.
```

继续确认：

``` bash
dig A mail.example.com
```

确认返回 IP 是否为当前 Postfix Server。

同时记录现有：

-   MX
-   A / AAAA
-   SPF TXT
-   DKIM
-   DMARC
-   `mail.example.com` 的公网 IP

### 验收

必须明确当前邮件路径：

``` text
example.com
↓
MX
↓
mail.example.com
↓
Postfix IP
↓
Postfix
```

**此时不要修改 MX。**

------------------------------------------------------------------------

## STEP 2：调查现有 Postfix 配置

执行：

``` bash
postconf myhostname
postconf mydomain
postconf myorigin
postconf mydestination
postconf virtual_mailbox_domains
postconf virtual_alias_domains
postconf relay_domains
```

另外保存：

``` bash
postconf -n
```

重点确认：

-   Postfix 如何识别企业域名
-   邮箱是 Linux 本地用户还是 Virtual Mailbox
-   用户信息是否保存在 MySQL/PostgreSQL/LDAP
-   是否使用 Dovecot
-   是否存在 Alias
-   是否存在转发
-   是否存在 Catch-all
-   是否存在自动回复
-   是否存在 Mailing List

------------------------------------------------------------------------

## STEP 3：制作现有邮箱用户清单

在正式操作之前，必须把全部邮箱分类。

例如：

  邮箱                当前服务器    本次是否迁移  转发    历史邮件
  ------------------- ------------ -------------- ------- ----------
  info@example.com    Postfix            否       Gmail   保留
  sales@example.com   Postfix            否       无      保留
  user1@example.com   Postfix            是       Gmail   迁移
  user2@example.com   Postfix            是       无      迁移
  user3@example.com   Postfix            否       无      保留

不要只调查 Mailbox。

同时调查：

``` text
.forward
/etc/aliases
virtual_alias_maps
数据库中的 alias
邮件列表
自动回复
catch-all
```

------------------------------------------------------------------------

## STEP 4：备份 Postfix 和现有邮箱数据

在修改邮件系统之前备份：

-   `/etc/postfix/`
-   Postfix `main.cf`
-   Postfix `master.cf`
-   Alias 配置
-   Virtual Mailbox 配置
-   邮箱数据库
-   用户邮件数据
-   Dovecot 配置（如果使用）
-   DNS 当前配置截图/导出

并记录当前 MX，以便必要时回滚。

------------------------------------------------------------------------

## STEP 5：准备 Microsoft 365 Tenant

在 Microsoft 365 管理中心添加企业域名：

``` text
example.com
```

Microsoft 会要求添加 TXT Record 验证域名所有权。

例如：

``` text
TXT
MS=xxxxxxxx
```

此时：

**只添加 Microsoft 要求的域名验证 TXT。**

不要提前修改 MX。

------------------------------------------------------------------------

## STEP 6：验证企业域名

在 DNS 添加 Microsoft 提供的 TXT 后，在 Microsoft 365 中完成：

``` text
example.com
→ Verified
```

### 注意

域名验证成功：

**不等于已经把邮件切换到 Exchange。**

只要 MX 仍然指向 Postfix：

``` text
Internet
↓
MX
↓
Postfix
```

现有用户仍按原方式收件。

------------------------------------------------------------------------

## STEP 7：创建本次准备迁移的 Exchange 用户

例如本次只迁移：

``` text
user1@example.com
user2@example.com
```

则只给这些用户准备：

-   Microsoft 365 / Exchange Online 用户
-   Exchange License
-   Exchange Mailbox
-   正确的 Primary SMTP Address

不要为了迁移两个人就把所有 Postfix 用户全部创建成普通 Exchange Mailbox。

------------------------------------------------------------------------

## STEP 8：配置 Exchange Accepted Domain

因为迁移期间：

``` text
一部分用户 → Exchange
一部分用户 → Postfix
```

所以 `example.com` 应按照共存设计配置为：

``` text
Accepted Domain
↓
Internal Relay
```

概念：

``` text
example.com
   ↓
Exchange 收到邮件
   ↓
Exchange 中存在 Mailbox？
   │
   ├── YES → Exchange Mailbox
   │
   └── NO  → 继续路由到 Postfix
```

------------------------------------------------------------------------

## STEP 9：准备 Exchange → Postfix Connector

这是保证未迁移 Postfix 用户继续收件的关键步骤。

目标：

``` text
Exchange Online
↓
Connector
↓
mail.example.com
↓
Postfix
```

Connector 需要根据实际环境确认：

-   Postfix FQDN
-   公网 IP
-   TCP 25 可达性
-   TLS/证书要求
-   防火墙
-   Postfix 是否允许来自 M365 的 SMTP
-   是否需要限制只允许 Exchange Online 来源

**此时仍不要修改 MX。**

------------------------------------------------------------------------

## STEP 10：调整 Postfix 以接受 Exchange 转发的邮件

确认 Exchange Online 可以通过 SMTP 将未迁移用户邮件送到 Postfix。

需要根据现行 Postfix 架构检查：

``` text
smtpd_recipient_restrictions
mynetworks
relay_domains
transport_maps
virtual_mailbox_domains
virtual_alias_maps
```

不要为了 Connector 简单做：

``` text
允许全世界 Relay
```

否则可能形成 Open Relay。

目标只是：

``` text
Exchange Online
↓
Postfix
↓
合法的 @example.com 用户
```

------------------------------------------------------------------------

## STEP 11：在切 MX 前测试 Connector

这是非常重要的一步。

必须确认：

``` text
Exchange
↓
Connector
↓
Postfix
```

能够成功通信。

至少验证：

-   SMTP 25 可达
-   TLS 正常
-   Postfix 接受邮件
-   未迁移用户能够收到测试邮件
-   Postfix 日志无 Relay denied / Recipient rejected

Postfix 日志可根据系统查看：

``` bash
/var/log/maillog
```

或：

``` bash
/var/log/mail.log
```

------------------------------------------------------------------------

## STEP 12：处理已迁移用户的历史邮件

创建 Exchange Mailbox 并不会自动把 Postfix 中的旧邮件搬过去。

根据现有邮箱架构选择：

-   IMAP Migration
-   PST 导入
-   其他迁移工具

目标：

``` text
Postfix旧邮箱
↓
历史邮件迁移
↓
Exchange Mailbox
```

建议先用 1～2 个测试用户验证：

-   Inbox
-   Sent
-   Folder
-   日期
-   中文/日文邮件
-   附件

------------------------------------------------------------------------

## STEP 13：重新建立迁移用户的转发等规则

例如原 Postfix：

``` text
user1@example.com
↓
Postfix Forward
↓
abc@gmail.com
```

迁移到 Exchange 后，Postfix 的原规则不会自动成为 Exchange 配置。

需要逐项重新确认：

-   Forwarding
-   Alias
-   自动回复
-   Distribution Group
-   Shared Mailbox
-   Catch-all 替代方案
-   邮件规则

特别注意：

**Exchange Online 对外部自动转发可能受安全策略限制。**

因此不仅要设置 Forwarding Address，还要确认 M365 的 Outbound Spam /
Automatic Forwarding Policy。

------------------------------------------------------------------------

## STEP 14：检查 SPF / DKIM / DMARC 共存设计

迁移期间可能出现：

``` text
Exchange Online
+
Postfix
```

都发送：

``` text
@example.com
```

所以 SPF 必须考虑两个合法发信来源。

不能直接把 SPF 改成只允许 Microsoft，而 Postfix 仍然在发邮件。

同时检查：

-   SPF
-   Exchange DKIM
-   Postfix DKIM
-   DMARC

------------------------------------------------------------------------

# 7. 正式切换阶段

完成 STEP 1～14 后，才进入正式切换。

## STEP 15：降低 DNS TTL

建议在正式切换 MX 前提前降低相关 DNS TTL。

目的：

``` text
发生问题
↓
需要回滚
↓
DNS 可以较快恢复
```

具体 TTL 根据现行 DNS 环境制定。

------------------------------------------------------------------------

## STEP 16：再次执行切换前检查

确认：

``` text
□ Exchange 域名验证完成
□ 迁移用户 Mailbox 已创建
□ Exchange License 正常
□ Accepted Domain = Internal Relay
□ Connector 已建立
□ Exchange → Postfix SMTP 测试成功
□ Postfix 未迁移用户测试成功
□ 历史邮件迁移方案确认
□ 转发规则已经整理
□ SPF 共存方案确认
□ DKIM/DMARC 确认
□ Postfix 已备份
□ DNS 已备份
□ 回滚步骤准备完成
```

全部确认以后才能切 MX。

------------------------------------------------------------------------

## STEP 17：修改 MX → Exchange Online

原来：

``` text
example.com
↓
MX
↓
mail.example.com
↓
Postfix
```

修改成 Microsoft 为该 Tenant 提供的实际 MX：

``` text
example.com
↓
MX
↓
xxxx.mail.protection.outlook.com
↓
Exchange Online
```

**不要自己猜 Microsoft MX 值。**

必须使用 Microsoft 365 管理后台显示的实际值。

------------------------------------------------------------------------

## STEP 18：正式验证已迁移用户

测试：

``` text
外部 Gmail
↓
user1@example.com
↓
Exchange Online
↓
Exchange Mailbox
```

反方向：

``` text
user1@example.com
↓
Exchange Online
↓
外部 Gmail
```

检查：

-   收件
-   发件
-   Reply
-   附件
-   SPF
-   DKIM
-   DMARC
-   Spam 判定
-   Outlook

------------------------------------------------------------------------

## STEP 19：正式验证未迁移 Postfix 用户

这是本次迁移最重要的验收之一。

测试：

``` text
外部 Gmail
↓
info@example.com
↓
MX
↓
Exchange Online
↓
Internal Relay
↓
Connector
↓
Postfix
↓
info@example.com
```

确认：

``` text
info@example.com      OK
sales@example.com     OK
user3@example.com     OK
```

同时检查 Exchange Mail Flow 和 Postfix Log。

------------------------------------------------------------------------

## STEP 20：验证 Exchange 用户 ↔ Postfix 用户互发

必须测试：

``` text
user1@example.com
Exchange
↓
info@example.com
Postfix
```

以及：

``` text
info@example.com
Postfix
↓
user1@example.com
Exchange
```

确保同域名内部用户之间也能正常互发。

------------------------------------------------------------------------

# 8. 第一批迁移完成后的状态

例如：

``` text
                         Internet
                            ↓
                     Exchange Online
                            │
              ┌─────────────┴─────────────┐
              │                           │
           M365用户                  Postfix用户
              │                           │
        user1@example.com              Connector
        user2@example.com                 │
                                          ↓
                                       Postfix
                                          │
                                 info@example.com
                                 sales@example.com
                                 user3@example.com
```

此时不要删除 Postfix。

------------------------------------------------------------------------

# 9. 第二批、第三批用户迁移

后续每迁移一个用户，都按照固定流程：

``` text
① 确认该用户 Postfix 邮箱
↓
② 调查 Forward / Alias / 自动回复
↓
③ 创建/确认 Exchange Mailbox
↓
④ 迁移历史邮件
↓
⑤ 在 Exchange 重建必要规则
↓
⑥ 切换该用户的实际投递关系
↓
⑦ 外部收件测试
↓
⑧ 外部发件测试
↓
⑨ Exchange ↔ Postfix 同域互发测试
↓
⑩ 确认稳定
```

然后继续下一批。

------------------------------------------------------------------------

# 10. 全部用户迁移完成

最终：

``` text
Postfix用户 = 0
```

此时：

``` text
Internet
   ↓
MX
   ↓
Exchange Online
   │
   ├── info@example.com
   ├── sales@example.com
   ├── user1@example.com
   ├── user2@example.com
   └── user3@example.com
```

不再需要：

``` text
Exchange
↓
Connector
↓
Postfix
```

------------------------------------------------------------------------

## STEP 21：取消 Postfix 共存路由

确认所有用户已经迁移并经过稳定运行后：

-   停止 Exchange → Postfix Connector
-   清理共存 Mail Flow
-   检查是否仍有应用/设备使用 Postfix SMTP
-   检查网站、监控、NAS、打印机、业务系统等是否通过 Postfix 发信

不要因为"员工邮箱迁移完成"就立即关闭 Postfix。

很多服务器可能仍然使用：

``` text
Web Server
NAS
Monitoring
Application
Cron
Printer
↓
Postfix SMTP
```

------------------------------------------------------------------------

## STEP 22：Accepted Domain 从 Internal Relay 调整到最终状态

所有收件人全部进入 Exchange 后，再根据最终架构把域名调整为正常的
Exchange Online 权威域设计。

最终：

``` text
example.com
↓
Exchange Online
↓
全部 Mailbox / Group / Shared Mailbox
```

------------------------------------------------------------------------

## STEP 23：最终整理 SPF / DKIM / DMARC

如果 Postfix 已经完全停止发送 `@example.com` 邮件，则可以从 SPF 中移除
Postfix 发信来源。

最终只保留实际仍然使用的发信平台。

再次验证：

``` text
SPF  → PASS
DKIM → PASS
DMARC → PASS
```

------------------------------------------------------------------------

# 11. 回滚方案

如果切 MX 后发现未迁移 Postfix 用户无法正常收件：

``` text
问题发生
↓
停止继续迁移
↓
检查 Exchange Message Trace
↓
检查 Connector
↓
检查 Postfix Log
↓
检查 Firewall / TCP 25 / TLS
```

如果短时间无法解决，并且业务要求立即恢复：

``` text
MX
Exchange Online
↓
回滚
↓
原 Postfix MX
```

恢复：

``` text
Internet
↓
MX
↓
mail.example.com
↓
Postfix
```

因此在正式切换之前必须保留：

-   原 MX 值
-   原 DNS 配置
-   Postfix 配置备份
-   用户数据备份

------------------------------------------------------------------------

# 12. 最终工作顺序总览

``` text
【调查阶段】

01. 调查现有 DNS，确认 MX 是否存在，并检查 A/AAAA
 ↓
02. 调查 Postfix
 ↓
03. 制作全部邮箱用户清单
 ↓
04. 调查 Forward / Alias / 自动回复
 ↓
05. 备份 Postfix / 邮箱 / DNS

        ↓

【M365准备阶段】

06. M365 添加域名
 ↓
07. TXT 验证域名
 ↓
08. 创建第一批 Exchange 用户
 ↓
09. 配置 Internal Relay
 ↓
10. 配置 Exchange → Postfix Connector
 ↓
11. 调整 Postfix 接收条件
 ↓
12. 测试 Connector

        ↓

【用户迁移准备】

13. 迁移历史邮件
 ↓
14. 重建 Forward / Alias 等
 ↓
15. 检查 SPF / DKIM / DMARC

        ↓

【正式切换】

16. 降低 TTL
 ↓
17. 最终检查
 ↓
18. MX → Exchange Online

        ↓

【验收】

19. 测试 Exchange 用户收发
 ↓
20. 测试 Postfix 用户收发
 ↓
21. 测试 Exchange ↔ Postfix
 ↓
22. 监控日志

        ↓

【继续分批迁移】

23. 第二批用户
 ↓
24. 第三批用户
 ↓
25. 全部用户进入 M365

        ↓

【收尾】

26. 停止 Connector
 ↓
27. 检查系统是否仍使用 Postfix SMTP
 ↓
28. 调整 Accepted Domain 最终状态
 ↓
29. 整理 SPF / DKIM / DMARC
 ↓
30. Postfix 下线或仅保留必要 SMTP 功能
```

# 13. 最重要的注意事项

1.  **不要先改 MX，再配置 Connector。**
2.  **不要使用两个 MX 来区分 Postfix 用户和 M365 用户。**
3.  **Connector 必须在 MX 切换之前配置并测试。**
4.  **Postfix 未迁移用户必须在切换后逐个验证。**
5.  **Postfix 的转发规则不会自动迁移到 Exchange。**
6.  **历史邮件迁移与新邮件路由是两件不同的工作。**
7.  **共存期间 SPF 必须同时考虑 Postfix 和 Exchange 的发信。**
8.  **全部用户迁完之前不要关闭 Postfix。**
9.  **全部用户迁完后也要检查网站、NAS、应用程序等是否仍使用 Postfix
    SMTP。**
10. **任何正式 DNS 修改前都必须准备回滚方案。**
