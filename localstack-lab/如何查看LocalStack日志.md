# LocalStack 日志查看快速指南

## LocalStack 容器已启动并运行正常 ✓

根据之前的验证,您的 LocalStack 已经成功启动:
- **容器 ID**: 90d10d1fd198
- **镜像**: localstack/localstack:latest
- **状态**: Up (healthy)
- **端口**: 0.0.0.0:4566->4566/tcp
- **运行时长**: 45+ 小时

---

## 最简单的查看日志方法

### 1. Docker Desktop 图形界面 (最简单)

1. 打开 **Docker Desktop** 应用
2. 点击左侧 **Containers** (容器)
3. 找到并点击 **localstack** 容器
4. 点击 **Logs** 标签
5. 可以看到实时滚动的日志输出

**优点**: 
- 图形化,易于使用
- 支持搜索和过滤
- 可以暂停/恢复日志滚动
- 彩色显示

---

### 2. PowerShell 命令行

#### 查看最近 50 行日志
```powershell
docker logs localstack --tail 50
```

#### 查看实时日志 (持续输出)
```powershell
docker logs -f localstack
```
按 `Ctrl+C` 停止查看

#### 保存日志到文件
```powershell
# 创建日志目录
New-Item -ItemType Directory -Force -Path "D:\dev\study\localstack-lab\logs"

# 保存所有日志
docker logs localstack > "D:\dev\study\localstack-lab\logs\localstack-all.log" 2>&1

# 保存最近 200 行
docker logs localstack --tail 200 > "D:\dev\study\localstack-lab\logs\localstack-recent.log" 2>&1
```

---

### 3. 在 IDEA 中查看

如果在 IntelliJ IDEA 中运行 Java 程序连接 LocalStack:

1. 运行程序时,日志在底部 **Run** 窗口显示
2. Java 应用的日志和 LocalStack 的日志是分开的
3. LocalStack 的日志需要用上面的命令查看

---

## Java 应用日志查看

### Hello LocalStack 示例

```powershell
# 进入项目目录
cd D:\dev\study\localstack-lab\projects\hello-localstack-java

# 运行并保存输出
mvn clean compile exec:java -Dexec.mainClass="com.example.localstack.HelloLocalStack" > app.log 2>&1

# 查看输出
Get-Content app.log
```

---

## 同时监控 LocalStack 和 Java 应用

**推荐方式**: 打开两个 PowerShell 窗口

**窗口 1** - 监控 LocalStack:
```powershell
docker logs -f localstack
```

**窗口 2** - 运行 Java 应用:
```powershell
cd D:\dev\study\localstack-lab\projects\hello-localstack-java
mvn clean compile exec:java
```

这样可以同时看到:
- 窗口 1: LocalStack 接收和处理请求的日志
- 窗口 2: Java 应用的执行输出

---

## 查看当前 LocalStack 状态

在任意 PowerShell 窗口运行:

```powershell
# 检查容器状态
docker ps | Select-String localstack

# 查看最近 10 行日志
docker logs localstack --tail 10
```

---

## 下次如何查看日志

**最快方式**: 直接运行
```powershell
docker logs -f localstack
```

**图形化方式**: 
打开 Docker Desktop → Containers → localstack → Logs

---

**提示**: LocalStack 日志位于 Docker 容器内,不是文件系统中的文件。必须通过 `docker logs` 命令或 Docker Desktop 查看。

**相关文档**: `LOCALSTACK_查看运行结果.md` (完整指南)

