import { useLearningStore } from './store'

function formatSourceList(files) {
  if (!files || files.length === 0) {
    return ['暂无对应源码文件']
  }

  return files
}

function formatTraceLabel(trace) {
  return `[${trace.type}] ${trace.message}`
}

function formatStateFlowLabel(trace) {
  if (trace.type === 'STATE') {
    return trace.message.replace(':', '：').replace('→', ' → ')
  }

  if (trace.type === 'RENDER') {
    return trace.message.replace('render', 'Render')
  }

  if (trace.type === 'EVENT') {
    return trace.message
  }

  if (trace.type === 'CALL') {
    return trace.message
  }

  return trace.message
}

export default function LearningPanel() {
  const snapshot = useLearningStore((currentState) => currentState)
  const stateFlowTraces = snapshot.traces.filter((trace) => ['EVENT', 'CALL', 'STATE', 'RENDER'].includes(trace.type)).slice(-5)
  const recentTraces = snapshot.traces.slice(-10)

  return (
    <details className="learning-panel" open>
      <summary>学习面板</summary>
      <div className="learning-panel-body">
        <section className="learning-block">
          <p className="learning-label">① 当前路由 <span className="sr-only">Current Route</span></p>
          <p className="learning-value">{snapshot.currentRouteLabel}</p>
        </section>

        <section className="learning-block">
          <p className="learning-label">② 当前页面 <span className="sr-only">Current Page</span></p>
          <p className="learning-value learning-current-page">{snapshot.currentPageName}</p>
          <p className="learning-muted">当前子组件：{snapshot.currentChildPage}</p>
          {snapshot.lastRenderReason ? <p className="learning-muted">为什么重新 Render：{snapshot.lastRenderReason}</p> : null}
        </section>

        <section className="learning-block">
          <p className="learning-label">③ 组件树 <span className="sr-only">Component Tree</span></p>
          <pre className="code learning-code">{snapshot.componentTree.join('\n')}</pre>
        </section>

        <section className="learning-block">
          <p className="learning-label">④ 使用的 Hook <span className="sr-only">Hooks Used</span></p>
          {snapshot.hooksUsed.length === 0 ? (
            <p className="learning-value">暂无</p>
          ) : (
            <ul className="learning-list">
              {snapshot.hooksUsed.map((hook) => (
                <li key={hook}>{hook}</li>
              ))}
            </ul>
          )}
        </section>

        <section className="learning-block">
          <p className="learning-label">⑤ Props 传递关系 <span className="sr-only">Props Flow</span></p>
          {snapshot.propsFlow.length === 0 ? (
            <p className="learning-value">暂无显式 Props</p>
          ) : (
            <ul className="learning-list">
              {snapshot.propsFlow.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          )}
        </section>

        <section className="learning-block">
          <p className="learning-label">⑥ 最近事件 <span className="sr-only">Last Event</span></p>
          <p className="learning-value">{snapshot.lastEvent || '暂无'}</p>
        </section>

        <section className="learning-block">
          <p className="learning-label">⑦ 最近状态变化 <span className="sr-only">Last State Change</span></p>
          <p className="learning-value">{snapshot.lastStateChange || '暂无'}</p>
        </section>

        <section className="learning-block">
          <p className="learning-label">⑧ State 变化流程 <span className="sr-only">State Flow</span></p>
          <ol className="learning-list learning-flow-list">
            {stateFlowTraces.length === 0 ? (
              <li>等待交互</li>
            ) : (
              stateFlowTraces.map((trace, index) => (
                <li key={trace.id}>
                  {String(index + 1).padStart(2, '0')} {formatStateFlowLabel(trace)}
                </li>
              ))
            )}
          </ol>
        </section>

        <section className="learning-block">
          <p className="learning-label">⑨ Hook 监视器 <span className="sr-only">Hook Monitor</span></p>
          <ul className="learning-list">
            {snapshot.hookSnapshots.length === 0 ? (
              <li>暂无 Hook 快照</li>
            ) : (
              snapshot.hookSnapshots.map((hook) => (
                <li key={hook.key}>
                  <strong>{hook.componentName}</strong>
                  <br />
                  {hook.hookName}
                  <br />
                  {hook.summary}
                </li>
              ))
            )}
          </ul>
        </section>

        <details className="learning-fold" open>
          <summary>⑩ 对应源码文件 <span className="sr-only">Source Files</span></summary>
          <ul className="learning-list">
            {formatSourceList(snapshot.sourceFiles).map((file) => (
              <li key={file}>{file}</li>
            ))}
          </ul>
        </details>

        <section className="learning-block">
          <p className="learning-label">⑪ 对应测试文件 <span className="sr-only">Test File</span></p>
          <p className="learning-value">{snapshot.testFile ?? '暂无对应测试文件'}</p>
        </section>

        <details className="learning-fold">
          <summary>⑫ 最近调用记录 <span className="sr-only">Recent Trace</span></summary>
          <ol className="learning-list learning-trace-list">
            {recentTraces.map((trace) => (
              <li key={trace.id}>
                [{String(trace.id).padStart(3, '0')}] {formatTraceLabel(trace)}
              </li>
            ))}
          </ol>
        </details>

        <p className="learning-label learning-strict-label">
          ⑬ StrictMode（开发模式） <span className="sr-only">StrictMode</span>
        </p>
        <p className="learning-note">Development 下 Render / Effect 可能因 React.StrictMode 执行两次。</p>
      </div>
    </details>
  )
}
