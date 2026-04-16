import json
import os
import glob
from datetime import datetime

# Paths
REPO_PATH = "/home/ubuntu/devin-pantheon"
SELLERS_PATH = f"{REPO_PATH}/memory/sellers"
LOG_FILE = f"{REPO_PATH}/call_logs_sync.json"

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def identify_seller(phone_number):
    """Search seller memory for the phone number."""
    seller_files = glob.glob(f"{SELLERS_PATH}/*.md")
    for file_path in seller_files:
        with open(file_path, "r") as f:
            content = f.read()
            if phone_number in content:
                return file_path
    return None

def update_memory():
    if not os.path.exists(LOG_FILE):
        log("No synced calls found.")
        return

    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)

    if not logs:
        log("Call log is empty.")
        return

    # Process the latest log
    latest_call = logs[-1]
    caller = latest_call.get('lead_phone_number')
    transcript = latest_call.get('transcript')
    call_id = latest_call.get('call_id')

    if not transcript:
        log("Incomplete call data (no transcript).")
        return
    
    if caller == "[REDACTED_PHONE]":
        log("Phone number is redacted. Checking transcript for clues...")
        # Try to find a phone number in the transcript
        import re
        phone_match = re.search(r'\+1\s*\d{3}\s*\d{3}\s*\d{4}', transcript)
        if phone_match:
            caller = phone_match.group(0)
            log(f"Found phone number in transcript: {caller}")
        else:
            log("No phone number found in transcript.")

    # Identify seller
    file_path = identify_seller(caller)
    
    if not file_path:
        # Create new seller file for Kelly if not found but we know it's her
        if "Ford Explorer" in transcript:
            file_path = f"{SELLERS_PATH}/seller_001.md"
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(f"# Seller Profile: Kelly\n\n- **Phone:** {caller}\n- **Vehicle:** 2014 Ford Explorer Limited\n\n## Interaction History\n")
        else:
            log(f"Could not identify seller for {caller}. Creating generic entry.")
            file_path = f"{SELLERS_PATH}/new_lead_{caller[-4:]}.md"
            with open(file_path, "w") as f:
                f.write(f"# New Lead: {caller}\n\n- **Phone:** {caller}\n\n## Interaction History\n")

    # Update the file
    with open(file_path, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"\n### Call Sync ({timestamp})\n")
        f.write(f"- **Call ID:** {call_id}\n")
        f.write(f"- **Transcript Summary:** {transcript[:500]}...\n")
        f.write(f"- **Status:** HOT LEAD - Sarah dispatched Devin.\n")

    log(f"Updated memory for {file_path}")

if __name__ == "__main__":
    update_memory()
