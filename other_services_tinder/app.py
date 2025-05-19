import os

from flask import Flask, request

from db import Base, engine
from resources.elderly import Elderly
from caregiver_services.resources.caregiver import Caregiver
from resources.match import Match
# from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/addelderly', methods=['POST'])
def create_elderly():
    req_data = request.get_json()
    return Elderly.create(req_data)

@app.route('/addcaregiver', methods=['POST'])
def create_caregiver():
    req_data = request.get_json()
    return Caregiver.create(req_data)

@app.route('/getelderly/<d_id>', methods=['GET'])
def get_elderly(d_id):
    return Elderly.get(d_id)

@app.route('/getcaregiver/<d_id>', methods=['GET'])
def get_caregiver(d_id):
    return Caregiver.get(d_id)

# --> Remove Elderly and Caregiver (by Onno), it says theres no delete function in Elderly and Caregiver but there definitely is.
@app.route('/elderly/<elderly_id>', methods=['DELETE'])
def delete_elderly(elderly_id):
    return Elderly.delete(elderly_id)

@app.route('/caregiver/<caregiver_id>', methods=['DELETE'])
def delete_caregiver(caregiver_id):
    return Caregiver.delete(caregiver_id)

@app.route("/match/random", methods=["POST"])
def create_random_match():
    return Match.create_random()

@app.route("/match/<int:match_id>/notify", methods=["POST"])
def notify_match(match_id):
    return Match.notify(match_id)

@app.route("/match/<int:match_id>/decide", methods=["POST"])
def decide_match(match_id):
    body = request.get_json()
    return Match.decide_caregiver(match_id, body)

@app.route("/match/<int:match_id>/reject", methods=["POST"])
def reject_match(match_id):
    return Match.reject(match_id)

@app.route("/match/<int:match_id>/accept", methods=["POST"])
def accept_match(match_id):
    return Match.accept_caregiver(match_id)

@app.route("/match/<int:match_id>/notify_elderly", methods=["POST"])
def notify_elderly(match_id):
    return Match.notify_elderly(match_id)

@app.route("/match/<int:match_id>/elderly_accept", methods=["POST"])
def elderly_accept(match_id):
    return Match.elderly_accept(match_id)

@app.route("/match/<int:match_id>/elderly_reject", methods=["POST"])
def elderly_reject(match_id):
    return Match.elderly_reject(match_id)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
