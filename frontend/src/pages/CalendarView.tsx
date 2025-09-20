import { useEffect, useRef, useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { api } from '../services/api'

export default function CalendarView(){
  const [events,setEvents] = useState<any[]>([])
  const [ical,setIcal] = useState('')
  const fileRef = useRef<HTMLInputElement>(null)

  useEffect(()=>{ (async()=>{
    try{ const data = await api.calendar.fetch('demo'); setEvents(data) }catch{}
  })() },[])

  async function uploadIcal(){
    if(!fileRef.current?.files?.[0]) return
    const file = fileRef.current.files[0]
    await api.calendar.upload('demo', file)
  }

  async function syncFromLink(){
    // Optionally handled server-side; placeholder to signal feature
    if(!ical.trim()) return
    // api.calendar.importFromLink('demo', ical)
  }

  return (
    <div className="grid grid-2">
      <div className="panel">
        <h2 className="title-arcade" style={{color:'var(--cornell-red)'}}>CALENDAR</h2>
        <FullCalendar
          plugins={[dayGridPlugin,timeGridPlugin,interactionPlugin]}
          initialView="timeGridWeek"
          height={600}
          events={events}
        />
      </div>
      <div className="panel">
        <h3 className="heading" style={{fontSize:22}}>Import iCal</h3>
        <input ref={fileRef} type="file" accept=".ics" className="field" style={{marginTop:8, marginBottom:8}}/>
        <div style={{display:'flex',gap:8}}>
          <button className="btn btn-primary" onClick={uploadIcal}>Upload .ics</button>
        </div>
        <hr style={{borderColor:'#22262f',margin:'16px 0'}}/>
        <h3 className="heading" style={{fontSize:22}}>Or paste iCal URL</h3>
        <input value={ical} onChange={e=>setIcal(e.target.value)} placeholder="https://.../calendar.ics" className="field"/>
        <div style={{marginTop:8}}>
          <button className="btn" onClick={syncFromLink}>Sync from URL</button>
        </div>
        <div className="mono-dim" style={{marginTop:12,fontSize:12}}>Backend: POST /upload, GET /events/:user_id</div>
      </div>
    </div>
  )
}


