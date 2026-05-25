# 🚀 快速启动导航 (Quick Start Navigation)

> **30 秒进入开发状态** | 完整项目地图、关键命令速查

---

## 📍 核心路由地图 (Core Route Map)

```
D:\dev\source_code\vscode_study
├── 🔵 QUICK_START_NAVIGATION.md          ← 你在这里
├── README.md                              ← 完整项目总览
│
├── 📁 scripts/ ★ 开发工具库 (Dev Tools)
│   ├── README.md                          ← 13 个工具索引
│   ├── wsl/                               ← WSL 一键启动
│   │   ├── start-wsl-vscode-dev.bat       ← ⭐ 主启动器
│   │   ├── init-wsl-local-repo.sh         ← 本地仓库初始化
│   │   ├── dev-check-gitbash.sh           ← 环境诊断
│   │   └── gitbash_aliases.sh             ← Bash 快捷命令
│   ├── docker/                            ← Docker 安装
│   │   ├── install-docker-quick.ps1       ← 3 分钟装好
│   │   └── DOCKER_INSTALL_GUIDE.md
│   └── localstack/                        ← AWS 本地模拟
│       ├── verify-localstack.ps1          ← 健康检查 ✓
│       ├── monitor-status.ps1             ← 实时监控
│       └── 其他诊断工具
│
├── 📁 java-projects/                      ← Java 生态
│   ├── README.md
│   ├── JtProject/                         ← Spring Boot E-commerce ★
│   ├── JtProject-React/                   ← React 前端
│   ├── JtProject-Vue/                     ← Vue 前端
│   └── JtProject-Thymeleaf/               ← Thymeleaf 前端
│
├── 📁 python-projects/                    ← Python 生态
│   └── ai-lab/                            ← LLM 应用实验室
│       ├── .venv/                         ← 虚拟环境
│       ├── LEARNING_GUIDE.md              ← 学习路线
│       └── projects/
│
├── 📁 sap-lab/                            ← SAP 学习空间
│   ├── LEARNING_GUIDE.md                  ← 7 模块课程
│   └── projects/                          ← 实操项目
│
├── 📁 devops-lab/                         ← DevOps 工程化
│   ├── README.md
│   ├── QUICK_REFERENCE.md                 ← 命令速查
│   └── templates/                         ← Docker/K8s 模板
│
├── 📁 llm-lab/                            ← LLM 应用工程
│   ├── 00-Python学习范围.md
│   ├── 02-模型调用基础.md
│   └── projects/
│
├── 📁 agent-lab/                          ← AI Agent 实验
│   ├── 02-模型调用基础.md
│   ├── 05-Agent工作流.md
│   └── projects/
│
├── 📁 localstack-lab/ & 📁 localstack/    ← AWS 本地测试
│
└── 📁 softbs/                             ← 教程文档库
    ├── vscode/                            ← VS Code 指南
    │   └── Win11_WSL_当前仓库实战教程_vscode_study.md ⭐
    ├── github/                            ← Git & GitHub 指南
    │   └── Windows_Git_Bash_开发实战教程_Java_Python_LLM.md ⭐
    └── tools/                             ← 示例工具
```

---

## ⚡ 3 步快速启动 (3-Step Quick Start)

### **第 1 步：启动 WSL + 仓库 + VS Code**
```powershell
D:\dev\source_code\vscode_study> scripts\wsl\start-wsl-vscode-dev.bat
```
✓ 自动打开 Windows Terminal (Ubuntu 配置文件)  
✓ 自动进入 `/mnt/d/dev/source_code/vscode_study`  
✓ 自动启动 VS Code (Remote-WSL 已连接)

**如果遇到问题：**
```bash
# WSL 中运行诊断
bash scripts/wsl/dev-check-gitbash.sh     # 检查环境
echo $PATH | grep -i git                   # 查看 Git 路径
```

---

### **第 2 步：验证开发环境**
```bash
# WSL 中自动运行（由 dev-check 执行）
devcheck                                    # Git, Java, Python, LLM keys 检查
venvon                                      # 激活 .venv
mkvenv ai-lab                              # 为 ai-lab 创建虚拟环境
```

### **第 3 步：启动开发工作**
选择你的技术栈：

