import type { ContainerStatus } from '../types/api';

interface Props {
  status: ContainerStatus;
}

export default function StatusBadge({ status }: Props) {
  const map = {
    running: { color: 'var(--success)', label: 'Running' },
    restarting: { color: 'var(--warning)', label: 'Restarting' },
    exited: { color: 'var(--danger)', label: 'Stopped' },
    paused: { color: 'var(--accent2)', label: 'Paused' },
    created: { color: 'var(--muted)', label: 'Created' },
  } as const;

  const cfg = map[status] ?? { color: 'var(--muted)', label: status };

  return (
    <div className="flex items-center gap-2 text-sm">
      <span
        className="status-dot"
        style={{ backgroundColor: cfg.color }}
        aria-hidden
      />
      <span style={{ color: 'var(--text)' }}>{cfg.label}</span>
    </div>
  );
}
