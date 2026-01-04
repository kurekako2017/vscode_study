# 🚀 手动启动项目完整指南 - IntelliJ IDEA

> **针对IDEA新手的详细启动教程，每一步都有截图说明位置**

---

## 📋 目录
- [准备工作](#准备工作)
- [方案1：使用主类启动（最简单）](#方案1使用主类启动最简单)
- [方案2：使用Maven启动](#方案2使用maven启动)
- [方案3：使用运行配置启动](#方案3使用运行配置启动)
- [验证启动成功](#验证启动成功)
- [常见启动失败及解决](#常见启动失败及解决)

---

## 准备工作

### 1. 确认项目已正确打开

**位置说明**：
- 看IDEA窗口**左侧**，有一个项目结构面板
- 应该能看到 `JtProject` 文件夹
- 文件夹下面有 `src`、`pom.xml` 等文件

**如果没有看到**：
1. 点击顶部菜单：`File` → `Open`
2. 选择：`D:\dev\source_code\vscode_study\java-projects\JtProject`
3. 点击 `OK`

### 2. 等待Maven依赖下载完成

**位置说明**：
- 看IDEA窗口**右下角**
- 如果有进度条在转，说明正在下载依赖
- **必须等待进度条消失**后再继续

**如果进度条一直不消失**：
1. 看右下角是否有错误提示
2. 点击右侧边栏的 `Maven` 标签（竖着的）
3. 点击刷新图标（两个箭头组成的圆圈）

### 3. 确认JDK已配置

按快捷键：`Ctrl + Alt + Shift + S`
- 左侧选择 `Project`
- 右侧 `Project SDK` 应该显示 JDK 11 或更高版本
- 如果显示 `<No SDK>`，点击下拉框选择或下载JDK

---

## 方案1：使用主类启动（最简单）⭐

### 步骤1：找到主类文件

#### 方法A：使用快捷键查找（推荐）
1. 按快捷键：`Ctrl + N`（查找类）
2. 在弹出的搜索框中输入：`JtSpringProjectApplication`
3. 看到匹配结果后，按 `Enter` 键

#### 方法B：手动导航
1. 在左侧项目面板中，找到并展开：
   ```
   JtProject
   └── src
       └── main
           └── java
               └── com
                   └── jtspringproject
                       └── JtSpringProject
                           └── JtSpringProjectApplication.java  ← 点击这个
   ```

### 步骤2：打开文件

- 文件应该在编辑器中打开了
- 你会看到代码，其中有一行：
  ```java
  public class JtSpringProjectApplication {
  ```

### 步骤3：运行主类

**方式A：使用右键菜单**
1. 在代码编辑器的**空白处**点击**右键**（不是在文字上）
2. 在弹出的菜单中找到：`Run 'JtSpringProjectApplication.main()'`
3. **点击它**

**方式B：使用快捷键（更快）**
1. 确保光标在 `JtSpringProjectApplication.java` 文件中
2. 按快捷键：`Shift + F10`

**方式C：使用顶部运行按钮**
1. 看IDEA窗口**顶部工具栏**（靠右的位置）
2. 找到一个**绿色的播放按钮** ▶️
3. **点击它**

### 步骤4：查看启动日志

**位置说明**：
- IDEA**底部**会自动弹出一个面板
- 标签页名称是：`Run` 或 `Run: JtSpringProjectApplication`
- 里面会滚动显示启动日志

**日志内容示例**：
```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::               (v2.7.18)

...
Started JtSpringProjectApplication in 5.234 seconds
========================================
JT电商系统启动成功！
访问地址: http://localhost:8080
========================================
```

**看到这些信息就说明启动成功了！** ✅

---

## 方案2：使用Maven启动

### 步骤1：打开Maven面板

**位置说明**：
- 看IDEA窗口**右侧边缘**
- 有一个竖着的标签：`Maven`
- **点击它**，Maven面板会展开

**如果找不到Maven标签**：
1. 点击顶部菜单：`View` → `Tool Windows` → `Maven`
2. 或按快捷键：`Alt + 1`，然后在项目面板底部找 Maven 标签

### 步骤2：找到spring-boot:run

在Maven面板中：
1. 找到 `JtSpringProject` 项目（最顶部）
2. **点击**左边的小三角，展开
3. 找到 `Plugins` 节点
4. **点击**左边的小三角，展开
5. 找到 `spring-boot` 节点
6. **点击**左边的小三角，展开
7. 看到 `spring-boot:run`

### 步骤3：运行

**双击** `spring-boot:run`

### 步骤4：查看日志

- 底部会弹出 `Run` 面板
- 显示启动日志
- 等待看到 "Started JtSpringProjectApplication" 即成功

---

## 方案3：使用运行配置启动

### 步骤1：创建运行配置

1. 点击顶部菜单：`Run` → `Edit Configurations...`
   - 或者点击顶部工具栏右侧的运行配置下拉框（显示运行配置名称的地方）
   - 然后点击 `Edit Configurations...`

### 步骤2：在配置对话框中操作

**对话框位置**：屏幕中央会弹出一个大窗口

#### 创建新配置：
1. 看对话框**左上角**
2. 点击 `+` 号按钮（添加新配置）
3. 在下拉列表中选择：`Application`

#### 填写配置信息：
在右侧表单中填写：

- **Name**（配置名称）：
  - 输入：`JtSpringProject`

- **Main class**（主类）：
  - 点击右边的三点按钮 `...`
  - 在搜索框中输入：`JtSpringProjectApplication`
  - 选中它，点击 `OK`
  - 或者直接输入：`com.jtspringproject.JtSpringProject.JtSpringProjectApplication`

- **Use classpath of module**（使用的模块）：
  - 下拉选择：`JtProject`

- **Working directory**（工作目录）：
  - 应该自动填充为：`D:\dev\source_code\vscode_study\java-projects\JtProject`
  - 如果没有，点击右边的文件夹图标，选择项目根目录

### 步骤3：保存配置

- 点击对话框底部的 `OK` 按钮（在右下角）
- **对话框会关闭**

### 步骤4：运行配置

**方式A：使用运行按钮**
1. 看顶部工具栏右侧
2. 运行配置下拉框现在应该显示：`JtSpringProject`
3. 点击旁边的绿色播放按钮 ▶️

**方式B：使用快捷键**
- 按：`Shift + F10`

### 步骤5：查看启动日志

- 底部弹出 `Run` 面板
- 查看日志，等待启动完成

---

## 验证启动成功

### 1. 查看日志输出

在 `Run` 面板中，向下滚动到最后，应该看到：

```
========================================
JT电商系统启动成功！
访问地址: http://localhost:8080
========================================
```

### 2. 查看端口状态

**在IDEA内置终端中检查**：
1. 按快捷键：`Alt + F12`（打开终端）
2. 输入命令：
   ```powershell
   netstat -ano | findstr :8080
   ```
3. 如果看到类似这样的输出，说明端口正在监听：
   ```
   TCP    0.0.0.0:8080    0.0.0.0:0    LISTENING    12345
   ```

### 3. 访问应用

1. 打开浏览器（Chrome、Edge、Firefox等）
2. 在地址栏输入：`http://localhost:8080`
3. 按回车键
4. **应该能看到登录页面** ✅

---

## 常见启动失败及解决

### ❌ 问题1：找不到主类

**错误信息**：
```
Error: Could not find or load main class com.jtspringproject.JtSpringProject.JtSpringProjectApplication
```

**解决方法**：
1. 右键点击 `pom.xml`
2. 选择：`Maven` → `Reload project`
3. 等待刷新完成
4. 重新运行

### ❌ 问题2：端口8080被占用

**错误信息**：
```
Web server failed to start. Port 8080 was already in use.
```

**解决方法A：停止占用端口的进程**
1. 按 `Alt + F12` 打开终端
2. 查找占用端口的进程：
   ```powershell
   netstat -ano | findstr :8080
   ```
3. 记下最后一列的进程ID（PID），例如：12345
4. 停止进程：
   ```powershell
   taskkill /F /PID 12345
   ```
5. 重新启动应用

**解决方法B：修改端口**
1. 打开 `application.properties` 文件
2. 添加一行：
   ```properties
   server.port=8081
   ```
3. 保存文件
4. 重新启动，访问：`http://localhost:8081`

### ❌ 问题3：Maven依赖下载失败

**错误信息**：
```
Could not resolve dependencies
```

**解决方法**：
1. 检查网络连接
2. 打开 `pom.xml`
3. 右键选择：`Maven` → `Reload project`
4. 如果还是失败，尝试配置国内Maven镜像：
   - 点击 `File` → `Settings`
   - 搜索：`Maven`
   - 配置阿里云镜像

### ❌ 问题4：数据库连接失败

**错误信息**：
```
Error creating bean with name 'sessionFactory'
```

**解决方法**：
1. 检查 `application.properties` 中的数据库配置
2. 确认使用H2数据库（嵌入式，不需要安装）：
   ```properties
   db.driver= org.h2.Driver
   db.url= jdbc:h2:file:./data/ecommjava
   ```
3. 确保项目目录下有 `data` 文件夹
4. 如果没有，手动创建：
   - 在项目根目录右键
   - 选择：`New` → `Directory`
   - 输入：`data`

### ❌ 问题5：JDK版本不匹配

**错误信息**：
```
Unsupported class file major version
```

**解决方法**：
1. 按 `Ctrl + Alt + Shift + S`
2. 选择 `Project`
3. `Project SDK` 选择 JDK 11 或更高
4. `Language level` 选择 11
5. 点击 `OK`
6. 重新运行

### ❌ 问题6：Run面板没有弹出

**解决方法**：
1. 点击顶部菜单：`View` → `Tool Windows` → `Run`
2. 或按快捷键：`Alt + 4`
3. Run面板会在底部显示

### ❌ 问题7：启动后立即停止

**可能原因**：main方法执行完就退出了

**解决方法**：
- 检查是否正确使用了 `SpringApplication.run()`
- 确保 `JtSpringProjectApplication` 类有 `@SpringBootApplication` 注解
- 查看日志中的错误信息

---

## 停止应用

### 方法1：使用停止按钮
1. 在 `Run` 面板顶部
2. 找到红色方块按钮 ⏹️
3. **点击它**

### 方法2：使用快捷键
- 按：`Ctrl + F2`
- 如果有多个运行中的应用，选择要停止的
- 按回车确认

### 方法3：强制停止
- 在 `Run` 面板顶部
- 找到红色骷髅头按钮 ☠️（Kill按钮）
- **点击它**（强制终止进程）

---

## 📝 启动检查清单

在启动前，确认以下事项：

- [ ] IDEA已打开JtProject项目
- [ ] 右下角没有进度条（Maven依赖已下载完成）
- [ ] JDK已正确配置（JDK 11+）
- [ ] 8080端口没有被占用
- [ ] `target` 目录下有编译好的 `.jar` 文件
- [ ] `application.properties` 配置正确
- [ ] 网络连接正常（首次启动需要下载依赖）

---

## 🎯 推荐的启动方式

**对于新手，推荐按此顺序尝试**：

1. **首选**：[方案1 - 使用主类启动](#方案1使用主类启动最简单)
   - 优点：最简单，最直接
   - 缺点：无

2. **备选**：[方案2 - 使用Maven启动](#方案2使用maven启动)
   - 优点：标准方式，适合学习
   - 缺点：需要找到Maven面板

3. **高级**：[方案3 - 使用运行配置](#方案3使用运行配置启动)
   - 优点：可以配置JVM参数、环境变量等
   - 缺点：配置稍复杂

---

## 💡 小贴士

### 启动速度优化
1. **首次启动慢是正常的**（需要下载依赖）
2. **后续启动会快很多**（3-10秒）
3. 使用 **Debug模式** 启动可以支持热更新

### 查看更详细的日志
在 `Run` 面板中：
- 右键点击日志区域
- 选择：`Clear All`（清空日志）
- 重新启动，日志会更清晰

### 使用Debug模式
- 右键主类 → `Debug 'JtSpringProjectApplication.main()'`
- 或按快捷键：`Shift + F9`
- 可以设置断点进行调试

---

**祝您成功启动项目！** 🎉

如果遇到问题，请查看：
- `Run` 面板中的错误信息
- 右下角的 `Event Log`（事件日志）
- 或参考 [IDEA操作完整指南-新手版.md](./IDEA操作完整指南-新手版.md)

