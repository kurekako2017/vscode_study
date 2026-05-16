import { notFound } from 'next/navigation'

type Props = { params: { id: string } }

async function fetchNewsItem(id: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_PATH || ''}/api/news/${id}`, {
    next: { revalidate: 60 },
  })
  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch news item')
  return res.json()
}

export default async function NewsDetailPage({ params }: Props) {
  const item = await fetchNewsItem(params.id)
  if (!item) return notFound()

  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-3xl font-bold mb-4">{item.title}</h1>
      <div className="text-sm text-gray-500 mb-6">{item.date}</div>
      <div className="prose">
        <p>{item.content}</p>
      </div>
    </div>
  )
}
