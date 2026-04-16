import requests
import json
import time
import os

# Configuration
CREDENTIALS_PATH = "/home/ubuntu/Devin-Pantheon/config/credentials.json"
TASK_ID = "YwSWBGGcTvdmRpXyFFy3vK"

def poll_task():
    """
    Poll the Manus API v2 for task messages and status.
    Endpoint: https://api.manus.ai/v2/task.listMessages
    Header: x-manus-api-key
    """
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            credentials = json.load(f)
        
        api_key = credentials.get("MANUS_API_KEY")
        if not api_key:
            print("Error: MANUS_API_KEY not found in credentials.json.")
            return

        url = f"https://api.manus.ai/v2/task.listMessages?task_id={TASK_ID}&order=desc&limit=10"
        headers = {
            "x-manus-api-key": api_key,
            "Content-Type": "application/json"
        }

        print(f"Polling task {TASK_ID}...")
        
        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    messages = data.get("messages", [])
                    
                    # Find the latest status update
                    status_update = next((m for m in messages if m.get("type") == "status_update"), None)
                    if status_update:
                        agent_status = status_update.get("status_update", {}).get("agent_status")
                        print(f"Current Status: {agent_status}")
                        
                        if agent_status == "stopped":
                            print("Task complete! Retrieving results...")
                            # Find the assistant message with results
                            assistant_msg = next((m for m in messages if m.get("type") == "assistant_message"), None)
                            if assistant_msg:
                                print(f"Result: {assistant_msg.get('assistant_message', {}).get('content')}")
                            break
                        elif agent_status == "error":
                            print("Task failed!")
                            error_msg = next((m for m in messages if m.get("type") == "error_message"), None)
                            if error_msg:
                                print(f"Error: {error_msg.get('error_message', {}).get('content')}")
                            break
                        elif agent_status == "waiting":
                            print("Task is waiting for user input.")
                            break
                    else:
                        print("No status update found yet...")
                else:
                    print(f"API returned error: {data.get('error')}")
                    break
            else:
                print(f"Failed to connect. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                break
            
            time.sleep(5)

    except Exception as e:
        print(f"An error occurred during polling: {e}")

if __name__ == "__main__":
    poll_task()
