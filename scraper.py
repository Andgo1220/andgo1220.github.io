import json
import subprocess
import time
from datetime import datetime

CHANNELS = [
    "UCDNkrZUKhA2VAGu5j11AhnQ",
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
]

def get_subscriber_count(channel_id):
    url = f"https://youtube.com{channel_id}"
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--no-warnings",
        "--playlist-items", "0",  # CRUCIAL: Blocks video loops, fetches only main headers
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Pull alternative key values depending on layout variations
        subs = data.get("follower_count") or data.get("channel_follower_count")
        
        if subs:
            return str(subs)
            
        # Fallback raw metadata text parsing if json structures switch
        if "description" in data and "subscribers" in data.get("description", "").lower():
            return "Protected Data"
            
        return "Hidden"
        
    except subprocess.CalledProcessError as e:
        print(f"CLI Error for {channel_id}: {e.stderr}")
        return "Blocked by YouTube"
    except Exception as e:
        print(f"Parsing Error for {channel_id}: {e}")
        return "Parsing Error"

def main():
    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": {}
    }
    
    for cid in CHANNELS:
        print(f"Processing: {cid}...")
        output_data["channels"][cid] = get_subscriber_count(cid)
        time.sleep(2) # Extended delay to stay clear of IP limits
        
    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Export Complete.")

if __name__ == "__main__":
    main()