| 栈 | 启动命令 | 文档 |
|---|------|------|
| **Spring Boot** (Java) | `cd java-projects/JtProject && ./mvnw spring-boot:run` | [java-projects/README.md](java-projects/README.md) |
| **Python LLM** | `cd python-projects/ai-lab && python projects/llm_api_demo.py` | [llm-lab/README.md](llm-lab/README.md) |
| **AWS LocalStack** | `scripts/localstack/verify-localstack.ps1` | [localstack-lab/QUICK_REFERENCE.md](localstack-lab/QUICK_REFERENCE.md) |
| **SAP ABAP** | 打开 [sap-lab/LEARNING_GUIDE.md](sap-lab/LEARNING_GUIDE.md) | [sap-lab/README.md](sap-lab/README.md) |
| **DevOps CI/CD** | 查看 [devops-lab/README.md](devops-lab/README.md) | [devops-lab/QUICK_REFERENCE.md](devops-lab/QUICK_REFERENCE.md) |

---

## 📚 项目快速查询表 (Project Quick Lookup)

| 项目 | 类型 | 启动命令 | 文档入口 | 状态 |
|------|------|--------|---------|------|
| **JtProject** | Spring Boot 2.7 + Hibernate + JSP | `cd java-projects/JtProject && ./start.sh` | [项目 README](java-projects/JtProject/README.md) | ✅ Active |
| **ai-lab** | Python ML/LLM 实验 | `cd python-projects/ai-lab && venvon && python 01_python_basics.py` | [学习指南](python-projects/ai-lab/LEARNING_GUIDE.md) | ✅ Active |
| **LocalStack** | AWS S3/DynamoDB 本地模拟 | `scripts/localstack/wait-for-docker-and-run.ps1` | [快速参考](localstack-lab/QUICK_REFERENCE.md) | ✅ Active |
| **sap-lab** | SAP ABAP/CDS/RAP/CAP 课程 | 手动代码审查 + 系统测试 | [7 模块课程](sap-lab/LEARNING_GUIDE.md) | 📚 Learning |
| **DevOps Lab** | Docker/K8s/GitHub Actions | 参考 [QUICK_REFERENCE.md](devops-lab/QUICK_REFERENCE.md) | [README](devops-lab/README.md) | 📚 Learning |
| **LLM Lab** | 大模型应用工程 | `cd llm-lab/projects && python main.py` | [学习范围](llm-lab/00-Python学习范围.md) | 📚 Learning |
| **Agent Lab** | AI Agent 工作流 | 参考项目文档 | [LLM-Agent 学习路径](agent-lab/LLM-Agent学习路径与计划.md) | 📚 Learning |

---

## 🔧 常用命令速查 (Command Cheat Sheet)

### **Windows PowerShell**
```powershell
# WSL + VS Code 一键启动
.\scripts\wsl\start-wsl-vscode-dev.bat

# 初始化 WSL 本地仓库（在 WSL 里执行）
bash ./scripts/wsl/init-wsl-local-repo.sh

# Docker 安装
.\scripts\docker\install-docker-quick.ps1        # 3 分钟快速版
.\scripts\docker\install-docker-desktop.ps1      # 完整版

# LocalStack 健康检查
.\scripts\localstack\verify-localstack.ps1
.\scripts\localstack\monitor-status.ps1           # 实时监控 Docker + LocalStack
```

### **Git Bash / WSL Bash**
```bash
# 快捷别名（已预加载到 ~/.bashrc）
devcheck                                  # 环境诊断报告
gs                                        # git status
gp                                        # git push
gpl                                       # git pull
gcm "message"                             # git commit -m

# 虚拟环境
venvon                                    # 激活 .venv
mkvenv <project>                          # 为项目创建 .venv
```

### **Java / Spring Boot**
```bash
cd java-projects/JtProject
./mvnw clean install                      # 构建 + 测试
./mvnw spring-boot:run                    # 启动应用（8080 端口）
# 或
./start.sh
```

### **Python / LLM**
```bash
cd python-projects/ai-lab
python -m venv .venv                      # 创建虚括环境（首次）
source .venv/bin/activate                 # 激活
pip install -r requirements.txt           # 安装依赖
python projects/llm_api_demo.py           # 运行 LLM 演示
```

---

## 📖 关键文档导航 (Key Documentation)

