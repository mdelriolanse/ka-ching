import { Routes, Route, Link } from 'react-router-dom'
import { useEffect, useState, useRef, useMemo } from 'react'
import { Gamepad2, CalendarDays, ClipboardList, Trophy } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Media from './pages/Media'
import CalendarView from './pages/CalendarView'

import axios from 'axios'

export default function App() {
  const [user, setUser] = useState<any>({
    xp: 0,
    level: 1,
    streak: 0,
    rebirths: 0,
    upgrades: {},
    tasks: []
  })

  // Load user from backend on initial mount
  useEffect(() => {
    async function loadUser() {
      try {
        const res = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/users/demo/load`)
        setUser(res.data)
      } catch (err) {
        console.error("Failed to load user:", err)
      }
    }
    loadUser()
  }, [])

  // Periodically save user data
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        await axios.post(`${import.meta.env.VITE_BACKEND_URL}/users/demo/save`, user)
      } catch (err) {
        console.error("Failed to save user:", err)
      }
    }, 60000)
    return () => clearInterval(interval)
  }, [user])
  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column'}}>
      <nav className="nav">
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <span className="title-arcade brand" style={{color:'var(--cornell-red)'}}>KA-CHING!</span>
          <span className="mono-dim blink">insert coin</span>
        </div>
        <div>
          <Link to="/" style={{marginRight:16}}><Gamepad2 size={18}/> Dashboard</Link>
          <Link to="/calendar" style={{marginRight:16}}><CalendarDays size={18}/> Calendar</Link>
          <Link to="/media"><Trophy size={18}/> Learn</Link>
        </div>
      </nav>
      <div style={{padding:16, flex:1}}>
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/calendar" element={<CalendarView/>} />
          <Route path="/media" element={<Media/>} />
        </Routes>
      </div>
      <footer style={{padding:12,textAlign:'center',color:'var(--text-dim)'}}>
        BigRed/Hacks 2025 - made by Maxwell, Mateo, Claire, and Abhay
      </footer>
    </div>
  )
}


