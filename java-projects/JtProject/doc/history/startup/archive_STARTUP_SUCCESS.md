# JT电商系统 - 启动成功指南

## ✅ 应用启动成功！

### 当前状态
- **状态**: ✅ 运行中
- **访问地址**: http://localhost:8082
- **端口**: 8082
- **Java版本**: OpenJDK 11.0.28
- **数据库**: H2 (文件模式，持久化存储)
- **数据文件位置**: `./data/ecommjava.mv.db`

### 访问应用

#### 1. 浏览器访问
打开浏览器，访问：
```
http://localhost:8082
```

#### 2. 默认账户

**管理员账户**:
- 用户名: `admin`
- 密码: `123`
- 管理后台: http://localhost:8082/admin

**普通用户账户**:
- 用户名: `lisa`
- 密码: `765`

### 快速启动脚本

#### Windows PowerShell
```powershell
# 进入项目目录
cd D:\dev\study\java-projects\JtProject

# 使用启动脚本
.\start-app.ps1

# 或手动启动
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar
```

#### Maven启动（适合开发）
```powershell
# 跳过测试编译和运行
mvn spring-boot:run "-Dmaven.test.skip=true"

# 或者先打包再运行
mvn clean package "-Dmaven.test.skip=true"
java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar
```

### 停止应用

#### 方法1: 使用Ctrl+C
在运行应用的终端窗口按 `Ctrl+C`

#### 方法2: 查找并终止进程
```powershell
# 查找占用8082端口的进程
netstat -ano | findstr :8082

# 终止进程（替换PID为实际进程ID）
Stop-Process -Id <PID> -Force
```

### 常见问题解决

#### 问题1: 启动失败 - 端口被占用
**症状**: 
```
Port 8082 was already in use
```

**解决方案**:
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8082

# 终止进程
Stop-Process -Id <PID> -Force

# 重新启动应用
```

#### 问题2: 编译错误 - Java版本不匹配
**症状**: 
```
类文件具有错误的版本 65.0, 应为 55.0
```

**解决方案**:
```powershell
# 清理并重新编译
cd D:\dev\study\java-projects\JtProject
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"
mvn clean package "-Dmaven.test.skip=true"
```

#### 问题3: 数据库连接失败
**当前配置**: H2嵌入式数据库（无需MySQL）

如需切换到MySQL数据库，修改 `application.properties`:
```properties
# 注释掉H2配置
#db.driver= org.h2.Driver
#db.url= jdbc:h2:file:./data/ecommjava;MODE=MySQL;AUTO_SERVER=TRUE

# 启用MySQL配置
db.driver= com.mysql.cj.jdbc.Driver
db.url= jdbc:mysql://192.168.10.2:3306/ecommjava?createDatabaseIfNotExist=true
db.username= root
db.password= 123456

hibernate.dialect= org.hibernate.dialect.MySQL5Dialect
```

### 应用日志

#### 查看实时日志
应用日志会输出到控制台。关键日志包括：

```
✅ 启动成功标志：
JT电商系统启动成功！
访问地址: http://localhost:8082

✅ Tomcat启动：
Tomcat started on port(s): 8082 (http)

✅ Hibernate初始化：
Hibernate SessionFactory配置完成
```

#### 日志级别配置
在 `application.properties` 中添加：
```properties
# 设置日志级别
logging.level.root=INFO
logging.level.com.jtspringproject=DEBUG
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```

### 开发工具集成

#### IntelliJ IDEA（推荐）⭐
详细的 IDEA 使用指南请查看: **[IDEA_启动指南.md](IDEA_启动指南.md)**

**快速开始**:
1. 打开项目: `File -> Open -> D:\dev\study\java-projects\JtProject`
2. Maven自动导入依赖
3. 配置JDK 11: `File -> Project Structure -> Project SDK`
4. 运行主类: 
   - 打开 `JtSpringProjectApplication.java`
   - 点击 `main` 方法旁的绿色运行图标 ▶
   - 或按 `Shift + F10`

**完整功能**:
- ✅ 直接运行/调试主类
- ✅ Maven 面板打包
- ✅ Spring Boot Dashboard（Ultimate）
- ✅ 热部署配置
- ✅ 数据库工具集成
- ✅ HTTP 客户端测试
- ✅ Git 版本控制

详见: [IDEA_启动指南.md](IDEA_启动指南.md)

#### Eclipse
1. 导入Maven项目: `File -> Import -> Existing Maven Projects`
2. 选择目录: `D:\dev\study\java-projects\JtProject`
3. 右键项目 -> `Run As -> Spring Boot App`

### 项目结构

```
JtProject/
├── src/main/
│   ├── java/com/jtspringproject/JtSpringProject/
│   │   ├── controller/        # 控制器层
│   │   │   ├── AdminController.java
│   │   │   └── UserController.java
│   │   ├── services/          # 服务层
│   │   │   ├── impl/
│   │   │   └── *Service.java
│   │   ├── dao/               # 数据访问层
│   │   │   ├── impl/
│   │   │   └── *Dao.java
│   │   ├── models/            # 实体模型
│   │   │   ├── Product.java
│   │   │   ├── Category.java
│   │   │   ├── User.java
│   │   │   ├── Cart.java
│   │   │   └── CartProduct.java
│   │   ├── HibernateConfiguration.java
│   │   └── JtSpringProjectApplication.java
│   ├── resources/
│   │   ├── application.properties
│   │   └── Product Images/    # 产品图片
│   └── webapp/views/          # JSP视图
│       ├── index.jsp
│       ├── userLogin.jsp
│       └── ...
├── data/                      # H2数据库文件
│   └── ecommjava.mv.db
├── target/                    # 编译输出
│   └── JtSpringProject-0.0.1-SNAPSHOT.jar
├── pom.xml                    # Maven配置
├── start-app.ps1              # 启动脚本
└── README.md

```

### 技术栈信息

- **框架**: Spring Boot 2.6.4
- **ORM**: Hibernate 5（手动配置SessionFactory）
- **视图**: JSP
- **服务器**: Embedded Tomcat
- **数据库**: H2 (开发) / MySQL 8 (生产)
- **构建工具**: Maven 3.x
- **Java版本**: 11

### 下一步操作

1. **访问首页**: http://localhost:8082
2. **测试用户登录**: 使用 `lisa` / `765`
3. **测试管理员功能**: 使用 `admin` / `123`
4. **查看产品列表**: http://localhost:8082/products
5. **访问管理后台**: http://localhost:8082/admin

### 相关文档

- [IDEA启动指南](IDEA_启动指南.md) - IntelliJ IDEA 完整使用教程
- [Controller注释说明](CONTROLLER_注释说明.md)
- [JavaDoc和日志总结](JAVADOC_LOGGING_SUMMARY.md)
- [重构指南](REFACTORING_GUIDE.md)
- [测试指南](TESTING_GUIDE.md)

---

**最后更新**: 2026-01-01  
**应用版本**: 0.0.1-SNAPSHOT  
**状态**: ✅ 运行正常


