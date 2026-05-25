import { NextResponse } from 'next/server'
import news from '@/data/news.json'
import { getSupabaseClient } from '@/lib/supabaseClient'

type Params = { params: { id: string } }

export async function GET(request: Request, { params }: Params) {
  const supabase = getSupabaseClient()
  if (supabase) {
    try {
      const { data, error } = await supabase.from('news').select('*').eq('id', params.id).limit(1).single()
      if (!error && data) {
        const item = {
          id: data.id,
          title: data.title,
          summary: data.summary,
          content: data.content,
          date: data.published_at ? new Date(data.published_at).toISOString().split('T')[0] : null,
        }
        return NextResponse.json(item)
      }
    } catch (err) {
      console.error('Supabase news item fetch failed:', err)
      // fallthrough to local JSON
    }
  }

  // Fallback to local JSON (ids in local JSON are numbers)
  const idNum = Number(params.id)
  const item = news.find((n) => n.id === idNum)
  if (!item) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(item)
}
