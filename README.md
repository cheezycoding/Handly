# ASL Alphabet Recognition

Real-time American Sign Language alphabet detection using a pretrained CNN model.

## Features
- **Pretrained Model**: 98.92% accuracy on ASL alphabet (A-Z)
- **Real-time Detection**: Uses webcam via browser
- **MediaPipe Landmarks**: Extracts 21 hand points (63 features)

## Project Structure
```
Handly/
├── app.py              # Flask server + prediction API
├── models/
│   └── best_cnn_asl_model.keras  # Pretrained CNN model
├── templates/
│   └── index.html      # Web interface
├── requirements.txt
└── README.md
```

## Usage
```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000 in Chrome
```

## Model Details
- **Architecture**: Conv1D CNN
- **Input**: 63 features (21 landmarks × 3 coordinates)
- **Output**: 26 letters (A-Z) + DEL, NOTHING, SPACE
- **Source**: [HuggingFace](https://huggingface.co/ademaulana/CNN-ASL-Alphabet-Sign-Recognition)
