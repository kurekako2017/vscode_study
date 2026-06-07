# 项目结构

```text
react-modern-learning/
├─ index.html
├─ package.json
├─ vite.config.js
├─ README.md
├─ LEARN.md
└─ src/
   ├─ main.jsx
   ├─ App.jsx
   ├─ style.css
   ├─ data/
   │  └─ chapters.js
   ├─ chapters/
   │  ├─ home/
   │  │  └─ HomePage.jsx
   │  ├─ hooks/
   │  │  ├─ HooksPage.jsx
   │  │  ├─ useState/
   │  │  │  └─ CounterDemo.jsx
   │  │  └─ useEffect/
   │  │     └─ TimerDemo.jsx
   │  ├─ router/
   │  │  ├─ RouterPage.jsx
   │  │  └─ RouterDemo.jsx
   │  ├─ context/
   │  │  ├─ ContextPage.jsx
   │  │  └─ ThemeContextDemo.jsx
   │  ├─ api/
   │  │  ├─ ApiPage.jsx
   │  │  └─ PostsDemo.jsx
   │  └─ test/
   │     ├─ TestPage.jsx
   │     ├─ Counter.jsx
   │     └─ Counter.test.jsx
   └─ test/
      └─ setup.js
```

## 设计原则

- 首页负责导航，不负责复杂逻辑
- 每个章节一个目录
- 每个子例子一个文件
- 测试文件和组件文件并排放
