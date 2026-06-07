# React Chat UI Demo

这个 demo 是一个最小的 Agent / RAG 前端壳子，重点不是对接真实后端，而是先把页面结构搭起来。

## 你会学到什么

- 聊天输入框怎么组织
- 消息列表怎么渲染
- 引用来源怎么展示
- 如何把“用户消息 / 系统回复 / sources”分层显示

## 运行方式

```bash
npm install
npm run dev
```

默认会在 `http://localhost:5173` 打开。

## 目录结构

```text
chat_ui_demo/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── src/
    ├── App.tsx
    ├── main.tsx
    └── styles.css
```

## 设计说明

- 这里使用假数据，先把 UI 和交互跑通
- 后面接真实 API 时，只需要把 `sendMessage()` 替换成后端请求即可
- 这个 demo 适合和 `agent-advanced/projects/internal_hybrid_rag_demo` 配合学习
