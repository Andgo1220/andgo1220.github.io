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
    "@bitesterxbeast",
    "@lemoncak3",
    "@beanable",
    "@ericvanwilderman",
    "@dorami",
    "@mikhagd",
    "@itzsquidygd",
    "@titanchannel",
    "@kingsammelot",
    "@dasher...",
    "@Нелис",
    "@vortrox",
    "@deluxe12",
    "@imfernandouwu",
    "@decody",
    "@accretiongd",
    "@neiro1999",
    "@zoink",
    "@junipergd",
    "@maffaka",
    "@dolphygeometrydash",
    "@2.2",
    "@srguillester",
    "@moldygd",
    "@simonisbestgd",
    "@leneuinst",
    "@rockyjones",
    "@mrtopi",
    "@staggy_01",
    "@spu7nix",
    "@viprin",
    "@doggiedasher",
    "@bycraftxx",
    "@crazybogdashgames",
    "@worldgameimpossiblechallenges",
    "@soulstrkgd",
    "@xcreatorgoal",
    "@sdslayer100",
    "@sikky",
    "@npesta",
    "@riottt",
    "@mrhappyjunior",
    "@toshdeluxe",
    "@knobbelboy",
    "@geck",
    "@very_big_head8845",
    "@michigun", # /\/\/\
    "@dsanimations",
    "@peterbrayhamgd",
    "@stacksoriginals",
    "@jhostyn25",
    "@tridegd",
    "@letsplaygeometrydash",
    "@fnm04",
    "@flubgeometrydash",
    "@waboo",
    "@krmal",
    "@kriszgd",
    "@icedcave",
    "@aeonair",
    "@sunixl",
    "@rektorgd",
    "@wulzy",
    "@musicsoundsgd",
    "@sirkaelgd",
    "@relz",
    "@liaxlogagd",
    "@boffisgd",
    "@how-d",
    "@voxicat",
    "@razing717",
    "@nk7338",
    "@matmart",
    "@vortroxtwo",
    "@aliasgd",
    "@trickgmd",
    "@stalliongd",
    "@squishyman67",
    "@cursed6125",
    "@freshlakewater",
    "@thehypno1208",
    "@chriscredible",
    "@johnathangd",
    "@zobrosgd",
    "@lands1ide",
    "@secretwaygd",
    "@mindcap.",
    "@swagroute0",
    "@justagdplayer",
    "@adyagd",
    "@technicaljl",
    "@kingsammelive",
    "@vernamgd",
    "@vernamica",
    "@italianapkdownloader",
    "@selpix",
    "@cobgd",
    "@coolpizzamanstuff",
    "@vix50x",
    "@dailydosegd",
    "@samifyingvods",
    "@samifying",
    "@mrlufegamertm",
    "@dima_gd_2",
    "@bli_gd",
    "@lopsidedchickengd",
    "@andromeda7674",
    "@algo.00",
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
    with open(f"sub_stats_archive/{timestamp}.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("Updates written successfully to stats.json!")

if __name__ == "__main__":
    main()
