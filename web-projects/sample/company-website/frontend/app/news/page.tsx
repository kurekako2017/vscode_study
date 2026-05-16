import Link from 'next/link'

async function fetchNews() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_PATH || ''}/api/news`, {
    // ISR: revalidate every 60 seconds
    next: { revalidate: 60 },
  })
  if (!res.ok) throw new Error('Failed to fetch news')
  return res.json()
}

export default async function NewsPage() {
  const items = await fetchNews()

  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-4xl font-bold mb-6">新闻动态</h1>

      <div className="grid md:grid-cols-3 gap-6">
        {items.map((it: any) => (
          <article key={it.id} className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="p-6">
              <div className="text-sm text-gray-500 mb-2">{it.date}</div>
              <h3 className="text-xl font-semibold mb-2">{it.title}</h3>
              <p className="text-gray-600 mb-4">{it.summary}</p>
              <Link href={`/news/${it.id}`} className="text-primary-600">阅读全文</Link>
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}
