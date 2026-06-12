import { createContext, useContext, useMemo, useState } from 'react'

// createContext 创建一个“跨层传值”的容器。
// 子组件可以通过 useContext 直接读取 Provider 提供的值。
const ThemeContext = createContext(null)

function ThemePreview() {
  // 子组件不需要 props 一层层往下传，直接从 Context 里取值即可。
  // 这就是 Context 最常见的使用方式：上层提供，下层消费。
  const theme = useContext(ThemeContext)

  return (
    // 这里的样式直接使用 Context 提供的颜色值，所以切换主题后会立即变化。
    <div className="card" style={{ background: theme.background, color: theme.color }}>
      <h3>主题预览</h3>
      <p>当前是 {theme.name} 主题。</p>
    </div>
  )
}

export default function ThemeContextDemo() {
  // dark 是布尔值，决定当前显示浅色还是深色主题。
  const [dark, setDark] = useState(false)

  // useMemo 用于缓存 theme 对象，避免每次渲染都创建一个新的对象引用。
  // 对初学者来说，先记住它的核心作用：减少不必要的重复创建。
  const theme = useMemo(
    () =>
      dark
        ? { name: '深色', background: '#111827', color: '#f9fafb' }
        : { name: '浅色', background: '#ffffff', color: '#111827' },
    [dark],
  )

  return (
    <article className="card stack">
      <span className="pill">useContext</span>
      <h3>主题切换</h3>
      <p className="muted">父组件提供值，子组件在更深层直接读取。</p>
      {/* Provider 负责把主题值传给下面的子组件。 */}
      {/* value 一变，所有消费这个 Context 的子组件都会跟着更新。 */}
      <ThemeContext.Provider value={theme}>
        <ThemePreview />
      </ThemeContext.Provider>
      <div className="button-row">
        {/* 点击按钮只改变一个布尔值，页面就能从浅色切换到深色。 */}
        <button onClick={() => setDark((value) => !value)}>切换主题</button>
      </div>
    </article>
  )
}
