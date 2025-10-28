from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
import cv2
import numpy as np
import json
import asyncio
from datetime import datetime

from services import model_service, counting_service

router = APIRouter()

class DetectedCard(BaseModel):
    name: str
    confidence: float
    rank: str
    suit: str
    bbox: List[float]

class DetectionResponse(BaseModel):
    cards: List[DetectedCard]
    count: int
    total_cards_detected: int
    timestamp: str

@router.post("/detect", response_model=DetectionResponse)
async def detect_cards(file: UploadFile = File(...)):
    """
    Detect playing cards in uploaded image
    Returns detected cards and current running count
    """
    try:
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Run YOLO inference
        results = model_service.predict(image)

        detected_cards = []
        if results and results.boxes:
            for box in results.boxes:
                # Extract box data
                bbox = box.xyxy[0].cpu().numpy().tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # For now, using placeholder card names
                # When you train your model, replace this with actual card detection
                card_name = f"Card_{cls}"
                rank = "A"  # Placeholder
                suit = "Spades"  # Placeholder

                # Create unique card ID for counting
                card_id = f"{rank}_{suit}_{bbox[0]:.0f}_{bbox[1]:.0f}"

                # Process card through counting service
                counting_result = counting_service.process_card(card_id, rank)

                detected_cards.append(DetectedCard(
                    name=card_name,
                    confidence=conf,
                    rank=rank,
                    suit=suit,
                    bbox=bbox
                ))

        # Get current state
        state = counting_service.get_state()

        return DetectionResponse(
            cards=detected_cards,
            count=state["running_count"],
            total_cards_detected=state["total_cards_detected"],
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_count():
    """Reset the running count and detected cards"""
    result = counting_service.reset()
    return {"message": "Count reset successfully", **result}

@router.get("/state")
async def get_state():
    """Get current counting state"""
    return counting_service.get_state()

# Server-Sent Events endpoint for real-time updates
@router.get("/stream")
async def stream_detections():
    """
    SSE endpoint for real-time detection updates
    Clients connect and receive detection events as they occur
    """
    async def event_generator():
        """Generate SSE events"""
        try:
            while True:
                # Get current state
                state = counting_service.get_state()

                # Format as SSE message
                data = json.dumps({
                    "type": "state_update",
                    "running_count": state["running_count"],
                    "total_cards_detected": state["total_cards_detected"],
                    "timestamp": datetime.now().isoformat()
                })

                yield f"data: {data}\n\n"

                # Update every 500ms
                await asyncio.sleep(0.5)

        except asyncio.CancelledError:
            # Client disconnected
            yield "data: {\"type\": \"disconnect\"}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
