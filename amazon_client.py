import os
from typing import List, Dict
from sp_api.base import SellingApiException
from sp_api.api import Feeds
from sp_api.base import Marketplaces


class AmazonInventoryClient:
    """Client for submitting inventory updates to Amazon SP-API."""

    def __init__(self) -> None:
        refresh_token = os.getenv("AMZ_REFRESH_TOKEN")
        client_id = os.getenv("AMZ_CLIENT_ID")
        client_secret = os.getenv("AMZ_CLIENT_SECRET")
        role_arn = os.getenv("AMZ_ROLE_ARN")
        if not all([refresh_token, client_id, client_secret, role_arn]):
            raise ValueError("Amazon SP-API credentials are not fully provided")

        self.feeds = Feeds(
            refresh_token=refresh_token,
            lwa_app_id=client_id,
            lwa_client_secret=client_secret,
            role_arn=role_arn,
            marketplace=Marketplaces.US,
        )

    def submit_inventory(self, items: List[Dict]) -> str:
        """Submit inventory update feed to Amazon."""
        # Convert items into the XML feed format required by Amazon.
        # This is a simplified example using a very small subset of the template.
        message_lines = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<AmazonEnvelope>",
            "  <Header>",
            "    <DocumentVersion>1.01</DocumentVersion>",
            "    <MerchantIdentifier>MERCHANT_ID</MerchantIdentifier>",
            "  </Header>",
            "  <MessageType>Inventory</MessageType>",
        ]
        for idx, item in enumerate(items, 1):
            sku = item["sku"]
            quantity = item["quantity"]
            message_lines += [
                f"  <Message>",
                f"    <MessageID>{idx}</MessageID>",
                f"    <OperationType>Update</OperationType>",
                f"    <Inventory>",
                f"      <SKU>{sku}</SKU>",
                f"      <Quantity>{quantity}</Quantity>",
                f"    </Inventory>",
                f"  </Message>",
            ]
        message_lines.append("</AmazonEnvelope>")
        feed_content = "\n".join(message_lines)

        try:
            result = self.feeds.submit_feed(
                feed_content,
                feed_type="POST_INVENTORY_AVAILABILITY_DATA",
            )
            return result.payload.get("feedDocumentId", "")
        except SellingApiException as exc:
            raise RuntimeError(f"Failed to submit feed: {exc}")
