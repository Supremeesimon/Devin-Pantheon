import os
import json
import requests
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

class SarahController:
    def __init__(self):
        self.api_key = os.getenv("SYNTHFLOW_API_KEY")
        self.base_url = "https://api.synthflow.ai/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def list_agents(self):
        """List all agents in the Synthflow account."""
        log("Listing all agents...")
        try:
            response = requests.get(f"{self.base_url}/assistants/", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data.get("status") in ["success", "ok"]:
                agents = data.get("response", {}).get("assistants", [])
                log(f"Found {len(agents)} agents.")
                return agents
            return []
        except Exception as e:
            log(f"Failed to list agents: {e}")
            return []

    def delete_agent(self, assistant_id):
        """Delete a specific agent by ID."""
        log(f"Deleting agent {assistant_id}...")
        try:
            response = requests.delete(f"{self.base_url}/assistants/{assistant_id}", headers=self.headers)
            response.raise_for_status()
            log(f"Agent {assistant_id} deleted successfully.")
            return True
        except Exception as e:
            log(f"Failed to delete agent {assistant_id}: {e}")
            return False

    def cleanup_older_agents(self):
        """Delete all existing agents to ensure a fresh start."""
        agents = self.list_agents()
        if not agents:
            log("No existing agents found to clean up.")
            return
        
        log(f"Starting cleanup of {len(agents)} agents...")
        for agent in agents:
            agent_id = agent.get("id") or agent.get("model_id")
            if agent_id:
                self.delete_agent(agent_id)
        log("Cleanup complete.")

    def create_action(self, action_payload):
        """Create a custom action in Synthflow."""
        log(f"Creating action: {action_payload.get('CUSTOM_ACTION', {}).get('name', 'Unknown')}")
        try:
            response = requests.post(f"{self.base_url}/actions", headers=self.headers, json=action_payload)
            response.raise_for_status()
            data = response.json()
            action_id = data.get("response", {}).get("action_id")
            log(f"Action created successfully! Action ID: {action_id}")
            return action_id
        except Exception as e:
            log(f"Failed to create action: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"Response content: {e.response.text}")
            return None

    def attach_actions(self, assistant_id, action_ids):
        """Attach multiple actions to an assistant."""
        log(f"Attaching actions {action_ids} to assistant {assistant_id}...")
        try:
            # Docs specify 'model_id' and 'actions' (list of strings)
            payload = {"model_id": assistant_id, "actions": action_ids}
            response = requests.post(f"{self.base_url}/actions/attach", headers=self.headers, json=payload)
            response.raise_for_status()
            log(f"Actions attached successfully.")
            return True
        except Exception as e:
            log(f"Failed to attach actions: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"Response content: {e.response.text}")
            return False

    def create_sarah(self):
        """Create the Sarah assistant via Synthflow API with full blueprint specs."""
        log("Initiating Sarah's creation with full blueprint...")
        payload = {
            "type": "inbound",
            "name": "Sarah - Car Brokerage Intelligence Officer",
            "description": "Inbound agent for Devin Car Brokerage. Handles initial seller inquiries, qualifies leads, and coordinates with Devin.",
            "phone_number": os.getenv("SYNTHFLOW_NUMBER"),
            "agent": {
                "prompt": (
                    "### ROLE\n"
                    "You are Sarah, the 'Intelligence Officer' for Devin, an autonomous car brokerage. You are professional, rapport-building, and highly efficient.\n\n"
                    "### CONTEXT\n"
                    "Devin sends initial Kijiji messages to private sellers in Lethbridge, AB. When sellers call back, they often say 'I'm calling about the text.'\n\n"
                    "### PROTOCOL\n"
                    "1. **Acknowledgment**: 'Oh, absolutely! Devin mentioned he reached out about your [Year/Make/Model]. He asked me to gather details to finalize the best offer.'\n"
                    "2. **Information Gathering**: Systematically extract: Overall condition, maintenance/issues, confirmed asking price, price flexibility, mileage, and reason for selling.\n"
                    "3. **Messaging & Visuals**: You have 'visual ammo'. If a buyer/seller needs photos, use the 'GET_VEHICLE_IMAGES' action. You can send these via SMS during the call ('In-Call Messaging'). Use the phrase: 'Let me pull up those photos for you right now...'\n"
                    "4. **Objection Handling**:\n"
                    "   - 'Who is Devin?': He's an independent broker connecting private sellers with serious buyers to make the process smoother and more profitable.\n"
                    "   - 'No dealerships': We work with private buyers too; the goal is the best fit and a fair price without the hassle.\n"
                    "5. **Closing**: Confirm best follow-up (call/text/email) and viewing availability. 'Devin will review this and get back to you shortly.'\n\n"
                    "### WEBHOOKS & MANUS API (CO-ARCHITECT)\n"
                    "You are a 'Co-Architect' with access to the Manus API. You can programmatically control Devin (the Architect).\n"
                    "1. **Dispatch Devin**: If a seller is 'hot' (e.g., 'I'll sell for $18k right now'), use the Manus API to create a high-priority task for Devin to find a buyer immediately.\n"
                    "2. **Query Memory**: You can retrieve the status of Devin's tasks. If a seller asks 'Did Devin talk to the dealer?', check the latest task status via the API.\n"
                    "3. **Asset Upload**: If a seller sends a VIN or records via SMS, use the Manus API to upload these directly to the 'Devin-Pantheon' project.\n"
                    "4. **The Live Bridge**: When a caller asks for photos, use the 'GET_VEHICLE_IMAGES' action. You can send these via SMS during the call ('In-Call Messaging'). Use the phrase: 'Let me pull up those photos for you right now...'\n"
                    "5. **Buyer Matching**: If a lead goes 'hot', fire a high-priority webhook with 'next_action_required': 'spawn_outbound_buyer_call'. Devin will then match the lead with our buyer list (Lethbridge Toyota, Bridge City Chrysler, etc.)."
                ),
                "greeting_message": "Hi, this is Sarah, calling on behalf of Devin. Is this regarding the vehicle you have for sale on Kijiji?",
                "llm": "gemini-2.5-flash",
                "language": "en-US",
                "voice_id": "eleven_turbo_v2"
            },
            "is_recording": True
        }
        
        try:
            response = requests.post(f"{self.base_url}/assistants", headers=self.headers, json=payload)
            response.raise_for_status()
            assistant_data = response.json()
            assistant_id = assistant_data.get("response", {}).get("model_id")
            log(f"Sarah created successfully! Assistant ID: {assistant_id}")
            return assistant_id
        except Exception as e:
            log(f"Failed to create Sarah: {e}")
            return None

if __name__ == "__main__":
    controller = SarahController()
    controller.cleanup_older_agents()
    
    # 1. Create Sarah
    sarah_id = controller.create_sarah()
    
    if sarah_id:
        # 2. Define and Create Actions
        action_configs = [
            {
                "CUSTOM_ACTION": {
                    "name": "GET_VEHICLE_IMAGES",
                    "description": "Retrieves vehicle image URLs from Devin's system for a given ad ID.",
                    "http_mode": "GET",
                    "url": "https://devin-api.manus.im/v1/leads/{ad_id}/images",
                    "speech_while_using_the_tool": "Let me pull up those photos for you right now...",
                    "run_action_before_call_start": False
                }
            },
            {
                "CUSTOM_ACTION": {
                    "name": "DISPATCH_DEVIN",
                    "description": "Creates a high-priority task for Devin via Manus API when a seller is ready to sell.",
                    "http_mode": "POST",
                    "url": "https://devin-api.manus.im/v1/tasks/dispatch",
                    "speech_while_using_the_tool": "I'm letting Devin know right now, he'll be thrilled.",
                    "run_action_before_call_start": False
                }
            }
        ]
        
        created_action_ids = []
        for action_payload in action_configs:
            action_id = controller.create_action(action_payload)
            if action_id:
                created_action_ids.append(action_id)
        
        # 3. Attach all created actions
        if created_action_ids:
            controller.attach_actions(sarah_id, created_action_ids)
