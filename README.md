# Fatigue Level Detection using RT-DETR

## Overview

This project implements a real-time fatigue level detection system using a deep learning object detection model (RT-DETR). The system analyzes facial features from video input to classify fatigue levels.

The model categorizes fatigue into three levels:

* Normal
* Moderate Fatigue
* Severe Fatigue

The system can be used for applications such as driver monitoring, workplace safety, and fatigue analysis.

---

## Project Structure

Deteksi-ngantuk

├── Dataset/                # Dataset used for training and testing
├── config.py               # Configuration parameters for the system
├── logic.py                # Core fatigue detection logic
├── main.py                 # Main program entry point
├── visualizer.py           # Visualization of detection results
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Files ignored by Git

---

## Installation

Clone the repository

git clone https://github.com/rzkydell/Fatigue-Level-Detection-using-RT-DETR.git

Navigate to the project folder

cd Fatigue-Level-Detection-using-RT-DETR

Install required libraries

pip install -r requirements.txt

---

## Usage

Run the main application

python main.py

The program will start the fatigue detection system and process the input video or webcam stream.

---

## Dataset

The dataset used for training should be placed inside the `Dataset` directory.

Due to size limitations, the dataset may not be included in the repository.

---

## Model

This system uses a deep learning object detection model (RT-DETR) to analyze facial fatigue indicators.

---

## Requirements

Python 3.9 or newer is recommended.

All required Python packages are listed in `requirements.txt`.

---

## Author

Rizky Dell
