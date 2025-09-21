import { useEffect, useRef, useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { api } from '../services/api'

export default function CalendarView() {
  const [events, setEvents] = useState<any[]>([])
  const [ical, setIcal] = useState('')
  const fileRef = useRef<HTMLInputElement>(null)
  const userId = 'demo'

  // Fetch events on mount
  useEffect(() => {
    (async () => {
      try {
        const data = await api.calendar.fetch(userId)
        const formatted = data.map((ev: any) => ({
          id: ev.id || ev.uid || Math.random().toString(),
          title: ev.title || ev.summary || 'Untitled Event',
          start: new Date(ev.start),  // ensure Date object
          end: new Date(ev.end),
        }))
        setEvents(formatted)
      } catch (err) {
        console.error('Error fetching events', err)
      }
    })()
  }, [])

  // Upload iCal file
  async function uploadIcal() {
    if (!fileRef.current?.files?.[0]) return alert('No file selected')
    const file = fileRef.current.files[0]

    try {
      const result = await api.calendar.upload(userId, file)
      alert(result.message + ` (${result.events_count} events)`)

      // Refetch events after upload
      const data = await api.calendar.fetch(userId)
      const formatted = data.map((ev: any) => ({
        id: ev.id || ev.uid || Math.random().toString(),
        title: ev.title || ev.summary || 'Untitled Event',
        start: new Date(ev.start),
        end: new Date(ev.end),
      }))
      setEvents(formatted)
    } catch (err: any) {
      console.error(err)
      alert('Upload failed: ' + (err.response?.data?.error || err.message))
    }
  }

  // Optional: sync from iCal URL
  async function syncFromLink() {
    if (!ical.trim()) return
    // Placeholder: await api.calendar.importFromLink(userId, ical)
  }

  return (
    <div className="grid grid-2">
      <div className="panel">
        <h2 className="title-arcade" style={{ color: 'var(--cornell-red)' }}>
          CALENDAR
        </h2>
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView="timeGridWeek"
          height={600}
          events={events}
        />
      </div>

      <div className="panel">
        <h3 className="heading" style={{ fontSize: 22 }}>Import iCal</h3>
        <input
          ref={fileRef}
          type="file"
          accept=".ics"
          className="field"
          style={{ marginTop: 8, marginBottom: 8 }}
        />
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-primary" onClick={uploadIcal}>
            Upload .ics
          </button>
        </div>

        <hr style={{ borderColor: '#22262f', margin: '16px 0' }} />

        <h3 className="heading" style={{ fontSize: 22 }}>Or paste iCal URL</h3>
        <input
          value={ical}
          onChange={(e) => setIcal(e.target.value)}
          placeholder="https://.../calendar.ics"
          className="field"
        />
        <div style={{ marginTop: 8 }}>
          <button className="btn" onClick={syncFromLink}>
            Sync from URL
          </button>
        </div>

        <div className="mono-dim" style={{ marginTop: 12, fontSize: 12 }}>
          Backend: POST /upload, GET /events/:user_id
        </div>
      </div>
    </div>
  )
}
