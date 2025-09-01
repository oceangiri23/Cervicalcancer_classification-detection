# Cervical Cancer Cell Detection & Classification

A YOLOv8-based object detection project for automated detection and classification of cervical cancer cells from cytological images. This system can identify and classify different types of cervical cells including Dyskeratotic, Koilocytotic, Metaplastic, Parabasal, and Superficial-Intermediate cells.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Results](#results)

## 🔍 Overview

This project implements YOLOv8 object detection to automatically detect and classify cervical cancer cells from cytological images. The system processes Pap smear images and can identify multiple cell types simultaneously, providing bounding box coordinates and classification labels for each detected cell. This assists pathologists in cervical cancer screening and diagnosis.

## ✨ Features

- **YOLOv8 Object Detection**: State-of-the-art real-time cell detection and classification
- **Multi-class Detection**: Identifies 5 different cervical cell types
- **Automated Preprocessing**: Converts polygon annotations to YOLO format
- **Data Augmentation**: Advanced augmentation techniques to prevent overfitting
- **Comprehensive Evaluation**: Detailed metrics including mAP, precision, recall, and F1-score
- **Visual Results**: Detection visualization with bounding boxes and class labels
- **GPU Acceleration**: CUDA support for fast training and inference

## 📊 Dataset

The project uses a cervical cancer cell dataset containing:

- **Image Format**: BMP cytological images
- **Annotation Format**: Polygon coordinates in .dat files (cytoplasm boundaries)
- **Cell Types**:
  - Dyskeratotic
  - Koilocytotic
  - Metaplastic
  - Parabasal
  - Superficial-Intermediate

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/oceangiri23/Cervicalcancer_classification-detection.git
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  
# Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install ultralytics opencv-python scikit-learn numpy pathlib
```

## 💻 Usage

### 1. Dataset Preparation

Convert the original dataset to YOLO format:

```bash
python create_yolo_dataset.py
```

### 2. Model Training

Train the YOLOv8 model:

```bash
python train_yolo_model.py
```

Or use the Jupyter notebook:

```bash
jupyter notebook detection.ipynb
```

### 3. Model Testing

Test the trained model on new images:

```bash
python test.py
```

### 4. Model Evaluation

Get detailed metrics and performance analysis:

```bash
python find_metrics.py
```

## Model Architecture

### YOLOv8 Configuration

- **Base Model**: YOLOv8s (small version to reduce overfitting)
- **Input Size**: 640x640 pixels
- **Optimizer**: AdamW with custom learning rate schedule
- **Loss Weights**:
  - Box localization: 7.0
  - Classification: 1.0
  - Distribution Focal Loss: 1.5

## Acknowledgments

- YOLOv8 by Ultralytics
- Cervical cancer cell dataset contributors
- Open-source computer vision libraries
