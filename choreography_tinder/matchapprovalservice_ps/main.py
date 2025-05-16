from pub_sub_util import create_topic, publish_message
from resources.caregiver import Caregiver
import time
import uuid
import json

PROJECT_ID = "ada2025-450118" 
TOPIC_NAME = "NotifyCaregiverOfMatch"

def simulate_match_creation():
    cg = Caregiver().get_random()
    match_id = str(uuid.uuid4())
    message = {
        "match_id": match_id,
        "elderly_id": "EU001",
        "caregiver_id": cg["caregiver_id"],
        "caregiver_name": cg["name"]
    }

    print(f"Simulating match creation: {message}")
    publish_message(PROJECT_ID, TOPIC_NAME, json.dumps(message), event_type="MatchCreated")


if __name__ == "__main__":
    create_topic(PROJECT_ID, TOPIC_NAME)
    simulate_match_creation()
    time.sleep(2)

