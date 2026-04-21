# Docker 与容器

## 1. 为什么先学这一块

在 `DevOps / SRE` 这条线上，`Docker` 往往是最容易先练起来的一步。

因为它直接关系到：

- 环境一致性
- 本地和部署环境的差异缩小
- 服务启动和排障
- 日志查看

对你这个工作区来说，`Docker` 也是现有材料最多的一块。

## 2. 这一阶段要掌握什么

- `Docker Desktop`
- 常用命令
- 容器日志
- 容器状态检查
- 启动失败排查

## 3. 最小教程

可以先把最小使用路径理解成：

1. 确认 Docker 已安装
2. 确认 Docker Engine 正常
3. 启动一个容器
4. 查看日志
5. 排查启动失败

## 4. 当前工作区里的教程

- [DOCKER_INSTALL_GUIDE.md](D:/dev/source_code/vscode_study/scripts/docker/DOCKER_INSTALL_GUIDE.md)
- [TROUBLESHOOTING.md](D:/dev/source_code/vscode_study/localstack-lab/TROUBLESHOOTING.md)
- [如何查看LocalStack日志.md](D:/dev/source_code/vscode_study/localstack-lab/%E5%A6%82%E4%BD%95%E6%9F%A5%E7%9C%8BLocalStack%E6%97%A5%E5%BF%97.md)
- [UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](D:/dev/source_code/vscode_study/softbs/UM890Pro_Win11_WSL2_Docker_Java_Python_%E6%9C%AC%E5%9C%B0%E6%A8%A1%E5%9E%8B%E8%BE%85%E5%8A%A9%E5%BC%80%E5%8F%91%E6%95%99%E7%A8%8B.md)

## 5. 当前工作区里的现成示例

- [check-docker-status.ps1](D:/dev/source_code/vscode_study/scripts/check-docker-status.ps1)
- [diagnostic.ps1](D:/dev/source_code/vscode_study/scripts/localstack/diagnostic.ps1)
- [monitor-status.ps1](D:/dev/source_code/vscode_study/scripts/localstack/monitor-status.ps1)
- [verify-localstack.ps1](D:/dev/source_code/vscode_study/scripts/localstack/verify-localstack.ps1)
- [wait-for-docker-and-run.ps1](D:/dev/source_code/vscode_study/scripts/localstack/wait-for-docker-and-run.ps1)

## 6. 最小示例

你现在最适合先跑的不是自己写容器，而是先跑检查脚本和日志查看链路。

例如：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-docker-status.ps1
```

再例如：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\localstack\monitor-status.ps1
```

## 7. 练习题

### 练习 1

运行 Docker 检查脚本，确认当前机器状态。

### 练习 2

读一遍 `TROUBLESHOOTING.md`，整理出最常见的 3 类 Docker 问题。

### 练习 3

跑一次 LocalStack 日志查看流程。

### 练习 4

自己修改一个状态脚本，让它多输出一个检查项。

## 8. 学到什么程度算过关

- 能确认 Docker 是否正常
- 能看容器日志
- 能解释容器启动失败的常见原因
- 能运行并理解当前工作区里的检查脚本
