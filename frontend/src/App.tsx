
import UnifiedDashboard from './components/UnifiedDashboard';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="p-4 border-b" style={{ borderColor: 'rgba(255,255,255,0.03)' }}>
        <nav className="flex items-center gap-4">
          <Link to="/" className="text-lg font-semibold" style={{ color: 'var(--text)' }}>Dashboard</Link>
        </nav>
      </div>

      <Routes>
        <Route path="/" element={<UnifiedDashboard />} />
        <Route path="/dashboard" element={<UnifiedDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
