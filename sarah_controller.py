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
            # Note: The docs show GET /v2/assistants/
            response = requests.get(f"{self.base_url}/assistants/", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            # Based on docs, response is { "status": "success", "response": { "assistants": [...] } }
            # But the real response seems to be "ok"
            if data.get("status") in ["success", "ok"]:
                agents = data.get("response", {}).get("assistants", [])
                log(f"Found {len(agents)} agents.")
                return agents
            log(f"List agents returned non-success status: {data.get('status')}")
            log(f"Full response: {json.dumps(data, indent=2)}")
            return []
        except Exception as e:
            log(f"Failed to list agents: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"Response content: {e.response.text}")
            return []

    def delete_agent(self, assistant_id):
        """Delete a specific agent by ID."""
        log(f"Deleting agent {assistant_id}...")
        try:
            # Note: The docs show DELETE /v2/assistants/:model_id
            response = requests.delete(f"{self.base_url}/assistants/{assistant_id}", headers=self.headers)
            response.raise_for_status()
            log(f"Agent {assistant_id} deleted successfully.")
            return True
        except Exception as e:
            log(f"Failed to delete agent {assistant_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"Response content: {e.response.text}")
            return False

    def cleanup_older_agents(self):
        """Delete all existing agents to ensure a fresh start."""
        agents = self.list_agents()
        if not agents:
            log("No existing agents found to clean up.")
            return
        
        log(f"Starting cleanup of {len(agents)} agents...")
        for agent in agents:
            # The list agents response for each agent seems to have "model_id" or "id"
            # Let's check both or log the agent object
            agent_id = agent.get("id") or agent.get("model_id")
            if agent_id:
                self.delete_agent(agent_id)
            else:
                log(f"Could not find ID for agent: {json.dumps(agent)}")
        log("Cleanup complete.")

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
                    "You are Sarah, a friendly and professional car brokerage agent working for Devin. "
                    "Your primary goal is to qualify private car sellers in Lethbridge, AB. "
                    "Acknowledge the Kijiji context. Extract: Year, Make, Model, Mileage, Condition, Price, Motivation. "
                    "If the seller is 'hot', fire a high-priority webhook. "
                    "Use the 'GET_VEHICLE_IMAGES' action if they want to see what photos we have."
                ),
                "greeting_message": "Hello, this is Sarah calling for Devin. I believe you're calling about the text we sent regarding your vehicle. Do you have a moment to chat?",
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
            log(f"Full Response: {json.dumps(assistant_data, indent=2)}")
            assistant_id = assistant_data.get("response", {}).get("model_id")
            log(f"Sarah created successfully! Assistant ID: {assistant_id}")
            return assistant_data
        except Exception as e:
            log(f"Failed to create Sarah: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"Response content: {e.response.text}")
            return None

if __name__ == "__main__":
    controller = SarahController()
    # First, list them to see what's actually there
    agents = controller.list_agents()
    if agents:
        controller.cleanup_older_agents()
    
    # Now create Sarah
    controller.create_sarah()
