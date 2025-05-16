from datetime import datetime

from flask import jsonify

# from constant import STATUS_CREATED
from daos.caregiver_dao import CaregiverDAO
# from daos.status_dao import StatusDAO
from db import Session


class Caregiver:
    @staticmethod
    def create(body):
        session = Session()
        caregiver = CaregiverDAO(body['caregiver_id'], body['name'], body['emailaddress'], body['password'], body['hobbies'])
        session.add(caregiver)
        session.commit()
        session.refresh(caregiver)
        session.close()
        return jsonify({'caregiver_id': caregiver.caregiver_id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        caregiver = session.query(CaregiverDAO).filter(CaregiverDAO.caregiver_id == d_id).first()

        if caregiver:
            text_out = {
                "caregiver_id:": caregiver.caregiver_id,
                "name": caregiver.name,
                "emailaddress": caregiver.emailaddress,
                "password": caregiver.password,
                "hobbies": caregiver.hobbies,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no caregiver with id {d_id}'}), 404

    #Onno: I changed the id's to caregiver_id, renamed the DAO to CaregiverDAO and added a delete function to app.py
    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(CaregiverDAO).filter(CaregiverDAO.caregiver_id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no caregiver with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The caregiver was removed'}), 200
