// Centralized API client. Adjust BASE_URLs to your backend services.

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000' // Flask mongoapi for calendar
const CORE_URL = import.meta.env.VITE_CORE_URL || 'http://localhost:8000' // Core gamification REST (tasks/xp)
const MCP_URL = import.meta.env.VITE_MCP_URL || 'http://localhost:7000' // AI orchestrator endpoints

async function http<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if(!res.ok) throw new Error(await res.text())
  return res.json() as Promise<T>
}

import { api } from '../services/api'

// Upload calendar
async function handleUpload(file: File, userId: string) {
  const result = await api.calendar.upload(userId, file)
  console.log(result.message, result.events_count)
}

// Fetch events
async function fetchEvents(userId: string) {
  const events = await api.calendar.fetch(userId)
  console.log(events)
}

export const api = {
  tasks: {
    create: (title: string, durationMin?: number) =>
      http<{ id: string }>(`${CORE_URL}/tasks`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ title, durationMin }) }),
    complete: (id: string) =>
      http<{ xp:number, level:number, streak?:number }>(`${CORE_URL}/tasks/${id}/complete`, { method:'POST' }),
    autofit: (userId: string) =>
      http<{ scheduled: number }>(`${CORE_URL}/tasks/autofit?userId=${encodeURIComponent(userId)}`)
  },
  users: {
    getXp: (id: string) => http<{ xp:number, level:number, streak?:number }>(`${CORE_URL}/users/${id}/xp`)
  },
  calendar: {
    upload: async (userId: string, file: File) => {
      const form = new FormData()
      form.append('ical', file)
      form.append('user_id', userId)
      return http<{ message:string, events_count:number }>(`${BACKEND_URL}/upload`, { method:'POST', body: form })
    },
    fetch: (userId: string) => http<any[]>(`${BACKEND_URL}/events/${userId}`)
  },
  media: {
    search: (query: string) => http<{ id:string; title:string; url:string; durationSec?:number; type:'video'|'podcast' }[]>(`${MCP_URL}/media/search?q=${encodeURIComponent(query)}`)
  },
  tycoon: {
    // Hook for ranking/levels if provided by tycoon module backend
    rankTask: (task: { id:string; title:string; durationMin?:number }) => http(`${CORE_URL}/tycoon/rank`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(task) })
  }
}




