import os
import json
import requests
from datetime import datetime

# Load credentials
CREDENTIALS_PATH = "/home/ubuntu/devin-pantheon/config/credentials.json"
with open(CREDENTIALS_PATH, 'r') as f:
    credentials = json.load(f)

SYNTHFLOW_API_KEY = credentials.get("SYNTHFLOW_API_KEY")
MANUS_API_KEY = credentials.get("MANUS_API_KEY")
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def fix_dispatch_action():
    """Update the DISPATCH_DEVIN action with correct headers and dynamic payload."""
    url = "https://api.synthflow.ai/v2/actions"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # We'll create a NEW action with the correct configuration
    action_payload = {
        "CUSTOM_ACTION": {
            "name": "dispatch_devin_v3",
            "description": "Creates a high-priority task for Devin via Manus API. Use this when a seller is ready to sell or provides key details.",
            "http_mode": "POST",
            "url": "https://api.manus.ai/v2/task.create",
            "speech_while_using_the_tool": "I'm letting Devin know right now, he'll be thrilled.",
            "run_action_before_call_start": False,
            "headers": [
                {
                    "key": "x-manus-api-key",
                    "value": MANUS_API_KEY
                },
                {
                    "key": "Content-Type",
                    "value": "application/json"
                }
            ],
            "json_body_stringified": json.dumps({
                "message": {
                    "content": "Sarah has a HOT lead! Caller: {{caller_phone_number}}. Summary: {{call_transcript_summary}}. Please find a buyer immediately."
                }
            })
        }
    }
    
    log("Creating fixed DISPATCH_DEVIN action...")
    response = requests.post(url, headers=headers, json=action_payload)
    if response.status_code == 200:
        action_id = response.json().get("response", {}).get("action_id")
        log(f"New action created: {action_id}")
        return action_id
    else:
        log(f"Failed to create action: {response.text}")
        return None

def attach_action(action_id):
    """Attach the new action to Sarah."""
    url = "https://api.synthflow.ai/v2/actions/attach"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": ASSISTANT_ID,
        "actions": [action_id, "a8e7bdd9-fd79-42b1-8826-730c439abcbf"] # Keep image action
    }
    
    log(f"Attaching action {action_id} to Sarah...")
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        log("Action attached successfully.")
    else:
        log(f"Failed to attach action: {response.text}")

def sync_latest_call():
    """Fetch the latest call and save it to memory."""
    url = "https://api.synthflow.ai/v2/calls"
    headers = {"Authorization": f"Bearer {SYNTHFLOW_API_KEY}"}
    params = {"model_id": ASSISTANT_ID, "limit": 1}
    
    log("Syncing latest call transcript...")
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        calls = response.json().get('response', {}).get('calls', [])
        if calls:
            call = calls[0]
            call_id = call.get('call_id')
            caller = call.get('customer_number')
            transcript = call.get('transcript')
            
            # Save to call_logs_sync.json
            log_file = "/home/ubuntu/devin-pantheon/call_logs_sync.json"
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
            
            # Check if call already logged
            if not any(l.get('call_id') == call_id for l in logs):
                logs.append({
                    "call_id": call_id,
                    "timestamp": datetime.now().isoformat(),
                    "caller": caller,
                    "transcript": transcript
                })
                with open(log_file, 'w') as f:
                    json.dump(logs, f, indent=2)
                log(f"Logged new call from {caller}.")
            else:
                log("Latest call already synced.")
            
            return call
    return None

if __name__ == "__main__":
    # 1. Fix the action
    new_action_id = fix_dispatch_action()
    if new_action_id:
        attach_action(new_action_id)
    
    # 2. Sync transcript
    sync_latest_call()
    
    log("Sarah integration fix complete.")
