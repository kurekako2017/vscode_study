# IntelliJ IDEA 完整操作指南 🚀

> 适合 IDEA 新手的详细操作手册 - 从零开始学习 IDEA

---

## 📑 目录

- [第一部分：基础入门](#第一部分基础入门)
  - [1. 打开和导入项目](#1-打开和导入项目)
  - [2. IDEA 界面介绍](#2-idea-界面介绍)
  - [3. 启动项目](#3-启动项目)
- [第二部分：常用快捷键](#第二部分常用快捷键)
- [第三部分：日常开发操作](#第三部分日常开发操作)
- [第四部分：调试技巧](#第四部分调试技巧)
- [第五部分：Maven 操作](#第五部分maven-操作)
- [第六部分：常见问题解决](#第六部分常见问题解决)

---

## 第一部分：基础入门

### 1. 打开和导入项目

#### 方法一：直接打开已有项目（最简单）

1. **启动 IntelliJ IDEA**
   - 双击桌面图标或从开始菜单启动

2. **打开项目**
   - 在欢迎界面点击 **`Open`** 按钮
   - 或者：`File` → `Open...`
   
3. **选择项目文件夹**
   ```
   D:\dev\source_code\vscode_study\java-projects\JtProject
   ```
   - ⚠️ 注意：选择包含 `pom.xml` 的根目录
   - 点击 **`OK`** 确认

4. **等待 Maven 导入**
   - 右下角会显示进度条：`Importing...`
   - 首次导入可能需要 3-5 分钟（下载依赖包）
   - 看到 `Build Successful` 即表示导入完成

#### 检查项目是否正确加载

- 左侧 **Project** 面板应该显示项目结构
- `src/main/java` 文件夹图标是蓝色（表示源代码目录）
- 右下角没有红色错误提示

---

### 2. IDEA 界面介绍

```
┌─────────────────────────────────────────────────────────────┐
│  文件菜单栏 (File, Edit, View...)                            │
├─────────────────────────────────────────────────────────────┤
│  工具栏 (运行▶, 调试🐛, 构建🔨...)                            │
├──────────┬──────────────────────────────────┬───────────────┤
│          │                                  │               │
│  项目    │        代码编辑区                 │   Maven       │
│  结构    │      (主工作区域)                │   工具窗口     │
│  树      │                                  │               │
│  (左侧)  │                                  │   (右侧)      │
│          │                                  │               │
├──────────┴──────────────────────────────────┴───────────────┤
│  底部工具栏 (Terminal, Run, Debug, TODO...)                 │
└─────────────────────────────────────────────────────────────┘
```

#### 重要区域说明

| 区域 | 说明 | 快捷键 |
|------|------|--------|
| **Project 面板** | 显示项目文件树 | `Alt + 1` |
| **编辑区** | 编写代码的主区域 | - |
| **Run 窗口** | 显示程序运行输出 | `Alt + 4` |
| **Debug 窗口** | 调试时的变量查看 | `Alt + 5` |
| **Terminal 窗口** | 命令行终端 | `Alt + F12` |
| **Maven 窗口** | Maven 项目管理 | 点击右侧 Maven 标签 |

---

### 3. 启动项目

#### 方法一：使用运行按钮（最简单）✨

1. **找到主类文件**
   ```
   src/main/java/com/jtspringproject/JtSpringProject/JtSpringProjectApplication.java
   ```
   - 在左侧 Project 面板中展开文件夹
   - 双击打开文件

2. **点击运行按钮**
   - 在 `main` 方法左侧有一个 **绿色▶三角形**
   - 点击它，选择 **`Run 'JtSpringProjectApplication.main()'`**

3. **等待启动**
   - 底部会弹出 **Run** 窗口显示日志
   - 看到 `Started JtSpringProjectApplication` 表示启动成功
   - 访问：http://localhost:8080

#### 方法二：使用快捷键（推荐）⚡

1. **打开主类文件** (同上)
2. **按快捷键**：
   - 运行：`Shift + F10`
   - 调试：`Shift + F9`

#### 方法三：使用 Maven 命令

1. **打开 Terminal**：按 `Alt + F12`
2. **输入命令**：
   ```bash
   mvn spring-boot:run -Dmaven.test.skip=true
   ```
3. **按回车运行**

---

## 第二部分：常用快捷键

### ⭐ 最常用快捷键（必记）

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **运行程序** | `Shift + F10` | `Ctrl + R` | 运行当前配置 |
| **调试程序** | `Shift + F9` | `Ctrl + D` | 以调试模式运行 |
| **停止程序** | `Ctrl + F2` | `Cmd + F2` | 停止运行中的程序 |
| **保存全部** | `Ctrl + S` | `Cmd + S` | 保存所有文件 |
| **查找类** | `Ctrl + N` | `Cmd + O` | 快速打开类文件 |
| **查找文件** | `Ctrl + Shift + N` | `Cmd + Shift + O` | 快速打开任意文件 |
| **全局搜索** | `Ctrl + Shift + F` | `Cmd + Shift + F` | 在整个项目中搜索 |

---

### 📝 代码编辑快捷键

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **复制当前行** | `Ctrl + D` | `Cmd + D` | 向下复制一行 |
| **删除当前行** | `Ctrl + Y` | `Cmd + Delete` | 删除光标所在行 |
| **上下移动行** | `Alt + Shift + ↑/↓` | `Option + Shift + ↑/↓` | 移动代码行 |
| **格式化代码** | `Ctrl + Alt + L` | `Cmd + Option + L` | 自动格式化 |
| **优化导入** | `Ctrl + Alt + O` | `Cmd + Option + O` | 删除未使用的import |
| **行注释** | `Ctrl + /` | `Cmd + /` | 单行注释/取消注释 |
| **块注释** | `Ctrl + Shift + /` | `Cmd + Shift + /` | 多行注释 |
| **自动补全** | `Ctrl + Space` | `Ctrl + Space` | 代码提示 |
| **智能补全** | `Ctrl + Shift + Space` | `Ctrl + Shift + Space` | 智能类型匹配 |
| **参数提示** | `Ctrl + P` | `Cmd + P` | 显示方法参数 |
| **快速修复** | `Alt + Enter` | `Option + Enter` | 显示修复建议 |

---

### 🔍 代码导航快捷键

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **跳转到定义** | `Ctrl + B` 或 `Ctrl + 左键` | `Cmd + B` | 查看方法/类定义 |
| **返回上一位置** | `Ctrl + Alt + ←` | `Cmd + [` | 后退 |
| **前进到下一位置** | `Ctrl + Alt + →` | `Cmd + ]` | 前进 |
| **查看类结构** | `Ctrl + F12` | `Cmd + F12` | 查看类的所有方法 |
| **最近文件** | `Ctrl + E` | `Cmd + E` | 打开最近编辑的文件 |
| **查找用途** | `Alt + F7` | `Option + F7` | 查找哪里使用了这个方法 |
| **跳转到行** | `Ctrl + G` | `Cmd + L` | 跳转到指定行号 |
| **查看继承关系** | `Ctrl + H` | `Ctrl + H` | 查看类层次结构 |

---

### 🐛 调试快捷键

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **设置/取消断点** | `Ctrl + F8` | `Cmd + F8` | 在当前行设置断点 |
| **单步跳过** | `F8` | `F8` | 执行下一行，不进入方法 |
| **单步进入** | `F7` | `F7` | 进入方法内部 |
| **单步跳出** | `Shift + F8` | `Shift + F8` | 跳出当前方法 |
| **继续运行** | `F9` | `Cmd + Option + R` | 运行到下一个断点 |
| **运行到光标** | `Alt + F9` | `Option + F9` | 运行到光标所在行 |
| **计算表达式** | `Alt + F8` | `Option + F8` | 在调试时计算变量 |
| **查看变量** | 鼠标悬停 | 鼠标悬停 | 查看变量当前值 |

---

### 🔧 重构快捷键

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **重命名** | `Shift + F6` | `Shift + F6` | 重命名变量/方法/类 |
| **提取变量** | `Ctrl + Alt + V` | `Cmd + Option + V` | 将表达式提取为变量 |
| **提取方法** | `Ctrl + Alt + M` | `Cmd + Option + M` | 将代码提取为方法 |
| **重构菜单** | `Ctrl + Alt + Shift + T` | `Ctrl + T` | 显示所有重构选项 |

---

### 🪟 窗口管理快捷键

| 功能 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| **项目面板** | `Alt + 1` | `Cmd + 1` | 打开/关闭项目树 |
| **Run 窗口** | `Alt + 4` | `Cmd + 4` | 打开运行窗口 |
| **Debug 窗口** | `Alt + 5` | `Cmd + 5` | 打开调试窗口 |
| **Terminal** | `Alt + F12` | `Option + F12` | 打开终端 |
| **隐藏所有窗口** | `Ctrl + Shift + F12` | `Cmd + Shift + F12` | 最大化编辑区 |

---

## 第三部分：日常开发操作

### 📄 文件操作

#### 创建新文件
1. **右键点击** 目标文件夹（如 `src/main/java/com/...`）
2. 选择 **`New`**：
   - `Java Class` - 创建类
   - `Package` - 创建包
   - `File` - 创建其他文件

#### 删除文件
1. 选中文件
2. 按 **`Delete`** 键
3. 确认删除

#### 重命名文件
1. 选中文件
2. 按 **`Shift + F6`**
3. 输入新名称
4. 按回车确认

---

### 📦 代码生成

#### 自动生成 Getter/Setter
1. 在类中右键点击
2. 选择 **`Generate...`** 或按 **`Alt + Insert`**
3. 选择 `Getter and Setter`
4. 选择要生成的字段

#### 自动生成构造方法
1. 右键 → **`Generate...`** (或 `Alt + Insert`)
2. 选择 `Constructor`
3. 选择要包含的字段

#### 自动 Override 方法
1. 右键 → **`Generate...`** (或 `Alt + Insert`)
2. 选择 `Override Methods...`
3. 选择要重写的方法

---

### 🔎 查找和替换

#### 当前文件中查找
- 查找：`Ctrl + F`
- 替换：`Ctrl + R`

#### 全局查找
- 查找：`Ctrl + Shift + F`
- 替换：`Ctrl + Shift + R`

#### 查找类
- 按 `Ctrl + N`，输入类名

#### 查找文件
- 按 `Ctrl + Shift + N`，输入文件名

#### 查找所有
- 按 `Shift + Shift`（双击Shift），搜索任何内容

---

### ✏️ 代码编辑技巧

#### 多行编辑
1. 按住 `Alt` 键
2. 用鼠标拖动选择多行
3. 同时编辑多行

#### 列选择模式
1. 按 `Alt + Shift + Insert` 切换到列模式
2. 可以竖向选择文本

#### 代码折叠/展开
- 折叠当前块：`Ctrl + -`
- 展开当前块：`Ctrl + +`
- 折叠全部：`Ctrl + Shift + -`
- 展开全部：`Ctrl + Shift + +`

---

## 第四部分：调试技巧

### 🐛 如何调试程序

#### 步骤1：设置断点
1. 在代码行号左侧 **单击**
2. 出现红色圆点 🔴 表示断点已设置
3. 再次单击可取消断点

#### 步骤2：启动调试
1. 点击工具栏的 **🐛 Debug** 按钮
2. 或按快捷键 **`Shift + F9`**
3. 程序会在断点处暂停

#### 步骤3：查看变量
- 在 **Variables** 面板查看所有变量值
- 鼠标悬停在代码上查看变量
- 右键变量选择 `Evaluate Expression` 计算值

#### 步骤4：单步调试
- **F8** - 单步跳过（执行下一行，不进入方法）
- **F7** - 单步进入（进入方法内部查看）
- **Shift + F8** - 单步跳出（跳出当前方法）
- **F9** - 继续运行到下一个断点

---

### 🎯 高级调试技巧

#### 条件断点
1. 右键点击断点（红色圆点）
2. 选择 **`More...`** 或 **`Condition`**
3. 输入条件，如：`i == 5`
4. 只有满足条件时才会暂停

#### 临时断点
1. 按 `Ctrl + Alt + Shift + F8`
2. 或右键断点选择 `One-time`
3. 只触发一次就自动删除

#### 查看调用栈
- 在 **Frames** 面板查看方法调用链
- 双击某个帧可跳转到对应代码

#### 计算表达式
1. 在调试时按 **`Alt + F8`**
2. 输入表达式（如 `user.getName()`）
3. 查看计算结果

---

## 第五部分：Maven 操作

### 📦 使用 Maven 面板

#### 打开 Maven 面板
1. 点击右侧的 **`Maven`** 标签
2. 或通过 `View` → `Tool Windows` → `Maven`

#### Maven 生命周期
```
JtSpringProject
├── Lifecycle
│   ├── clean          ← 清理编译文件
│   ├── validate
│   ├── compile        ← 编译代码
│   ├── test           ← 运行测试
│   ├── package        ← 打包成 JAR
│   ├── verify
│   ├── install        ← 安装到本地仓库
│   └── deploy
└── Plugins
```

#### 常用操作
1. **清理项目**
   - 双击 `clean`
   
2. **编译项目**
   - 双击 `compile`
   
3. **打包项目**
   - 点击工具栏的 `m` 图标（跳过测试）
   - 双击 `package`
   
4. **刷新 Maven 项目**
   - 点击刷新图标 🔄

---

### 🔧 Maven 常用命令（Terminal）

打开 Terminal（`Alt + F12`），输入以下命令：

```bash
# 清理编译
mvn clean

# 编译项目
mvn compile

# 运行测试
mvn test

# 打包（跳过测试）
mvn package -Dmaven.test.skip=true

# 清理并打包
mvn clean package -Dmaven.test.skip=true

# 运行 Spring Boot 应用
mvn spring-boot:run

# 运行（跳过测试）
mvn spring-boot:run -Dmaven.test.skip=true

# 查看依赖树
mvn dependency:tree

# 更新依赖
mvn clean install -U
```

---

## 第六部分：常见问题解决

### ❌ 项目导入后有红色错误

**原因**：JDK 未配置或 Maven 依赖未下载

**解决方案**：
1. 配置 JDK：
   - `File` → `Project Structure...` (`Ctrl + Alt + Shift + S`)
   - 选择 `Project` → 设置 `Project SDK` 为 `Java 11`
   
2. 重新导入 Maven：
   - 右键点击 `pom.xml`
   - 选择 `Maven` → `Reload Project`

---

### ❌ 运行按钮是灰色的

**原因**：没有配置运行配置

**解决方案**：
1. 打开主类文件 `JtSpringProjectApplication.java`
2. 右键点击 `main` 方法
3. 选择 `Run 'JtSpringProjectApplication.main()'`

---

### ❌ 端口 8080 已被占用

**解决方案1**：修改端口
1. 打开 `src/main/resources/application.properties`
2. 添加：
   ```properties
   server.port=8081
   ```

**解决方案2**：停止占用端口的进程
1. 打开 Terminal（`Alt + F12`）
2. Windows 执行：
   ```powershell
   netstat -ano | findstr :8080
   Stop-Process -Id <进程ID> -Force
   ```

---

### ❌ Maven 依赖下载失败

**解决方案**：
1. 检查网络连接
2. 配置国内镜像（阿里云）：
   - 打开 Maven 设置文件 `~/.m2/settings.xml`
   - 添加镜像配置：
   ```xml
   <mirror>
     <id>aliyun</id>
     <mirrorOf>central</mirrorOf>
     <url>https://maven.aliyun.com/repository/public</url>
   </mirror>
   ```
3. 重新下载依赖：
   ```bash
   mvn clean install -U
   ```

---

### ❌ 代码无法自动提示

**解决方案**：
1. **清除缓存**：
   - `File` → `Invalidate Caches...`
   - 选择 `Invalidate and Restart`

2. **检查索引**：
   - 等待右下角索引完成
   - 看到 `Indexing...` 时请耐心等待

---

## 🎓 学习建议

### 初学者学习路径

#### 第1天：基础操作
- [ ] 学会打开项目
- [ ] 学会运行程序（`Shift + F10`）
- [ ] 学会停止程序（`Ctrl + F2`）
- [ ] 学会保存文件（`Ctrl + S`）

#### 第2天：代码编辑
- [ ] 学会复制/删除行（`Ctrl + D` / `Ctrl + Y`）
- [ ] 学会格式化代码（`Ctrl + Alt + L`）
- [ ] 学会行注释（`Ctrl + /`）
- [ ] 学会查找类（`Ctrl + N`）

#### 第3天：代码导航
- [ ] 学会跳转到定义（`Ctrl + B`）
- [ ] 学会返回上一位置（`Ctrl + Alt + ←`）
- [ ] 学会查看类结构（`Ctrl + F12`）
- [ ] 学会最近文件（`Ctrl + E`）

#### 第4天：调试技能
- [ ] 学会设置断点（点击行号）
- [ ] 学会启动调试（`Shift + F9`）
- [ ] 学会单步调试（`F8`, `F7`, `F9`）
- [ ] 学会查看变量值

#### 第5天：Maven 操作
- [ ] 学会使用 Maven 面板
- [ ] 学会打包项目
- [ ] 学会使用 Terminal 命令

---

## 🌟 常用操作速查表

### 一分钟启动项目
```
1. File → Open → 选择项目文件夹
2. 等待 Maven 导入完成
3. 打开 JtSpringProjectApplication.java
4. 点击 main 方法旁的绿色▶
5. 访问 http://localhost:8080
```

### 每天开发流程
```
1. 打开 IDEA，自动打开上次项目
2. Ctrl + E - 打开最近文件
3. 编写代码
4. Ctrl + Alt + L - 格式化代码
5. Shift + F10 - 运行测试
6. Ctrl + S - 保存
7. Git 提交（后续学习）
```

### 遇到问题时
```
1. Alt + Enter - 查看快速修复建议
2. Ctrl + F1 - 查看错误详情
3. Alt + F7 - 查找用途
4. Ctrl + Shift + F - 全局搜索
```

---

## 📚 推荐资源

1. **IDEA 官方文档**：https://www.jetbrains.com/help/idea/
2. **IDEA 快捷键 PDF**：`Help` → `Keyboard Shortcuts PDF`
3. **IDEA 学习插件**：`IDE Features Trainer`（内置）

---

## 💡 实用技巧

### 提高效率的小技巧

1. **使用双击 Shift**
   - 可以搜索任何内容：类、文件、设置、操作

2. **使用 TODO 注释**
   ```java
   // TODO: 这里需要实现
   ```
   - 可在 `View` → `Tool Windows` → `TODO` 查看所有待办

3. **使用 Live Templates**
   - 输入 `sout` 然后按 `Tab` → `System.out.println()`
   - 输入 `psvm` 然后按 `Tab` → `public static void main`

4. **代码模板**
   - `fori` + `Tab` → for 循环
   - `ifn` + `Tab` → if null 判断
   - `inn` + `Tab` → if not null 判断

5. **多光标编辑**
   - `Alt` + 鼠标点击 → 添加多个光标
   - 同时编辑多处

---

## ✅ 本项目快速启动

### JtProject 专用启动步骤

1. **打开项目**
   ```
   File → Open → D:\dev\source_code\vscode_study\java-projects\JtProject
   ```

2. **等待 Maven 导入**（首次约 3-5 分钟）

3. **运行项目**（三种方式任选）
   - ✨ **方式1**：打开 `JtSpringProjectApplication.java`，点击 main 方法旁的绿色▶
   - ⚡ **方式2**：按 `Shift + F10`
   - 🔧 **方式3**：Terminal 执行 `mvn spring-boot:run -Dmaven.test.skip=true`

4. **访问应用**
   ```
   http://localhost:8080
   
   管理员：admin / 123
   用户：lisa / 765
   ```

5. **停止应用**
   - 点击红色停止按钮 ⬛
   - 或按 `Ctrl + F2`

---

## 🎯 总结

**必记的 5 个快捷键：**
1. `Shift + F10` - 运行
2. `Ctrl + F2` - 停止
3. `Ctrl + Alt + L` - 格式化代码
4. `Ctrl + /` - 注释
5. `Ctrl + N` - 查找类

**每天必做的操作：**
1. 运行程序测试
2. 格式化代码
3. 保存文件

**遇到问题先尝试：**
1. `Alt + Enter` - 查看建议
2. `File` → `Invalidate Caches...` - 清除缓存
3. Maven 面板点刷新 🔄

---

> 💪 **记住**：熟能生巧！多用快捷键，少用鼠标，效率会越来越高！

> 📖 **提示**：可以打印 `Help` → `Keyboard Shortcuts PDF` 放在手边随时查看

> 🚀 **祝您学习愉快！**

