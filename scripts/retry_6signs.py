"""
Retry downloading missing non-YouTube videos for the 6 target signs.
"""
import json
import os
import time
import random
import urllib.request

TARGET_SIGNS = ['who', 'help', 'yes', 'what', 'no', 'why']
DATA_DIR = 'data'

def download_video(url, save_path, video_id):
    """Download a single video with better error handling."""
    if os.path.exists(save_path):
        return "skip"
    
    # Skip YouTube - they're all dead
    if 'youtube' in url or 'youtu.be' in url:
        return "skip_yt"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'video/mp4,video/*,*/*',
        }
        
        # Handle ASLPro specially
        if 'aslpro' in url:
            headers['Referer'] = 'http://www.aslpro.com/cgi-bin/aslpro/aslpro.cgi'
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=60)
        
        with open(save_path, 'wb') as f:
            f.write(response.read())
        
        # Verify file is not empty/corrupted
        if os.path.getsize(save_path) < 1000:
            os.remove(save_path)
            return "fail"
        
        return "ok"
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        return f"fail: {str(e)[:40]}"

def main():
    with open('WLASL_v0.3.json') as f:
        data = json.load(f)
    
    print("Retrying missing videos for 6 target signs (non-YouTube only)\n")
    
    total_new = 0
    total_failed = 0
    
    for entry in data:
        if entry['gloss'].lower() not in TARGET_SIGNS:
            continue
        
        sign = entry['gloss'].lower()
        sign_dir = os.path.join(DATA_DIR, sign)
        
        downloaded = set(f.replace('.mp4','').replace('.swf','') for f in os.listdir(sign_dir))
        missing = [inst for inst in entry['instances'] if inst['video_id'] not in downloaded]
        non_yt_missing = [inst for inst in missing if 'youtube' not in inst['url'] and 'youtu.be' not in inst['url']]
        
        if not non_yt_missing:
            print(f"[{sign}] No missing non-YouTube videos")
            continue
        
        print(f"[{sign}] Retrying {len(non_yt_missing)} missing videos...")
        
        for inst in non_yt_missing:
            video_id = inst['video_id']
            url = inst['url']
            save_path = os.path.join(sign_dir, f"{video_id}.mp4")
            
            result = download_video(url, save_path, video_id)
            
            if result == "ok":
                print(f"  [NEW] {video_id}")
                total_new += 1
            elif result == "skip":
                pass
            elif result == "skip_yt":
                pass
            else:
                print(f"  [FAIL] {video_id} - {result}")
                total_failed += 1
            
            time.sleep(random.uniform(1.0, 2.0))
    
    print(f"\n{'='*50}")
    print(f"New downloads: {total_new}")
    print(f"Failed: {total_failed}")
    
    print(f"\nFinal counts:")
    for sign in TARGET_SIGNS:
        count = len([f for f in os.listdir(os.path.join(DATA_DIR, sign)) if f.endswith('.mp4')])
        print(f"  {sign}: {count}")

if __name__ == '__main__':
    main()

