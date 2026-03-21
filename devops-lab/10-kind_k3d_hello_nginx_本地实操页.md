# kind / k3d + hello-nginx 本地实操页

## 1. 这一页做什么

前面的 `Kubernetes` 页面已经讲了概念和模板。

这一页把它们收束成一个真正可执行的本地实操目标：

1. 创建本地集群
2. 部署 `hello-nginx`
3. 查看 Pod / Deployment / Service
4. 删除集群

## 2. 实操目标

你这次不需要上来就学很多对象。

最小目标只有这些：

- 会创建集群
- 会应用 YAML
- 会看运行状态
- 会删除环境

## 3. 演练前检查

开始前，至少确认：

- Docker 正常
- `docker ps` 能执行
- 你已经看过 [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- 你已经看过 [07-kind_k3d本地练习模板页.md](D:/dev/source_code/vscode_study/devops-lab/07-kind_k3d%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0%E6%A8%A1%E6%9D%BF%E9%A1%B5.md)

## 4. 实操文件

先准备一个 `hello-nginx.yaml`：

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

当前工作区里已经给你准备了一份可直接复制的模板：

- [templates/k8s-hello-nginx/hello-nginx.yaml](D:/dev/source_code/vscode_study/devops-lab/templates/k8s-hello-nginx/hello-nginx.yaml)

## 5. 用 kind 实操

### 第 1 步：创建集群

```bash
kind create cluster --name devops-lab
```

### 第 2 步：检查节点

```bash
kubectl get nodes
```

### 第 3 步：部署应用

```bash
kubectl apply -f hello-nginx.yaml
```

### 第 4 步：查看资源

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

### 第 5 步：看详情

```bash
kubectl describe deployment hello-nginx
kubectl describe service hello-nginx
```

### 第 6 步：删除集群

```bash
kind delete cluster --name devops-lab
```

## 6. 用 k3d 实操

### 第 1 步：创建集群

```bash
k3d cluster create devops-lab
```

### 第 2 步：检查节点

```bash
kubectl get nodes
```

### 第 3 步：部署应用

```bash
kubectl apply -f hello-nginx.yaml
```

### 第 4 步：查看资源

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

### 第 5 步：删除集群

```bash
k3d cluster delete devops-lab
```

## 7. 你现在最该观察什么

这次实操里，最值得观察的是：

- `replicas: 2` 后到底起来了几个 Pod
- `Service` 是怎么通过 `selector` 找到 Pod 的
- `Deployment` 和 `Pod` 的关系

也就是说，这次重点不是“服务访问得多完整”，而是：

- 理解对象关系

## 8. 常见问题

### 1. 集群创建失败

优先检查：

- Docker 是否正常
- 本机资源是否够

### 2. `kubectl get nodes` 看不到节点

通常表示：

- 集群没有创建成功
- 当前上下文不对

### 3. Pod 起不来

可以先看：

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### 4. 一开始就想暴露外部访问

这一步先不强求。

当前阶段更重要的是：

- Deployment 正常
- Pod 正常
- Service 正常创建

## 9. 练习题

### 练习 1

直接复制模板 YAML，把副本数从 `2` 改成 `1`，再解释会发生什么。

### 练习 2

把 Deployment 名字改掉，再观察 `kubectl get deployments` 的输出变化。

### 练习 3

自己写一段 5 行以内的总结，解释：

- Pod
- Deployment
- Service

三者关系。

### 练习 4

记录你本地实操中遇到的第一个错误，以及你是怎么排查的。

## 10. 学到什么程度算过关

- 能按步骤创建和删除一个本地集群
- 能部署最小 `hello-nginx`
- 能查看 Pod / Deployment / Service
- 能说出自己最常见的一类错误是什么
