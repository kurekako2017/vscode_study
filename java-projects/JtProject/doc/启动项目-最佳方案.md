# 🚀 JT电商项目启动 - 最佳方案

> ⚠️ 文档状态：历史说明（建议归档）
>
> 请优先使用主文档：`../README.md` 和 `手动启动项目完整指南.md`。
> 导航入口：`文档导航.md`。
> 当前项目默认端口为 `8082`。

## ⚠️ 当前问题

通过命令行启动项目时，遇到了 **端口8082持续被占用** 的问题。这是因为：

1. 之前的Java进程可能没有完全停止。
2. Windows系统端口释放需要时间。
3. 可能有其他应用占用了8082端口。

---

## ✅ 推荐方案：使用IntelliJ IDEA启动（成功率99%）

### 方案1：IDEA直接运行主类 ⭐⭐⭐⭐⭐（最推荐）

#### 步骤

1. **打开IntelliJ IDEA**
   - 双击桌面图标或开始菜单中的IDEA。
2. **打开项目**
   - `File` → `Open`。
   - 选择目录：`D:\dev\source_code\vscode_study\java-projects\JtProject`。
   - 点击 `OK`。
3. **等待项目加载**
   - IDEA会自动识别Maven项目。
   - 右下角会显示 `Indexing...`，等待完成。
   - Maven会自动下载依赖。
4. **找到主类**
   - 按 `Ctrl + N` 打开查找类对话框。
   - 输入 `JtSpringProjectApplication`。
   - 按回车打开该文件。
5. **运行项目**
   - 方式A：点击类名左侧的绿色 ▶️ 图标，选择 `Run 'JtSpringProjectApplication'`。
   - 方式B：右键点击类文件，选择 `Run 'JtSpringProjectApplication.main()'`。
   - 方式C：按快捷键 `Shift + F10`。
6. **查看启动日志**
   - 底部会打开 `Run` 控制台。
   - 等待看到：

```text
JT电商系统启动成功！
访问地址: http://localhost:8082
```

1. **访问应用**
   - 浏览器打开：<http://localhost:8082>。
   - 如果端口被占用，IDEA会自动提示。

#### 优点

- ✅ **最稳定**：IDEA会自动管理端口和进程。
- ✅ **实时日志**：彩色输出，易于阅读。
- ✅ **支持调试**：可以打断点调试。
- ✅ **热部署**：代码修改后自动重启。
- ✅ **一键停止**：点击红色 ⏹️ 按钮即可停止。

---

### 方案2：IDEA使用Maven运行 ⭐⭐⭐⭐

#### 方案2步骤

1. **打开Maven工具窗口**
   - 点击右侧边栏的 `Maven` 标签。
   - 或按 `Ctrl + E` 输入 `Maven`。
2. **运行Spring Boot**
   - 展开 `JtSpringProject` → `Plugins` → `spring-boot`。
   - 双击 `spring-boot:run`。
3. **查看日志**
   - 在 `Run` 控制台查看启动过程。

---

## 🔧 方案3：命令行启动（需要先解决端口问题）

### 前置步骤：彻底清理8082端口

#### Windows PowerShell命令

```powershell
# 1. 进入项目目录
cd D:\dev\source_code\vscode_study\java-projects\JtProject

# 2. 查找占用8082端口的进程
netstat -ano | findstr ":8082"
# 记下最后一列的PID（进程ID）

# 3. 停止该进程（替换<PID>为实际的进程ID）
taskkill /F /PID <PID>

# 或者直接停止所有Java进程
Get-Process -Name java | Stop-Process -Force

# 4. 等待5秒让端口释放
Start-Sleep -Seconds 5

# 5. 确认端口已释放
netstat -ano | findstr ":8082"
# 如果没有输出，说明端口空闲
```

### 启动方式A：使用Maven（推荐）

```powershell
# 跳过测试启动
mvn spring-boot:run -Dmaven.test.skip=true
```

### 启动方式B：直接运行JAR包

```powershell
# 使用JDK 21
& "C:\Program Files\jdk-21.0.2\bin\java.exe" -jar .\target\JtSpringProject-0.0.1-SNAPSHOT.jar
```

### 启动方式C：使用不同端口

如果8082端口始终被占用，可以使用其他端口：

```powershell
# 使用8083端口
java -jar .\target\JtSpringProject-0.0.1-SNAPSHOT.jar --server.port=8083

# 访问地址变为：http://localhost:8083
```

---

## 🛠️ 方案4：修改配置文件永久更换端口

