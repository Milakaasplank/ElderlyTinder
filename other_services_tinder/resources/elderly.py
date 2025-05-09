from datetime import datetime

from flask import jsonify

# from constant import STATUS_CREATED
from daos.elderly_dao import ElderlyDAO
# from daos.status_dao import StatusDAO
from db import Session


class Elderly:
    @staticmethod
    def create(body):
        session = Session()
        elderly = ElderlyDAO(body['elderly_id'], body['name'], body['emailaddress'], body['password'])
        session.add(elderly)
        session.commit()
        session.refresh(elderly)
        session.close()
        return jsonify({'elderly_id': elderly.elderly_id}), 200

    # @staticmethod
    # def get(d_id):
    #     session = Session()
    #     # https://docs.sqlalchemy.org/en/14/orm/query.html
    #     # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
    #     elderly = session.query(ElderlyDAO).filter(ElderlyDAO.id == d_id).first()

    #     if elderly:
    #         status_obj = elderly.status
    #         text_out = {
    #             "elderly_id:": elderly.elderly_id,
    #             "name": elderly.name,
    #             "emailaddress": elderly.emailaddress,
    #             "order_time": elderly.order_time.isoformat(),
    #             "elderly_time": elderly.elderly_time.isoformat(),
    #             "status": {
    #                 "status": status_obj.status,
    #                 "last_update": status_obj.last_update.isoformat(),
    #             }
    #         }
    #         session.close()
    #         return jsonify(text_out), 200
    #     else:
    #         session.close()
    #         return jsonify({'message': f'There is no elderly with id {d_id}'}), 404

    # @staticmethod
    # def delete(d_id):
    #     session = Session()
    #     effected_rows = session.query(ElderlyDAO).filter(ElderlyDAO.id == d_id).delete()
    #     session.commit()
    #     session.close()
    #     if effected_rows == 0:
    #         return jsonify({'message': f'There is no elderly with id {d_id}'}), 404
    #     else:
    #         return jsonify({'message': 'The elderly was removed'}), 200
