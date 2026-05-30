# chat_cli 处理流程图

下面是 `main.py` 的处理流程图（Mermaid 格式），可在支持 Mermaid 的渲染器中直接预览。

![详细处理流程图（SVG）](/agent-lab/projects/chat_cli/docs/flowchart.svg)

> 说明：此 SVG 为静态流程图，适用于在 GitHub 或不支持 Mermaid 的 Markdown 渲染器中直接查看。

如果平台不直接渲染 SVG，CI 会生成 `flowchart.png` 作为回退：

![详细处理流程图（PNG）](/agent-lab/projects/chat_cli/docs/flowchart.png)

如何在本地渲染此 Mermaid 图：

- 推荐（VS Code）：安装 `Markdown Preview Mermaid Support` 或 使用内置的 Mermaid 渲染扩展，在打开此文件或项目的 README 时即可看到图形。
- 使用 `mmdc` (mermaid-cli) 渲染为图片：

```bash
# 安装（需要 Node.js + npm）
npm install -g @mermaid-js/mermaid-cli

# 从文件渲染为 PNG
mmdc -i docs/flowchart.md -o docs/flowchart.png

# 或直接渲染内嵌的 Mermaid 片段（用临时 mermaid 文件）
```

注意：CI 或 GitHub 的 README 渲染页面在某些地方不直接渲染 Mermaid，建议同时保留一个 PNG/SVG 版本以便在不支持 Mermaid 的平台也能查看。

如果你希望我现在生成并添加 PNG/SVG（需要在 runner 或你本地安装 `mmdc`），我可以继续执行；否则我会把这个文档作为独立说明提交。 
