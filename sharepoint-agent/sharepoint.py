import os
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
TENANT_ID = os.getenv("MICROSOFT_TENANT_ID")

GRAPH_SCOPE = [
    "https://graph.microsoft.com/.default"
]


def get_access_token():
    if not CLIENT_ID:
        raise ValueError("MICROSOFT_CLIENT_ID is missing from .env")

    if not CLIENT_SECRET:
        raise ValueError("MICROSOFT_CLIENT_SECRET is missing from .env")

    if not TENANT_ID:
        raise ValueError("MICROSOFT_TENANT_ID is missing from .env")

    authority = f"https://login.microsoftonline.com/{TENANT_ID}"

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(
        scopes=GRAPH_SCOPE
    )

    if "access_token" not in result:
        raise Exception(
            result.get(
                "error_description",
                "Microsoft authentication failed"
            )
        )

    return result["access_token"]


def graph_get(endpoint):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(
        endpoint,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def get_sharepoint_sites():
    endpoint = "https://graph.microsoft.com/v1.0/sites?search=*"

    return graph_get(endpoint)