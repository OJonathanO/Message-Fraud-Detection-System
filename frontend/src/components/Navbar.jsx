import { NavLink, Link } from 'react-router-dom'
import { Shield, Home, Search, History, BarChart3, Info } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" className="navbar-logo">
          <Shield className="navbar-icon" />
          <span className="navbar-title">Fraud Detection</span>
        </Link>
      </div>
      <div className="navbar-links">
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Home size={18} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/analyzer" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Search size={18} />
          <span>Analyzer</span>
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <History size={18} />
          <span>History</span>
        </NavLink>
        <NavLink to="/model-performance" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <BarChart3 size={18} />
          <span>Model</span>
        </NavLink>
        <NavLink to="/about" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Info size={18} />
          <span>About</span>
        </NavLink>
      </div>
    </nav>
  )
}
