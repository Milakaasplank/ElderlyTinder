# choreography/matchapprovalservice_ps/resources/caregiver.py

import random

caregivers = [
    {
        "caregiver_id": "CG001",
        "name": "Jennifer Lee",
        "email": "jennifer.lee@example.com"
    },
    {
        "caregiver_id": "CG002",
        "name": "Michael Harris",
        "email": "michael.harris@example.com"
    },
    {
        "caregiver_id": "CG003",
        "name": "Priya Nair",
        "email": "priya.nair@example.com"
    }
]


class Caregiver:
    def get_random(self):
        return random.choice(caregivers)

    def get_all(self):
        return caregivers
