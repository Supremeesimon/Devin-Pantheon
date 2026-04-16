# Inter-Agent Communication: The "Live Bridge" Framework

## 1. Overview
This framework defines how Sarah (the Intelligence Officer) and Devin (the Architect) communicate in real-time to ensure a seamless flow from Kijiji lead to closed deal. It utilizes Synthflow's Custom Actions and Webhooks to create a "Live Bridge" between the voice agent and the autonomous backend.

## 2. Sarah's "Live" Image Retrieval (Custom Action)

When a buyer or seller asks for photos during a call, Sarah triggers a **Custom Action** to retrieve the image URLs from Devin's Pantheon.

### 2.1. Technical Workflow
1.  **Trigger:** Sarah identifies a request for images (e.g., "Can you send me photos of the car?").
2.  **API Call:** Sarah makes a `GET` request to Devin's endpoint:
    `GET https://devin-api.manus.im/v1/leads/{ad_id}/images`
3.  **Response:** Devin's API returns a JSON object with the image URLs:
    ```json
    {
      "ad_id": "1731517390",
      "image_urls": [
        "https://pantheon-storage.s3.amazonaws.com/1731517390/img1.jpg",
        "https://pantheon-storage.s3.amazonaws.com/1731517390/img2.jpg"
      ]
    }
    ```
4.  **In-Call Messaging:** Sarah uses the returned URLs to trigger an **In-Call Messaging** action, sending the links via SMS/WhatsApp to the caller instantly.

## 3. The "Wake-Up" Webhook (Sarah to Devin)

When Sarah identifies a "hot" seller or receives vital information, she fires a webhook to wake Devin up immediately.

### 3.1. Webhook Payload
Sarah's webhook is the "Command Signal" for Devin. It includes a `priority` flag and a `next_action_required` field.

```json
{
  "event": "call_completed",
  "priority": "high",
  "caller_info": {
    "phone": "+14036346282",
    "name": "Kelly"
  },
  "lead_intel": {
    "ad_id": "1731517390",
    "status": "ready_to_sell",
    "vital_info": "Price dropped to $18,500 for cash deal today.",
    "availability": "Available for viewing at 4 PM today."
  },
  "next_action_required": "spawn_outbound_buyer_call"
}
```

### 3.2. Devin's Response (The "Wake" Cycle)
1.  **Receive Webhook:** Devin's server receives the payload and triggers an immediate "Wake" cycle.
2.  **Analyze & Match:** Devin cross-references the `lead_intel` with his **Buyer's List** in the GitHub Pantheon.
3.  **Spawn Outbound Sarah:** Devin identifies the best buyer (e.g., "Lethbridge Toyota") and programmatically spawns an **Outbound Sarah** mission.

## 4. The Buyer's List (Devin's Database)

Devin maintains a persistent list of buyers to ensure he knows exactly who to call when a lead goes "hot."

| Buyer Name | Contact | Preferred Models | Max Buy Price | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Lethbridge Toyota | +1 403-320-1234 | RAV4, Tacoma, Corolla | $25,000 | Prefers low mileage, quick turnarounds. |
| Bridge City Chrysler | +1 403-329-4444 | RAM 1500, Jeep, SUVs | $40,000 | Looking for late-model trade-ins. |
| Cash For Cars AB | +1 800-555-0199 | Any (Scrap/Resale) | $5,000 | Good for older vehicles or high mileage. |

## 5. Summary of the "Live Bridge"
*   **Sarah** is the eyes and ears, gathering intel and sending images in real-time.
*   **The Webhook** is the nervous system, waking Devin up when action is needed.
*   **Devin** is the brain, matching sellers to buyers and spawning new missions.
*   **GitHub Pantheon** is the memory, storing every image, lead, and buyer preference.
