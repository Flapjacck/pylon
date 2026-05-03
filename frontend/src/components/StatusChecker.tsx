/**
 * StatusChecker Component
 * Displays the backend connection status and health information
 * Auto-polls the health endpoint every 5 seconds
 */

import { fetchHealth } from '../services/api';
import type { HealthResponse } from '../types/api';
import { usePolling } from '../hooks/usePolling';

export function StatusChecker() {
  const { data, error, isLoading, refetch } = usePolling<HealthResponse>(() => fetchHealth(), {
    interval: 10000,
  });

  const status = isLoading ? 'loading' : data ? 'connected' : error ? 'disconnected' : 'loading';

  const borderColor =
    status === 'connected'
      ? 'var(--success)'
      : status === 'loading'
      ? 'var(--warning)'
      : 'var(--danger)';

  return (
    <div className="card m-4 p-4" style={{ backgroundColor: 'var(--surface)', border: `2px solid ${borderColor}` }}>
      <div className="flex items-center gap-3 mb-3">
        <span className="status-dot" style={{ backgroundColor: borderColor, animation: isLoading ? 'pulse 1.5s infinite' : 'none' }} />
        <strong style={{ color: 'var(--text)' }}>Backend Connection:</strong>
        <span style={{ color: borderColor }}>
          {status === 'connected' && ' Connected'}
          {status === 'disconnected' && ' Disconnected'}
          {status === 'loading' && ' Checking...'}
        </span>
        <div className="ml-auto">
          <button className="btn btn-ghost" onClick={() => refetch()} disabled={isLoading}>Check</button>
        </div>
      </div>

      {data && (
        <div className="text-sm" style={{ color: 'var(--muted)' }}>
          <div>
            Status: <code style={{ background: 'rgba(255,255,255,0.02)', padding: '2px 6px', borderRadius: 4 }}>{data.status}</code>
          </div>
          <div>Uptime: <code style={{ background: 'rgba(255,255,255,0.02)', padding: '2px 6px', borderRadius: 4 }}>{data.uptime_seconds.toFixed(1)}s</code></div>
          <div>Last Check: <code style={{ background: 'rgba(255,255,255,0.02)', padding: '2px 6px', borderRadius: 4 }}>{new Date(data.timestamp).toLocaleTimeString()}</code></div>
        </div>
      )}

      {error && (
        <div className="text-sm mt-3" style={{ color: 'var(--danger)' }}>
          ⚠️ {(error as any).message}
        </div>
      )}

      <style>{`@keyframes pulse { 0%,100% { opacity: 1 } 50% { opacity: 0.5 } }`}</style>
    </div>
  );
}
