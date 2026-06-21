import { useEffect, useRef, useState } from 'react'

const DEFAULT_BASE_URL = import.meta.env.VITE_RAG_API_BASE_URL || 'http://127.0.0.1:8000'
const DEFAULT_MODEL = 'gpt-5'
const DEFAULT_QUESTION = '请总结文档重点，并列出最重要的来源。'

// 浏览器只是客户端；真正使用的 provider/model 由 FastAPI 后端决定。
console.info(`MODEL: provider=backend model=${DEFAULT_MODEL} mode=selected-by-api`)

function normalizeBaseUrl(value) {
  // 去掉末尾斜杠，避免拼接接口路径时出现 //health。
  return value.replace(/\/+$/, '')
}

function formatSourceLabel(source) {
  // 把后端来源对象转换成页面上容易阅读的一行文字。
  if (!source) {
    return 'unknown'
  }
  return `${source.source_label} · score ${source.score}`
}

function createEntryId(prefix) {
  // 优先使用浏览器 UUID；旧环境没有该 API 时退回时间戳和随机数。
  return `${prefix}-${globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`}`
}

export default function App() {
  // 连接配置、问答结果和页面操作状态分别保存，便于初学者逐项观察变化。
  const [baseUrl, setBaseUrl] = useState(DEFAULT_BASE_URL)
  const [question, setQuestion] = useState(DEFAULT_QUESTION)
  const [model, setModel] = useState(DEFAULT_MODEL)
  const [health, setHealth] = useState(null)
  const [rootInfo, setRootInfo] = useState(null)
  const [answer, setAnswer] = useState(null)
  const [history, setHistory] = useState([])
  const [activity, setActivity] = useState([])
  const [busyAction, setBusyAction] = useState(null)
  const [error, setError] = useState('')
  const didInit = useRef(false)

  const endpoint = normalizeBaseUrl(baseUrl)

  async function requestJson(url, options) {
    // 所有 HTTP 请求共用这里的 JSON 解析和错误处理。
    const response = await fetch(url, options)
    const payload = await response.json().catch(() => null)
    if (!response.ok) {
      const message = payload?.detail || payload?.message || response.statusText
      throw new Error(message)
    }
    return payload
  }

  async function loadRootInfo() {
    setBusyAction('root')
    setError('')
    try {
      const data = await requestJson(`${endpoint}/`, {
        method: 'GET',
        headers: { Accept: 'application/json' },
      })
      setRootInfo(data)
      setActivity((current) => [
        ...current,
        {
          id: createEntryId('root'),
          type: 'root',
          title: '检查根路径',
          detail: data.message || '服务根路径正常返回。',
        },
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : '无法获取服务根路径信息')
    } finally {
      setBusyAction(null)
    }
  }

  async function loadHealth() {
    setBusyAction('health')
    setError('')
    try {
      const data = await requestJson(`${endpoint}/health`, {
        method: 'GET',
        headers: { Accept: 'application/json' },
      })
      setHealth(data)
      setActivity((current) => [
        ...current,
        {
          id: createEntryId('health'),
          type: 'health',
          title: '检查健康状态',
          detail: `docs_dir: ${data.docs_dir}, chunks: ${data.chunk_count}`,
        },
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : '健康检查失败')
    } finally {
      setBusyAction(null)
    }
  }

  async function askQuestion() {
    setBusyAction('ask')
    setError('')
    setHistory((current) => [
      ...current,
      {
        id: createEntryId('question'),
        role: 'user',
        text: question,
      },
    ])
    try {
      // model 是用户选择的请求模型；后端仍可能按回退策略改用其他 provider。
      const data = await requestJson(`${endpoint}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ question, model }),
      })
      setAnswer(data)
      console.info(`MODEL: provider=backend model=${data.model} mode=api-response`)
      setHistory((current) => [
        ...current,
        {
          id: createEntryId('answer'),
          role: 'assistant',
          text: data.answer,
          meta: `${data.source_count} sources · ${data.model}`,
          sources: data.sources || [],
        },
      ])
      setHealth((current) =>
        current
          ? {
              ...current,
              docs_dir: data.docs_dir,
            }
          : current,
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : '问答失败')
    } finally {
      setBusyAction(null)
    }
  }

  async function reloadDocs() {
    setBusyAction('reload')
    setError('')
    try {
      const data = await requestJson(`${endpoint}/reload`, {
        method: 'POST',
        headers: { Accept: 'application/json' },
      })
      setHealth((current) =>
        current
          ? {
              ...current,
              docs_dir: data.docs_dir,
              chunk_count: data.chunk_count,
            }
          : {
              status: 'ok',
              docs_dir: data.docs_dir,
              chunk_count: data.chunk_count,
            },
      )
      setActivity((current) => [
        ...current,
        {
          id: createEntryId('reload'),
          type: 'reload',
          title: '重载文档',
          detail: `docs_dir: ${data.docs_dir}, chunks: ${data.chunk_count}`,
        },
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : '重载失败')
    } finally {
      setBusyAction(null)
    }
  }

  function clearHistory() {
    setHistory([])
  }

  useEffect(() => {
    if (didInit.current) {
      return
    }
    didInit.current = true
    void (async () => {
      await loadRootInfo()
      await loadHealth()
    })()
  }, [])

  const statusText = busyAction
    ? `正在执行 ${busyAction}`
    : error
      ? '有请求失败'
      : '准备就绪'

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">React client for rag_api_demo</p>
          <h1>最常见的 agent 客户端，就是一个 Web 应用。</h1>
          <p className="lead">
            这个页面就是调用 `FastAPI` 的前端客户端，它会用 `fetch` 请求 `GET /health`、
            `POST /ask` 和 `POST /reload`。
          </p>

          <div className="hero-metrics">
            <article className="metric">
              <span>Base URL</span>
              <strong>{endpoint}</strong>
            </article>
            <article className="metric">
              <span>Status</span>
              <strong>{statusText}</strong>
            </article>
          </div>
        </div>

        <aside className="hero-panel">
          <div className="panel-card">
            <p className="panel-title">客户端角色说明</p>
            <ul>
              <li>浏览器是客户端</li>
              <li>React 页面是 UI 客户端</li>
              <li>`main.py` 启动的 FastAPI 是服务端</li>
              <li>本地文档是数据源</li>
            </ul>
          </div>
        </aside>
      </section>

      <section className="content-grid">
        <div className="stack">
          <section className="card">
            <div className="card-head">
              <h2>服务连接</h2>
              <div className="actions">
                <button type="button" onClick={loadRootInfo} disabled={busyAction !== null}>
                  检查 /
                </button>
                <button type="button" onClick={loadHealth} disabled={busyAction !== null}>
                  检查 /health
                </button>
              </div>
            </div>

            <label className="field">
              <span>Backend URL</span>
              <input
                value={baseUrl}
                onChange={(event) => setBaseUrl(event.target.value)}
                placeholder="http://127.0.0.1:8000"
              />
            </label>

            <div className="info-row">
              <div className="info-box">
                <span>Root</span>
                <strong>{rootInfo?.status || 'unknown'}</strong>
                <small>{rootInfo?.message || '点击“检查 /”获取信息'}</small>
              </div>
              <div className="info-box">
                <span>Health</span>
                <strong>{health?.status || 'unknown'}</strong>
                <small>{health ? `${health.chunk_count} chunks` : '点击“检查 /health”获取信息'}</small>
              </div>
            </div>
          </section>

          <section className="card">
            <div className="card-head">
              <h2>问答调用</h2>
              <button type="button" className="primary" onClick={askQuestion} disabled={busyAction !== null}>
                发送问题
              </button>
            </div>

            <label className="field">
              <span>Question</span>
              <textarea
                rows="6"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="请输入你想问的问题"
              />
            </label>

            <div className="inline-fields">
              <label className="field">
                <span>Model</span>
                <input value={model} onChange={(event) => setModel(event.target.value)} />
              </label>
              <div className="field">
                <span>Quick action</span>
                <div className="actions compact">
                  <button type="button" onClick={() => setQuestion(DEFAULT_QUESTION)}>
                    恢复示例问题
                  </button>
                  <button type="button" onClick={reloadDocs} disabled={busyAction !== null}>
                    重载文档
                  </button>
                </div>
              </div>
            </div>
          </section>
        </div>

        <div className="stack">
          <section className="card response-card">
            <div className="card-head">
              <h2>响应</h2>
              <span className="badge">{answer ? `${answer.source_count} sources` : 'waiting'}</span>
            </div>

            <div className="response-block">
              <p className="label">Answer</p>
              <pre>{answer?.answer || '点击“发送问题”后这里会显示返回内容。'}</pre>
            </div>

            <div className="response-meta">
              <div>
                <span>model</span>
                <strong>{answer?.model || model}</strong>
              </div>
              <div>
                <span>docs_dir</span>
                <strong>{answer?.docs_dir || health?.docs_dir || 'unknown'}</strong>
              </div>
            </div>

            <div>
              <p className="label">Sources</p>
              <div className="sources">
                {(answer?.sources || []).length > 0 ? (
                  answer.sources.map((source) => (
                    <div key={`${source.source_label}-${source.score}`} className="source-chip">
                      {formatSourceLabel(source)}
                    </div>
                  ))
                ) : (
                  <p className="empty-state">还没有来源，发送一次问题后会显示。</p>
                )}
              </div>
            </div>
          </section>

          <section className="card">
            <div className="card-head">
              <h2>对话历史</h2>
              <button type="button" onClick={clearHistory} disabled={history.length === 0}>
                清空
              </button>
            </div>

            <div className="conversation">
              {history.length > 0 ? (
                history.map((entry) => (
                  <article key={entry.id} className={`message ${entry.role}`}>
                    <span className="message-role">{entry.role === 'user' ? 'User' : 'Assistant'}</span>
                    <p>{entry.text}</p>
                    {entry.meta ? <small>{entry.meta}</small> : null}
                    {entry.sources?.length ? (
                      <div className="message-sources">
                        {entry.sources.map((source) => (
                          <span key={`${entry.id}-${source.source_label}-${source.score}`} className="source-chip">
                            {formatSourceLabel(source)}
                          </span>
                        ))}
                      </div>
                    ) : null}
                  </article>
                ))
              ) : (
                <p className="empty-state">还没有对话，先发一个问题试试。</p>
              )}
            </div>
          </section>

          <section className="card">
            <h2>调用顺序</h2>
            <ol className="steps">
              <li>React 客户端通过 `fetch` 调用后端。</li>
              <li>FastAPI 接口接收请求。</li>
              <li>服务按需加载文档状态。</li>
              <li>服务执行检索并生成回答。</li>
              <li>前端展示结果和来源。</li>
            </ol>
            <div className="activity-log">
              <p className="label">Activity</p>
              {activity.length > 0 ? (
                activity.slice(-4).map((item) => (
                  <div key={item.id} className="activity-item">
                    <strong>{item.title}</strong>
                    <span>{item.detail}</span>
                  </div>
                ))
              ) : (
                <p className="empty-state">操作记录会显示在这里。</p>
              )}
            </div>
          </section>
        </div>
      </section>

      {error ? <div className="toast error">{error}</div> : null}
    </main>
  )
}
