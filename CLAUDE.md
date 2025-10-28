# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack real-time playing card detection application for Hi-Lo blackjack counting practice:
- **Backend**: FastAPI + YOLOv8 (Ultralytics) + OpenCV
- **Frontend**: React 19 + TanStack Start/Router/Query + shadcn/ui
- **Real-time**: Server-Sent Events for live count updates
- **Current Status**: Uses placeholder YOLOv8 model (`yolov8n.pt`) - not trained on playing cards

## Development Commands

### Primary Method: Docker
```bash
# Start entire stack (from project root)
docker-compose up --build

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs

# Logs
docker logs card-detection-backend -f
docker logs card-detection-frontend -f
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows: venv\Scripts\activate | Unix: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev                # Development server (hot reload)
npm run build              # Production build
npm start                  # Start production server
```

**Node Version**: Requires 20.19.0+ (recommended 22.12.0+)

## Architecture Overview

### Backend Architecture (Singleton Pattern)

Entry point: `backend/main.py`

```
FastAPI App
├── Routers
│   └── detection.py           # All API endpoints (/api prefix)
└── Services (Singletons)
    ├── model_service.py       # YOLOv8 model lifecycle management
    └── counting_service.py    # Hi-Lo card counting state & logic
```

**Key Pattern**: Services use singleton pattern to maintain single instances across requests. This means:
- Model loaded once at first prediction
- Counting state shared across all requests (single-user design)
- State persists until server restart or explicit reset

**Model Service** (`backend/services/model_service.py`):
- Lazy loads YOLOv8 model on first `predict()` call
- Currently uses generic `yolov8n.pt` (placeholder)
- Returns list of detections with labels and confidence

**Counting Service** (`backend/services/counting_service.py`):
- Implements Hi-Lo strategy: Low (2-6) = +1, Neutral (7-9) = 0, High (10-A) = -1
- Tracks `running_count` and `detected_cards` set (prevents double-counting)
- Thread-safe with lock for concurrent requests

### Frontend Architecture (Domain-Based API)

Entry points:
- `frontend/app/client.tsx` - Client hydration
- `frontend/app/ssr.tsx` - Server-side rendering
- `frontend/app/routes/index.tsx` - Main card detection page

```
app/
├── api/                       # Domain-based organization
│   └── detection/
│       ├── detection.query.ts     # React Query queryOptions
│       └── detection.mutation.ts  # React Query mutationOptions
├── components/ui/             # shadcn/ui components
├── routes/                    # File-based routing
├── services/
│   └── apiClient.ts          # Axios instance
└── lib/utils.ts              # Utilities (cn, etc.)
```

**React Query Pattern** (see `.claude/patterns.md` for comprehensive guide):
- **No hooks abstraction**: Export `queryOptions()` directly, consume with `useSuspenseQuery(options)`
- **DTOs colocated**: Type definitions above API functions in same file
- **Pure API layer**: No toast notifications or UI logic in API functions
- **Component-level feedback**: Toast notifications in components using `onSuccess`/`onError`

Example:
```typescript
// In detection.query.ts
export const getDetectionStateOptions = () => queryOptions({
  queryKey: ['detection', 'state'],
  queryFn: getDetectionState,
})

// In component
const { data } = useSuspenseQuery(getDetectionStateOptions())
```

### Real-Time Communication Flow

1. Frontend captures webcam frame on canvas
2. `POST /api/detect` - Sends frame as multipart/form-data
3. Backend runs YOLOv8 inference
4. CountingService processes new cards with Hi-Lo logic
5. Response includes detected cards + current count
6. **SSE Stream** (`GET /api/stream`) continuously pushes state updates every 500ms
7. Frontend `EventSource` receives updates and invalidates React Query cache

## API Endpoints

All endpoints prefixed with `/api` (configured in `backend/main.py`).

**Detection & State:**
- `POST /api/detect` - Card detection (accepts: multipart image file)
- `POST /api/reset` - Reset running count and detected cards
- `GET /api/state` - Get current count state
- `GET /api/stream` - SSE endpoint for real-time state updates (event: `state-update`)

**Health:**
- `GET /` - Root health check
- `GET /health` - Explicit health check

## Important Technical Details

### Backend

**CORS Configuration** (`backend/main.py`):
- Default origins: `http://localhost:3000`, `http://localhost:5173`
- Override via `CORS_ORIGINS` environment variable

