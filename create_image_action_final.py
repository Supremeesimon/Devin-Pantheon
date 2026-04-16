import requests
import json
import os

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
MANUS_API_KEY = "sk-gMxOx2pvYudAzIo8E4-ubbezDtuJZMwRhxeLZi3bkHjV_SighFzxnucQ14ubH1LHxHNKzzRgnN4T4iUJ-ydtbtcUgTas"

def create_action():
    url = "https://api.synthflow.ai/v2/actions"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "CUSTOM_ACTION": {
            "name": "GET_VEHICLE_IMAGES_PROD",
            "description": "Retrieves vehicle image URLs from Devin's system for a given ad ID.",
            "http_mode": "GET",
            "url": "https://api.manus.im/v1/leads/{ad_id}/images",
            "speech_while_using_the_tool": "Let me pull up those photos for you right now...",
            "run_action_before_call_start": False,
            "headers": [
                {
                    "name": "x-manus-api-key",
                    "value": MANUS_API_KEY
                }
            ]
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        action_id = response.json().get('response', {}).get('action_id')
        print(f"Action Created Successfully! ID: {action_id}")
        return action_id
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def attach_action(assistant_id, action_id):
    url = "https://api.synthflow.ai/v2/actions/attach"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    # Fetch current actions to avoid overwriting DISPATCH_DEVIN_PROD
    get_url = f"https://api.synthflow.ai/v2/assistants/{assistant_id}"
    get_res = requests.get(get_url, headers=headers)
    current_actions = get_res.json().get('response', {}).get('assistants', [{}])[0].get('actions', [])
    
    new_actions = list(set(current_actions + [action_id]))
    payload = {"model_id": assistant_id, "actions": new_actions}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Action attached successfully!")
    else:
        print(f"Error attaching: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    aid = create_action()
    if aid:
        attach_action("0a420ae4-6d32-46b4-8c84-7f9315831736", aid)
