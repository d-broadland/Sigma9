# sigma9_api.py

import requests
from typing import Any, Dict, Iterator, Optional

BASE_URL = "https://mlb25.theshow.com/apis"

class TheShowAPI:
    def __init__(self, base_url: str = BASE_URL, session: Optional[requests.Session] = None):
        self.base = base_url.rstrip('/')
        self.s = session or requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base}/{path.lstrip('/')}"
        resp = self.s.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_captains(self, page: int = 1) -> Dict[str, Any]:
        """GET /apis/captains.json?page={page}"""
        return self._get("captains.json", params={"page": page})

    def iter_captains(self) -> Iterator[Dict[str, Any]]:
        """Generator: yields each captains page."""
        page = 1
        while True:
            data = self.get_captains(page=page)
            items = data.get("captains") or data.get("data")
            if not items:
                break
            yield from items
            if not data.get("next_page"):
                break
            page += 1

    def get_game_log(self, game_id: str) -> Dict[str, Any]:
        """GET /apis/game_log.json?id={game_id}"""
        return self._get("game_log.json", params={"id": game_id})

    def get_roster_updates(self, id: Optional[int] = None) -> Dict[str, Any]:
        """GET /apis/roster_update.json or ?id={id}"""
        params = {"id": id} if id else {}
        return self._get("roster_update.json", params=params)

    def get_items(self, type: Optional[str] = None, page: int = 1) -> Dict[str, Any]:
        """GET /apis/items.json?type={type}&page={page}"""
        params = {}
        if type:
            params["type"] = type
        params["page"] = page
        return self._get("items.json", params=params)

    def iter_items(self, type: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        """Generator over all items (optionally by type)."""
        page = 1
        while True:
            data = self.get_items(type=type, page=page)
            items = data.get("items") or data.get("data")
            if not items:
                break
            yield from items
            if not data.get("next_page"):
                break
            page += 1

    def get_item(self, item_id: str) -> Dict[str, Any]:
        """GET /apis/item.json?id={item_id}"""
        return self._get("item.json", params={"id": item_id})

    def get_listings(self, type: Optional[str] = None, page: int = 1) -> Dict[str, Any]:
        """GET /apis/listings.json?type={type}&page={page}"""
        params = {}
        if type:
            params["type"] = type
        params["page"] = page
        return self._get("listings.json", params=params)

    def iter_listings(self, type: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            data = self.get_listings(type=type, page=page)
            items = data.get("listings") or data.get("data")
            if not items:
                break
            yield from items
            if not data.get("next_page"):
                break
            page += 1

    def get_inventory(self, type: str, page: int = 1) -> Dict[str, Any]:
        """GET /apis/inventory.json?type={type}&page={page}"""
        return self._get("inventory.json", params={"type": type, "page": page})

    def iter_inventory(self, type: str) -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            data = self.get_inventory(type=type, page=page)
            items = data.get("inventory") or data.get("data")
            if not items:
                break
            yield from items
            if not data.get("next_page"):
                break
            page += 1

    def get_meta_data(self) -> Dict[str, Any]:
        """GET /apis/meta_data.json"""
        return self._get("meta_data.json")