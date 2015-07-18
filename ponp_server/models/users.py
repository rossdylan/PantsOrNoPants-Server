from sqlalchemy import Column, String, Integer, Float, relationship
from sqlalchemy_utils import PasswordType
from ponp_server.database import Base
from ponp_server.models.reports import assoc_table


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    lang = Column(String(10))
    username = Column(String(20))
    home_lat = Column(Float)
    home_lng = Column(Float)
    password = Column(PasswordType)
    apikey = Column(String(32))
    height = Column(Float)
    weight = Column(Float)
    reports = relationship("PCIReport", secondary=assoc_table)

    def __repr__(self):
        return "<User {0} {1:d}>".format(self.username, self.id)
