import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'

export default function MainLayout() {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>Message Fraud Detection System — For educational purposes only.</p>
        <p className="footer-disclaimer">
          Messages may contain personal or financial information. Use at your own discretion.
        </p>
      </footer>
    </div>
  )
}
