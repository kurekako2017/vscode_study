# GitHub 学生版学习与 DevOps 实践教程（含 Actions / Pages 示例）

> 目标：从“会用 GitHub”进阶到“能用 GitHub 做完整 DevOps 流程”。

## 1. 先搞清楚：GitHub 学生版怎么用最值

GitHub Student Developer Pack（学生权益）通常会覆盖以下学习价值（具体权益以官网当期为准）：

- GitHub 平台高级能力（如私有仓库协作、CI/CD、安全扫描等）
- 面向学生的开发工具或云资源优惠（第三方服务）
- 更适合做作品集与工程化实践的能力组合

**建议你把它当成“实战平台”，而不是“福利集合”**：

- 用 `Actions` 学 CI/CD
- 用 `Pages` 做个人技术网站/项目文档站
- 用 `Issues + Projects + PR` 学团队协作
- 用 `CodeQL + Dependabot` 学安全与依赖治理

---

## 2. 学习路径（建议 4 周）

## 第 1 周：GitHub 基础工程化

目标：形成稳定的开发节奏。

- 学会分支模型：`main`、`feature/*`、`fix/*`
- 每个需求走 `Issue -> Branch -> PR -> Review -> Merge`
- 使用 PR 模板和 Issue 模板（规范提交）
- 学会写可读的 `README`（运行方式、目录结构、截图）

## 第 2 周：GitHub Actions（CI）

目标：每次提交自动检查质量。

- 自动执行构建（Build）
- 自动执行测试（Test）
- 自动执行格式化/静态检查（Lint）
- PR 必须通过 CI 才允许合并

## 第 3 周：GitHub Pages（文档与展示）

目标：把成果公开展示。

- 发布个人主页（简历、项目、联系方式）
- 发布项目文档（安装、架构、API、截图）
- 配置自动部署：提交后自动更新网站

## 第 4 周：DevOps 串联

目标：形成端到端流水线。

- 从需求（Issue）到代码（PR）到验证（CI）到发布（Pages）
- 引入安全检查（CodeQL）和依赖自动更新（Dependabot）
- 用项目看板（Projects）追踪“待办 -> 进行中 -> 已完成”

---

## 3. 示例一：最小可用 GitHub Pages 项目

适合你先快速建立“可展示成果”。

### 目录结构

```text
softbs/
  student-pages-demo/
    index.html
    styles.css
.github/
  workflows/
    deploy-softbs-pages.yml
```

### `index.html`（示例）

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>我的 GitHub 学习主页</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <main>
    <h1>你好，我是 XXX</h1>
    <p>这里展示我的 GitHub Actions / Pages / DevOps 学习成果。</p>
    <ul>
      <li>项目 1：Java 电商系统 CI</li>
      <li>项目 2：LocalStack 云服务模拟</li>
      <li>项目 3：Python AI 学习实验</li>
    </ul>
  </main>
</body>
</html>
```

### `.github/workflows/deploy-softbs-pages.yml`

```yaml
name: Deploy softbs Pages

on:
  push:
    branches: ["main"]
    paths:
      - "softbs/student-pages-demo/**"
      - ".github/workflows/deploy-softbs-pages.yml"
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: softbs/student-pages-demo

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 启用步骤

1. 仓库设置中打开 `Settings -> Pages`，Source 选择 `GitHub Actions`。
2. 修改 `softbs/student-pages-demo` 下任意文件并推送到 `main`。
3. 在 Actions 中查看 `Deploy softbs Pages` 工作流运行成功。
4. 访问 Pages 地址，确认页面已更新。

---

## 4. 示例二：给你的 Java 项目加 CI（JtProject）

你的仓库已有 `java-projects/JtProject`，可直接加工作流。

### `.github/workflows/jtproject-ci.yml`

```yaml
name: JtProject CI

on:
  push:
    paths:
      - "java-projects/JtProject/**"
      - ".github/workflows/jtproject-ci.yml"
  pull_request:
    paths:
      - "java-projects/JtProject/**"
      - ".github/workflows/jtproject-ci.yml"

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: java-projects/JtProject

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'
          cache: maven

      - name: Make Maven wrapper executable
        run: chmod +x mvnw

      - name: Build and test
        run: ./mvnw -B clean test
```

