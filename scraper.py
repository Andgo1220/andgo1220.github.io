import json
import re
import requests
from datetime import datetime

CHANNELS = [
    "UCDNkrZUKhA2VAGu5j11AhnQ",
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
]

def get_subscriber_count_modern(channel_id):
    # Fetch from desktop channel endpoint to access the canonical ytInitialData layout
    url = f"https://youtube.com{channel_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return f"HTTP {response.status_code}"
            
        html = response.text
        
        # 1. Isolate the internal JSON configuration block from YouTube
        json_extract = re.search(r'var ytInitialData\s*=\s*(\{.*?\});\s*</script>', html)
        
        if json_extract:
            raw_json = json_extract.group(1)
            
            # 2. Extract the count text from the isolated string block using a targeted regex
            sub_match = re.search(r'"subscriberCountText"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"\s*\}', raw_json)
            if sub_match:
                return sub_match.group(1)
                
            # Alternative layout structural match fallback
            alt_match = re.search(r'"label"\s*:\s*"([^"]+subscribers)"', raw_json)
            if alt_match:
                return alt_match.group(1)

        # 3. Last resort layout parsing: search the global document body text directly
        body_match = re.search(r'"([^"]+subscribers)"', html)
        if body_match:
            return body_match.group(1)
            
        return "Not Extracted"
        
    except Exception as e:
        return f"Error: {str(e)[:20]}"

def main():
    print("Executing structural string matching pipeline...")
    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": {}
    }
    
    for cid in CHANNELS:
        print(f"Parsing data fields for: {cid}")
        output_data["channels"][cid] = get_subscriber_count_modern(cid)
        
    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Processing sequence complete.")

if __name__ == "__main__":
    main()
