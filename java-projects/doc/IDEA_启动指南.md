# IntelliJ IDEA 启动指南

## 📋 目录
- [环境要求](#环境要求)
- [导入项目](#导入项目)
- [配置项目](#配置项目)
- [启动方式](#启动方式)
- [调试运行](#调试运行)
- [打包部署](#打包部署)
- [常见问题](#常见问题)

---

## 🔧 环境要求

### 必需软件
- **IntelliJ IDEA**: 2021.3 或更高版本（推荐使用 Ultimate 版本以获得更好的 Spring Boot 支持）
- **Java JDK**: 11（OpenJDK 或 Oracle JDK）
- **Maven**: 3.6+ （IDEA 内置或外部安装）

### 推荐配置
```
操作系统: Windows 10/11, macOS, Linux
内存: 8GB 以上
磁盘空间: 2GB 以上
```

---

## 📂 导入项目

### 方法1: 打开现有项目（推荐）

1. **启动 IntelliJ IDEA**

2. **选择打开项目**
   - 点击 `File` → `Open...`
   - 或在欢迎界面点击 `Open`

3. **选择项目目录**
   ```
   D:\dev\study\java-projects\JtProject
   ```
   - 选择包含 `pom.xml` 的根目录
   - 点击 `OK`

4. **Maven 自动导入**
   - IDEA 会自动检测到 Maven 项目
   - 右下角会提示 "Maven projects need to be imported"
   - 点击 `Import Changes` 或 `Enable Auto-Import`
   - 等待依赖下载完成（首次可能需要几分钟）

### 方法2: 从 VCS 导入

1. **从版本控制克隆**
   ```
   File → New → Project from Version Control...
   ```

2. **输入 Git 仓库地址**
   ```
   URL: https://github.com/kurekako2017/study.git
   Directory: D:\dev\study
   ```

3. **克隆后打开项目**
   ```
   导航到: java-projects/JtProject
   ```

---

## ⚙️ 配置项目

### 1. 配置 JDK

#### 方法A: 通过项目结构设置
1. **打开项目结构**
   ```
   File → Project Structure... (Ctrl+Alt+Shift+S)
   ```

2. **配置 Project SDK**
   - 选择左侧 `Project`
   - `Project SDK`: 选择 `Java 11`
   - 如果没有，点击 `Add SDK` → `Download JDK...`
   - 选择 `Eclipse Adoptium (AdoptOpenJDK HotSpot) 11`
   - `Project language level`: `11 - Local variable syntax for lambda parameters`

3. **配置 Modules SDK**
   - 选择左侧 `Modules`
   - 确保 `Language level` 为 `11`

#### 方法B: 通过 Maven 配置
IDEA 会自动使用 `pom.xml` 中配置的 Java 版本：
```xml
<properties>
    <java.version>11</java.version>
</properties>
```

### 2. 配置 Maven

1. **打开 Maven 设置**
   ```
   File → Settings... (Ctrl+Alt+S)
   Build, Execution, Deployment → Build Tools → Maven
   ```

2. **配置 Maven 选项**
   - `Maven home path`: 使用内置 Maven 或指定外部 Maven
   - `User settings file`: 默认或自定义 settings.xml
   - `Local repository`: Maven 本地仓库路径

3. **Maven Runner 配置**
   - 导航到 `Maven → Runner`
   - `JRE`: 选择 Java 11
   - `VM Options` (可选):
     ```
     -DskipTests=true
     -Dmaven.test.skip=true
     ```

### 3. 启用自动编译（可选）

```
File → Settings → Build, Execution, Deployment → Compiler
☑ Build project automatically
```

---

## 🚀 启动方式

### 方式1: 直接运行主类（最简单）⭐

1. **定位主类**
   ```
   导航到: src/main/java/com/jtspringproject/JtSpringProject
   打开文件: JtSpringProjectApplication.java
   ```

2. **运行应用**
   - 在代码编辑器中，找到 `main` 方法
   - 点击行号旁的绿色运行图标 ▶
   - 选择 `Run 'JtSpringProjectApplication.main()'`
   - 或使用快捷键: `Shift + F10`

3. **查看启动日志**
   - 底部会自动打开 `Run` 面板
   - 等待出现启动成功日志：
     ```
     JT电商系统启动成功！
     访问地址: http://localhost:8080
     ```

### 方式2: 使用 Maven 运行配置

1. **打开 Run/Debug 配置**
   ```
   Run → Edit Configurations...
   ```

2. **添加 Maven 运行配置**
   - 点击左上角 `+` → `Maven`
   - 配置如下：
     ```
     Name: Spring Boot Run
     Command line: spring-boot:run -Dmaven.test.skip=true
     ```
   - 点击 `OK`

3. **运行配置**
   - 选择工具栏的运行配置下拉框 → `Spring Boot Run`
   - 点击运行按钮 ▶
   - 或按 `Shift + F10`

### 方式3: 使用 Spring Boot Dashboard（Ultimate）

如果您使用 IDEA Ultimate 版本：

1. **打开 Services 面板**
   ```
   View → Tool Windows → Services (Alt+8)
   ```

2. **找到 Spring Boot 应用**
   - 在 Services 面板中会自动检测到 Spring Boot 应用
   - 展开 `Spring Boot` 节点

3. **启动应用**
   - 右键点击应用名称
   - 选择 `Run` 或 `Debug`

### 方式4: 运行打包的 JAR

1. **打开 Terminal**
   ```
   View → Tool Windows → Terminal (Alt+F12)
   ```

2. **运行 JAR 文件**
   ```powershell
   java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar
   ```

---

## 🐛 调试运行

### 1. Debug 模式启动

#### 方法A: 直接 Debug 主类
1. 在 `JtSpringProjectApplication.java` 中
2. 点击行号旁的绿色图标 → 选择 `Debug 'JtSpringProjectApplication.main()'`
3. 或使用快捷键: `Shift + F9`

#### 方法B: 使用运行配置 Debug
1. 选择工具栏的运行配置
2. 点击调试按钮 🐛 (或 `Shift + F9`)

### 2. 设置断点

1. **添加断点**
   - 在代码行号处点击，出现红点 🔴
   - 或将光标放在该行，按 `Ctrl + F8`

2. **常用断点位置**
   ```java
   // Controller 层 - 请求入口
   AdminController.java:
     - index() 方法
     - login() 方法
   
   UserController.java:
     - userlogin() 方法
     - addProduct() 方法
   
   // Service 层 - 业务逻辑
   ProductServiceImpl.java:
     - addProduct() 方法
   
   // DAO 层 - 数据库操作
   ProductDaoImpl.java:
     - addProduct() 方法
   ```

3. **条件断点**
   - 右键点击断点 → `Edit Breakpoint...`
   - 添加条件表达式，如: `id == 1`

### 3. Debug 工具栏

启动 Debug 后，底部会显示 Debug 面板：

```
工具栏图标说明:
▶ Resume Program (F9)         - 继续运行
⏸ Pause Program               - 暂停
⏹ Stop (Ctrl+F2)              - 停止
🔄 Rerun (Ctrl+F5)             - 重新运行

步进调试:
⬇ Step Over (F8)              - 单步跳过
⬇ Step Into (F7)              - 单步进入
⬆ Step Out (Shift+F8)         - 单步跳出
🏃 Run to Cursor (Alt+F9)      - 运行到光标处
```

### 4. 查看变量

在 Debug 模式下：
- **Variables 面板**: 查看当前作用域的所有变量
- **Watches**: 添加监视表达式
  - 右键变量 → `Add to Watches`
  - 或在 Watches 面板手动添加表达式

### 5. 评估表达式

- **Evaluate Expression** (Alt+F8)
  - 可以在断点处执行任意代码
  - 查看方法返回值
  - 修改变量值进行测试

---

## 📦 打包部署

### 1. Maven 打包

#### 方法A: 使用 Maven 面板（推荐）

1. **打开 Maven 面板**
   ```
   View → Tool Windows → Maven (右侧边栏)
   ```

2. **执行打包命令**
   - 展开项目名称 `JtSpringProject`
   - 展开 `Lifecycle`
   - 双击 `clean`（清理）
   - 双击 `package`（打包）
   - 或右键 `package` → `Run Maven Build`

3. **跳过测试打包**
   - 在 Maven 面板工具栏点击 `m` 图标（Toggle 'Skip Tests' Mode）
   - 再执行 `package`

#### 方法B: 使用 Terminal 命令

1. **打开 Terminal** (Alt+F12)

2. **执行打包命令**
   ```powershell
   # 清理并打包（跳过测试）
   mvn clean package -Dmaven.test.skip=true
   
   # 或者只编译不打包
   mvn clean compile -DskipTests
   
   # 完整打包（包含测试）
   mvn clean package
   ```

3. **查看输出**
   ```
   成功后输出:
   [INFO] BUILD SUCCESS
   [INFO] ------------------------------------------------------------------------
   
   JAR 文件位置:
   target/JtSpringProject-0.0.1-SNAPSHOT.jar
   ```

### 2. 配置打包选项

#### 创建 Maven Run Configuration

1. **打开运行配置**
   ```
   Run → Edit Configurations...
   ```

2. **添加 Maven 配置**
   - 点击 `+` → `Maven`
   - 配置选项：
     ```
     Name: Package (Skip Tests)
     Command line: clean package -Dmaven.test.skip=true
     ```
   - 点击 `OK`

3. **运行打包**
   - 选择配置 → 点击运行 ▶

### 3. Spring Boot 重新打包

IDEA Ultimate 版本支持 Spring Boot 特性：

1. **使用 Spring Boot Maven 插件**
   ```
   Maven → Plugins → spring-boot → spring-boot:repackage
   ```

2. **生成可执行 JAR**
   - 双击 `spring-boot:repackage`
   - 生成优化的可执行 JAR 文件

### 4. 构建产物说明

打包后的文件结构：
```
target/
├── JtSpringProject-0.0.1-SNAPSHOT.jar          # 可执行 JAR（包含所有依赖）
├── JtSpringProject-0.0.1-SNAPSHOT.jar.original # 原始 JAR（不包含依赖）
├── classes/                                     # 编译后的 class 文件
│   ├── com/jtspringproject/...
│   ├── application.properties
│   └── ...
└── maven-status/                                # Maven 构建状态
```

### 5. 运行打包的应用

#### 在 IDEA Terminal 中运行
```powershell
# 方法1: 使用 java 命令
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar

# 方法2: 指定配置文件
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar --spring.profiles.active=prod

# 方法3: 修改端口
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar --server.port=8081

# 方法4: 后台运行（Windows）
start /B java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar

# 方法5: 后台运行（Linux/Mac）
nohup java -jar target/JtSpringProject-0.0.1-SNAPSHOT.jar &
```

#### 创建运行配置

1. **添加 JAR Application 配置**
   ```
   Run → Edit Configurations... → + → JAR Application
   
   配置:
   Name: Run JAR
   Path to JAR: target/JtSpringProject-0.0.1-SNAPSHOT.jar
   VM options: (留空或添加 JVM 参数)
   Program arguments: (可选的应用参数)
   ```

2. **运行 JAR**
   - 选择配置 → 点击运行 ▶

---

## 🔧 IDEA 实用功能

### 1. 热部署配置（Spring Boot DevTools）

项目已包含 DevTools 依赖，启用热部署：

1. **启用自动构建**
   ```
   File → Settings → Build, Execution, Deployment → Compiler
   ☑ Build project automatically
   ```

2. **启用运行时自动编译**
   ```
   File → Settings → Advanced Settings
   ☑ Allow auto-make to start even if developed application is currently running
   ```

3. **重启应用**
   - 修改代码后，IDEA 会自动编译
   - DevTools 会自动重启应用（几秒钟）

### 2. 数据库工具（Ultimate）

1. **打开 Database 面板**
   ```
   View → Tool Windows → Database (右侧边栏)
   ```

2. **连接 H2 数据库**
   ```
   + → Data Source → H2
   
   配置:
   Name: JtProject-H2
   Host: localhost
   Database: ./data/ecommjava
   URL: jdbc:h2:file:./data/ecommjava
   User: sa
   Password: (留空)
   ```

3. **执行 SQL**
   - 右键数据库 → `Open Query Console`
   - 编写并执行 SQL 查询

### 3. HTTP 客户端

1. **创建 HTTP 请求文件**
   ```
   右键项目 → New → HTTP Request
   文件名: api-test.http
   ```

2. **编写测试请求**
   ```http
   ### 测试首页
   GET http://localhost:8080/
   
   ### 用户登录
   POST http://localhost:8080/userloginvalidate
   Content-Type: application/x-www-form-urlencoded
   
   username=lisa&password=765
   
   ### 管理员登录
   POST http://localhost:8080/admin/adminloginvalidate
   Content-Type: application/x-www-form-urlencoded
   
   username=admin&password=123
   
   ### 获取产品列表
   GET http://localhost:8080/admin/products
   ```

3. **执行请求**
   - 点击请求旁的 ▶ 图标
   - 查看响应结果

### 4. Git 集成

1. **查看变更**
   ```
   View → Tool Windows → Commit (Alt+0)
   ```

2. **提交代码**
   - 勾选要提交的文件
   - 输入提交信息
   - 点击 `Commit` 或 `Commit and Push`

3. **查看历史**
   ```
   View → Tool Windows → Git (Alt+9)
   ```

### 5. 代码导航快捷键

```
常用快捷键:
Ctrl + N          - 查找类
Ctrl + Shift + N  - 查找文件
Ctrl + Alt + B    - 跳转到实现
Ctrl + B          - 跳转到定义
Ctrl + F12        - 查看文件结构
Ctrl + H          - 查看类层次结构
Alt + F7          - 查找使用位置
Ctrl + Alt + L    - 格式化代码
Ctrl + Alt + O    - 优化导入
Ctrl + /          - 行注释
Ctrl + Shift + /  - 块注释
```

---

## ❓ 常见问题

### 问题1: Maven 依赖下载失败

**症状**: 
```
Failed to download artifact
Connection timeout
```

**解决方案**:
1. **配置 Maven 镜像**
   ```
   File → Settings → Build Tools → Maven → User settings file
   ```
   
2. **编辑 settings.xml**（通常在 `~/.m2/settings.xml`）
   ```xml
   <mirrors>
     <mirror>
       <id>aliyun</id>
       <mirrorOf>central</mirrorOf>
       <name>Aliyun Maven</name>
       <url>https://maven.aliyun.com/repository/public</url>
     </mirror>
   </mirrors>
   ```

3. **重新导入 Maven 项目**
   ```
   Maven 面板 → 刷新图标 (Reload All Maven Projects)
   ```

### 问题2: 找不到主类

**症状**:
```
Error: Could not find or load main class
```

**解决方案**:
1. **重新构建项目**
   ```
   Build → Rebuild Project
   ```

2. **清理 IDEA 缓存**
   ```
   File → Invalidate Caches... → Invalidate and Restart
   ```

3. **检查输出目录**
   ```
   File → Project Structure → Modules → Paths
   确认 Output path 正确
   ```

### 问题3: 端口被占用

**症状**:
```
Port 8080 was already in use
```

**解决方案**:
1. **停止现有应用**
   - 点击 Run 面板的停止按钮 ⏹ (Ctrl+F2)

2. **修改端口**
   ```
   application.properties:
   server.port=8081
   ```

3. **查找占用端口的进程**（Terminal）
   ```powershell
   netstat -ano | findstr :8080
   Stop-Process -Id <PID> -Force
   ```

### 问题4: 启动后立即退出

**症状**:
```
应用启动后立即停止
SilentExitException
```

**解决方案**:
1. **禁用 DevTools**
   ```xml
   <!-- 在 pom.xml 中注释掉 -->
   <!--
   <dependency>
     <groupId>org.springframework.boot</groupId>
     <artifactId>spring-boot-devtools</artifactId>
   </dependency>
   -->
   ```

2. **使用 JAR 方式运行**
   ```
   先打包，再运行 JAR 文件
   ```

### 问题5: JSP 页面无法访问

**症状**:
```
404 Not Found
Whitelabel Error Page
```

**解决方案**:
1. **检查视图配置**
   ```properties
   spring.mvc.view.prefix=/views/
   spring.mvc.view.suffix=.jsp
   ```

2. **确认 JSP 文件位置**
   ```
   src/main/webapp/views/
   ```

3. **添加 Tomcat Jasper 依赖**（pom.xml）
   ```xml
   <dependency>
     <groupId>org.apache.tomcat.embed</groupId>
     <artifactId>tomcat-embed-jasper</artifactId>
   </dependency>
   ```

### 问题6: 数据库连接失败

**症状**:
```
Cannot create PoolableConnectionFactory
Connection refused
```

**解决方案**:
1. **检查 H2 配置**
   ```properties
   db.driver=org.h2.Driver
   db.url=jdbc:h2:file:./data/ecommjava;MODE=MySQL;AUTO_SERVER=TRUE
   db.username=sa
   db.password=
   ```

2. **确认数据文件路径**
   ```
   项目根目录/data/ecommjava.mv.db
   ```

3. **切换到内存数据库测试**
   ```properties
   db.url=jdbc:h2:mem:testdb
   ```

### 问题7: 编码问题（中文乱码）

**解决方案**:
1. **设置文件编码**
   ```
   File → Settings → Editor → File Encodings
   Global Encoding: UTF-8
   Project Encoding: UTF-8
   Default encoding for properties files: UTF-8
   ☑ Transparent native-to-ascii conversion
   ```

2. **设置 Console 编码**
   ```
   Help → Edit Custom VM Options
   添加: -Dfile.encoding=UTF-8
   ```

---

## 📚 推荐 IDEA 插件

### 开发效率插件

1. **Lombok Plugin**
   - 简化 Java 代码
   - 自动生成 Getter/Setter

2. **Maven Helper**
   - 分析 Maven 依赖冲突
   - 可视化依赖树

3. **Rainbow Brackets**
   - 彩色括号配对
   - 提高代码可读性

4. **String Manipulation**
   - 字符串处理工具
   - 大小写转换等

5. **GenerateAllSetter**
   - 快速生成对象的所有 setter 调用

### Spring 开发插件

1. **Spring Boot Assistant**
   - Spring Boot 配置提示
   - 依赖管理

2. **JPA Buddy**
   - JPA 实体管理
   - 数据库映射

### 代码质量插件

1. **SonarLint**
   - 代码质量检查
   - 实时代码分析

2. **CheckStyle-IDEA**
   - 代码规范检查

---

## 🎯 最佳实践

### 1. 项目配置管理

创建不同环境的配置文件：
```
src/main/resources/
├── application.properties              # 通用配置
├── application-dev.properties          # 开发环境
├── application-test.properties         # 测试环境
└── application-prod.properties         # 生产环境
```

在 IDEA 运行配置中指定：
```
Program arguments: --spring.profiles.active=dev
```

### 2. 日志配置

在 IDEA 中查看彩色日志：
```properties
# application.properties
spring.output.ansi.enabled=ALWAYS
```

### 3. 远程调试

生产环境问题调试：
```
1. 服务器启动时添加参数:
   java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar app.jar

2. IDEA 配置:
   Run → Edit Configurations → + → Remote JVM Debug
   Host: 服务器IP
   Port: 5005

3. 启动 Debug 连接
```

---

## 📖 相关文档

- [启动问题解决](启动问题解决.md)
- [详细启动指南](STARTUP_SUCCESS.md)
- [JavaDoc和日志总结](JAVADOC_LOGGING_SUMMARY.md)
- [Controller注释说明](CONTROLLER_注释说明.md)

---

## 📞 获取帮助

### IntelliJ IDEA 官方资源
- 官方文档: https://www.jetbrains.com/idea/documentation/
- 快捷键参考: `Help → Keyboard Shortcuts PDF`
- 在线帮助: `Help → Online Documentation`

### 项目资源
- GitHub: https://github.com/kurekako2017/study
- 本地路径: `D:\dev\study\java-projects\JtProject`

---

**最后更新**: 2026-01-01  
**IDEA 版本**: 2021.3+  
**适用项目**: JT电商系统 Spring Boot 应用

