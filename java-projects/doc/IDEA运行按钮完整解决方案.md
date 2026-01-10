# IDEA运行按钮完整解决方案

## 问题现象
在IDEA中打开JtSpringProjectApplication.java文件后，没有看到运行按钮（绿色三角形）。

## 解决方案（按顺序尝试）

### 方案1：刷新Maven项目（最常见）
1. 找到IDEA右侧的 **Maven** 标签页（如果没看到，点击菜单 **View → Tool Windows → Maven**）
2. 点击刷新按钮（圆形箭头图标）🔄
3. 等待Maven下载依赖完成
4. 完成后，main方法旁边应该会出现绿色运行按钮

### 方案2：手动添加运行配置
1. 点击IDEA右上角的运行配置下拉框（显示"Add Configuration..."或当前配置名）
2. 点击 **Edit Configurations...**
3. 点击左上角的 **+** 号
4. 选择 **Spring Boot**
5. 填写以下信息：
   - Name: `JtSpringProjectApplication`
   - Main class: `com.jtspringproject.JtSpringProject.JtSpringProjectApplication`
   - Use classpath of module: 选择 `JtSpringProject`
6. 点击 **OK**
7. 现在右上角应该有绿色运行按钮了

### 方案3：重新导入项目
1. 关闭当前项目：**File → Close Project**
2. 在欢迎界面点击 **Open**
3. 选择项目的 `pom.xml` 文件
4. 选择 **Open as Project**
5. 等待IDEA索引完成（右下角进度条）
6. 打开 `JtSpringProjectApplication.java`，应该会看到运行按钮

### 方案4：使用PowerShell脚本自动修复
我已经为你准备了一个自动修复脚本。请按以下步骤操作：

1. **关闭IDEA**（这很重要！）
2. 打开PowerShell
3. 运行以下命令：
```powershell
cd "D:\dev\source_code\vscode_study\java-projects\JtProject"
.\修复IDEA运行按钮.ps1
```
4. 重新打开IDEA，打开项目

## 快捷键提示

### 运行相关
- **Shift + F10** - 运行当前配置
- **Ctrl + Shift + F10** - 运行当前文件（包含main方法的类）
- **Shift + F9** - 调试当前配置
- **Ctrl + Shift + F9** - 调试当前文件

### 即使没有运行按钮，你也可以：
1. 在 `JtSpringProjectApplication.java` 文件中
2. 将光标放在 `main` 方法内
3. 按 **Ctrl + Shift + F10**
4. 项目会立即运行，并自动创建运行配置

## 验证是否成功
成功后你应该看到：
1. ✅ main方法左侧有绿色三角形按钮
2. ✅ IDEA右上角有运行按钮和配置名称
3. ✅ 按Ctrl + Shift + F10可以运行项目

## 如果还是不行
运行下面的命令来诊断问题：
```powershell
cd "D:\dev\source_code\vscode_study\java-projects\JtProject"
.\check-status.ps1
```

## 常见原因
- Maven依赖还在下载中（查看右下角进度条）
- JDK配置不正确（File → Project Structure → Project SDK 应该是Java 11）
- IDEA缓存问题（File → Invalidate Caches → Invalidate and Restart）

