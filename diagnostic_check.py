import os
import requests
import json

def diagnostic():
    api_key = os.getenv("SYNTHFLOW_API_KEY")
    sarah_id = "0a420ae4-6d32-46b4-8c84-7f9315831736"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"--- Fetching Assistant Details for {sarah_id} ---")
    response = requests.get(f"https://api.synthflow.ai/v2/assistants/{sarah_id}", headers=headers)
    data = response.json()
    print(json.dumps(data, indent=2))
    
    print("\n--- Checking for all actions in account ---")
    response = requests.get(f"https://api.synthflow.ai/v2/actions", headers=headers)
    actions_data = response.json()
    print(f"Total actions in account: {len(actions_data.get('response', {}).get('actions', []))}")

if __name__ == "__main__":
    diagnostic()
