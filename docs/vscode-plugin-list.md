# VS Code 插件清单

这个清单只列这个工作区里非 Java 代码真正有用的核心插件，以及它们的作用。

## 已安装的核心插件

| 插件 | 状态 | 作用 |
|---|---|---|
| Python | 已安装 | Python 语言支持、运行、调试、虚拟环境识别 |
| Pylance | 已安装 | Python 智能补全、类型分析、跳转 |
| Jupyter | 已安装 | Notebook、交互式单元格、Python 笔记本支持 |
| Jupyter Keymap | 已安装 | Notebook 快捷键支持 |
| Jupyter Notebook Renderers | 已安装 | 图表、图片、富输出渲染 |
| Docker | 已安装 | Dockerfile、Compose、容器操作支持 |
| YAML | 已安装 | YAML 语法、高亮、校验，覆盖 Kubernetes 和 GitHub Actions |
| HashiCorp Terraform | 已安装 | Terraform 语法、高亮、补全 |
| ESLint | 已安装 | JavaScript 和 TypeScript 代码检查 |
| Prettier | 已安装 | 代码格式化 |
| Vue (Official) | 已安装 | Vue 文件、模板、脚本支持 |
| Angular Language Service | 已安装 | Angular 模板和 TypeScript 支持 |
| EditorConfig | 已安装 | 统一代码风格配置 |
| Code Spell Checker | 已安装 | 拼写检查 |
| Todo Tree | 已安装 | 汇总 TODO / FIXME 注释 |
| GitHub Actions | 已安装 | GitHub Actions workflow 支持 |
| Dev Containers | 已安装 | 容器化开发环境支持 |
| ABAP Syntax Highlighting | 已安装 | ABAP 语法高亮 |
| ABAP CDS Language Support | 已安装 | ABAP CDS 高亮和片段 |

## 当前不需要单独安装的补充项

- GitHub Pull Request and Issues：适合看 PR 和评论，不是运行代码必需项
- 中文语言包：方便界面使用，不影响运行

## 结论

如果你的目标只是把这个工作区的非 Java 代码跑起来，核心是这几组：

1. Python + Pylance + Jupyter
2. Docker + YAML + Terraform
3. ESLint + Prettier + Vue / Angular
4. ABAP / CDS 仅在 SAP 学习线里需要