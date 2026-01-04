# 📖 IDEA Markdown插件安装指南

> **让你的IntelliJ IDEA完美支持Markdown文件预览和编辑**

---

## 📑 目录
- [为什么需要Markdown插件](#为什么需要markdown插件)
- [方法一：推荐使用内置插件（最简单）](#方法一推荐使用内置插件最简单)
- [方法二：安装第三方增强插件](#方法二安装第三方增强插件)
- [使用技巧](#使用技巧)
- [常见问题](#常见问题)

---

## 为什么需要Markdown插件

IntelliJ IDEA **2020.1及以上版本已内置Markdown支持**，但如果你想要：
- ✅ 实时预览Markdown渲染效果
- ✅ 更好的语法高亮
- ✅ 表格、图表、流程图支持
- ✅ 导出为HTML/PDF
- ✅ 目录（TOC）自动生成

那么你需要确认插件是否已启用或安装增强插件。

---

## 方法一：推荐使用内置插件（最简单）

### ✅ 步骤1：检查内置Markdown插件是否启用

1. **打开IDEA**，点击菜单栏：
   ```
   File → Settings (Windows/Linux)
   或
   IntelliJ IDEA → Preferences (macOS)
   ```

2. **进入插件管理**：
   ```
   左侧菜单 → Plugins
   ```

3. **切换到"Installed"标签页**

4. **搜索"Markdown"**

5. **确认以下插件已启用**（打勾）：
   - ✅ **Markdown** (JetBrains官方插件)
   - ✅ **Grazie** (可选，提供语法检查)

6. **如果插件被禁用**：
   - 找到 "Markdown" 插件
   - 右侧勾选复选框
   - 点击 "OK"
   - 重启IDEA

### ✅ 步骤2：验证Markdown功能

1. **打开任意 `.md` 文件**（如本项目的 `README.md`）

2. **查看编辑器右上角**，应该有三个按钮：
   - 📝 **Editor only** - 仅编辑模式
   - 🔄 **Editor and preview** - 分屏模式（推荐）
   - 👁️ **Preview only** - 仅预览模式

3. **点击分屏图标** 🔄，即可看到：
   ```
   左侧：Markdown源码
   右侧：实时渲染预览
   ```

### ✅ 步骤3：配置Markdown设置（可选）

1. **进入设置**：
   ```
   File → Settings → Languages & Frameworks → Markdown
   ```

2. **推荐配置**：
   - ✅ 启用 **Preview browser**: IntelliJ HTML panel
   - ✅ 启用 **Auto-scroll preview**（自动滚动预览）
   - ✅ 启用 **Show line numbers**（显示行号）
   - ✅ 启用 **Soft-wrap files**（自动换行）

3. **点击 "OK" 保存**

---

## 方法二：安装第三方增强插件

如果你需要更强大的功能，可以安装第三方插件。

### ⚠️ 重要说明

**Markdown Navigator Enhanced** 插件可能因以下原因搜索不到：
- 📌 插件已更名或停止维护
- 📌 需要使用不同的搜索关键词
- 📌 IntelliJ IDEA内置插件已足够强大

**建议：优先使用IDEA内置的Markdown插件（方法一），功能已经很完善！**

---

### 🎯 可选插件：Markdown（如未启用）

**这是IDEA官方内置插件，推荐使用！**

**功能特点**：
- ✅ 实时预览（分屏/独立预览）
- ✅ 语法高亮
- ✅ 代码块高亮
- ✅ 表格支持
- ✅ 链接跳转
- ✅ 图片预览
- ✅ HTML导出

**启用步骤**：

1. **打开插件管理**：
   ```
   File → Settings → Plugins → Installed
   ```

2. **搜索 "Markdown"**

3. **确认插件已启用**（勾选）

4. **如未启用，勾选并重启IDEA**

---

### 🎯 其他可选增强插件

#### 1. Grazie Professional（语法检查）

**功能**：为Markdown提供拼写和语法检查

**安装**：
```
Settings → Plugins → Marketplace
搜索：Grazie Professional
```

#### 2. PlantUML Integration（图表支持）

**功能**：在Markdown中绘制UML图

**安装**：
```
Settings → Plugins → Marketplace
搜索：PlantUML integration
```

#### 3. Diagrams.net Integration（流程图）

**功能**：在Markdown中创建流程图、架构图

**安装**：
```
Settings → Plugins → Marketplace
搜索：diagrams.net
```

---

### 💡 如果确实想要增强功能

**推荐使用以下插件名称搜索**（2024年可用）：

1. 搜索："**Markdown**" - 确认官方插件已启用
2. 搜索："**Markdown Support**" - 可能的替代品
3. 搜索："**Markdown Editor**" - 轻量级编辑器

**通用安装步骤**：

1. **打开插件市场**：
   ```
   File → Settings → Plugins → Marketplace
   ```

2. **搜索插件名称**

3. **点击 "Install" 按钮**

4. **等待下载完成**

5. **点击 "Restart IDE" 重启IDEA**

6. **重启后打开 `.md` 文件验证**


---

## 使用技巧

### 📝 1. 快速切换预览模式

**快捷键**：
- Windows/Linux: `Ctrl + Shift + P`
- macOS: `Cmd + Shift + P`

### 📝 2. 分屏预览（推荐）

1. 打开Markdown文件
2. 点击右上角的 **分屏图标** 🔄
3. 左侧编辑，右侧实时预览

### 📝 3. 导出HTML

1. 在Markdown文件中右键
2. 选择 **Copy as HTML**
3. 或使用插件的导出功能

### 📝 4. 自动生成目录

**IDEA内置方式**（推荐）：
在Markdown文件中使用标题结构，IDEA会自动识别文档大纲

**查看文档大纲**：
1. 打开Markdown文件
2. 点击右上角的 **Structure** 按钮（或按 `Alt + 7`）
3. 可以看到文档的标题树形结构
4. 点击任意标题可快速跳转

**手动创建目录**：
```markdown
## 目录
- [第一章](#第一章)
- [第二章](#第二章)
  - [2.1 小节](#21-小节)

## 第一章
内容...

## 第二章
内容...

### 2.1 小节
内容...
```

### 📝 5. 表格编辑技巧

**IDEA内置支持**：
IDEA的Markdown插件对表格有良好支持

**表格语法**：
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

**快速对齐**：
1. 输入表格后，光标放在表格内
2. 使用 `Tab` 键在单元格间跳转
3. IDEA会自动格式化表格对齐

**预览效果**：
表格会在预览窗口中自动渲染为漂亮的HTML表格

### 📝 6. 查看本项目的Markdown文档

现在你可以舒适地查看项目中的所有文档：
- ✅ `README.md` - 项目说明
- ✅ `项目框架与调用流程完整总结.md` - 框架总结
- ✅ `STARTUP_SUCCESS.md` - 启动成功总结
- ✅ 各种指南文档

---

## 常见问题

### ❓ Q1: 看不到预览按钮？

**解决方案**：
1. 确认文件扩展名是 `.md` 或 `.markdown`
2. 检查Markdown插件是否启用
3. 重启IDEA

### ❓ Q2: 预览样式不好看？

**解决方案**：
1. 进入 `Settings → Languages & Frameworks → Markdown`
2. 选择 **CSS settings**
3. 可以自定义CSS样式
4. 或者选择不同的预览主题

### ❓ Q3: 无法显示代码高亮？

**解决方案**：
1. 使用三个反引号 \`\`\` 包裹代码块
2. 指定语言类型，如：
   ````markdown
   ```java
   public class Test {}
   ```
   ````

### ❓ Q4: 图片无法显示？

**解决方案**：
1. 使用相对路径：`![图片](./images/pic.png)`
2. 或使用绝对路径
3. 确保图片文件存在

### ❓ Q5: Markdown Navigator Enhanced是付费的？

**答**：
- 基础功能免费
- 高级功能需要许可证
- 可以先试用基础功能
- IntelliJ内置的Markdown插件对大多数用户已足够

### ❓ Q6: 预览和GitHub显示效果不一样？

**解决方案**：
1. IDEA的Markdown插件支持 **GitHub Flavored Markdown (GFM)**
2. 在设置中确认：
   ```
   Settings → Languages & Frameworks → Markdown
   → 选择 GitHub flavor
   ```
3. 大部分情况下，预览效果与GitHub一致
4. 如需精确验证，可以直接在GitHub上预览

**提示**：某些GitHub特定的功能（如任务列表、提及用户等）可能显示略有差异，但基础Markdown语法完全兼容。

---

## 🎉 安装完成后的使用建议

### 1️⃣ 立即打开查看项目文档

```
推荐按以下顺序阅读：
1. README.md - 了解项目基本信息
2. 项目框架与调用流程完整总结.md - 深入理解项目架构
3. STARTUP_SUCCESS.md - 学习启动流程
4. CONTROLLER_注释说明.md - 理解Controller层
```

### 2️⃣ 使用分屏模式

- 左侧：编辑Markdown
- 右侧：实时预览效果
- **最舒适的阅读体验** ✨

### 3️⃣ 善用搜索功能

在Markdown文件中按 `Ctrl + F` (Windows/Linux) 或 `Cmd + F` (macOS) 快速查找内容

### 4️⃣ 设置合适的字体和大小

```
Settings → Editor → Font
推荐字体：
- Consolas (Windows)
- Monaco (macOS)
- JetBrains Mono (跨平台)
```

---

## 📚 更多资源

- [IntelliJ IDEA官方Markdown文档](https://www.jetbrains.com/help/idea/markdown.html)
- [Markdown语法指南](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)

---

## ✅ 快速验证清单

安装完成后，请验证以下功能：

- [ ] 可以打开 `.md` 文件
- [ ] 右上角有预览按钮
- [ ] 可以切换到分屏模式
- [ ] 代码块有语法高亮
- [ ] 表格正常显示
- [ ] 标题层级清晰
- [ ] 链接可以点击
- [ ] 图片正常显示

---

## 🎊 恭喜！

现在你可以在IDEA中愉快地阅读和编辑Markdown文档了！

**立即试试打开本项目的文档，享受流畅的阅读体验吧！** 📖✨

---

*最后更新：2026-01-03*

