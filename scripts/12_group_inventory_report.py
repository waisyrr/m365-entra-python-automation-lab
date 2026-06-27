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

groups_url = "https://graph.microsoft.com/v1.0/groups?$select=id,displayName,description,securityEnabled,mailEnabled"

groups = []

while groups_url:
    response = requests.get(groups_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    groups.extend(data.get("value", []))
    groups_url = data.get("@odata.nextLink")

report_rows = []

for group in groups:
    group_id = group["id"]
    members_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=id,displayName,userPrincipalName"

    members = []

    while members_url:
        response = requests.get(members_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        members.extend(data.get("value", []))
        members_url = data.get("@odata.nextLink")

    member_names = [member.get("displayName", "Unknown") for member in members]

    report_rows.append({
        "group_name": group.get("displayName"),
        "description": group.get("description"),
        "security_enabled": group.get("securityEnabled"),
        "mail_enabled": group.get("mailEnabled"),
        "member_count": len(members),
        "members": "; ".join(member_names)
    })

report = pd.DataFrame(report_rows)

os.makedirs("outputs/reports", exist_ok=True)

output_file = "outputs/reports/group_inventory_report.csv"
report.to_csv(output_file, index=False)

print("✅ Group inventory report generated successfully!")
print(report[["group_name", "member_count"]])
print(f"\nSaved to: {output_file}")