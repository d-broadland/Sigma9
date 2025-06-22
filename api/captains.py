# sigma9_api.py

import requests
from typing import Any, Dict, Iterator, Optional

BASE_URL = "https://mlb25.theshow.com/apis"

class CaptainsAPI:
    def __init__(self, base_url: str = BASE_URL, session: Optional[requests.Session] = None):
        self.base = base_url.rstrip('/')
        self.s = session or requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base}/{path.lstrip('/')}"
        resp = self.s.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get(self, page: int = 1) -> Dict[str, Any]:
        """GET /apis/captains.json?page={page}"""
        return self._get("captains.json", params={"page": page})

    def getAll(self) -> Iterator[Dict[str, Any]]:
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

