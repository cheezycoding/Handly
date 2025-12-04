"""
Retry downloading only for signs with less than 10 videos.
"""
import json
import os
import time
import random
import urllib.request
import subprocess

# Signs that need more videos (less than 10)
SIGNS_NEED_MORE = ['hello', 'bye', 'which', 'sorry', 'thank you', 'where', 'please', 'when', 'how']

def load_and_filter_json(json_path):
    """Load WLASL JSON and filter for signs that need more videos."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    filtered = []
    for entry in data:
        if entry['gloss'].lower() in SIGNS_NEED_MORE:
            filtered.append(entry)
    
    return filtered

def download_video(url, save_path, video_id):
    """Download a single video."""
    if os.path.exists(save_path):
        return "skip"
    
    try:
        if 'youtube' in url or 'youtu.be' in url:
            # Use yt-dlp for YouTube with more retries
            cmd = f'yt-dlp -q --no-warnings --retries 3 -o "{save_path}" "{url}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=90)
            if result.returncode == 0 and os.path.exists(save_path):
                return "ok"
            else:
                return "fail"
        else:
            # Direct download for other URLs
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=45)
            with open(save_path, 'wb') as f:
                f.write(response.read())
            return "ok"
    except Exception as e:
        return "fail"

def get_current_count(sign_folder):
    """Get current video count for a sign."""
    if os.path.exists(sign_folder):
        return len([f for f in os.listdir(sign_folder) if f.endswith('.mp4')])
    return 0

def main():
    json_path = 'WLASL_v0.3.json'
    save_dir = 'data'
    target_min = 10
    
    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} not found")
        return
    
    # Filter for signs that need more
    filtered_data = load_and_filter_json(json_path)
    print(f"Retrying downloads for {len(filtered_data)} signs that need more videos\n")
    
    total_new = 0
    
    for entry in filtered_data:
        gloss = entry['gloss']
        instances = entry['instances']
        
        # Create subfolder for each sign
        sign_folder = os.path.join(save_dir, gloss.lower().replace(' ', '_'))
        os.makedirs(sign_folder, exist_ok=True)
        
        current_count = get_current_count(sign_folder)
        needed = target_min - current_count
        
        if needed <= 0:
            print(f"[{gloss.upper()}] Already has {current_count} videos, skipping")
            continue
        
        print(f"[{gloss.upper()}] Has {current_count}, needs {needed} more")
        
        new_downloads = 0
        for inst in instances:
            if new_downloads >= needed:
                break
                
            video_id = inst['video_id']
            url = inst['url']
            
            # Determine file extension
            ext = 'mp4'
            save_path = os.path.join(sign_folder, f"{video_id}.{ext}")
            
            result = download_video(url, save_path, video_id)
            
            if result == "ok":
                print(f"  [NEW] {video_id}")
                new_downloads += 1
                total_new += 1
            elif result == "skip":
                pass  # Already exists
            else:
                print(f"  [FAIL] {video_id}")
            
            # Be nice to servers
            time.sleep(random.uniform(0.8, 2.0))
        
        final_count = get_current_count(sign_folder)
        print(f"  -> Now has {final_count} videos\n")
    
    print(f"{'='*50}")
    print(f"DONE: {total_new} new videos downloaded")
    
    # Final summary
    print(f"\nFinal counts:")
    for sign in SIGNS_NEED_MORE:
        folder = os.path.join(save_dir, sign.replace(' ', '_'))
        count = get_current_count(folder)
        status = "✓" if count >= 10 else "✗"
        print(f"  {status} {sign}: {count}")

if __name__ == '__main__':
    main()

