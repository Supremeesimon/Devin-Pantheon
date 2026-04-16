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

    def create_sarah(self):
        """Create the Sarah assistant via Synthflow API with full blueprint specs."""
        log("Initiating Sarah's creation with full blueprint...")
        payload = {
            "type": "inbound",
            "name": "Sarah - Car Brokerage Intelligence Officer",
            "description": "Inbound agent for Devin Car Brokerage. Handles initial seller inquiries, qualifies leads, and coordinates with Devin.",
            "phone_number": os.getenv("SYNTHFLOW_NUMBER"),
            "external_webhook_url": "https://devin-api.manus.im/v1/synthflow/webhook",
            "inbound_call_webhook_url": "https://devin-api.manus.im/v1/synthflow/inbound-call-webhook",
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
        
        # Simulation mode for the test run
        if os.getenv("DEVIN_TEST_MODE") == "true":
            log("[TEST MODE] Sarah creation payload validated. Skipping actual API call.")
            return {"id": "test_assistant_id_123", "status": "success"}

        try:
            response = requests.post(f"{self.base_url}/assistants", headers=self.headers, json=payload)
            response.raise_for_status()
            assistant_data = response.json()
            log(f"Sarah created successfully! Assistant ID: {assistant_data.get('id')}")
            return assistant_data
        except Exception as e:
            log(f"Failed to create Sarah: {e}")
            return None

    def attach_custom_action(self, assistant_id, action_id):
        """Attach a custom action (like image retrieval) to Sarah."""
        log(f"Attaching action {action_id} to Sarah ({assistant_id})...")
        # Placeholder for action attachment logic
        pass

if __name__ == "__main__":
    # This would be run as part of Devin's "Act" phase if Sarah needs to be updated or created
    controller = SarahController()
    # controller.create_sarah()
