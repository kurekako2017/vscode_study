/**
 * server/index.js
 * 简单的 Express 后端示例（教学注释）
 * 说明：
 * - 提供了一个最小 API：GET /api/hello 返回 JSON。
 * - 默认端口由环境变量 `PORT` 控制（开发时默认 4000）。
 * - 若希望后端同时提供前端打包文件（生产部署），可以取消注释底部的静态托管代码。
 * 本地运行：
 *   cd web-projects/sample/react-node-template/server
 *   npm install
 *   npm run dev
 */

const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());

// 简单 API：返回 JSON，用于演示前端如何请求后端
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Express API' });
});

// 如果你想要用后端提供前端打包文件（例如生产部署），取消下面注释：
// const clientBuildPath = path.join(__dirname, '..', 'client', 'dist');
// app.use(express.static(clientBuildPath));
// app.get('*', (req, res) => res.sendFile(path.join(clientBuildPath, 'index.html')));

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
