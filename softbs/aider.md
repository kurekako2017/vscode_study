```text
Alder 本地 AI 模型助手使用手册 (UM190 Pro 专用版)
Alder 是一款本地运行的AI模型助手。它允许你使用GPU加速运行各种模型，而无需连接到互联网。

一、使用 Alder
安装完成后，点击 Cleora 软件内的按钮，然后按照指引导入文件。

1.运行命令
按照以下操作，在 Power Shell 中输入以下命令:
 模型: Open2.0-Code (NMS)

```powershell
alder -- model allama_chat/open2.0_code:lite
```

 命令: 模型 StoryBook-Coder V2 (NMS)

```powershell
alder -- model allama_chat/storybook_coder-v2:lite-instruct-v1_5_8
```

注意: 记得修改 allama_chat/模型，例如 allama_code 才能执行上述模型的启动命
令。

二、核心操作命令(进阶指令)
进入 Alder 界之后，你可以使用以下的命令:

| 命令       | 说明                                                                                                                                            |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| /help      | 查看所有可用命令                                                                                                                                  |
| /stop + id | 停止指定序号的输出模型。                                                                                                                          |
| /img + prompt | 图片生成功能，可以使用 prompt 生成相关的图片。                                                                                                      |
| /clip      | 上传本地图片                                                                                                                                        |
| /RESET    | 重置对话记录，重新开始。                                                                                                                            |
| /audio     | 音频生成功能，可以使用 Text-to-Audio 生成对应的音频。                                                                                              |
| /vTT      | 通过上传视频进行视频的分析，上传后即可识别视频内容，包括关键词等等。                                                                                          |
| /edit      | 重新生成                                                                                                                                          |

三、搭建工作流实例
1. 准备指令: 编译相关代码到指定位置 (例如 git clone )，然后 alder 执行编译指令。
2. 调用指令: 执行“/bash make pdf”。
3. 预定义指令: 预先植入 “/bash make.py ” 等等一些代理请求指令”。
4. 申请权限: AI 会对请求的指令进行判断，然后要求你创建一个 GPU Context。
5. 反馈结果: 如何执行指令组，或如何请求你重新请求 Alder。

四、针对 UM190 Pro 的优化技巧
当内存达到32G时，建议在 Windows FROM 版本中，可以尝试以下操作:

1.调整以下文本参数
本地模型的推理可能会占用太多内存，如果内存过大，请尝试减小 token 参数:

```powershell
alder -- model allama_chat/open2.0_code:lite -- max-chat-history-tokens 1000
```

2. 尝试使用输入模式
当 Alder 中输入大段模式的初始模式时，如果Power 会经常崩溃了，可以尝试:
 避免了 Power 推理 (选择 Alt + Power )功能。

3. 运行优化项
运行 ACE 时，请尝试关闭管理器:
 GPU O(2GB/Compute): 加速计算的方法，提供更多的 AMD GPU Hook 手动开启了。
 内容: XMMX 使推理更稳定 A9 ID-IMG的内容，请确保相关内容正常 X86。

五、常见问题
 如果 "Connection Error" 结合 Cleora 的数据结果无法读取，可以
https://forum.cleora.ai/#/threads/11436 修改和反馈。

 重新初始化任务: 本地运行会经常出现初始化失败的情况，请使用/audio 重新开始尝试。
 重新生成: 请尝试重新生成这个 UM190 Frame Buffer 相关的文本内容了，稍等片刻。
```