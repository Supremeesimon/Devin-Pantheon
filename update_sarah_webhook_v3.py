import requests
import json

SYNTHFLOW_API_KEY = "15l6mlQNXNpsVHO-VugQbczSGJ4LhDCpO6Dt2PZcl2Y"
ASSISTANT_ID = "0a420ae4-6d32-46b4-8c84-7f9315831736"
WEBHOOK_URL = "https://8000-if1w718srqawckv2yug6k-a569c4d6.us2.manus.computer/webhook"

def update_webhook():
    url = f"https://api.synthflow.ai/v2/assistants/{ASSISTANT_ID}"
    headers = {
        "Authorization": f"Bearer {SYNTHFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "webhook_url": WEBHOOK_URL
    }
    
    print(f"Updating webhook for Assistant ID: {ASSISTANT_ID} via PUT...")
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("✅ SUCCESS: Sarah's webhook URL has been updated.")
        print(f"New Webhook: {WEBHOOK_URL}")
    else:
        print(f"❌ FAILED to update: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    update_webhook()
