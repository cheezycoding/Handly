#!/usr/bin/env python3
"""
Simple demo script to test gesture recognition with pre-trained model
This script demonstrates the gesture recognition system in action
"""

import sys
sys.path.insert(0, '/home/ubuntu')

from gesture_recognizer import GestureRecognizer


def main():
    """Run a simple demo of the gesture recognition system"""
    
    print("\n" + "="*70)
    print(" "*15 + "GESTURE RECOGNITION SYSTEM - DEMO")
    print("="*70)
    
    # Initialize recognizer
    recognizer = GestureRecognizer()
    
    print("\n📋 System Information:")
    print(f"   • Model Status: {'✓ Trained' if recognizer.model_trained else '✗ Not Trained'}")
    print(f"   • Recognized Gestures: Thank You, Hello, I Love You")
    print(f"   • Detection Method: MediaPipe Hand Pose Estimation")
    print(f"   • Classification: Random Forest Classifier")
    
    print("\n" + "="*70)
    print("\n🎯 QUICK START OPTIONS:")
    print("\n   Option 1: Train Model (Recommended First Time)")
    print("   ─────────────────────────────────────────────")
    print("   This will collect training data for each gesture:")
    print("   • Thank You - Wave hand with palm open")
    print("   • Hello - Raise hand and wave")
    print("   • I Love You - Thumb, index, and pinky extended")
    print("   ")
    print("   For each gesture, you'll capture 30 samples by pressing SPACE")
    
    print("\n   Option 2: Run Live Recognition")
    print("   ──────────────────────────────")
    print("   Perform gestures in front of the camera")
    print("   The system will detect and classify them in real-time")
    print("   Press 'q' to quit, 's' to save frames")
    
    print("\n" + "="*70)
    
    if not recognizer.model_trained:
        print("\n⚠️  NOTE: Model is not trained yet!")
        print("   You must train the model first before running live recognition.")
        print("\n   Would you like to train the model now? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            recognizer.train_model()
            print("\n✓ Model training complete!")
        else:
            print("\nExiting without training...")
            return
    
    print("\n🎥 Starting Live Gesture Recognition...")
    print("   Press 'q' to quit the application")
    print("   Press 's' to save a frame with detected gesture")
    print("\n" + "="*70 + "\n")
    
    recognizer.run_live_recognition()


if __name__ == "__main__":
    main()
