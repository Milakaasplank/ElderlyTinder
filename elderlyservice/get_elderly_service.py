# Onno: Code to here is used to convert 'get' to FaaS
from db import Session
from daos.elderly_dao import ElderlyDAO

def get_elderly_user(elderly_id):
    session = Session()
    elderly = session.query(ElderlyDAO).filter(ElderlyDAO.elderly_id == elderly_id).first()
    session.close()

    if elderly:
        return {
            "elderly_id": elderly.elderly_id,
            "name": elderly.name,
            "emailaddress": elderly.emailaddress,
            "password": elderly.password,
            "hobbies": elderly.hobbies
        }, 200
    else:
        return {'message': f'There is no elderly with id {elderly_id}'}, 404
