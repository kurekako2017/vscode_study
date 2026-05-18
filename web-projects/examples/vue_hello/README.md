# Vue 3 + Vite 示例

此模板可帮助你使用 Vite 开始开发 Vue 3 项目。

## 推荐的 IDE 设置

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar)（请禁用 Vetur）。

## 推荐的浏览器设置

- 基于 Chromium 的浏览器（Chrome、Edge、Brave 等）：
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [在 Chrome 开发者工具中启用自定义对象格式化](http://bit.ly/object-formatters)
- Firefox：
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [在 Firefox 开发者工具中启用自定义对象格式化](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## 自定义配置

参见 [Vite Configuration Reference](https://vite.dev/config/)。

## 项目设置

```sh
npm install
```

### 开发模式：编译并热重载

```sh
npm run dev
```

### 生产模式：编译并压缩

```sh
npm run build
```

### 快速启动（完整步骤）

1. 确保已安装 Node.js（推荐 Node 16+ 或更高）。
2. 在项目根目录运行依赖安装：

```powershell
npm install
```

3. 启动开发服务器（带热重载）：

```powershell
npm run dev
```

4. 在浏览器中打开开发地址（默认）：

```
http://localhost:5173
```

5. 预览构建产物（可选）：

```powershell
npm run build
npm run preview
```

常见问题：
- 若端口被占用，Vite 会提示并尝试使用其它端口；也可以设置环境变量 `PORT` 来固定端口。
- 遇到依赖或构建错误，先确认 Node 版本并删除 `node_modules` 后重试 `npm install`。
