import { NextResponse } from 'next/server'
import news from '@/data/news.json'
import { getSupabaseClient } from '@/lib/supabaseClient'

export async function GET() {
  const supabase = getSupabaseClient()
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('news')
        .select('id, title, summary, published_at, is_published')
        .eq('is_published', true)
        .order('published_at', { ascending: false })
      if (error) throw error
      // Normalize field names for frontend
      const items = (data || []).map((it: any) => ({
        id: it.id,
        title: it.title,
        summary: it.summary,
        date: it.published_at ? new Date(it.published_at).toISOString().split('T')[0] : null,
      }))
      return NextResponse.json(items)
    } catch (err) {
      console.error('Supabase news fetch failed:', err)
      // fallthrough to local JSON
    }
  }

  // Fallback: return local JSON
  return NextResponse.json(news)
}
