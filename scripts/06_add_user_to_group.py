import os
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

USER_UPN = "test.user01@northwinditlab6outlook.onmicrosoft.com"
GROUP_NAME = "SG-DEPT-IT"

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

# Get user
user_response = requests.get(
    f"https://graph.microsoft.com/v1.0/users/{USER_UPN}",
    headers=headers
)
user_response.raise_for_status()
user = user_response.json()

# Get group
group_response = requests.get(
    f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{GROUP_NAME}'",
    headers=headers
)
group_response.raise_for_status()

groups = group_response.json()["value"]

if not groups:
    raise Exception(f"Group not found: {GROUP_NAME}")

group = groups[0]

# Add user to group
add_member_url = f"https://graph.microsoft.com/v1.0/groups/{group['id']}/members/$ref"

member_data = {
    "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user['id']}"
}

add_response = requests.post(
    add_member_url,
    headers=headers,
    json=member_data
)

if add_response.status_code == 400 and "added object references already exist" in add_response.text:
    print("ℹ️ User is already a member of the group.")
else:
    add_response.raise_for_status()
    print("✅ User added to group successfully!")

print(f"User: {user['displayName']}")
print(f"Group: {group['displayName']}")