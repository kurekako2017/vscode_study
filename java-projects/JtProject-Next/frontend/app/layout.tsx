import type { Metadata } from 'next'
import './globals.css'

// Metadata 是 Next.js App Router 提供的页面元数据类型。
// 在 layout.tsx 中导出 metadata 后，Next 会自动生成 <title> 和 description。
export const metadata: Metadata = {
  title: 'JtProject Next',
  description: 'Spring Boot + Next.js + TypeScript learning project'
}

// RootLayout 是 App Router 的根布局。
// app/page.tsx、以后新增的 app/admin/page.tsx 等页面都会被包在 children 里。
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
