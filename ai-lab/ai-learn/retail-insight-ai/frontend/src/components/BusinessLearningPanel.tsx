interface LearningCase {
  id: string;
  group: "标准业务 Case" | "异常与维护测试 Case";
  purpose: string;
  input: string;
  expected: string;
  steps?: string[];
  prerequisite?: string;
  operation?: string;
  expectedApi?: string;
  pageOutput?: string;
  businessCheck?: string;
}

interface LearningFlow {
  title: string;
  api: string;
  frontend: string[];
  backend: string[];
  note?: string;
}

interface LearningJourney {
  previous: string;
  current: string;
  completion: string;
  next: string;
  recommendedCase: string;
  transferredObjects: string;
  connection: string;
}

interface SopStep {
  title: string;
  purpose: string;
  prerequisite: string;
  input: string;
  action: string;
  api: string;
  backendResult: string;
  pageResult: string;
  technology: string;
  failureCheck: string;
  next: string;
}

interface OperationGuide {
  title: string;
  prerequisite: string;
  action: string;
  expected: string;
  input?: string;
  settings?: string;
  verification?: string;
  troubleshooting?: string;
  next?: string;
}

interface BusinessLearningPanelProps {
  pageName: string;
  purpose: string;
  scenario: string;
  prerequisites: string;
  relationship: string;
  journey: LearningJourney;
  cases: LearningCase[];
  flows: LearningFlow[];
  standardSop?: { title: string; scenarioFile: string; summary: string; steps: SopStep[] };
  operationGuides?: OperationGuide[];
  operationGuideTitle?: string;
}

/**
 * BusinessLearningPanel 是四个业务页面的可执行 SOP 与测试学习入口。
 *
 * 谁调用它：DocumentsPage、RagPage、TasksPage、ApprovalPage 传入已按真实 API 核对的数据。
 * 它调用谁：不调用 API；只把页面已有的业务顺序、前置条件和测试 Case 组织为学习内容。
 * 输入与输出：输入是页面专属的 SOP、Case、调用链和衔接信息；输出是纯展示的操作说明。
 * 为什么这样设计：让初学者先照标准路径完成业务，再单独执行异常和维护 Case，避免把 Archive 误认为主流程步骤。
 * 日本现场面试怎么讲：前端把业务操作说明与实际接口合同并列展示，但不复制业务数据或承担流程编排责任。
 */
export function BusinessLearningPanel({
  pageName,
  purpose,
  scenario,
  prerequisites,
  relationship,
  journey,
  cases,
  flows,
  standardSop,
  operationGuides,
  operationGuideTitle,
}: BusinessLearningPanelProps) {
  const standardCases = cases.filter((item) => item.group === "标准业务 Case");
  const exceptionCases = cases.filter((item) => item.group === "异常与维护测试 Case");

  return (
    <section className="business-learning" aria-label={`${pageName} 业务测试与源码学习`}>
      <details>
        <summary>业务测试与源码学习</summary>
        <div className="business-learning-content">
          <p><strong>业务目的：</strong>{purpose}</p>
          <p><strong>企业业务场景：</strong>{scenario}</p>
          <p><strong>前置条件：</strong>{prerequisites}</p>
          <p><strong>与其他页面的关系：</strong>{relationship}</p>

          <section className="learning-journey" aria-label={`${pageName} 上一步下一步`}>
            <h3>页面衔接</h3>
            <p><strong>上一步：</strong>{journey.previous}</p>
            <p><strong>当前步骤：</strong>{journey.current}</p>
            <p><strong>完成条件：</strong>{journey.completion}</p>
            <p><strong>下一步：</strong>{journey.next}</p>
            <p><strong>推荐 Case：</strong>{journey.recommendedCase}</p>
            <p><strong>需要传递的对象：</strong>{journey.transferredObjects}</p>
            <p><strong>当前连接方式：</strong>{journey.connection}</p>
          </section>

          {standardSop && (
            <section className="standard-sop" aria-label="标准业务 SOP">
              <h3>{standardSop.title}</h3>
              <p><strong>Scenario01 示例文件：</strong><code>{standardSop.scenarioFile}</code></p>
              <p>{standardSop.summary}</p>
              <ol className="sop-step-list">
                {standardSop.steps.map((step) => (
                  <li key={step.title} className="sop-step-card">
                    <h4>{step.title}</h4>
                    <p><strong>业务目的：</strong>{step.purpose}</p>
                    <p><strong>前置条件：</strong>{step.prerequisite}</p>
                    <p><strong>输入：</strong>{step.input}</p>
                    <p><strong>页面操作：</strong>{step.action}</p>
                    <p><strong>API：</strong><code>{step.api}</code></p>
                    <p><strong>预期 Backend 结果：</strong>{step.backendResult}</p>
                    <p><strong>预期页面输出：</strong>{step.pageResult}</p>
                    <p><strong>技术点：</strong>{step.technology}</p>
                    <p><strong>失败时检查：</strong>{step.failureCheck}</p>
                    <p><strong>下一步：</strong>{step.next}</p>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {operationGuides && (
            <section className="operation-guides" aria-label={`${pageName} 操作说明`}>
              <h3>{operationGuideTitle ?? "页面操作说明"}</h3>
              {operationGuides.map((guide) => (
                <article key={guide.title} className="learning-flow">
                  <h4>{guide.title}</h4>
                  <p><strong>前置条件：</strong>{guide.prerequisite}</p>
                  {guide.input && <p><strong>输入：</strong>{guide.input}</p>}
                  {guide.settings && <p><strong>设置：</strong>{guide.settings}</p>}
                  <p><strong>操作：</strong>{guide.action}</p>
                  <p><strong>预期：</strong>{guide.expected}</p>
                  {guide.verification && <p><strong>验证点：</strong>{guide.verification}</p>}
                  {guide.troubleshooting && <p><strong>insufficient_context 检查：</strong>{guide.troubleshooting}</p>}
                  {guide.next && <p><strong>下一步：</strong>{guide.next}</p>}
                </article>
              ))}
            </section>
          )}

          <h3>标准业务 Case</h3>
          <CaseGrid cases={standardCases} />
          <h3>异常与维护测试 Case</h3>
          <CaseGrid cases={exceptionCases} />

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

function CaseGrid({ cases }: { cases: LearningCase[] }) {
  return (
    <div className="learning-case-grid">
      {cases.map((item) => (
        <article key={item.id} className="learning-case">
          <strong>{item.id}</strong>
          <p><b>业务目的：</b>{item.purpose}</p>
          {item.prerequisite && <p><b>前置条件：</b>{item.prerequisite}</p>}
          <p><b>输入／操作：</b>{item.input}</p>
          {item.operation && <p><b>操作：</b>{item.operation}</p>}
          {item.expectedApi && <p><b>预期 API：</b><code>{item.expectedApi}</code></p>}
          {item.pageOutput && <p><b>预期页面输出：</b>{item.pageOutput}</p>}
          {item.businessCheck && <p><b>业务确认点：</b>{item.businessCheck}</p>}
          {item.steps && <ol>{item.steps.map((step) => <li key={step}>{step}</li>)}</ol>}
          <p><b>预期结果与确认点：</b>{item.expected}</p>
        </article>
      ))}
    </div>
  );
}
