/**
 * API Connection Service
 * Centralized service for communicating with the backend
 * Handles connection management and HTTP requests with error handling
 */

import type { HealthResponse, ApiError } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetches the health status from the backend
 * @returns HealthResponse object containing server status, uptime, and timestamp
 * @throws ApiError if the request fails or response is malformed
 */
export async function fetchHealth(): Promise<HealthResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Validate response structure
        if (!data.status || data.uptime_seconds === undefined || !data.timestamp) {
            throw new Error('Invalid health response format');
        }

        return data as HealthResponse;
    } catch (error) {
        const apiError: ApiError = {
            message:
                error instanceof Error ? error.message : 'Failed to connect to backend',
            status: error instanceof TypeError ? 0 : 500, // 0 = network error
        };
        throw apiError;
    }
}

/**
 * Check if the backend is accessible
 * @returns true if backend is healthy, false otherwise
 */
export async function isBackendHealthy(): Promise<boolean> {
    try {
        await fetchHealth();
        return true;
    } catch {
        return false;
    }
}
