import requests
import json
import os

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"

def get_last_call():
    url = "https://api.synthflow.ai/v2/calls"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}"
    }
    params = {
        "model_id": ASSISTANT_ID,
        "limit": 1
    }
    
    print(f"Fetching last call for Assistant ID: {ASSISTANT_ID}...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        calls = data.get('response', {}).get('calls', [])
        if not calls:
            print("No calls found for this assistant.")
            return None
        
        last_call = calls[0]
        call_id = last_call.get('call_id')
        transcript = last_call.get('transcript')
        
        print(f"\n--- Last Call Found ---")
        print(f"Call ID: {call_id}")
        print(f"Status: {last_call.get('call_status')}")
        print(f"Duration: {last_call.get('duration')} seconds")
        print(f"Transcript:\n{transcript}")
        return last_call
    else:
        print(f"Error fetching calls: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    get_last_call()
