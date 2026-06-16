import React, {useState} from 'react'

export default function App(){
  const [q, setQ] = useState('')
  const [res, setRes] = useState(null)

  async function ask(){
    const r = await fetch('/api/question', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({question: q})})
    const j = await r.json()
    setRes(j)
  }

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h2>AI Accountant — Demo</h2>
      <textarea value={q} onChange={e=>setQ(e.target.value)} rows={4} style={{width:'100%'}} />
      <div style={{marginTop:8}}>
        <button onClick={ask}>Ask</button>
      </div>
      {res && (
        <pre style={{whiteSpace:'pre-wrap', marginTop:12}}>{JSON.stringify(res, null, 2)}</pre>
      )}
    </div>
  )
}
