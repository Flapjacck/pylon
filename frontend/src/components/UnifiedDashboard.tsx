import { useMemo } from 'react';
import { usePolling } from '../hooks/usePolling';
import { fetchHealth, listContainers } from '../services/api';
import type { HealthResponse, ContainerListResponse } from '../types/api';
import ContainerCard from './ContainerCard';

export default function UnifiedDashboard() {
  // Poll health status
  const { 
    data: healthData, 
    error: healthError, 
    isLoading: healthLoading, 
    refetch: refetchHealth 
  } = usePolling<HealthResponse>(() => fetchHealth(), { interval: 10000 });

  // Poll container list
  const { 
    data: containerData, 
    error: containerError, 
    isLoading: containerLoading, 
    refetch: refetchContainers 
  } = usePolling<ContainerListResponse>(() => listContainers(), { interval: 10000 });

  // Track last updated time
  const lastUpdated = useMemo(
    () => (healthData || containerData ? new Date() : null),
    [healthData, containerData]
  );

  const isLoading = healthLoading || containerLoading;
  const isConnected = healthData && !healthError;

  const statusColor = isLoading
    ? 'var(--warning)'
    : isConnected
    ? 'var(--success)'
    : 'var(--danger)';

  const handleRefresh = () => {
    refetchHealth();
    refetchContainers();
  };

  return (
    <div className="min-h-screen p-6" style={{ backgroundColor: 'var(--bg)' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'var(--text)' }}>
          System Dashboard
        </h1>
        <p className="text-sm" style={{ color: 'var(--muted)' }}>
          Monitor your backend health and container status in real-time
        </p>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <button 
            className="btn btn-primary" 
            onClick={handleRefresh} 
            disabled={isLoading}
            title="Refresh health and container status"
          >
            {isLoading ? 'Refreshing...' : 'Refresh'}
          </button>
          {lastUpdated && (
            <span className="text-sm" style={{ color: 'var(--muted)' }}>
              Updated {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      {/* Health Status Section */}
      <div 
        className="card mb-8 p-6" 
        style={{ 
          backgroundColor: 'var(--surface)',
          border: `2px solid ${statusColor}`,
          transition: 'border-color 0.3s'
        }}
      >
        <div className="flex items-center gap-4 mb-4">
          <span 
            className="w-4 h-4 rounded-full" 
            style={{ 
              backgroundColor: statusColor, 
              animation: isLoading ? 'pulse 1.5s infinite' : 'none'
            }} 
          />
          <h2 className="text-xl font-semibold" style={{ color: 'var(--text)' }}>
            Backend Connection
          </h2>
          <span className="text-lg font-medium" style={{ color: statusColor }}>
            {isLoading && '⏳ Checking...'}
            {isConnected && '✓ Connected'}
            {!isLoading && !isConnected && '✗ Disconnected'}
          </span>
        </div>

        {healthData && (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-(--muted)">Status</span>
              <div 
                className="mt-1 px-2 py-1 rounded text-xs font-mono"
                style={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
              >
                {healthData.status}
              </div>
            </div>
            <div>
              <span className="text-(--muted)">Uptime</span>
              <div 
                className="mt-1 px-2 py-1 rounded text-xs font-mono"
                style={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
              >
                {healthData.uptime_seconds.toFixed(1)}s
              </div>
            </div>
            <div>
              <span className="text-(--muted)">Last Check</span>
              <div 
                className="mt-1 px-2 py-1 rounded text-xs font-mono"
                style={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
              >
                {new Date(healthData.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        )}

        {healthError && !isLoading && (
          <div className="text-sm mt-4" style={{ color: 'var(--danger)' }}>
            ⚠️ Connection Error: {(healthError as any).message}
          </div>
        )}
      </div>

      {/* Containers Section */}
      <div>
        <h2 className="text-2xl font-semibold mb-4" style={{ color: 'var(--text)' }}>
          Containers
        </h2>

        {containerError && !containerLoading && (
          <div className="mb-4 text-sm" style={{ color: 'var(--danger)' }}>
            ⚠️ Error loading containers: {(containerError as any).message}
          </div>
        )}

        {containerData && containerData.containers.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {containerData.containers.map((container) => (
              <ContainerCard 
                key={container.id} 
                container={container} 
                onActionComplete={() => refetchContainers()} 
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-8" style={{ color: 'var(--muted)' }}>
            {containerLoading ? 'Loading containers...' : 'No containers found'}
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}
