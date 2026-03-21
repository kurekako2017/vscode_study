# GitHub Actions 最小示例项目页

## 1. 为什么要单独看这一页

因为 `GitHub Actions` 是你这个工作区里最直接、最真实的 `CI/CD` 示例来源。

与其只看概念，不如直接看现成工作流：

- [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)
- [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)

这两份文件刚好可以分别代表：

- 最小 `CI`
- 最小 `CD`

## 2. 先说结论

如果只记最重要的差别，可以记成：

- `CI`：代码变更后自动检查、构建、测试
- `CD`：代码变更后自动部署或发布

在你这个工作区里：

- `jtproject-ci.yml` 偏 `CI`
- `deploy-softbs-pages.yml` 偏 `CD`

## 3. 最小 CI 示例

可以先看：

- [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)

这个工作流做的事情很典型：

1. 代码变更触发
2. 检出仓库
3. 安装 Java
4. 运行 Maven 测试

对应关键结构是：

```yaml
name: JtProject CI

on:
  push:
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
      - run: ./mvnw -B clean test
```

### 这个最小 CI 示例学的是什么

你要先看懂：

1. `on` 是触发条件
2. `jobs` 是要执行的工作
3. `steps` 是具体步骤
4. `uses` 是复用官方 action
5. `run` 是直接执行命令

## 4. 最小 CD 示例

再看：

- [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)

这个工作流代表的是最小部署流程：

1. 代码推送到 `main`
2. 检出仓库
3. 配置 Pages
4. 上传产物
5. 部署到 GitHub Pages

对应关键结构是：

```yaml
name: Deploy softbs Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
      - uses: actions/deploy-pages@v4
```

### 这个最小 CD 示例学的是什么

你要先看懂：

1. 部署也可以由代码变更自动触发
2. `workflow_dispatch` 表示支持手动触发
3. 有些工作流不是执行 shell，而是串联现成 action
4. 部署前通常要先准备产物

## 5. 最小工作流怎么读

你现在读任意一个 `GitHub Actions` 文件，都可以按这个顺序看：

1. 什么时候触发
2. 在什么机器上运行
3. 有几个 job
4. 每个 job 的 step 在做什么
5. 最终产出是什么

只要能把这 5 个问题说清楚，这份工作流你就算基本读懂了。

## 6. 当前工作区里还能继续看的文件

如果你看完上面两份，还可以继续看：

- [jtproject-deploy.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-deploy.yml)
- [jtproject-deploy-safe.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-deploy-safe.yml)

这两份更适合用来比较：

- 普通部署
- 更安全或更谨慎的部署方式

## 7. 练习题

### 练习 1

用自己的话解释：

- `jtproject-ci.yml` 为什么属于 `CI`

### 练习 2

用自己的话解释：

- `deploy-softbs-pages.yml` 为什么属于 `CD`

### 练习 3

指出一份工作流里的：

- 触发条件
- job 名
- 最关键的 2 到 3 个 step

### 练习 4

比较 `jtproject-deploy.yml` 和 `jtproject-deploy-safe.yml`，写下你观察到的差异。

### 练习 5

自己写一段 5 到 8 行的最小工作流草稿，哪怕只是：

- 检出代码
- 打印一行字

## 8. 学到什么程度算过关

- 能解释 `CI` 和 `CD` 的区别
- 能看懂最小 `GitHub Actions` 结构
- 能读懂当前工作区里一份真实工作流
- 能指出一份工作流是偏检查、还是偏部署
