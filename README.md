# Pylon

Terraria server supervisor produced with FastAPI in the coding language Python and React in the other coding language TypeScript.

## Prerequisites

- **Docker** and **Docker Compose** (latest stable version)
- **Python** 3.10 or higher
- **Node.js** 18+ and package manager

## Development Setup

### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   **Windows (PowerShell):**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies using uv/hatchling:

   ```bash
   pip install -e .
   ```

5. (Optional) Install development dependencies for testing:

   ```bash
   pip install -e ".[dev]"
   ```

### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies using pnpm:

   ```bash
   pnpm install
   ```

3. Available scripts:
   - **Development server:** `pnpm dev` (runs on `http://localhost:5173`)
   - **Production build:** `pnpm build`

## Docker Startup

Start both services using Docker Compose:

```bash
docker-compose up --build
```

To run in detached mode (background):

```bash
docker-compose up -d --build
```

### Service URLs

| Service | URL |
|---------|-----|
| Backend | `http://localhost:8000` |
| Frontend | `http://localhost:5173` |

Both services include health checks configured in `docker-compose.yml`. The frontend depends on the backend being healthy before starting.
