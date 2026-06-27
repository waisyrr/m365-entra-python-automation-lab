import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Microsoft identity platform endpoint
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

# Request an access token
token_data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://graph.microsoft.com/.default"
}

response = requests.post(token_url, data=token_data)
response.raise_for_status()

access_token = response.json()["access_token"]
print("✅ Successfully authenticated to Microsoft Graph!")

# Test the Microsoft Graph connection
headers = {
    "Authorization": f"Bearer {access_token}"
}

graph_response = requests.get(
    "https://graph.microsoft.com/v1.0/users?$top=5",
    headers=headers
)

graph_response.raise_for_status()

print("\nFirst 5 users:\n")

for user in graph_response.json()["value"]:
    print(f"- {user['displayName']}")