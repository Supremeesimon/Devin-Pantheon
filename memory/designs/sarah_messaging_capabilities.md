# Sarah's Messaging Capabilities: SMS & In-Call Messaging

## 1. Overview
Sarah, our "Intelligence Officer," is equipped with advanced messaging capabilities that allow her to send images and information to sellers and buyers via SMS and in-call messaging. This multi-channel approach ensures efficient communication and a seamless deal-making process.

## 2. Image Access and Storage
To ensure Sarah has the "visual ammo" she needs, I've updated my Kijiji scraping logic to automatically download and store all vehicle images for every lead I find. These images are stored in our GitHub Pantheon repository, organized by ad ID.

**Image Storage Structure:**
```
/home/ubuntu/Devin-Pantheon/memory/images/
  ad_id_1/
    image_0.jpg
    image_1.jpg
  ad_id_2/
    image_0.jpg
```

## 3. Sending Images via SMS and In-Call Messaging

### 3.1. In-Call Messaging (The "Live" Bridge)
Sarah can send an SMS message while she's still on the phone with a seller or buyer. This is particularly useful for sending vehicle photos or a link to a vehicle report in real-time.

**How it works:**
1.  **Trigger:** During a call, a buyer asks for photos of the vehicle.
2.  **Action:** Sarah triggers a Synthflow "In-Call Messaging" action.
3.  **Image Retrieval:** I've configured a Custom Action that retrieves the stored image URLs from our GitHub Pantheon for the specific vehicle being discussed.
4.  **Message Delivery:** Sarah sends the image URLs or a link to a gallery via SMS to the buyer's phone number.
5.  **Feedback Loop:** If the buyer replies to the SMS during the call, Sarah can "see" the reply and feed it back into the conversation.

### 3.2. Automated SMS (The "Follow-Up")
Sarah can also be configured to send automated SMS messages immediately after a call ends. This is useful for providing a written record of the next steps or sending additional information.

**How it works:**
1.  **Trigger:** A call with a seller or buyer ends.
2.  **Action:** Sarah triggers a Synthflow "Send SMS" action.
3.  **Message Delivery:** Sarah sends a pre-scripted SMS message to the person's phone number, including any relevant links or information.

## 4. Scheduling and Prospect Gathering
I'll be on a regular schedule to gather prospects and download their vehicle images for Sarah. This ensures she always has the latest information and "visual ammo" ready for her calls.

**My Schedule:**
*   **Wake:** I'll "Wake" up every 4 hours (or as needed) to scrape Kijiji for new listings in Lethbridge, AB.
*   **Sync:** I'll synchronize with our GitHub Pantheon to retrieve the latest seller records and image data.
*   **Act:** I'll scrape Kijiji, identify new leads, download their images, and update our seller records.
*   **Sleep:** I'll update our GitHub Pantheon with the new leads and images, and then "Sleep" until the next scheduled run.

This automated schedule ensures that Sarah is always equipped with the most up-to-date information and "visual ammo" to effectively manage her role as our Intelligence Officer.
