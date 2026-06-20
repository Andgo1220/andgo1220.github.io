import json
import re
import requests
from datetime import datetime

CHANNELS = [
    "UCDNkrZUKhA2VAGu5j11AhnQ",
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
]

def get_subscriber_count_mobile(channel_id):
    # Using m.youtube.com forces YouTube to load the high-trust mobile web app layout
    url = f"https://youtube.com{channel_id}"
    
    # Emulate an iOS Mobile Safari fingerprint perfectly
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 404:
            return "Channel Not Found"
        response.raise_for_status()
        
        html_content = response.text
        
        # Search the raw mobile page configuration object for subscriber details
        match = re.search(r'"subscriberCountText"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"\s*\}', html_content)
        
        if match:
            return match.group(1)
            
        # Alternative fallback pattern search used on some mobile layout distributions
        fallback_match = re.search(r'"accessibilityData"\s*:\s*\{\s*"label"\s*:\s*"([^"]+subscribers[^"]*)"\s*\}', html_content)
        if fallback_match:
            # Cleans up long labels like "1.42 million subscribers"
            return fallback_match.group(1)

        return "Hidden/Private"
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "Rate Limited"
        return f"HTTP Error {e.response.status_code}"
    except Exception as e:
        return "Extraction Error"

def main():
    print("Initiating Mobile Header Scraping Cycle...")
    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": {}
    }
    
    for cid in CHANNELS:
        print(f"Scraping {cid}...")
        output_data["channels"][cid] = get_subscriber_count_mobile(cid)
        
    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
        
    print("Workflow Complete. Output saved to stats.json")

if __name__ == "__main__":
    main()