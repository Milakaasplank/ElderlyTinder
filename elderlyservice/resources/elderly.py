from datetime import datetime

from flask import jsonify

# from constant import STATUS_CREATED
from daos.elderly_dao import ElderlyDAO
# from daos.status_dao import StatusDAO
from db import Session

# We import this to make it adhere to the FaaS structure
from elderly_service import get_elderly_user

class Elderly:
    @staticmethod
    def create(body):
        session = Session()
        elderly = ElderlyDAO(body['elderly_id'], body['name'], body['emailaddress'], body['password'], body['hobbies'])
        session.add(elderly)
        session.commit()
        session.refresh(elderly)
        session.close()
        return jsonify({'elderly_id': elderly.elderly_id}), 200
    
    # Onno: Code from here to line 28 is used to convert 'get' to FaaS
    @staticmethod
    def get(d_id):
    response, status_code = get_elderly_user(d_id)
    return jsonify(response), status_code

    #Onno: Old get method, commented since we wanted to change it to FaaS 

    # @staticmethod
    # def get(d_id):
    #     session = Session()
    #     # https://docs.sqlalchemy.org/en/14/orm/query.html
    #     # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
    #     elderly = session.query(ElderlyDAO).filter(ElderlyDAO.elderly_id == d_id).first()

    #     if elderly:
    #         text_out = {
    #             "elderly_id:": elderly.elderly_id,
    #             "name": elderly.name,
    #             "emailaddress": elderly.emailaddress,
    #             "password": elderly.password,
    #             "hobbies": elderly.hobbies,
    #         }
    #         session.close()
    #         return jsonify(text_out), 200
    #     else:
    #         session.close()
    #         return jsonify({'message': f'There is no elderly with id {d_id}'}), 404


    #Onno: I changed the id's to elderly_id, renamed the DAO to ElderlyDAO and added a delete function to app.py
    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(ElderlyDAO).filter(ElderlyDAO.elderly_id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no elderly user with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The elderly user was removed'}), 200
