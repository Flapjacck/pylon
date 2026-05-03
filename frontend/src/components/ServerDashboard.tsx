import { useEffect, useMemo } from 'react';
import { usePolling } from '../hooks/usePolling';
import { listContainers } from '../services/api';
import type { ContainerListResponse } from '../types/api';
import ContainerCard from './ContainerCard';

export default function ServerDashboard() {
  const { data, error, isLoading, refetch } = usePolling<ContainerListResponse>(() => listContainers(), {
    interval: 10000,
  });

  // Track last updated time when `data` changes
  const lastUpdated = useMemo(() => (data ? new Date() : null), [data]);

  useEffect(() => {
    // noop: placeholder if we want side-effects on update
  }, [data]);

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold" style={{ color: 'var(--text)' }}>Server Dashboard</h2>
        <div className="flex items-center gap-2">
          <button className="btn btn-ghost" onClick={() => refetch()} disabled={isLoading}>
            Refresh
          </button>
          <div className="text-sm text-(--muted)">
            {lastUpdated ? `Updated ${lastUpdated.toLocaleTimeString()}` : 'No data yet'}
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 text-sm" style={{ color: 'var(--danger)' }}>
          Error: {(error as any).message}
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {data && data.containers.length > 0 ? (
          data.containers.map((c) => (
            <ContainerCard key={c.id} container={c} onActionComplete={() => refetch()} />
          ))
        ) : (
          <div className="text-(--muted)">{isLoading ? 'Loading containers...' : 'No containers found.'}</div>
        )}
      </div>
    </div>
  );
}
