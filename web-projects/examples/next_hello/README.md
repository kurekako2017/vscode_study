# Next.js Hello

这是一个更完整的 Next.js 示例，包含页面、全局样式与基本配置文件。

## 运行方式

```bash
npm install
npm run dev
```

## 可用脚本

- `npm run dev`：启动开发服务器
- `npm run build`：构建生产产物
- `npm run start`：启动生产服务器

## 学习重点

- `pages/index.js`：页面入口
- `pages/_app.js`：全局样式和应用包装
- `styles/globals.css`：全局样式
- `next.config.js`：Next.js 配置

### 快速启动（完整步骤）

1. 确保已安装 Node.js（推荐 Node 16+）。
2. 在项目根目录安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

4. 在浏览器中打开默认地址（Next.js 默认为）：

```
http://localhost:3000
```

5. 构建并在生产模式下运行：

```bash
npm run build
npm run start
```

常见问题：
- 若需要固定端口，可在启动时设置 `PORT` 环境变量，例如 `PORT=4000 npm run dev`（Windows PowerShell 可能需使用 `$env:PORT=4000; npm run dev`）。
- 遇到模块或构建错误，先确认 Node 版本并清理 `node_modules` 后重装。
