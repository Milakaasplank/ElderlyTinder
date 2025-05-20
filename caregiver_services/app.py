import os

from flask import Flask, request

from db import Base, engine
from resources.elderly import Elderly
from caregiver_services.resources.caregiver import Caregiver
from resources.match import Match
from resources.caregiver import Caregiver
# from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/addcaregiver', methods=['POST'])
def create_caregiver():
    req_data = request.get_json()
    return Caregiver.create(req_data)

@app.route('/getcaregiver/<d_id>', methods=['GET'])
def get_caregiver(d_id):
    return Caregiver.get(d_id)

@app.route('/caregiver/<caregiver_id>', methods=['DELETE'])
def delete_caregiver(caregiver_id):
    return Caregiver.delete(caregiver_id)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
