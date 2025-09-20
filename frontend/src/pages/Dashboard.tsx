import { useEffect, useMemo, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Coins, CheckCircle2, Plus, Sparkles } from 'lucide-react'
import { api } from '../services/api'
import { useSfx } from '../sfx/useSfx'

type Task = { id: string; title: string; durationMin?: number; scheduledAt?: string; completed?: boolean }

export default function Dashboard(){
  const [tasks,setTasks] = useState<Task[]>([])
  const [title,setTitle] = useState('')
  const [duration,setDuration] = useState(25)
  const [xp,setXp] = useState(0)
  const [level,setLevel] = useState(1)
  const [streak,setStreak] = useState(0)
  const coinRef = useRef<HTMLDivElement>(null)
  const { playKaching } = useSfx()

  useEffect(()=>{
    api.users.getXp('demo').then(x=>{ setXp(x.xp); setLevel(x.level); setStreak(x.streak||0) }).catch(()=>{})
  },[])

  const xpPercent = useMemo(()=> Math.min(100, (xp % 100)), [xp])

  function addTask(){
    if(!title.trim()) return
    const temp: Task = { id: Math.random().toString(36).slice(2), title, durationMin: duration }
    setTasks(prev=>[temp,...prev])
    setTitle('')
    // Integration point to tycoon framework: rank priority and difficulty
    api.tycoon.rankTask(temp)
  }

  async function completeTask(id: string){
    setTasks(prev=> prev.map(t=> t.id===id?{...t, completed:true}:t))
    // Ka-ching sound & coin pop
    playKaching()
    coinRef.current?.classList.add('coin-pop')
    setTimeout(()=> coinRef.current?.classList.remove('coin-pop'), 800)

    // Backend: complete task & gain XP
    try{
      const payload = await api.tasks.complete(id)
      setXp(payload.xp)
      setLevel(payload.level)
      setStreak(payload.streak||0)
    }catch{}
  }

  async function autofit(){
    // Backend: schedule tasks into user calendar based on availability
    api.tasks.autofit('demo')
  }

  return (
    <div className="grid grid-3">
      <section className="panel" style={{gridColumn:'span 2'}}>
        <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
          <h2 className="title-arcade" style={{color:'var(--cornell-red)'}}>QUESTS</h2>
          <button className="btn btn-primary" onClick={autofit}><Sparkles size={16}/> Auto-fit</button>
        </div>
        <div style={{display:'flex',gap:8,marginBottom:12}}>
          <input className="field" style={{flex:1}} value={title} onChange={e=>setTitle(e.target.value)} placeholder="Add an arcade task"/>
          <input className="field" type="number" value={duration} onChange={e=>setDuration(parseInt(e.target.value||'0'))} style={{width:120}}/>
          <button className="btn btn-primary" onClick={addTask}><Plus size={16}/> Add</button>
        </div>
        <div>
          <AnimatePresence>
            {tasks.map(t=> (
              <motion.div key={t.id} initial={{opacity:0, y:6}} animate={{opacity:1, y:0}} exit={{opacity:0, y:-6}} className="panel" style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:8}}>
                <div>
                  <div className="heading" style={{fontSize:22}}>{t.title}</div>
                  <div className="mono-dim">{t.durationMin||25} min</div>
                </div>
                <button className="btn btn-coin" onClick={()=>completeTask(t.id)} disabled={t.completed}>
                  <CheckCircle2 size={16}/> {t.completed?'Done':'Complete'}
                </button>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </section>
      <aside className="panel" style={{position:'relative'}}>
        <h2 className="title-arcade" style={{color:'var(--cornell-red)',marginBottom:12}}>PROGRESS</h2>
        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
          <Coins color="var(--coin)"/>
          <div ref={coinRef} style={{width:10,height:10,borderRadius:999,background:'var(--coin)'}}/>
        </div>
        <div className="mono-dim" style={{marginBottom:6}}>Level {level} • Streak {streak}🔥</div>
        <div style={{height:14, background:'#1f2430', borderRadius:6, border:'2px solid #2a2f3a', overflow:'hidden'}}>
          <div className="xp-fill" style={{height:'100%', width: xpPercent+'%', background:'linear-gradient(90deg, var(--cornell-red), var(--coin))'}}/>
        </div>
        <div className="mono-dim" style={{marginTop:6}}>{xp} XP</div>
        <div className="mono-dim" style={{marginTop:12,fontSize:12}}>
          Calls: tasks → POST /tasks, POST /tasks/:id/complete; users → GET /users/:id/xp
        </div>
      </aside>
    </div>
  )
}


