# JtProject-Next 文档总索引

相关入口：

- 项目根入口：[README.md](../README.md)
- Java 项目总导航：[Java项目总启动导航.md](../../Java项目总启动导航.md)
- Java 项目文档入口：[doc/README.md](../../doc/README.md)

这个项目的文档入口已经调整为 **Next.js + TypeScript 学习版**。原始 JSP / Spring Boot 文档仍保留在子目录里，主要作为业务和后端对照资料。

## 建议先看

如果你主要学习 Next.js + TypeScript，推荐顺序：

1. [README.md](../README.md)
2. [Next.js 框架系统学习指南](./reference/nextjs-framework-guide.md)
3. [Next.js + TypeScript 前后端处理流程图](./reference/nextjs-typescript-flow.md)
4. [frontend/app/layout.tsx](../frontend/app/layout.tsx)
5. [frontend/app/page.tsx](../frontend/app/page.tsx)
6. [frontend/lib/api.ts](../frontend/lib/api.ts)
7. [frontend/lib/types.ts](../frontend/lib/types.ts)

## 1. Next.js + TypeScript

核心学习文件：

- [Next.js 框架系统学习指南](./reference/nextjs-framework-guide.md)
- [Next.js + TypeScript 前后端处理流程图](./reference/nextjs-typescript-flow.md)
- [frontend/app/layout.tsx](../frontend/app/layout.tsx)
- [frontend/app/page.tsx](../frontend/app/page.tsx)
- [frontend/lib/api.ts](../frontend/lib/api.ts)
- [frontend/lib/types.ts](../frontend/lib/types.ts)

这些文件都添加了学习注释，重点说明 App Router、Client Component、TypeScript 泛型、React state、表单事件和 API 调用链路。

## 2. guides

路径：`doc/guides/`

这些文档来自原始项目，保留作启动、排障和后端对照资料：

- [手动启动项目完整指南.md](./guides/手动启动项目完整指南.md)
- [手动启动项目完整指南-IDEA版.md](./guides/手动启动项目完整指南-IDEA版.md)
- [启动失败解决方案.md](./guides/启动失败解决方案.md)
- [REFACTORING_GUIDE.md](./guides/REFACTORING_GUIDE.md)
- [TESTING_GUIDE.md](./guides/TESTING_GUIDE.md)

## 3. reference

路径：`doc/reference/`

Next.js 学习入口：

- [nextjs-typescript-flow.md](./reference/nextjs-typescript-flow.md)
- [nextjs-framework-guide.md](./reference/nextjs-framework-guide.md)

后端和原始项目对照资料：

- [CONTROLLER_注释说明.md](./reference/CONTROLLER_注释说明.md)
- [ENV_CONFIG.md](./reference/ENV_CONFIG.md)
- [JAVADOC_LOGGING_SUMMARY.md](./reference/JAVADOC_LOGGING_SUMMARY.md)
- [数据访问层与调用链学习文档.md](./reference/数据访问层与调用链学习文档.md)
- [userLogin.jsp跳转到UserController的完整流程.md](./reference/userLogin.jsp跳转到UserController的完整流程.md)
- [启动到登录页面的完整流程.md](./reference/启动到登录页面的完整流程.md)
- [测试类已禁用说明.md](./reference/测试类已禁用说明.md)
- [项目框架与内容总结.md](./reference/项目框架与内容总结.md)
- [项目框架与调用流程完整总结.md](./reference/项目框架与调用流程完整总结.md)

## 4. jp-docs

路径：`doc/jp-docs/`

面向日本项目风格的交付文档：

- [README.md](./jp-docs/README.md)
- 設計書、基本設計書、詳細設計書、製造説明書
- 単体テスト仕様書、結合テスト仕様書、総合テスト仕様書
- 障害票、改修票、調査票

## 5. history

路径：`doc/history/`

归档历史性文档，保留过程记录，但不作为主入口。

建议先看合并后的 3 份主文档：

- [01_启动历史总结.md](./history/01_启动历史总结.md)
- [02_问题修复历史总结.md](./history/02_问题修复历史总结.md)
- [03_历史归档索引.md](./history/03_历史归档索引.md)

旧目录说明：

- `startup/`: 启动成功、快速启动、旧启动方案
- `fixes/`: 问题修复、运行按钮、登录 404 等修复记录
- `notes/`: 临时导航、memo

## 使用建议

- 想先把项目跑起来：先看 [README.md](../README.md)
- 想系统理解 Next.js 框架：先看 [nextjs-framework-guide.md](./reference/nextjs-framework-guide.md)
- 想理解 Next.js + TypeScript 前后端流程：先看 [nextjs-typescript-flow.md](./reference/nextjs-typescript-flow.md)
- 想看前端代码：先看 [frontend/app/page.tsx](../frontend/app/page.tsx)
- 想看 TypeScript 类型：先看 [frontend/lib/types.ts](../frontend/lib/types.ts)
- 想看 API 封装：先看 [frontend/lib/api.ts](../frontend/lib/api.ts)
- 想看后端如何接住前端请求：看 `src/main/java/.../controller/ApiController.java`
- 想查看日式项目资料：先看 [doc/jp-docs/README.md](./jp-docs/README.md)
