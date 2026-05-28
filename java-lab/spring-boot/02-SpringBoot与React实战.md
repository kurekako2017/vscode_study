# Spring Boot 与 React 实战

Spring Boot + React 是最常见的前后端分离组合之一。后端负责业务、权限、接口和数据，前端负责页面、状态和交互。

## 1. 这个组合是什么 / この組み合わせは何か

- 中文：Spring Boot 提供 REST API，React 负责构建单页应用和前端交互。
- 日本語：Spring Boot が REST API を提供し、React が SPA と画面操作を担当します。

## 2. 核心知识点 / 核心ポイント

| 中文概念 | 日本語概念 | 说明 |
|---|---|---|
| REST API | REST API | 前后端通信接口 |
| JSON | JSON | 前后端交换数据格式 |
| CORS | CORS | 跨域访问控制 |
| Axios / fetch | Axios / fetch | 前端请求工具 |
| Router | ルーター | 页面路由 |
| State | 状態 | 页面状态管理 |
| DTO | DTO | 接口传输对象 |
| Pagination | ページネーション | 分页查询 |

## 3. 典型开发链路 / 典型的な開発フロー

1. 后端先定义接口和返回结构。
2. 前端根据接口设计页面与状态。
3. React 通过请求调用 Spring Boot 接口。
4. Spring Boot 在 Controller / Service / DAO 中处理业务。
5. 后端返回 JSON，前端渲染页面。

日本語：
1. 先にバックエンドが API とレスポンス形式を定義する。
2. フロントエンドがその API に合わせて画面と状態を作る。
3. React が Spring Boot の API を呼ぶ。
4. Spring Boot が Controller / Service / DAO で処理する。
5. JSON を返し、React が画面を描画する。

## 4. 适合做什么 / どんな場面に向くか

- 中文：管理后台、用户中心、运营系统、表单较多的中后台项目。
- 日本語：管理画面、ユーザー管理、業務システム、フォーム中心の中台案件。
- 中文：需要前后端职责清晰、接口长期维护的项目。
- 日本語：フロントとバックエンドの責務を分け、API を長期保守したい案件。

## 5. 开发重点 / 開発ポイント

- 中文：后端要把接口设计清楚，字段命名和错误码要稳定。
- 日本語：バックエンドは API 設計、フィールド名、エラーコードを安定させる必要がある。
- 中文：前端要管理加载状态、空状态、分页、表单校验。
- 日本語：フロントはローディング、空状態、ページング、入力チェックを管理する。
- 中文：跨域、登录态、刷新 token 和权限控制要提前设计。
- 日本語：CORS、ログイン状態、トークン更新、権限制御を先に設計する。

## 6. 常见技术组合 / よくある技術組み合わせ

- 中文：Spring Boot + React + MySQL + Redis
- 日本語：Spring Boot + React + MySQL + Redis
- 中文：Spring Boot + React + Spring Security + JWT
- 日本語：Spring Boot + React + Spring Security + JWT
- 中文：Spring Boot + React + Docker + Nginx
- 日本語：Spring Boot + React + Docker + Nginx

## 7. 常见坑 / よくある落とし穴

- 中文：接口字段经常变化，前端和后端无法对齐。
- 日本語：API フィールドが頻繁に変わり、フロントとバックエンドがずれる。
- 中文：前端直接拼业务逻辑，导致状态混乱。
- 日本語：フロントに業務ロジックを詰め込みすぎて状態が混乱する。
- 中文：后端没有统一错误处理，前端难以展示提示。
- 日本語：バックエンドのエラー処理が統一されておらず、フロントで表示しにくい。

## 8. 一句话总结 / 一言まとめ

- 中文：Spring Boot + React 适合做职责清晰、接口明确、可扩展性强的现代 Web 系统。
- 日本語：Spring Boot + React は、責務が明確で API がはっきりした拡張しやすい Web システムに向いています。
