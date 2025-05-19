import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import './App.css'

// Import pages
import Home from './pages/Home'
import Patients from './pages/Patients'
import PatientDetail from './pages/PatientDetail'
import Scheduling from './pages/Scheduling'
import Appointments from './pages/Appointments'

function App() {
  const [isNavOpen, setIsNavOpen] = useState(false)

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">
          <h1>Healthcare Scheduling</h1>
        </div>
        <button 
          className="nav-toggle" 
          onClick={() => setIsNavOpen(!isNavOpen)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>
        <nav className={`main-nav ${isNavOpen ? 'open' : ''}`}>
          <ul>
            <li><Link to="/" onClick={() => setIsNavOpen(false)}>Home</Link></li>
            <li><Link to="/patients" onClick={() => setIsNavOpen(false)}>Patients</Link></li>
            <li><Link to="/scheduling" onClick={() => setIsNavOpen(false)}>Scheduling</Link></li>
            <li><Link to="/appointments" onClick={() => setIsNavOpen(false)}>Appointments</Link></li>
          </ul>
        </nav>
      </header>

      <main className="app-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/patients/:id" element={<PatientDetail />} />
          <Route path="/scheduling" element={<Scheduling />} />
          <Route path="/appointments" element={<Appointments />} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Healthcare Scheduling App</p>
      </footer>
    </div>
  )
}

export default App