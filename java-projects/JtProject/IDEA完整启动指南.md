# IntelliJ IDEA 完整启动指南

## 📚 目录
1. [IDEA基础操作](#idea基础操作)
2. [主题设置（黑色主题）](#主题设置)
3. [项目启动步骤](#项目启动步骤)
4. [常用快捷键](#常用快捷键)
5. [故障排除](#故障排除)

---

## 🎯 IDEA基础操作

### 打开项目
1. **启动IDEA**
   - 双击桌面图标或开始菜单中的 IntelliJ IDEA
   
2. **打开JtProject项目**
   - 方式1：在欢迎界面点击 **"Open"** 按钮
   - 方式2：如果已有项目打开，点击菜单栏 `File` → `Open`
   
3. **在文件选择对话框中选择项目**
   - 对话框会显示文件浏览器
   - 导航到：`D:\dev\source_code\vscode_study\java-projects\JtProject`
   - **只需单击选中** `JtProject` 文件夹（文件夹会高亮显示）
   - **不需要右键**，也不需要双击进入文件夹
   - 选中后，直接点击对话框右下角的 **"OK"** 按钮即可

### 等待项目加载
- IDEA会自动识别为Maven项目
- 右下角会显示 "Indexing..." 等待索引完成
- Maven会自动下载依赖（需要网络）

---

## 🎨 主题设置（黑色主题）

### 方法1：通过设置菜单
1. **打开设置**
   - 快捷键：`Ctrl + Alt + S` （Windows）
   - 或菜单：`File` → `Settings`

2. **选择主题**
   - 左侧导航：`Appearance & Behavior` → `Appearance`
   - 在右侧找到 **"Theme"** 下拉菜单
   - 选择以下任一黑色主题：
     - **Darcula** （经典深色主题，推荐）
     - **High contrast** （高对比度深色）
     - **IntelliJ Light**（如果想要亮色主题）

3. **应用设置**
   - 点击 **"Apply"** 应用更改
   - 点击 **"OK"** 关闭设置窗口

### 方法2：快速切换
1. **快速操作**
   - 快捷键：`Ctrl + ` (反引号，Esc下方的键)
   - 或：`Ctrl + Shift + A` 输入 "theme"
   - 选择 "Theme" 后选择 Darcula

### 编辑器字体和配色
1. **设置代码编辑器配色**
   - `Settings` → `Editor` → `Color Scheme`
   - 选择 **"Darcula"** 或其他深色方案

2. **调整字体大小**
   - `Settings` → `Editor` → `Font`
   - 推荐字体：Consolas、JetBrains Mono
   - 推荐大小：14-16

---

## 🚀 项目启动步骤

### 步骤1：配置JDK
1. **检查项目JDK**
   - 快捷键：`Ctrl + Alt + Shift + S` 打开项目结构
   - 或菜单：`File` → `Project Structure`
   
2. **设置SDK**
   - 左侧选择 **"Project"**
   - **"Project SDK"** 选择 JDK 11 或 JDK 21
   - 如果没有，点击 "Add SDK" → "Download JDK" 或 "Add SDK" → "JDK" 选择本地JDK
   - 项目语言级别：选择 11 或 17

3. **点击 "OK" 保存**

### 步骤2：Maven配置
1. **刷新Maven项目**
   - 右键点击 `pom.xml`
   - 选择 **"Maven"** → **"Reload project"**
   - 或点击右侧 Maven 工具窗口的刷新按钮 🔄

2. **等待依赖下载完成**
   - 查看右下角进度条
   - 可能需要几分钟

### 步骤3：启动应用

#### 方式A：使用IDEA内置运行（推荐）
1. **找到主类**
   - 打开文件：`src/main/java/com/jtspringproject/JtSpringProject/JtSpringProjectApplication.java`
   - 快捷键：`Ctrl + N` 输入 "JtSpringProjectApplication"

2. **运行应用**
   - 点击类名或main方法左侧的 **绿色▶️图标**
   - 选择 **"Run 'JtSpringProjectApplication'"**
   - 或快捷键：`Shift + F10`

3. **查看运行结果**
   - 底部会打开 "Run" 控制台
   - 等待看到 "JT电商系统启动成功！"
   - 访问：http://localhost:8080

#### 方式B：使用Maven命令
1. **打开Maven工具窗口**
   - 右侧边栏点击 **"Maven"**
   - 或快捷键：`Ctrl + E` → 输入 "Maven"

2. **运行Spring Boot**
   - 展开 `JtSpringProject` → `Plugins` → `spring-boot`
   - 双击 **"spring-boot:run"**

3. **查看控制台输出**

#### 方式C：使用终端
1. **打开IDEA终端**
   - 快捷键：`Alt + F12`
   - 或底部工具栏点击 **"Terminal"**

2. **执行启动命令**
   ```powershell
   # 方式1：Maven启动（跳过测试）
   mvn spring-boot:run -Dmaven.test.skip=true
   
   # 方式2：直接运行JAR
   java -jar .\target\JtSpringProject-0.0.1-SNAPSHOT.jar
   ```

### 步骤4：验证启动
1. **检查控制台日志**
   - 应该看到 Spring Boot 启动日志
   - 最后显示 "JT电商系统启动成功！"
   - 端口：8080

2. **访问应用**
   - 浏览器打开：http://localhost:8080
   - 应该看到网站首页

3. **停止应用**
   - 点击控制台的红色 ⏹️ 停止按钮
   - 或快捷键：`Ctrl + F2`

---

## ⌨️ 常用快捷键

### 导航类
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl + N` | 查找类 | 输入类名快速打开 |
| `Ctrl + Shift + N` | 查找文件 | 查找任意文件 |
| `Ctrl + E` | 最近文件 | 显示最近打开的文件 |
| `Ctrl + Shift + E` | 最近编辑位置 | 跳转到最近编辑的地方 |
| `Ctrl + B` | 跳转到定义 | 跳转到类/方法定义处 |
| `Ctrl + Alt + ←/→` | 前进/后退 | 导航历史位置 |
| `Alt + F7` | 查找用法 | 查找方法/类被使用的地方 |
| `Ctrl + H` | 查看类层次结构 | 查看继承关系 |

### 编辑类
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl + Space` | 基本代码补全 | 自动完成代码 |
| `Ctrl + Shift + Space` | 智能代码补全 | 更智能的补全 |
| `Ctrl + /` | 单行注释 | 注释/取消注释 |
| `Ctrl + Shift + /` | 块注释 | 多行注释 |
| `Ctrl + D` | 复制行 | 复制当前行到下一行 |
| `Ctrl + Y` | 删除行 | 删除当前行 |
| `Ctrl + Shift + ↑/↓` | 移动代码块 | 上下移动方法 |
| `Alt + Insert` | 生成代码 | 生成getter/setter等 |
| `Ctrl + Alt + L` | 格式化代码 | 自动排版代码 |
| `Ctrl + Alt + O` | 优化导入 | 移除未使用的import |

### 运行和调试
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Shift + F10` | 运行 | 运行当前配置 |
| `Shift + F9` | 调试 | 调试模式运行 |
| `Ctrl + F2` | 停止 | 停止运行的程序 |
| `F8` | 单步跳过 | 调试时执行下一行 |
| `F7` | 单步进入 | 调试时进入方法内部 |
| `Shift + F8` | 单步跳出 | 调试时跳出当前方法 |
| `Ctrl + F8` | 切换断点 | 添加/删除断点 |
| `Alt + F8` | 计算表达式 | 调试时查看变量值 |

### 搜索和替换
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl + F` | 查找 | 在当前文件查找 |
| `Ctrl + R` | 替换 | 在当前文件替换 |
| `Ctrl + Shift + F` | 全局查找 | 在整个项目查找 |
| `Ctrl + Shift + R` | 全局替换 | 在整个项目替换 |
| `F3` / `Shift + F3` | 查找下一个/上一个 | 跳转到下一个匹配 |

### 窗口管理
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Alt + 1` | 项目窗口 | 打开/关闭项目树 |
| `Alt + 4` | 运行窗口 | 打开运行控制台 |
| `Alt + 5` | 调试窗口 | 打开调试窗口 |
| `Alt + 9` | Git窗口 | 打开版本控制 |
| `Alt + F12` | 终端窗口 | 打开终端 |
| `Shift + Esc` | 关闭活动窗口 | 关闭当前工具窗口 |
| `Ctrl + Shift + F12` | 最大化编辑器 | 隐藏所有工具窗口 |

### 重构
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Shift + F6` | 重命名 | 重命名变量/类/方法 |
| `Ctrl + Alt + M` | 提取方法 | 将代码提取为方法 |
| `Ctrl + Alt + V` | 提取变量 | 将表达式提取为变量 |
| `Ctrl + Alt + C` | 提取常量 | 提取为常量 |
| `Ctrl + Alt + P` | 提取参数 | 提取为方法参数 |

### 其他常用
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl + Alt + S` | 设置 | 打开设置窗口 |
| `Ctrl + Shift + A` | 查找动作 | 搜索任何操作 |
| `双击 Shift` | 全局搜索 | 搜索一切（文件/类/操作） |
| `Alt + Enter` | 快速修复 | 显示建议和修复 |
| `Ctrl + Q` | 快速文档 | 显示方法文档 |
| `Ctrl + P` | 参数信息 | 显示方法参数 |

---

## 🔧 故障排除

### 问题1：端口8080被占用

**错误信息：**
```
Port 8080 is already in use
```

**解决方法A：通过IDEA停止**
1. 点击运行窗口的停止按钮 ⏹️
2. 或按 `Ctrl + F2` 停止所有运行

**解决方法B：通过终端停止**
1. 打开IDEA终端（`Alt + F12`）
2. 执行命令：
```powershell
# 查找占用8080端口的进程
netstat -ano | findstr ":8080"

# 停止该进程（替换<PID>为实际进程ID）
taskkill /F /PID <PID>

# 或停止所有Java进程
Get-Process -Name java | Stop-Process -Force
```

**解决方法C：修改端口**
1. 打开 `src/main/resources/application.properties`
2. 添加或修改：
```properties
server.port=8081
```
3. 重新启动应用

### 问题2：Maven依赖下载失败

**现象：**
- 红色波浪线提示类找不到
- 编译错误

**解决方法：**
1. **配置Maven镜像（使用阿里云）**
   - `Settings` → `Build, Execution, Deployment` → `Build Tools` → `Maven`
   - 修改 User settings file 指向 Maven 的 settings.xml
   - 在 settings.xml 中添加阿里云镜像：
   ```xml
   <mirror>
       <id>aliyun</id>
       <mirrorOf>central</mirrorOf>
       <name>Aliyun Maven</name>
       <url>https://maven.aliyun.com/repository/public</url>
   </mirror>
   ```

2. **重新导入Maven项目**
   - 右键 `pom.xml` → `Maven` → `Reload project`
   - 或点击 Maven 窗口的刷新按钮

3. **清理并重新构建**
   - Maven 窗口：`Lifecycle` → `clean` 双击
   - 然后 `Lifecycle` → `install` 双击

### 问题3：JDK版本不匹配

**错误信息：**
```
java: invalid source release: 11
```

**解决方法：**
1. **检查项目JDK**
   - `Ctrl + Alt + Shift + S` → `Project`
   - 确保 SDK 选择 JDK 11 或更高
   - Project language level: 11

2. **检查模块JDK**
   - 同一窗口 → `Modules` → `JtSpringProject`
   - Language level: 11

3. **检查Java编译器**
   - `Settings` → `Build, Execution, Deployment` → `Compiler` → `Java Compiler`
   - Project bytecode version: 11

### 问题4：数据库连接失败

**错误信息：**
```
Unable to create requested service [org.hibernate.engine.jdbc.env.spi.JdbcEnvironment]
```

**解决方法：**
1. **检查H2数据库文件**
   - 确保 `data/ecommjava.mv.db` 存在
   - 如果不存在，应用会自动创建

2. **检查数据库配置**
   - 打开 `src/main/resources/application.properties`
   - 确认数据源配置正确：
   ```properties
   spring.datasource.url=jdbc:h2:file:./data/ecommjava
   spring.datasource.username=sa
   spring.datasource.password=
   ```

### 问题5：代码提示不工作

**解决方法：**
1. **重建索引**
   - `File` → `Invalidate Caches` → 勾选 "Invalidate and Restart"

2. **检查Power Save Mode**
   - 确保右下角没有 ⚡ 图标
   - 如果有，点击取消省电模式

---

## 📝 启动检查清单

启动前请确认：

- [ ] JDK已正确配置（JDK 11 或 JDK 21）
- [ ] Maven依赖已全部下载完成
- [ ] 8080端口未被占用
- [ ] 项目已完成索引（右下角无进度条）
- [ ] 没有编译错误（代码无红色波浪线）

---

## 🌐 访问地址

启动成功后访问以下地址：

- **首页**: http://localhost:8080
- **管理员登录**: http://localhost:8080/admin/login
- **用户登录**: http://localhost:8080/user/login
- **H2控制台**: http://localhost:8080/h2-console

---

## 💡 小技巧

1. **快速查看方法文档**
   - 鼠标悬停在方法上
   - 或按 `Ctrl + Q`

2. **快速修复错误**
   - 光标移到红色波浪线
   - 按 `Alt + Enter` 查看建议

3. **多光标编辑**
   - 按住 `Alt` 点击多个位置
   - 或 `Ctrl + Ctrl(按住)` + ↑/↓

4. **代码模板**
   - 输入 `sout` + `Tab` → `System.out.println()`
   - 输入 `psvm` + `Tab` → `public static void main`
   - 输入 `fori` + `Tab` → `for` 循环

5. **查看最近修改**
   - `Alt + Shift + C` 查看最近的更改

---

## 🎓 学习资源

- **IDEA官方文档**: https://www.jetbrains.com/idea/documentation/
- **快捷键PDF**: `Help` → `Keyboard Shortcuts PDF`
- **提示技巧**: `Help` → `Tip of the Day`

---

**祝您使用愉快！** 🎉

如有问题，请查看项目的其他文档：
- `IDEA_启动指南.md` - 简化版启动指南
- `启动问题解决.md` - 常见问题汇总
- `TESTING_GUIDE.md` - 测试指南

