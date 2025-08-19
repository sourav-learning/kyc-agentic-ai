import json
import requests
import os

API_HOST = os.environ.get("ACCOUNT_API_HOST", "localhost")
API_PORT = os.environ.get("ACCOUNT_API_PORT", "8000")

def create_account(details):
    """
    Calls the REST API to create a new account with the given details.
    Returns the API response.
    """
    try:
        api_url = f"http://{API_HOST}:{API_PORT}/create_account"
        response = requests.post(api_url, json=details)
        return response.json()
    except Exception as e:
        return {"status": "failed", "reason": str(e)}
