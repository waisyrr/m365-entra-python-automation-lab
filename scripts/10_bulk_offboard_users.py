import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

DOMAIN = "northwinditlab6outlook.onmicrosoft.com"

# Authenticate
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

df = pd.read_csv("data/offboard_users.csv")

disabled = 0

for _, row in df.iterrows():

    upn = f"{row['username']}@{DOMAIN}"

    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/users/{upn}",
        headers=headers,
        json={
            "accountEnabled": False
        }
    )

    if response.status_code == 204:
        disabled += 1
        print(f"✅ Disabled {upn}")
    else:
        print(f"❌ Failed: {upn}")
        print(response.text)

print(f"\n🎉 Successfully disabled {disabled} users.")