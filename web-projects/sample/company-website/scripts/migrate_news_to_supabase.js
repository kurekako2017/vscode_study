/**
 * 简单迁移脚本：把 frontend/data/news.json 的条目导入 Supabase 的 `news` 表
 *
 * 使用方法：
 *   node migrate_news_to_supabase.js
 * 需要环境变量：SUPABASE_URL 和 SUPABASE_SERVICE_ROLE
 */

const fs = require('fs')
const path = require('path')
const { createClient } = require('@supabase/supabase-js')

async function main() {
  const url = process.env.SUPABASE_URL
  const key = process.env.SUPABASE_SERVICE_ROLE
  if (!url || !key) {
    console.error('Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE in environment')
    process.exit(1)
  }

  const supabase = createClient(url, key)

  const dataPath = path.join(__dirname, '..', 'frontend', 'data', 'news.json')
  const raw = fs.readFileSync(dataPath, 'utf-8')
  const items = JSON.parse(raw)

  for (const it of items) {
    const slug = (it.title || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
    const payload = {
      title: it.title,
      slug: slug,
      summary: it.summary || null,
      content: it.content || it.summary || '',
      category: 'general',
      is_published: true,
      published_at: it.date ? new Date(it.date).toISOString() : new Date().toISOString(),
    }

    console.log('Upserting', payload.title)
    const { data, error } = await supabase.from('news').upsert(payload, { onConflict: 'slug' }).select()
    if (error) {
      console.error('Upsert failed for', it.title, error)
    } else {
      console.log('OK:', data && data[0] && data[0].id)
    }
  }

  console.log('Migration completed')
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
