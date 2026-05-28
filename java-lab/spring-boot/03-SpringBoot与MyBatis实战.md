# Spring Boot 与 MyBatis 实战

Spring Boot + MyBatis 是日本企业项目里非常常见的组合，特点是 SQL 可控、结构清晰、适合按设计书实现业务。

## 1. 这个组合是什么 / この組み合わせは何か

- 中文：Spring Boot 负责应用框架和接口层，MyBatis 负责 SQL 映射和数据库访问。
- 日本語：Spring Boot がアプリ基盤と API 層を担当し、MyBatis が SQL マッピングと DB アクセスを担当します。

## 2. 核心知识点 / 核心ポイント

| 中文概念 | 日本語概念 | 说明 |
|---|---|---|
| Mapper | Mapper | SQL 接口定义 |
| XML SQL | XML SQL | 传统 MyBatis 映射方式 |
| Annotation Mapper | アノテーション Mapper | 注解式 SQL |
| Parameter | パラメータ | SQL 入参 |
| ResultMap | ResultMap | 结果映射 |
| Dynamic SQL | 動的 SQL | 条件拼接 |
| PageHelper | ページング | 分页插件 |
| Transaction | トランザクション | 事务控制 |

## 3. 典型开发链路 / 典型的な開発フロー

1. Controller 接收请求。
2. Service 进行业务判断。
3. Mapper 调用 SQL。
4. MyBatis 执行查询或更新。
5. 数据返回后由 Service 组装结果。

日本語：
1. Controller がリクエストを受ける。
2. Service が業務判断を行う。
3. Mapper が SQL を呼ぶ。
4. MyBatis が検索・更新を実行する。
5. 結果を Service が整形して返す。

## 4. 适合做什么 / どんな場面に向くか

- 中文：用户管理、订单管理、权限管理、报表查询等典型业务系统。
- 日本語：ユーザー管理、受注管理、権限管理、帳票検索などの業務システム。
- 中文：SQL 需要可读、可控、可审查的项目。
- 日本語：SQL を明確に管理し、レビューしやすくしたい案件。

## 5. 开发重点 / 開発ポイント

- 中文：SQL 要和设计书、索引、性能要求一起考虑。
- 日本語：SQL は設計書、インデックス、性能要件と合わせて考える。
- 中文：Mapper 接口命名要稳定，避免随意改动。
- 日本語：Mapper の命名は安定させ、むやみに変更しない。
- 中文：动态 SQL 要保持可读性，不要过度复杂。
- 日本語：動的 SQL は可読性を保ち、複雑にしすぎない。

## 6. 常见技术组合 / よくある技術組み合わせ

- 中文：Spring Boot + MyBatis + MySQL
- 日本語：Spring Boot + MyBatis + MySQL
- 中文：Spring Boot + MyBatis + PageHelper
- 日本語：Spring Boot + MyBatis + PageHelper
- 中文：Spring Boot + MyBatis + Redis
- 日本語：Spring Boot + MyBatis + Redis
- 中文：Spring Boot + MyBatis + Lombok
- 日本語：Spring Boot + MyBatis + Lombok

## 7. 常见坑 / よくある落とし穴

- 中文：把 SQL 写得太复杂，后期难维护。
- 日本語：SQL が複雑すぎて保守しづらい。
- 中文：ResultMap 和字段名不一致，导致映射错误。
- 日本語：ResultMap とカラム名が一致せず、マッピングが壊れる。
- 中文：事务边界不清晰，更新逻辑容易出问题。
- 日本語：トランザクション境界が曖昧で更新処理に問題が出る。

## 8. 一句话总结 / 一言まとめ

- 中文：Spring Boot + MyBatis 适合重视 SQL 可控性、可维护性和对日项目落地的业务系统。
- 日本語：Spring Boot + MyBatis は、SQL の制御性、保守性、日本案件での実装しやすさを重視する業務システムに向いています。
