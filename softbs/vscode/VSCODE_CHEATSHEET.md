# VS Code 快捷键与操作速查（单页 Cheatsheet）

说明：本 cheatsheet 面向多语言开发（Python / TypeScript / React / Java 等），包含常用操作、导航、编辑与调试流程的快捷键与小技巧。

---

## 常用（跨平台常用）
- 打开文件：`Ctrl + P`
- 命令面板：`Ctrl + Shift + P`
- 打开终端：`Ctrl + ` ``
- 保存：`Ctrl + S`
- 查找：`Ctrl + F`（当前文件） / `Ctrl + Shift + F`（全局）
- 切换侧栏：`Ctrl + B`
- 切换标签：`Ctrl + Tab`
- 运行当前文件（不调试）：`Ctrl + F5`
- 开始调试：`F5`

## 编辑与代码操作
- 撤销 / 重做：`Ctrl + Z` / `Ctrl + Y`
- 注释/取消注释：`Ctrl + /`
- 复制行 / 删除行：`Shift + Alt + Down` / `Ctrl + Shift + K`
- 多光标：`Alt + Click` 或 `Ctrl + Alt + Up/Down`
- 重命名符号：`F2`（安全重命名，更新所有引用）
- 快速修复：`Ctrl + .`（自动导入、修复建议）

## 导航（快速跳转）
- 转到行：`Ctrl + G`
- 跳到定义：`F12`
- Peek 定义（内联查看）：`Alt + F12`
- 查找引用：`Shift + F12`
- 文件内符号列表：`Ctrl + Shift + O`
- 全局符号 / 跳转到符号：`Ctrl + T` 或 `Ctrl + P` 然后 `@`
- 回到上次位置 / 前进：`Alt + ←` / `Alt + →`（或 `Ctrl + -` / `Ctrl + Shift + -`）
- 面包屑导航：在编辑器顶部点击面包屑或 View → Toggle Breadcrumbs

## 搜索与替换
- 当前文件查找：`Ctrl + F`，替换 `Ctrl + H`
- 在文件中查找下一项/上一个：`F3` / `Shift + F3`
- 选择所有匹配：`Alt + Enter`

## Git 与源码管理
- 打开 Git 视图：`Ctrl + Shift + G`
- 提交（面板中）：`Ctrl + Enter`
- 查看文件历史/比较：右键文件 → `Open File History` 或使用扩展

## 调试（快速流程）
- 启动调试：`F5`
- 继续/恢复：`F5`
- 单步（Step Over）：`F10`
- 进入（Step Into）：`F11`
- 退出当前函数（Step Out）：`Shift + F11`
- 切换断点：点击行号或 `F9`
- 查看调用栈与监视面板：Run and Debug 视图

## 语言/场景特定提示

### Python
- 选择解释器：`Ctrl + Shift + P` → `Python: Select Interpreter`（优先选择 `.venv`）
- 在终端运行选中文本：`Shift + Enter`（需要 Python 扩展）
- 格式化：`Shift + Alt + F`（或保存时自动格式化）
- 推荐扩展：`Python`、`Pylance`、`Black`、`isort`、`pytest`

### TypeScript / React
- 转到类型定义：`Ctrl + F12`
- 快速修复导入：`Ctrl + .`（自动添加未导入符号）
- 重命名组件/prop：`F2`（会重写所有引用）
- 推荐扩展：`ESLint`、`Prettier`、`TS Server`、`React` snippets

### Java
- 跳转到实现：`Ctrl + F12`
- 运行/调试 JUnit：右键测试 → Run/Debug 或使用 Testing 侧栏
- 推荐扩展：`Language Support for Java(TM)`、`Debugger for Java`

## 工作区与任务（自动化常用步骤）
- 在 `.vscode/tasks.json` 中定义任务（例如：创建 venv、安装依赖、运行服务），在命令面板运行 `Tasks: Run Task`。
- 推荐任务：`create-venv`、`install-deps`、`run-mock-server`、`run-smoke-test`

## 小技巧与习惯
- 在大型项目中：先用 `Ctrl + Shift + F` 全局搜索定位，然后用 `Shift + F12` 查看引用。
- 使用 `Alt + Click` 多光标快速批量修改相似行。
- 配置 `editor.formatOnSave` 与 `saveActions` 来保持代码风格一致。

---

文件：`softbs/vscode/VSCODE_CHEATSHEET.md`

如需我把此文件转为 PDF 或加入到 README 侧边栏导航中，我可以继续处理。
