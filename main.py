"""Synchronize inventory from CWR to Amazon."""
from typing import List, Dict
from cwr_client import CWRClient
from amazon_client import AmazonInventoryClient


def sync_inventory() -> None:
    cwr = CWRClient()
    amazon = AmazonInventoryClient()

    items: List[Dict] = cwr.get_inventory()
    if not items:
        print("No inventory retrieved from CWR")
        return

    feed_id = amazon.submit_inventory(items)
    print(f"Submitted inventory feed: {feed_id}")


if __name__ == "__main__":
    sync_inventory()
