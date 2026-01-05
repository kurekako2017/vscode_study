import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })

export const metadata: Metadata = {
  title: {
    default: '公司名称 - 专业的企业服务',
    template: '%s | 公司名称',
  },
  description: '我们提供专业的企业服务解决方案',
  keywords: ['企业服务', '解决方案', '专业团队'],
  authors: [{ name: '公司名称' }],
  openGraph: {
    type: 'website',
    locale: 'zh_CN',
    url: 'https://yourcompany.com',
    siteName: '公司名称',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: '公司名称',
      },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className={inter.variable}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
