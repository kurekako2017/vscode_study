# LocalStack 运行日志查看指南

## LocalStack 已成功启动

根据之前的验证,LocalStack 容器已经启动并处于健康状态:
- 容器名称: `localstack`
- 状态: `Up` (healthy)
- 端口映射: `0.0.0.0:4566->4566/tcp`
- 镜像: `localstack/localstack:latest`

---

## 如何查看 LocalStack 运行日志

### 方法 1: 使用 Docker 命令 (推荐)

#### 查看实时日志
```powershell
docker logs -f localstack
```
- `-f` 参数表示持续跟踪日志输出 (follow)
- 按 `Ctrl+C` 停止查看

#### 查看最近的日志
```powershell
# 查看最近 50 行日志
docker logs localstack --tail 50

# 查看最近 100 行日志
docker logs localstack --tail 100
```

#### 查看带时间戳的日志
```powershell
docker logs localstack --timestamps --tail 50
```

#### 保存日志到文件
```powershell
# 保存所有日志
docker logs localstack > D:\dev\study\localstack-lab\logs\localstack.log 2>&1

# 保存最近 200 行日志
docker logs localstack --tail 200 > D:\dev\study\localstack-lab\logs\localstack-recent.log 2>&1
```

### 方法 2: 使用 Docker Desktop (图形界面)

1. 打开 **Docker Desktop**
2. 点击左侧 **Containers** 标签
3. 找到 `localstack` 容器
4. 点击容器名称进入详情页
5. 选择 **Logs** 标签查看实时日志
6. 可以:
   - 搜索日志内容
   - 暂停/恢复日志滚动
   - 复制日志内容

### 方法 3: 使用 LocalStack CLI (如果已安装)

```powershell
# 查看 LocalStack 日志
localstack logs

# 实时跟踪日志
localstack logs -f
```

---

## LocalStack 日志文件位置

### 容器内日志路径
LocalStack 容器内的日志默认位置:
```
/var/lib/localstack/logs/
```

### 持久化日志配置

如果想将日志持久化到宿主机,可以在启动 LocalStack 时挂载卷:

#### 使用 Docker 命令
```powershell
docker run -d `
  --name localstack `
  -p 4566:4566 `
  -e LOCALSTACK_AUTH_TOKEN=$env:LOCALSTACK_AUTH_TOKEN `
  -v D:\dev\study\localstack-lab\logs:/var/lib/localstack/logs `
  localstack/localstack
```

#### 使用 Docker Compose
创建 `docker-compose.yml`:
```yaml
version: '3.8'
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,dynamodb,sqs,lambda
      - DEBUG=1
      - LS_LOG=trace
      - LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN}
    volumes:
      - ./logs:/var/lib/localstack/logs
      - ./data:/var/lib/localstack/data
```

然后运行:
```powershell
cd D:\dev\study\localstack-lab
docker-compose up -d
```

配置后,日志会自动保存到 `D:\dev\study\localstack-lab\logs\` 目录。

---

## 常见日志内容说明

### 启动成功标志
看到以下内容表示 LocalStack 已就绪:
```
Ready.
```

### 服务初始化日志
```
DEBUG --- [  MainThread] localstack.runtime.init    : Starting services...
DEBUG --- [  MainThread] localstack.dns.server      : DNS Server started
```

### API 请求日志
当你调用 AWS 服务时,会看到:
```
INFO  --- [   asgi_gw_0] localstack.request.aws     : AWS s3.CreateBucket => 200
INFO  --- [   asgi_gw_1] localstack.request.aws     : AWS dynamodb.CreateTable => 200
```

### 错误日志
如果有错误,会看到 `ERROR` 或 `WARN` 级别的日志:
```
ERROR --- [  MainThread] localstack.services.lambda : Failed to execute Lambda function
```

---

## Java 应用程序日志

### 运行 Java 项目时的日志

#### Hello LocalStack 示例
```powershell
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
mvn clean compile exec:java -Dexec.mainClass="com.example.localstack.HelloLocalStack"
```

日志输出在**控制台**,如需保存:
```powershell
mvn clean compile exec:java -Dexec.mainClass="com.example.localstack.HelloLocalStack" > output.log 2>&1
```

#### 在 IntelliJ IDEA 中
1. 运行 Java 程序时,日志显示在 IDEA 底部的 **Run** 窗口
2. 右键点击 Run 窗口 → **Export to Text File** 可保存日志
3. 或在 Run Configuration 中:
   - **Run** → **Edit Configurations**
   - 勾选 **Save console output to file**
   - 指定日志文件路径

---

## 实时监控 LocalStack

### 终端方式 (推荐用于调试)
```powershell
# 新开一个 PowerShell 窗口,运行:
docker logs -f localstack
```
保持这个窗口开着,在另一个窗口运行你的 Java 程序,就能实时看到 LocalStack 处理请求的日志。

### Web UI 方式
访问 LocalStack Web UI: https://app.localstack.cloud
- 连接到本地实例: `http://localhost:4566`
- 可以图形化查看:
  - 所有 AWS 资源 (S3 buckets, DynamoDB tables, Lambda 函数等)
  - API 调用历史
  - 日志输出

---

## 日志级别配置

可以通过环境变量调整 LocalStack 日志详细程度:

```powershell
# 停止当前容器
docker stop localstack
docker rm localstack

# 以调试模式启动
docker run -d `
  --name localstack `
  -p 4566:4566 `
  -e DEBUG=1 `
  -e LS_LOG=trace `
  -e LOCALSTACK_AUTH_TOKEN=$env:LOCALSTACK_AUTH_TOKEN `
  localstack/localstack
```

日志级别选项:
- `LS_LOG=trace` - 最详细
- `LS_LOG=debug` - 调试信息
- `LS_LOG=info` - 一般信息 (默认)
- `LS_LOG=warning` - 仅警告和错误
- `LS_LOG=error` - 仅错误

---

## 快速检查脚本

我已经创建了检查脚本,可以直接运行:

### PowerShell 脚本
```powershell
D:\dev\study\scripts\verify-localstack.ps1
```

### 批处理脚本
```cmd
D:\dev\study\scripts\check-localstack.bat
```

这些脚本会自动:
1. 检查 Docker 状态
2. 检查 LocalStack 容器状态
3. 启动 LocalStack (如果未运行)
4. 测试 API 连通性
5. 显示最近日志

---

## 故障排查

### 看不到日志输出?
```powershell
# 确认容器正在运行
docker ps | Select-String localstack

# 如果容器停止了
docker start localstack

# 等待几秒后再查看日志
docker logs localstack
```

### 日志太多找不到关键信息?
```powershell
# 使用 grep 过滤
docker logs localstack | Select-String "ERROR"
docker logs localstack | Select-String "Lambda"
docker logs localstack | Select-String "Ready"
```

### 清空日志重新开始?
```powershell
# 重启容器会清空日志
docker restart localstack

# 或完全删除并重新创建
docker stop localstack
docker rm localstack
docker run -d --name localstack -p 4566:4566 localstack/localstack
```

---

## 总结

**最常用的命令:**
```powershell
# 查看实时日志
docker logs -f localstack

# 查看最近 50 行
docker logs localstack --tail 50

# 保存日志到文件
docker logs localstack > localstack.log 2>&1
```

**图形化方式:**
- Docker Desktop → Containers → localstack → Logs 标签
- LocalStack Web UI: https://app.localstack.cloud

---

**创建日期**: 2026-01-01  
**维护者**: Study Repository

