# Angular Hello

这是一个更完整的 Angular 示例，采用 standalone 组件方式，包含入口文件、全局样式和项目配置。

## 运行方式

```bash
npm install
npm run dev
```

## 可用脚本

- `npm run dev`：启动开发服务器
- `npm run build`：构建生产产物
- `npm run start`：启动开发服务器（与 `dev` 一致）

## 学习重点

- `src/main.ts`：应用启动入口
- `src/app/app.component.ts`：根组件
- `src/app/app.component.html`：组件模板
- `src/app/app.component.css`：组件样式
- `angular.json`：Angular CLI 配置

更详细的处理流程图与分层说明见 [LEARN.md](LEARN.md)。

### 快速启动（完整步骤）

1. 确保已安装 Node.js（推荐 Node 16+）和 `@angular/cli`（可选，本示例的脚本会使用本地安装的 CLI）。
2. 在项目根目录安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

4. 在浏览器中打开默认地址（Angular CLI 默认为）：

```
http://localhost:4200
```

5. 构建并在生产模式下运行（可选）：

```bash
npm run build
npm run start
```

常见问题：
- 若端口占用，可在启动时传入 `--port` 参数或设置 `PORT` 环境变量。
- 如果遇到 TypeScript 配置或编译错误，确认 `tsconfig.json` 与项目一致，并尝试清理缓存（删除 `node_modules` 并重装）。
