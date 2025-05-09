import logging
import os

import connexion

# do not remove these imports https://stackoverflow.com/questions/44941757/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table
from daos.address_dao import AddressDAO
from daos.place_dao import PlaceDAO

from db import Base, engine
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('place-service-api.yaml',
            arguments={'title': 'Place Service API'})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
