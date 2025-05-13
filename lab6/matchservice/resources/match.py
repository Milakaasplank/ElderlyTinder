from flask import Blueprint, request, jsonify
from db import Session
from daos.match_dao import Match
import random

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/match', methods=['POST'])
def create_match():
    data = request.get_json()
    elderly_id = data.get("elderly_id")
    match_date = data.get("match_date")

    if not elderly_id or not match_date:
        return jsonify({"error": "elderly_id and match_date required"}), 400

    # Simulate selecting random caregiver ID from dataset
    caregiver_id = f"CG{str(random.randint(1, 10)).zfill(3)}"
    match_id = f"M{str(random.randint(100, 999))}"  # Simulated match ID

    new_match = Match(
        match_id=match_id,
        elderly_id=elderly_id,
        caregiver_id=caregiver_id,
        match_date=match_date,
        status_elderly_user="Waiting",
        status_caregiver="Waiting"
    )

    session = Session()
    session.add(new_match)
    session.commit()
    session.close()

    return jsonify({
        "message": "Match created",
        "match_id": match_id,
        "elderly_id": elderly_id,
        "caregiver_id": caregiver_id
    })

@match_bp.route('/match/<match_id>', methods=['GET'])
def get_match(match_id):
    session = Session()
    match = session.query(Match).filter_by(match_id=match_id).first()
    session.close()
    if not match:
        return jsonify({"error": "Match not found"}), 404
    return jsonify({
        "match_id": match.match_id,
        "elderly_id": match.elderly_id,
        "caregiver_id": match.caregiver_id,
        "match_date": match.match_date,
        "status_elderly_user": match.status_elderly_user,
        "status_caregiver": match.status_caregiver
    })
