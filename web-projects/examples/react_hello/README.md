# React Hello

这是一个完整但极简的 React + Vite 示例，包含入口文件、组件、样式和项目配置。

## 运行方式

```bash
npm install
npm run dev
```

## 可用脚本

- `npm run dev`：启动开发服务器
- `npm run build`：构建生产产物
- `npm run preview`：预览构建结果

## 学习重点

- `src/main.jsx`：应用入口与挂载逻辑
- `src/App.jsx`：根组件
- `src/style.css`：基础样式
- `vite.config.js`：Vite 配置

### 快速启动（完整步骤）

1. 确保已安装 Node.js（推荐 Node 16+ 或更高）。
2. 在项目根目录安装依赖：

```bash
npm install
```

3. 启动开发服务器（带热重载）：

```bash
npm run dev
```

4. 在浏览器中打开默认地址（Vite 默认为）：

```
http://localhost:5173
```

5. 构建并预览生产包（可选）：

```bash
npm run build
npm run preview
```

常见问题：
- 若端口被占用，可设置环境变量 `PORT` 或按提示选择其它端口。
- 遇到依赖或构建错误，先确认 Node 版本并删除 `node_modules` 后重试 `npm install`。
