# DevOps / SRE Quick Reference

## 1. 最小学习顺序

1. `Docker`
2. `CI/CD`
3. 自动化运维
4. `Kubernetes`
5. 监控与可观测性
6. `Prometheus / Grafana`
7. `docker-compose` 最小监控栈

一句话版本：

- `Docker -> GitHub Actions -> 脚本排障 -> kind / k3d -> 监控意识 -> 最小监控栈 -> 真正跑起来`

## 2. 当前工作区最重要入口

- [README.md](D:/dev/source_code/vscode_study/devops-lab/README.md)
- [01-学习路线.md](D:/dev/source_code/vscode_study/devops-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
- [02-Docker与容器.md](D:/dev/source_code/vscode_study/devops-lab/02-Docker%E4%B8%8E%E5%AE%B9%E5%99%A8.md)
- [03-CI_CD与自动化运维.md](D:/dev/source_code/vscode_study/devops-lab/03-CI_CD%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BF%90%E7%BB%B4.md)
- [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [11-监控与可观测性入口.md](D:/dev/source_code/vscode_study/devops-lab/11-%E7%9B%91%E6%8E%A7%E4%B8%8E%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%85%A5%E5%8F%A3.md)
- [12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [13-docker-compose_最小监控栈演练页.md](D:/dev/source_code/vscode_study/devops-lab/13-docker-compose_%E6%9C%80%E5%B0%8F%E7%9B%91%E6%8E%A7%E6%A0%88%E6%BC%94%E7%BB%83%E9%A1%B5.md)

## 3. 最重要现成材料

### Docker

- [DOCKER_INSTALL_GUIDE.md](D:/dev/source_code/vscode_study/scripts/DOCKER_INSTALL_GUIDE.md)
- [TROUBLESHOOTING.md](D:/dev/source_code/vscode_study/localstack-lab/TROUBLESHOOTING.md)
- [如何查看LocalStack日志.md](D:/dev/source_code/vscode_study/localstack-lab/%E5%A6%82%E4%BD%95%E6%9F%A5%E7%9C%8BLocalStack%E6%97%A5%E5%BF%97.md)

### GitHub Actions

- [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)
- [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)
- [06-GitHub_Actions最小示例项目页.md](D:/dev/source_code/vscode_study/devops-lab/06-GitHub_Actions%E6%9C%80%E5%B0%8F%E7%A4%BA%E4%BE%8B%E9%A1%B9%E7%9B%AE%E9%A1%B5.md)

### Kubernetes

- [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [07-kind_k3d本地练习模板页.md](D:/dev/source_code/vscode_study/devops-lab/07-kind_k3d%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0%E6%A8%A1%E6%9D%BF%E9%A1%B5.md)
- [10-kind_k3d_hello_nginx_本地实操页.md](D:/dev/source_code/vscode_study/devops-lab/10-kind_k3d_hello_nginx_%E6%9C%AC%E5%9C%B0%E5%AE%9E%E6%93%8D%E9%A1%B5.md)

### 监控与可观测性

- [11-监控与可观测性入口.md](D:/dev/source_code/vscode_study/devops-lab/11-%E7%9B%91%E6%8E%A7%E4%B8%8E%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%85%A5%E5%8F%A3.md)
- [monitor-status.ps1](D:/dev/source_code/vscode_study/scripts/monitor-status.ps1)
- [diagnostic.ps1](D:/dev/source_code/vscode_study/scripts/diagnostic.ps1)
- [如何查看LocalStack日志.md](D:/dev/source_code/vscode_study/localstack-lab/%E5%A6%82%E4%BD%95%E6%9F%A5%E7%9C%8BLocalStack%E6%97%A5%E5%BF%97.md)

### 最小监控栈

- [12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [13-docker-compose_最小监控栈演练页.md](D:/dev/source_code/vscode_study/devops-lab/13-docker-compose_%E6%9C%80%E5%B0%8F%E7%9B%91%E6%8E%A7%E6%A0%88%E6%BC%94%E7%BB%83%E9%A1%B5.md)
- [prometheus-grafana-demo/README.md](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/README.md)

## 4. 最小命令速查

### Docker

```bash
docker --version
docker ps
docker build -t demo:local .
docker run --rm -p 8080:80 demo:local
docker logs <container-id>
```

### kind

```bash
kind create cluster --name devops-lab
kubectl get nodes
kubectl apply -f hello-nginx.yaml
kind delete cluster --name devops-lab
```

### k3d

```bash
k3d cluster create devops-lab
kubectl get nodes
kubectl apply -f hello-nginx.yaml
k3d cluster delete devops-lab
```

## 5. 最小模板入口

- [docker-actions-demo/README.md](D:/dev/source_code/vscode_study/devops-lab/templates/docker-actions-demo/README.md)
- [k8s-hello-nginx/README.md](D:/dev/source_code/vscode_study/devops-lab/templates/k8s-hello-nginx/README.md)

## 6. 常见误区

- 只看概念，不跑脚本
- 只会 `Docker`，不会看工作流
- 一上来就冲 `Kubernetes`，跳过容器基础
- 只会跑成功路径，不会看日志和报错

## 7. 当前最大缺口

- `Kubernetes` 仍然是入门级，不是完整项目线
- 监控 / 告警 / 可观测性材料虽然已经有可跑模板，但还不是完整生产级体系
- 生产级部署、安全、密钥管理还没有单独展开
