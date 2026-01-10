UM890 Pro 上安装本地 Aider + DeepSeek-Coder V2
Lite (16B) 和 Qwen2.5-Coder 14B (Q4/Q5)的详细指南
文档版本:2026-01-10
适用硬件:Minisforum UM890 Pro (AMD Ryzen 9 8945HS + Radeon 780M iGPU, 32GB RAM, Win11
Pro)
目标:使用 Ollama 运行本地量化模型(GGUFQ4_K_M或Q5_K_M),结合 Aider 实现 AI 编码助手。32GB
RAM 足够运行这些-9-11GB模型,主要依赖CPU (iGPU支持需额外配置,可能fallback 到CPU,推理速
度5-20 tokens/s)。
下载此MD文件:
复制以下内容到记事本,保存为 Aider_UM890Pro_安装指南.md,用VSCode/Obsidian 预览
(Ctrl+Shift+V)。或用浏览器打印成PDF。针对你的ABAP/SAP开发,可在 VSCode 中用 Aider 编辑
S/4HANA 项目代码,结合 GitHub Copilot 补充上下文。
关键注意事项
硬件
Radeon 780M (gfx1103) iGPU 共享 RAM (BIOS 默认512MB-2GB,建议设4-8GB)。Ollama Windows AMD
支持预览版,常 fallback CPU, 32GB RAM足用,但加载模型时关闭其他程序。
安装位程序(Python/Git/Ollama/Aider): C盘(系统 SSD快)。模型:D盘(大容量,避免C盘调)。总~20GB。
置
量化选 Q4_K_M (-9GB):速度快、RAM低;Q5_K_M (~11GB):质量高。优先Q4测试。
GPU
设置
性能
默认 CPU跑;AMD ROCm 支持需 hack (替换 room 文件夹,支持 gfx1103)。若失败,用CPU(你的Ryzen 9
强)。BIOS设UMA 8GB.
CPU: 10-15 t/s; GPU 成功:20+t/s。测试前更新 AMD 驱动。
前提 联网下载;管理员权限;备份数据。Aider 需 Git (你的 abapGit 经验适用)。
问题排 GPU 不识别:用 OLLAMA_DEBUG-1 查日志。慢:Q4或CPU。模型下载:Hugging Face bartowski 仓库稳
查 定。
为什么本地 Aider?比GitHub Copilot 免费、无限上下文(全项目源代码,如S4H_400_u1219_zh),适合
ABAP/IDoc/RFC开发。结合 VSCode(你的偏好),Copilot 读全文。
步骤1: 更新系统& AMD 驱动
1. Win+1→更新与安全→ Windows Update → 检查更新,重启。
2.下载最新 AMD 驱动:amd.com/support→处理器图形→ Ryzen 98945HS→下载 Adrenalin Edition
(含HIP SDK 支持 Ollama ROCm)。安装后重启。
3.任务管理器确认 Radeon 780M显示。
步骤 2: BIOS 配置 iGPU 内存(推荐,提升GPU潜力)
1.重后,按Del进BIOS (Minisforum UM890 Pro用 Del/F2,参考手册)。
2. Advanced → AMD CBS → NBIO Common Options → GFX Configuration → UMA Frame Buffer Size 设
8G(或4G,留 RAM给系统;Auto 默认低)。
3. F10保存退出,重启。
注意:若无此选项,用Auto + AMD 软件调整(Gaming → Graphics → Advanced)。Clear CMOS 按
钮重置(机箱前)。
步骤3: 安装 Python & Git
1. python.org/downloads 下载 Python 3.12.x (64-bit),安装时勾 Add to PATH,默认 C:\Users\你的用
户名\AppData\Local\Programs\Python.
2. CMD (Win+R+cmd)验证: python--version.
3. git-scm.com/download/win 下载 Git,安装默认 C:\Program Files\Git,
4. 验证: git --version (你的abapGit 项目直接用)。
步骤4: 安装 Ollama (含 AMD GPU 支持)
1. ollama.com/download 下载 OllamaSetup.exe,安装默认位置(C:\Users\你的用户名
\AppData\Local\Programs\Ollama).
2. AMD GPU Hack (gfx1103 780M):
下载 likelovewant/ollama-for-amd→ ollama-windows-amd64.7z (支持 gfx1103)。
删除 C:\Users\你的用户名\AppData\Local\Programs\0llama\lib\ollama\rocm 文件夹。
解压替换 room 文件夹(含rocbias.dll等)。
3. 系统托盘见 Ollama 图标。CMD: ollama --version
步骤5: 设置 Ollama 模型路径(D盘)
1. Win+1→系统→关于高级系统设置→环境变量。
2.系统变量→新建: OLLAMA_MODELS D:\01lama\Models (先建文件夹)。
3.用户变量→新建:OLLAMA_DEBUG = 1 (日志查GPU)。
4.重后 CMD。模型默认 C:\Users\...\.ollama\models,现改D盘。
步骤6:下载&导入模型(GGUF 自定义 Modelfile)
创建 D:\Ollama\Models 文件夹。
6.1 DeepSeek-Coder V2 Lite 16B
1. huggingface.co/bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF 下载:
Q4: DeepSeek-Coder-V2-Lite-Instruct-04_K_M.gguf (~9GB)
Q5: DeepSeek-Coder-V2-Lite-Instruct-05_K_M.gguf (~11GB)
2. 同文件夹建 Modelfile-deepseek.txt:
text
FROM./DeepSeek-Coder-V2-Lite-Instruct-04_K_M.gguf
TEMPLATE *** if .System }}</in_start]>systen
{{ .System }}<|im_end >
{{ end }}{{ if.Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end >
{{ end }}<im_start]>assistant
PARAMETER stop "<lim_end >"
PARAMETER stop "<lin_start/>"
3. CMD: cd /d D:\0llama Models ollama create deepseek-coder-v2-lite -f Modelfile-
deepseek.txt
6.2 Qwen2.5-Coder 14B
huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF下載:
Q4: Qwen2.5-Coder-148-Instruct-Q4_K_M.gguf (~9GB)
Q5: Qwen2.5-Codex-148-Instruct-05_K_M.gguf (~11GB)
2. Modelfile-quen.txt:
text
FROM./Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf
TEMPLATE ***<im_start]>system
{{.System }}<lin_end >
</im_start]>user
{{ .Prompt }}<lim_end >
</im_start]>assistant
3. ollama create quen-codex-14b-f Modelfile-qwen.txt
4. ollama list 验证。
提示:用 huggingface-cli 下载更快(pip install huggingface-hub): huggingface-cli download
bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF DeepSeek-Coder-V2-Lite-Instruct-04_K_M.gguf.
步骤 7: 安装 Aider
1. CMD: pip install aider-chat (最新版支持 Ollama)。
2. 验证: aider --version.
步骤8: 测试 & 使用
1. CMD: ollama serve (后台跑)。
2. 测试模型:ollama run deepseek-coder-v2-lite “写ABAP BDC示例”,查任务管理器 GPU/CPU,
日志:托盘 Ollama → View logs,搜“gfx1103"确认GPU。
3. Aider:新文件夹 git init (你的SAP项目)。
aider --model ollama/deepseek-coder-v2-lite
或--model ollama/qwen-coder-14b。添加文件/a your_abap_file.abap,Al编辑。
VSCode 集成: Aider VSCode扩展,或终端跑。
4. 示例:针对S/4HANA Unicode 转换,提示“优化此Shift JIS 到 Unicode 的 IDoc ALE 代码”。
故障排除
GPU不工作确认rocm 替换、HSA_OVERRIDE_GFX_VERSION=gfx1163 环境变量;否则CPU跑(你的硬件强)。
模型慢/崩溃 Q4,关程序;RAM <20GB 剩设 OLLAMA_NUM_GPU-0.
Alder 无模型 ollana ps 确认服务跑。
下载失败 VPN 或 Defender 排除 Ollama。
高级: VSCode + Aider + Copilot:本地模型读全项目源(如abapGit repo), Copilot 补云端。适合你的
Eclipse/VSCode + S/4HANA 开发。
参考:Ollama Docs [docs.ollama.com/windows], Aider [aider.chat/docs/ollama.html],你的过去对话
(VSCode ABAP 插件、Copilot 比较)。
完- 复制保存即下载。如需精简版或 ABAP 示例,回复!
4 35 web pages
< 1/2 > 0912.68
