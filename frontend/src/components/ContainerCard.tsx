import type { ContainerInfo } from '../types/api';
import StatusBadge from './StatusBadge';
import StartStopButton from './StartStopButton';

interface Props {
  container: ContainerInfo;
  onActionComplete?: () => void;
}

export default function ContainerCard({ container, onActionComplete }: Props) {
  const shortId = container.id.slice(0, 12);

  return (
    <div className="card p-4" style={{ backgroundColor: 'var(--surface)' }}>
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <div className="text-lg font-semibold" style={{ color: 'var(--text)' }}>{container.name}</div>
            <div className="text-xs text-(--muted)">{shortId}</div>
          </div>
          <div className="text-sm text-(--muted) mt-2">{container.image}</div>
        </div>

        <div className="flex flex-col items-end gap-3">
          <StatusBadge status={container.status} />
          <StartStopButton containerId={container.id} isRunning={container.status === 'running'} onComplete={onActionComplete} />
        </div>
      </div>
    </div>
  );
}
