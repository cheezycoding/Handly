#!/usr/bin/env python3
"""
Real-time Hand Gesture Recognition System
Recognizes three gestures: Thank You, Hello, and I Love You
Using MediaPipe for hand detection and a trained classifier for gesture recognition
"""

import cv2
import mediapipe as mp
import numpy as np
import pickle
import os
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


class GestureRecognizer:
    """Main gesture recognition system using MediaPipe and ML classifier"""
    
    def __init__(self, model_path='gesture_model.pkl', scaler_path='scaler.pkl'):
        """Initialize the gesture recognizer with MediaPipe and trained model"""
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Gesture labels
        self.gesture_labels = {
            0: 'Thank You',
            1: 'Hello',
            2: 'I Love You'
        }
        
        # Gesture colors for visualization
        self.gesture_colors = {
            'Thank You': (0, 255, 0),      # Green
            'Hello': (255, 0, 0),           # Blue
            'I Love You': (0, 0, 255)       # Red
        }
        
        # Load trained model and scaler
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.model_trained = False
        
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model and scaler if they exist"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.model_trained = True
                print("✓ Loaded pre-trained model and scaler")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model_trained = False
        else:
            print("⚠ No pre-trained model found. Training mode will be available.")
    
    def extract_hand_landmarks(self, frame):
        """Extract hand landmarks from a frame using MediaPipe"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        landmarks = None
        hand_detected = False
        
        if results.multi_hand_landmarks and results.multi_handedness:
            hand_detected = True
            # Get the first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract 21 landmarks (x, y, z coordinates)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            landmarks = np.array(landmarks, dtype=np.float32)
        
        return landmarks, hand_detected, results
    
    def predict_gesture(self, landmarks):
        """Predict gesture from hand landmarks"""
        if self.model is None or not self.model_trained:
            return None, 0.0
        
        try:
            # Normalize landmarks using the scaler
            landmarks_scaled = self.scaler.transform([landmarks])
            
            # Predict gesture
            prediction = self.model.predict(landmarks_scaled)[0]
            confidence = np.max(self.model.predict_proba(landmarks_scaled))
            
            return prediction, confidence
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None, 0.0
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame"""
        if hand_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
    
    def run_live_recognition(self, camera_id=0):
        """Run live gesture recognition from webcam"""
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print("Error: Cannot open camera")
            return
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("\n" + "="*60)
        print("GESTURE RECOGNITION SYSTEM - LIVE MODE")
        print("="*60)
        print("Recognized Gestures:")
        print("  1. Thank You - Wave hand with palm open")
        print("  2. Hello - Raise hand and wave")
        print("  3. I Love You - Thumb, index, and pinky extended")
        print("\nControls:")
        print("  'q' - Quit")
        print("  's' - Save frame with detected gesture")
        print("="*60 + "\n")
        
        frame_count = 0
        gesture_history = []
        history_size = 5  # Smooth predictions using history
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Extract hand landmarks
            landmarks, hand_detected, results = self.extract_hand_landmarks(frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw_landmarks(frame, hand_landmarks)
            
            # Predict gesture if hand is detected
            gesture_text = "No Hand Detected"
            gesture_color = (128, 128, 128)  # Gray
            confidence = 0.0
            
            if hand_detected and landmarks is not None:
                if self.model_trained:
                    prediction, confidence = self.predict_gesture(landmarks)
                    
                    if prediction is not None and confidence > 0.5:
                        gesture_text = self.gesture_labels[prediction]
                        gesture_color = self.gesture_colors[gesture_text]
                        gesture_history.append(prediction)
                    else:
                        gesture_text = "Uncertain"
                        gesture_color = (0, 165, 255)  # Orange
                        gesture_history.append(-1)
                else:
                    gesture_text = "Model Not Trained"
                    gesture_color = (0, 165, 255)  # Orange
            else:
                gesture_history.append(-1)
            
            # Keep history size limited
            if len(gesture_history) > history_size:
                gesture_history.pop(0)
            
            # Draw information on frame
            cv2.rectangle(frame, (10, 10), (630, 100), (0, 0, 0), -1)
            cv2.putText(frame, "Gesture Recognition System", (20, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Display detected gesture
            cv2.putText(frame, f"Gesture: {gesture_text}", (20, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, gesture_color, 2)
            
            # Display confidence if available
            if self.model_trained and confidence > 0:
                cv2.putText(frame, f"Confidence: {confidence:.2f}", (20, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, gesture_color, 1)
            
            # Display frame info
            cv2.putText(frame, f"Frame: {frame_count}", (w - 150, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Display status
            status_text = "Ready" if self.model_trained else "Training Required"
            status_color = (0, 255, 0) if self.model_trained else (0, 165, 255)
            cv2.putText(frame, f"Status: {status_text}", (w - 200, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
            
            # Show frame
            cv2.imshow('Gesture Recognition', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nExiting...")
                break
            elif key == ord('s'):
                filename = f"gesture_frame_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Frame saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()
        print("Live recognition ended.")
    
    def collect_training_data(self, gesture_name, num_samples=30, camera_id=0):
        """Collect training data for a specific gesture"""
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print("Error: Cannot open camera")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"\n{'='*60}")
        print(f"COLLECTING DATA FOR: {gesture_name.upper()}")
        print(f"{'='*60}")
        print(f"Collect {num_samples} samples of the gesture")
        print("Press SPACE to capture a sample")
        print("Press 'q' to finish collecting this gesture")
        print(f"{'='*60}\n")
        
        collected_landmarks = []
        sample_count = 0
        
        while sample_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            landmarks, hand_detected, results = self.extract_hand_landmarks(frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw_landmarks(frame, hand_landmarks)
            
            # Draw UI
            cv2.rectangle(frame, (10, 10), (630, 100), (0, 0, 0), -1)
            cv2.putText(frame, f"Collecting: {gesture_name}", (20, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Samples: {sample_count}/{num_samples}", (20, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            status = "Hand Detected" if hand_detected else "No Hand"
            status_color = (0, 255, 0) if hand_detected else (0, 0, 255)
            cv2.putText(frame, status, (w - 200, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
            
            cv2.imshow('Data Collection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space to capture
                if hand_detected and landmarks is not None:
                    collected_landmarks.append(landmarks)
                    sample_count += 1
                    print(f"✓ Sample {sample_count} captured")
                else:
                    print("✗ No hand detected, try again")
            elif key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Save collected data
        if collected_landmarks:
            data_file = f"training_data_{gesture_name.lower().replace(' ', '_')}.pkl"
            with open(data_file, 'wb') as f:
                pickle.dump(collected_landmarks, f)
            print(f"\n✓ Saved {len(collected_landmarks)} samples to {data_file}")
            return collected_landmarks
        else:
            print("\n✗ No data collected")
            return []
    
    def train_model(self, gestures_to_train=['Thank You', 'Hello', 'I Love You']):
        """Train the gesture recognition model"""
        print(f"\n{'='*60}")
        print("MODEL TRAINING")
        print(f"{'='*60}\n")
        
        all_landmarks = []
        all_labels = []
        
        for gesture_idx, gesture_name in enumerate(gestures_to_train):
            print(f"\n[{gesture_idx + 1}/{len(gestures_to_train)}] Training for: {gesture_name}")
            
            # Collect training data
            landmarks = self.collect_training_data(gesture_name, num_samples=30)
            
            if landmarks:
                all_landmarks.extend(landmarks)
                all_labels.extend([gesture_idx] * len(landmarks))
        
        if len(all_landmarks) > 0:
            print(f"\n{'='*60}")
            print("TRAINING CLASSIFIER")
            print(f"{'='*60}")
            
            X = np.array(all_landmarks)
            y = np.array(all_labels)
            
            print(f"Total samples: {len(X)}")
            print(f"Feature dimension: {X.shape[1]}")
            
            # Normalize features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Random Forest classifier
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_scaled, y)
            
            # Save model and scaler
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            self.model_trained = True
            
            # Calculate training accuracy
            train_accuracy = self.model.score(X_scaled, y)
            print(f"\n✓ Model trained successfully!")
            print(f"✓ Training accuracy: {train_accuracy:.2%}")
            print(f"✓ Model saved to: {self.model_path}")
            print(f"✓ Scaler saved to: {self.scaler_path}")
        else:
            print("\n✗ No training data collected")


def main():
    """Main function to run the gesture recognition system"""
    import sys
    
    recognizer = GestureRecognizer()
    
    print("\n" + "="*60)
    print("HAND GESTURE RECOGNITION SYSTEM")
    print("="*60)
    print("\nOptions:")
    print("  1. Train new model")
    print("  2. Run live recognition")
    print("  3. Exit")
    print("="*60)
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            recognizer.train_model()
        elif choice == '2':
            if recognizer.model_trained:
                recognizer.run_live_recognition()
            else:
                print("\n⚠ Model not trained yet. Please train the model first (option 1)")
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
