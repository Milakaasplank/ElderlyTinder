from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = 'elderly_matches'
    match_id = Column(String, primary_key=True) 
    elderly_id = Column(String, nullable=False)
    caregiver_id = Column(String, nullable=False)
    match_date = Column(TIMESTAMP, nullable=False)
    status_elderly_user = Column(String, default="Waiting")
    status_caregiver = Column(String, default="Waiting")