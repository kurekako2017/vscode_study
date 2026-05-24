#!/usr/bin/env bash
set -euo pipefail

# setup_env.sh - 用户级安装工作区常用工具（非破坏、非交互）
# 说明：本脚本把工具安装到 `~/.local/bin`，并尝试为 `python-projects/ai-lab` 创建 virtualenv 并安装依赖。

export PATH="$HOME/.local/bin:$PATH"

echo "[setup_env] 确认基本命令"
command -v curl >/dev/null 2>&1 || { echo "请先安装 curl 并重试" >&2; exit 1; }
command -v unzip >/dev/null 2>&1 || { echo "请先安装 unzip 并重试" >&2; exit 1; }

mkdir -p "$HOME/.local/bin"

install_kubectl(){
  echo "[setup_env] 安装 kubectl 到 ~/.local/bin"
  tmp="/tmp/kubectl.$$"
  curl -fsSL -o "$tmp" "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x "$tmp"
  mv "$tmp" "$HOME/.local/bin/kubectl"
}

install_terraform(){
  echo "[setup_env] 安装 terraform 到 ~/.local/bin (示例版本 1.12.0)"
  tmpzip="/tmp/terraform.zip.$$"
  curl -fsSL -o "$tmpzip" "https://releases.hashicorp.com/terraform/1.12.0/terraform_1.12.0_linux_amd64.zip"
  unzip -o "$tmpzip" -d /tmp
  mv /tmp/terraform "$HOME/.local/bin/terraform"
  rm -f "$tmpzip"
}

install_awscli(){
  echo "[setup_env] 安装 aws CLI 到 ~/.local/bin"
  tmpzip="/tmp/awscliv2.zip.$$"
  curl -fsSL -o "$tmpzip" "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
  unzip -o "$tmpzip" -d /tmp/awscli_install
  /tmp/awscli_install/aws/install -i "$HOME/.local/aws-cli" -b "$HOME/.local/bin" || true
  rm -rf /tmp/awscli_install "$tmpzip"
}

install_localstack(){
  echo "[setup_env] 使用 pip 用户级安装 LocalStack"
  python3 -m pip install --user --break-system-packages localstack
}

# 执行安装（按需注释掉不需要的部分）
install_kubectl || echo "kubectl install skipped"
install_terraform || echo "terraform install skipped"
install_awscli || echo "awscli install skipped"
install_localstack || echo "localstack install skipped"

echo "[setup_env] 尝试为 python-projects/ai-lab 创建并安装依赖"
if [ -d "python-projects/ai-lab" ]; then
  pushd python-projects/ai-lab >/dev/null
  if ! command -v python3 >/dev/null 2>&1; then
    echo "找不到 python3，请先安装 Python 3" >&2
    popd >/dev/null
    exit 1
  fi

  if [ ! -f "requirements.txt" ]; then
    echo "没有找到 requirements.txt，跳过 Python 依赖安装"
  else
    if [ ! -d ".venv" ]; then
      if python3 -c "import venv" 2>/dev/null; then
        python3 -m venv .venv
      else
        echo "系统缺少 python3 venv 模块，请在宿主机安装 python3-venv 或手动创建 venv" >&2
      fi
    fi
    # 使用 venv 的 pip 安装依赖
    if [ -f ".venv/bin/activate" ]; then
      . .venv/bin/activate
      pip install --upgrade pip
      pip install -r requirements.txt || echo "pip install 部分失败，检查错误信息"
      deactivate
    fi
  fi
  popd >/dev/null
fi

echo "[setup_env] 完成。请确认 ~/.local/bin 在 PATH 中，或在 ~/.bashrc 添加：\n  export PATH=\"$HOME/.local/bin:$PATH\""
