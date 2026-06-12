# 项目结构

```text
react-modern-learning/
├─ index.html（页面挂载入口）
├─ package.json（项目依赖与脚本）
├─ vite.config.js（Vite 构建配置）
├─ README.md（快速学习入口）
├─ LEARN.md（详细学习说明）
└─ src/
   ├─ main.jsx（React 应用入口）
   ├─ App.jsx（应用主页面）
   ├─ style.css
   ├─ data/
   │  └─ chapters.js
   ├─ chapters/
   │  ├─ home/
   │  │  └─ HomePage.jsx（章节总入口）
   │  ├─ hooks/
   │  │  ├─ HooksPage.jsx（Hooks 章节页）
   │  │  ├─ useState/
   │  │  │  └─ CounterDemo.jsx（计数器示例）
   │  │  └─ useEffect/
   │  │     └─ TimerDemo.jsx（定时器示例）
   │  ├─ router/
   │  │  ├─ RouterPage.jsx（Router 章节页）
   │  │  └─ RouterDemo.jsx（路由说明示例）
   │  ├─ context/
   │  │  ├─ ContextPage.jsx（Context 章节页）
   │  │  └─ ThemeContextDemo.jsx（主题切换示例）
   │  ├─ api/
   │  │  ├─ ApiPage.jsx（API 章节页）
   │  │  └─ PostsDemo.jsx（帖子列表示例）
   │  └─ test/
   │     ├─ TestPage.jsx（Test 章节页）
   │     ├─ Counter.jsx（计数器组件）
   │     └─ Counter.test.jsx（计数器测试）
   └─ test/
      └─ setup.js（测试环境初始化）
```

## 页面名称总览

- `HomePage.jsx`：章节总入口
- `HooksPage.jsx`：Hooks 章节页
- `CounterDemo.jsx`：计数器示例
- `TimerDemo.jsx`：定时器示例
- `RouterPage.jsx`：Router 章节页
- `RouterDemo.jsx`：路由说明示例
- `ContextPage.jsx`：Context 章节页
- `ThemeContextDemo.jsx`：主题切换示例
- `ApiPage.jsx`：API 章节页
- `PostsDemo.jsx`：帖子列表示例
- `TestPage.jsx`：Test 章节页
- `Counter.jsx`：计数器组件
- `Counter.test.jsx`：计数器测试
- `setup.js`：测试环境初始化

## 页面目录结构

```text
AppShell（公共外壳）
├─ 顶部导航栏
├─ 页面标题区域
└─ 内容区
   ├─ /                -> HomePage.jsx
   │  ├─ 页面名称：章节总入口
   │  └─ 简述功能：展示所有章节卡片，作为整个项目的学习入口
   ├─ /hooks           -> HooksPage.jsx
   │  ├─ 页面名称：Hooks 章节页
   │  └─ 简述功能：讲解 useState 和 useEffect 这两个基础 Hook
   │  ├─ CounterDemo.jsx
   │  │  ├─ 页面名称：计数器示例
   │  │  └─ 简述功能：演示状态更新、事件处理和派生值
   │  └─ TimerDemo.jsx
   │     ├─ 页面名称：定时器示例
   │     └─ 简述功能：演示副作用、定时器启动和清理
   ├─ /router          -> RouterPage.jsx
   │  ├─ 页面名称：Router 章节页
   │  └─ 简述功能：演示嵌套路由、导航切换和子页面插槽
   │  ├─ RouterHome
   │  │  ├─ 页面名称：路由首页子页
   │  │  └─ 简述功能：作为 /router 的默认子页面
   │  ├─ AboutPage
   │  │  ├─ 页面名称：About 子页
   │  │  └─ 简述功能：演示静态子路由切换
   │  └─ UserProfile
   │     ├─ 页面名称：用户详情页
   │     └─ 简述功能：演示动态参数路由 /router/users/:id
   ├─ /context         -> ContextPage.jsx
   │  ├─ 页面名称：Context 章节页
   │  └─ 简述功能：讲解跨层传值、Provider 和 useContext
   │  └─ ThemeContextDemo.jsx
   │     ├─ 页面名称：主题切换示例
   │     └─ 简述功能：演示上下文传值和主题状态切换
   ├─ /api             -> ApiPage.jsx
   │  ├─ 页面名称：API 章节页
   │  └─ 简述功能：讲解请求数据后的 loading、error、success 三态
   │  └─ PostsDemo.jsx
   │     ├─ 页面名称：帖子列表示例
   │     └─ 简述功能：演示 fetch 请求、数据渲染和请求取消
   └─ /test            -> TestPage.jsx
      ├─ 页面名称：Test 章节页
      └─ 简述功能：讲解组件与测试文件如何配对学习
      ├─ Counter.jsx
      │  ├─ 页面名称：计数器组件
      │  └─ 简述功能：提供一个可交互的小组件供测试使用
      └─ Counter.test.jsx
         ├─ 页面名称：计数器测试
         └─ 简述功能：验证点击按钮后计数是否正确增加
```

### 怎么读这张图

- `AppShell` 是所有页面共享的外壳，负责导航和整体布局
- `/` 是首页，负责把所有章节卡片列出来
- 每个章节路由下面再挂自己的页面组件和 demo 组件
- `Router` 章节最特别，它还有子路由，所以能看到嵌套路由和动态参数
- `Test` 章节把组件和测试文件放在一起，方便对照学习

## 设计原则

- 首页负责导航，不负责复杂逻辑
- 每个章节一个目录
- 每个子例子一个文件
- 测试文件和组件文件并排放
