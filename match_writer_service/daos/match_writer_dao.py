
from sqlalchemy import Column, Integer, String
from db import SessionLocal, Base

class ApprovedMatch(Base):
    __tablename__ = 'approved_matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(String, nullable=False)
    caregiver_id = Column(String, nullable=False)
    elderly_id = Column(String, nullable=False)

class MatchWriterDAO:
    def write_match(self, match_data):
        session = SessionLocal()
        try:
            match = ApprovedMatch(
                match_id=match_data["match_id"],
                caregiver_id=match_data["caregiver_id"],
                elderly_id=match_data["elderly_id"]
            )
            session.add(match)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
