import os
import requests

def clear_all():
    api_key = os.getenv("SYNTHFLOW_API_KEY")
    sarah_id = "0a420ae4-6d32-46b4-8c84-7f9315831736"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # The 4 IDs currently attached to Sarah
    ids_to_detach = [
        "55ebba51-01cc-48d1-96d4-699eceef642e",
        "bf8c935b-1521-4830-8b9e-c0d832b19248",
        "01174625-4472-4f96-835c-7a6319e33257",
        "8a370f1a-04dc-44a6-81c7-5f694b63c7dd"
    ]
    
    print(f"--- Detaching {len(ids_to_detach)} actions ---")
    payload = {
        "model_id": sarah_id,
        "actions": ids_to_detach
    }
    
    try:
        response = requests.post("https://api.synthflow.ai/v2/actions/detach", headers=headers, json=payload)
        print(f"Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clear_all()