### 说明

- 该工作流只在 `JtProject` 相关改动时触发（节省 CI 时间）。
- 先做 CI，不强求立即做自动部署。
- 后续可再加 `./mvnw -B clean verify` 或安全扫描。

---

## 5. 从“会用工具”到“会做 DevOps”

建议你按下面这个闭环练习：

1. **需求管理**：创建 Issue，写清验收标准。
2. **开发协作**：新建分支开发，提交 PR。
3. **质量门禁**：Actions 自动构建测试，通过才可合并。
4. **发布展示**：Pages 自动发布文档或主页。
5. **运行反馈**：在 Issue 记录故障与改进点，进入下一轮。

这就是一个最小 DevOps 循环：

`Plan -> Code -> Build/Test -> Release -> Feedback`

---

## 6. 建议你马上做的 3 个实践任务

### 任务 A：1 小时内完成个人主页上线

- 创建 `index.html`
- 配置 `deploy-softbs-pages.yml`
- 页面写清你的 3 个学习项目

### 任务 B：给 JtProject 接入 CI

- 添加 `jtproject-ci.yml`
- 开一个 PR，验证 CI 是否自动触发
- 在 PR 描述中贴上 CI 结果截图

### 任务 C：建立你的 DevOps 看板

- 新建 GitHub Project（看板）
- 列：`Todo / In Progress / Done`
- 每个任务绑定 Issue 和 PR

---

## 7. 常见问题（避坑）

- **Pages 没更新**：检查 `Settings -> Pages` 是否选了 `GitHub Actions`。
- **Actions 权限报错**：确认工作流 `permissions` 包含 `pages: write`、`id-token: write`（Pages 部署场景）。
- **CI 太慢**：使用路径过滤（`paths`）和缓存（Maven cache）。
- **只会写代码不会交付**：一定要把“文档站 + CI 状态 + 项目看板”一起做出来。

---

## 8. 你可以继续升级的方向

- 加 `Dependabot`：自动升级依赖并提 PR
- 加 `CodeQL`：自动安全扫描
- 用 `CODEOWNERS`：关键目录自动请求评审
- 用 `Environments`：区分测试与生产发布策略

---

## 9. 学习成果验收标准（自检）

如果下面 5 条你都达成，说明你已经具备初级 DevOps 实战能力：

- 能独立创建并维护一个公开项目主页（Pages）
- 能给项目接入自动 CI（Actions）
- 能使用 PR 流程协作并完成代码评审
- 能把任务管理（Issue/Project）和代码交付打通
- 能解释你的发布流程与质量门禁

---

## 10. 本仓库已落地文件（可直接使用）

- `softbs/student-pages-demo/index.html`
- `softbs/student-pages-demo/styles.css`
- `.github/workflows/deploy-softbs-pages.yml`
- `.github/workflows/jtproject-ci.yml`
- `.github/workflows/codeql.yml`
- `.github/dependabot.yml`

### 快速验证

1. 在仓库设置中确认 `Settings -> Pages -> Source` 为 `GitHub Actions`。
2. 修改 `softbs/student-pages-demo/index.html` 并推送，观察 `Deploy softbs Pages`。
3. 修改 `java-projects/JtProject` 任意文件并推送，观察 `JtProject CI`。
4. 修改 `java-projects/JtProject` 或 `python-projects/ai-lab` 并推送，观察 `CodeQL`。
5. 进入仓库 `Insights -> Dependency graph -> Dependabot`，确认已启用并等待周更 PR。
6. 全部通过后，把 Pages 链接和 CI/CodeQL 状态徽章贴到你的项目文档。

---

## 11. 执行版打卡计划（14 天）

- 入口文档：`softbs/github/GitHub学生版14天DevOps学习打卡计划.md`
- 建议每天投入：30~60 分钟
- 建议执行方式：每天一个最小可交付（Issue/PR/页面更新/工作流通过）
