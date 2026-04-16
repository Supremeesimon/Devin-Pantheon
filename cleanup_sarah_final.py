import requests
import json

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"
PROD_ACTIONS = [
    "03c34552-662f-402d-ba59-92b72f3270fd", # DISPATCH_DEVIN_PROD
    "a8e7bdd9-fd79-42b1-8826-730c439abcbf"  # GET_VEHICLE_IMAGES_PROD
]

def cleanup():
    url = "https://api.synthflow.ai/v2/actions/attach"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Force set only the production actions
    payload = {"model_id": ASSISTANT_ID, "actions": PROD_ACTIONS}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Cleanup successful! Sarah now has exactly 2 production actions.")
    else:
        print(f"Error during cleanup: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    cleanup()
