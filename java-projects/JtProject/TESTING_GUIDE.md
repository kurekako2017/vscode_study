# 测试类使用教程（当前项目）

本教程只覆盖当前仓库里**实际可运行**的测试，不再使用过时示例。

## 当前测试结构

- 有效测试目录：`src/test/java`
- 当前测试类（2个）：
  - `controller/AdminControllerProductUpdateTest.java`
  - `controller/UserControllerCartTest.java`
- 历史备份测试目录：`src/test_disabled_backup`（默认不参与当前测试执行）

## 运行前准备（Windows）

1. 进入项目目录：

```powershell
cd D:\dev\source_code\vscode_study\java-projects\JtProject
```

1. 确认 Java 环境（若提示 `JAVA_HOME not found`，先设置）：

```powershell
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"
$env:Path="$env:JAVA_HOME\\bin;$env:Path"
```

## 一键运行测试

### 方式1：运行全部当前测试（推荐）

```powershell
.\mvnw.cmd test
```

### 方式2：只运行单个测试类

```powershell
.\mvnw.cmd -Dtest=AdminControllerProductUpdateTest test
.\mvnw.cmd -Dtest=UserControllerCartTest test
```

### 方式3：只运行单个测试方法

```powershell
.\mvnw.cmd -Dtest=AdminControllerProductUpdateTest#updateProduct_ShouldKeepOldImage_WhenImageBlank test
```

## 查看结果

- 命令行：看 `Tests run / Failures / Errors / Skipped`
- 报告目录：`target/surefire-reports`
  - 文本：`*.txt`
  - XML：`TEST-*.xml`

## 与打包的关系

- 开发打包（跳过测试）：

```powershell
.\mvnw.cmd clean package -DskipTests
```

- CI 或发布前建议：

```powershell
.\mvnw.cmd clean test
```

## 常见问题

### 1) `JAVA_HOME not found`

- 原因：终端未配置 Java 环境。
- 处理：按上面的“运行前准备”先设置 `JAVA_HOME`，再执行测试。

### 2) 想把历史备份测试也跑起来

当前不建议直接启用全部历史测试（内容较旧，可能与现实现不一致）。

如需迁回，请分批迁移：

```powershell
# 示例：先只迁移一个测试类回 src/test，再单独运行
```

### 3) 只想快速验证本轮修改

- 优先跑相关测试类，不要一上来全量跑：

```powershell
.\mvnw.cmd -Dtest=AdminControllerProductUpdateTest test
```

## 推荐流程（最稳妥）

1. 改代码。
2. 只跑相关测试类。
3. 通过后再跑 `clean test`。
4. 最后再执行打包或启动验证。
