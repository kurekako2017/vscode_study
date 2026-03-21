# Kubernetes 最小入门

## 1. 为什么现在补这一块

在 `DevOps / SRE` 这条线上，`Kubernetes` 经常会被提到。

但对当前学习阶段来说，重点不是一上来就学复杂集群，而是先理解：

- 为什么只有 `Docker` 还不够
- `Kubernetes` 多解决了什么问题

可以先把它理解成：

- `Docker` 解决“怎么把一个应用装进容器并跑起来”
- `Kubernetes` 解决“很多容器怎么稳定地管理、扩缩、发布和服务发现”

## 2. 这一章要掌握什么

这一章至少先掌握这些概念：

- `Pod`
- `Deployment`
- `Service`
- `kubectl`
- 声明式配置

当前阶段不要求你立刻搭完整生产集群。

目标只是：

- 建立最小可用理解

## 3. 最小概念图

可以先这样记：

- `Pod`
  - 最小运行单元
- `Deployment`
  - 管理一组 Pod，负责副本数和滚动更新
- `Service`
  - 给 Pod 提供稳定访问入口
- `kubectl`
  - 和集群交互的命令行工具

如果压缩成一句话：

- `Deployment` 管 Pod
- `Service` 暴露访问
- `kubectl` 负责操作

## 4. 为什么会需要 Kubernetes

单个容器用 `Docker` 跑起来很方便。

但一旦你开始遇到这些需求：

- 服务挂了要自动拉起
- 需要多个副本
- 需要滚动更新
- 需要统一暴露访问
- 需要多个服务协同

就会开始碰到编排问题。

这时 `Kubernetes` 才真正有意义。

所以它不是“更高级的 Docker”，而是：

- 容器编排平台

## 5. 最小示例

下面给一个最小 `Deployment + Service` 示例。

你现在不一定马上运行它，但应该先看懂结构。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-nginx
  template:
    metadata:
      labels:
        app: hello-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:stable
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: hello-nginx
spec:
  selector:
    app: hello-nginx
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

### 这个最小示例学的是什么

你要先看懂 5 个点：

1. `Deployment` 定义了要跑几个副本
2. `Pod` 是由模板生成出来的
3. `labels` 和 `selector` 用来关联对象
4. `Service` 用来稳定访问 Pod
5. 这是一种声明式写法，不是逐条手工启动容器

## 6. 最小命令

当前阶段先认识这几个命令就够了：

```bash
kubectl apply -f hello-nginx.yaml
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe pod <pod-name>
```

你现在不用急着背全。

先知道：

- `apply`
- `get`
- `describe`

这三类命令是最常见的基础操作。

## 7. 和当前工作区的关系

你这个工作区里，`Kubernetes` 还没有完整的实战项目。

所以这篇的定位是：

- 补概念
- 给后续扩展留入口

当前最接近的参考仍然是：

- [Codespaces学习要点.md](D:/dev/source_code/vscode_study/softbs/github/Codespaces%E5%AD%A6%E4%B9%A0%E8%A6%81%E7%82%B9.md)

其中和 `Kubernetes` 相关的关键词包括：

- `kubectl`
- `kind`
- `k3d`
- 容器化与云原生入门

## 8. 当前阶段最推荐的补法

建议顺序是：

1. 先把 `Docker` 学稳
2. 先把 `CI/CD` 和自动化脚本看懂
3. 再补 `Kubernetes` 基础概念
4. 后面再补 `kind` 或 `k3d` 的本地练习

不要反过来。

## 9. 练习题

### 练习 1

用自己的话解释：

- `Docker` 解决了什么
- `Kubernetes` 多解决了什么

### 练习 2

看懂上面的 YAML，并指出：

- 哪一段是 `Deployment`
- 哪一段是 `Service`

### 练习 3

解释 `replicas: 2` 表示什么。

### 练习 4

解释为什么 `labels` 和 `selector` 要对上。

### 练习 5

整理出你当前最不理解的 3 个 `Kubernetes` 术语。

## 10. 学到什么程度算过关

- 能解释 `Pod`、`Deployment`、`Service` 是什么
- 能看懂最小 YAML 结构
- 能说出 `Docker` 和 `Kubernetes` 的区别
- 能说明为什么当前阶段先学基础，不急着上复杂集群
