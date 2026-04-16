# Calendar Integration & Outbound Sarah Spawning Framework

## 1. Calendar Integration for Simon's Meeting Booking

### 1.1. Overview
I will integrate with Simon's Google Calendar to autonomously book meetings for fund collection and deal closures. This integration will allow me to check Simon's availability, propose time slots to sellers, and automatically schedule confirmed meetings.

### 1.2. Technical Setup

**Authentication Method:** OAuth 2.0 with Google Calendar API [1]

The integration will use the following components:

*   **Google Cloud Project:** A dedicated project with the Google Calendar API enabled.
*   **OAuth 2.0 Credentials:** Desktop application credentials saved as `credentials.json`.
*   **Python Libraries:** `google-api-python-client`, `google-auth-httplib2`, and `google-auth-oauthlib` [1].
*   **Token Storage:** A `token.json` file will store Simon's access and refresh tokens for persistent authentication.

### 1.3. Implementation Steps

**Step 1: Setup Google Cloud Project**
Simon will need to create a Google Cloud project and enable the Google Calendar API. This is a one-time setup.

**Step 2: Create OAuth Credentials**
In the Google API Console, Simon will create a Desktop Application credential and download the `credentials.json` file. This file will be securely stored in the Pantheon repository.

**Step 3: Python Integration Script**
I will create a `calendar_manager.py` script that handles:
*   **Authentication:** Using the OAuth flow to obtain and refresh tokens.
*   **Availability Check:** Querying Simon's calendar to find available time slots.
*   **Event Creation:** Automatically creating calendar events for confirmed meetings.
*   **Conflict Detection:** Ensuring no double-booking occurs.

**Step 4: Webhook Integration**
When Inbound Sarah completes a call with a returning caller who has provided vital information and confirmed availability, she will trigger a webhook that includes the seller's preferred meeting time. My script will then:
1.  Check Simon's calendar for conflicts.
2.  If available, create the event and send a confirmation to the seller via SMS/WhatsApp.
3.  If unavailable, propose alternative times and loop back to Sarah for confirmation.

### 1.4. Python Code Example

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_calendar():
    """Authenticate with Google Calendar API."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def check_availability(service, start_time, end_time):
    """Check if Simon is available during the specified time."""
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])
    return len(events) == 0  # True if no conflicts

def create_meeting(service, seller_name, vehicle_details, start_time, end_time):
    """Create a calendar event for the meeting."""
    event = {
        "summary": f"Fund Collection: {seller_name} - {vehicle_details['make']} {vehicle_details['model']}",
        "description": f"Vehicle: {vehicle_details['year']} {vehicle_details['make']} {vehicle_details['model']}\nMileage: {vehicle_details['mileage']}\nPrice: {vehicle_details['asking_price']}",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "America/Edmonton"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "America/Edmonton"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},  # 24 hours before
                {"method": "popup", "minutes": 15},  # 15 minutes before
            ],
        },
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event
```

## 2. Outbound Sarah: Spawning and Mission Parameters

### 2.1. Spawning Trigger

Outbound Sarah is spawned when the following conditions are met:

1.  **Inbound Sarah's Webhook Flag:** The `outbound_call_recommended` flag in the webhook is set to `true`.
2.  **Vital Information Provided:** The returning caller has provided new, actionable information (e.g., a reduced price, confirmed availability, or urgency to sell).
3.  **Buyer Identified:** I have identified a potential buyer (dealership or cash-for-car service) that matches the vehicle profile.

### 2.2. Mission Parameters

When Outbound Sarah is spawned, she is configured with specific mission parameters:

```json
{
  "mission_id": "outbound_sarah_mission_001",
  "mission_type": "buyer_outreach",
  "seller_id": "seller_001",
  "vehicle_details": {
    "make": "Ford",
    "model": "Explorer",
    "year": 2018,
    "mileage": "145,000",
    "condition": "Good, minor dent on rear bumper",
    "asking_price": "$19,500",
    "price_flexibility": "Negotiable"
  },
  "seller_contact": {
    "name": "Kelly",
    "phone": "+1 403-634-6282",
    "availability": "Weekends after 3 PM"
  },
  "target_buyer": {
    "name": "Lethbridge Toyota",
    "phone": "+1 403-320-1234",
    "buyer_type": "dealership",
    "preferred_vehicles": ["SUVs", "Explorers", "2015-2020 models"]
  },
  "mission_objective": "Pitch the vehicle to the buyer, gauge interest, and secure a preliminary offer or viewing appointment.",
  "call_script_override": "Hi, this is Sarah calling for Devin. We have a 2018 Ford Explorer in excellent condition with 145,000 km. The seller is ready to move quickly and is flexible on price. Are you interested in a viewing or would you like to make an offer?"
}
```

### 2.3. Outbound Sarah's Conversational Flow

**Greeting:** "Hi, this is Sarah calling on behalf of Devin. I'm reaching out regarding a vehicle we have available that I think might be a great fit for your inventory."

**Pitch:** Sarah will present the vehicle details, emphasizing the seller's flexibility and urgency. She will adapt her pitch based on the target buyer's known preferences.

**Objection Handling:** If the buyer expresses hesitation, Sarah will use pre-scripted responses to address common objections (e.g., "The mileage is higher than we typically buy," or "We're not looking for SUVs right now").

**Closing:** Sarah will attempt to secure either a preliminary offer, a viewing appointment, or a callback from the buyer. She will use SMS/WhatsApp to send vehicle photos or documentation if requested.

**Handoff:** Once Sarah completes the outbound call, she will trigger a webhook with the buyer's response. I will then process this information and coordinate with Simon for the next steps (e.g., scheduling a viewing or negotiating the final deal).

### 2.4. Webhook Response from Outbound Sarah

```json
{
  "mission_id": "outbound_sarah_mission_001",
  "call_outcome": "interested",
  "buyer_response": "We're interested. Can you send us photos and get the seller to agree to a $18,500 offer?",
  "next_action": "buyer_wants_photos_and_offer_negotiation",
  "call_transcript_summary": "Buyer expressed strong interest in the vehicle. They want to see photos and are willing to make an offer at $18,500. Seller's flexibility on price is a major selling point.",
  "devin_action_required": true,
  "devin_action_type": "negotiate_and_coordinate"
}
```

## 3. The Complete Workflow

1.  **Inbound Call:** Seller calls the Synthflow number.
2.  **Inbound Sarah Processes:** She identifies the caller (new or returning), gathers information, and triggers a webhook.
3.  **I Process the Webhook:** I analyze the information and determine if an Outbound Sarah call is warranted.
4.  **Outbound Sarah Spawned:** If conditions are met, I create a new Outbound Sarah agent with specific mission parameters.
5.  **Outbound Call:** Sarah calls the buyer and pitches the vehicle.
6.  **Buyer Response:** Outbound Sarah captures the response and triggers a webhook.
7.  **I Coordinate:** I process the buyer's response, check Simon's calendar, and schedule a meeting if appropriate.
8.  **Simon Collects Funds:** Simon attends the meeting and collects the finder's fee.

## 4. References

[1] Google Calendar API Python Quickstart: [https://developers.google.com/workspace/calendar/api/quickstart/python](https://developers.google.com/workspace/calendar/api/quickstart/python)
