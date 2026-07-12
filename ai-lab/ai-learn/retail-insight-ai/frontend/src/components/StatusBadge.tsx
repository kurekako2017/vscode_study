interface StatusBadgeProps {
  value: string;
}

/**
 * StatusBadge 统一状态标签，避免不同页面自己拼接不同 class。
 */
export function StatusBadge({ value }: StatusBadgeProps) {
  return <span className={`pill status-pill status-pill-${value}`}>{value}</span>;
}
