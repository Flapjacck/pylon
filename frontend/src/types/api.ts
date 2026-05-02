/**
 * API Type Definitions
 * Defines TypeScript interfaces for all API responses from the backend
 */

/**
 * Server health status response from GET /health endpoint
 */
export interface HealthResponse {
    status: string;
    uptime_seconds: number;
    timestamp: string;
}

/**
 * Standard API error response
 */
export interface ApiError {
    message: string;
    status?: number;
}
