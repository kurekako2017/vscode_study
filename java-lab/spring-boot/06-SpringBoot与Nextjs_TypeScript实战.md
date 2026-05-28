# Spring Boot 与 Next.js / TypeScript 实战

Spring Boot + Next.js + TypeScript 是很适合现代前后端分离项目的组合。Spring Boot 负责后端业务、认证和数据，Next.js 负责页面、路由和渲染，TypeScript 负责前端类型安全。

## 1. 这个组合是什么 / この組み合わせは何か

- 中文：Spring Boot 提供后端 REST API，Next.js 负责前端页面和 SSR / SSG，TypeScript 负责前端开发的类型约束。
- 日本語：Spring Boot がバックエンド REST API を提供し、Next.js が画面と SSR / SSG を担当し、TypeScript がフロントエンドの型安全を担います。

## 2. 核心知识点 / 核心ポイント

| 中文概念 | 日本語概念 | 说明 |
|---|---|---|
| REST API | REST API | 前后端通信接口 |
| TypeScript | TypeScript | JavaScript 的类型化版本 |
| Next.js Routing | Next.js ルーティング | 文件路由和页面组织 |
| SSR | SSR | 服务端渲染 |
| SSG | SSG | 静态生成 |
| CSR | CSR | 客户端渲染 |
| DTO | DTO | 接口传输对象 |
| Hydration | ハイドレーション | 前端接管服务端 HTML |

## 3. 典型开发链路 / 典型的な開発フロー

1. 后端先定义 API、DTO 和权限规则。
2. 前端用 Next.js 构建页面和路由。
3. TypeScript 为页面状态、接口返回值和组件 props 提供类型约束。
4. Next.js 通过 fetch / axios 调用 Spring Boot 接口。
5. Spring Boot 返回 JSON，Next.js 渲染页面。

日本語：
1. 先にバックエンドが API、DTO、権限制御を定義する。
2. フロントエンドが Next.js で画面とルーティングを作る。
3. TypeScript で状態、レスポンス、props に型を付ける。
4. Next.js が fetch / axios で Spring Boot API を呼ぶ。
5. Spring Boot が JSON を返し、Next.js が画面を描画する。

## 4. 适合做什么 / どんな場面に向くか

- 中文：需要 SEO、首屏性能、路由组织清晰的前后端分离项目。
- 日本語：SEO、初期表示速度、ルーティング整理を重視するフロント分離案件。
- 中文：中后台系统、门户网站、营销页面、内容展示类站点。
- 日本語：中台システム、ポータル、マーケティングページ、コンテンツ系サイト。

## 5. 开发重点 / 開発ポイント

- 中文：接口契约要稳定，前后端字段命名和错误码要统一。
- 日本語：API 契約を安定させ、前後端でフィールド名とエラーコードを統一する。
- 中文：TypeScript 类型定义要尽量跟后端 DTO 对齐。
- 日本語：TypeScript の型定義はバックエンド DTO にできるだけ合わせる。
- 中文：如果使用 SSR / SSG，要提前考虑鉴权和缓存策略。
- 日本語：SSR / SSG を使う場合は、認証とキャッシュ方針を先に考える。

## 6. 常见技术组合 / よくある技術組み合わせ

- 中文：Spring Boot + Next.js + TypeScript + MySQL
- 日本語：Spring Boot + Next.js + TypeScript + MySQL
- 中文：Spring Boot + Next.js + TypeScript + Spring Security + JWT
- 日本語：Spring Boot + Next.js + TypeScript + Spring Security + JWT
- 中文：Spring Boot + Next.js + TypeScript + Redis
- 日本語：Spring Boot + Next.js + TypeScript + Redis
- 中文：Spring Boot + Next.js + TypeScript + Docker + Nginx
- 日本語：Spring Boot + Next.js + TypeScript + Docker + Nginx

## 7. 常见坑 / よくある落とし穴

- 中文：把 Next.js 当成纯静态站点工具，忽略了服务端渲染和路由能力。
- 日本語：Next.js を単なる静的サイト生成ツールとして扱い、SSR やルーティング機能を見落とす。
- 中文：前端没有类型约束，接口字段一变就大面积报错。
- 日本語：フロントに型制約がなく、API フィールド変更で大きく壊れる。
- 中文：后端和前端各自定义一套数据模型，导致长期维护困难。
- 日本語：前後端が別々のデータモデルを持ち、長期保守が難しくなる。

## 8. 一句话总结 / 一言まとめ

- 中文：Spring Boot + Next.js + TypeScript 适合做现代化、可扩展、类型安全的前后端分离系统。
- 日本語：Spring Boot + Next.js + TypeScript は、現代的で拡張しやすく、型安全なフロント分離システムに向いています。

## 9. 下一步 / 次のステップ

- [Spring Boot 与 Next.js 项目结构图 / 流程图](./07-SpringBoot与Nextjs项目结构图流程图.md)
- [Spring Boot 与 Next.js 前端目录结构 / 组件拆分图](./08-SpringBoot与Nextjs前端目录结构组件拆分图.md)

中文：如果你已经知道这组技术怎么配合，下一步就看目录结构和请求流转。

日本語：この組み合わせの役割が分かったら、次はディレクトリ構成とリクエストの流れを見ると理解しやすいです。
