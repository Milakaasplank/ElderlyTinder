
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

    caregiver_accepts = random.choice([True, False])

    if caregiver_accepts:
        event = {
            "match_id": data["match_id"],
            "caregiver_id": data["caregiver_id"],
            "elderly_id": data["elderly_id"]
        }
        publish_message(PROJECT_ID, TOPIC_MATCH_APPROVED, json.dumps(event), event_type="CaregiverApproved")
    else:
        event = {
            "match_id": data["match_id"],
            "caregiver_id": data["caregiver_id"],
            "elderly_id": data["elderly_id"]
        }
        publish_message(PROJECT_ID, TOPIC_MATCH_REJECTED, json.dumps(event), event_type="CaregiverRejected")

    message.ack()


def handle_match_approved_by_caregiver(message):
    data = json.loads(message.data.decode("utf-8"))
    print(f"[MatchApprovedByCaregiver] {data}")

    # Simulate notifying elderly
    publish_message(PROJECT_ID, TOPIC_NOTIFY_ELDERLY, json.dumps(data), event_type="NotifyElderly")
    # Simulate elderly decision
    elderly_accepts = random.choice([True, False])


    if elderly_accepts:
        event = {
            "match_id": data["match_id"],
            "elderly_id": data["elderly_id"],
            "caregiver_id": data["caregiver_id"]
        }
        publish_message(PROJECT_ID, TOPIC_ELDERLY_APPROVED, json.dumps(event), event_type="ElderlyApproved")
    else:
        event = {
            "match_id": data["match_id"],
            "elderly_id": data["elderly_id"],
            "caregiver_id": data["caregiver_id"]
        }
        publish_message(PROJECT_ID, TOPIC_ELDERLY_REJECTED, json.dumps(event), event_type="ElderlyRejected")
        publish_message(PROJECT_ID, TOPIC_NOTIFY_CAREGIVER_REJECTED, json.dumps(event), event_type="NotifyCaregiverRejection")

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
