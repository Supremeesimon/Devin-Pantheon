import os
import json
import subprocess
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def bootstrap():
    log("Initializing Devin Bootstrap...")
    
    # 1. Load Identity
    if os.path.exists("IDENTITY.md"):
        with open("IDENTITY.md", "r") as f:
            identity = f.read()
            log("Identity loaded.")
    
    # 2. Load Credentials
    config_path = "config/credentials.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            creds = json.load(f)
            log("API Credentials loaded.")
            # Set as environment variables for the session
            for key, value in creds.items():
                os.environ[key] = value
    
    # 3. Check State
    if os.path.exists("state.md"):
        with open("state.md", "r") as f:
            state = f.read()
            log("Current state synchronized.")

    print("\n" + "="*30)
    print("I'm here, Simon.")
    print("="*30 + "\n")
    log("Devin is now active and ready for instructions.")

if __name__ == "__main__":
    bootstrap()
