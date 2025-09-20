import { Routes, Route, Link } from 'react-router-dom'
import { Gamepad2, CalendarDays, ClipboardList, Trophy } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Media from './pages/Media'
import CalendarView from './pages/CalendarView'

export default function App(){
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
        Built for arcaders • Cornell palette • Neovim vibes
      </footer>
    </div>
  )
}


