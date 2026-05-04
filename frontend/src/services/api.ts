/**
 * API Connection Service
 * Centralized service for communicating with the backend
 * Uses Axios for HTTP requests with comprehensive error handling
 */

import axios from 'axios';
import type { AxiosInstance, AxiosError } from 'axios';
import type {
    HealthResponse,
    ApiError,
    ApiErrorType,
    ContainerListResponse,
    ContainerStatusResponse,
    ContainerActionResponse,
} from '../types/api';

// Use relative URLs so requests are routed through the frontend's origin
// In Docker, nginx proxies /docker, /health, and root routes to the backend
// In local dev, update CORS_ORIGINS in backend .env if making direct backend calls
const API_BASE_URL = '';

/**
 * Axios instance configured with base URL and default headers
 */
const axiosInstance: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Map HTTP status codes and error types to determine if a request is retryable
 */
function isErrorRetryable(status?: number, errorType?: ApiErrorType): boolean {
    if (!status) return false;
    // Retryable: network timeouts (0), 408 (timeout), 429 (rate limit), 5xx (server errors)
    if (status === 0 || status === 408 || status === 429 || status >= 500) return true;
    if (errorType === 'network') return true;
    return false;
}

/**
 * Determine the error type from HTTP status code and error response
 */
function getErrorType(status?: number): ApiErrorType {
    if (!status) return 'network';
    if (status === 400 || status === 422) return 'validation';
    if (status === 404) return 'not_found';
    if (status === 409) return 'conflict';
    if (status >= 500) return 'server';
    return 'unknown';
}

/**
 * Comprehensive error handler that transforms Axios errors into ApiError objects
 */
function handleApiError(error: unknown): ApiError {
    if (axios.isAxiosError(error)) {
        const axError = error as AxiosError<{ detail?: string }>;
        const status = axError.response?.status;
        const errorType = getErrorType(status);
        const message =
            axError.response?.data?.detail ||
            axError.message ||
            'An unknown error occurred';

        return {
            message,
            status,
            errorType,
            retryable: isErrorRetryable(status, errorType),
        };
    }

    if (error instanceof Error) {
        return {
            message: error.message,
            errorType: 'unknown',
            retryable: false,
        };
    }

    return {
        message: 'An unknown error occurred',
        errorType: 'unknown',
        retryable: false,
    };
}

// ============================================================================
// HEALTH ENDPOINTS
// ============================================================================

/**
 * Fetches the health status from the backend
 * @returns HealthResponse object containing server status, uptime, and timestamp
 * @throws ApiError if the request fails or response is malformed
 */
export async function fetchHealth(): Promise<HealthResponse> {
    try {
        const { data } = await axiosInstance.get<HealthResponse>('/health');

        // Validate response structure
        if (!data.status || data.uptime_seconds === undefined || !data.timestamp) {
            throw new Error('Invalid health response format');
        }

        return data;
    } catch (error) {
        throw handleApiError(error);
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

// ============================================================================
// DOCKER CONTAINER ENDPOINTS
// ============================================================================

/**
 * List all Docker containers (running and stopped)
 * @returns ContainerListResponse with list of all containers and their count
 * @throws ApiError if the request fails
 */
export async function listContainers(): Promise<ContainerListResponse> {
    try {
        const { data } = await axiosInstance.get<{
            success: boolean;
            data: ContainerListResponse;
        }>('/docker/containers');

        return data.data;
    } catch (error) {
        throw handleApiError(error);
    }
}

/**
 * Get detailed status of a specific Docker container
 * @param containerId - The ID or name of the container
 * @returns ContainerStatusResponse with detailed container status
 * @throws ApiError if the request fails or container not found
 */
export async function getContainerStatus(
    containerId: string
): Promise<ContainerStatusResponse> {
    try {
        const { data } = await axiosInstance.get<{
            success: boolean;
            data: ContainerStatusResponse;
        }>(`/docker/containers/${containerId}`);

        return data.data;
    } catch (error) {
        throw handleApiError(error);
    }
}

/**
 * Start a Docker container
 * @param containerId - The ID or name of the container to start
 * @returns ContainerActionResponse with operation result
 * @throws ApiError if the request fails, container not found, or already running
 */
export async function startContainer(containerId: string): Promise<ContainerActionResponse> {
    try {
        const { data } = await axiosInstance.post<{
            success: boolean;
            data: ContainerActionResponse;
        }>(`/docker/containers/${containerId}/start`);

        return data.data;
    } catch (error) {
        throw handleApiError(error);
    }
}

/**
 * Stop a Docker container
 * @param containerId - The ID or name of the container to stop
 * @returns ContainerActionResponse with operation result
 * @throws ApiError if the request fails, container not found, or already stopped
 */
export async function stopContainer(containerId: string): Promise<ContainerActionResponse> {
    try {
        const { data } = await axiosInstance.post<{
            success: boolean;
            data: ContainerActionResponse;
        }>(`/docker/containers/${containerId}/stop`);

        return data.data;
    } catch (error) {
        throw handleApiError(error);
    }
}
