# DevOps Lab

面向当前工作区已有材料整理的 `DevOps / SRE` 学习入口。

这条线不是从零堆概念，而是优先复用你这个工作区里已经存在的：

- `Docker` 教程
- `CI/CD` 工作流示例
- 自动化运维脚本
- 日志与排障资料

当前这条线的现实情况是：

- `Docker`：材料较多
- `CI/CD`：已有真实工作流示例
- 自动化运维：有脚本和排障资料
- `Kubernetes`：只有入门入口，仍是缺口
- 监控与可观测性：有日志和检查脚本基础，但还没有平台化教程
- `Prometheus / Grafana`：现在补到了最小入门层
- `docker-compose` 最小监控栈：现在有可直接运行模板

## 快速入口

如果你现在只想知道“先看什么”，直接按这个顺序：

1. [01-学习路线.md](D:/dev/source_code/vscode_study/devops-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
2. [02-Docker与容器.md](D:/dev/source_code/vscode_study/devops-lab/02-Docker%E4%B8%8E%E5%AE%B9%E5%99%A8.md)
3. [03-CI_CD与自动化运维.md](D:/dev/source_code/vscode_study/devops-lab/03-CI_CD%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BF%90%E7%BB%B4.md)
4. [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
5. [06-GitHub_Actions最小示例项目页.md](D:/dev/source_code/vscode_study/devops-lab/06-GitHub_Actions%E6%9C%80%E5%B0%8F%E7%A4%BA%E4%BE%8B%E9%A1%B9%E7%9B%AE%E9%A1%B5.md)
6. [07-kind_k3d本地练习模板页.md](D:/dev/source_code/vscode_study/devops-lab/07-kind_k3d%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0%E6%A8%A1%E6%9D%BF%E9%A1%B5.md)
7. [08-自己写第一个GitHub_Actions_Workflow.md](D:/dev/source_code/vscode_study/devops-lab/08-%E8%87%AA%E5%B7%B1%E5%86%99%E7%AC%AC%E4%B8%80%E4%B8%AAGitHub_Actions_Workflow.md)
8. [09-Docker_GitHub_Actions_最小部署演练.md](D:/dev/source_code/vscode_study/devops-lab/09-Docker_GitHub_Actions_%E6%9C%80%E5%B0%8F%E9%83%A8%E7%BD%B2%E6%BC%94%E7%BB%83.md)
9. [10-kind_k3d_hello_nginx_本地实操页.md](D:/dev/source_code/vscode_study/devops-lab/10-kind_k3d_hello_nginx_%E6%9C%AC%E5%9C%B0%E5%AE%9E%E6%93%8D%E9%A1%B5.md)
10. [11-监控与可观测性入口.md](D:/dev/source_code/vscode_study/devops-lab/11-%E7%9B%91%E6%8E%A7%E4%B8%8E%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%85%A5%E5%8F%A3.md)
11. [12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
12. [13-docker-compose_最小监控栈演练页.md](D:/dev/source_code/vscode_study/devops-lab/13-docker-compose_%E6%9C%80%E5%B0%8F%E7%9B%91%E6%8E%A7%E6%A0%88%E6%BC%94%E7%BB%83%E9%A1%B5.md)

## 这套资料怎么用

建议按下面这个方式使用：

1. 先看一篇教程文档
2. 再跑工作区里的对应示例
3. 再自己改一版脚本或配置
4. 再进入下一篇

也就是说，不要只看概念。

更好的节奏是：

- 教程负责讲清思路
- 工作区里的现成文件负责给你真实例子
- 自己改脚本和配置负责真正学会

## 主线结论

如果只记一条线，记这个就够了：

- `Docker -> CI/CD -> 自动化运维 -> Kubernetes 基础 -> 监控与可观测性入口 -> Prometheus / Grafana 最小入门 -> docker-compose 最小监控栈`

对应的学习原则是：

- 先把容器和脚本用起来
- 先看真实工作流
- 先学会排障和日志
- 再补 `Kubernetes`
- 最后把状态检查、日志和监控意识串起来
- 再推进到最小监控栈
- 再把最小模板真正跑起来

## 每一篇是干什么的

- [01-学习路线.md](D:/dev/source_code/vscode_study/devops-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
  - 给出学习顺序和当前工作区里的材料分布
- [02-Docker与容器.md](D:/dev/source_code/vscode_study/devops-lab/02-Docker%E4%B8%8E%E5%AE%B9%E5%99%A8.md)
  - 学 `Docker Desktop`、容器、日志、排障、LocalStack 相关示例
- [03-CI_CD与自动化运维.md](D:/dev/source_code/vscode_study/devops-lab/03-CI_CD%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BF%90%E7%BB%B4.md)
  - 学 `GitHub Actions`、部署工作流、脚本化运维和状态检查
- [04-Kubernetes入口.md](D:/dev/source_code/vscode_study/devops-lab/04-Kubernetes%E5%85%A5%E5%8F%A3.md)
  - 说明当前工作区里的 `Kubernetes` 缺口和后续补法
- [05-Kubernetes最小入门.md](D:/dev/source_code/vscode_study/devops-lab/05-Kubernetes%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
  - 补最小 `Kubernetes` 概念和 YAML 结构
- [06-GitHub_Actions最小示例项目页.md](D:/dev/source_code/vscode_study/devops-lab/06-GitHub_Actions%E6%9C%80%E5%B0%8F%E7%A4%BA%E4%BE%8B%E9%A1%B9%E7%9B%AE%E9%A1%B5.md)
  - 用当前工作区真实工作流讲最小 `CI/CD`
- [07-kind_k3d本地练习模板页.md](D:/dev/source_code/vscode_study/devops-lab/07-kind_k3d%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0%E6%A8%A1%E6%9D%BF%E9%A1%B5.md)
  - 补本地 `kind / k3d` 练习路径
- [08-自己写第一个GitHub_Actions_Workflow.md](D:/dev/source_code/vscode_study/devops-lab/08-%E8%87%AA%E5%B7%B1%E5%86%99%E7%AC%AC%E4%B8%80%E4%B8%AAGitHub_Actions_Workflow.md)
  - 补自己写第一个 workflow 的最小教程
- [09-Docker_GitHub_Actions_最小部署演练.md](D:/dev/source_code/vscode_study/devops-lab/09-Docker_GitHub_Actions_%E6%9C%80%E5%B0%8F%E9%83%A8%E7%BD%B2%E6%BC%94%E7%BB%83.md)
  - 补一个真正可串起来的 `Docker + GitHub Actions` 最小演练
- [10-kind_k3d_hello_nginx_本地实操页.md](D:/dev/source_code/vscode_study/devops-lab/10-kind_k3d_hello_nginx_%E6%9C%AC%E5%9C%B0%E5%AE%9E%E6%93%8D%E9%A1%B5.md)
  - 补一个真正可执行的本地 `Kubernetes` 小演练
- [11-监控与可观测性入口.md](D:/dev/source_code/vscode_study/devops-lab/11-%E7%9B%91%E6%8E%A7%E4%B8%8E%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%85%A5%E5%8F%A3.md)
  - 补日志、状态检查、最小指标意识和后续监控平台补法
- [12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
  - 补 `Prometheus`、`Grafana`、最小监控栈和后续模板方向
- [13-docker-compose_最小监控栈演练页.md](D:/dev/source_code/vscode_study/devops-lab/13-docker-compose_%E6%9C%80%E5%B0%8F%E7%9B%91%E6%8E%A7%E6%A0%88%E6%BC%94%E7%BB%83%E9%A1%B5.md)
  - 把 `Prometheus + Grafana + demo-app` 做成真正可跑的最小演练

## 当前工作区里最值得先看的现成材料

### Docker

- [DOCKER_INSTALL_GUIDE.md](D:/dev/source_code/vscode_study/scripts/docker/DOCKER_INSTALL_GUIDE.md)
- [TROUBLESHOOTING.md](D:/dev/source_code/vscode_study/localstack-lab/TROUBLESHOOTING.md)
- [如何查看LocalStack日志.md](D:/dev/source_code/vscode_study/localstack-lab/%E5%A6%82%E4%BD%95%E6%9F%A5%E7%9C%8BLocalStack%E6%97%A5%E5%BF%97.md)
- [UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](D:/dev/source_code/vscode_study/softbs/UM890Pro_Win11_WSL2_Docker_Java_Python_%E6%9C%AC%E5%9C%B0%E6%A8%A1%E5%9E%8B%E8%BE%85%E5%8A%A9%E5%BC%80%E5%8F%91%E6%95%99%E7%A8%8B.md)

### CI/CD

- [jtproject-ci.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-ci.yml)
- [jtproject-deploy.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-deploy.yml)
- [jtproject-deploy-safe.yml](D:/dev/source_code/vscode_study/.github/workflows/jtproject-deploy-safe.yml)
- [deploy-softbs-pages.yml](D:/dev/source_code/vscode_study/.github/workflows/deploy-softbs-pages.yml)
- [GitHub学生版学习与DevOps实践教程.md](D:/dev/source_code/vscode_study/softbs/github/GitHub%E5%AD%A6%E7%94%9F%E7%89%88%E5%AD%A6%E4%B9%A0%E4%B8%8EDevOps%E5%AE%9E%E8%B7%B5%E6%95%99%E7%A8%8B.md)

### 自动化运维

- [scripts/README.md](D:/dev/source_code/vscode_study/java-projects/JtProject/scripts/README.md)
- [monitor-status.ps1](D:/dev/source_code/vscode_study/scripts/localstack/monitor-status.ps1)
- [diagnostic.ps1](D:/dev/source_code/vscode_study/scripts/localstack/diagnostic.ps1)
- [verify-localstack.ps1](D:/dev/source_code/vscode_study/scripts/localstack/verify-localstack.ps1)
- [如何查看LocalStack日志.md](D:/dev/source_code/vscode_study/localstack-lab/%E5%A6%82%E4%BD%95%E6%9F%A5%E7%9C%8BLocalStack%E6%97%A5%E5%BF%97.md)

### Kubernetes

- [Codespaces学习要点.md](D:/dev/source_code/vscode_study/softbs/github/Codespaces%E5%AD%A6%E4%B9%A0%E8%A6%81%E7%82%B9.md)

## 当前目录结构

```text
devops-lab/
|-- README.md
|-- QUICK_REFERENCE.md
|-- 01-学习路线.md
|-- 02-Docker与容器.md
|-- 03-CI_CD与自动化运维.md
|-- 04-Kubernetes入口.md
|-- 05-Kubernetes最小入门.md
|-- 06-GitHub_Actions最小示例项目页.md
|-- 07-kind_k3d本地练习模板页.md
|-- 08-自己写第一个GitHub_Actions_Workflow.md
|-- 09-Docker_GitHub_Actions_最小部署演练.md
|-- 10-kind_k3d_hello_nginx_本地实操页.md
|-- 11-监控与可观测性入口.md
|-- 12-Prometheus_Grafana最小入门.md
`-- templates/
    |-- docker-actions-demo/
    |-- k8s-hello-nginx/
    `-- prometheus-grafana-demo/
```
