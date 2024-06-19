import time
from supabase import Client

from retrieve_map_card_data import get_map_card_data

class DataCache:
    def __init__(self, db: Client):
        self._cards = {}
        self._maps = {}

        self._dataValidationTimeS = 60 * 60 * 24 # 1 day in seconds (24 hours)
        self._lastFetchTime = 0
        self._db = db
    
    def get_all_cards(self):
        self.fetch_data_if_needed()

        if len(self._cards) > 0:
            return self._cards.values()
        return None

    def get_cards(self, ids):
        self.fetch_data_if_needed()

        cards = []
        for id in ids:
            if id in self._cards:
                cards.append(self._cards[id])
        return cards

    def get_card_id(self, id):
        self.fetch_data_if_needed()

        if id in self._cards:
            return self._cards[id]
        return None

    def get_all_maps(self):
        self.fetch_data_if_needed()

        if len(self._maps) > 0:
            return self._maps.values()
        return None
    
    def get_maps(self, ids):
        self.fetch_data_if_needed()

        maps = []
        for id in ids:
            if id in self._maps:
                maps.append(self._maps[id])
        return maps

    def get_map_id(self, id):
        self.fetch_data_if_needed()

        if id in self._maps:
            return self._maps[id]
        return None 

    def fetch_data_if_needed(self) -> None:
        if time.time() - self._lastFetchTime < self._dataValidationTimeS:
            return

        # Fetch the data from the external APIs
        maps, cards = get_map_card_data()

        if maps and len(maps) > 0:
            self._maps = maps

            # Update the data in the database
            maps_list = list(maps.values())
            self._db.table("maps").upsert(maps_list).execute()
        else:
            # Fetch the data from the database
            maps = self._db.table("maps").select("*").execute()
            if maps and len(maps.data) > 0:
                self._maps = maps

        if cards and len(cards) > 0:
            self._cards = cards

            # Update the data in the database
            cards_list = list(cards.values())
            self._db.table("cards").upsert(cards_list).execute()
        else:
            # Fetch the data from the database
            cards = self._db.table("cards").select("*").execute()
            if cards and len(cards.data) > 0:
                self._cards = cards
        

        self._lastFetchTime = time.time()