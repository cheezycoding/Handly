"""
Download only the 14 signs we need from WLASL dataset.
"""
import json
import os
import time
import random
import urllib.request
import subprocess

# Our target signs
TARGET_SIGNS = [
    'hello', 'thank you', 'please', 'sorry', 'yes', 'no', 'bye', 
    'help', 'who', 'what', 'when', 'where', 'why', 'which', 'how'
]

def load_and_filter_json(json_path):
    """Load WLASL JSON and filter for target signs only."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    filtered = []
    for entry in data:
        if entry['gloss'].lower() in TARGET_SIGNS:
            filtered.append(entry)
    
    return filtered

def download_video(url, save_path, video_id):
    """Download a single video."""
    if os.path.exists(save_path):
        print(f"  [SKIP] {video_id} already exists")
        return True
    
    try:
        if 'youtube' in url or 'youtu.be' in url:
            # Use yt-dlp for YouTube
            cmd = f'yt-dlp -q --no-warnings -o "{save_path}" "{url}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=60)
            if result.returncode == 0:
                print(f"  [OK] {video_id} (YouTube)")
                return True
            else:
                print(f"  [FAIL] {video_id} - yt-dlp error")
                return False
        else:
            # Direct download for other URLs
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            with open(save_path, 'wb') as f:
                f.write(response.read())
            print(f"  [OK] {video_id}")
            return True
    except Exception as e:
        print(f"  [FAIL] {video_id} - {str(e)[:50]}")
        return False

def main():
    json_path = 'WLASL_v0.3.json'
    save_dir = 'data'
    
    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} not found")
        return
    
    os.makedirs(save_dir, exist_ok=True)
    
    # Filter for our signs
    filtered_data = load_and_filter_json(json_path)
    print(f"Found {len(filtered_data)} signs matching our targets")
    
    # Count total videos
    total_videos = sum(len(entry['instances']) for entry in filtered_data)
    print(f"Total videos to download: {total_videos}")
    
    # Download each sign's videos
    downloaded = 0
    failed = 0
    
    for entry in filtered_data:
        gloss = entry['gloss']
        instances = entry['instances']
        
        # Create subfolder for each sign
        sign_folder = os.path.join(save_dir, gloss.lower().replace(' ', '_'))
        os.makedirs(sign_folder, exist_ok=True)
        
        print(f"\n[{gloss.upper()}] - {len(instances)} videos -> {sign_folder}/")
        
        for inst in instances:
            video_id = inst['video_id']
            url = inst['url']
            
            # Determine file extension
            if 'youtube' in url or 'youtu.be' in url:
                ext = 'mp4'
            elif 'aslpro' in url:
                ext = 'swf'
            else:
                ext = 'mp4'
            
            save_path = os.path.join(sign_folder, f"{video_id}.{ext}")
            
            if download_video(url, save_path, video_id):
                downloaded += 1
            else:
                failed += 1
            
            # Be nice to servers
            time.sleep(random.uniform(0.5, 1.5))
    
    print(f"\n{'='*50}")
    print(f"DONE: {downloaded} downloaded, {failed} failed")
    print(f"Videos saved to: {save_dir}/<sign_name>/")

if __name__ == '__main__':
    main()

