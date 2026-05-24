# Docker Desktop + WSL 快速配置

这个清单面向当前 Linux/WSL 环境，用来恢复 `docker` 命令并让依赖 Docker 的项目可跑。

## 1. 在 Windows 安装 Docker Desktop

- 安装 Docker Desktop
- 确认 Windows 侧能正常启动 Docker Desktop

## 2. 打开 WSL integration

在 Docker Desktop 里进入设置：

- `Settings`
- `Resources`
- `WSL Integration`

然后：

- 勾选你的 WSL 发行版
- 应用并重启 Docker Desktop

## 3. 重启 WSL

在 Windows 侧执行：

```powershell
wsl --shutdown
```

然后重新打开 WSL 终端。

## 4. 验证

在 WSL 里执行：

```bash
docker --version
docker compose version
docker run hello-world
```

## 5. 如果仍然不可用

- 确认 Docker Desktop 仍在运行
- 确认 WSL integration 对当前发行版是开启状态
- 确认没有把 `docker` 相关命令装在错误的环境里
- 重新执行 `wsl --shutdown`

## 影响范围

如果 `docker` 仍不可用，下面这些目录里的示例通常会继续受影响：

- `devops-lab`
- `localstack-lab`
