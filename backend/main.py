from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Card Detection API",
    description="Real-time playing card detection with Hi-Lo counting",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers import detection

app.include_router(detection.router, prefix="/api", tags=["detection"])

@app.get("/")
async def root():
    return {"message": "Card Detection API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
