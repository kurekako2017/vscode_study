import { createContext, useContext, useMemo, useState } from 'react'

const ThemeContext = createContext(null)

function ThemePreview() {
  const theme = useContext(ThemeContext)

  return (
    <div className="card" style={{ background: theme.background, color: theme.color }}>
      <h3>主题预览</h3>
      <p>当前是 {theme.name} 主题。</p>
    </div>
  )
}

export default function ThemeContextDemo() {
  const [dark, setDark] = useState(false)

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
      <ThemeContext.Provider value={theme}>
        <ThemePreview />
      </ThemeContext.Provider>
      <div className="button-row">
        <button onClick={() => setDark((value) => !value)}>切换主题</button>
      </div>
    </article>
  )
}
