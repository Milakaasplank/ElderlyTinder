from db import Base, engine
from daos.match_writer_dao import ApprovedMatch

def init_db():
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized.")

if __name__ == "__main__":
    init_db()
