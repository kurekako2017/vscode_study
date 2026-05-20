# Student Pages Demo — 部署指南（GitHub Actions + GitHub Pages）

本文档说明如何使用 GitHub Actions 自动将本仓库中的 `student-pages-demo` 示例发布到 GitHub Pages。

## 概要
- 目标：把 `softbs/github/student-pages-demo` 下的静态文件发布到 `gh-pages` 分支，并通过 GitHub Pages 提供站点访问。
- 优点：自动化部署、可回滚、与 CI 集成。

## 先决条件
- 仓库已推送到 GitHub，并且你对仓库有写权限。
- 示例目录：`softbs/github/student-pages-demo`（包含 `index.html`、`styles.css` 等）。

## 操作流程概览
1. 在仓库中添加一个 GitHub Actions workflow 文件：`.github/workflows/deploy-student-pages.yml`。
2. Workflow 会在 push 到 `main` 时将静态文件目录内容推送到 `gh-pages` 分支。
3. 在 GitHub 仓库 Settings → Pages 将发布源设置为 `gh-pages` / `root`。
4. 等待几分钟后站点即可访问：`https://<owner>.github.io/<repo>/`。

## 推荐的 Workflow 模板
将下面内容保存为 `.github/workflows/deploy-student-pages.yml`：

```yaml
name: Deploy Student Pages
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./softbs/github/student-pages-demo
          publish_branch: gh-pages
```

说明：
- `publish_dir` 指向仓库内要发布的静态文件目录。
- 使用 `GITHUB_TOKEN` 无需额外配置 secrets。
- `workflow_dispatch` 允许在 Actions 页面手动触发部署。

## 在 GitHub 上启用 Pages
1. 进入仓库 Settings → Pages。
2. 在 "Source" 中选择 `gh-pages` 分支，文件夹选择 `/ (root)`，保存。
3. 等待几分钟，页面将生效并显示站点 URL。

## 本地测试（可选）
在本地预览静态页面：

```bash
cd softbs/github/student-pages-demo
python -m http.server 8000
# 然后访问 http://localhost:8000
```

## 验证与回滚
- 在仓库的 Actions 页面查看 workflow 运行日志，确认 `peaceiris/actions-gh-pages` 步骤成功并将内容推送到 `gh-pages`。
- 若需回滚：在仓库中还原导致问题的 commit，或在 Pages 设置中临时切换发布源。

## 可选替代方案
- 将静态文件放到仓库根下的 `docs/` 并在 Settings → Pages 选择 `main` / `docs`（适合不想使用 Actions 的情况）。
- 也可使用 `JamesIves/github-pages-deploy-action`，配置方式与上类似。

## 常见问题
- 为什么看不到更新？——检查 Actions 日志和 Pages 设置，确认 `gh-pages` 分支被正确推送并作为发布源。
- 权限问题导致推送失败？——确认 workflow 使用的 `GITHUB_TOKEN` 有默认写入 `gh-pages` 的权限（仓库管理员未限制）。

---

如果需要，我可以：
- 1) 直接在仓库创建并提交上述 workflow 文件；
- 2) 立即触发一次手动部署。 

## 在 GitHub 上操作 Workflow（详细步骤）
下面是一步一步的具体操作，你可以直接按顺序执行。

1) 在本地创建并提交 workflow 文件（推荐）

```bash
# 切换到仓库目录
cd /path/to/your/local/repo

# 新建分支（可选，但推荐通过 PR 合并）
git checkout -b add-pages-workflow

# 创建工作流目录并把前面给出的 YAML 保存为
# .github/workflows/deploy-student-pages.yml
mkdir -p .github/workflows
# 使用你喜欢的编辑器创建并粘贴 YAML 内容

git add .github/workflows/deploy-student-pages.yml
git commit -m "ci: add GitHub Pages deploy workflow"
git push -u origin add-pages-workflow

# 在 GitHub 上打开 PR 并合并到 main，或直接推送到 main（根据权限）
```

2) 在 GitHub 上直接创建或编辑文件（可选）
- 打开仓库页面 → 点击 `Add file` → `Create new file`。
- 在文件名输入框填写 `.github/workflows/deploy-student-pages.yml`，粘贴 YAML 内容并 Commit 到 `main`（或新分支并打开 PR）。

3) 手动触发 workflow（如果启用了 `workflow_dispatch`）
- 打开仓库的 `Actions` 选项卡。
- 在左侧列表中选择 `Deploy Student Pages` workflow。
- 点击 `Run workflow` 按钮，选择分支（例如 `main`），再点击 `Run workflow`。

4) 观看运行日志并调试
- 点击正在运行或已完成的 workflow，选择具体 job（例如 `deploy`）。
- 展开每个 step 查看控制台日志，错误信息通常会指明原因（如找不到目录、权限不足等）。

5) 权限与审批
- `GITHUB_TOKEN` 在多数仓库可直接用于 push 到 `gh-pages`。若组织策略限制，管理员可能需要在仓库设置中授予权限或手动批准第一次运行。
- 若 workflow 来自 fork，默认会被禁用，管理员需允许来自 fork 的工作流运行。

6) 管理 Secrets（如需要额外凭证）
- 进入仓库 Settings → Secrets and variables → Actions，新增自定义 Secret。
- 在 workflow 中通过 `${{ secrets.YOUR_SECRET }}` 引用。

7) 启用 GitHub Pages（若尚未启用）
- 进入仓库 Settings → Pages，选择 `gh-pages` 分支和 `/ (root)`，保存。

8) 常见问题与快速定位
- 看不到更新：确认 workflow 成功将内容推送到 `gh-pages` 分支并且 Pages 的 Source 已设置为 `gh-pages`。
- 推送失败：检查 Actions 日志，确认 `GITHUB_TOKEN` 权限或组织策略；尝试用个人 PAT（作为 secret）代替 `GITHUB_TOKEN`（仅在必要时）。

按以上步骤操作，你就可以在 GitHub 网站上创建、运行并管理自动化部署流程。如果你希望我现在在仓库中添加并提交该 workflow 文件，我可以为你创建分支并提交文件（请确认是否直接合并到 `main` 或先通过 PR）。
