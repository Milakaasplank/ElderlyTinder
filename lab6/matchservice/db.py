from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual DB credentials/environment vars
DATABASE_URI = "postgresql://user:password@host:port/dbname"

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
