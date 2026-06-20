import json
import subprocess
import time
from datetime import datetime

# 1. Define the channels you want to monitor
CHANNELS = [
    "UCDNkrZUKhA2VAGu5j11AhnQ",
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
]

def get_subscriber_count(channel_id):
    """Uses yt-dlp to safely fetch the follower/subscriber count string."""
    url = f"https://youtube.com{channel_id}"
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--no-warnings",
        url
    ]
    
    try:
        # Run yt-dlp via CLI and catch the raw json metadata payload
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # yt-dlp populates channel details inside 'channel_follower_count'
        subs = data.get("channel_follower_count")
        return str(subs) if subs else "Hidden"
        
    except Exception as e:
        print(f"Error scraping {channel_id}: {e}")
        return "Error"

def main():
    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": {}
    }
    
    for cid in CHANNELS:
        print(f"Scraping channel: {cid}...")
        output_data["channels"][cid] = get_subscriber_count(cid)
        time.sleep(1) # Brief polite pause between network calls
        
    # Overwrite your local static stats file 
    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Successfully updated stats.json!")

if __name__ == "__main__":
    main()