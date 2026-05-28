# Spring Boot 中日学习概要教程（01）

Spring Boot 是现代 Java 企业开发里最常见的入口框架之一。它的重点不是“替代所有框架”，而是把项目启动、自动配置、依赖整合、内嵌容器和工程化体验统一起来。

## 1. Spring Boot 是什么 / Spring Boot とは何か

- 中文：Spring Boot 是一个用于快速构建 Java 应用的框架，核心是自动配置、约定优于配置和独立运行。
- 日本語：Spring Boot は Java アプリを素早く構築するためのフレームワークで、主な特徴は自動設定、設定より規約、単独起動です。

### 你可以先记住这三句话 / まず覚える3点

- 中文：它负责“把项目跑起来”。
- 日本語：プロジェクトを「起動できる形」にする。
- 中文：它负责“把常见配置自动接好”。
- 日本語：よく使う設定を自動でつなぐ。
- 中文：它负责“把 Web、数据库、事务、日志等能力整合起来”。
- 日本語：Web、DB、トランザクション、ログなどをまとめて整合する。

## 2. Spring Boot 的核心知识点 / Spring Boot の核心ポイント

| 中文概念 | 日本語概念 | 说明 |
|---|---|---|
| 自动配置 | 自動設定 | 根据依赖自动配置常用组件 |
| 约定优于配置 | 規約優先 | 默认结构和默认行为更重要 |
| Starter | スターター | 一组常用依赖的集合 |
| 内嵌容器 | 組み込みコンテナ | 例如内嵌 Tomcat |
| Actuator | Actuator | 健康检查、指标、监控端点 |
| Profiles | プロファイル | 区分开发、测试、生产环境 |

## 3. 常见注解 / よく使うアノテーション

| 中文注解 | 日本語 | 作用 |
|---|---|---|
| `@SpringBootApplication` | 起動アノテーション | 启动 Spring Boot 应用 |
| `@RestController` | REST コントローラ | 返回 JSON 或接口结果 |
| `@Controller` | コントローラ | 返回页面或视图 |
| `@Service` | サービス | 放业务逻辑 |
| `@Repository` | リポジトリ | 放数据访问逻辑 |
| `@Configuration` | 設定クラス | 放配置类 |
| `@Component` | コンポーネント | 通用组件 |
| `@Autowired` | 自動注入 | 自动注入依赖 |
| `@Value` | 値注入 | 注入配置值 |
| `@Transactional` | トランザクション | 控制事务边界 |

## 4. 典型项目结构 / 典型的なプロジェクト構成

```text
src/
|-- main/
|   |-- java/
|   |   `-- com/example/demo/
|   |       |-- DemoApplication.java
|   |       |-- controller/
|   |       |-- service/
|   |       |-- repository/
|   |       |-- dao/
|   |       |-- entity/
|   |       `-- config/
|   `-- resources/
|       |-- application.properties
|       |-- application.yml
|       |-- static/
|       `-- templates/
`-- test/
    `-- java/
```

### 每层大概做什么 / 各層の役割

- 中文：controller 负责接请求。
- 日本語：controller はリクエスト受付。
- 中文：service 负责业务流程。
- 日本語：service は業務ロジック。
- 中文：repository/dao 负责数据库访问。
- 日本語：repository/dao は DB アクセス。
- 中文：entity/model 负责数据对象。
- 日本語：entity/model はデータオブジェクト。
- 中文：config 负责配置与集成。
- 日本語：config は設定と統合。

## 5. 典型处理流程 / 典型フロー

1. 浏览器或前端发起 HTTP 请求。
2. Spring Boot 启动内嵌容器并接收请求。
3. Controller 解析参数并调用 Service。
4. Service 组织业务规则并调用 DAO/Repository。
5. DAO/Repository 访问数据库。
6. 返回 JSON、页面或重定向结果。

日本語：
1. ブラウザまたはフロントエンドが HTTP リクエストを送る。
2. Spring Boot が組み込みコンテナを起動してリクエストを受ける。
3. Controller がパラメータを解釈し Service を呼ぶ。
4. Service が業務ルールをまとめ DAO/Repository を呼ぶ。
5. DAO/Repository が DB にアクセスする。
6. JSON、ページ、リダイレクトを返す。

## 6. 和哪些框架结合最好 / 相性の良いフレームワーク

| 组合 | 中文说明 | 日本語説明 | 适合做什么 |
|---|---|---|---|
| Spring Boot + Spring MVC | 标准 Web 后端组合 | 標準的な Web バックエンド構成 | 页面、表单、接口 |
| Spring Boot + MyBatis | SQL 可控、适合传统项目 | SQL を直接管理しやすい | 复杂查询、对日项目 |
| Spring Boot + Hibernate / JPA | ORM 自动映射 | ORM による自動マッピング | CRUD、实体映射 |
| Spring Boot + Thymeleaf | 服务端模板渲染 | サーバーサイドテンプレート | 传统 Web 页面 |
| Spring Boot + JSP | 老项目兼容 | レガシー互換 | 既有 JSP 项目维护 |
| Spring Boot + React | 前后端分离 | フロント分離構成 | 管理后台、SPA |
| Spring Boot + Vue | 前后端分离 | フロント分離構成 | 后台系统、表单页面 |
| Spring Boot + Next.js / TypeScript | 前后端分离 + 类型安全 + SSR | フロント分離 + 型安全 + SSR | 中后台、门户站点、内容展示 |
| Spring Boot + Angular | 企业级前端 | エンタープライズ向けフロント | 大型业务系统 |

## 7. 和哪些技术结合运用比较好 / 相性の良い技術

