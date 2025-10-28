# Playing Card Detection with YOLOv8

Educational computer vision notebook exploring real-time object detection for Hi-Lo blackjack counting practice. Demonstrates PyTorch + YOLOv8 training, OpenCV inference pipelines, and CUDA-accelerated ML fundamentals.

**📓 [Open card-detection.ipynb](./card-detection.ipynb) to get started**

## Results

- **mAP@0.5**: 99.5% on validation set
- **Inference**: 30+ FPS on RTX 4070
- **Dataset**: 21,203 training images, 52 classes (13 ranks × 4 suits)
- **Model**: YOLOv8n (3.2M params, 6MB)

## What's Inside

**[card-detection.ipynb](./card-detection.ipynb)** - Comprehensive notebook covering:

1. **Dataset Exploration** - YOLO annotation format, class distribution, bbox analysis
2. **ML Fundamentals** - Loss functions (CIoU + BCE + DFL), training loop concepts
3. **Model Training** - YOLOv8n fine-tuning with data augmentation
4. **Inference Pipeline** - Manual NMS implementation, OpenCV visualization
5. **Hi-Lo Counting** - Blackjack counting strategy with state management

## Tech Stack

- **PyTorch** 2.5.1+ (CUDA 12.1)
- **YOLOv8** (Ultralytics)
- **OpenCV** 4.8+
- **matplotlib**, **seaborn** (visualization)
- **NumPy**, **pandas** (data analysis)

## Quick Start

### Setup

```bash
pip install ultralytics opencv-python torch matplotlib seaborn pandas
jupyter notebook card-detection.ipynb
```

**Requirements**: Python 3.10+, CUDA 11.7+ (for GPU acceleration)

### Project Structure

```
card-detection/
├── card-detection.ipynb              # Main educational notebook
├── datasets/
│   ├── train/                        # 21,203 training images
│   ├── valid/                        # 2,020 validation images
│   └── data.yaml                     # Dataset config (52 classes)
└── backend/runs/card_detection/
    └── weights/best.pt               # Fine-tuned model weights
```

## Key Concepts Covered

### Dataset & Annotations
- YOLO annotation format (normalized bounding boxes)
- Class distribution analysis and balancing
- Bbox aspect ratio and area statistics
- Data augmentation (mosaic, mixup, HSV jitter)

### Training Pipeline
- Transfer learning from COCO pretrained weights
- Multi-component loss function: `7.5×CIoU + 0.5×BCE + 1.5×DFL`
- AdamW optimizer with learning rate scheduling
- Training metrics visualization and interpretation

### Inference & Post-Processing
- Manual NMS (Non-Maximum Suppression) implementation
- Confidence threshold tuning (0.5-0.7 recommended)
- OpenCV visualization pipeline
- Real-time performance optimization

### Hi-Lo Card Counting
- Blackjack counting strategy implementation
- State management (running count, seen cards)
- Duplicate detection prevention

| Card Range | Value | Strategy |
|------------|-------|----------|
| 2-6        | +1    | Favors player |
| 7-9        | 0     | Neutral |
| 10-A       | -1    | Favors dealer |

## Performance

**Metrics** (after 5 epochs):
- Precision: 99.36%
- Recall: 99.51%
- mAP@0.5: 99.5%
- mAP@0.5:0.95: 70.77%

**Inference Speed** (RTX 4070):
- 30ms/frame (33 FPS)
- ~2GB GPU memory

## Dataset

[Roboflow Playing Cards Dataset](https://universe.roboflow.com/augmented-startups/playing-cards-ow27d)
- 21,203 training images
- 2,020 validation images
- 52 classes (13 ranks × 4 suits)
- Well-balanced: ~400 instances per class

## Learning Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Object Detection Metrics Explained](https://github.com/rafaelpadilla/Object-Detection-Metrics)
- [Hi-Lo Card Counting Strategy](https://en.wikipedia.org/wiki/Card_counting#Hi-Lo)

## Author

**Raghunath Prabhakar**
[![GitHub](https://img.shields.io/badge/GitHub-Raghuboi-181717?style=flat&logo=github)](https://github.com/Raghuboi)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-raghunath--prabhakar-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/raghunath-prabhakar)

## Acknowledgments

- [Ultralytics](https://ultralytics.com/) - YOLOv8 framework
- [Roboflow](https://roboflow.com/) - Playing Cards dataset
- [OpenCV](https://opencv.org/) Community

---

**Educational project for hands-on computer vision learning**
MIT License
