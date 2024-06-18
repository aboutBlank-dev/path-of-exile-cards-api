import re
import os
from typing import Dict, List, Tuple, TypedDict
import requests

URL = "https://www.poewiki.net/w/api.php"
POE_LEAGUE_URL = "https://api.pathofexile.com/league"
POE_NINJA_DIV_URL = "https://poe.ninja/api/data/itemoverview?type=DivinationCard&league="
CARD_ART_URL_BASE = "https://web.poecdn.com/image/divination-card/"

class Map(TypedDict):
    id: str
    name: str
    unique: bool
    alias: str

class Card(TypedDict):
    id: str
    name: str
    drop_areas: List[str]
    stack_size: int
    reward_text: List[Dict[str, str]]
    chaos_value: float
    divine_value: float
    art_url: str
    alias: str

def to_snake_case(string: str) -> str:
    """
    Converts a string to snake case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The string in snake case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

def get_map_card_data() -> Tuple[Dict[str, Map], Dict[str, Card]]:
    """
    Fetches the current league, maps and cards from the PoE Wiki API and PoE Ninja API.

    Returns:
        Tuple[Dict[str, Map], Dict[str, Card]]: A Tuple containing a Dictionary of Maps and a Dictionary of Cards.
    """
    current_league = fetch_current_league()
    if(current_league == None):
        return {}, {}

    maps = fetch_maps(current_league)
    cards = fetch_cards(current_league, maps)

    if (len(maps) < 1 or len(cards) < 1):
        return {}, {}

    #Remove any area that has no cards
    maps = {k: v for k, v in maps.items() if "cards" in v}

    return maps, cards
    

def fetch_current_league() -> str:
    """
    Fetch current league information from the Path of Exile API.

    Returns:
        str: The current league id.
    """

    current_leagues = requests.get(
        POE_LEAGUE_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'},
        params={
            "realm": "pc",
            "type": "main",
        })

    try:
        current_leagues = current_leagues.json()
    except:
        return os.getenv("CURRENT_LEAGUE")

    for league in current_leagues:
        if "current" in league["category"]:
            return league["category"]["id"]
    
    return None

def fetch_maps(current_league: str) -> Dict[str, Map]:
    """
        Fetch Map and Area data from PoE Wiki API (cargoquery)

        Returns:
            Dict[str, Map]: A Dictionary of Maps. Where the key is the Map id and the value is a Dictionary representing the Map
    """

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
    )
    wiki_maps = wiki_maps.json()["cargoquery"]

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
    )
    wiki_areas = wiki_areas.json()["cargoquery"]

    maps = {}
    for map in wiki_maps:
        area_id = map["title"]["area id"]
        name = None

        for area in wiki_areas:
            if area["title"]["id"] == area_id:
                name = area["title"]["name"]
                break

        map_id = to_snake_case(map["title"]["area id"])

        if name:
            maps[map_id] = {
                "id": map_id,
                "name": name,
                "unique": "unique" in map_id.lower(), 
                "alias": name.lower().replace(" ", "").replace("'", "")
            }

    return maps 


def fetch_cards(current_league: str, maps: Dict[str, Map]):
    """
        Fetch Map and Area data from PoE Wiki API (cargoquery)

        Returns:
            Dict[str, Map]: A Dictionary of Maps. Where the key is the Map id and the value is a Dictionary representing the Map
    """
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
    )
    wiki_cards = wiki_cards.json()["cargoquery"]

    poe_ninja_prices = requests.get(POE_NINJA_DIV_URL + current_league).json()["lines"]
    print("URL ==== ", POE_NINJA_DIV_URL + current_league)
    print("POE NINJA PRICES ===== ", poe_ninja_prices)

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
            card_id = to_snake_case(card_art)
            drop_area_ids = card["drop areas"]

            drop_areas = []
            if drop_area_ids:
                drop_area_ids = drop_area_ids.split(",")
                for drop_area in drop_area_ids:
                    drop_area_id = to_snake_case(drop_area)
                    if drop_area_id in maps:
                        drop_areas.append(drop_area_id)
                        if "cards" not in maps[drop_area_id]:
                            maps[drop_area_id]["cards"] = []
                        maps[drop_area_id]["cards"].append(card_id)

            if len(drop_areas) < 1:
                continue

            cards[card_id] = {
               "id": card_id,
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
            new_reward_text.append({"tag": match[0], "text": match[1].replace("{", "").replace("}", "").strip()})
        
        card["reward_text"] = new_reward_text
    
    return cards
