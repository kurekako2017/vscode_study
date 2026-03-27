type Props = {
  eyebrow: string
  title: string
  subtitle: string
  message: string
  meta?: string
}

export function PageHeader({ eyebrow, title, subtitle, message, meta }: Props) {
  return (
    <div className="pageHeader">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="subtitle">{subtitle}</p>
      </div>
      <div className="status">
        <span>{message}</span>
        {meta ? <span>{meta}</span> : null}
      </div>
    </div>
  )
}
