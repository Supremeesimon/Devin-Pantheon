import os
import requests

def final_clear():
    api_key = os.getenv("SYNTHFLOW_API_KEY")
    sarah_id = "0a420ae4-6d32-46b4-8c84-7f9315831736"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # The 4 IDs currently on Sarah
    ids = [
        "0bbdc252-a4d7-44cc-a015-ef3c8fdb6058",
        "ecc91c41-5666-44ae-aac7-d332c01d00dc",
        "072546e0-18a0-4373-93f9-35271b611bfd",
        "6ce7ef09-1b21-456d-9cb5-1a691df6d505"
    ]
    
    print(f"--- Detaching {len(ids)} actions ---")
    payload = {"model_id": sarah_id, "actions": ids}
    try:
        response = requests.post("https://api.synthflow.ai/v2/actions/detach", headers=headers, json=payload)
        print(f"Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_clear()
