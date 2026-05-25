# IntelliJ IDEA 文档汇总中心

> **最后更新**: 2026年1月4日  
> **适用项目**: JtSpringProject (Spring Boot + Hibernate + JSP)  
> **快速导航**: 选择下方相应章节获取所需帮助

---

## 📑 文档导航

### 🚀 快速启动（新用户必读）
- [快速启动卡片](#快速启动卡片) - 3分钟快速上手
- [项目打开详解](#项目打开详解) - 如何打开项目
- [JDK 配置指南](#jdk-配置指南) - 配置开发环境

### 🔧 故障排除（遇到问题请看）
- [运行按钮问题](#运行按钮问题) - 右键没有运行按钮
- [启动问题完整方案](#启动问题完整方案) - 无法运行主类
- [常见问题解决](#常见问题解决) - 其他常见问题

### 📚 深度指南
- [快捷键大全](#快捷键大全) - 提高编码效率
- [黑色主题设置](#黑色主题设置) - 护眼主题配置
- [调试技巧](#调试技巧) - Debug 方法
- [Maven 操作](#maven-操作) - 依赖管理

### 🎯 功能教程
- [代码编辑](#代码编辑) - 代码编辑技巧
- [代码导航](#代码导航) - 在代码中快速跳转
- [生成代码](#生成代码) - 自动生成getter/setter

---

## 快速启动卡片

### 🚀 最快启动方式（3分钟）

#### 第1步：打开项目
```
File → Open → D:\dev\source_code\vscode_study\java-projects\JtProject
```
- 选择包含 `pom.xml` 的根文件夹
- 点击 `OK`

#### 第2步：等待Maven导入
```
右下角会显示: "Importing..." 或 "Indexing..."
首次约需2-5分钟（依赖网络速度）
完全导入后，右下角进度条消失
```

#### 第3步：运行应用
```
1. 打开: JtSpringProjectApplication.java
2. 点击 main 方法旁的 ▶ 绿色运行按钮
3. 选择: Run 'JtSpringProjectApplication.main()'
4. 等待启动完成
```

#### 第4步：访问应用
```
浏览器访问: http://localhost:8080
用户名: lisa
密码: 765
```

---

## 项目打开详解

### 方法1：从欢迎界面打开（推荐首次）

1. **启动IDEA**
   - 双击桌面 IntelliJ IDEA 图标

2. **看到欢迎界面**
   - 点击 `Open` 按钮（左下角或中间）

3. **选择项目**
   ```
   导航到: D:\dev\source_code\vscode_study\java-projects\JtProject
   只需单击选中 JtProject 文件夹（会高亮）
   不需要双击进入文件夹！
   点击对话框右下角 OK 按钮
   ```

4. **等待加载**
   - IDEA 自动检测 Maven 项目
   - 右下角显示 "Importing..." 或 "Indexing..."
   - 等待完成（不要中断）

### 方法2：已经打开项目时
```
File → Open...
或
Ctrl + O
```

### 方法3：从命令行
```powershell
cd D:\dev\source_code\vscode_study\java-projects\JtProject
idea .
```

---

## JDK 配置指南

### 快速检查

**快捷键**：`Ctrl + Alt + Shift + S` 打开项目结构

**检查项目是否有JDK**：
- 左侧选择 `Project`
- 右侧 `SDK:` 字段
  - ✅ 正常：显示 `11` 或 `17` 或 `21`
  - ❌ 异常：显示 `<No SDK>` 或空白

### 配置JDK（如果没有）

#### 方法A：下载JDK（推荐）
```
1. Ctrl + Alt + Shift + S 打开项目结构
2. Project → SDK 下拉框
3. 点击 "Add SDK" → "Download JDK..."
4. 选择：
   - Version: 11 或 17
   - Vendor: Eclipse Temurin
5. 点击 Download
6. 下载完成后点 OK
```

#### 方法B：使用本地JDK
```
1. Ctrl + Alt + Shift + S 打开项目结构
2. Project → SDK 下拉框
3. 点击 "Add SDK" → "JDK"
4. 选择本地JDK安装目录
5. 点击 OK
```

### 配置Language Level

```
1. Ctrl + Alt + Shift + S 打开项目结构
2. Project → Language level
3. 选择: 11 或更高
4. 点击 OK
```

### 配置模块SDK

```
1. Ctrl + Alt + Shift + S 打开项目结构
2. 左侧 Modules
3. 选择 JtProject 模块
4. Module SDK: 确保选择了JDK 11或更高
5. 点击 OK
```

---

## 运行按钮问题

### 症状1：右键没有运行按钮

**现象**：
- 右键点击代码，没有 `Run` 选项
- main 方法旁边没有绿色运行箭头 ▶️

**快速解决**（大多数情况下有效）：

#### 步骤1：重新导入Maven
```
1. 右键点击 pom.xml
2. 选择 Maven → Reload project
3. 等待导入完成
```

#### 步骤2：刷新Maven
```
1. 右侧打开 Maven 工具窗口
   (如果没有: Ctrl + E 搜索 Maven)
2. 点击顶部刷新按钮 🔄
3. 等待完成
```

#### 步骤3：重启IDEA
```
1. 关闭IDEA
2. 重新打开项目
```

### 症状2：绿色运行按钮是灰色的

**现象**：
- 顶部工具栏的绿色播放按钮无反应
- 或右键有 Run 选项，但无法执行

**解决方案**：
```
1. Ctrl + Alt + Shift + S 打开项目结构
2. 检查 Project SDK 是否配置
3. 如果没有，按上面的 JDK配置指南 配置
4. 点击 OK 保存
```

---

## 启动问题完整方案

### 问题诊断

**第一步：检查项目识别**

打开左侧项目面板，查看图标：
- ✅ 正常：`JtProject` 文件夹有 Maven 图标（m字母）
- ❌ 异常：`JtProject` 只是普通文件夹图标

**第二步：检查pom.xml**
- ✅ 正常：`pom.xml` 有 Maven 图标
- ❌ 异常：`pom.xml` 是普通 XML 文件图标

**第三步：检查右下角**
- ❌ 如果有进度条转圈，说明索引未完成（等待）
- ❌ 如果有红色错误，查看错误信息

### 方案1：重新导入Maven项目（最常用）⭐

#### 步骤1：打开Maven面板
```
1. 按 Ctrl + E
2. 输入 "maven"
3. 点击 Maven 选项打开工具窗口
```

如果工具窗口已在右侧，直接点击 `Maven` 标签

#### 步骤2：刷新Maven项目
```
1. 在Maven面板中找到 JtSpringProject
2. 点击面板顶部的刷新按钮（蓝色双箭头）
3. 等待刷新完成
```

#### 步骤3：重新导入
```
1. 右键点击 pom.xml
2. Maven → Reload project
3. 等待导入完成
```

### 方案2：清除缓存并重启

```
1. File → Invalidate Caches...
2. 勾选：
   ☑ Invalidate and Restart
   ☑ Clear file system cache and Local History
   ☑ Clear downloaded shared indexes
3. 点击 Invalidate and Restart
4. IDEA自动重启
5. 等待重新索引完成（可能需要2-5分钟）
```

### 方案3：重新标记源代码目录

```
1. 左侧项目面板，导航到 src/main/java
2. 右键点击 java 文件夹
3. Mark Directory as → Sources Root
4. 文件夹应该变成蓝色

对于测试目录：
1. 右键点击 src/test/java
2. Mark Directory as → Test Sources Root
3. 文件夹应该变成绿色
```

### 方案4：手动创建运行配置

**步骤1：打开运行配置**
```
Run → Edit Configurations...
或
点击顶部工具栏右侧运行配置下拉框 → Edit Configurations...
```

**步骤2：添加新配置**
```
1. 点击左上角 + 按钮
2. 选择 Application
```

**步骤3：填写配置**
```
Name: JtSpringProject

Main class: 
  com.jtspringproject.JtSpringProject.JtSpringProjectApplication

Use classpath of module: JtProject

Working directory: $MODULE_WORKING_DIR$

JDK: 选择 JDK 11 或更高
```

**步骤4：保存并运行**
```
1. 点击 OK 保存
2. 顶部工具栏应该显示配置名称
3. 点击旁边的绿色播放按钮 ▶️
```

---

## 常见问题解决

### Q1：编译出错，出现红色波浪线

**原因**：Maven 依赖未下载完成或 JDK 配置不正确

**解决**：
```
1. 检查网络连接
2. File → Invalidate Caches → Invalidate and Restart
3. 右侧 Maven 工具窗口点击刷新按钮
4. 等待下载完成
```

### Q2：项目打开很慢

**原因**：首次导入需要下载所有 Maven 依赖，或 IDEA 在索引

**解决**：
```
耐心等待，这是正常的。
首次可能需要5-10分钟。
可以查看右下角的进度。
```

### Q3：端口8080被占用

**原因**：之前的应用没有完全停止

**解决**：
```powershell
# 查看占用8080的进程
netstat -ano | findstr :8080

# 停止进程（PID为查找到的进程ID）
Stop-Process -Id <PID> -Force

# 或在IDEA中点击 Stop 按钮（红色方块）
```

### Q4：MySQL连接失败

**错误信息**：`Connection refused` 或 `Can't connect to MySQL`

**解决**：
```
1. 确保 MySQL 服务已启动
   Windows: 检查 Windows 服务中 MySQL80 的状态
   
2. 检查配置文件中的数据库地址
   文件: src/main/resources/application.properties
   确保地址是 192.168.10.2:3306
   
3. 如果无法连接到192.168.10.2，改为本地地址：
   db.url=jdbc:mysql://127.0.0.1:3306/ecommjava?useUnicode=true&characterEncoding=utf-8
```

### Q5："无法解析符号"错误

**原因**：项目结构配置不正确

**解决**：
```
1. Ctrl + Alt + Shift + S 打开项目结构
2. 检查 Project SDK 是否配置
3. 检查 Language level 是否为 11
4. 检查 src/main/java 是否标记为 Sources Root
5. 右键 pom.xml → Maven → Reload project
```

### Q6：调试时无法启动或断点不生效

**原因**：配置问题或调试配置不正确

**解决**：
```
1. Shift + F9 启动调试
2. 确保在 main 方法旁点击了红色圆点设置断点
3. 如果无法进入断点，清除缓存：
   File → Invalidate Caches → Invalidate and Restart
4. 重新启动调试
```

---

## 快捷键大全

### 快速启动
| 快捷键 | 功能 |
|--------|------|
| `Shift + F10` | 运行应用 |
| `Shift + F9` | 调试应用 |
| `Ctrl + F2` | 停止应用 |
| `Ctrl + F5` | 重新运行 |

### 调试步进
| 快捷键 | 功能 |
|--------|------|
| `F8` | 单步跳过（不进入函数） |
| `F7` | 单步进入（进入函数） |
| `Shift + F8` | 单步跳出（退出函数） |
| `F9` | 继续运行 |
| `Alt + F9` | 运行到光标处 |

### 代码导航
| 快捷键 | 功能 |
|--------|------|
| `Ctrl + N` | 搜索类 |
| `Ctrl + Shift + N` | 搜索文件 |
| `Ctrl + B` | 跳转到定义 |
| `Ctrl + Alt + B` | 跳转到实现 |
| `Ctrl + H` | 查看类层级 |
| `Ctrl + Alt + H` | 查看调用层级 |
| `Alt + F7` | 查找所有引用 |
| `Ctrl + E` | 最近打开的文件 |
| `Ctrl + Shift + E` | 最近编辑的位置 |

### 代码编辑
| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Space` | 基础代码补全 |
| `Ctrl + Shift + Space` | 智能补全 |
| `Alt + Enter` | 快速修复 |
| `Ctrl + Alt + L` | 格式化代码 |
| `Ctrl + Alt + O` | 优化导入 |
| `Ctrl + /` | 行注释 |
| `Ctrl + Shift + /` | 块注释 |
| `Ctrl + D` | 复制行 |
| `Ctrl + Y` | 删除行 |
| `Ctrl + Shift + U` | 切换大小写 |

### 重构
| 快捷键 | 功能 |
|--------|------|
| `Shift + F6` | 重命名 |
| `Ctrl + Alt + M` | 提取方法 |
| `Ctrl + Alt + V` | 提取变量 |
| `Ctrl + Alt + N` | 内联变量 |
| `Ctrl + Alt + Shift + T` | 打开重构菜单 |

### 搜索和替换
| 快捷键 | 功能 |
|--------|------|
| `Ctrl + F` | 当前文件搜索 |
| `Ctrl + H` | 全局搜索替换 |
| `Ctrl + Shift + F` | 全局搜索 |
| `Shift + Shift` | 搜索任何东西（超级搜索） |

### 窗口和视图
| 快捷键 | 功能 |
|--------|------|
| `Alt + 1` | 打开/关闭 Project 窗口 |
| `Alt + 2` | 打开/关闭 Favorites 窗口 |
| `Alt + 6` | 打开/关闭 Problems 窗口 |
| `Alt + 9` | 打开/关闭 Git 窗口 |
| `Ctrl + Shift + F12` | 最大化编辑区（隐藏所有工具窗口） |
| `Ctrl + Tab` | 在打开的文件间切换 |
| `Ctrl + W` | 关闭当前文件 |
| `Ctrl + F4` | 关闭当前文件 |

### 版本控制
| 快捷键 | 功能 |
|--------|------|
| `Ctrl + K` | 提交 |
| `Ctrl + Shift + K` | 推送 |
| `Ctrl + T` | 更新/Pull |

### 生成代码
| 快捷键 | 功能 |
|--------|------|
| `Alt + Insert` | 打开 Generate 菜单 |
| `Ctrl + O` | 重写方法 |
| `Ctrl + I` | 实现接口 |

### 其他实用快捷键
| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Alt + S` | 打开设置 |
| `Ctrl + Alt + Shift + S` | 打开项目结构 |
| `Ctrl + Q` | 查看文档（光标在代码上） |
| `Ctrl + P` | 显示方法参数 |
| `Ctrl + J` | 查看实时模板 |

---

## 黑色主题设置

### 快速方式

**快捷键**：
```
Ctrl + Alt + S  打开设置
输入: theme
选择: Darcula
点击: OK
```

### 菜单方式

```
1. File → Settings
2. 左侧: Appearance & Behavior → Appearance
3. Theme: 选择 Darcula（或其他深色主题）
4. 点击 Apply，再点击 OK
```

### 可选主题

| 主题名称 | 风格 | 特点 |
|---------|------|------|
| **Darcula** | 深灰 | 经典黑色，舒适护眼 ⭐推荐 |
| **High contrast** | 纯黑 | 高对比度，适合视力不好 |
| **IntelliJ Light** | 白色 | 亮色主题 |
| **Visual Studio Dark** | VS风格 | 深蓝主题 |

### 进阶设置 - 自定义颜色

#### 编辑器背景色
```
Ctrl + Alt + S
Editor → Color Scheme
选择基础方案（如 Darcula）
点击右边的 ⚙️
选择 Duplicate（创建副本）
输入新名称，如 "My Theme"
现在可以自由修改各种颜色
```

#### 常用颜色值
```
纯黑: #000000
深灰: #2B2B2B (Darcula默认)
深蓝: #1E1E2E
暗褐: #1a1a1a
```

#### 修改字体
```
Ctrl + Alt + S
Editor → Font
Font: JetBrains Mono / Consolas / Courier New
Size: 14-16
Line height: 1.2
```

---

## 调试技巧

### 设置断点

**添加断点**：
```
点击代码行号旁边的空白区域
会出现红色圆点 ●
```

**条件断点**：
```
右键点击断点（红色圆点）
选择 Edit Breakpoint...
输入条件，如: i > 5
```

**临时断点**：
```
Alt + Click 在行号旁
```

### 启动调试

```
Shift + F9  启动调试模式
应用会在第一个断点停下
```

### 常用调试操作

**单步跳过**（不进入函数）：
```
F8
```

**单步进入**（进入函数）：
```
F7
```

**单步跳出**（跳出当前函数）：
```
Shift + F8
```

**继续运行**（运行到下一个断点）：
```
F9
```

**运行到光标**：
```
Alt + F9
点击代码中要跳到的位置，然后按快捷键
```

### 查看变量

**Variables 面板**：
```
在调试模式下自动显示在底部窗口
显示当前作用域所有变量的值
```

**Watches（监视）**：
```
1. 在 Variables 面板右键点击变量
2. 选择 Add to Watches
3. 或直接输入表达式
```

**Evaluate（即时计算）**：
```
Alt + F8
可以执行任意Java代码
查看表达式的值
```

### 常见断点位置

在这些位置设置断点便于调试：

```java
// Controller 入口
public String userlogin() { ... }  // F8进入

// Service 业务逻辑
public Product getProduct(int id) { ... }

// DAO 数据操作
public List<Product> getAll() { ... }

// 循环内部
for (Product p : products) {
    // 设置条件断点: p.getId() == targetId
    ...
}
```

### 调试技巧总结

1. **快速定位问题**：在 Controller 设置断点，F8逐步调试
2. **查看对象内容**：悬停鼠标或在 Watches 中输入对象名
3. **跳过长循环**：使用"运行到光标"而不是逐步执行
4. **检查条件**：使用条件断点过滤特定场景
5. **调试动态代码**：在 Evaluate 窗口执行Java代码查看结果

---

## Maven 操作

### 使用 Maven 面板

**打开 Maven 工具窗口**：
```
Ctrl + E
输入: maven
点击 Maven 选项
```

或在右侧直接点击 `Maven` 标签

**常用操作**：

| 操作 | 步骤 |
|------|------|
| 清理编译 | 展开 Lifecycle → 双击 clean |
| 编译项目 | 展开 Lifecycle → 双击 compile |
| 打包应用 | 展开 Lifecycle → 双击 package（需跳过测试） |
| 刷新依赖 | 点击面板顶部的刷新按钮 🔄 |
| 展开依赖树 | Dependencies 标签查看所有依赖 |

### 在 Terminal 中运行 Maven 命令

**打开 Terminal**：
```
Alt + F12
或 View → Tool Windows → Terminal
```

**常用命令**：
```powershell
# 清理编译输出
mvn clean

# 编译项目
mvn compile

# 打包（跳过测试）
mvn package -Dmaven.test.skip=true

# 运行 Spring Boot 应用
mvn spring-boot:run -Dmaven.test.skip=true

# 刷新依赖
mvn clean install

# 跳过测试快速编译
mvn compile -DskipTests
```

### Maven 依赖问题

**依赖无法下载**：
```
1. 检查网络连接
2. 右侧 Maven 面板点击刷新按钮
3. 或在 Terminal 运行: mvn clean install
```

**pom.xml 报错**：
```
1. 右键点击 pom.xml
2. Maven → Reload project
3. File → Invalidate Caches → Invalidate and Restart
```

**清除本地仓库**：
```
1. 找到 Maven 本地仓库目录（通常是 ~/.m2/repository）
2. 删除有问题的依赖文件夹
3. 重新导入项目
```

---

## 代码编辑

### 自动补全

**基础补全**：
```
Ctrl + Space
在输入时按，会显示可用的代码建议
```

**智能补全**：
```
Ctrl + Shift + Space
根据上下文猜测想要的代码
```

### 代码生成

**打开 Generate 菜单**：
```
Alt + Insert
```

**常用生成**：
| 操作 | 功能 |
|------|------|
| Getter | 生成 getter 方法 |
| Setter | 生成 setter 方法 |
| Getter and Setter | 同时生成 getter/setter |
| Constructor | 生成构造方法 |
| toString() | 生成 toString 方法 |
| equals() and hashCode() | 生成这两个方法 |

**生成步骤**：
```
1. 在类中按 Alt + Insert
2. 选择要生成的方法
3. 选择要生成的字段
4. 点击 OK
```

### 快速修复

**红色波浪线代表错误**：
```
点击代码，看到红色波浪线
按 Alt + Enter
IDEA会提示可能的修复方案
```

**常见修复**：
- 导入缺失的类
- 修复拼写错误
- 创建缺失的方法
- 修改访问修饰符

### 代码重构

**重命名**：
```
Shift + F6
会重命名所有使用处
```

**提取方法**：
```
Ctrl + Alt + M
选中代码 → 按快捷键 → 输入方法名
将代码提取为新方法
```

**提取变量**：
```
Ctrl + Alt + V
选中表达式 → 按快捷键 → 输入变量名
创建新变量保存表达式结果
```

---

## 代码导航

### 跳转到定义

```
Ctrl + B
光标在某个类/方法/变量上
按快捷键会跳转到定义位置
```

### 跳转到实现

```
Ctrl + Alt + B
光标在接口上
会列出所有实现类
选择一个即可跳转
```

### 查看类层级

```
Ctrl + H
显示类的继承树
可以看到父类和实现的接口
```

### 查看调用层级

```
Ctrl + Alt + H
显示方法的调用树
可以看到谁调用了这个方法
```

### 查找所有引用

```
Alt + F7
找到所有使用某个方法/变量的地方
会在底部窗口列出所有引用
```

### 快速查看

```
Ctrl + Q
光标放在代码上
不跳转，直接在浮窗中显示定义和文档
```

### 最近文件

```
Ctrl + E
显示最近打开的文件列表
输入文件名可搜索
```

### 搜索任何东西

```
Shift + Shift（按两次 Shift）
IDEA 的超级搜索
可以搜索：类、文件、方法、配置、快捷键等
```

---

## 生成代码

### 生成 getter/setter

```
1. 在类中按 Alt + Insert
2. 选择 Getter（或 Setter 或 Getter and Setter）
3. 选中要生成的字段
4. 点击 OK
```

### 生成构造方法

```
1. 在类中按 Alt + Insert
2. 选择 Constructor
3. 选中要包含的字段
4. 点击 OK
```

### 生成 toString()

```
1. 在类中按 Alt + Insert
2. 选择 toString()
3. 选中要包含的字段
4. 点击 OK
```

### 生成 equals/hashCode

```
1. 在类中按 Alt + Insert
2. 选择 equals() and hashCode()
3. 选中要比较的字段
4. 点击 OK
```

### 实现接口方法

```
1. 类实现接口后，会看到红色波浪线
2. 按 Alt + Enter
3. 选择 Implement methods
4. 选择要实现的方法
5. 点击 OK
```

### 覆盖父类方法

```
1. 在类中按 Alt + Insert
2. 选择 Override Methods
3. 选择要覆盖的方法
4. 点击 OK
```

---

## 提示和技巧

### 💡 代码提示
```
光标放在任何代码上，按 Ctrl + Q
会显示该代码的文档和提示信息
```

### 📖 查看源代码
```
Ctrl + B 跳转到定义
可以查看 JDK 源代码或第三方库的源代码
```

### 🔍 快速搜索
```
Ctrl + Shift + F 全局搜索
支持正则表达式
可以在所有文件中搜索
```

### 📋 代码模板
```
Ctrl + J 显示可用的代码模板
输入简写，自动展开为代码块
例如: sout → System.out.println()
```

### 🎯 查看 TODO
```
Alt + 6 打开 Problems 窗口
显示所有 TODO 和 FIXME 注释
```

### 🔗 字符串复制
```
选中字符串后
Ctrl + Shift + C 复制路径或完全限定名
```

---

## 推荐插件

### 必装插件

在 `File → Settings → Plugins → Marketplace` 中安装：

| 插件名 | 功能 |
|--------|------|
| **Lombok** | 简化Java代码，自动生成getter/setter |
| **Maven Helper** | 增强Maven支持，快速查看依赖 |
| **Rainbow Brackets** | 彩色括号匹配，代码更清晰 |

### 推荐插件

| 插件名 | 功能 |
|--------|------|
| **String Manipulation** | 字符串转换工具（大小写、格式等） |
| **GenerateAllSetter** | 快速生成所有setter |
| **Spring Boot Assistant** | Spring Boot 增强支持 |
| **SonarLint** | 代码质量检查，找出问题 |
| **Git Commit Message Helper** | 帮助编写规范的Git提交信息 |

---

## 常用工作流

### 日常开发流程

```
1. 打开项目
   File → Open → JtProject

2. 等待 Maven 导入和索引完成
   右下角进度条消失

3. 编写代码
   在 src/main/java 中编写代码

4. 运行应用
   Shift + F10 或点击绿色播放按钮

5. 访问应用
   打开浏览器访问 http://localhost:8080

6. 调试问题
   设置断点 → Shift + F9 进入调试
   F8/F7逐步执行
```

### 添加新功能

```
1. 在 models/ 创建Entity类
2. 在 dao/ 创建DAO实现
3. 在 services/ 创建Service实现
4. 在 controller/ 创建Controller方法
5. 在 src/main/webapp/views/ 创建JSP视图
6. 运行测试
```

### 调试流程

```
1. 在可能有问题的地方设置断点
   通常在 Controller 或 Service 方法开头

2. 启动调试
   Shift + F9

3. 应用运行到断点处停下

4. 查看变量
   在 Variables 面板或 Watches 中查看

5. 逐步执行
   F8 跳过，F7 进入，Shift + F8 跳出

6. 找到问题，修改代码，重启调试
```

---

## 快速查找表

### 按场景查找

| 场景 | 快捷键或位置 |
|------|-----------|
| **如何运行应用** | Shift + F10 或点击绿色播放按钮 |
| **如何调试** | Shift + F9，设置断点，F8/F7执行 |
| **如何搜索某个类** | Ctrl + N |
| **如何搜索某个方法** | Ctrl + Alt + Shift + N |
| **如何格式化代码** | Ctrl + Alt + L |
| **如何查看快捷键** | Help → Keymap Reference |
| **如何优化导入** | Ctrl + Alt + O |
| **如何查看文档** | Ctrl + Q（光标在代码上） |
| **如何生成getter/setter** | Alt + Insert |
| **如何重命名** | Shift + F6 |

---

## 常见问题速查

| 问题 | 位置 |
|------|------|
| **右键没有运行按钮** | [运行按钮问题](#运行按钮问题) |
| **启动时出错** | [启动问题完整方案](#启动问题完整方案) |
| **无法连接数据库** | [常见问题解决](#常见问题解决) - Q4 |
| **编译出错** | [常见问题解决](#常见问题解决) - Q1 |
| **端口被占用** | [常见问题解决](#常见问题解决) - Q3 |
| **想要黑色主题** | [黑色主题设置](#黑色主题设置) |
| **想要学习快捷键** | [快捷键大全](#快捷键大全) |
| **想要学习调试** | [调试技巧](#调试技巧) |

---

## 相关文档位置

所有原始文档位置（用于参考）：

```
d:\dev\source_code\vscode_study\
├── idea快捷键.md                          # 快捷键对照表
├── java-projects\JtProject\
│   ├── IDEA_快速参考.md                    # 快速参考卡片
│   ├── IDEA_启动指南.md                    # 详细启动教程
│   ├── IDEA_Markdown插件安装指南.md        # 插件安装
│   ├── IDEA启动问题完整解决方案.md         # 启动故障排除
│   ├── IDEA完整启动指南.md                 # 完整启动指南
│   ├── IDEA黑色主题完整设置指南.md         # 主题设置
│   ├── IDEA操作完整指南-新手版.md          # 新手指南
│   ├── IDEA打开项目详细说明.md             # 打开项目
│   ├── IDEA完整操作指南.md                 # 完整操作
│   ├── IDEA主题设置指南.md                 # 主题指南
│   ├── IDEA运行按钮完整解决方案.md         # 运行按钮问题
│   └── 手动启动项目完整指南-IDEA版.md      # 手动启动
└── localstack-lab\
    └── 如何查看LocalStack日志.md           # LocalStack日志查看
```

---

## 版本历史

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-01-04 | v1.0 | 汇总整理所有IDEA相关文档 |

---

**提示**：将此文件添加到IDEA收藏夹以便快速查阅：
```
右键文件 → Add to Favorites
或 Alt + 2 打开 Favorites 面板查看
```

**如有问题**：首先查看 [常见问题解决](#常见问题解决) 或 [启动问题完整方案](#启动问题完整方案)
