import requests
import json

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"

# The only two actions Sarah should have
PROD_ACTION_IDS = [
    "03c34552-662f-402d-ba59-92b72f3270fd", # DISPATCH_DEVIN_PROD
    "a8e7bdd9-fd79-42b1-8826-730c439abcbf"  # GET_VEHICLE_IMAGES_PROD
]

def audit_and_fix():
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 1. Get current assistant state to see attached actions
    print(f"Auditing Assistant ID: {ASSISTANT_ID}...")
    get_url = f"https://api.synthflow.ai/v2/assistants/{ASSISTANT_ID}"
    response = requests.get(get_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching assistant: {response.status_code}")
        print(response.text)
        return

    assistant_data = response.json().get('response', {}).get('assistants', [{}])[0]
    attached_action_ids = assistant_data.get('actions', [])
    
    print(f"Currently attached action IDs: {attached_action_ids}")
    
    # 2. Identify duplicates or unwanted actions
    unwanted = [aid for aid in attached_action_ids if aid not in PROD_ACTION_IDS]
    missing = [aid for aid in PROD_ACTION_IDS if aid not in attached_action_ids]
    
    if not unwanted and not missing:
        print("✅ Sarah's actions are already clean. No duplicates or missing actions found.")
        return

    if unwanted:
        print(f"Found {len(unwanted)} unwanted or duplicate actions: {unwanted}")
    if missing:
        print(f"Missing {len(missing)} production actions: {missing}")

    # 3. Force-set to only the production actions
    print("Fixing... Force-setting actions to only production-ready IDs.")
    attach_url = "https://api.synthflow.ai/v2/actions/attach"
    payload = {
        "model_id": ASSISTANT_ID,
        "actions": PROD_ACTION_IDS
    }
    
    fix_response = requests.post(attach_url, headers=headers, json=payload)
    if fix_response.status_code == 200:
        print("✅ SUCCESS: Sarah's actions have been cleaned. Only the 2 production actions remain.")
    else:
        print(f"❌ FAILED to fix: {fix_response.status_code}")
        print(fix_response.text)

if __name__ == "__main__":
    audit_and_fix()
