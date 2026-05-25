# LocalStack 无法启动排查指南

## 问题现象
昨天可以正常运行，今天无法启动或测试失败。

---

## 最常见原因（按概率排序）

### 1. Docker Desktop 未启动 ⭐⭐⭐⭐⭐ (最常见)

**检查方法**:
```powershell
docker ps
```

**如果显示错误**: "error during connect: This error may indicate that the docker daemon is not running"

**解决方法**:
1. 在 Windows 开始菜单搜索 "Docker Desktop"
2. 点击启动
3. 等待 Docker 图标在系统托盘显示为正常（非加载状态）
4. 再次运行 `docker ps` 确认

**启动成功标志**:
- 系统托盘 Docker 图标不再旋转
- 运行 `docker ps` 显示容器列表（可能为空）

---

### 2. LocalStack 容器已停止 ⭐⭐⭐⭐

**检查方法**:
```powershell
docker ps -a | Select-String localstack
```

**如果显示**: `Exited` 或 `Created`

**解决方法**:
```powershell
docker start localstack
```

**验证**:
```powershell
docker ps | Select-String localstack
```
应显示 `Up` 状态

---

### 3. 端口 4566 被占用 ⭐⭐⭐

**检查方法**:
```powershell
netstat -ano | findstr 4566
```

**如果有输出**: 说明端口被占用

**解决方法**:
```powershell
# 方法 A: 重启 LocalStack
docker restart localstack

# 方法 B: 停止占用端口的程序
# 找到 PID (最后一列数字)，在任务管理器中结束该进程
```

---

### 4. 电脑重启后容器未自动启动 ⭐⭐

Windows 重启后，Docker 容器默认不会自动启动。

**解决方法**:
```powershell
# 每次重启后运行
docker start localstack
```

**永久解决**: 设置容器自动启动
```powershell
docker update --restart=unless-stopped localstack
```

---

### 5. LocalStack 容器被删除 ⭐

**检查方法**:
```powershell
docker ps -a
```

**如果没有 localstack**: 容器被删除了

**解决方法**: 重新创建容器
```powershell
docker run -d `
  --name localstack `
  -p 4566:4566 `
  -e LOCALSTACK_AUTH_TOKEN=$env:LOCALSTACK_AUTH_TOKEN `
  localstack/localstack
```

---

## 完整诊断流程

### 步骤 1: 检查 Docker
```powershell
docker --version
docker info
```

**预期结果**: 
- 显示 Docker 版本
- 显示 Docker 系统信息（不报错）

**如果失败**: Docker Desktop 未启动 → 启动 Docker Desktop

---

### 步骤 2: 检查 LocalStack 容器
```powershell
docker ps -a | Select-String localstack
```

**预期结果**: 显示 localstack 容器状态

**情况分析**:
- `Up X minutes`: 容器正在运行 ✓
- `Exited (0)`: 容器已停止 → `docker start localstack`
- 无输出: 容器不存在 → 重新创建容器

---

### 步骤 3: 测试 LocalStack API
```powershell
curl http://localhost:4566/_localstack/health
```

**预期结果**: 返回 JSON 数据

**如果失败**: 
- 检查容器是否真的在运行: `docker ps`
- 检查端口映射: `docker port localstack`
- 查看容器日志: `docker logs localstack --tail 20`

---

### 步骤 4: 运行测试
```powershell
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
.\test-localstack.ps1
```

---

## 快速修复命令（按顺序执行）

```powershell
# 1. 确保 Docker Desktop 已启动（手动从开始菜单启动）

# 2. 启动 LocalStack
docker start localstack

# 3. 等待 5 秒
Start-Sleep -Seconds 5

# 4. 验证状态
docker ps | Select-String localstack

# 5. 测试 API
Invoke-WebRequest -Uri http://localhost:4566/_localstack/health -UseBasicParsing

# 6. 运行测试
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
.\test-localstack.ps1
```

---

## 查看日志

### LocalStack 容器日志
```powershell
# 查看最近 50 行
docker logs localstack --tail 50

# 实时查看
docker logs -f localstack

# 查找错误
docker logs localstack 2>&1 | Select-String "error"
```

### Java 测试日志
```powershell
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
Get-Content test-output.log
```

---

## 常见错误消息

### "error during connect"
**原因**: Docker Desktop 未运行  
**解决**: 启动 Docker Desktop

### "No such container: localstack"
**原因**: 容器不存在  
**解决**: 重新创建容器

### "port is already allocated"
**原因**: 端口 4566 被占用  
**解决**: 
```powershell
docker stop localstack
docker start localstack
```

### "Cannot connect to LocalStack"
**原因**: LocalStack 未启动或端口问题  
**解决**: 检查容器状态和端口

---

## 完全重置（最后手段）

如果所有方法都失败，完全重置 LocalStack:

```powershell
# 1. 停止并删除容器
docker stop localstack
docker rm localstack

# 2. 重新创建
docker run -d `
  --name localstack `
  -p 4566:4566 `
  -e LOCALSTACK_AUTH_TOKEN=$env:LOCALSTACK_AUTH_TOKEN `
  localstack/localstack

# 3. 等待启动
Start-Sleep -Seconds 10

# 4. 验证
docker logs localstack --tail 20
```

---

## 预防措施

### 设置自动启动
```powershell
# Docker Desktop 开机自启动（设置中启用）
# LocalStack 容器自动启动
docker update --restart=unless-stopped localstack
```

### 创建快速启动脚本
保存为 `start-localstack.bat`:
```batch
@echo off
echo Starting LocalStack...
docker start localstack
timeout /t 5
docker ps | findstr localstack
pause
```

---

## 使用诊断工具

我已创建诊断脚本:
```powershell
cd D:\dev\study\localstack-lab
.\diagnose.ps1
```

该脚本会自动检查:
- Docker 状态
- LocalStack 容器状态
- 端口占用
- Java/Maven 环境
- 项目文件
- LocalStack API 连通性

并提供自动修复选项。

---

## 联系信息

**相关文档**:
- `QUICK_REFERENCE.md` - 快速参考
- `LOCALSTACK_TEST_SUMMARY.md` - 测试总结
- `运行指南.md` - 详细运行说明

**诊断工具**:
- `diagnose.ps1` - 自动诊断脚本
- `test-localstack.ps1` - 测试脚本

---

**最后更新**: 2026-01-02

