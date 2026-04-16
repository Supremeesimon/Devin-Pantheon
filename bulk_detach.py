import os
import requests

def bulk_detach():
    api_key = os.getenv("SYNTHFLOW_API_KEY")
    sarah_id = "0a420ae4-6d32-46b4-8c84-7f9315831736"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # The 10 redundant IDs identified from the diagnostic check
    ids_to_detach = [
        "e87e8d54-4f51-42d7-9f89-d1e43f0d850b",
        "dbffed1c-b411-4058-9bab-51c14af418d5",
        "90d9bdcb-d1cf-46ba-8ee6-375102109e15",
        "175f5eba-af6c-417e-97c4-716ae4824098",
        "e3889df8-7a9f-4510-8309-985cc5d72193",
        "6f3acc02-243e-497e-a402-412c67efd1a3",
        "29853736-d558-4916-ad47-49b6f50e12d3",
        "908e8188-3c6b-44ac-aff1-7ea15b38c053",
        "6a0848e4-bbb3-45dd-ab44-964d2757eac2",
        "6cbea9e9-60a9-42dd-9fcc-cdd75a17c802"
    ]
    
    print(f"--- Starting Bulk Detachment for {len(ids_to_detach)} actions ---")
    
    # The documentation specifies the payload should have 'actions' as a list of strings
    payload = {
        "model_id": sarah_id,
        "actions": ids_to_detach
    }
    
    try:
        response = requests.post("https://api.synthflow.ai/v2/actions/detach", headers=headers, json=payload)
        if response.status_code == 200:
            print("Successfully detached all actions in bulk.")
            print(f"Response: {response.json()}")
        else:
            print(f"Bulk detachment failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during bulk detachment: {e}")

if __name__ == "__main__":
    bulk_detach()
