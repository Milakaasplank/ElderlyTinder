import os

from flask import Flask, request

from db import Base, engine
from resources.elderly import Elderly
from resources.caregiver import Caregiver
from resources.match import Match
# from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/addelderly', methods=['POST'])
def create_elderly():
    req_data = request.get_json()
    return Elderly.create(req_data)

@app.route('/getelderly/<d_id>', methods=['GET'])
def get_elderly(d_id):
    return Elderly.get(d_id)

@app.route('/elderly/<elderly_id>', methods=['DELETE'])
def delete_elderly(elderly_id):
    return Elderly.delete(elderly_id)
    

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