### **环境与基础设置**
- 🔴 **必读** [Win11 WSL 实战教程](softbs/vscode/Win11_WSL_当前仓库实战教程_vscode_study.md) — 30 秒启动流、目录映射、GitHub 同步
- 🔴 **必读** [Windows Git Bash 实战教程](softbs/github/Windows_Git_Bash_开发实战教程_Java_Python_LLM.md) — 环境诊断、别名、自动化

### **项目特定文档**
- [JtProject 项目说明](java-projects/JtProject/README.md) — Hibernate 手动配置、3 层 JSP、数据库连接
- [ai-lab 学习指南](python-projects/ai-lab/LEARNING_GUIDE.md) — 完整 Python ML/LLM 学习路线
- [sap-lab 课程](sap-lab/LEARNING_GUIDE.md) — 7 模块 SAP ABAP/CDS/RAP/CAP 渐进式课程
- [DevOps 快速参考](devops-lab/QUICK_REFERENCE.md) — Docker/K8s/GitHub Actions 命令集

### **脚本和工具文档**
- [scripts/README.md](scripts/README.md) — 13 个工具完整索引和用法
- [LocalStack 快速参考](localstack-lab/QUICK_REFERENCE.md) — AWS 本地服务命令
- [Docker 安装指南](scripts/docker/DOCKER_INSTALL_GUIDE.md)

---

## ❓ 常见问题排查 (Troubleshooting)

| 问题 | 解决方案 |
|------|--------|
| 启动器打不开 WSL | 运行 `wsl --list --verbose` 检查 Ubuntu 是否安装；运行 `bash scripts/wsl/dev-check-gitbash.sh` 诊断 |
| Git 命令找不到 | 检查 Git Bash 别名已加载：`alias \| grep gs` |
| Python venv 无法激活 | WSL 中运行 `source .venv/bin/activate`；Windows 中运行 `.venv\Scripts\activate.bat` |
| LocalStack 连接失败 | 运行 `scripts/localstack/verify-localstack.ps1` 或查看 [LocalStack 故障排查](localstack-lab/TROUBLESHOOTING.md) |
| Java Maven 报错 | 运行 `./mvnw --version` 检查 Maven Wrapper；确保 JAVA_HOME 已设置 |

---

## 🎯 学习路径建议 (Recommended Learning Path)

### **第 1 周：基础环境**
1. 阅读 [Win11 WSL 实战教程](softbs/vscode/Win11_WSL_当前仓库实战教程_vscode_study.md) §2-3 (WSL 映射与启动)
2. 跑通 `scripts\wsl\start-wsl-vscode-dev.bat` 一次启动完整开发环境
3. 运行 `devcheck` 验证 Git/Java/Python/LLM keys

### **第 2 周：选择技术栈**
- **Java 方向**: [java-lab/04-Java基础教程.md](java-lab/04-Java基础教程.md) → [JtProject README](java-projects/JtProject/README.md)
- **Python LLM 方向**: [llm-lab/02-模型调用基础.md](llm-lab/02-模型调用基础.md) → [ai-lab LEARNING_GUIDE](python-projects/ai-lab/LEARNING_GUIDE.md)
- **SAP 方向**: [sap-lab/LEARNING_GUIDE.md](sap-lab/LEARNING_GUIDE.md) (7 模块渐进式)
- **DevOps 方向**: [devops-lab/02-Docker与容器.md](devops-lab/02-Docker与容器.md) → [QUICK_REFERENCE](devops-lab/QUICK_REFERENCE.md)

### **第 3 周+：深度学习**
- 按相应项目的 LEARNING_GUIDE.md 逐模块推进
- 在 projects/ 中动手实现每个技能模块

---

## 🌟 一句话速记 (TL;DR)

```
启动：scripts\wsl\start-wsl-vscode-dev.bat
诊断：devcheck
文档：先看本文件 → 再看 softbs/{vscode,github} → 再看具体项目
选栈：Java/Python/SAP/DevOps — 都有完整 LEARNING_GUIDE
```

---

**最后更新**: 2025 年社区维护版  
**推荐查阅顺序**:  
1️⃣ 本文 (QUICK_START_NAVIGATION.md)  
2️⃣ [scripts/README.md](scripts/README.md)  
3️⃣ [项目 README](README.md)  
4️⃣ [WSL 实战教程](softbs/vscode/Win11_WSL_当前仓库实战教程_vscode_study.md)
