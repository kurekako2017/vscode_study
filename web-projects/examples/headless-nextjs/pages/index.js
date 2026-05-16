import { useState } from 'react'

export default function Home() {
  const [prompt, setPrompt] = useState('写一段关于 Docker Compose 的中文简介，约 150 字')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleGenerate(e){
    e.preventDefault()
    setLoading(true)
    setResult('')
    try{
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      })
      const data = await res.json()
      setResult(data.result || JSON.stringify(data))
    }catch(err){
      setResult('Error: ' + err.message)
    }finally{ setLoading(false) }
  }

  return (
    <main style={{padding:20,fontFamily:'Arial'}}>
      <h1>Headless Next.js 示例 — 调用 ai-codex-agent</h1>
      <form onSubmit={handleGenerate}>
        <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={6} cols={80} />
        <br/>
        <button type="submit" disabled={loading}>{loading? '生成中...':'生成草稿'}</button>
      </form>
      <section style={{marginTop:20}}>
        <h2>生成结果</h2>
        <pre style={{whiteSpace:'pre-wrap', background:'#f6f8fa', padding:12}}>{result}</pre>
      </section>
    </main>
  )
}
