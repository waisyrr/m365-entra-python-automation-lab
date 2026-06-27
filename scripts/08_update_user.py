import os
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

USER_UPN = "test.user01@northwinditlab6outlook.onmicrosoft.com"

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

update_data = {
    "jobTitle": "Systems Administrator II",
    "department": "IT",
    "companyName": "UWatkins IT Group",
    "officeLocation": "Chicago HQ",
    "city": "Chicago",
    "state": "Illinois",
    "country": "United States"
}

response = requests.patch(
    f"https://graph.microsoft.com/v1.0/users/{USER_UPN}",
    headers=headers,
    json=update_data
)

response.raise_for_status()

print("✅ User updated successfully!")
print("User: Test User 01")
print("New job title: Systems Administrator II")
print("New office location: Chicago HQ")