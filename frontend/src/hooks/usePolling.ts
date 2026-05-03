/**
 * usePolling Hook
 * Custom React hook that implements polling logic for auto-updating data
 * Auto-starts polling on mount with configurable interval, stops on error
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import type { ApiError } from '../types/api';

/**
 * Generic polling hook configuration
 */
interface UsePollingOptions {
    /** Polling interval in milliseconds (default: 5000ms) */
    interval?: number;
    /** Array of dependencies that trigger re-initialization */
    dependencies?: React.DependencyList;
    /** Whether to poll immediately on mount (default: true) */
    autoStart?: boolean;
}

/**
 * Polling hook return value
 */
interface UsePollingReturn<T> {
    /** Current data from successful polls */
    data: T | null;
    /** Error from failed poll, if any */
    error: ApiError | null;
    /** Whether a poll request is currently in flight */
    isLoading: boolean;
    /** Manually trigger a poll (useful for retry) */
    refetch: () => Promise<void>;
    /** Manually reset the state */
    reset: () => void;
}

/**
 * usePolling - Custom React hook for polling data
 *
 * @template T - Type of data being polled
 * @param fetchFn - Async function that fetches and returns data of type T
 * @param options - Configuration options for polling behavior
 * @returns Object containing data, error, isLoading, refetch, and reset
 *
 * @example
 * ```tsx
 * const { data: containers, error, isLoading } = usePolling(
 *   () => listContainers(),
 *   { interval: 5000 }
 * );
 * ```
 *
 * Behavior:
 * - Auto-starts polling immediately on mount
 * - Calls fetchFn every `interval` milliseconds
 * - Stops polling immediately when an error occurs
 * - Cleans up interval and abort signal on unmount
 * - Provides refetch() to manually retry after errors
 * - Returns stale data on error (doesn't clear it automatically)
 */
export function usePolling<T>(
    fetchFn: () => Promise<T>,
    options: UsePollingOptions = {}
): UsePollingReturn<T> {
    const {
        interval = 5000,
        dependencies = [],
        autoStart = true,
    } = options;

    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<ApiError | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Use refs to track if we're currently polling and abort controller
    const abortControllerRef = useRef<AbortController | null>(null);
    const intervalIdRef = useRef<ReturnType<typeof setInterval> | null>(null);
    const isPollingRef = useRef(false);
    const isLoadingRef = useRef(false);
    const fetchFnRef = useRef(fetchFn);

    // Keep the latest fetchFn in a ref so polling setup does not restart when callers pass inline functions
    useEffect(() => {
        fetchFnRef.current = fetchFn;
    }, [fetchFn]);

    /**
     * Execute a single poll request
     */
    const executePoll = useCallback(async () => {
        // Skip if already loading or polling has been stopped
        if (isLoadingRef.current || !isPollingRef.current) return;

        isLoadingRef.current = true;
        setIsLoading(true);

        try {
            const result = await fetchFnRef.current();
            setData(result);
            setError(null);
        } catch (err) {
            // Stop polling on error
            isPollingRef.current = false;
            const apiError = err as ApiError;
            setError(apiError);
        } finally {
            isLoadingRef.current = false;
            setIsLoading(false);
        }
    }, []);

    /**
     * Refetch manually (useful for retry after error)
     */
    const refetch = useCallback(async () => {
        isPollingRef.current = true;

        if (isLoadingRef.current) return;
        isLoadingRef.current = true;
        setIsLoading(true);

        try {
            const result = await fetchFnRef.current();
            setData(result);
            setError(null);
        } catch (err) {
            const apiError = err as ApiError;
            setError(apiError);
            // Stop polling if error occurred
            isPollingRef.current = false;
        } finally {
            isLoadingRef.current = false;
            setIsLoading(false);
        }
    }, [fetchFn]);

    /**
     * Reset the state
     */
    const reset = useCallback(() => {
        setData(null);
        setError(null);
        setIsLoading(false);
    }, []);

    /**
     * Setup polling interval on mount
     */
    useEffect(() => {
        // Start polling if autoStart is true
        if (autoStart) {
            isPollingRef.current = true;
            // Execute first poll immediately
            executePoll();

            // Setup interval for subsequent polls
            intervalIdRef.current = setInterval(executePoll, interval);
        }

        // Cleanup on unmount
        return () => {
            isPollingRef.current = false;
            if (intervalIdRef.current) {
                clearInterval(intervalIdRef.current);
            }
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
        // executePoll is stable (uses fetchFnRef) so it's safe to include here
    }, [interval, autoStart, executePoll]);

    // Re-initialize polling if dependencies change
    useEffect(() => {
        // If caller provided dependencies, trigger a refetch when they change
        if (dependencies && dependencies.length > 0) {
            refetch();
        }
        // We deliberately want to re-run when items in `dependencies` change
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, dependencies);

    return {
        data,
        error,
        isLoading,
        refetch,
        reset,
    };
}
