import os
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

DOMAIN = "northwinditlab6outlook.onmicrosoft.com"

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

new_user = {
    "accountEnabled": True,
    "displayName": "Test User 01",
    "mailNickname": "test.user01",
    "userPrincipalName": f"test.user01@{DOMAIN}",
    "passwordProfile": {
        "forceChangePasswordNextSignIn": True,
        "password": "TempPassword123!"
    },
    "givenName": "Test",
    "surname": "User01",
    "jobTitle": "Test Automation User",
    "department": "IT",
    "companyName": "UWatkins IT Group",
    "officeLocation": "Manhattan HQ",
    "city": "New York",
    "state": "New York",
    "country": "United States"
}

response = requests.post(
    "https://graph.microsoft.com/v1.0/users",
    headers=headers,
    json=new_user
)

response.raise_for_status()

created_user = response.json()

print("✅ User created successfully!")
print(f"Display name: {created_user['displayName']}")
print(f"User principal name: {created_user['userPrincipalName']}")