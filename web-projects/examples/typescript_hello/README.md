# TypeScript Hello

这是一个 Vanilla TypeScript + Vite 最小示例，用来学习 TypeScript 如何通过 Vite 转换为浏览器可运行的 JavaScript。

## 运行方式

```bash
npm install
npm run dev
```

默认打开：

```text
http://localhost:5173
```

## 可用脚本

- `npm run dev`：启动开发服务器
- `npm run build`：先运行 TypeScript 类型检查，再构建生产产物
- `npm run preview`：预览构建产物

## 学习重点

- `index.html`：提供页面根节点 `#app`
- `src/main.ts`：定义类型、创建数据、渲染 DOM
- `src/style.css`：控制页面外观
- `tsconfig.json`：控制 TypeScript 类型检查规则
- `package.json`：定义 Vite 与 TypeScript 脚本

更详细的流程图见 [LEARN.md](LEARN.md)。
