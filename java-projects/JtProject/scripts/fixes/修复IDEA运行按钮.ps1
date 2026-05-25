# IDEA运行按钮修复脚本
# 请先关闭IDEA再运行此脚本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "IDEA运行按钮修复脚本" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 检查IDEA是否在运行
$ideaProcess = Get-Process | Where-Object { $_.ProcessName -like "*idea*" }
if ($ideaProcess) {
    Write-Host "⚠️  检测到IDEA正在运行！" -ForegroundColor Yellow
    Write-Host "请先关闭IDEA，然后重新运行此脚本。" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按Enter键退出"
    exit
}

Write-Host "✓ 未检测到IDEA进程" -ForegroundColor Green
Write-Host ""

# 项目根目录
$projectDir = $PSScriptRoot
$ideaDir = Join-Path $projectDir ".idea"

Write-Host "正在修复运行配置..." -ForegroundColor Yellow

# 1. 确保.idea目录存在
if (!(Test-Path $ideaDir)) {
    New-Item -ItemType Directory -Path $ideaDir | Out-Null
    Write-Host "✓ 创建.idea目录" -ForegroundColor Green
}

# 2. 确保runConfigurations目录存在
$runConfigDir = Join-Path $ideaDir "runConfigurations"
if (!(Test-Path $runConfigDir)) {
    New-Item -ItemType Directory -Path $runConfigDir | Out-Null
    Write-Host "✓ 创建runConfigurations目录" -ForegroundColor Green
}

# 3. 创建运行配置文件
$runConfigFile = Join-Path $runConfigDir "JtSpringProjectApplication.xml"
$runConfigContent = @"
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="JtSpringProjectApplication" type="SpringBootApplicationConfigurationType" factoryName="Spring Boot" nameIsGenerated="true">
    <module name="JtSpringProject" />
    <option name="SPRING_BOOT_MAIN_CLASS" value="com.jtspringproject.JtSpringProject.JtSpringProjectApplication" />
    <option name="ALTERNATIVE_JRE_PATH" />
    <option name="SHORTEN_COMMAND_LINE" value="NONE" />
    <option name="FRAME_DEACTIVATION_UPDATE_POLICY" value="UpdateClassesAndResources" />
    <method v="2">
      <option name="Make" enabled="true" />
    </method>
  </configuration>
</component>
"@

Set-Content -Path $runConfigFile -Value $runConfigContent -Encoding UTF8
Write-Host "✓ 创建运行配置文件" -ForegroundColor Green

# 4. 更新workspace.xml
$workspaceFile = Join-Path $ideaDir "workspace.xml"
$workspaceContent = @"
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="SELECTIVE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="default" name="Changes" comment="" />
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="ProjectId" id="JtSpringProject" />
  <component name="ProjectViewState">
    <option name="hideEmptyMiddlePackages" value="true" />
    <option name="showLibraryContents" value="true" />
  </component>
  <component name="PropertiesComponent">
    <property name="RunOnceActivity.OpenProjectViewOnStart" value="true" />
    <property name="RunOnceActivity.ShowReadmeOnStart" value="true" />
    <property name="last_opened_file_path" value="`$PROJECT_DIR`$" />
    <property name="settings.editor.selected.configurable" value="preferences.lookFeel" />
  </component>
  <component name="RunManager" selected="Spring Boot.JtSpringProjectApplication">
    <configuration name="JtSpringProjectApplication" type="SpringBootApplicationConfigurationType" factoryName="Spring Boot" nameIsGenerated="true">
      <module name="JtSpringProject" />
      <option name="SPRING_BOOT_MAIN_CLASS" value="com.jtspringproject.JtSpringProject.JtSpringProjectApplication" />
      <method v="2">
        <option name="Make" enabled="true" />
      </method>
    </configuration>
  </component>
  <component name="SpellCheckerSettings" RuntimeDictionaries="0" Folders="0" CustomDictionaries="0" DefaultDictionary="application-level" UseSingleDictionary="true" transferred="true" />
</project>
"@

Set-Content -Path $workspaceFile -Value $workspaceContent -Encoding UTF8
Write-Host "✓ 更新workspace.xml" -ForegroundColor Green

# 5. 确保misc.xml正确配置JDK
$miscFile = Join-Path $ideaDir "misc.xml"
$miscContent = @"
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" languageLevel="JDK_11" default="true" project-jdk-name="11" project-jdk-type="JavaSDK">
    <output url="file://`$PROJECT_DIR`$/out" />
  </component>
</project>
"@

Set-Content -Path $miscFile -Value $miscContent -Encoding UTF8
Write-Host "✓ 更新misc.xml" -ForegroundColor Green

# 6. 清理IDEA缓存目录（可选）
Write-Host ""
Write-Host "正在清理IDEA缓存..." -ForegroundColor Yellow
$ideaCacheDir = Join-Path $ideaDir "cache"
if (Test-Path $ideaCacheDir) {
    Remove-Item -Path $ideaCacheDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ 清理缓存目录" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✓ 修复完成！" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "接下来的步骤：" -ForegroundColor Yellow
Write-Host "1. 打开IDEA" -ForegroundColor White
Write-Host "2. 打开项目：D:\dev\source_code\vscode_study\java-projects\JtProject" -ForegroundColor White
Write-Host "3. 等待IDEA加载和索引完成（查看右下角进度条）" -ForegroundColor White
Write-Host "4. 打开文件：src/main/java/com/jtspringproject/JtSpringProject/JtSpringProjectApplication.java" -ForegroundColor White
Write-Host "5. 你应该会看到main方法左侧的绿色运行按钮" -ForegroundColor White
Write-Host ""
Write-Host "快捷键提示：" -ForegroundColor Yellow
Write-Host "- Ctrl + Shift + F10：运行当前文件" -ForegroundColor White
Write-Host "- Shift + F10：运行上次配置" -ForegroundColor White
Write-Host ""
Write-Host "如果还是没有运行按钮，请尝试：" -ForegroundColor Yellow
Write-Host "1. File → Invalidate Caches → Invalidate and Restart" -ForegroundColor White
Write-Host "2. 右键点击项目根目录 → Maven → Reload Project" -ForegroundColor White
Write-Host ""

Read-Host "按Enter键退出"

