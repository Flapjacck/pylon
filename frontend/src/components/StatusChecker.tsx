/**
 * StatusChecker Component
 * Displays the backend connection status and health information
 * Auto-polls the health endpoint every 5 seconds
 */

import { useEffect, useState } from 'react';
import { fetchHealth } from '../services/api';
import type { HealthResponse, ApiError } from '../types/api';

export function StatusChecker() {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'loading'>(
    'loading'
  );
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let pollingInterval: ReturnType<typeof setInterval>;

    const checkHealth = async () => {
      try {
        setStatus('loading');
        const data = await fetchHealth();
        setHealthData(data);
        setStatus('connected');
        setError(null);
      } catch (err) {
        const apiError = err as ApiError;
        setStatus('disconnected');
        setError(apiError.message);
        setHealthData(null);
      }
    };

    // Initial check
    checkHealth();

    // Poll every 5 seconds
    pollingInterval = setInterval(checkHealth, 5000);

    return () => clearInterval(pollingInterval);
  }, []);

  return (
    <div
      style={{
        padding: '16px',
        margin: '16px',
        borderRadius: '8px',
        backgroundColor: '#f5f5f5',
        border: `2px solid ${
          status === 'connected' ? '#10b981' : status === 'loading' ? '#f59e0b' : '#ef4444'
        }`,
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <div style={{ marginBottom: '12px' }}>
        <span
          style={{
            display: 'inline-block',
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor:
              status === 'connected' ? '#10b981' : status === 'loading' ? '#f59e0b' : '#ef4444',
            marginRight: '8px',
            animation: status === 'loading' ? 'pulse 1.5s infinite' : 'none',
          }}
        />
        <strong>Backend Connection: </strong>
        {status === 'connected' && <span style={{ color: '#10b981' }}>Connected</span>}
        {status === 'disconnected' && <span style={{ color: '#ef4444' }}>Disconnected</span>}
        {status === 'loading' && <span style={{ color: '#f59e0b' }}>Checking...</span>}
      </div>

      {healthData && (
        <div style={{ fontSize: '14px', color: '#333' }}>
          <div>Status: <code style={{ backgroundColor: '#e5e7eb', padding: '2px 4px' }}>{healthData.status}</code></div>
          <div>Uptime: <code style={{ backgroundColor: '#e5e7eb', padding: '2px 4px' }}>{healthData.uptime_seconds.toFixed(1)}s</code></div>
          <div>Last Check: <code style={{ backgroundColor: '#e5e7eb', padding: '2px 4px' }}>{new Date(healthData.timestamp).toLocaleTimeString()}</code></div>
        </div>
      )}

      {error && (
        <div style={{ fontSize: '14px', color: '#ef4444', marginTop: '8px' }}>
          ⚠️ {error}
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}
