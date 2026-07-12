interface LearningCase {
  id: string;
  purpose: string;
  input: string;
  expected: string;
}

interface LearningFlow {
  title: string;
  api: string;
  frontend: string[];
  backend: string[];
  note?: string;
}

interface BusinessLearningPanelProps {
  pageName: string;
  purpose: string;
  scenario: string;
  prerequisites: string;
  relationship: string;
  cases: LearningCase[];
  flows: LearningFlow[];
}

/**
 * BusinessLearningPanel 是四个业务页面共用的学习入口。
 *
 * 谁调用它：
 * - DocumentsPage、RagPage、TasksPage、ApprovalPage 在业务操作区之后传入真实 API 流程。
 *
 * 它做什么：
 * - 用可折叠区域把企业测试 Case、页面操作和已核对的前后端调用链放在同一处。
 * - 只展示说明，不发起请求、不修改任何页面状态，因此不会改变原有业务处理。
 *
 * 为什么这样设计：
 * - 学习内容集中复用，避免四个业务页面逐渐出现不同格式的说明。
 * - 面试时可以从页面操作直接说明 React 事件如何进入 FastAPI 的 Router、Service 与 Repository/Workflow。
 */
export function BusinessLearningPanel({
  pageName,
  purpose,
  scenario,
  prerequisites,
  relationship,
  cases,
  flows,
}: BusinessLearningPanelProps) {
  return (
    <section className="business-learning" aria-label={`${pageName} 业务测试与源码学习`}>
      <details>
        <summary>业务测试与源码学习</summary>
        <div className="business-learning-content">
          <p><strong>业务目的：</strong>{purpose}</p>
          <p><strong>企业业务场景：</strong>{scenario}</p>
          <p><strong>前置条件：</strong>{prerequisites}</p>
          <p><strong>与其他页面的关系：</strong>{relationship}</p>

          <h3>企业业务测试用例</h3>
          <div className="learning-case-grid">
            {cases.map((item) => (
              <article key={item.id} className="learning-case">
                <strong>{item.id}</strong>
                <p><b>业务目的：</b>{item.purpose}</p>
                <p><b>输入／操作：</b>{item.input}</p>
                <p><b>预期结果与确认点：</b>{item.expected}</p>
              </article>
            ))}
          </div>

          <h3>实际调用流程</h3>
          {flows.map((flow) => (
            <article key={flow.title} className="learning-flow">
              <h4>{flow.title}</h4>
              <p><strong>相关 API：</strong><code>{flow.api}</code></p>
              <p><strong>前端链：</strong>{flow.frontend.join(" → ")}</p>
              <p><strong>后端链：</strong>{flow.backend.join(" → ")}</p>
              {flow.note && <p><strong>说明：</strong>{flow.note}</p>}
            </article>
          ))}
        </div>
      </details>
    </section>
  );
}
