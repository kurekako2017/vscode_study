import type { ReactNode } from "react";

interface StatusBannerProps {
  tone: "success" | "error" | "info" | "warning";
  children: ReactNode;
}

/**
 * StatusBanner 统一成功、错误和说明提示的视觉与可访问性。
 *
 * 设计理由：
 * - 页面状态反馈很多，如果每页都各写一套，视觉和读屏语义会很快分叉。
 */
export function StatusBanner({ tone, children }: StatusBannerProps) {
  const className = tone === "error"
    ? "error"
    : tone === "success"
      ? "success-banner"
      : tone === "warning"
        ? "info-banner"
        : "info-banner";

  return (
    <div className={className} role={tone === "error" ? "alert" : "status"}>
      {children}
    </div>
  );
}
