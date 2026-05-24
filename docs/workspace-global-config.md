# 工作区全局环境配置说明

这个文档记录了在本工作区（非 Java 部分）已安装的全局工具、当前状态、复现步骤和注意事项，适合学习和复现环境配置。

## 一览（已验证）

- Python: `Python 3.12.3`
- pip: `pip 26.1.1` (位于 `~/.local/lib/python3.12/site-packages`)
- Node: `v22.22.1`
- npm: `10.9.4`
- LocalStack CLI: `LocalStack CLI 2026.5.0` (安装到 `~/.local/bin/localstack`)
- kubectl: 安装到 `~/.local/bin/kubectl`（用户级）
- Terraform: `Terraform v1.12.0`（安装到 `~/.local/bin/terraform`）
- AWS CLI: `aws-cli/2.34.53`（安装到 `~/.local/bin`，通过 AWS 安装脚本）
- Docker CLI: 在当前 WSL 中**不可用**（需要在宿主 Windows 上启用 Docker Desktop 的 WSL integration）

验证命令（示例）：

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 --version
python3 -m pip --version
node --version
npm --version
localstack --version
kubectl version --client --short || true
terraform version || true
aws --version || true
docker --version || echo "docker: not found"
echo "PATH=$PATH"
```

（上述命令在本环境的返回值已记录在仓库历史中）

## 安装位置与 PATH

- 我们采用“用户级安装”把工具放在 `~/.local/bin`，并把它加入 `PATH`。
- 建议把下面一行加入 `~/.bashrc`：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 复现（最小步骤）

1. 确认 `~/.local/bin` 在 PATH：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

2. 必要的用户级工具（示例命令）：

```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && mv kubectl ~/.local/bin/

# terraform（示例版本）
curl -LO https://releases.hashicorp.com/terraform/1.12.0/terraform_1.12.0_linux_amd64.zip
unzip terraform_1.12.0_linux_amd64.zip && mv terraform ~/.local/bin/

# aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && ./aws/install -i ~/.local/aws-cli -b ~/.local/bin

# localstack
python3 -m pip install --user localstack
```

3. Python 项目（以 `python-projects/ai-lab` 为例）：

```bash
cd python-projects/ai-lab
# 如果没有系统级 python3-venv，请先在宿主机或使用 sudo 安装：
# sudo apt install python3-venv
./setup.sh
source .venv/bin/activate
python3 01_python_basics.py
```

## 注意事项与故障排查

- Docker 在 WSL 中不可用时，`devops-lab` 与 `localstack-lab` 的示例无法完整运行。请参见 `docs/docker-wsl-quickstart.md` 获取快速排障步骤（Windows 上安装 Docker Desktop 并启用 WSL integration）。
- 有些系统（受 PEP 668 管理）会阻止直接使用 `pip install --user`，如果遇到错误，推荐使用 `python3 -m pip install --user --break-system-packages`，但更好做法是安装 `python3-venv` 并在虚拟环境中操作。
- 推荐长期做法：把所有 Python 项目放入各自的 `venv`，并避免在系统 Python 上直接安装大量包。
- 如果 `aws`、`kubectl`、`terraform` 等命令不可用，确认 `~/.local/bin` 在 `PATH`，并检查文件可执行权限（`chmod +x ~/.local/bin/<binary>`）。

## 已安装的 VS Code 扩展（摘要）

- 已安装扩展包括：Python、Pylance、Jupyter、Jupyter Renderers、Jupyter Keymap、Docker、YAML、HashiCorp Terraform、ESLint、Volar（Vue）、Angular Language Service、EditorConfig、Code Spell Checker、Todo Tree、GitHub Actions、Remote Containers、Prettier、Chinese language pack、GitHub PR chat 等。

（如需完整可复制的扩展 ID 清单，我可以导出一份 `extensions-list.txt`）

## 推荐下一步

- 如果你要学习并完整运行 `localstack-lab` / `devops-lab`，先在 Windows 主机上启用 Docker Desktop WSL integration。参见 `docs/docker-wsl-quickstart.md`。
- 如需我把当前环境以脚本化形式导出（包括安装命令与版本固定），我可以生成一个 `setup_env.sh` 或 `setup_env.ps1`。

---

文档由自动化脚本与人工验证生成，必要时我可以把命令整理成可执行脚本供你一键运行。 
