import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Dashboard from './pages/Dashboard'
import Analyzer from './pages/Analyzer'
import History from './pages/History'
import ModelPerformance from './pages/ModelPerformance'
import About from './pages/About'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="analyzer" element={<Analyzer />} />
        <Route path="history" element={<History />} />
        <Route path="model-performance" element={<ModelPerformance />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  )
}

export default App
