import requests
from typing import Dict, Any, Optional, Iterator
import subprocess
import json
import shlex

BASE_URL = "https://mlb25.theshow.com/apis"

class TheShowAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base = BASE_URL
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Cookie": "tsn_toastr_position=toast-top-full-width; tsn_toastr_duration=5000; tsn_toastr_enabled=body; _ga=GA1.1.455382549.1750567255; _gcl_au=1.1.996389221.1750567255; GA1.3.455382549.1750567255; tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MjIxMzg3NSwidXNlcm5hbWUiOiJ0b3Bib3k2MTJfUFNOIiwicGljdHVyZSI6Imh0dHBzOi8vdGhlc2hvd25hdGlvbi1wcm9kdWN0aW9uLnMzLmFtYXpvbmF3cy5jb20vZm9ydW1faWNvbnMvbWxiMjUvaWNvbl9taW5fbWFzY290LndlYnAiLCJncm91cHMiOltdfQ.FBCU8tFngw38-8QTSlHwxq056afWK2x2W_EPkSOBWgw; ab.storage.userId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=%7B%22g%22%3A%2213413896%22%2C%22c%22%3A1751922788394%2C%22l%22%3A1751922788394%7D; ab.storage.deviceId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=%7B%22g%22%3A%223bed10d3-addc-c106-27d2-6963ea49a4c0%22%2C%22c%22%3A1751922788395%2C%22l%22%3A1751922788395%7D; tsn_hide_forums_tou=2; _ga_LSJREQ8593=GS2.1.s1751927728$o1$g1$t1751928333$j60$l0$h0; _tsn_session=45044597aaa6cc510551ef6dfa9c8668; tsn_last_url=Qcppt8EQj2h2pgzQph4KcowvwddPSOkK_0Fd_Gdwm-6u5250d8kXYG-rU0UMpy-PloZSdRykIDmSSRKvx8JHCongmoCCm3aucEWhjwee721BixVevjroODfwldigQjlK4xdlZIN8_xNnJJwJZB1KJ2dPTAeqWbBghl0siJK3Hvsl4U2RLsLsh-sxWV3is01JhuNmFEL3_U_6WsES1Bt7JirMftSAHoYQdmgn70Ymf3RhLZbJpyc7r1xEUB7aK4WCc7X0yxWyTTpMwfvsSWO6FjzbjbdThN8RFuyVMtzW_FGFGqOr9ewmfqqIkAaamNFz; _ga_7NX8QXLJQK=GS2.1.s1751927676$o3$g1$t1751928656$j60$l0$h0; _ga_Y01S4T0NK9=GS2.1.s1751927676$o3$g1$t1751928656$j60$l0$h0; _ga_XRJ0TD5FYX=GS2.1.s1751927540$o3$g1$t1751928656$j60$l0$h0; ab.storage.sessionId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=%7B%22g%22%3A%2272dfc84d-0062-bc47-fc79-231d1582c9d3%22%2C%22e%22%3A1751930456579%2C%22c%22%3A1751928502666%2C%22l%22%3A1751928656579%7D; _ga_EJKYYHZPBF=GS2.1.s1751927540$o3$g1$t1751928656$j60$l0$h0; _gid=GA1.3.1584679708.1751928657"
        })
        print("🔐 Using Headers:")
        for k, v in self.session.headers.items():
            print(f"{k}: {v}")

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        import shlex

        # Construct URL with params manually
        query = "&".join(f"{k}={v}" for k, v in (params or {}).items())
        url = f"https://mlb25.theshow.com/{path.lstrip('/')}"
        if query:
            url = f"{url}?{query}"

        print(f"🌀 Curl GET {url}")

        full_curl = f"""
        curl '{url}' \\
          -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \\
          -H 'accept-language: en-US,en;q=0.9' \\
          -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36' \\
          -H 'cookie: {self.session.headers["Cookie"]}' \\
          --compressed -s
        """

        result = subprocess.run(full_curl, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            raise RuntimeError(f"Curl failed: {result.stderr}")

        try:
            data = json.loads(result.stdout)
            print(f"🧾 Curl response: {data}")
            return data
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON: {result.stdout}")

    def get_inventory(self, type: str, page: int = 1) -> Dict[str, Any]:
        return self._get("inventory.json", {"type": type, "page": page})

    def iter_inventory(self, type: str) -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            data = self.get_inventory(type, page=page)
            items = data.get("inventory") or data.get("data")
            if not items:
                break
            for item in items:
                yield item
            page += 1

    def get_items(self, page: int = 1) -> Dict[str, Any]:
        return self._get("items.json", {"page": page})

    def iter_items(self) -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            data = self.get_items(page=page)
            items = data.get("items") or data.get("data")
            if not items:
                break
            for item in items:
                yield item
            page += 1