import os
import requests
import json
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def verify_images(ad_id):
    api_key = os.getenv("MANUS_API_KEY")
    # Production URL based on the updated controller
    url = f"https://api.manus.im/v1/leads/{ad_id}/images"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    log(f"--- Verifying GET_VEHICLE_IMAGES for ad_id: {ad_id} ---")
    log(f"Target URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            log("SUCCESS: 200 OK")
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            log(f"FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        log(f"ERROR: {e}")

if __name__ == "__main__":
    # Using the ad_id found in the seller_001.md (Kelly's Ford Explorer)
    test_ad_id = "1731517390"
    verify_images(test_ad_id)
