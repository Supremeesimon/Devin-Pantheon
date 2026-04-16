import requests
import json

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"
# The IDs we just created and verified
PROD_ACTIONS = ["3c061019-1598-41c7-b1f0-203ea56e06e6", "a69ed132-7bfb-4395-9aca-d12dd756df39"]

def cleanup():
    url = "https://api.synthflow.ai/v2/actions/attach"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {"model_id": ASSISTANT_ID, "actions": PROD_ACTIONS}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Sarah's actions cleaned up successfully!")
        print(f"Current Actions: {PROD_ACTIONS}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    cleanup()
