# IntelliJ IDEA 快速启动卡片

## 🚀 最快启动方式

### 1️⃣ 打开项目
```
File → Open → D:\dev\study\java-projects\JtProject
```

### 2️⃣ 等待 Maven 导入
```
右下角会显示: "Importing..."
等待完成（首次约2-5分钟）
```

### 3️⃣ 运行应用
```
打开: JtSpringProjectApplication.java
点击 main 方法旁的 ▶ 图标
选择: Run 'JtSpringProjectApplication.main()'
```

### 4️⃣ 访问应用
```
http://localhost:8080
用户名: lisa
密码: 765
```

---

## ⚡ 常用快捷键

### 运行和调试
| 功能 | 快捷键 |
|------|--------|
| 运行 | `Shift + F10` |
| 调试 | `Shift + F9` |
| 停止 | `Ctrl + F2` |
| 重新运行 | `Ctrl + F5` |

### 调试步进
| 功能 | 快捷键 |
|------|--------|
| 单步跳过 | `F8` |
| 单步进入 | `F7` |
| 单步跳出 | `Shift + F8` |
| 继续运行 | `F9` |
| 运行到光标 | `Alt + F9` |

### 代码导航
| 功能 | 快捷键 |
|------|--------|
| 查找类 | `Ctrl + N` |
| 查找文件 | `Ctrl + Shift + N` |
| 跳转到定义 | `Ctrl + B` |
| 查看结构 | `Ctrl + F12` |
| 最近文件 | `Ctrl + E` |

### 代码编辑
| 功能 | 快捷键 |
|------|--------|
| 格式化代码 | `Ctrl + Alt + L` |
| 优化导入 | `Ctrl + Alt + O` |
| 行注释 | `Ctrl + /` |
| 块注释 | `Ctrl + Shift + /` |
| 复制行 | `Ctrl + D` |
| 删除行 | `Ctrl + Y` |

---

## 📦 Maven 快速操作

### 使用 Maven 面板
```
1. 打开: View → Tool Windows → Maven (右侧)
2. 展开: JtSpringProject → Lifecycle
3. 清理: 双击 clean
4. 打包: 双击 package (需先点工具栏 m 图标跳过测试)
```

### Terminal 命令
```powershell
# 清理编译
mvn clean

# 编译项目
mvn compile

# 打包（跳过测试）
mvn package -Dmaven.test.skip=true

# 运行
mvn spring-boot:run -Dmaven.test.skip=true
```

---

## 🐛 调试技巧

### 设置断点
```
1. 点击行号旁添加断点
2. 右键断点可设置条件
3. Debug 模式启动 (Shift + F9)
```

### 常用断点位置
```java
// Controller - 请求入口
AdminController.index()
UserController.userlogin()

// Service - 业务逻辑
ProductServiceImpl.addProduct()

// DAO - 数据库操作
ProductDaoImpl.getProducts()
```

### 查看变量
```
Variables 面板: 查看所有变量
Watches: 添加监视表达式
Evaluate (Alt+F8): 执行任意代码
```

---

## 🔧 常见问题快速修复

### Maven 依赖问题
```
Maven 面板 → 刷新图标 (Reload All Maven Projects)
或
File → Invalidate Caches → Invalidate and Restart
```

### 端口被占用
```powershell
# 查找进程
netstat -ano | findstr :8080

# 停止进程
Stop-Process -Id <PID> -Force
```

### 编译错误
```
1. 确认 JDK 版本: File → Project Structure → Project SDK (Java 11)
2. 重新构建: Build → Rebuild Project
3. 清理缓存: File → Invalidate Caches
```

---

## 📁 项目结构

```
JtProject/
├── src/main/java/
│   └── com/jtspringproject/JtSpringProject/
│       ├── JtSpringProjectApplication.java  ⭐ 主类
│       ├── controller/                       → Controller 层
│       ├── services/                         → Service 层
│       ├── dao/                              → DAO 层
│       └── models/                           → Entity 层
├── src/main/resources/
│   ├── application.properties                ⚙ 配置文件
│   └── Product Images/                       → 图片资源
├── src/main/webapp/views/                    → JSP 视图
├── target/                                   → 编译输出
│   └── JtSpringProject-0.0.1-SNAPSHOT.jar   📦 可执行JAR
└── pom.xml                                   → Maven 配置
```

---

## 🎯 四种启动方式

### ① 直接运行主类（推荐）⭐
```
1. 打开 JtSpringProjectApplication.java
2. 点击 main 方法旁的 ▶
3. 等待启动完成
```

### ② Maven 运行
```
Run → Edit Configurations → + → Maven
Command line: spring-boot:run -Dmaven.test.skip=true
```

### ③ Spring Boot Dashboard（Ultimate）
```
View → Tool Windows → Services
展开 Spring Boot → 右键 Run
```

### ④ 运行 JAR
```
Terminal:
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar
```

---

## 🔨 实用功能

### 热部署（自动重启）
```
File → Settings → Compiler
☑ Build project automatically

File → Settings → Advanced Settings
☑ Allow auto-make to start even if developed application is currently running
```

### HTTP 测试
```
创建文件: api-test.http

### 测试登录
POST http://localhost:8080/userloginvalidate
Content-Type: application/x-www-form-urlencoded

username=lisa&password=765
```

### 数据库工具（Ultimate）
```
View → Tool Windows → Database
+ → Data Source → H2
URL: jdbc:h2:file:./data/ecommjava
User: sa
```

### Git 操作
```
Alt + 0    - 打开 Commit 面板
Alt + 9    - 打开 Git 日志
Ctrl + K   - 提交
Ctrl + Shift + K - 推送
```

---

## 🎨 推荐插件

安装方式: `File → Settings → Plugins → Marketplace`

```
必装:
✅ Lombok                   - 简化 Java 代码
✅ Maven Helper             - Maven 依赖管理
✅ Rainbow Brackets         - 彩色括号

推荐:
⭐ String Manipulation      - 字符串工具
⭐ GenerateAllSetter        - 快速生成 setter
⭐ Spring Boot Assistant    - Spring Boot 增强
⭐ SonarLint                - 代码质量检查
```

---

## 📚 文档链接

| 文档 | 说明 |
|------|------|
| [IDEA_启动指南.md](IDEA_启动指南.md) | 📖 完整详细教程 |
| [STARTUP_SUCCESS.md](STARTUP_SUCCESS.md) | 🚀 通用启动指南 |
| [启动问题解决.md](启动问题解决.md) | 🔧 问题解决方案 |

---

## 💡 小贴士

1. **首次启动慢？** 正常的，Maven 需要下载依赖
2. **代码自动补全？** 输入后按 `Ctrl + Space`
3. **查看文档？** 光标放在代码上按 `Ctrl + Q`
4. **格式化代码？** 选中代码按 `Ctrl + Alt + L`
5. **优化导入？** 按 `Ctrl + Alt + O` 自动整理 import

---

**快速访问**: 将此文件添加到 IDEA 收藏夹
```
右键文件 → Add to Favorites
```

**随时查看**: `Alt + 2` 打开 Favorites 面板

