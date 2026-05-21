# scripts 目录说明

本目录按用途拆分为 4 个子目录，便于快速定位：

- `wsl/`：WSL 与 Git Bash 开发入口
- `docker/`：Docker Desktop 安装与指南
- `localstack/`：LocalStack 运行、验证、诊断
- `deploy/`：JtProject 服务器初始化与 sudoers 模板

## 快速入口

- 启动 WSL 开发环境：`scripts\wsl\start-wsl-vscode-dev.bat`
- 验证 LocalStack：`powershell -ExecutionPolicy Bypass -File .\scripts\localstack\verify-localstack.ps1`
- 查看 LocalStack 日志：`scripts\localstack\show-localstack-logs.bat`

## WSL 脚本

| 文件 | 作用 | 典型用法 |
|---|---|---|
| `scripts/wsl/start-wsl-vscode-dev.bat` | 一键打开 Ubuntu + 仓库 + VS Code（支持 `mnt/local` 模式） | `scripts\wsl\start-wsl-vscode-dev.bat local` |
| `scripts/wsl/sync-from-wsl.bat` | 从 WSL 主目录同步最新内容到 Windows D 盘 | `scripts\wsl\sync-from-wsl.bat` |
| `scripts/wsl/sync-from-wsl.ps1` | 同步脚本主体，支持 `-NoMirror` 等参数 | `powershell -ExecutionPolicy Bypass -File .\scripts\wsl\sync-from-wsl.ps1` |
| `scripts/wsl/init-wsl-local-repo.sh` | 把当前仓库复制到 WSL 本地工作区 `~/workspace/vscode_study` | `bash ./scripts/wsl/init-wsl-local-repo.sh` |
| `scripts/wsl/dev-check-gitbash.sh` | Git Bash 开发环境一键检查（Git/Java/Python/LLM 变量） | `bash ./scripts/wsl/dev-check-gitbash.sh` |
| `scripts/wsl/gitbash_aliases.sh` | Git Bash 常用别名和函数（`gs`、`venvon`、`devcheck`） | `source /d/dev/source_code/vscode_study/scripts/wsl/gitbash_aliases.sh` |

## WSL 同步建议

1. 以 `scripts/wsl/sync-from-wsl.bat` 作为 Windows 双击入口。
2. 默认使用镜像模式，把 WSL 的 `/home/victorkure/workspace/vscode_study` 同步到 `D:\dev\source_code\vscode_study`。
3. 若想保留 Windows 端多余文件，改用 `sync-from-wsl.ps1 -NoMirror`。

## Docker 脚本与文档

| 文件 | 作用 | 典型用法 |
|---|---|---|
| `scripts/docker/install-docker-quick.ps1` | 快速下载并启动 Docker Desktop 安装 | `powershell -ExecutionPolicy Bypass -File .\scripts\docker\install-docker-quick.ps1` |
| `scripts/docker/install-docker-desktop.ps1` | 完整 Docker Desktop 安装流程（包含更多检查） | `powershell -ExecutionPolicy Bypass -File .\scripts\docker\install-docker-desktop.ps1` |
| `scripts/docker/DOCKER_INSTALL_GUIDE.md` | Docker 安装说明文档 | 打开文档阅读 |

## LocalStack 脚本

| 文件 | 作用 | 典型用法 |
|---|---|---|
| `scripts/localstack/check-localstack.bat` | 快速检查 Docker/LocalStack，必要时启动容器并测健康接口 | `scripts\localstack\check-localstack.bat` |
| `scripts/localstack/show-localstack-logs.bat` | 确认 LocalStack 运行并输出最近日志 | `scripts\localstack\show-localstack-logs.bat` |
| `scripts/localstack/verify-localstack.ps1` | 深度验证 LocalStack 状态、健康、API 和日志 | `powershell -ExecutionPolicy Bypass -File .\scripts\localstack\verify-localstack.ps1` |
| `scripts/localstack/monitor-status.ps1` | 持续监控 Docker 与 LocalStack 状态（5 秒刷新） | `powershell -ExecutionPolicy Bypass -File .\scripts\localstack\monitor-status.ps1` |
| `scripts/localstack/diagnostic.ps1` | 系统诊断（Docker、WSL、端口、容器） | `powershell -ExecutionPolicy Bypass -File .\scripts\localstack\diagnostic.ps1` |
| `scripts/localstack/wait-for-docker-and-run.ps1` | 等待 Docker 就绪后运行 LocalStack Java 示例流程 | `powershell -ExecutionPolicy Bypass -File .\scripts\localstack\wait-for-docker-and-run.ps1` |

## 建议使用顺序（LocalStack 场景）

1. `scripts/docker/install-docker-quick.ps1` 或 `scripts/docker/install-docker-desktop.ps1`
2. `scripts/localstack/diagnostic.ps1`
3. `scripts/localstack/verify-localstack.ps1`
4. `scripts/localstack/show-localstack-logs.bat`

## Deploy 脚本

| 文件 | 作用 | 典型用法 |
|---|---|---|
| `scripts/deploy/init-jtproject-server.sh` | 初始化服务器部署环境（目录、systemd、nginx、sudoers） | `sudo bash scripts/deploy/init-jtproject-server.sh --deploy-user <user> --domain <domain>` |
| `scripts/deploy/jtproject-sudoers.example` | 部署账号最小 sudo 白名单模板 | `sudo visudo -cf /tmp/jtproject-sudoers` |

## 说明

- 每个保留脚本文件头都已补充中文 `说明` 和 `用法` 注释。
- 若后续新增脚本，请按目录职责放置，并同步更新此 README。
