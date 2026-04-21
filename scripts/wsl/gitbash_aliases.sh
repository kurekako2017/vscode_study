#!/usr/bin/env bash

# Windows 日常开发使用的 Git Bash 别名集合。
# 用法: source /d/dev/source_code/vscode_study/scripts/wsl/gitbash_aliases.sh

# ---- Navigation ----
alias croot='cd /d/dev/source_code/vscode_study'
alias csoft='cd /d/dev/source_code/vscode_study/softbs'

# ---- Git shortcuts ----
alias gs='git status -sb'
alias ga='git add'
alias gaa='git add .'
alias gc='git commit'
alias gcm='git commit -m'
alias gp='git push'
alias gpl='git pull --rebase'
alias gl='git log --oneline --graph --decorate -20'
alias gd='git diff'
alias gco='git checkout'
alias gcb='git checkout -b'

# ---- Python / venv ----
venvon() {
  if [ -f ".venv/Scripts/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/Scripts/activate
  elif [ -f "venv/Scripts/activate" ]; then
    # shellcheck disable=SC1091
    source venv/Scripts/activate
  else
    echo "No virtualenv found. Expected .venv/Scripts/activate or venv/Scripts/activate"
    return 1
  fi
}

venvoff() {
  deactivate 2>/dev/null || true
}

# ---- Dev helpers ----
alias py='python'
alias pi='python -m pip'
alias ll='ls -lah'
alias rr='rg --files'
alias rrg='rg'
alias cls='clear'

devcheck() {
  bash /d/dev/source_code/vscode_study/scripts/wsl/dev-check-gitbash.sh
}

mkvenv() {
  python -m venv .venv && source .venv/Scripts/activate && python -m pip install --upgrade pip
}