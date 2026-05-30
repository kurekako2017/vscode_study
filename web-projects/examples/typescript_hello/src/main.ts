import './style.css'

type Lesson = {
  title: string
  description: string
  steps: string[]
}

const lesson: Lesson = {
  title: 'Hello TypeScript!',
  description: '这是一个 Vanilla TypeScript + Vite 最小示例，重点观察类型、DOM 渲染和构建流程。',
  steps: ['定义类型', '创建数据', '渲染到页面'],
}

const app = document.querySelector<HTMLDivElement>('#app')

if (!app) {
  throw new Error('Missing #app element')
}

app.innerHTML = `
  <main class="page-shell">
    <section class="hero-card">
      <p class="eyebrow">TypeScript</p>
      <h1>${lesson.title}</h1>
      <p>${lesson.description}</p>
      <ol>
        ${lesson.steps.map((step) => `<li>${step}</li>`).join('')}
      </ol>
    </section>
  </main>
`
