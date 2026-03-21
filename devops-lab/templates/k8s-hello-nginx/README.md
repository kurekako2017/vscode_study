# k8s-hello-nginx

最小可运行的本地 `Kubernetes` 练习模板。

这个模板解决的问题是：

- 用最小 `Deployment + Service` YAML 练习
- 在 `kind` 或 `k3d` 本地集群里部署
- 查看 `Pod / Deployment / Service`

## 文件结构

```text
k8s-hello-nginx/
|-- hello-nginx.yaml
`-- README.md
```

## 用 kind 运行

创建集群：

```bash
kind create cluster --name devops-lab
```

部署：

```bash
kubectl apply -f hello-nginx.yaml
```

查看：

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

删除：

```bash
kind delete cluster --name devops-lab
```

## 用 k3d 运行

创建集群：

```bash
k3d cluster create devops-lab
```

部署：

```bash
kubectl apply -f hello-nginx.yaml
```

查看：

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

删除：

```bash
k3d cluster delete devops-lab
```

## 你可以先改什么

- 把副本数从 `2` 改成 `1`
- 修改 `metadata.name`
- 修改 `image`

## 对应教程

- [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [07-kind_k3d本地练习模板页.md](D:/dev/source_code/vscode_study/devops-lab/07-kind_k3d%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0%E6%A8%A1%E6%9D%BF%E9%A1%B5.md)
- [10-kind_k3d_hello_nginx_本地实操页.md](D:/dev/source_code/vscode_study/devops-lab/10-kind_k3d_hello_nginx_%E6%9C%AC%E5%9C%B0%E5%AE%9E%E6%93%8D%E9%A1%B5.md)
