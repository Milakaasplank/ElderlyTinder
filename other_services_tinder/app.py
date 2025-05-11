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

# @app.route('/deliveries/<d_id>', methods=['GET'])
# def get_elderly(d_id):
#     return Elderly.get(d_id)


# @app.route('/deliveries/<d_id>/status', methods=['PUT'])
# def update_elderly_status(d_id):
#     status = request.args.get('status')
#     return Status.update(d_id, status)


# @app.route('/deliveries/<d_id>', methods=['DELETE'])
# def delete_elderly(d_id):
#     return Elderly.delete(d_id)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
