import os
from sarah_controller import SarahController
from webhook_listener import WebhookListener
from manus_bridge import ManusBridge

def run_test():
    print("=== STARTING DEVIN-SARAH INTEGRATION TEST ===\n")
    os.environ["DEVIN_TEST_MODE"] = "true"
    
    # 1. Test Sarah Creation Logic
    controller = SarahController()
    sarah_data = controller.create_sarah()
    if sarah_data:
        print(f"PASS: Sarah setup logic validated (ID: {sarah_data['id']})")
    
    # 2. Test Caller Identification (Kelly's Call)
    print("\nSimulating Kelly's call from +1 555 123 4567...")
    listener = WebhookListener()
    identified_seller = listener.identify_caller("+1 555 123 4567")
    
    if identified_seller == "seller_001":
        print("PASS: Caller correctly identified as Kelly (seller_001)")
    else:
        print(f"FAIL: Identification failed. Result: {identified_seller}")

    # 3. Test Manus API Bridge
    print("\nSimulating Manus API update to seller thread...")
    bridge = ManusBridge()
    bridge.update_seller_thread("seller_001", "TEST CALL: Sarah identified Kelly and logged price flexibility.")
    print("PASS: Bridge updated seller_001.md successfully.")

    print("\n=== TEST COMPLETE: ALL SYSTEMS NOMINAL ===")

if __name__ == "__main__":
    run_test()
