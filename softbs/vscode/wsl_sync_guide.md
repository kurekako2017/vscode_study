# WSL 到 Windows 本地工作区同步指南

本指南介绍如何在不通过 Git 的情况下，将 WSL (Ubuntu) 中的工作区内容高效、增量地同步到 Windows 的 D 盘目标备份目录。

---

## 🛠️ 核心同步命令 (`rsync`)

在 WSL 终端中，Windows 的 **D 盘** 默认挂载在 `/mnt/d/`。我们使用 `rsync` 工具来实现增量同步：它会自动比对文件，只传输有修改的部分，并支持过滤依赖、缓存与构建产物目录。

### 当前完整别名（推荐）

```bash
alias syncD="rsync -av --delete --exclude='node_modules/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.git/' --exclude='.deps/' --exclude='.cache/' --exclude='dist/' --exclude='build/' --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='*.pyc' ~/workspace/vscode_study/ /mnt/d/dev/source_code/vscode_study/"
```

#### 路径与斜杠说明

| 角色 | 路径 | 末尾 `/` | 含义 |
|------|------|----------|------|
| 源目录 | `~/workspace/vscode_study/` | 有 | 同步该目录的**内容**到目标 |
| 目标目录 | `/mnt/d/dev/source_code/vscode_study/` | 有 | 写入该目录内部 |

源路径**必须**带尾部斜杠，才能实现「内容镜像」而不是在目标下再套一层同名文件夹。

#### 排除项一览

| 类别 | 排除项 |
|------|--------|
| 依赖 / 虚拟环境 | `node_modules/`、`.venv/`、`.deps/` |
| 版本控制 | `.git/` |
| Python 缓存 | `__pycache__/`、`.pytest_cache/`、`.mypy_cache/`、`*.pyc` |
| 通用缓存 / 构建产物 | `.cache/`、`dist/`、`build/` |

---

## ⚙️ 快捷配置步骤

为了免去每次手动输入长命令，我们将同步命令封装为别名 **`syncD`**，并放在专门的别名文件 `~/.bash_aliases` 中（由 `~/.bashrc` 自动加载，比直接改 `.bashrc` 更清晰、更易维护）。

#### 1. 打开或创建别名文件

在 WSL 终端中运行：

```bash
code ~/.bash_aliases
```

> 若尚未安装 VS Code 的 `code` 命令，也可使用：
>
> ```bash
> nano ~/.bash_aliases
> ```

#### 2. 粘贴完整别名配置

将文件内容设为（或覆盖为）下面这一整行（注意：`alias` 等号两边不能有空格）：

```bash
alias syncD="rsync -av --delete --exclude='node_modules/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.git/' --exclude='.deps/' --exclude='.cache/' --exclude='dist/' --exclude='build/' --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='*.pyc' ~/workspace/vscode_study/ /mnt/d/dev/source_code/vscode_study/"
```

保存并关闭编辑器。

#### 3. 使配置立即生效

在当前终端执行：

```bash
source ~/.bash_aliases
```

验证是否加载成功：

```bash
alias syncD
```

输出中应能看到完整的 `--exclude` 列表（含 `.deps/`、`.cache/`、`dist/` 等）。

> **说明**：新开的 WSL 终端会通过 `~/.bashrc` 自动 `source ~/.bash_aliases`，一般无需再手动加载。

#### （可选）一键覆盖写入

若希望在终端里一次性覆盖文件并立即生效，可直接粘贴：

```bash
cat > ~/.bash_aliases << 'EOF'
alias syncD="rsync -av --delete --exclude='node_modules/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.git/' --exclude='.deps/' --exclude='.cache/' --exclude='dist/' --exclude='build/' --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='*.pyc' ~/workspace/vscode_study/ /mnt/d/dev/source_code/vscode_study/"
EOF
source ~/.bash_aliases && alias syncD
```

---

## 🚀 日常使用方法

配置完成后，日常开发结束或需要备份时，在 WSL 终端任意路径下执行：

```bash
syncD
```

即可将 `~/workspace/vscode_study/` 增量镜像到 Windows：

`D:\dev\source_code\vscode_study\`

---

## 💡 关键机制说明

### `--delete` 镜像同步

若在 WSL 中删除了某个文件，执行 `syncD` 后，Windows D 盘对应路径下的文件也会被同步删除，确保两端内容一致（镜像语义）。

> 注意：被 `--exclude` 排除的源侧目录不会再传输；若目标上此前已同步过这些目录（例如旧的 `.deps/`），下次带 `--delete` 的同步会把目标上对应内容删掉，这通常正是我们想要的效果。

### `--exclude` 智能过滤：为什么要加这么多？

WSL 同步到 `/mnt/d/` 属于**跨文件系统**访问（Linux 文件系统 → Windows 的 DrvFs/9p 挂载）。`rsync` 在增量比对时，需要对每个文件做元数据/内容检查；当项目中存在海量「小文件依赖与缓存」时，瓶颈往往不在「真正要拷贝多少代码」，而在于：

1. **海量小文件的逐一 stat / 比对** 在跨文件系统路径上极慢；
2. **依赖与缓存目录体积大、文件多**，却几乎没有备份价值（可随时在本机重建）；
3. 日志里若长时间卡在类似  
   `.../.deps/numpy-....dist-info/...`  
   这类路径，就是典型的「依赖缓存拖垮同步」现象。

因此，当前别名一次性排除：

- **依赖目录**：`node_modules/`、`.venv/`、`.deps/`
- **语言/工具缓存**：`__pycache__/`、`.pytest_cache/`、`.mypy_cache/`、`*.pyc`、`.cache/`
- **构建产物**：`dist/`、`build/`
- **版本库本体**：`.git/`（体积大，且 Windows 侧一般不需要完整 Git 对象做日常浏览）

这能显著减少跨文件系统比对与传输的文件数量，从而**大幅缩短 `syncD` 耗时**，并避免无意义的磁盘占用。

### 推荐实践

1. **先排除、再同步**：改 exclude 后第一次执行可能仍会稍慢（清理目标上旧的缓存目录），之后会明显变快。
2. **需要在 Windows 侧跑项目时**：依赖应在 Windows 环境或 WSL 内重新安装，不要指望从 D 盘镜像里带过去完整的 `node_modules` / `.venv`。
3. **仍觉得慢时**：可再按项目实际情况追加 exclude（例如 `.next/`、`coverage/`、`.tox/`、`.ruff_cache/` 等）。

---

## 📎 快速对照

| 项目 | 内容 |
|------|------|
| 别名名 | `syncD` |
| 配置文件 | `~/.bash_aliases`（由 `~/.bashrc` 加载） |
| 生效命令 | `source ~/.bash_aliases` |
| 源 | `~/workspace/vscode_study/` |
| 目标 | `/mnt/d/dev/source_code/vscode_study/`（Windows：`D:\dev\source_code\vscode_study\`） |
| 核心参数 | `-av --delete` + 完整 `--exclude` 列表 |
