import os
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Get access token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

token_data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://graph.microsoft.com/.default"
}

token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()

access_token = token_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Find Test User 01
upn = "test.user01@northwinditlab6outlook.onmicrosoft.com"

response = requests.get(
    f"https://graph.microsoft.com/v1.0/users/{upn}",
    headers=headers
)

response.raise_for_status()

user = response.json()
user_id = user["id"]

# Disable the account
disable_data = {
    "accountEnabled": False
}

response = requests.patch(
    f"https://graph.microsoft.com/v1.0/users/{user_id}",
    headers=headers,
    json=disable_data
)

response.raise_for_status()

print("✅ User disabled successfully!")
print(f"Display name: {user['displayName']}")
print(f"User principal name: {user['userPrincipalName']}")