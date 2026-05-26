/*
  `App` 组件（入口页面）
  - 目的：展示最小的 React + Vite 示例页面，用于教学与练手。
  - 对应后端/JSP：在学习迁移时，可将此页面的内容映射到对应的 JSP 片段。
*/
export default function App() {
  // 返回应用的根节点结构（JSX）
  return (
    // 主容器：应用外壳，通常用于放置布局相关的全局样式
    <main className="app-shell">
      {/* 卡片区域：示例页面的主要可见区域 */}
      <section className="card">
        {/* 小标题/徽标文本，说明这是一个 React + Vite 项目 */}
        <p className="eyebrow">React + Vite</p>
        {/* 页面主标题 */}
        <h1>Hello React!</h1>
        {/* 描述性文本：说明示例用途与练习目标 */}
        <p>这是一个最小但完整的 React 示例，用来练习组件、样式与入口文件结构。</p>
      </section>
    </main>
  )
}