如果8082端口经常被占用，可以永久修改端口。

### 方案4步骤

1. **打开配置文件**
   - 文件路径：`src/main/resources/application.properties`。
1. **添加或修改端口配置**

```properties
# 服务器端口配置
server.port=8083
```

1. **保存文件**。
1. **重新启动项目**
   - 现在默认端口就是8083了。

---

## ❌ 常见启动失败原因及解决方法

### 问题1：端口8082被占用

**错误信息：**

```text
Port 8082 is already in use
```

**解决方法：**

1. **查找占用进程**

```powershell
netstat -ano | findstr ":8082"
```

1. **停止进程**

```powershell
taskkill /F /PID <进程ID>
```

1. **或更换端口**

```powershell
java -jar xxx.jar --server.port=8083
```

### 问题2：Maven命令找不到

**错误信息：**

```text
'mvn' 不是内部或外部命令
```

**解决方法：**

- 使用Maven Wrapper（项目自带）：

```powershell
.\mvnw spring-boot:run
```

### 问题3：Java命令找不到

**错误信息：**

```text
'java' 不是内部或外部命令
```

**解决方法：**

- 使用完整路径：

```powershell
& "C:\Program Files\jdk-21.0.2\bin\java.exe" -jar xxx.jar
```

### 问题4：数据库连接失败

**错误信息：**

```text
Unable to create requested service [org.hibernate.engine.jdbc.env.spi.JdbcEnvironment]
```

**解决方法：**

1. 确认H2数据库文件路径存在。
2. 检查 `application.properties` 配置。
3. 默认使用H2文件数据库，无需额外配置。

---

## ✅ 启动成功标志

当您看到以下日志时，说明启动成功：

```text
========================================
JT电商系统启动成功！
访问地址: http://localhost:8082
========================================
```

或者：

```text
Started JtSpringProjectApplication in X.XXX seconds
```

---

## 🌐 访问应用

启动成功后，在浏览器访问：

### 用户端

- **首页**：<http://localhost:8082>
- **用户登录**：<http://localhost:8082/user/login>
- **用户注册**：<http://localhost:8082/register>

### 管理端

- **管理员登录**：<http://localhost:8082/admin/login>
  - 默认账号：`admin` / `admin`

### 测试账号

- **用户账号**：`lisa` / `765`
- **管理员**：`admin` / `123`

---

## 🔄 停止应用

### IDEA中停止

- 点击 `Run` 控制台的红色 **⏹️ 停止按钮**。
- 或按快捷键 `Ctrl + F2`。

### 命令行停止

- 按 `Ctrl + C`。
- 或找到Java进程并停止：

```powershell
Get-Process -Name java | Stop-Process -Force
```

---

## 📊 启动方式对比

| 方式 | 难度 | 成功率 | 调试 | 热部署 | 推荐度 |
| --- | --- | --- | --- | --- | --- |
| **IDEA运行主类** | ⭐ | 99% | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **IDEA Maven运行** | ⭐⭐ | 95% | ✅ | ✅ | ⭐⭐⭐⭐ |
| **命令行Maven** | ⭐⭐⭐ | 85% | ❌ | ✅ | ⭐⭐⭐ |
| **命令行JAR** | ⭐⭐⭐ | 80% | ❌ | ❌ | ⭐⭐ |

---

## 💡 最佳实践建议

1. **首次启动**：使用IDEA运行主类。
2. **日常开发**：使用IDEA，利用热部署功能。
3. **测试部署**：使用Maven打包后运行JAR。
4. **生产部署**：使用JAR包 + 外部配置。

---

## 📚 相关文档

- [IDEA完整启动指南.md](IDEA完整启动指南.md)：IDEA详细教程。
- [IDEA黑色主题完整设置指南.md](IDEA黑色主题完整设置指南.md)：主题设置。
- [项目框架与内容总结.md](项目框架与内容总结.md)：项目完整文档。
- [启动问题解决.md](启动问题解决.md)：常见问题汇总。

---

## 🎯 快速启动清单

启动前请确认：

- [ ] JDK已安装（JDK 11 或 JDK 21）
- [ ] IDEA已安装并配置好JDK
- [ ] 项目已用IDEA打开
- [ ] Maven依赖已下载完成
- [ ] 8082端口未被占用
- [ ] 项目索引已完成（右下角无进度条）

---

**强烈建议：使用IntelliJ IDEA启动项目，这是最简单、最可靠的方式。** 🎉

如果您在IDEA中也遇到端口占用问题，IDEA会智能提示您停止之前的实例或更换端口。


