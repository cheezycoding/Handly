"""
Download one video per word for demo purposes
"""
import json
import urllib.request
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

# 12 words from the original list
WORDS = ['hello', 'bye', 'yes', 'no', 'help', 'please', 'sorry', 'who', 'what', 'where', 'why', 'how']

OUTPUT_DIR = 'demo_videos'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load WLASL
with open('WLASL_v0.3.json', 'r') as f:
    wlasl = json.load(f)

print("Downloading one video per word...")
print("=" * 40)

for entry in wlasl:
    gloss = entry['gloss'].lower()
    
    if gloss in WORDS:
        # Find first non-YouTube URL
        for inst in entry['instances']:
            url = inst.get('url', '')
            
            # Skip YouTube (often broken)
            if not url or 'youtube' in url.lower():
                continue
            
            out_path = f'{OUTPUT_DIR}/{gloss}.mp4'
            
            if os.path.exists(out_path):
                print(f"✓ {gloss}.mp4 (already exists)")
                break
            
            try:
                urllib.request.urlretrieve(url, out_path)
                print(f"✓ {gloss}.mp4")
                break
            except Exception as e:
                continue
        else:
            print(f"✗ {gloss} - no working URL found")

print("=" * 40)
print(f"\nVideos saved to: {OUTPUT_DIR}/")

# List what we got
files = os.listdir(OUTPUT_DIR)
print(f"Downloaded: {len(files)} videos")
for f in sorted(files):
    print(f"  - {f}")

