# docker-actions-demo

最小可运行的 `Docker + GitHub Actions` 练习模板。

这个模板解决的问题是：

- 用最小静态页面练 `Dockerfile`
- 本地构建并运行容器
- 用最小 `GitHub Actions` 工作流验证镜像能构建

## 文件结构

```text
docker-actions-demo/
|-- index.html
|-- Dockerfile
|-- README.md
`-- .github/
    `-- workflows/
        `-- demo-ci.yml
```

## 本地运行

构建镜像：

```bash
docker build -t devops-demo:local .
```

运行容器：

```bash
docker run --rm -p 8080:80 devops-demo:local
```

浏览器访问：

- `http://127.0.0.1:8080`

## GitHub Actions

模板里自带：

- `.github/workflows/demo-ci.yml`

它会做最小检查：

- 检出代码
- 构建 Docker 镜像

## 你可以先改什么

- 改 `index.html` 里的标题
- 改版本号
- 给 workflow 加一个 `echo` 步骤

## 对应教程

- [09-Docker_GitHub_Actions_最小部署演练.md](D:/dev/source_code/vscode_study/devops-lab/09-Docker_GitHub_Actions_%E6%9C%80%E5%B0%8F%E9%83%A8%E7%BD%B2%E6%BC%94%E7%BB%83.md)
- [08-自己写第一个GitHub_Actions_Workflow.md](D:/dev/source_code/vscode_study/devops-lab/08-%E8%87%AA%E5%B7%B1%E5%86%99%E7%AC%AC%E4%B8%80%E4%B8%AAGitHub_Actions_Workflow.md)
