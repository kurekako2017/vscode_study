import { useMemo, useState } from 'react'

type Message = {
  role: 'user' | 'assistant'
  content: string
}

type Source = {
  title: string
  link: string
  score: number
}

const MOCK_SOURCES: Source[] = [
  { title: '发布与部署 FAQ', link: 'wiki://deployment-faq', score: 0.98 },
  { title: '休假与远程办公制度', link: 'file://server_docs/vacation_policy.md', score: 0.74 },
]

function buildMockAnswer(question: string): { answer: string; sources: Source[] } {
  return {
    answer: `我先根据本地资料模拟回答“${question}”。你可以把这里替换成真实 RAG API 的返回结果。`,
    sources: MOCK_SOURCES,
  }
}

export default function App() {
  const [input, setInput] = useState('远程办公和发布流程有什么要求？')
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '这里是一个最小的社内知识问答前端壳子。' },
  ])
  const [sources, setSources] = useState<Source[]>(MOCK_SOURCES)

  const latestAnswer = useMemo(
    () => messages.filter((message) => message.role === 'assistant').at(-1)?.content ?? '',
    [messages],
  )

  function sendMessage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const question = input.trim()
    if (!question) return

    setMessages((current) => [...current, { role: 'user', content: question }])
    const result = buildMockAnswer(question)
    setMessages((current) => [...current, { role: 'assistant', content: result.answer }])
    setSources(result.sources)
    setInput('')
  }

  return (
    <main className="page">
      <section className="panel">
        <header className="header">
          <h1>Agent Advanced Chat UI Demo</h1>
          <p>先把消息流、来源引用和问答布局跑通，再接真实后端。</p>
        </header>

        <form className="composer" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="输入一个社内知识问题"
          />
          <button type="submit">发送</button>
        </form>

        <div className="chat">
          {messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`bubble ${message.role}`}>
              <strong>{message.role === 'user' ? '用户' : '助手'}</strong>
              <p>{message.content}</p>
            </article>
          ))}
        </div>
      </section>

      <aside className="panel sidebar">
        <h2>引用来源</h2>
        <ul>
          {sources.map((source) => (
            <li key={source.link}>
              <strong>{source.title}</strong>
              <span>{source.link}</span>
              <em>score: {source.score.toFixed(2)}</em>
            </li>
          ))}
        </ul>

        <h2>最新回答</h2>
        <p>{latestAnswer || '暂无回答'}</p>
      </aside>
    </main>
  )
}
