interface PageHeaderProps {
  title: string;
  description: string;
  eyebrow?: string;
}

/**
 * PageHeader 统一页面标题区，让每个页面都先说明“这页做什么”。
 *
 * 谁会调用它：
 * - Dashboard、Tasks、Documents、RAG、Approval 页面。
 *
 * 为什么先抽这一层：
 * - 这一块在多个页面重复出现，而且会直接影响学习者第一次进入页面时的理解速度。
 */
export function PageHeader({ title, description, eyebrow = "LOCAL MVP WORKSPACE" }: PageHeaderProps) {
  return (
    <header className="page-header">
      <p className="page-eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p className="page-description">{description}</p>
    </header>
  );
}
