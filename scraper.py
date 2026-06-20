import os
import json
import requests
from datetime import datetime

# Define your target YouTube Channel IDs here
CHANNELS = [
    "UCDNkrZUKhA2VAGu5j11AhnQ",
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
]

def main():
    # Safely extracts the hidden encrypted credential key from the runner environment
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Configuration Error: YOUTUBE_API_KEY Environment Variable is missing.")
        return

    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": {}
    }

    # YouTube permits a maximum of 50 channel IDs per single web request payload
    chunk_size = 50
    for i in range(0, len(CHANNELS), chunk_size):
        chunk = CHANNELS[i:i + chunk_size]
        ids_str = ",".join(chunk)
        
        url = f"https://googleapis.com{ids_str}&key={api_key}"
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Map the parsed numerical results to the output object
            for item in data.get("items", []):
                cid = item.get("id")
                stats = item.get("statistics", {})
                output_data["channels"][cid] = stats.get("subscriberCount", "Hidden")
                
            # Handle channels that were not returned (e.g. deleted or invalid IDs)
            for cid in chunk:
                if cid not in output_data["channels"]:
                    output_data["channels"][cid] = "Not Found"
                    
        except Exception as e:
            print(f"Network error processing chunk index {i}: {e}")
            for cid in chunk:
                output_data["channels"][cid] = "API Connection Error"

    # Write data file directly back into the repository environment workspace
    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Updates written successfully to stats.json!")

if __name__ == "__main__":
    main()