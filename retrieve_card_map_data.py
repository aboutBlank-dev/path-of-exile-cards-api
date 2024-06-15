import re
from typing import Tuple
import requests

URL = "https://www.poewiki.net/w/api.php"
POE_LEAGUE_URL = "https://api.pathofexile.com/leagues"
POE_NINJA_DIV_URL = "https://poe.ninja/api/data/itemoverview?type=DivinationCard&league="
CARD_ART_URL_BASE = "https://web.poecdn.com/image/divination-card/"

'''
Get all divination cards and their drop areas from the wiki and poe.ninja
'''
def get_card_map_data() -> Tuple[dict, dict]:
    current_leagues = requests.get(
        POE_LEAGUE_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'},
        params={
            "realm": "pc",
            "type": "main",
        }).json()

    current_league = ""
    for league in current_leagues:
        if "current" in league["category"]:
            current_league = league["category"]["id"]
            break

    wiki_maps = requests.get(
        URL,
        params={
            "action": "cargoquery",
            "format": "json",
            "limit": "500",
            "tables": "maps",
            "fields": "maps.area_id",
            "where": f"maps.series='{current_league}' AND maps.guild_character NOT LIKE '' AND maps.area_id NOT LIKE '%Synthesised%' AND maps.tier<=16",
        },
    ).json()["cargoquery"]

    wiki_areas = requests.get(
        URL,
        params={
            "action": "cargoquery",
            "format": "json",
            "limit": "500",
            "tables": "areas",
            "fields": "areas.name, areas.id",
            "where": "areas.id LIKE 'MapWorlds%' AND areas.is_legacy_map_area=false AND (areas.is_unique_map_area=true OR areas.is_map_area=true)",
        },
    ).json()["cargoquery"]

    maps = {}
    for map in wiki_maps:
        id = map["title"]["area id"]
        name = None
        for area in wiki_areas:
            if area["title"]["id"] == id:
                name = area["title"]["name"]
                break

        if name:
            maps[id] = {
                "id": id,
                "name": name,
                "unique": "unique" in id.lower(), 
                "alias": name.lower().replace(" ", "").replace("'", "")
            }

    wiki_cards = requests.get(
        URL,
        params={
            "action": "cargoquery",
            "format": "json",
            "limit": "500",
            "tables": "items",
            "fields": "items.name, items.drop_areas, items.drop_text",
            "where": f'items.class_id="DivinationCard" AND items.drop_enabled="1"',
        },
    ).json()["cargoquery"]

    poe_ninja_prices = requests.get(POE_NINJA_DIV_URL + current_league).json()["lines"]

    cards = {}
    for card in wiki_cards:
        card = card["title"]
        name = card["name"]

        #Unfortunately, the poe wiki doesn't have an id for div cards OR an image url, so we have to get it from somewhere else.
        ninja_card = None
        for item in poe_ninja_prices:
            if item["name"] == name:
                ninja_card = item
                break
        
        if ninja_card:
            card_art = ninja_card["artFilename"] #Use this as ID
            drop_area_ids = card["drop areas"]
            drop_areas = []

            if drop_area_ids:
                drop_area_ids = drop_area_ids.split(",")
                for drop_area in drop_area_ids:
                    drop_area_id = drop_area.strip()
                    if drop_area_id in maps:
                        drop_areas.append(drop_area_id)
                        if "cards" not in maps[drop_area_id]:
                            maps[drop_area_id]["cards"] = []
                        maps[drop_area_id]["cards"].append(card_art)

            if len(drop_areas) < 1:
                continue

            cards[card_art] = {
               "id": card_art,
               "name": name,
               "drop_areas": drop_areas, 
               "stack_size": ninja_card["stackSize"] if "stackSize" in ninja_card else 1,
               "reward_text": ninja_card["explicitModifiers"] if "explicitModifiers" in ninja_card else [],
               "chaos_value": ninja_card["chaosValue"] if "chaosValue" in ninja_card else 0,
               "divine_value": ninja_card["divineValue"] if "divineValue" in ninja_card else 0,
               "art_url": CARD_ART_URL_BASE + card_art + ".png",
               "alias": name.lower().replace(" ", "").replace("'", "")
            } 


    #Remove unwanted <size> tags (they come from poe.ninja)
    for card in cards.values():
        reward_text = card["reward_text"][0]
        new_reward_text = []

        #remove all <size:xx> tags
        reward_text["text"] = re.sub(r'<size:\d+>', '', reward_text["text"])

        #find all <tag>{content} and turn it into a list of tuples with tag and content
        matches = re.findall(r'<(\w+)>([^<]+)', reward_text["text"])
        for match in matches:
            new_reward_text.append({"tag": match[0], "text": match[1].replace("{", "").replace("}", "")})
        
        card["reward_text"] = new_reward_text

    #Remove any area that has no cards
    maps = {k: v for k, v in maps.items() if "cards" in v}

    return maps, cards
    
    