# ai-website-cloner-template 详细使用教程（2026最新版）

**项目地址**：https://github.com/JCodesMore/ai-website-cloner-template （28k+ Stars）

这个工具能用 AI 编程助手快速把任意网站逆向成**干净的 Next.js 16 + shadcn/ui + Tailwind v4** 项目。

## 第一步：创建自己的项目（必须这么做）

1. 打开 [https://github.com/JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template)
2. 点击右上角 **“Use this template”** → **“Create a new repository”**
3. 填写仓库名称（例如 `my-clone-site`），创建仓库。

## 第二步：本地初始化

```bash
# 克隆你的仓库
git clone https://github.com/你的用户名/my-clone-site.git
cd my-clone-site

# 安装依赖
npm install
```

## 第三步：启动 AI 助手并克隆网站

### 推荐：Claude Code

```bash
claude --chrome
```

在 Claude Code 中输入：

```
/clone-website https://目标网站.com
```

**批量克隆**：

```
/clone-website https://site1.com https://site2.com
```

## 第四步：预览与部署

```bash
npm run dev     # 本地预览
npm run build   # 构建生产版本
```

**部署上线**（Vercel 最简单）：
1. `git push` 到 GitHub
2. 去 [vercel.com](https://vercel.com) 导入仓库
3. 自动部署完成

## 高级用法

- `/build-from-spec`：根据规格重建组件
- `/customize`：整体风格调整
- 支持 Cursor、Copilot 等多个 AI 工具

## 注意事项

- **合法使用**：仅用于自己网站、学习、源码恢复
- 复杂动画网站可能需手动优化
- 推荐先用设计现代的网站练习

---

**教程结束**。祝你克隆顺利！

如需修改或添加示例，随时告诉我。
