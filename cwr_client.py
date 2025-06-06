import os
from typing import List, Dict
import requests


class CWRClient:
    """Client for fetching inventory data from CWR supplier API."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = base_url or os.getenv("CWR_BASE_URL")
        self.api_key = api_key or os.getenv("CWR_API_KEY")
        if not self.base_url or not self.api_key:
            raise ValueError("CWR_BASE_URL and CWR_API_KEY must be provided")

    def get_inventory(self) -> List[Dict]:
        """Retrieve inventory from the CWR API."""
        url = f"{self.base_url}/inventory"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Expecting JSON list of items with SKU and quantity
        return data.get("items", [])
