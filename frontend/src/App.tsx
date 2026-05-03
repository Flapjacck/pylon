
import { StatusChecker } from './components/StatusChecker';
import ServerDashboard from './components/ServerDashboard';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="p-4 border-b" style={{ borderColor: 'rgba(255,255,255,0.03)' }}>
        <nav className="flex items-center gap-4">
          <Link to="/" className="text-lg font-semibold" style={{ color: 'var(--text)' }}>Home</Link>
          <Link to="/dashboard" className="text-sm text-(--muted)">Dashboard</Link>
        </nav>
      </div>

      <Routes>
        <Route path="/" element={<StatusChecker />} />
        <Route path="/dashboard" element={<ServerDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
