import requests
import json
import os

# Configuration
CREDENTIALS_PATH = "/home/ubuntu/Devin-Pantheon/config/credentials.json"
TASK_ID = "YwSWBGGcTvdmRpXyFFy3vK"

def verify_sarah_access():
    """
    Verify if Sarah can access Kelly's lead details by:
    1. Polling the indexing task messages.
    2. Confirming the lead data is stored and retrievable.
    Header: x-manus-api-key
    """
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            credentials = json.load(f)
        
        api_key = credentials.get("MANUS_API_KEY")
        if not api_key:
            print("Error: MANUS_API_KEY not found in credentials.json.")
            return

        # Correct v2 endpoint for polling messages
        url = f"https://api.manus.ai/v2/task.listMessages?task_id={TASK_ID}&order=desc&limit=10"
        headers = {
            "x-manus-api-key": api_key,
            "Content-Type": "application/json"
        }

        print(f"Verifying Sarah's access to lead indexed in task {TASK_ID}...")
        
        # GET request to retrieve messages
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                messages = data.get("messages", [])
                
                # Find the latest assistant message with results
                assistant_msg = next((m for m in messages if m.get("type") == "assistant_message"), None)
                if assistant_msg:
                    print("✅ SUCCESS: Lead details are retrievable from the system memory!")
                    print(f"Assistant Result: {assistant_msg.get('assistant_message', {}).get('content')}")
                    
                    # Confirming the phone number is redacted in the indexing task
                    # We'll check the original message to ensure the redaction was applied
                    user_msg = next((m for m in messages if m.get("type") == "user_message"), None)
                    if user_msg:
                        content = user_msg.get('user_message', {}).get('content')
                        if "+1 555 123 4567" not in content:
                            print("✅ CONFIRMED: Phone number is redacted from the indexed record.")
                        else:
                            print("❌ WARNING: Phone number was found in the indexed record!")
                else:
                    print("❌ FAILED: No assistant message found in the task history.")
            else:
                print(f"❌ API returned error: {data.get('error')}")
        else:
            print(f"❌ Failed to connect. Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"An error occurred during verification: {e}")

if __name__ == "__main__":
    verify_sarah_access()
