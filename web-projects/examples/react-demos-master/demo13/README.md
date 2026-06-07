这个示例复制自 [github.com/mhart/react-server-example](https://github.com/mhart/react-server-example)，我用 JSX 语法重新整理过。

## 如何运行

```bash
# 进入 demo13 目录
cd web-projects/examples/react-demos-master/demo13

# 安装依赖
npm install

# 把 src 目录里的 jsx 文件编译成 js 文件
npm run build

# 启动 HTTP 服务器
node server.js
```

启动后，在浏览器里打开：

```text
http://localhost:3000
```

## 如何学习

这个示例最适合按下面的顺序看：

1. 先看 `src/app.js`，理解服务端渲染时组件是怎么写的
2. 再看 `src/browser.js`，理解浏览器端如何接管已经渲染好的页面
3. 最后看 `src/server.js`，理解服务器如何把 HTML、初始数据和前端脚本拼起来

如果你要边改边学，推荐这样做：

- 先改 `src/app.js` 里的文案
- 重新执行 `npm run build`
- 刷新 `http://localhost:3000`
- 观察页面是如何变化的

这样你会很快看懂“服务端先渲染一版 HTML，浏览器再接管”的整体流程。
