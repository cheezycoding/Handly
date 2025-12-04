"""
Sign Language Recognition - 3 Words (help, no, yes)
Uses LSTM model trained on MediaPipe hand landmarks
"""
from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import base64
import cv2
import mediapipe as mp
import tensorflow as tf
from collections import deque

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("models/sign_classifier.keras")
with open("models/label_map.pkl", 'rb') as f:
    label_data = pickle.load(f)
signs = label_data['signs']

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

# Buffer for sequence
SEQUENCE_LENGTH = 30
buffers = {}

def extract_landmarks(frame):
    # No flip - model was trained on non-flipped videos
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        landmarks = []
        for lm in hand.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
        return landmarks, True
    return [0.0] * 63, False

@app.route('/')
def index():
    return render_template('index.html', signs=signs)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    frame_data = data['frame']
    session_id = data.get('session', 'default')
    
    if session_id not in buffers:
        buffers[session_id] = deque(maxlen=SEQUENCE_LENGTH)
    
    buffer = buffers[session_id]
    
    # Decode image
    img_bytes = base64.b64decode(frame_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    landmarks, hand_detected = extract_landmarks(frame)
    buffer.append(landmarks)
    
    if len(buffer) == SEQUENCE_LENGTH:
        X = np.array([list(buffer)])
        pred = model.predict(X, verbose=0)
        idx = int(np.argmax(pred))
        conf = float(pred[0][idx])
        return jsonify({
            'prediction': signs[idx],
            'confidence': conf,
            'hand_detected': hand_detected,
            'ready': True
        })
    
    return jsonify({
        'prediction': None,
        'confidence': 0,
        'hand_detected': hand_detected,
        'ready': False,
        'buffer_size': len(buffer)
    })

@app.route('/reset', methods=['POST'])
def reset():
    session_id = request.json.get('session', 'default')
    if session_id in buffers:
        buffers[session_id].clear()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print(f"\nSigns: {signs}")
    print("Open http://localhost:8080 in Chrome\n")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
