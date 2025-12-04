"""
Quick setup script - downloads videos, extracts landmarks, trains model
For signs: help, no, yes
"""
import json
import os
import urllib.request
import ssl
import cv2
import numpy as np
import mediapipe as mp
from collections import defaultdict
import pickle

# Disable SSL verification for problematic URLs
ssl._create_default_https_context = ssl._create_unverified_context

SIGNS = ['help', 'no', 'yes']
DATA_DIR = 'data'
PROCESSED_DIR = 'processed'
MODELS_DIR = 'models'

# Create directories
for d in [DATA_DIR, PROCESSED_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)
for sign in SIGNS:
    os.makedirs(f'{DATA_DIR}/{sign}', exist_ok=True)

print("=" * 50)
print("STEP 1: Downloading videos")
print("=" * 50)

# Load WLASL data
with open('WLASL_v0.3.json', 'r') as f:
    wlasl = json.load(f)

# Find videos for our signs
for entry in wlasl:
    gloss = entry['gloss'].lower()
    if gloss in SIGNS:
        for inst in entry['instances'][:15]:  # Get up to 15 per sign
            vid_id = inst['video_id']
            url = inst.get('url', '')
            
            if not url or 'youtube' in url.lower():
                continue
                
            out_path = f'{DATA_DIR}/{gloss}/{vid_id}.mp4'
            if os.path.exists(out_path):
                continue
                
            try:
                urllib.request.urlretrieve(url, out_path)
                print(f"✓ {gloss}/{vid_id}.mp4")
            except:
                pass

# Count downloads
for sign in SIGNS:
    count = len([f for f in os.listdir(f'{DATA_DIR}/{sign}') if f.endswith('.mp4')])
    print(f"{sign}: {count} videos")

print("\n" + "=" * 50)
print("STEP 2: Extracting landmarks")
print("=" * 50)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

os.makedirs(f'{PROCESSED_DIR}/landmarks', exist_ok=True)

for sign in SIGNS:
    sign_dir = f'{DATA_DIR}/{sign}'
    out_dir = f'{PROCESSED_DIR}/landmarks/{sign}'
    os.makedirs(out_dir, exist_ok=True)
    
    videos = [f for f in os.listdir(sign_dir) if f.endswith('.mp4')]
    
    for vid_file in videos:
        vid_path = os.path.join(sign_dir, vid_file)
        out_path = os.path.join(out_dir, vid_file.replace('.mp4', '.npy'))
        
        if os.path.exists(out_path):
            continue
        
        cap = cv2.VideoCapture(vid_path)
        landmarks_seq = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                frame_landmarks = []
                for lm in hand.landmark:
                    frame_landmarks.extend([lm.x, lm.y, lm.z])
                landmarks_seq.append(frame_landmarks)
        
        cap.release()
        
        if len(landmarks_seq) >= 5:
            np.save(out_path, np.array(landmarks_seq))
            print(f"✓ {sign}/{vid_file}")

hands.close()

print("\n" + "=" * 50)
print("STEP 3: Preparing dataset")
print("=" * 50)

SEQUENCE_LENGTH = 30
X, y = [], []

for idx, sign in enumerate(SIGNS):
    lm_dir = f'{PROCESSED_DIR}/landmarks/{sign}'
    if not os.path.exists(lm_dir):
        continue
    
    for f in os.listdir(lm_dir):
        if not f.endswith('.npy'):
            continue
        
        seq = np.load(os.path.join(lm_dir, f))
        
        # Pad or truncate
        if len(seq) < SEQUENCE_LENGTH:
            pad = np.zeros((SEQUENCE_LENGTH - len(seq), 63))
            seq = np.vstack([seq, pad])
        else:
            seq = seq[:SEQUENCE_LENGTH]
        
        X.append(seq)
        y.append(idx)

X = np.array(X)
y = np.array(y)

print(f"Dataset: {X.shape[0]} samples, {len(SIGNS)} classes")

# Save
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

with open(f'{PROCESSED_DIR}/dataset.pkl', 'wb') as f:
    pickle.dump({'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}, f)

with open(f'{MODELS_DIR}/label_map.pkl', 'wb') as f:
    pickle.dump({'signs': SIGNS}, f)

print("\n" + "=" * 50)
print("STEP 4: Training model")
print("=" * 50)

import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.LSTM(64, return_sequences=True, input_shape=(30, 63)),
    keras.layers.Dropout(0.2),
    keras.layers.LSTM(32),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(len(SIGNS), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.2, verbose=1)
model.save(f'{MODELS_DIR}/sign_classifier.keras')

print("\n" + "=" * 50)
print("DONE! Model saved to models/sign_classifier.keras")
print("=" * 50)

