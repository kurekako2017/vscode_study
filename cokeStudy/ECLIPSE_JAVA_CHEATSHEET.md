# Eclipse Java 使用教程与快捷键（Windows）

**概述**
- 目标读者：希望在 Windows 下使用 Eclipse 开发 Java 的工程师/学生。
- 主要内容：环境准备、创建项目、常用快捷键、调试技巧、构建与依赖、单元测试、常见问题与性能优化。

**环境准备**
- 安装 JDK（建议使用 LTS 版本，如 Java 11 或 17）。安装后设置系统环境变量 `JAVA_HOME` 指向 JDK 根目录，并把 `%JAVA_HOME%\bin` 加入 `PATH`。
- 下载 Eclipse：推荐使用 “Eclipse IDE for Java Developers”。解压后启动，选择工作区（workspace）。
- 在 Eclipse 中确认 JRE：`Window > Preferences > Java > Installed JREs`，添加并勾选你安装的 JDK。

**快速创建并运行 Java 应用**
1. `File > New > Java Project`，输入项目名（例如 `MyApp`）。
2. 右键项目 `New > Package`，再 `New > Class`，勾选 `public static void main(String[] args)`。
3. 运行类：右键类文件 `Run As > Java Application` 或选中编辑器按 `Ctrl+F11`（运行上次启动）。

**常用快捷键（Windows）**
- 打开/定位
  - Open Type: `Ctrl+Shift+T`（按类名打开）
  - Open Resource: `Ctrl+Shift+R`（按文件名打开）
  - Quick Outline: `Ctrl+O`（当前类大纲）
- 编辑与帮助
  - Content Assist（代码提示）: `Ctrl+Space`
  - Quick Fix / 快速修复: `Ctrl+1`（导入、生成方法、重命名建议等）
  - 格式化代码: `Ctrl+Shift+F`
  - 注释/取消注释: `Ctrl+/`
  - 删除当前行: `Ctrl+D`
- 导航与搜索
  - 跳转到声明 (Open Declaration): `F3`
  - 查找引用 (Find References): `Ctrl+Shift+G`
  - 搜索对话框: `Ctrl+H`
- 重构
  - Rename: `Alt+Shift+R`
  - Extract Method: `Alt+Shift+M`
  - Source 菜单（生成 getter/setter，重写方法）: `Alt+Shift+S`
- 运行与调试
  - Run Last Launched: `Ctrl+F11`
  - Debug Last Launched: `F11`
  - Toggle Breakpoint: `Ctrl+Shift+B`（或在行号区单击）
  - Step Into: `F5`, Step Over: `F6`, Step Return: `F7`, Resume: `F8`
- 视图与 Perspective
  - 切换 Perspective: `Alt+Shift+Q`，然后按 `Q`（或使用右上角图标）

**调试实战要点**
- 设置断点：在左侧行号区单击，或选中行 `Ctrl+Shift+B`。
- 条件断点：右键断点 → Properties → 勾选 `Enable Condition` 并输入表达式，减少无关触发。
- 使用 `Variables`、`Expressions`、`Breakpoints`、`Debug Console` 查看变量与表达式。
- 热替换（Hot Swap）：在调试时修改方法体并保存，若字节码结构未更改，JVM 通常允许热替换。
- 建议把认证/密码校验等敏感逻辑放到 Service 层，DAO 只做查询，便于单测与调试。

**构建与依赖管理**
- Maven 项目：Eclipse 通常内置 M2E 插件。导入：`File > Import > Existing Maven Projects`。
- Gradle 项目：使用 Buildship 插件。导入：`File > Import > Gradle > Existing Gradle Project`。
- 常见命令行：
```bash
# Maven
mvn clean package
mvn test

# Gradle (Windows wrapper)
gradlew build
gradlew test
```
- 在 Eclipse 中可创建 `Run As > Maven build...` 或 Gradle Run configuration 来运行构建任务。

**单元测试**
- 新建 JUnit 测试：`New > JUnit Test Case`（根据项目依赖选择 JUnit4 或 JUnit5）
- 运行测试：右键测试类或包 → `Run As > JUnit Test`；在 `Package Explorer` 上右键可运行整个测试包。

**代码质量与自动化**
- Save Actions：`Window > Preferences > Java > Editor > Save Actions`，启用自动格式化、删除未使用的 import。
- 静态检查：推荐安装并配置 `Checkstyle`、`SpotBugs` 插件，保持代码风格一致。

**常见问题与解决**
- Eclipse 卡顿/内存不足：编辑 `eclipse.ini` 增加 JVM 参数，例如：
```text
-Xms512m
-Xmx2g
-XX:+UseG1GC
```
- 类路径/依赖冲突：右键项目 `Properties > Java Build Path` 检查 `Libraries` 与 `Order and Export`。
- JDK 与项目编译级别不匹配：检查 `Project > Properties > Java Compiler` 与 `Installed JREs`。
- 索引/编译器错误：尝试 `Project > Clean...`，或重建项目、重启 Eclipse。

**安全与最佳实践（针对你提供的 DAO 登录代码的提示）**
- 切勿以明文存储或直接用 `equals` 比较密码。使用 BCrypt 等哈希算法并使用常量时间比较（例如 Spring 的 `PasswordEncoder`）。
- DAO 层只负责数据访问，认证逻辑放在 Service 层更合理。
- 为 `username` 添加数据库唯一约束，避免多条记录时模糊处理。
- 失败时不要返回空对象误导调用方，优先使用 `Optional<User>` 或明确异常/状态返回。

**推荐插件**
- EGit（Git 支持）
- M2E（Maven 集成）
- Buildship（Gradle）
- Spring Tools（Spring 开发）
- Checkstyle / SpotBugs

**附：快速操作清单**
- 新建项目：`File > New > Java Project`
- 运行：选类 → `Run As > Java Application` 或 `Ctrl+F11`
- 调试：`F11` 或 `Debug As > Java Application`
- 快速修复：`Ctrl+1`
- 跳类：`Ctrl+Shift+T`

---

如果需要，我可以：
- 把本文件保存为 `ECLIPSE_JAVA_CHEATSHEET.md`（已保存到工作区）。
- 基于你给的 DAO 代码生成一个重构后的示例实现（使用 `PasswordEncoder` + `Optional<User>`）。
- 添加截图或更详细的逐步操作（含具体菜单截图）。

请告诉我你想要我继续做的下一步（例如：生成重构补丁 / 添加示例代码并运行）。