# React + Node（Express）全栈入门示例

本项目为前后端分离的全栈入门模板，包含：
- 前端：React（Vite 构建，端口 5173）
- 后端：Express API（端口 4000）

---

## 目录结构

```
react-node-demo/
  client/    # React 前端
  server/    # Express 后端
```

---

## 快速开始

### 1. 启动后端
```bash
cd server
npm install
npm start
```
访问：http://localhost:4000/api/hello

### 2. 启动前端
```bash
cd client
npm install
npm run dev
```
访问：http://localhost:5173

---

## 前端代码要点
- `client/src/App.jsx`：页面加载时自动请求 `/api/hello`，显示后端返回内容。
- `client/package.json`：已配置 Vite、React。

## 后端代码要点
- `server/index.js`：提供 `/api/hello` 路由，返回 JSON。
- `server/package.json`：已配置 Express。

---

## 学习路线建议

1. **Node.js & npm 基础**
2. **Express 基础**：路由、req/res、JSON 返回
3. **React 基础**：JSX、组件、状态、生命周期
4. **前后端联调**：fetch 请求、CORS 处理
5. **进阶练习**：
   - 增加更多 API 路由
   - 前端页面美化
   - 尝试部署到 Vercel/Render

---

## 常见问题
- 端口冲突：确保 4000/5173 端口未被占用
- 跨域问题：如遇 CORS，可在 Express 端加 `cors` 中间件

---

Happy Coding!
