# Docker + GitHub Actions 最小部署演练

## 1. 这一页做什么

前面的内容已经把这些点拆开讲过了：

- `Docker`
- `GitHub Actions`
- 自动化运维

这一页把它们串成一个最小演练。

目标不是做复杂生产系统，而是先理解这条最小链路：

1. 本地能跑
2. 能容器化
3. 能用工作流自动检查
4. 能理解后续怎么走向部署

## 2. 演练目标

这个最小演练建议你用一个最简单的静态页面或小服务来理解。

你要得到的不是“炫的项目”，而是：

- 一个 `Dockerfile`
- 一个本地可运行容器
- 一个最小 `GitHub Actions` 工作流
- 一份你自己能讲清楚的部署链路

## 3. 最小项目结构

可以先假设一个最小静态页面项目结构：

```text
my-demo/
|-- index.html
|-- Dockerfile
`-- .github/
    `-- workflows/
        `-- demo-ci.yml
```

当前工作区里已经给你准备了一份可直接复制的模板：

- [templates/docker-actions-demo/index.html](D:/dev/source_code/vscode_study/devops-lab/templates/docker-actions-demo/index.html)
- [templates/docker-actions-demo/Dockerfile](D:/dev/source_code/vscode_study/devops-lab/templates/docker-actions-demo/Dockerfile)
- [templates/docker-actions-demo/.github/workflows/demo-ci.yml](D:/dev/source_code/vscode_study/devops-lab/templates/docker-actions-demo/.github/workflows/demo-ci.yml)

## 4. 最小页面示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <title>DevOps Demo</title>
  </head>
  <body>
    <h1>Hello DevOps</h1>
    <p>This is a minimal Docker + GitHub Actions demo.</p>
  </body>
</html>
```

## 5. 最小 Dockerfile

```dockerfile
FROM nginx:stable
COPY index.html /usr/share/nginx/html/index.html
```

这份 `Dockerfile` 的作用很简单：

- 以 `nginx` 作为基础镜像
- 把你的页面复制进去

## 6. 本地运行步骤

### 构建镜像

```bash
docker build -t devops-demo:local .
```

### 运行容器

```bash
docker run --rm -p 8080:80 devops-demo:local
```

### 验证结果

浏览器打开：

- `http://127.0.0.1:8080`

## 7. 最小 GitHub Actions 工作流

你现在不一定马上提交到远端仓库，但应该先看懂最小工作流。

```yaml
name: Demo CI

on:
  push:
  workflow_dispatch:

jobs:
  docker-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build image
        run: docker build -t devops-demo:ci .
```

### 这个 workflow 学的是什么

你要先看懂：

1. 推送代码会触发
2. 工作流会检出仓库
3. 工作流会尝试构建镜像
4. 如果镜像构建失败，就说明项目有问题

## 8. 如何和当前工作区对应

你这个工作区里已经有现成参考材料：

- `Docker`
  - [DOCKER_INSTALL_GUIDE.md](D:/dev/source_code/vscode_study/scripts/docker/DOCKER_INSTALL_GUIDE.md)
- `GitHub Actions`
  - [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)
  - [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)

所以这一页的重点不是替代它们，而是：

- 给你一个最小、自成闭环的练习模板

## 9. 最小部署怎么理解

当前阶段先不要把“部署”理解得太重。

你可以先把它理解成：

- 本地构建镜像
- 远端工作流验证镜像可构建
- 后续再扩展为推镜像仓库或发布页面

也就是说，这一页更偏：

- 最小部署演练入口

不是完整生产部署方案。

## 10. 练习题

### 练习 1

直接复制模板文件并跑通本地构建。

### 练习 2

在本地执行：

- `docker build`
- `docker run`

### 练习 3

把最小 workflow 保存成一个独立文件，解释每一步在做什么。

### 练习 4

在页面里再加一行版本信息，例如：

- `v0.1.0`

然后重新构建镜像并验证变化。

### 练习 5

用自己的话解释这条链路：

- 页面
- Docker
- GitHub Actions
- 最小部署

## 11. 学到什么程度算过关

- 能自己写最小 `Dockerfile`
- 能本地跑起一个最小容器
- 能看懂一个只做镜像构建的 workflow
- 能解释这条最小部署链路
