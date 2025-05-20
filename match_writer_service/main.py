import os
import json
from google.cloud import pubsub_v1
from daos.match_writer_dao import MatchWriterDAO

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "matchapprovaldemo")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME", "MatchApprovedByCaregiver-sub")

print(f"Using PROJECT_ID: {PROJECT_ID}", flush=True)
print(f"Using SUBSCRIPTION_NAME: {SUBSCRIPTION_NAME}", flush=True)

def callback(message):
    try:
        data = message.data.decode("utf-8")
        print(f"📨 Received message: {data}", flush=True)
        if "[MatchApprovedByCaregiver]" not in data:
            print("⚠️ Unsupported message type.", flush=True)
            message.ack()
            return

        payload_str = data.split("]")[-1].strip()
        payload = eval(payload_str)
        dao = MatchWriterDAO()
        dao.write_match(payload)
        print(f"✅ Match {payload['match_id']} written to DB.", flush=True)
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
    finally:
        message.ack()

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    subscriber.subscribe(subscription_path, callback=callback)
    print(f"🟢 Listening to Pub/Sub subscription: {subscription_path}", flush=True)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("🔴 Stopped.", flush=True)

if __name__ == "__main__":
    main()
