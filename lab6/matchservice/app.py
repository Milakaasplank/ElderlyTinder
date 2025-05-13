from flask import Flask
from resources.match import match_bp
from daos.match_dao import Base
from db import engine

app = Flask(__name__)
app.register_blueprint(match_bp)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(debug=True)
