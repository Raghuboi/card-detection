# Real-Time Playing Card Detection System

A full-stack web application for real-time playing card detection with Hi-Lo counting, built with modern technologies and production-ready patterns.

## Architecture

```
┌─────────────────────────────────────────────┐
│  React 19 Frontend (TanStack Stack)        │
│  - Webcam capture with MediaDevices API     │
│  - Real-time video preview                  │
│  - Live card count display                  │
│  - Beautiful Radix UI components            │
└──────────────────┬──────────────────────────┘
                   │ Server-Sent Events (SSE)
┌──────────────────┴──────────────────────────┐
│  Python FastAPI Backend                     │
│  - YOLOv8 inference endpoint                │
│  - Real-time frame processing               │
│  - Hi-Lo card counting logic                │
│  - SSE for live state updates               │
└──────────────────┬──────────────────────────┘
                   │
              ┌────┴────┐
              │ YOLOv8  │
              │ Model   │
              └─────────┘
```

## Tech Stack

### Frontend
- **React 19** - Latest React with concurrent features
- **TanStack Start** - Full-stack React framework with SSR
- **TanStack Router** - Type-safe file-based routing
- **TanStack Query** - Powerful async state management
- **Tailwind CSS v4** - Modern utility-first CSS
- **Radix UI (shadcn/ui)** - Accessible component primitives
- **Sonner** - Beautiful toast notifications
- **Axios** - HTTP client with interceptors

### Backend
- **FastAPI** - Modern Python web framework
- **YOLOv8 (Ultralytics)** - State-of-the-art object detection
- **OpenCV** - Computer vision and image processing
- **Uvicorn** - Lightning-fast ASGI server
- **Server-Sent Events** - Real-time unidirectional updates

### DevOps
- **Docker** - Containerization with multi-stage builds
- **Docker Compose** - Multi-container orchestration

## Features

- **Live Webcam Feed** - Capture video directly from your camera
- **Real-Time Detection** - Detect playing cards with YOLOv8
- **Hi-Lo Counting** - Automatic card counting with proven strategy
  - Low cards (2-6): +1
  - Neutral (7-9): 0
  - High cards (10-A): -1
- **Server-Sent Events** - Live count updates without polling
- **Beautiful UI** - Modern design with Radix UI components
- **Production-Ready** - Docker deployment, error handling, type safety

## Project Structure

```
card-detection/
├── frontend/                 # TanStack Start application
│   ├── app/
│   │   ├── api/             # API layer (domain-based)
│   │   │   └── detection/
│   │   │       ├── detection.query.ts
│   │   │       └── detection.mutation.ts
│   │   ├── components/
│   │   │   └── ui/          # shadcn/ui components
│   │   ├── routes/          # File-based routes
│   │   │   ├── __root.tsx
│   │   │   └── index.tsx
│   │   ├── services/        # API client
│   │   ├── lib/             # Utilities
│   │   └── styles/          # Global styles
│   ├── Dockerfile
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── routers/
│   │   └── detection.py     # Detection endpoints
│   ├── services/
│   │   ├── model_service.py # YOLO model singleton
│   │   └── counting_service.py # Hi-Lo counting logic
│   ├── main.py              # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── .claude/                  # Claude Code patterns
│   └── patterns.md          # React Query patterns
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites

- **Node.js** >= 22.12.0 (for frontend)
- **Python** >= 3.11 (for backend)
- **Docker & Docker Compose** (recommended)

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   cd card-detection
   ```

