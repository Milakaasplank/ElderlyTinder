from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

# from daos.status_dao import StatusDAO
from db import Base


class ElderlyDAO(Base):
    __tablename__ = 'elderly'
    elderly_id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String)
    emailaddress = Column(String)
    password = Column(String)
    # reference to status as foreign key relationship. This will be automatically assigned.
    # status_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    # status = relationship(StatusDAO.__name__, backref=backref("elderly", uselist=False))

    def __init__(self, elderly_id, name, emailaddress, password):
        self.elderly_id = elderly_id
        self.name = name
        self.emailaddress = emailaddress
        # self.order_time = order_time
        self.password = password
        # self.status = status
