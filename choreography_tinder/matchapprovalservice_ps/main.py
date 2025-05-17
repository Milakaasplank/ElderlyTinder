from pub_sub_util import create_topic, publish_message
from resources.caregiver import Caregiver
import time
import uuid
import json

PROJECT_ID = "ada2025-450118" 
TOPIC_NAME = "NotifyCaregiverOfMatch"

match_counter = 1

def get_next_match_id():
    global match_counter
    match_id = f"match_{match_counter:03d}"
    match_counter += 1
    return match_id

def simulate_match_creation():
    cg = Caregiver().get_random()
    match_id = get_next_match_id()
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

    # Example: simulate 3 matches in one run
    for _ in range(3):
        simulate_match_creation()
        time.sleep(1)

