# 使用 VS Code 提交代码到 GitHub 仓库的教程

## 前置条件
1. **安装 Git**：确保你的电脑上已经安装了 Git。如果未安装，可以从 [Git 官网](https://git-scm.com/) 下载并安装。
2. **安装 VS Code**：确保已安装 Visual Studio Code。
3. **配置 GitHub 账户**：
   - 注册一个 GitHub 账户（如果还没有）。
   - 在本地配置 Git 用户名和邮箱：
     ```bash
     git config --global user.name "你的用户名"
     git config --global user.email "你的邮箱"
     ```
4. **安装 VS Code 的 Git 插件**：
   - 打开 VS Code，进入扩展市场，搜索并安装 `GitHub Pull Requests and Issues` 插件。

---

## 步骤 1：克隆 GitHub 仓库到本地
1. 打开 VS Code。
2. 按下 `Ctrl+Shift+P` 打开命令面板，输入 `Git: Clone` 并选择。
3. 输入 GitHub 仓库的 URL（例如 `https://github.com/username/repository.git`）。
4. 选择本地保存代码的文件夹。
5. 克隆完成后，VS Code 会提示你打开该文件夹，点击 **打开**。

---

## 步骤 2：修改代码并提交到本地仓库
1. 在 VS Code 中打开需要编辑的文件，进行修改。
2. 保存修改（`Ctrl+S`）。
3. 点击左侧的 **源代码管理图标**（类似树枝的图标）。
4. 在 "更改" 区域查看修改的文件。
5. 输入提交信息（如 "修复了一个 bug"）。
6. 点击 **✔ 提交** 按钮，将更改提交到本地仓库。

---

## 步骤 3：推送更改到 GitHub
1. 确保已经连接到远程仓库。
   - 如果未连接，使用以下命令添加远程仓库：
     ```bash
     git remote add origin https://github.com/username/repository.git
     ```
2. 点击 VS Code 下方的 **同步更改** 按钮，或者在终端中运行：
   ```bash
   git push origin main
   ```
   > 注意：如果你的分支不是 `main`，请将 `main` 替换为当前分支名。
3. 如果是第一次推送，可能需要输入 GitHub 的用户名和密码。

---

## 步骤 4：从 GitHub 拉取最新代码
1. 点击 VS Code 下方的 **同步更改** 按钮，或者在终端中运行：
   ```bash
   git pull origin main
   ```
2. 如果有冲突，VS Code 会提示你解决冲突。

---

## 常见问题
1. **无法推送代码**：
   - 检查是否有推送权限。
   - 确保远程仓库 URL 正确。
2. **冲突问题**：
   - 使用 VS Code 提供的冲突解决工具，手动合并冲突后提交。
3. **认证失败**：
   - 确保 GitHub 账户的用户名和密码正确。
   - 建议使用 SSH 密钥认证，参考 [GitHub SSH 配置教程](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)。

---

通过以上步骤，你可以轻松地使用 VS Code 将代码提交到 GitHub 仓库！