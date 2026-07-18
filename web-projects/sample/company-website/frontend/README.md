# Company Website Frontend

本目录包含公司网站前端（Next.js + Tailwind CSS）。此文档说明本地开发、构建与常见问题排查步骤。

## 要求
- Node >= 18
- npm（随 Node 一起安装）

## 本地开发（推荐）
1. 进入项目目录并确认路径：

```bash
cd ~/workspace/vscode_study/web-projects/sample/company-website/frontend
pwd
```

2. 按锁文件重新安装依赖：

```bash
npm ci
```

3. 启动开发服务器：

```bash
npm run dev
# 打开 http://localhost:3000
```

停止服务器：在终端按 `Ctrl+C`。

## 构建与启动（生产）

```bash
npm run build
npm run start
```

## 常见问题
- 错误：端口被占用 → 使用 `netstat` 或任务管理器查找并释放 3000 端口，或设置环境变量 `PORT`。
- 错误：`next: Permission denied` 或依赖目录权限异常 → 保留 `package-lock.json`，重新生成依赖：

```bash
npm ci
```

## 代理与镜像（在国内网络）
- 使用 npm 镜像：

```bash
npm config set registry https://registry.npmmirror.com
```

## 调试与日志
- 日志输出会在终端显示；若需要更详细的安装日志，可使用 `npm ci --loglevel=info`。

## 其他说明
- 该前端示例与后端、数据库等分离；可在 `frontend` 下开发并指向本地或远端 API。

