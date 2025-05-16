from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

# from daos.status_dao import StatusDAO
from db import Base


class MatchDAO(Base):
    __tablename__ = 'match'
    match_id = Column(Integer, primary_key=True)  # Auto generated primary key
    elderly_id = Column(Integer, ForeignKey('elderly.elderly_id'))
    caregiver_id = Column(Integer, ForeignKey('caregiver.caregiver_id'))
    status_caregiver = Column(String, default="PENDING")
    status_elderly = Column(String, default="PENDING")

    def __init__(self, match_id, status_elderly, status_caregiver, elderly_id, caregiver_id):
        self.match_id = match_id
        self.elderly_id = elderly_id
        self.caregiver_id = caregiver_id
        self.status_elderly = status_elderly
        self.status_caregiver = status_caregiver

