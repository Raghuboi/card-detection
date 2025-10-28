from ultralytics import YOLO
import numpy as np
from typing import Optional
import os

class ModelService:
    """Singleton service for YOLO model management"""
    _instance: Optional['ModelService'] = None
    _model: Optional[YOLO] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._load_model()

    def _load_model(self):
        """Load YOLO model (singleton pattern - loads once)"""
        # Default to trained model in models/ directory, fallback to placeholder
        default_model = "models/best.pt" if os.path.exists("models/best.pt") else "yolov8n.pt"
        model_path = os.getenv("MODEL_PATH", default_model)
        print(f"Loading YOLO model from {model_path}...")
        self._model = YOLO(model_path)
        print("YOLO model loaded successfully")

    def predict(self, image: np.ndarray):
        """Run inference on image"""
        if self._model is None:
            raise RuntimeError("Model not loaded")

        # Run inference
        results = self._model(image, verbose=False)
        return results[0] if results else None

    def get_model(self) -> YOLO:
        """Get the YOLO model instance"""
        if self._model is None:
            raise RuntimeError("Model not loaded")
        return self._model

# Create singleton instance
model_service = ModelService()
