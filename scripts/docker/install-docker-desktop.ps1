# 脚本: install-docker-desktop.ps1
# 说明: Docker Desktop 完整安装流程（含前置条件检查）。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\docker\install-docker-desktop.ps1

$ErrorActionPreference = 'Stop'

Write-Host @"

╔══════════════════════════════════════════════════════╗
║         Docker Desktop 自动安装脚本                   ║
╚══════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"

# 步骤 1: 下载 Docker Desktop
Write-Host "[1/3] 下载 Docker Desktop 安装程序..." -ForegroundColor Yellow

try {
    # 如果文件已存在且大小合理，跳过下载
    if (Test-Path $installerPath) {
        $existingSize = (Get-Item $installerPath).Length
        if ($existingSize -gt 100MB) {
            Write-Host "  发现已下载的安装文件 ($([math]::Round($existingSize/1MB, 2)) MB)" -ForegroundColor Green
            $skip = Read-Host "  是否使用已有文件？(Y/n)"
            if ($skip -ne 'n' -and $skip -ne 'N') {
                Write-Host "  使用已有安装文件" -ForegroundColor Green
            } else {
                Remove-Item $installerPath -Force
                Write-Host "  开始下载 (约 600 MB，请耐心等待)..." -ForegroundColor Yellow
                $webClient = New-Object System.Net.WebClient
                $webClient.DownloadFile($dockerUrl, $installerPath)
            }
        }
    } else {
        Write-Host "  开始下载 (约 600 MB，请耐心等待)..." -ForegroundColor Yellow
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($dockerUrl, $installerPath)
    }

    $fileSize = (Get-Item $installerPath).Length
    Write-Host "  ✓ 下载完成！文件大小: $([math]::Round($fileSize/1MB, 2)) MB" -ForegroundColor Green

} catch {
    Write-Host "  ✗ 下载失败: $_" -ForegroundColor Red
    Write-Host "`n请手动下载安装程序：" -ForegroundColor Yellow
    Write-Host "  URL: https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
    exit 1
}

# 步骤 2: 检查系统要求
Write-Host "`n[2/3] 检查系统要求..." -ForegroundColor Yellow

# 检查 WSL 2
$wslVersion = wsl --status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠ WSL 未安装或未启用" -ForegroundColor Yellow
    Write-Host "  Docker Desktop 需要 WSL 2，安装程序会自动配置" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ WSL 已安装" -ForegroundColor Green
}

# 检查 Hyper-V
$hyperv = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue
if ($hyperv.State -eq 'Enabled') {
    Write-Host "  ✓ Hyper-V 已启用" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Hyper-V 未启用（将使用 WSL 2 后端）" -ForegroundColor Yellow
}

# 步骤 3: 安装 Docker Desktop
Write-Host "`n[3/3] 安装 Docker Desktop..." -ForegroundColor Yellow
Write-Host "  这可能需要几分钟时间，请等待..." -ForegroundColor Yellow

try {
    $process = Start-Process -FilePath $installerPath -ArgumentList "install --quiet --accept-license" -Wait -PassThru -NoNewWindow

    if ($process.ExitCode -eq 0) {
        Write-Host "  ✓ Docker Desktop 安装成功！" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ 安装程序退出代码: $($process.ExitCode)" -ForegroundColor Yellow
        Write-Host "  可能需要手动完成安装" -ForegroundColor Yellow
    }

} catch {
    Write-Host "  ✗ 安装过程出错: $_" -ForegroundColor Red
    Write-Host "  请尝试手动运行安装程序: $installerPath" -ForegroundColor Yellow
    exit 1
}

# 完成提示
Write-Host @"

╔══════════════════════════════════════════════════════╗
║                 安装完成                              ║
╚══════════════════════════════════════════════════════╝

"@ -ForegroundColor Green

Write-Host "后续步骤：" -ForegroundColor Yellow
Write-Host "  1. 重启计算机（如果安装程序要求）" -ForegroundColor White
Write-Host "  2. 启动 Docker Desktop 应用程序" -ForegroundColor White
Write-Host "  3. 等待 Docker 引擎启动完成" -ForegroundColor White
Write-Host "  4. 在终端运行: docker --version" -ForegroundColor White
Write-Host ""
Write-Host "验证安装：" -ForegroundColor Yellow
Write-Host "  docker --version" -ForegroundColor Cyan
Write-Host "  docker run hello-world" -ForegroundColor Cyan
Write-Host ""

