import os
import json
import glob
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

class WebhookListener:
    def __init__(self):
        self.sellers_path = "/home/ubuntu/devin-pantheon/memory/sellers"

    def identify_caller(self, phone_number):
        """Search seller memory to identify a caller by their phone number."""
        log(f"Attempting to identify caller: {phone_number}")
        
        seller_files = glob.glob(f"{self.sellers_path}/*.md")
        for file_path in seller_files:
            with open(file_path, "r") as f:
                content = f.read()
                # Simple check for the phone number in the markdown content
                if phone_number in content:
                    seller_name = file_path.split("/")[-1].replace(".md", "")
                    log(f"Caller identified as: {seller_name}")
                    return seller_name
        
        log("Caller not found in existing seller database.")
        return None

    def handle_synthflow_webhook(self, payload):
        """Process the incoming payload from Sarah/Synthflow."""
        caller_phone = payload.get("caller_phone_number")
        transcript = payload.get("call_transcript_summary")
        
        seller_id = self.identify_caller(caller_phone)
        
        if seller_id:
            log(f"Updating records for {seller_id}...")
            # Here we would call the ManusBridge to update the file
        else:
            log("Creating new lead entry for unidentified caller.")

if __name__ == "__main__":
    # Test identification with a dummy number
    listener = WebhookListener()
    # listener.identify_caller("+1XXXXXXXXXX")
