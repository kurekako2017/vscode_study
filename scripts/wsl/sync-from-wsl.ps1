param(
  [string]$Distro = "Ubuntu",
  [string]$SourcePath = "/home/victorkure/workspace/vscode_study",
  [string]$TargetPath = "D:\dev\source_code\vscode_study",
  [switch]$NoMirror
)

$ErrorActionPreference = "Stop"

function Write-Info {
  param([string]$Message)
  Write-Host "[INFO] $Message"
}

function Write-Warn {
  param([string]$Message)
  Write-Host "[WARN] $Message"
}

function Write-ErrorAndExit {
  param([string]$Message)
  Write-Host "[ERROR] $Message"
  exit 1
}

$normalizedSourcePath = $SourcePath.TrimStart('/').Replace('/', '\')
$source = "\\wsl$\$Distro\$normalizedSourcePath"

Write-Info "WSL distribution: $Distro"
Write-Info "Source: $source"
Write-Info "Target: $TargetPath"

if (-not (Test-Path -LiteralPath $source)) {
  Write-ErrorAndExit "Cannot access WSL source path. Check the distro name and source path."
}

if (-not (Test-Path -LiteralPath $TargetPath)) {
  Write-Info "Creating target directory."
  New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

$robocopyArgs = @(
  $source
  $TargetPath
  "/E"
  "/XD"
  ".git"
  "node_modules"
  ".venv"
  "/R:2"
  "/W:1"
)

if (-not $NoMirror) {
  $robocopyArgs[2] = "/MIR"
}

Write-Info "Starting file sync. Use -NoMirror if you want to keep extra files on the target."
& robocopy @robocopyArgs
$exitCode = $LASTEXITCODE

if ($exitCode -le 7) {
  Write-Info "Sync finished successfully. Robocopy exit code: $exitCode"
  exit 0
}

Write-Warn "Sync finished with robocopy exit code: $exitCode"
exit $exitCode