2. **Create environment files**
   ```bash
   # Backend
   cp backend/.env.example backend/.env

   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Access at** http://localhost:3000

## API Endpoints

### Detection Endpoints

- **POST /api/detect** - Detect cards in uploaded image
  ```json
  Request: multipart/form-data with image file
  Response: {
    "cards": [...],
    "count": 2,
    "total_cards_detected": 15,
    "timestamp": "2025-10-27T..."
  }
  ```

- **GET /api/stream** - SSE endpoint for real-time updates
  ```
  Stream: text/event-stream
  Events: { "type": "state_update", "running_count": 2, ... }
  ```

- **POST /api/reset** - Reset counting state
  ```json
  Response: {
    "message": "Count reset successfully",
    "running_count": 0
  }
  ```

- **GET /api/state** - Get current counting state
  ```json
  Response: {
    "running_count": 2,
    "total_cards_detected": 15
  }
  ```

## Model Training

### Current Setup

The application currently uses a generic **YOLOv8n** model as a placeholder. For production card detection:

1. **Collect Dataset**
   - Capture images of playing cards from various angles
   - Label cards with rank and suit (e.g., "Ace_Spades", "10_Hearts")
   - Recommended: 1000+ images with augmentations

2. **Train Custom Model**
   ```python
   from ultralytics import YOLO

   # Load base model
   model = YOLO('yolov8n.pt')

   # Train on your dataset
   model.train(
       data='cards.yaml',
       epochs=100,
       imgsz=640,
       batch=16
   )
   ```

3. **Replace Model**
   - Place trained model in `backend/` directory
   - Update `MODEL_PATH` in `.env` to your model filename

### Recommended Datasets

- [Roboflow Playing Cards Dataset](https://universe.roboflow.com/augmented-startups/playing-cards-ow27d)
- Create your own using [Roboflow](https://roboflow.com/)

## Development Patterns

### React Query Patterns

This project follows strict React Query patterns (see `.claude/patterns.md`):

- **No hooks abstraction** - Use `queryOptions` directly
- **DTOs colocated** - Type definitions above functions
- **Component-level toasts** - API layer stays pure
- **Domain-based organization** - Group by feature

Example:
```typescript
// api/detection/detection.query.ts
type GetStateResponseDTO = { running_count: number }

const getState = async () => {
  const response = await apiClient.get<GetStateResponseDTO>('/api/state')
  return response.data
}

export const getStateOptions = () => queryOptions({
  queryKey: ['detection', 'state'],
  queryFn: getState,
})
```

## Technical Decisions

### Why TanStack Start?

- Type-safe routing with TanStack Router
- Built-in SSR for better performance
- Seamless integration with TanStack Query
- Modern React patterns (Server Components ready)

### Why FastAPI?

- Automatic API documentation (Swagger/ReDoc)
- Native async/await support
- Excellent type hints with Pydantic
- Fast performance with Uvicorn

### Why SSE over WebSocket?

- **Simpler** - HTTP-based, no protocol upgrade
- **Unidirectional** - Perfect for server → client updates
- **Auto-reconnect** - Built into EventSource API
- **Easier deployment** - Works with standard HTTP infrastructure

### Why YOLOv8?

- **State-of-the-art** - Best accuracy/speed tradeoff
- **Easy integration** - Simple Python API
- **Pre-trained models** - Quick start with transfer learning
- **Active development** - Regular updates from Ultralytics

## Production Roadmap

- [ ] **Train Custom Model** - Card-specific YOLOv8 model
- [ ] **WebSocket Option** - Lower latency alternative to SSE
- [ ] **Redis Caching** - Cache detection results
- [ ] **Cloud Deployment** - AWS/GCP/Azure deployment guides
- [ ] **Model Optimization** - TensorRT, ONNX for inference speed
- [ ] **Multi-camera Support** - Multiple streams simultaneously
- [ ] **Historical Analytics** - Track counting sessions
- [ ] **Authentication** - User accounts and sessions
- [ ] **Mobile App** - React Native version

## Troubleshooting

### Camera Not Working

- Ensure HTTPS or localhost (required for `getUserMedia`)
- Check browser permissions for camera access
- Try different browsers (Chrome/Firefox recommended)

### YOLO Model Not Loading

- Verify model file exists at `MODEL_PATH`
- Check file permissions
- First run downloads base model (may take time)

### CORS Errors

- Verify `CORS_ORIGINS` in backend `.env`
- Check frontend `VITE_API_URL` points to backend
- Ensure both services are running

### SSE Connection Fails

- Check backend `/api/stream` endpoint is accessible
- Verify no proxy blocking SSE connections
- Check browser console for connection errors

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow existing code patterns (see `.claude/patterns.md`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Acknowledgments

- **Ultralytics** - YOLOv8 framework
- **TanStack** - Amazing React ecosystem
- **shadcn/ui** - Beautiful component library
- **FastAPI** - Excellent Python web framework

---

Built with modern best practices for production-ready applications.
