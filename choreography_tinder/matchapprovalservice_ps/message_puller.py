
import json
import logging
import random
from google.cloud import pubsub_v1
from pub_sub_util import publish_message

PROJECT_ID = "ada2025-450118"

# Topics
TOPIC_NOTIFY_CAREGIVER = "NotifyCaregiverOfMatch"
TOPIC_MATCH_APPROVED = "MatchApprovedByCaregiver"
TOPIC_MATCH_REJECTED = "MatchRejectedByCaregiver"
TOPIC_NOTIFY_ELDERLY = "NotifyElderlyUserOfMatch"
TOPIC_ELDERLY_APPROVED = "MatchApprovedByElderlyUser"
TOPIC_ELDERLY_REJECTED = "MatchRejectedByElderlyUser"
TOPIC_NOTIFY_CAREGIVER_REJECTED = "NotifyCaregiverOfRejection"

# Subscriptions
SUB_NOTIFY_CAREGIVER = "NotifyCaregiverOfMatch-sub"
SUB_APPROVED_BY_CAREGIVER = "MatchApprovedByCaregiver-sub"


def handle_notify_caregiver(message):
    data = json.loads(message.data.decode("utf-8"))
    print(f"[NotifyCaregiverOfMatch] {data}")
    caregiver_accepts = random.choices([True, False], weights=[0.9, 0.3])[0]
    if caregiver_accepts:
        event = {
            "match_id": data["match_id"],
            "caregiver_id": data["caregiver_id"],
            "elderly_id": data["elderly_id"]
        }
        event_text = f"[MatchApprovedByCaregiver] {event}"
        publish_message(PROJECT_ID, TOPIC_MATCH_APPROVED, event_text, event_type="CaregiverApproved")
    else:
        event = {
            "match_id": data["match_id"],
            "caregiver_id": data["caregiver_id"],
            "elderly_id": data["elderly_id"]
        }
        publish_message(PROJECT_ID, TOPIC_MATCH_REJECTED, json.dumps(event), event_type="CaregiverRejected")

    message.ack()


def handle_match_approved_by_caregiver(message):
    raw = message.data.decode("utf-8")
    print(f"🟡 Raw message: {raw}", flush=True)

    if "[MatchApprovedByCaregiver]" not in raw:
        print("⚠️ Unexpected message format", flush=True)
        message.ack()
        return

    try:
        # Extract and parse dictionary portion after the tag
        payload_str = raw.split("]")[-1].strip()
        data = eval(payload_str)  # ⚠️ safe only in controlled environments
        print(f"[MatchApprovedByCaregiver] {data}", flush=True)
    except Exception as e:
        print(f"❌ Failed to parse tagged message: {e}", flush=True)
        message.ack()
        return

    # Simulate notifying elderly
    publish_message(PROJECT_ID, TOPIC_NOTIFY_ELDERLY, json.dumps(data), event_type="NotifyElderly")

    # Simulate elderly decision (95% accept, 5% reject)
    elderly_accepts = random.choices([True, False], weights=[0.95, 0.05])[0]

    # Continue with the rest of your logic here...
    message.ack()



def start():
    subscriber = pubsub_v1.SubscriberClient()

    # Subscription paths
    sub_paths = {
        SUB_NOTIFY_CAREGIVER: handle_notify_caregiver,
        SUB_APPROVED_BY_CAREGIVER: handle_match_approved_by_caregiver
    }

    # Start listening to both
    for sub, callback in sub_paths.items():
        sub_path = subscriber.subscription_path(PROJECT_ID, sub)
        subscriber.subscribe(sub_path, callback=callback)
        print(f"Listening on {sub_path}...")

    print("Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    start()
