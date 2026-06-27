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

df = pd.read_csv("data/new_users.csv")

created = 0

for _, row in df.iterrows():

    upn = f"{row['username']}@{DOMAIN}"

    user = {
        "accountEnabled": True,
        "displayName": f"{row['first_name']} {row['last_name']}",
        "mailNickname": row["username"],
        "userPrincipalName": upn,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": "TempPassword123!"
        },
        "givenName": row["first_name"],
        "surname": row["last_name"],
        "jobTitle": row["job_title"],
        "department": row["department"],
        "employeeId": row["employee_id"],
        "officeLocation": row["office_location"],
        "city": row["city"],
        "state": row["state"],
        "country": row["country"]
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/users",
        headers=headers,
        json=user
    )

    if response.status_code == 201:
        created += 1
        print(f"✅ Created {user['displayName']}")
    else:
        print(f"❌ Failed: {user['displayName']}")
        print(response.text)

print(f"\n🎉 Successfully created {created} users.")