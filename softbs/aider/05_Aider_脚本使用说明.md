# 一键启动 Aider（PowerShell 脚本）

## 文件说明
- `05_Aider_OneClick_PowerShell.ps1`：一键启动脚本

## 使用步骤

### 1. 允许脚本执行（仅一次）
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. 放置脚本
建议放在：
```
D:\aider\start-aider.ps1
```

### 3. 运行方式

#### 默认（当前目录 + Qwen）
```powershell
.\start-aider.ps1
```

#### 指定项目目录
```powershell
.\start-aider.ps1 -ProjectPath D:\projects\myapp
```

#### 指定模型
```powershell
.\start-aider.ps1 -Model ollama/deepseek-coder-v2-lite:16b
```

---