| 技术 | 中文说明 | 日本語説明 | 典型用途 |
|---|---|---|---|
| MySQL / PostgreSQL | 关系型数据库 | リレーショナル DB | 业务数据存储 |
| Redis | 缓存和会话 | キャッシュとセッション | 热点数据、验证码 |
| RabbitMQ | 消息队列 | メッセージキュー | 异步处理、削峰 |
| Kafka | 事件流 | イベントストリーム | 日志、流处理 |
| Spring Security | 安全认证授权 | 認証認可 | 登录、权限控制 |
| JWT / OAuth2 | 认证协议 | 認証プロトコル | 前后端分离登录 |
| TypeScript | 类型化前端语言 | 型付きフロント言語 | 前端类型安全 |
| Docker | 容器化部署 | コンテナ化 | 本地开发、上线部署 |
| Nginx | 反向代理 | リバースプロキシ | 静态资源、转发 |
| AWS ECS / Fargate | 容器运行平台 | コンテナ実行基盤 | 云上部署 |
| AWS RDS | 托管数据库 | マネージド DB | 生产数据库 |
| LocalStack | 本地 AWS 模拟 | ローカル AWS 模擬 | 本地联调 |

## 8. 常见应用场景 / よくある利用シーン

### 场景1：Spring Boot + React

- 中文：后端提供 REST API，React 负责页面和交互，适合管理后台和 SPA。
- 日本語：バックエンドが REST API を提供し、React が画面と操作を担当します。管理画面や SPA に向いています。

### 场景2：Spring Boot + Vue

- 中文：结构和 React 类似，适合中小型前后端分离项目。
- 日本語：React と似た構成で、中小規模のフロント分離案件に向いています。

### 场景3：Spring Boot + Next.js + TypeScript

- 中文：适合需要 SSR / SSG、SEO 和强类型前端开发的现代 Web 项目。
- 日本語：SSR / SSG、SEO、型安全なフロント開発が必要なモダン Web 案件に向いています。

### 场景4：Spring Boot + MyBatis

- 中文：适合日本企业常见的数据库驱动型业务，SQL 可控，便于按设计书实现。
- 日本語：日本企業で多い DB 主導の業務に向き、SQL を細かく制御しやすいです。

### 场景5：Spring Boot + JPA / Hibernate

- 中文：适合 CRUD 比较多、实体建模清晰的系统。
- 日本語：CRUD が多く、エンティティ設計が明確なシステムに向いています。

### 场景6：Spring Boot + Redis + MySQL

- 中文：适合高频读取、会话管理、缓存优化。
- 日本語：高頻度参照、セッション管理、キャッシュ最適化に向いています。

### 场景7：Spring Boot + RabbitMQ / Kafka

- 中文：适合异步通知、订单处理、日志流转、事件驱动架构。
- 日本語：非同期通知、注文処理、ログ連携、イベント駆動アーキテクチャに向いています。

### 场景8：Spring Boot + Docker + ECS/Fargate

- 中文：适合现代云上部署和容器化交付。
- 日本語：現代的なクラウドデプロイとコンテナ配布に向いています。

## 9. 学习路线建议 / 学習順のおすすめ

1. 先理解 Spring Boot 的启动、自动配置和项目结构。
2. 再理解 Controller、Service、Repository/DAO 的分层。
3. 然后把 Spring Boot 和 MyBatis 或 JPA 结合起来练 CRUD。
4. 接着再结合 React、Vue 或 Next.js / TypeScript 做前后端分离。
5. 最后补上 Redis、消息队列、安全认证和容器部署。

## 10. 初学者容易混淆的点 / 初学者が混同しやすい点

- 中文：Spring Boot 不是数据库框架。
- 日本語：Spring Boot は DB フレームワークではありません。
- 中文：Spring Boot 不是前端框架。
- 日本語：Spring Boot はフロントエンドフレームワークではありません。
- 中文：TypeScript 不是框架，而是前端开发里常用的类型语言。
- 日本語：TypeScript はフレームワークではなく、フロント開発でよく使う型付き言語です。
- 中文：Spring Boot 负责项目启动和整合，不等于业务逻辑本身。
- 日本語：Spring Boot は起動と統合を担い、業務ロジックそのものではありません。
- 中文：React / Vue 负责前端页面展示，不负责后端事务。
- 日本語：React / Vue は画面表示を担当し、バックエンドのトランザクションは扱いません。

## 11. 一句话总结 / 一言まとめ

- 中文：Spring Boot 是现代 Java 企业开发的整合器，最适合和前后端分离、数据库、缓存、消息队列、容器部署一起学习。
- 日本語：Spring Boot は現代 Java 企業開発の統合基盤であり、フロント分離、DB、キャッシュ、メッセージキュー、コンテナ配備と一緒に学ぶのが最適です。

## 12. 继续细分的专题页 / さらに分けるとよい专题

- [Spring Boot 专区主页](./README.md)

中文：如果你已经理解了 Spring Boot 的基础，就可以进入专用目录继续按专题展开。

日本語：Spring Boot の基礎を理解したら、専用ディレクトリで各テーマを順番に掘り下げると整理しやすいです。

### 专题入口 / テーマ入口

- [Spring Boot 与 React 实战](./02-SpringBoot与React实战.md)
- [Spring Boot 与 MyBatis 实战](./03-SpringBoot与MyBatis实战.md)
- [Spring Boot 与 JPA / Hibernate 对比](./04-SpringBoot与JPA_Hibernate对比.md)
- [Spring Boot 部署运维专题](./05-SpringBoot部署运维专题.md)
- [Spring Boot 与 Next.js / TypeScript 实战](./06-SpringBoot与Nextjs_TypeScript实战.md)
- [Spring Boot 与 Next.js 项目结构图 / 流程图](./07-SpringBoot与Nextjs项目结构图流程图.md)
