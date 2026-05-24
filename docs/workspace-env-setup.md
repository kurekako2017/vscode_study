# 全局环境安装说明

这个文档只覆盖这个工作区里非 Java 代码常用的全局环境。

## 当前已确认的基础环境

- Python 3.12.3
- Node.js 22.22.1
- npm 10.9.4

## 当前缺口

- Docker CLI 在当前 WSL 里不可用，仍需要 Docker Desktop 的 WSL integration

## 推荐安装目标

如果你想一次性把非 Java 代码常用的环境补齐，建议至少准备下面这些能力：

- Docker Desktop 并开启 WSL integration
- localstack CLI

## 本次已补齐

- kubectl
- terraform
- aws CLI
- localstack CLI

## Docker Desktop

这个工作区里很多项目都依赖 Docker，但当前 WSL 里没有可用的 Docker CLI。

你需要在宿主机上安装 Docker Desktop，然后在 Docker Desktop 里打开 WSL integration，让当前 Ubuntu/WSL 可以直接访问 Docker。

更短的排障清单见：[docs/docker-wsl-quickstart.md](docs/docker-wsl-quickstart.md)

验证方式：

```bash
docker --version
docker compose version
```

## 用户级安装方式

当前环境没有无密码 sudo，所以更适合把工具装到用户目录。

建议先确保下面目录在 PATH 里：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

如果你希望长期生效，把这一行加到 `~/.bashrc`。

### kubectl

```bash
mkdir -p ~/.local/bin
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl ~/.local/bin/
```

### terraform

```bash
mkdir -p ~/.local/bin
curl -LO https://releases.hashicorp.com/terraform/1.12.0/terraform_1.12.0_linux_amd64.zip
unzip terraform_1.12.0_linux_amd64.zip
mv terraform ~/.local/bin/
```

### aws CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install -i ~/.local/aws-cli -b ~/.local/bin
```

### localstack CLI

```bash
python3 -m pip install --user localstack
```

## 验证命令

```bash
python3 --version
node --version
npm --version
docker --version
kubectl version --client --short
terraform version
aws --version
localstack --version
```

## 备注

- kubectl 和 terraform 的版本号可以按你自己的需要替换成更新版本。
- aws CLI 和 localstack CLI 都可以改成 pipx 或其他用户级安装方式。
- 只要 Docker 没有在 WSL 里可用，devops-lab 和 localstack-lab 的很多示例都无法完整跑通。