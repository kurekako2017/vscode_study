# Scripts

本项目脚本已按用途整理。

## 目录说明

- `start/`: 当前推荐使用的启动脚本
- `diagnostics/`: 状态检查、端口检查等诊断脚本
- `fixes/`: IDE 或环境修复脚本
- `history/`: 历史脚本归档，不再作为主入口

## 推荐入口

### Windows PowerShell

```powershell
.\scripts\start\run.ps1
```

### Windows CMD

```cmd
scripts\start\run.cmd
```

### Windows CMD - Batch Sample

```cmd
scripts\start\run-product-inventory-check.cmd
```

### Windows CMD - Quartz Batch Sample

```cmd
scripts\start\run-quartz-product-inventory-check.cmd
```

### Linux / macOS

```bash
./scripts/start/start.sh
```

## 说明

- 根目录只保留 Maven Wrapper: `mvnw`, `mvnw.cmd`
- Batch / Quartz 示例脚本会优先使用 Maven Wrapper，失败时自动回退到本地 `mvn`
- 旧的 `start.ps1`、`一键启动.ps1`、`启动项目.bat` 等已归档到 `scripts/history/start/`
- 如需检查应用状态，使用 `scripts/diagnostics/check-status.ps1`
