# Docker Desktop 安装指南

## 自动安装（推荐）

### 方法 1: 使用本脚本自动下载安装

```powershell
# 在管理员 PowerShell 中运行以下命令
cd D:\dev\study\scripts
.\install-docker-desktop-final.ps1
```

### 方法 2: 手动下载安装

1. **下载安装程序**
   - 访问：https://www.docker.com/products/docker-desktop/
   - 或直接下载：https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
   - 文件大小约 600 MB

2. **运行安装程序**
   ```powershell
   # 双击下载的文件，或在 PowerShell 中运行：
   Start-Process "下载的文件路径\DockerDesktopInstaller.exe" -Verb RunAs
   ```

3. **等待安装完成**
   - 安装过程需要 5-10 分钟
   - 可能需要重启计算机

4. **启动 Docker Desktop**
   - 从开始菜单启动 "Docker Desktop"
   - 等待 Docker 引擎启动（首次启动需要几分钟）

## 系统要求

- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- 或 Windows 11 64-bit
- 启用 WSL 2 功能
- 至少 4GB RAM

## 验证安装

安装完成后，在新的 PowerShell 窗口中运行：

```powershell
# 检查 Docker 版本
docker --version

# 运行测试容器
docker run hello-world

# 检查 Docker 服务状态
docker info
```

## 运行 LocalStack Java 示例

安装并启动 Docker Desktop 后：

```powershell
# 1. 启动 LocalStack
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
.\run.ps1

# 或手动启动
localstack start -d

# 2. 运行 Java 项目
mvn clean compile exec:java
```

## 常见问题

### WSL 2 未安装
如果遇到 WSL 2 错误，运行：
```powershell
wsl --install
```
然后重启计算机。

### Hyper-V 问题
确保虚拟化已在 BIOS 中启用。

### 权限问题
确保以管理员身份运行 PowerShell。

## 备选方案：使用 Chocolatey

如果 Chocolatey 工作正常：
```powershell
choco install docker-desktop -y
```

## 备选方案：使用 winget

如果有 winget（Windows 11 或更新的 Windows 10）：
```powershell
winget install Docker.DockerDesktop
```

