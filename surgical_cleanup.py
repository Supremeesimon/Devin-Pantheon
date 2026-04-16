import os
import requests
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

class SarahCleanup:
    def __init__(self):
        self.api_key = os.getenv("SYNTHFLOW_API_KEY")
        self.base_url = "https://api.synthflow.ai/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.sarah_id = "0a420ae4-6d32-46b4-8c84-7f9315831736"

    def list_attached_actions(self):
        log(f"Fetching all actions for Sarah ({self.sarah_id})...")
        try:
            response = requests.get(f"{self.base_url}/assistants/{self.sarah_id}", headers=self.headers)
            response.raise_for_status()
            data = response.json().get("response", {}).get("assistants", [])
            if not data:
                # Try singular
                data = response.json().get("response", {}).get("assistant", {})
            
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
                
            actions = data.get("actions", [])
            log(f"Found {len(actions)} actions attached.")
            return actions
        except Exception as e:
            log(f"Failed to list actions: {e}")
            return []

    def detach_all_actions(self):
        actions = self.list_attached_actions()
        if not actions:
            log("No actions to detach.")
            return
        
        log(f"Detaching {len(actions)} actions...")
        for aid in actions:
            try:
                payload = {"model_id": self.sarah_id, "action_id": aid}
                requests.post(f"{self.base_url}/actions/detach", headers=self.headers, json=payload)
                log(f"Detached {aid}")
            except Exception as e:
                log(f"Failed to detach {aid}: {e}")

    def create_and_attach_production_actions(self):
        log("Creating and attaching production actions...")
        manus_api_key = os.getenv("MANUS_API_KEY")
        
        action_configs = [
            {
                "CUSTOM_ACTION": {
                    "name": "GET_VEHICLE_IMAGES",
                    "description": "Retrieves vehicle image URLs from Devin's system for a given ad ID.",
                    "http_mode": "GET",
                    "url": "https://api.manus.im/v1/leads/{ad_id}/images",
                    "speech_while_using_the_tool": "Let me pull up those photos for you right now...",
                    "run_action_before_call_start": False
                }
            },
            {
                "CUSTOM_ACTION": {
                    "name": "DISPATCH_DEVIN",
                    "description": "Creates a high-priority task for Devin via Manus API when a seller is ready to sell.",
                    "http_mode": "POST",
                    "url": "https://api.manus.im/v1/tasks",
                    "speech_while_using_the_tool": "I'm letting Devin know right now, he'll be thrilled.",
                    "run_action_before_call_start": False,
                    "custom_auth": {
                        "type": "bearer",
                        "header_value": manus_api_key
                    }
                }
            }
        ]
        
        new_action_ids = []
        for config in action_configs:
            try:
                response = requests.post(f"{self.base_url}/actions", headers=self.headers, json=config)
                response.raise_for_status()
                aid = response.json().get("response", {}).get("action_id")
                log(f"Created action {config['CUSTOM_ACTION']['name']} (ID: {aid})")
                new_action_ids.append(aid)
            except Exception as e:
                log(f"Failed to create action: {e}")

        if new_action_ids:
            try:
                payload = {"model_id": self.sarah_id, "actions": new_action_ids}
                requests.post(f"{self.base_url}/actions/attach", headers=self.headers, json=payload)
                log(f"Successfully attached {len(new_action_ids)} production actions.")
            except Exception as e:
                log(f"Failed to attach actions: {e}")

if __name__ == "__main__":
    cleanup = SarahCleanup()
    cleanup.detach_all_actions()
    cleanup.create_and_attach_production_actions()
    # Final check
    cleanup.list_attached_actions()
