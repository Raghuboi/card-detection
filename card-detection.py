#!/usr/bin/env python3
"""
Real-Time Playing Card Detection with Hi-Lo Counting

Simple OpenCV webcam inference script using trained YOLOv8 model.
Detects playing cards and maintains a running Hi-Lo blackjack count.

Usage:
    python card-detection.py

Controls:
    'q' - Quit
    'r' - Reset count
    'c' - Toggle confidence display
    SPACE - Pause/Resume

Requirements:
    - opencv-python
    - ultralytics
    - PyTorch with CUDA (for GPU acceleration)
"""

import cv2
import torch
from pathlib import Path
from ultralytics import YOLO


class HiLoCounter:
    """Hi-Lo card counting system for blackjack"""

    # Hi-Lo values: +1 for low cards (2-6), 0 for neutral (7-9), -1 for high (10-A)
    CARD_VALUES = {
        '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,  # Low cards (favor player)
        '7': 0, '8': 0, '9': 0,                   # Neutral
        '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1  # High cards (favor dealer)
    }

    def __init__(self):
        self.running_count = 0
        self.seen_cards = set()

    def extract_rank(self, card_name):
        """Extract rank from card name (e.g., '10C' -> '10', 'AS' -> 'A')"""
        if card_name.startswith('10'):
            return '10'
        return card_name[0]

    def update(self, detected_cards):
        """Update count with newly detected cards"""
        new_cards = []
        for card in detected_cards:
            if card not in self.seen_cards:
                rank = self.extract_rank(card)
                value = self.CARD_VALUES.get(rank, 0)
                self.running_count += value
                self.seen_cards.add(card)
                new_cards.append((card, value))
        return new_cards

    def reset(self):
        """Reset count for new deck"""
        self.running_count = 0
        self.seen_cards.clear()


def draw_detection_box(frame, x1, y1, x2, y2, label, confidence, color=(0, 255, 0)):
    """Draw bounding box with label on frame"""
    # Draw rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Prepare label text
    text = f"{label} {confidence:.2f}"

    # Get text size for background rectangle
    (text_width, text_height), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
    )

    # Draw background rectangle for text
    cv2.rectangle(
        frame,
        (x1, y1 - text_height - 10),
        (x1 + text_width, y1),
        color,
        -1
    )

    # Draw text
    cv2.putText(
        frame, text, (x1, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )


def draw_count_overlay(frame, counter, fps, paused=False):
    """Draw running count and stats overlay"""
    height, width = frame.shape[:2]

    # Semi-transparent background for stats
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Running count (large and prominent)
    count_text = f"Count: {counter.running_count:+d}"
    count_color = (0, 255, 0) if counter.running_count > 0 else (0, 0, 255) if counter.running_count < 0 else (255, 255, 255)
    cv2.putText(frame, count_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, count_color, 3)

    # Card count
    cv2.putText(frame, f"Cards seen: {len(counter.seen_cards)}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Paused indicator
    if paused:
        cv2.putText(frame, "PAUSED", (width // 2 - 80, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    # Controls help (bottom)
    controls = "Q:Quit | R:Reset | C:Confidence | SPACE:Pause"
    cv2.putText(frame, controls, (10, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def main():
    """Main inference loop"""
    # Configuration
    MODEL_PATH = Path('backend/runs/card_detection/weights/best.pt')
    CONFIDENCE_THRESHOLD = 0.6

    # Check if trained model exists
    if not MODEL_PATH.exists():
        print(f"Error: Model not found at {MODEL_PATH}")
        print("Please train the model first or update MODEL_PATH")
        return

    # Check CUDA availability
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    if device == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # Load model
    print(f"Loading model from {MODEL_PATH}...")
    model = YOLO(str(MODEL_PATH))
    print("Model loaded successfully!")

    # Initialize counter
    counter = HiLoCounter()

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    # Set resolution (optional, adjust as needed)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nWebcam opened. Starting detection...")
    print("Controls: Q=Quit, R=Reset count, C=Toggle confidence, SPACE=Pause\n")

    # State variables
    show_confidence = True
    paused = False
    fps = 0.0

    while True:
        if not paused:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break

            # Start timer for FPS
            timer = cv2.getTickCount()

            # Run detection
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]

            # Extract detected cards
            detected_cards = []
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                card_name = model.names[class_id]

                detected_cards.append(card_name)

                # Draw detection
                if show_confidence:
                    draw_detection_box(frame, x1, y1, x2, y2, card_name, confidence)
                else:
                    draw_detection_box(frame, x1, y1, x2, y2, card_name, confidence)

            # Update counter
            new_cards = counter.update(detected_cards)

            # Calculate FPS
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        else:
            # Just read frame but don't process
            ret, frame = cap.read()
            if not ret:
                break

        # Draw overlay
        draw_count_overlay(frame, counter, fps, paused)

        # Display frame
        cv2.imshow('Card Detection - Hi-Lo Counter', frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            counter.reset()
            print("Count reset!")
        elif key == ord('c'):
            show_confidence = not show_confidence
        elif key == ord(' '):
            paused = not paused
            print("Paused" if paused else "Resumed")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

    # Final statistics
    print("\n" + "="*50)
    print("SESSION SUMMARY")
    print("="*50)
    print(f"Final running count: {counter.running_count:+d}")
    print(f"Total cards seen: {len(counter.seen_cards)}")
    if counter.seen_cards:
        print(f"Cards detected: {sorted(counter.seen_cards)}")
    print("="*50)


if __name__ == "__main__":
    main()
