import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

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
    "Authorization": f"Bearer {access_token}"
}

url = "https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,jobTitle,department,companyName,officeLocation,accountEnabled"

users = []

while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    users.extend(data.get("value", []))
    url = data.get("@odata.nextLink")

df = pd.DataFrame(users)

os.makedirs("outputs", exist_ok=True)

output_file = "outputs/users_inventory.csv"
df.to_csv(output_file, index=False)

print(f"✅ Exported {len(df)} users to {output_file}")