# Enterprise Retail Intelligence Platform（ERIP）
# Agent 面试指南 V4 正式版
## Part 02-2：PostgreSQL / JWT / RBAC

# Chapter 8 PostgreSQL

## 面接官
なぜPostgreSQLを採用しましたか。

## 回答
ERIPでは文書、チャンク、承認、監査ログなど、
リレーショナルデータを安全に管理する必要があります。

そのため、ACID特性を備えたPostgreSQLを採用しました。

---

## 面接官
InMemoryでは駄目ですか。

## 回答
学習用途では問題ありませんが、
企業システムでは永続化、トランザクション、
バックアップが必要なためPostgreSQLを利用します。

# Chapter 9 JWT

## 面接官
JWTを利用した理由は何ですか。

## 回答
JWTにより利用者を認証し、
APIごとにログイン状態を確認できます。

JWTには本人情報のみを保持し、
権限情報はRBACで管理しています。

---

## 面接官
JWTへ権限を書いていますか。

## 回答
いいえ。

ERIPではJWTは認証、
RBACは認可として役割を分離しています。

# Chapter 10 RBAC

## 面接官
RBACとは何ですか。

## 回答
Role Based Access Controlです。

ロールごとに利用可能な機能を制御します。

---

## 面接官
ERIPのロールを説明してください。

## 回答
管理者、マネージャー、一般利用者を定義しています。

管理者は権限管理、
マネージャーは承認、
一般利用者は文書検索・分析依頼などを利用します。

---

## 面接官
なぜRBACを採用しましたか。

## 回答
企業システムでは利用者ごとに
操作可能な機能を制御する必要があるためです。

# Chapter 11 認証・認可フロー

```text
Client
 ↓
JWT認証
 ↓
Current User
 ↓
Permission Check
 ↓
Business Service
```

## 学习提示（中文）

- JWT = Authentication（认证）
- RBAC = Authorization（授权）
- 面试回答时不要混淆两者。

# Part02 总结

ERIP Backend 采用以下架构：

React
→ FastAPI
→ Router
→ Service
→ Repository
→ PostgreSQL

认证使用 JWT，
授权使用 RBAC，
各层职责清晰，便于维护与测试。
