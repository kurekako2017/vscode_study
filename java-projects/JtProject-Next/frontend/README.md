# JtProject-Next Frontend

这个目录是 `JtProject-Next` 的 Next.js + TypeScript 前端。

## 学习入口

- `app/layout.tsx`：根布局、全局 CSS、页面 metadata
- `app/page.tsx`：首页路由、Client Component、React state、表单、事件、API 调用
- `lib/api.ts`：统一 `fetch` 请求封装
- `lib/types.ts`：接口返回和页面状态的 TypeScript 类型

## 启动

```bash
npm install
npm run dev
```

访问：

```text
http://localhost:3000
```

## 构建检查

```bash
npm run build
```

`next build` 会同时检查 Next.js 页面构建和 TypeScript 类型。

## 前后端流程图

见项目文档：

[../doc/reference/nextjs-typescript-flow.md](../doc/reference/nextjs-typescript-flow.md)
