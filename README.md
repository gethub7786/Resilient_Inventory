# Resilient Inventory Automation

This project provides a simple example of synchronizing product inventory from the
CWR API to Amazon via the Selling Partner API (SP-API).

## Requirements

- Python 3.9+
- `requests` library
- `sp-api` library (for communicating with Amazon SP-API)

## Environment Variables

Create a `.env` file (or export in your environment) with the following
variables:

```
CWR_BASE_URL=<supplier-api-url>
CWR_API_KEY=<supplier-api-key>
AMZ_REFRESH_TOKEN=<amazon-refresh-token>
AMZ_CLIENT_ID=<amazon-client-id>
AMZ_CLIENT_SECRET=<amazon-client-secret>
AMZ_ROLE_ARN=<amazon-role-arn>
```

See the supplier documentation and Amazon SP-API documentation for details on
obtaining these values.

## Running

Install dependencies and run the sync:

```bash
python -m pip install -r requirements.txt
python main.py
```

The script downloads inventory data from CWR and submits it to Amazon. You can
schedule the script with `cron` or another scheduler to keep your inventory in
sync.
