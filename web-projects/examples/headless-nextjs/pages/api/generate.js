export default async function handler(req, res){
  if (req.method !== 'POST') return res.status(405).end()
  const { prompt } = req.body || {}
  if (!prompt) return res.status(400).json({ error: 'missing prompt' })

  const WP_API_URL = process.env.WP_API_URL || ''
  if (!WP_API_URL) return res.status(500).json({ error: 'WP_API_URL not configured' })

  try{
    const endpoint = `${WP_API_URL.replace(/\/$/, '')}/wp-json/ai-codex/v1/generate`
    // 这里示例使用服务器端代理以避免前端直接暴露凭证
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    })
    const data = await resp.json()
    return res.status(200).json(data)
  }catch(err){
    return res.status(500).json({ error: err.message })
  }
}
