# 🚀 Aider 本地 AI 编程助手实战指南

> **适用设备**: Minisforum UM890 Pro (Win11 / 32G RAM / 780M)  
> **推荐模型**: Qwen2.5-Coder 14B (已验证可在您的设备上流畅运行)

---

## 一、 启动前的准备
在使用 Aider 之前，请确保满足以下两个条件：
1. **Ollama 服务已在后台运行**（任务栏右下角可以看到小羊图标）。
2. **您的代码项目已由 Git 管理**。
   - 如果是新文件夹，请先在文件夹内右键打开终端输入：
     ```powershell
     git init
     ```

---

## 二、 启动 Aider
请在您的**项目文件夹**下打开 PowerShell，执行以下命令：

### 🌟 推荐启动方式 (使用 Qwen)
这是您目前最稳定、速度最快的选择。
```powershell
aider --model ollama_chat/qwen2.5-coder:14b

备用启动方式 (如果内存允许)
如果您关闭了其他大型软件，想尝试逻辑更强的 DeepSeek，可使用：
aider --model ollama_chat/deepseek-coder-v2:16b-lite-instruct-q4_K_M
小贴士： 启动命令太长记不住？可以将上面的命令保存为 Start-Aider.bat 文件放在项目根目录，双击即可运行。

三、 Aider 交互与快捷键
进入 Aider 界面后（看到 > 提示符），您的操作逻辑如下：

1. 基础对话
直接输入需求：例如 "帮我写一个 Python 贪吃蛇游戏" 或 "解释这段代码"。

换行输入：如果您要输入多行内容，请按 Alt + Enter（或者是 Esc 然后 Enter），直接按 Enter 会发送消息。

2. 文件操作命令 (Slash Commands)
Aider 使用 / 开头的命令来管理文件：

命令,作用,示例
/add,添加文件给 AI 看 (最常用),/add main.py utils.py
/drop,让 AI 停止关注某文件 (省内存),/drop utils.py
/undo,撤销 AI 上一步的代码修改,/undo
/diff,查看 AI 刚才改了哪里,/diff
/run,在终端运行系统命令,/run python main.py
/exit,退出 Aider,/exit
