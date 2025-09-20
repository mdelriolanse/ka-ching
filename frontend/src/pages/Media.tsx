import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { PlayCircle, Podcast, Youtube } from 'lucide-react'

type MediaItem = { id: string; title: string; url: string; durationSec?: number; type: 'video' | 'podcast' }

export default function Media(){
  const [query,setQuery] = useState('learn algorithms')
  const [items,setItems] = useState<MediaItem[]>([])

  async function search(){
    try{
      const res = await api.media.search(query)
      setItems(res)
    }catch{}
  }

  useEffect(()=>{ search() },[])

  return (
    <div className="panel">
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 className="title-arcade" style={{color:'var(--cornell-red)'}}>LEARN</h2>
        <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search YouTube/Podcasts" className="field" style={{flex:1}}/>
        <button className="btn btn-primary" onClick={search}>Search</button>
      </div>
      <div className="grid grid-3">
        {items.map(m=> (
          <a key={m.id} href={m.url} target="_blank" className="panel" style={{textDecoration:'none',color:'var(--cornell-white)'}}>
            <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
              {m.type==='video' ? <Youtube color="#ff4e45"/> : <Podcast color="#ffb703"/>}
              <div className="heading" style={{fontSize:22}}>{m.title}</div>
            </div>
            <div className="mono-dim" style={{display:'flex',alignItems:'center',gap:6}}>
              <PlayCircle size={16}/> {Math.round((m.durationSec||0)/60)} min
            </div>
          </a>
        ))}
      </div>
      <div className="mono-dim" style={{marginTop:12,fontSize:12}}>AI/MCP: backend orchestrates Gemini → YouTube API and returns items.</div>
    </div>
  )
}


