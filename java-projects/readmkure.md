TypeScript 是语言 → Node.js 是运行环境 → Express/NestJS 是后端框架。

                 JtProject-TypeScript
                      │
             语言：TypeScript
                      │
          ┌───────────┴───────────┐
          │                       │
        前端                     后端
          │                       │
        React                   Node.js
          │                       │
        Vite              ┌───────┴───────┐
                          │               │
                       Express          NestJS
                       基础对照          ★重点

| 项目                            | 核心目的                                  |
| ------------------------------- | ----------------------------------------- |
| JtProject                       | Spring Boot + JSP                         |
| JtProject-Thymeleaf             | Spring Boot + Thymeleaf                   |
| JtProject-React                 | Spring Boot + React + TS                  |
| JtProject-Vue                   | Spring Boot + Vue + TS                    |
| JtProject-Next                  | Spring Boot + Next.js + TS                |
| JtProject-SpringBoot-TypeScript | Spring Boot + 原生 TS                     |
| JtProject-TypeScript            | **Node + Express + React + TS**     |
| **JtProject-NestJS**      | **Node + NestJS + Next/React + TS** |

JtProject-NestJS = Next.js + React + TypeScript + Node.js + NestJS

`TypeScript + React + Next.js + Node.js + NestJS 就全部覆盖，而且不会为了框架再无限增加项目。`

| 功能         | Express           | NestJS     | Spring Boot             |
| ------------ | ----------------- | ---------- | ----------------------- |
| HTTP入口     | Router            | Controller | Controller              |
| GET          | `router.get()`  | `@Get()` | `@GetMapping`         |
| 业务层       | 自己组织          | Service    | Service                 |
| DI           | 自己处理          | 内置DI     | Spring DI               |
| 模块         | 自己组织          | Module     | Configuration/Component |
| DTO          | TS interface/type | DTO class  | Java DTO                |
| 企业项目结构 | 自己规定          | 框架规定   | 框架规定                |

| 技术                 | 到底是什么                           |
| -------------------- | ------------------------------------ |
| JavaScript           | 编程语言                             |
| **TypeScript** | JavaScript 的类型化扩展/语言         |
| **React**      | 前端 UI Library                      |
| **Next.js**    | 基于 React 的应用框架                |
| **Node.js**    | JavaScript/TypeScript 服务端运行环境 |
| **Express**    | Node.js Web 框架                     |
| **NestJS**     | Node.js 企业级后端框架               |
| Vite                 | 前端构建工具                         |

TypeScript + React/Next.js + Node/NestJS  更接近

                  TypeScript
                      │
          ┌───────────┴────────────┐
          │                        │
         前端                     后端
          │                        │
        React                    Node.js
          │                        │
       Next.js                  NestJS
     （需要时使用）          （主要后端框架）
