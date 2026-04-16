import requests
import json
import os

# Configuration
MANUS_API_URL = "https://api.manus.im/v1/leads"
# Note: You need to set the MANUS_API_KEY environment variable before running this script
MANUS_API_KEY = os.environ.get("MANUS_API_KEY")

def index_lead(ad_id, lead_data):
    """
    Manually index a lead to the Manus API to resolve 404 errors for GET_VEHICLE_IMAGES.
    """
    if not MANUS_API_KEY:
        print("Error: MANUS_API_KEY environment variable is not set.")
        return

    headers = {
        "Authorization": f"Bearer {MANUS_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(MANUS_API_URL, headers=headers, json=lead_data)
        if response.status_code in [200, 201]:
            print(f"Successfully indexed lead {ad_id}.")
        else:
            print(f"Failed to index lead {ad_id}. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while indexing lead {ad_id}: {e}")

if __name__ == "__main__":
    # Data for Kelly's Ford Explorer (ad_id: 1731517390)
    kelly_ad_id = "1731517390"
    kelly_lead_data = {
        "ad_id": kelly_ad_id,
        "name": "Kelly",
        "vehicle": "2018 Ford Explorer Limited",
        "price": "$20,500",
        "mileage": "145,000 km",
        "location": "Pincher Creek, AB",
        "url": "https://www.kijiji.ca/v-cars-trucks/lethbridge/explorer/1731517390",
        "image_urls": [
            "https://i.ebayimg.com/images/g/example1/s-l1600.jpg",
            "https://i.ebayimg.com/images/g/example2/s-l1600.jpg"
        ]
    }
    
    print(f"Indexing lead {kelly_ad_id}...")
    index_lead(kelly_ad_id, kelly_lead_data)
