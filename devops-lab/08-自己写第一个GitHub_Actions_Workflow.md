# 自己写第一个 GitHub Actions Workflow

## 1. 为什么要补这一页

前一页解决的是：

- 怎么读懂别人写的 workflow

这一页解决的是：

- 你自己怎么写第一个最小 workflow

目标不是一开始写复杂流水线，而是先写一个最小可运行版本。

## 2. 先说结论

如果你第一次自己写 `GitHub Actions`，最小版本只要做到：

1. 指定触发条件
2. 定义一个 job
3. 跑 1 到 2 个 step

就够了。

## 3. 最小工作流长什么样

下面是一个最小示例：

```yaml
name: Hello Workflow

on:
  push:
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Print message
        run: echo "Hello from GitHub Actions"
```

## 4. 这段 YAML 在做什么

可以这样理解：

- `name`
  - 工作流名字
- `on`
  - 什么时候触发
- `jobs`
  - 要做哪些工作
- `runs-on`
  - 在什么机器环境里执行
- `steps`
  - 一步一步做什么

## 5. 推荐文件位置

如果你自己以后要加 workflow，文件一般放在：

- `.github/workflows/`

例如：

- `.github/workflows/hello-workflow.yml`

## 6. 第一个 workflow 最推荐怎么写

第一次最适合做下面两种之一：

### 方式 1：打印一行字

优点：

- 最简单
- 最容易确认流程是通的

### 方式 2：打印仓库文件列表

例如：

```yaml
name: List Files

on:
  workflow_dispatch:

jobs:
  list-files:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: List files
        run: ls -la
```

优点：

- 能直观看到仓库已经被检出

## 7. 和当前工作区现有文件怎么对应

你可以把这一页和这些真实工作流对照着看：

- [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)
- [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)

理解顺序建议是：

1. 先看这页的最小版本
2. 再看 `jtproject-ci.yml`
3. 再看 `deploy-softbs-pages.yml`

这样不会一开始就被复杂工作流结构压住。

## 8. 最小练习模板

如果你自己要写第一个练习版，可以直接按这个模板改：

```yaml
name: My First Workflow

on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Show current directory
        run: pwd

      - name: Show files
        run: ls -la
```

## 9. 常见错误

### 1. 文件位置放错

工作流文件要放在：

- `.github/workflows/`

### 2. YAML 缩进错

这是最常见的问题之一。

如果缩进错了，工作流可能直接无法识别。

### 3. 一开始就写太复杂

例如一开始就想做：

- 多 job
- 多环境
- 构建加部署加通知

这样很容易卡住。

第一次更好的策略是：

- 先让它跑起来

## 10. 练习题

### 练习 1

自己写一个只会打印一句话的 workflow。

### 练习 2

再改成会打印当前目录和文件列表。

### 练习 3

指出你写的 workflow 里：

- 触发条件是什么
- job 名是什么
- 每个 step 在做什么

### 练习 4

对照 [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)，找出它比你的最小 workflow 多了哪些部分。

## 11. 学到什么程度算过关

- 能自己写一个最小 workflow
- 知道 workflow 文件该放哪
- 能解释 `on / jobs / steps / runs-on`
- 能把最小 workflow 和真实项目 workflow 对上