**YOLOv8 Model Path**:
- Configurable via `MODEL_PATH` env var (default: `yolov8n.pt`)
- Model must be in backend directory or provide absolute path
- To use custom trained model: Replace placeholder and update env var

**Hi-Lo Counting Logic** (`backend/services/counting_service.py:20-30`):
```python
CARD_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,  # Low cards
    '7': 0, '8': 0, '9': 0,                   # Neutral
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1  # High cards
}
```

### Frontend

**Environment Variables** (`.env` in frontend/):
- `VITE_API_URL` - Backend base URL (default: `http://localhost:8000`)

**Webcam Integration** (`frontend/app/routes/index.tsx:55-70`):
- Uses `navigator.mediaDevices.getUserMedia()`
- Video rendered to `<video>` element
- Frame captured via `<canvas>` element
- Canvas converted to Blob → FormData

**SSE Connection** (`frontend/app/routes/index.tsx:115-135`):
```typescript
const eventSource = new EventSource(`${apiUrl}/api/stream`)
eventSource.addEventListener('state-update', (event) => {
  const data = JSON.parse(event.data)
  queryClient.setQueryData(['detection', 'state'], data)
})
```

**shadcn/ui Components**:
- Installed: Badge, Button, Card, CardContent, CardDescription, CardHeader, CardTitle
- Add new components: Use shadcn CLI (components use Radix UI + Tailwind)

## Configuration Files

**TypeScript** (`frontend/tsconfig.json`):
- Path alias: `@/*` maps to `./app/*`
- Target: ES2020, strict mode enabled

**Tailwind CSS** (`frontend/app/styles/globals.css`):
- Uses Tailwind CSS v4 (imported via `@import "tailwindcss"``)
- Custom theme with CSS variables for colors
- Dark mode support via class strategy

**Docker** (`docker-compose.yml`):
- Network: `card-detection-network`
- Volumes mounted for hot reload in development
- Backend depends_on: none
- Frontend depends_on: backend

## Key Patterns & Conventions

### Backend
- **All endpoints async**: Use `async def` for route handlers
- **Pydantic models**: Request/response validation (see `backend/routers/detection.py`)
- **Error handling**: Raise `HTTPException` with appropriate status codes
- **Service layer**: Business logic in `services/`, routers stay thin

### Frontend
- **File-based routing**: Routes in `app/routes/` (TanStack Router)
- **Domain-based API**: Group queries/mutations by feature domain (detection, user, etc.)
- **Query keys**: Array format `['domain', 'resource', ...params]`
- **Invalidation**: Invalidate domain queries after mutations: `queryClient.invalidateQueries({ queryKey: ['detection'] })`
- **Component structure**: Use shadcn/ui for base components, compose in pages
- **Type safety**: Define DTOs for all API responses in query/mutation files

## Current Limitations & Production Roadmap

**Limitations:**
1. **Generic YOLO model**: `yolov8n.pt` is NOT trained on playing cards - detections are placeholder
2. **Single-user design**: Singleton services mean single shared state (one active session)
3. **No authentication**: All endpoints open
4. **No persistence**: State lost on server restart
5. **No tests**: Test suite not implemented

**To Deploy with Real Card Detection:**
1. Collect/label playing cards dataset (1000+ images with rank/suit labels)
2. Train YOLOv8 model using Ultralytics
3. Replace `yolov8n.pt` with trained model (e.g., `best.pt`)
4. Update `MODEL_PATH` environment variable
5. Test detection accuracy and adjust confidence thresholds

**Production Improvements** (from README.md):
- Multi-user support (Redis for state or per-session isolation)
- WebSocket alternative to SSE for bidirectional communication
- Authentication system
- Model optimization (TensorRT, ONNX export)
- Comprehensive test coverage

## File Locations Reference

**Backend:**
- Entry: `backend/main.py`
- API routes: `backend/routers/detection.py`
- Services: `backend/services/model_service.py`, `backend/services/counting_service.py`
- Dependencies: `backend/requirements.txt`

**Frontend:**
- Entry: `frontend/app/client.tsx`, `frontend/app/ssr.tsx`
- Main page: `frontend/app/routes/index.tsx`
- API layer: `frontend/app/api/detection/`
- HTTP client: `frontend/app/services/apiClient.ts`
- Dependencies: `frontend/package.json`

**Configuration:**
- Docker: `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`
- Environment: `.env.example` in both backend/ and frontend/
- React Query patterns: `.claude/patterns.md`
- Permissions: `.claude/settings.local.json`