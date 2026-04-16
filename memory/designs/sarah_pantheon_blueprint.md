# Sarah's Pantheon Blueprint: Programmatic Setup

This document outlines the programmatic steps to create and configure Sarah, our "Intelligence Officer," within her Synthflow Pantheon. This setup enables her to handle inbound calls, interact with Devin via the Manus API, and trigger webhooks for seamless inter-agent communication.

## 1. Programmatic Agent Creation (Synthflow API)

Sarah will be created using the Synthflow API endpoint `POST https://api.synthflow.ai/v2/assistants`.

### Configuration Payload
```json
{
  "type": "inbound",
  "name": "Sarah - Car Brokerage Intelligence Officer",
  "description": "Inbound agent for Devin Car Brokerage. Handles initial seller inquiries, qualifies leads, and coordinates with Devin.",
  "phone_number": "+14375254343",
  "external_webhook_url": "https://devin-api.manus.im/v1/synthflow/webhook",
  "inbound_call_webhook_url": "https://devin-api.manus.im/v1/synthflow/inbound-call-webhook",
  "agent": {
    "prompt": "You are Sarah, a friendly and professional car brokerage agent working for Devin. Your primary goal is to qualify private car sellers in Lethbridge, AB, and gather essential vehicle information. You are aware that Devin sends initial Kijiji messages, so when a seller mentions 'your text,' acknowledge it and seamlessly transition into the qualification process. Be empathetic, persistent, and efficient in extracting details like year, make, model, mileage, condition, asking price, and seller's motivation. If the seller is 'hot' (e.g., ready to sell, open to negotiation, or has vital new information), fire a high-priority webhook to Devin. You have access to a custom action to send vehicle images via SMS.",
    "greeting_message": "Hello, this is Sarah calling for Devin. I believe you're calling about the text we sent regarding your vehicle. Do you have a moment to chat?",
    "llm": "gemini-2.5-flash",
    "language": "en-US",
    "voice_id": "eleven_turbo_v2"
  },
  "is_recording": true
}
```

## 2. Custom Actions for Sarah

### 2.1. Image Retrieval Action (`GET_VEHICLE_IMAGES`)
Allows Sarah to fetch vehicle image URLs from Devin's system during a call.
- **HTTP Mode:** `GET`
- **URL:** `https://devin-api.manus.im/v1/leads/{ad_id}/images`
- **Speech While Using Tool:** "Let me pull up those photos for you right now..."

### 2.2. In-Call SMS Action
Sarah will use the `INCALL_SMS` action to send the retrieved image URLs to the caller.

## 3. Webhook Integration
- **Real-time Notifications:** Immediate alerts when an inbound call starts.
- **Post-Call Data:** Full call transcript and structured data extraction.

## 4. Manus API for Sarah (Future Integration)
Giving Sarah access to the Manus API (via `https://api.manus.ai`) allows her to:
- **Create tasks for Devin:** `POST /v2/tasks`
- **Update Pantheon files:** `PUT /v2/files`

## 5. Next Steps
1. **Confirm Synthflow API Key:** Already stored in `config/credentials.json`.
2. **Implement Webhook Listener:** Create the endpoint for Sarah to report back to.
3. **Execute Creation Script:** Automate the creation of Sarah via API.
