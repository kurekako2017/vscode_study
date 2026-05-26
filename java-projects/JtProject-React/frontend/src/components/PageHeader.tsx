type Props = {
  eyebrow: string
  title: string
  subtitle: string
  message: string
  meta?: string
}

// 复用的页面标题区，用于统一展示当前页面的主题和状态信息。
export function PageHeader({ eyebrow, title, subtitle, message, meta }: Props) {
// 文件说明：
// 页面头部组件，统一展示标题、副标题、提示信息等元信息，便于页面一致性。
// 学习点：复用小组件提升应用一致性与可维护性。
// 对应 JSP：index.jsp / adminHome.jsp 中的标题与状态展示区域
  return (
    <div className="pageHeader">
      <div>
        {/* 小标题/分类（例如 'Products' / 'Admin Dashboard'） */}
        <p className="eyebrow">{eyebrow}</p>
        {/* 页面主标题 */}
        <h1>{title}</h1>
        {/* 页面副标题或说明文字 */}
        <p className="subtitle">{subtitle}</p>
      </div>
      <div className="status">
        {/* 全局提示信息（如操作成功/失败） */}
        <span>{message}</span>
        {/* 可选的元信息，例如当前登录用户名 */}
        {meta ? <span>{meta}</span> : null}
      </div>
    </div>
  )
}
