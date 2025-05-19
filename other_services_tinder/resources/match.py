from datetime import datetime

from flask import jsonify
from sqlalchemy.sql.expression import func
# from constant import STATUS_CREATED
from daos.match_dao import MatchDAO
from daos.elderly_dao import ElderlyDAO
from daos.caregiver_dao import CaregiverDAO
# from daos.status_dao import StatusDAO
from db import Session


class Match:
    @staticmethod
    def create(body):
        session = Session()
        match = MatchDAO(body['match_id'], body['status'])
        session.add(match)
        session.commit()
        session.refresh(match)
        session.close()
        return jsonify({'match_id': match.match_id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        match = session.query(MatchDAO).filter(MatchDAO.match_id == d_id).first()

        if match:
            text_out = {
                "match_id:": match.match_id,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no match with id {d_id}'}), 404

    #Onno: I changed the id's to match_id, renamed the DAO to matchDAO and added a delete function to app.py
    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(MatchDAO).filter(MatchDAO.match_id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no match with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The match was removed'}), 200

    @staticmethod
    def create_random():
        session = Session()

        elderly = session.query(ElderlyDAO).order_by(func.random()).first()
        caregiver = session.query(CaregiverDAO).order_by(func.random()).first()

        if not elderly or not caregiver:
            session.close()
            return jsonify({"message": "Not enough data to create a match"}), 400

        match = MatchDAO(elderly.elderly_id, caregiver.caregiver_id, status_caregiver="CREATED")
        session.add(match)
        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            "match_id": match.match_id,
            "elderly_id": match.elderly_id,
            "caregiver_id": match.caregiver_id,
            "status_elderly": match.status_elderly,
            "status_caregiver": match.status_caregiver,
        }), 200
    
    @staticmethod
    def notify(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        caregiver = session.query(CaregiverDAO).filter(CaregiverDAO.id == match.caregiver_id).first()
        elderly = session.query(ElderlyDAO).filter(ElderlyDAO.id == match.elderly_id).first()

        if not caregiver or not elderly:
            session.close()
            return jsonify({'message': 'Caregiver or elderly person not found'}), 404

        # "Notify" the caregiver (log/print for now)
        print(f"[NOTIFY] Caregiver {caregiver.name} matched with Elderly {elderly.name}")

        session.close()
        return jsonify({
            'message': f'Caregiver {caregiver.name} notified about match with {elderly.name}'
        }), 200
    
    @staticmethod
    def decide_caregiver(match_id, body):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        decision = body.get("decision")
        if decision is None:
            session.close()
            return jsonify({'message': 'Missing "decision" in request body (true/false)'}), 400

        # Set status based on decision
        if decision is True:
            match.status_caregiver = "ACCEPTED"
        elif decision is False:
            match.status_caregiver = "DECLINED"
        else:
            session.close()
            return jsonify({'message': 'Decision must be true or false'}), 400

        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Match {match.match_id} has been {"accepted" if decision else "declined"}',
            'status': match.status_caregiver
        }), 200
    
    @staticmethod
    def reject(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        match.status_caregiver = "REJECTED"
        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Match {match.match_id} has been rejected',
            'status': match.status_caregiver
        }), 200

    @staticmethod
    def accept_caregiver(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        match.status_caregiver = "ACCEPTED"
        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Match {match.match_id} has been accepted',
            'status': match.status_caregiver
        }), 200

    @staticmethod
    def notify_elderly(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        from daos.elderly_dao import ElderlyDAO
        from daos.caregiver_dao import CaregiverDAO

        elderly = session.query(ElderlyDAO).filter(ElderlyDAO.id == match.elderly_id).first()
        caregiver = session.query(CaregiverDAO).filter(CaregiverDAO.id == match.caregiver_id).first()

        if not elderly or not caregiver:
            session.close()
            return jsonify({'message': 'Elderly or caregiver not found'}), 404

        # Update status_elderly
        match.status_elderly = "NOTIFIED"
        session.commit()

        print(f"[NOTIFY] Elderly {elderly.name} notified of match with caregiver {caregiver.name}")

        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Elderly {elderly.name} notified about match',
            'status_elderly': match.status_elderly
        }), 200
    
    @staticmethod
    def elderly_accept(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        match.status_elderly = "ACCEPTED"
        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Elderly has accepted match {match.match_id}',
            'status_elderly': match.status_elderly
        }), 200


    @staticmethod
    def elderly_reject(match_id):
        session = Session()

        match = session.query(MatchDAO).filter(MatchDAO.match_id == match_id).first()
        if not match:
            session.close()
            return jsonify({'message': f'Match {match_id} not found'}), 404

        match.status_elderly = "REJECTED"
        session.commit()
        session.refresh(match)
        session.close()

        return jsonify({
            'message': f'Elderly has rejected match {match.match_id}',
            'status_elderly': match.status_elderly
        }), 200



