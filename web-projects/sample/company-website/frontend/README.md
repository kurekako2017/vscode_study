# Company Website Frontend

本目录包含公司网站前端（Next.js + Tailwind CSS）。此文档说明本地开发、构建与常见问题排查步骤。

## 要求
- Node >= 18
- npm（随 Node 一起安装）或可选使用 `pnpm` / `corepack`

## 本地开发（推荐）
1. 进入目录：

```powershell
cd web-projects/sample/company-website/frontend
```

2. 安装依赖：

```powershell
npm install
```

3. 启动开发服务器：

```powershell
npm run dev
# 打开 http://localhost:3000
```

停止服务器：在终端按 `Ctrl+C`。

## 构建与启动（生产）

```powershell
npm run build
npm run start
```

## 使用 pnpm（可选）
如果你更喜欢 `pnpm`：

```powershell
# 安装 pnpm（若未安装）
npm install -g pnpm
# 或使用 corepack（Node 自带）
corepack enable
corepack prepare pnpm@latest --activate

cd web-projects/sample/company-website/frontend
pnpm install
pnpm dev
```

如果看到 "pnpm is not recognized"，说明系统没有安装 pnpm，按上面步骤安装或直接使用 `npm`。

## 常见问题
- 错误：`'pnpm' is not recognized` → 请安装 pnpm 或使用 `npm`。
- 错误：端口被占用 → 使用 `netstat` 或任务管理器查找并释放 3000 端口，或设置环境变量 `PORT`。
- 构建失败（依赖问题）→ 删除 `node_modules` 与 lock 文件后重装：

```powershell
Remove-Item -Recurse -Force node_modules, package-lock.json, pnpm-lock.yaml
npm install
```

## 代理与镜像（在国内网络）
- 使用 npm 镜像：

```powershell
npm config set registry https://registry.npmmirror.com
```

## 调试与日志
- 日志输出会在终端显示；若需要更详细的构建日志，可在安装时使用 `npm install --loglevel=info`。

## 其他说明
- 该前端示例与后端、数据库等分离；可在 `frontend` 下开发并指向本地或远端 API。

欢迎我把这部分文档合并到项目根的 `GETTING_STARTED.md`（若需要我可执行）。
