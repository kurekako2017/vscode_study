import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

// 教学要点：
// - 这个前端不是普通聊天框，而是“任务运行控制台”。
// - 用户提交问题后，后端创建 task，前端用 SSE 订阅 task events。
// - 页面把固定问数工作流、研究 Agent、执行时间线、最终报告分区展示。

type RunMode = 'auto' | 'data' | 'research' | 'hybrid';

type RunEvent = {
  task_id: string;
  type: string;
  message: string;
  payload: Record<string, unknown>;
  timestamp: string;
};

type CreateTaskResponse = {
  task_id: string;
  status: string;
  sse_url: string;
  websocket_url: string;
};

const exampleQuestion =
  '売上と在庫を確認し、市場トレンドと競合を含めて経営会議向けに報告';

function App() {
  // React state 对应后端任务生命周期：输入 -> 创建任务 -> 接收事件 -> 展示报告。
  const [question, setQuestion] = React.useState(exampleQuestion);
  const [mode, setMode] = React.useState<RunMode>('hybrid');
  const [taskId, setTaskId] = React.useState('');
  const [status, setStatus] = React.useState('idle');
  const [events, setEvents] = React.useState<RunEvent[]>([]);
  const [report, setReport] = React.useState('');
  const [error, setError] = React.useState('');

  async function startTask() {
    // 1. 先调用 REST API 创建任务。
    // 2. 后端立即返回 task_id，不等待长任务完成。
    // 3. 前端再用 task_id 建立 SSE 连接。
    setStatus('creating');
    setEvents([]);
    setReport('');
    setError('');
    const response = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, mode })
    });
    if (!response.ok) {
      setStatus('failed');
      setError(`HTTP ${response.status}`);
      return;
    }
    const body = (await response.json()) as CreateTaskResponse;
    setTaskId(body.task_id);
    setStatus(body.status);
    connectSse(body.task_id);
  }

  function connectSse(nextTaskId: string) {
    // SSE 是浏览器原生能力，适合“服务端持续推送进度，客户端只读”的场景。
    // 如果后续要做人工审批、取消任务、继续任务，可以再使用 WebSocket。
    const source = new EventSource(`/api/tasks/${nextTaskId}/events`);
    const eventTypes = [
      'started',
      'route',
      'workflow_started',
      'workflow_completed',
      'research_started',
      'research_completed',
      'report_started',
      'completed',
      'failed'
    ];
    const listener = (message: MessageEvent) => {
      // 后端每个事件都是 RunEvent JSON。前端不解析业务细节，只按 type 分区展示。
      const event = JSON.parse(message.data) as RunEvent;
      handleEvent(event);
      if (event.type === 'completed' || event.type === 'failed') {
        source.close();
      }
    };
    eventTypes.forEach((eventType) => source.addEventListener(eventType, listener));
    source.onerror = () => {
      setError('SSE connection interrupted. The task may still be running.');
      source.close();
    };
  }

  function handleEvent(event: RunEvent) {
    // 所有事件先进统一 timeline；completed 事件额外携带最终 Markdown report。
    setEvents((current) => [...current, event]);
    setStatus(event.type);
    if (event.type === 'completed' && typeof event.payload.report_markdown === 'string') {
      setReport(event.payload.report_markdown);
    }
    if (event.type === 'failed') {
      setError(String(event.payload.error ?? event.message));
    }
  }

  const fixedEvents = events.filter((event) => event.type.includes('workflow') || event.type === 'route');
  const researchEvents = events.filter((event) => event.type.includes('research'));

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Japan Retail AI Portfolio</p>
          <h1>日本小売经营分析 Agent</h1>
          <p className="lead">
            固定经营图用于可验证 KPI，自主 Agent 用于市场、竞品和社内资料调查。SSE 实时显示执行路径，报告由后端持久化。
          </p>
        </div>
        <div className="status-card">
          <span>Status</span>
          <strong>{status}</strong>
          <small>{taskId || 'no task yet'}</small>
        </div>
      </section>

      <section className="control-panel">
        <label>
          Question
          <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
        </label>
        <label>
          Mode
          <select value={mode} onChange={(event) => setMode(event.target.value as RunMode)}>
            <option value="auto">auto</option>
            <option value="data">data</option>
            <option value="research">research</option>
            <option value="hybrid">hybrid</option>
          </select>
        </label>
        <button onClick={startTask} disabled={status === 'creating' || status === 'started'}>
          Run Analysis
        </button>
        {error ? <p className="error">{error}</p> : null}
      </section>

      <section className="grid">
        <Panel title="固定图 / 问数工作流" events={fixedEvents} empty="No fixed workflow events yet." />
        <Panel title="自主 Research Agent" events={researchEvents} empty="No research events yet." />
      </section>

      <section className="timeline">
        <h2>Execution Timeline</h2>
        {events.map((event) => (
          <article key={`${event.timestamp}-${event.type}`} className="event-row">
            <span>{event.type}</span>
            <div>
              <strong>{event.message}</strong>
              <pre>{JSON.stringify(event.payload, null, 2)}</pre>
            </div>
          </article>
        ))}
      </section>

      <section className="report">
        <h2>Markdown Report</h2>
        <pre>{report || 'Report will appear after completion.'}</pre>
      </section>
    </main>
  );
}

function Panel({ title, events, empty }: { title: string; events: RunEvent[]; empty: string }) {
  // Panel 是教学用 UI，把后端事件按职责拆开看。
  return (
    <section className="panel">
      <h2>{title}</h2>
      {events.length === 0 ? <p>{empty}</p> : null}
      {events.map((event) => (
        <div className="pill" key={`${event.timestamp}-${event.type}`}>
          <span>{event.type}</span>
          <strong>{event.message}</strong>
        </div>
      ))}
    </section>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
