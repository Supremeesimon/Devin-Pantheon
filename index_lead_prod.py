import requests
import json
import os

# Configuration
CREDENTIALS_PATH = "/home/ubuntu/Devin-Pantheon/config/credentials.json"
MANUS_API_URL = "https://api.manus.ai/v2/task.create"

def index_lead_prod():
    """
    Index Kelly's lead in the Manus system by creating a task to store her data.
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

        # Lead Data for Kelly (Phone Redacted)
        kelly_ad_id = "1731517390"
        kelly_lead_data = {
            "ad_id": kelly_ad_id,
            "name": "Kelly",
            "vehicle": "2018 Ford Explorer Limited",
            "price": "$20,500",
            "mileage": "145,000 km",
            "location": "Pincher Creek, AB",
            "url": "https://www.kijiji.ca/v-cars-trucks/lethbridge/explorer/1731517390",
            "image_urls": [
                "https://i.ebayimg.com/images/g/example1/s-l1600.jpg",
                "https://i.ebayimg.com/images/g/example2/s-l1600.jpg"
            ],
            "notes": "Phone number redacted. Pending Sarah's qualification call."
        }

        # Header: x-manus-api-key
        headers = {
            "x-manus-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        # Payload: Create a task for Devin to 'index' this lead in his memory
        payload = {
            "message": {
                "content": f"Devin, please index this new lead in your memory for Sarah's upcoming pilot call:\n\n{json.dumps(kelly_lead_data, indent=2)}"
            }
        }

        print(f"Indexing lead {kelly_ad_id} via Manus API v2...")
        
        # POST request to create the indexing task
        response = requests.post(MANUS_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                print(f"✅ SUCCESS: Lead {kelly_ad_id} indexed successfully!")
                print(f"Task ID: {data.get('task_id')}")
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ Failed to connect. Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"An error occurred during indexing: {e}")

if __name__ == "__main__":
    index_lead_prod()
