# kind / k3d 本地练习模板页

## 1. 为什么补这一页

前面的 `Kubernetes` 教程主要解决的是：

- 概念怎么理解

这一页解决的是：

- 如果你后面要在本机练，最小路径怎么走

当前工作区里还没有现成的 `kind` 或 `k3d` 实战项目，所以这一页的定位是：

- 练习模板
- 环境准备清单
- 最小命令索引

## 2. 先说结论

如果你只是想本地练 `Kubernetes`，比较常见的两个轻量方案是：

- `kind`
- `k3d`

可以先粗略理解成：

- `kind`
  - 用 Docker 容器跑 Kubernetes 集群
- `k3d`
  - 用 Docker 跑轻量版 `k3s` 集群

对初学者来说，两者都可以。

## 3. 当前阶段推荐怎么选

可以先这样选：

- 如果你更想贴近“标准 Kubernetes 概念”，先试 `kind`
- 如果你更想要轻量和启动快，也可以试 `k3d`

如果你不想一开始纠结太多：

- 先选一个就行

## 4. 开始前的最小前提

在当前工作区环境里，开始前至少确认：

- Docker 正常
- 能执行 `docker ps`
- 你已经看过 [02-Docker与容器.md](D:/dev/source_code/vscode_study/devops-lab/02-Docker%E4%B8%8E%E5%AE%B9%E5%99%A8.md)
- 你已经看过 [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)

## 5. 最小练习目标

这一页建议的最小目标不是：

- 学完整集群管理

而是：

1. 创建本地集群
2. 确认节点正常
3. 部署一个最小应用
4. 查看 Pod / Deployment / Service
5. 删除集群

## 6. kind 最小模板

### 最小步骤

1. 安装 `kind`
2. 创建集群
3. 用 `kubectl` 查看节点
4. 部署最小 YAML
5. 删除集群

### 最小命令

```bash
kind create cluster --name devops-lab
kubectl get nodes
kubectl apply -f hello-nginx.yaml
kubectl get pods
kubectl get deployments
kubectl get services
kind delete cluster --name devops-lab
```

## 7. k3d 最小模板

### 最小步骤

1. 安装 `k3d`
2. 创建集群
3. 用 `kubectl` 查看节点
4. 部署最小 YAML
5. 删除集群

### 最小命令

```bash
k3d cluster create devops-lab
kubectl get nodes
kubectl apply -f hello-nginx.yaml
kubectl get pods
kubectl get deployments
kubectl get services
k3d cluster delete devops-lab
```

## 8. 可复用的最小 YAML

你可以直接复用上一页里的最小示例：

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

## 9. 最小检查点

跑完后，至少检查这些：

- `kubectl get nodes`
  - 有节点
- `kubectl get pods`
  - Pod 正常起来
- `kubectl get deployments`
  - 副本数符合预期
- `kubectl get services`
  - Service 已创建

## 10. 常见问题

### 1. Docker 没起来

这是最常见的问题。

先回去检查：

- Docker Desktop 是否正常
- `docker ps` 是否能执行

### 2. `kubectl` 能执行，但没有上下文

这通常表示：

- 集群没创建成功
- 或 kubeconfig 没切过去

### 3. Pod 起不来

先看：

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### 4. 一开始就想学太多对象

当前阶段不要急着学：

- Ingress
- StatefulSet
- Helm
- Operator

先把：

- Pod
- Deployment
- Service

这 3 个打牢更重要。

## 11. 练习题

### 练习 1

在纸上或文档里写出你更想先试 `kind` 还是 `k3d`，以及原因。

### 练习 2

把最小 YAML 保存成 `hello-nginx.yaml`，解释每个字段大概在做什么。

### 练习 3

写出你准备执行的 5 条最小命令。

### 练习 4

整理一份“本地 k8s 练习前检查清单”。

## 12. 学到什么程度算过关

- 知道 `kind` 和 `k3d` 是干什么的
- 能写出最小练习步骤
- 能看懂最小部署 YAML
- 能说出本地练习最常见的 2 到 3 个问题
