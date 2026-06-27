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

url = "https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,department,assignedLicenses"

users = []

while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    users.extend(data.get("value", []))
    url = data.get("@odata.nextLink")

rows = []

for user in users:
    licenses = user.get("assignedLicenses", [])

    rows.append({
        "display_name": user.get("displayName"),
        "user_principal_name": user.get("userPrincipalName"),
        "department": user.get("department"),
        "license_count": len(licenses),
        "has_license": len(licenses) > 0
    })

report = pd.DataFrame(rows)

os.makedirs("outputs/reports", exist_ok=True)

output_file = "outputs/reports/license_report.csv"
report.to_csv(output_file, index=False)

print("✅ License report generated successfully!")
print(report[["display_name", "department", "license_count", "has_license"]])
print(f"\nSaved to: {output_file}")