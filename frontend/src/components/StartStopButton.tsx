import { useState } from 'react';
import { startContainer, stopContainer } from '../services/api';

interface Props {
  containerId: string;
  isRunning: boolean;
  onComplete?: () => void;
}

export default function StartStopButton({ containerId, isRunning, onComplete }: Props) {
  const [isLoading, setIsLoading] = useState(false);
  const actionLabel = isRunning ? 'Stop' : 'Start';

  const handleClick = async () => {
    if (isLoading) return;

    if (isRunning) {
      const ok = window.confirm('Are you sure you want to stop this container?');
      if (!ok) return;
    }

    setIsLoading(true);
    try {
      if (isRunning) {
        await stopContainer(containerId);
      } else {
        await startContainer(containerId);
      }

      // Notify parent to refetch
      onComplete?.();
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Action failed', err);
      // For now, alert the user; a toast system can replace this later
      alert((err as any)?.message || 'Action failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      className={`btn ${isRunning ? 'btn-ghost' : 'btn-primary'}`}
      onClick={handleClick}
      disabled={isLoading}
      aria-busy={isLoading}
      aria-disabled={isLoading}
      title={`${actionLabel} container`}
    >
      {isLoading ? (
        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" strokeOpacity="0.25" />
          <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
        </svg>
      ) : null}
      <span>{actionLabel}</span>
    </button>
  );
}
