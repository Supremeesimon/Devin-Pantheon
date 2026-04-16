import requests
import json
import os

# Configuration
CREDENTIALS_PATH = "/home/ubuntu/Devin-Pantheon/config/credentials.json"

def test_manus_final():
    """
    Test the Manus API v2 task creation endpoint with the correct header.
    Header: x-manus-api-key
    Endpoint: https://api.manus.ai/v2/task.create
    """
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            credentials = json.load(f)
        
        api_key = credentials.get("MANUS_API_KEY")
        if not api_key:
            print("Error: MANUS_API_KEY not found in credentials.json.")
            return

        # Correct v2 endpoint for task creation
        url = "https://api.manus.ai/v2/task.create"
        
        # CORRECT HEADER: x-manus-api-key
        headers = {
            "x-manus-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        # Payload as per documentation
        payload = {
            "message": {
                "content": "Hello, this is a connectivity test. Please reply with 'Success'."
            }
        }

        print(f"Testing Manus API v2 with x-manus-api-key header...")
        
        # POST request to create a task
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                print("Successfully connected to Manus API v2!")
                print(f"Task Created! ID: {data.get('task_id')}")
            else:
                print(f"API returned error: {data.get('error')}")
        else:
            print(f"Failed to connect. Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"An error occurred during Manus API testing: {e}")

if __name__ == "__main__":
    test_manus_final()
