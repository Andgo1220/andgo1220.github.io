import os
import json
import googleapiclient.discovery
from datetime import datetime, timezone

api_key = os.environ["YOUTUBE_API_KEY"]
api_service_name = "youtube"
api_version = "v3"

CHANNELS = [
    "@gdcolon",
    "@andgo122",
    "@robtopgames",
    "@itszedargd",
    "@itzbran",
    "@zedardash",
    "@guitarherostyles",
    "@speedroute",
    "@stivenelvro",
    "@nexusgd10",
    "@glowstgd",
    "@habaneroagd",
    "@partitionsion",
    "@kaiguygd",
    "@chiefbrioso",
    "@mulpan",
    "@galluxi",
    "@xtrapnation",
    "@dashzedar",
    "@ciroxp",
    "@hbargd",
    "@hbargdclips",
    "@bitesterxbeast"
]

def main():
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    
    output_data = {
        "lastUpdated": None,
        "Channels": {

        }
    }
    
    for channel in CHANNELS:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forHandle=channel
        )
        response = request.execute()
        sub_count = response['items'][0]['statistics']['subscriberCount']
        display_name = response['items'][0]['snippet']['title']
        output_data["Channels"][display_name] = [
                sub_count,
                channel
            ]
    
    timestamp = datetime.now(timezone.utc).timestamp()
    output_data["lastUpdated"] = timestamp

    print(output_data)

    with open("stats.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Updates written successfully to stats.json!")

if __name__ == "__main__":
    main()
