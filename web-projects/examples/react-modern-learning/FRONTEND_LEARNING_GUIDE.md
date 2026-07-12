# Frontend Learning Guide

这个项目的学习路径按真实源码组织，不按概念堆文档。

## 架构路径

```text
main.jsx
↓
App.jsx
↓
Router
↓
Page
↓
Component
↓
Hook
↓
Event
↓
State
↓
Render
↓
Test
```

## 当前项目入口

- `src/main.jsx`：挂载 React、包住 `BrowserRouter`
- `src/App.jsx`：定义外层 Layout、导航、Routes
- `src/data/chapters.js`：生成首页和顶部导航
- `src/learning/`：统一 Trace、学习面板、路由桥接

## 页面怎么找源码

1. 先看右侧 `Learning Panel`
2. 读 `Current Route` 和 `Current Page`
3. 看 `Component Tree` 找到页面组件和子组件
4. 看 `Source Files` 找到真实源码文件
5. 看 `Test File` 找到对应测试
6. 对照页面上的按钮、状态和 Trace，回到源码找对应函数

## 页面到源码示例

- `HooksPage` → `src/chapters/hooks/HooksPage.jsx`
- `CounterDemo` → `src/chapters/hooks/useState/CounterDemo.jsx`
- `TimerDemo` → `src/chapters/hooks/useEffect/TimerDemo.jsx`
- `RouterPage` → `src/chapters/router/RouterPage.jsx`
- `ThemeContextDemo` → `src/chapters/context/ThemeContextDemo.jsx`
- `PostsDemo` → `src/chapters/api/PostsDemo.jsx`
- `Counter` → `src/chapters/test/Counter.jsx`
- `Counter.test.jsx` → `src/chapters/test/Counter.test.jsx`

## Trace 阅读顺序

```text
BOOT
→ ROUTE
→ RENDER
→ COMPONENT
→ HOOK
→ EVENT
→ CALL
→ STATE
→ EFFECT
→ CLEANUP
→ ERROR
```

## 学习建议

- 先看页面，再看 `Learning Panel`
- 再回到对应源码和测试
- 如果你改了按钮，先找 `EVENT` 和 `CALL`
- 如果你改了状态，先找 `STATE`
- 如果页面重渲染，先看 `Why render`

