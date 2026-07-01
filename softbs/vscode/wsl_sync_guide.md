# WSL 到 Windows 本地工作区同步指南

本指南介绍如何在不通过 Git 的情况下，将 WSL (Ubuntu) 中的工作区内容高效、增量地同步到 Windows 的 D 盘目标备份目录。

---

## 🛠️ 核心同步命令 (`rsync`)

在 WSL 终端中，Windows 的 **D 盘** 默认挂载在 `/mnt/d/`。我们使用 `rsync` 工具来实现增量同步，它会自动比对文件，只传输有修改的部分，并支持过滤巨型缓存文件夹。

### 快捷配置步骤

为了免去每次手动输入长命令的麻烦，我们将同步命令封装为一个好记的别名 **`syncD`**。

#### 1. 打开 WSL 配置文件
在 WSL 终端中运行以下命令，使用 Nano 编辑器打开 `~/.bashrc`：
```bash
nano ~/.bashrc
```

#### 2. 添加别名 (Alias)
使用键盘方向键 `↓` 拉到文件最底部，粘贴以下整行配置（注意：`alias` 等号两边不能有空格）：

```bash
alias syncD="rsync -av --delete --exclude='node_modules/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.git/' ~/workspace/vscode_study/ /mnt/d/dev/source_code/vscode_study/"
```

#### 3. 保存并退出编辑器
* 按下快捷键 `Ctrl + O`，随后按 `Enter` 键确认保存。
* 按下快捷键 `Ctrl + X` 退出 Nano 编辑器。

#### 4. 使配置立即生效
在终端中执行以下命令刷新环境配置：
```bash
source ~/.bashrc
```

---

## 🚀 日常使用方法

配置完成后，今后无论是日常开发完毕还是需要同步备份，您只需要在 WSL 终端的任何路径下输入以下简短命令：

```bash
syncD
```

### 💡 关键机制说明
* **`--delete` 镜像同步**：如果在 WSL 中删除了某个文件，执行 `syncD` 后，Windows D 盘对应路径下的文件也会被同步删除，确保两端完全一致。
* **`--exclude` 智能过滤**：命令中已经自动为您排除了 `node_modules/`、`.venv/`、`__pycache__/` 以及 `.git/` 等巨型依赖和缓存目录。这能为您**节省 95% 以上的同步时间**并避免文件占用冲突。
