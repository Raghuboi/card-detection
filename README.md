# Playing Card Detection with OpenCV & PyTorch

Educational computer vision project exploring real-time object detection. Demonstrates OpenCV pipelines, PyTorch fine-tuning, and CUDA-accelerated inference with YOLOv8 on a playing cards dataset.

## Key Results

- **mAP@0.5**: 99.46% on validation set (5 epochs)
- **Inference**: 30+ FPS on RTX 4070
- **Dataset**: 21,203 training images, 52 card classes
- **Model**: YOLOv8n (3.2M params, 6MB)

## Tech Stack

**Computer Vision & Deep Learning**
- **OpenCV** - Video capture, image processing, visualization
- **PyTorch** - Deep learning framework with CUDA support
- **CUDA** - NVIDIA GPU acceleration
- **YOLOv8** - Anchor-free object detection (Ultralytics)

**Analysis & Visualization**
- **matplotlib**, **seaborn** - Training metrics and plots
- **NumPy**, **pandas** - Data analysis

## Overview

I built this to learn modern computer vision workflows. The project covers:

- Transfer learning from COCO pretrained weights to 52 playing card classes
- Real-time inference pipeline with OpenCV video processing
- GPU-accelerated training and inference with CUDA
- Hi-Lo card counting implementation

## Project Files

```
card-detection/
├── card-detection.ipynb              # Educational notebook (START HERE)
├── card-detection.py                 # Webcam inference script
├── playing_cards.v2-release.yolov8/
│   ├── train/                        # 21,203 training images
│   ├── valid/                        # 2,020 validation images
│   └── data.yaml                     # Dataset config
└── runs/card_detection/
    └── weights/best.pt               # Fine-tuned model
```

## Quick Start

### Educational Notebook (Recommended)

The notebook walks through the complete pipeline:

```bash
pip install ultralytics opencv-python torch matplotlib seaborn pandas
jupyter notebook card-detection.ipynb
```

**Topics covered**: CV fundamentals with OpenCV, traditional vs deep learning detection, YOLO architecture, dataset analysis, training workflow, metrics interpretation, real-time inference.

### Webcam Inference

Real-time card detection with Hi-Lo counting:

```bash
python card-detection.py
```

**Controls**: `Q` (quit), `R` (reset count), `C` (toggle confidence), `SPACE` (pause)

## Training

### Dataset

[Roboflow Playing Cards](https://universe.roboflow.com/augmented-startups/playing-cards-ow27d):
- 21,203 training images with YOLO annotations
- 52 classes (10C, 10D, 10H, 10S ... AS)
- ~400 instances per class (well-balanced)

### Configuration

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.train(
    data='playing_cards.v2-release.yolov8/data.yaml',
    epochs=100,
    batch=16,
    imgsz=640,
    device=0,
    patience=50
)
```

### Results

| Epoch | Box Loss | Cls Loss | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|-------|----------|----------|-----------|--------|---------|--------------|
| 1     | 0.8733   | 1.1310   | 0.9381    | 0.9606 | 0.9838  | 0.6619       |
| 5     | 0.6917   | 0.7519   | 0.9936    | 0.9951 | 0.9946  | 0.7077       |

## Hi-Lo Card Counting

Implements the Hi-Lo blackjack counting strategy in `card-detection.py`:

| Card Range | Value | Interpretation |
|------------|-------|----------------|
| 2-6        | +1    | Favors player  |
| 7-9        | 0     | Neutral        |
| 10-A       | -1    | Favors dealer  |

Tracks seen cards to prevent double-counting across frames.

## Performance Optimization

**Current Performance** (RTX 4070):
- Inference: 30ms/frame (33 FPS)
- GPU Memory: ~2GB

**Optimization Techniques**:

1. **ONNX Export** (20-30% faster)
   ```python
   model.export(format='onnx', dynamic=True)
   ```

2. **TensorRT** (2-5x faster on NVIDIA GPUs)
   ```python
   model.export(format='engine', half=True)
   ```

3. **Quantization** (FP32 → INT8)
   - 4x smaller model size
   - 2-4x faster inference
   - <1% accuracy loss

4. **Model Variants**
   - YOLOv8n (current): 6MB, fastest
   - YOLOv8s: 22MB, more accurate
   - YOLOv8m: 52MB, balanced

## Technical Deep Dives

### Why YOLOv8?

**vs Traditional CV** (edge detection, contours):
- Semantic understanding, not just bounding boxes
- Robust to lighting/rotation/occlusion
- No manual threshold tuning

**vs Two-Stage Detectors** (R-CNN, Faster R-CNN):
- Single-pass detection (real-time capable)
- End-to-end training
- Simpler architecture

**YOLOv8 Improvements**:
- Anchor-free detection
- CIoU + DFL loss (better localization)
- Advanced augmentation (mosaic, mixup)
- CSPDarknet53 backbone with FPN

### Metrics

- **Precision**: Of all predictions, what % are correct? (99.36%)
- **Recall**: Of all ground truth, what % detected? (99.51%)
- **mAP@0.5**: Average precision at IoU ≥ 0.5 (99.46%)
- **mAP@0.5:0.95**: Stricter metric across IoU thresholds (70.77%)

### Loss Functions

- **Box Loss (CIoU)**: Bounding box localization quality
- **Class Loss (BCE)**: Classification accuracy
- **DFL Loss**: Distribution Focal Loss for better regression

## Requirements

### Core Dependencies
```
ultralytics>=8.0.0
opencv-python>=4.8.0
torch>=2.0.0
torchvision>=0.15.0
matplotlib>=3.7.0
seaborn>=0.12.0
pandas>=2.0.0
numpy>=1.24.0
```

### System
- Python 3.10+
- CUDA 11.7+ (for GPU acceleration)
- 8GB+ RAM (16GB recommended)
- 5GB+ storage (dataset + models)

## Learning Roadmap

Optional extensions to explore:

- [ ] Complete 100-epoch training with early stopping
- [ ] Hyperparameter tuning (learning rate, batch size, augmentation)
- [ ] Model comparison (YOLOv8s, YOLOv8m)
- [ ] Export to ONNX/TensorRT for faster inference
- [ ] True Count calculation (running count / remaining decks)
- [ ] Multi-object tracking for temporal consistency
- [ ] Mobile deployment exploration (TensorFlow Lite)

## Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Object Detection Metrics](https://github.com/rafaelpadilla/Object-Detection-Metrics)
- [Hi-Lo Card Counting](https://en.wikipedia.org/wiki/Card_counting#Hi-Lo)

## Author

**Raghunath Prabhakar**

[![GitHub](https://img.shields.io/badge/GitHub-Raghuboi-181717?style=flat&logo=github)](https://github.com/Raghuboi)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-raghunath--prabhakar-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/raghunath-prabhakar)
[![Twitter](https://img.shields.io/badge/Twitter-@Raghunath__Pr-1DA1F2?style=flat&logo=twitter)](https://twitter.com/Raghunath_Pr)

## License

MIT License

## Acknowledgments

- Ultralytics - YOLOv8 framework
- Roboflow - Playing Cards dataset
- OpenCV Community

---

*Educational computer vision project for hands-on ML/CV learning.*
