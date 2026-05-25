# GitHub Pages 网站发布教程

本教程将指导你如何在 GitHub 上创建一个网站，并通过 GitHub Pages 免费发布。

---

## 1. 注册 GitHub 账号
- 访问 [https://github.com/](https://github.com/) 注册账号。

## 2. 新建仓库
1. 登录 GitHub，点击右上角“+” → New repository。
2. 仓库命名建议：`your-username.github.io`（个人主页型），或任意名称（项目型）。
3. 选择 Public（公开），可勾选 Initialize with a README。
4. 点击 Create repository。

## 3. 准备网站文件
- 可用 HTML/CSS/JS 静态网页，也可用 Jekyll、Hugo 等静态站点生成器。
- 示例：新建 `index.html`，内容如下：
  ```html
  <!DOCTYPE html>
  <html>
  <head><meta charset="utf-8"><title>Hello GitHub Pages</title></head>
  <body><h1>我的第一个 GitHub Pages 网站！</h1></body>
  </html>
  ```

## 4. 上传网站文件到仓库
### 方法一：网页上传
1. 进入仓库页面，点击 Add file → Upload files。
2. 拖拽或选择本地文件上传。
3. 填写 commit 信息，点击 Commit changes。

### 方法二：Git 命令行
1. 安装 Git 并配置（[下载](https://git-scm.com/)）。
2. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
3. 添加文件并推送：
   ```bash
   git add .
   git commit -m "add website files"
   git push
   ```

## 5. 启用 GitHub Pages
1. 进入仓库页面，点击 Settings → Pages。
2. Source 选择 `main` 分支（或 `gh-pages`），文件夹选 `/ (root)`。
3. 点击 Save。
4. 稍等片刻，页面会显示网站访问地址，如：
   - `https://your-username.github.io/`（个人主页型）
   - `https://your-username.github.io/your-repo/`（项目型）

## 6. 访问你的网站
- 用浏览器访问上面显示的网址即可。

---

## 常见问题
- **更改内容后如何更新？**
  - 只需再次上传/推送文件，GitHub Pages 会自动重新部署。
- **自定义域名？**
  - 在 Pages 设置中绑定域名，并在域名服务商设置 CNAME 解析。
- **支持 HTTPS 吗？**
  - GitHub Pages 默认支持 HTTPS。

---

如需更详细教程或遇到问题，欢迎随时提问！