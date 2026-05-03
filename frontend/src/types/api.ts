/**
 * API Type Definitions
 * Defines TypeScript interfaces for all API responses from the backend
 */

// ============================================================================
// HEALTH ENDPOINT TYPES
// ============================================================================

/**
 * Server health status response from GET /health endpoint
 */
export interface HealthResponse {
    status: string;
    uptime_seconds: number;
    timestamp: string;
}

// ============================================================================
// DOCKER CONTAINER TYPES
// ============================================================================

/**
 * Union type for all possible Docker container states
 */
export type ContainerStatus = 'running' | 'exited' | 'paused' | 'created' | 'restarting';

/**
 * Basic container information returned when listing containers
 */
export interface ContainerInfo {
    id: string;
    name: string;
    status: ContainerStatus;
    image: string;
}

/**
 * Detailed container state information
 */
export interface ContainerState {
    running: boolean;
    paused: boolean;
    restarting: boolean;
    pid: number | null;
    exit_code: number | null;
    started_at: string | null;
    finished_at: string | null;
}

/**
 * Detailed status information for a specific container (GET /docker/containers/{id})
 */
export interface ContainerStatusResponse {
    id: string;
    name: string;
    status: ContainerStatus;
    image: string;
    running: boolean;
    paused: boolean;
    restarting: boolean;
    pid: number | null;
    exit_code: number | null;
    started_at: string | null;
    finished_at: string | null;
}

/**
 * Response for listing all containers (GET /docker/containers)
 */
export interface ContainerListResponse {
    containers: ContainerInfo[];
    count: number;
}

/**
 * Response for container action endpoints (POST /docker/containers/{id}/start|stop)
 */
export interface ContainerActionResponse {
    message: string;
    container_id: string;
}

// ============================================================================
// ERROR HANDLING TYPES
// ============================================================================

/**
 * Type of error that occurred
 */
export type ApiErrorType = 'network' | 'validation' | 'not_found' | 'conflict' | 'server' | 'unknown';

/**
 * Comprehensive API error with retry information
 */
export interface ApiError {
    message: string;
    status?: number;
    errorType?: ApiErrorType;
    retryable?: boolean;
}
