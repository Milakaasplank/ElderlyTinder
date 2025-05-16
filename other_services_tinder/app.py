import os

from flask import Flask, request

from db import Base, engine
from resources.elderly import Elderly
from resources.caregiver import Caregiver
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

# TODO: i think we can use this to update the hobbies of the elderly: Jessie
# @app.route('/deliveries/<d_id>/status', methods=['PUT'])
# def update_elderly_status(d_id):
#     status = request.args.get('status')
#     return Status.update(d_id, status)

# TODO: i think we can use this to update the hobbies of the elderly: Aurelia
# @app.route('/deliveries/<d_id>/status', methods=['PUT'])
# def update_elderly_status(d_id):
#     status = request.args.get('status')
#     return Status.update(d_id, status)


# --> Remove Elderly and Caregiver (by Onno), it says theres no delete function in Elderly and Caregiver but there definitely is.
@app.route('/elderly/<elderly_id>', methods=['DELETE'])
def delete_elderly(elderly_id):
    return Elderly.delete(elderly_id)

@app.route('/caregiver/<caregiver_id>', methods=['DELETE'])
def delete_caregiver(caregiver_id):
    return Caregiver.delete(caregiver_id)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
